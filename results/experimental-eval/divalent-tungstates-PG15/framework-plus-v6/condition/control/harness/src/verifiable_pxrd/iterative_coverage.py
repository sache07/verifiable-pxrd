"""Alternating blind review and fresh continuation for pXRD solver attempts."""

from __future__ import annotations

import concurrent.futures
import dataclasses
import hashlib
import shutil
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .benchmark import Problem, load_problem_collection
from .condition import Condition, load_condition
from .coverage import (
    FirstPassAttempt,
    _copy_trace,
    _prepare_agent_home,
    _run_agent,
    _source_attempts,
)
from .llm_verifier import render_review_prompt, validate_decision
from .matching import declared_candidates, evaluate_candidates
from .run import _remove_auth_links, doctor, now
from .util import load_json, sha256_file, sha256_tree, write_json


@dataclass(frozen=True, slots=True)
class Snapshot:
    """One immutable solver output that can be reviewed or continued."""

    label: str
    root: Path
    trace: Path
    final_response: Path
    candidates: tuple[Path, ...]


def _manifest_path(path: Path) -> Path:
    path = path.resolve()
    return path / "manifest.json" if path.is_dir() else path


def render_continuation_prompt(
    template: str,
    condition: Condition,
    problem: Problem,
    evidence: Path,
    decision_path: Path,
    candidates: tuple[Path, ...],
) -> str:
    candidate_text = "\n".join(f"- {path}" for path in candidates) or "- None submitted"
    capability = evidence.parent / "workspace/.vpbench-capability/SKILL.md"
    if condition.capability is None:
        raise ValueError("continuation condition requires a capability package")
    values = {
        "capability_path": str(capability),
        "formula": problem.formula,
        "pattern_path": str(evidence / "pattern.csv"),
        "wavelength": f"{problem.wavelength} angstrom ({problem.radiation})",
        "first_trace_path": str(evidence / "first-pass-trace.jsonl"),
        "first_response_path": str(evidence / "first-pass-final.md"),
        "first_pass_cifs": candidate_text,
        "decision_json_path": str(decision_path),
    }
    prompt = template
    for key, value in values.items():
        prompt = prompt.replace("{" + key + "}", value)
    unresolved = [key for key in values if "{" + key + "}" in prompt]
    if unresolved:
        raise ValueError(f"unresolved continuation prompt fields: {unresolved}")
    return prompt.rstrip() + "\n"


def _copy_snapshot(
    destination: Path,
    problem: Problem,
    source: FirstPassAttempt,
) -> Snapshot:
    submitted = destination / "submitted"
    submitted.mkdir(parents=True)
    shutil.copy2(problem.pattern, destination / "pattern.csv")
    _copy_trace(source.trace, destination / "trace.jsonl")
    final_response = destination / "final-response.md"
    if source.final_response is not None:
        shutil.copy2(source.final_response, final_response)
    else:
        final_response.write_text(
            "No final response was captured for this attempt.\n", encoding="utf-8"
        )
    records = []
    for candidate in source.candidates:
        output = submitted / candidate.name
        shutil.copy2(candidate, output)
        records.append({"file": output.name, "sha256": sha256_file(output)})
    write_json(
        destination / "manifest.json",
        {
            "schema_version": "iterative-snapshot-v1",
            "label": "initial",
            "origin": str(source.root),
            "pattern_sha256": sha256_file(destination / "pattern.csv"),
            "trace_sha256": sha256_file(destination / "trace.jsonl"),
            "final_response_sha256": sha256_file(final_response),
            "candidates": records,
        },
    )
    return Snapshot(
        label="initial",
        root=destination,
        trace=destination / "trace.jsonl",
        final_response=final_response,
        candidates=tuple(declared_candidates(submitted)),
    )


def _stage_case(
    run_root: Path,
    problem: Problem,
    source: FirstPassAttempt,
    judge_condition: Condition,
    solver_condition: Condition,
) -> tuple[Path, Snapshot]:
    attempt = run_root / "attempts" / problem.problem_id
    if attempt.exists():
        raise FileExistsError(attempt)
    control = attempt / "control"
    control.mkdir(parents=True)
    shutil.copy2(problem.reference, control / "reference.cif")
    initial = _copy_snapshot(attempt / "initial", problem, source)
    write_json(
        control / "assignment.json",
        {
            "problem_id": problem.problem_id,
            "formula": problem.formula,
            "reference": "reference.cif",
            "reference_sha256": sha256_file(problem.reference),
            "pattern_sha256": sha256_file(problem.pattern),
            "source_attempt": str(source.root),
            "source_manifest_sha256": sha256_file(initial.root / "manifest.json"),
            "judge_condition": judge_condition.condition_id,
            "solver_condition": solver_condition.condition_id,
        },
    )
    return attempt, initial


def _copy_review_evidence(problem: Problem, snapshot: Snapshot, evidence: Path) -> tuple[Path, ...]:
    evidence.mkdir(parents=True)
    shutil.copy2(problem.pattern, evidence / "pattern.csv")
    _copy_trace(snapshot.trace, evidence / "first-pass-trace.jsonl")
    shutil.copy2(snapshot.final_response, evidence / "first-pass-final.md")
    candidates = []
    for candidate in snapshot.candidates:
        output = evidence / candidate.name
        shutil.copy2(candidate, output)
        candidates.append(output)
    write_json(
        evidence / "comparable-rwp-report.json",
        {"available": False, "reason": "not supplied"},
    )
    return tuple(candidates)


def _stage_review(
    attempt: Path,
    judge_condition: Condition,
    problem: Problem,
    snapshot: Snapshot,
    review_index: int,
    wrapper: str,
    policy: str,
) -> tuple[Path, Path, Path, str]:
    stage = attempt / "rounds" / f"review-{review_index:02d}"
    evidence = stage / "evidence"
    workspace = stage / "workspace"
    codex_home = stage / "codex-home"
    run_dir = stage / "run"
    run_dir.mkdir(parents=True)
    candidates = _copy_review_evidence(problem, snapshot, evidence)
    prompt = render_review_prompt(wrapper, policy, problem, evidence, candidates)
    (stage / "prompt.md").write_text(prompt, encoding="utf-8")
    _prepare_agent_home(judge_condition, workspace, codex_home, (evidence,))
    write_json(
        stage / "input.json",
        {
            "schema_version": "iterative-review-input-v1",
            "review_index": review_index,
            "snapshot": snapshot.label,
            "snapshot_manifest_sha256": sha256_file(snapshot.root / "manifest.json"),
            "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        },
    )
    return workspace, codex_home, run_dir, prompt


def _archive_review(stage: Path) -> dict[str, Any]:
    decision = validate_decision(stage / "workspace/decision.json")
    write_json(stage / "decision.json", decision)
    return decision


def _copy_continuation_evidence(
    problem: Problem,
    snapshot: Snapshot,
    decision_path: Path,
    evidence: Path,
) -> tuple[tuple[Path, ...], Path]:
    submitted = evidence / "first-pass-cifs"
    submitted.mkdir(parents=True)
    shutil.copy2(problem.pattern, evidence / "pattern.csv")
    _copy_trace(snapshot.trace, evidence / "first-pass-trace.jsonl")
    shutil.copy2(snapshot.final_response, evidence / "first-pass-final.md")
    candidates = []
    for candidate in snapshot.candidates:
        output = submitted / candidate.name
        shutil.copy2(candidate, output)
        candidates.append(output)
    copied_decision = evidence / "decision.json"
    shutil.copy2(decision_path, copied_decision)
    return tuple(candidates), copied_decision


def _stage_continuation(
    attempt: Path,
    solver_condition: Condition,
    problem: Problem,
    snapshot: Snapshot,
    continuation_index: int,
    decision_path: Path,
    template: str,
) -> tuple[Path, Path, Path, str]:
    stage = attempt / "rounds" / f"continuation-{continuation_index:02d}"
    evidence = stage / "evidence"
    workspace = stage / "workspace"
    codex_home = stage / "codex-home"
    run_dir = stage / "run"
    run_dir.mkdir(parents=True)
    candidates, copied_decision = _copy_continuation_evidence(
        problem, snapshot, decision_path, evidence
    )
    _prepare_agent_home(solver_condition, workspace, codex_home, (evidence,))
    prompt = render_continuation_prompt(
        template,
        solver_condition,
        problem,
        evidence,
        copied_decision,
        candidates,
    )
    (stage / "prompt.md").write_text(prompt, encoding="utf-8")
    write_json(
        stage / "input.json",
        {
            "schema_version": "iterative-continuation-input-v1",
            "continuation_index": continuation_index,
            "previous_snapshot": snapshot.label,
            "previous_snapshot_manifest_sha256": sha256_file(snapshot.root / "manifest.json"),
            "decision_sha256": sha256_file(copied_decision),
            "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        },
    )
    return workspace, codex_home, run_dir, prompt


def _archive_continuation(stage: Path, continuation_index: int) -> Snapshot:
    workspace = stage / "workspace"
    candidates = tuple(declared_candidates(workspace))
    if not candidates or candidates[0].name != "selected.cif":
        raise ValueError("continuation produced no canonical selected.cif")
    submitted = stage / "submitted"
    submitted.mkdir()
    records = []
    for candidate in candidates:
        output = submitted / candidate.name
        shutil.copy2(candidate, output)
        records.append({"file": output.name, "sha256": sha256_file(output)})
    trace = stage / "trace.jsonl"
    _copy_trace(stage / "run/codex-events.jsonl", trace)
    final_response = stage / "final-response.md"
    captured = stage / "run/final-answer.md"
    if captured.is_file():
        shutil.copy2(captured, final_response)
    else:
        final_response.write_text(
            "No final response was captured for this continuation.\n", encoding="utf-8"
        )
    write_json(
        stage / "manifest.json",
        {
            "schema_version": "iterative-snapshot-v1",
            "label": f"continuation-{continuation_index:02d}",
            "workspace_sha256": sha256_tree(workspace),
            "trace_sha256": sha256_file(trace),
            "final_response_sha256": sha256_file(final_response),
            "candidates": records,
        },
    )
    return Snapshot(
        label=f"continuation-{continuation_index:02d}",
        root=stage,
        trace=trace,
        final_response=final_response,
        candidates=tuple(declared_candidates(submitted)),
    )


def _materialize_final(
    attempt: Path,
    snapshot: Snapshot,
    termination: str,
    continuation_count: int,
    decisions: list[dict[str, Any]],
) -> dict[str, Any]:
    submission = attempt / "submission"
    submission.mkdir()
    records = []
    for candidate in snapshot.candidates:
        output = submission / candidate.name
        shutil.copy2(candidate, output)
        records.append({"file": output.name, "sha256": sha256_file(output)})
    manifest = {
        "schema_version": "iterative-submission-v1",
        "final_snapshot": snapshot.label,
        "termination": termination,
        "candidates": records,
    }
    write_json(submission / "manifest.json", manifest)
    write_json(
        attempt / "chain.json",
        {
            "schema_version": "iterative-chain-v1",
            "termination": termination,
            "final_snapshot": snapshot.label,
            "continuations": continuation_count,
            "reviews": decisions,
        },
    )
    return manifest


def _run_chain_attempt(
    run_root: Path,
    judge_condition: Condition,
    solver_condition: Condition,
    problem: Problem,
    source: FirstPassAttempt,
    wrapper: str,
    policy: str,
    continuation_template: str,
    max_continuations: int,
    judge_timeout: int,
    continuation_timeout: int,
    stage_update: Any,
) -> dict[str, Any]:
    attempt, current = _stage_case(
        run_root, problem, source, judge_condition, solver_condition
    )
    decisions: list[dict[str, Any]] = []
    continuation_count = 0
    termination = ""
    timed_out = False
    while True:
        review_index = continuation_count
        stage_update(
            {
                "status": "running",
                "stage": "review",
                "review_index": review_index,
                "continuations": continuation_count,
                "current_snapshot": current.label,
            }
        )
        workspace, codex_home, run_dir, prompt = _stage_review(
            attempt,
            judge_condition,
            problem,
            current,
            review_index,
            wrapper,
            policy,
        )
        launch = _run_agent(
            judge_condition,
            workspace,
            codex_home,
            run_dir,
            prompt,
            "iterative-review-"
            + hashlib.sha256(str(run_dir).encode()).hexdigest()[:10],
            float(judge_timeout),
        )
        timed_out = timed_out or bool(launch["timed_out"])
        decision = _archive_review(attempt / "rounds" / f"review-{review_index:02d}")
        decisions.append(
            {
                "review_index": review_index,
                "snapshot": current.label,
                **decision,
            }
        )
        stage_update(
            {
                "last_decision": decision["decision"],
                "last_reason": decision["reason"],
            }
        )
        if decision["decision"] == "stop":
            termination = "judge-stop"
            break
        if continuation_count >= max_continuations:
            termination = "continuation-limit"
            break
        continuation_count += 1
        stage_update(
            {
                "status": "running",
                "stage": "continuation",
                "continuations": continuation_count,
                "current_snapshot": current.label,
            }
        )
        continuation_stage = attempt / "rounds" / f"continuation-{continuation_count:02d}"
        workspace, codex_home, run_dir, prompt = _stage_continuation(
            attempt,
            solver_condition,
            problem,
            current,
            continuation_count,
            attempt / "rounds" / f"review-{review_index:02d}/decision.json",
            continuation_template,
        )
        launch = _run_agent(
            solver_condition,
            workspace,
            codex_home,
            run_dir,
            prompt,
            "iterative-continuation-"
            + hashlib.sha256(str(run_dir).encode()).hexdigest()[:10],
            float(continuation_timeout),
        )
        timed_out = timed_out or bool(launch["timed_out"])
        current = _archive_continuation(continuation_stage, continuation_count)
    manifest = _materialize_final(
        attempt, current, termination, continuation_count, decisions
    )
    return {
        "problem_id": problem.problem_id,
        "status": "archived",
        "stage": "complete",
        "valid_output": True,
        "termination": termination,
        "continuations": continuation_count,
        "reviews": len(decisions),
        "last_decision": decisions[-1]["decision"],
        "final_snapshot": current.label,
        "candidate_count": len(manifest["candidates"]),
        "timed_out": timed_out,
        "ended_at": now(),
    }


def evaluate_iterative_coverage(run_root: Path) -> dict[str, Any]:
    run_root = run_root.resolve()
    rows = []
    for assignment_path in sorted((run_root / "attempts").glob("*/control/assignment.json")):
        attempt = assignment_path.parents[1]
        assignment = load_json(assignment_path)
        problem_id = str(assignment["problem_id"])
        reference = assignment_path.parent / str(assignment["reference"])
        initial = evaluate_candidates(
            reference,
            declared_candidates(attempt / "initial/submitted"),
            problem_id,
        )
        final_candidates = declared_candidates(attempt / "submission")
        final = evaluate_candidates(reference, final_candidates, problem_id)
        chain = (
            load_json(attempt / "chain.json")
            if (attempt / "chain.json").is_file()
            else {"termination": "invalid", "reviews": []}
        )
        continuation_results = []
        for stage in sorted((attempt / "rounds").glob("continuation-*")):
            result = evaluate_candidates(
                reference,
                declared_candidates(stage / "submitted"),
                problem_id,
            )
            continuation_results.append(
                {
                    "snapshot": stage.name,
                    "selected_exact": bool(result["selected_exact"]),
                    "candidates_exact": bool(result["candidates_exact"]),
                    "matched_candidates": result["metrics"]["matched_candidates"],
                }
            )
        row = {
            "problem_id": problem_id,
            "valid_output": bool(final_candidates and (attempt / "chain.json").is_file()),
            "initial_selected_exact": bool(initial["selected_exact"]),
            "initial_candidates_exact": bool(initial["candidates_exact"]),
            "final_selected_exact": bool(final["selected_exact"]),
            "final_candidates_exact": bool(final["candidates_exact"]),
            "recovered": bool(final["candidates_exact"] and not initial["candidates_exact"]),
            "regressed": bool(initial["candidates_exact"] and not final["candidates_exact"]),
            "termination": chain["termination"],
            "continuations": len(continuation_results),
            "reviews": len(chain["reviews"]),
            "matched_final_candidates": final["metrics"]["matched_candidates"],
            "continuation_results": continuation_results,
        }
        write_json(attempt / "control/evaluation.json", row)
        rows.append(row)
    summary = {
        "schema_version": "iterative-coverage-evaluation-v1",
        "attempts": len(rows),
        "valid_outputs": sum(row["valid_output"] for row in rows),
        "initial_selected_exact": sum(row["initial_selected_exact"] for row in rows),
        "initial_candidates_exact": sum(row["initial_candidates_exact"] for row in rows),
        "final_selected_exact": sum(row["final_selected_exact"] for row in rows),
        "final_candidates_exact": sum(row["final_candidates_exact"] for row in rows),
        "recoveries": sum(row["recovered"] for row in rows),
        "regressions": sum(row["regressed"] for row in rows),
        "judge_stops": sum(row["termination"] == "judge-stop" for row in rows),
        "continuation_limits": sum(
            row["termination"] == "continuation-limit" for row in rows
        ),
        "solver_continuations": sum(row["continuations"] for row in rows),
        "judge_calls": sum(row["reviews"] for row in rows),
        "results": rows,
    }
    write_json(run_root / "evaluation.json", summary)
    return summary


def _copy_contract(
    output: Path,
    judge_condition_path: Path,
    solver_condition_path: Path,
    panel_path: Path,
    source: Path,
    wrapper_path: Path,
    policy_path: Path,
    continuation_prompt_path: Path,
    solver_condition: Condition,
) -> None:
    contract = output / "contract"
    contract.mkdir()
    for source_path, name in (
        (judge_condition_path, "judge-condition.toml"),
        (solver_condition_path, "solver-condition.toml"),
        (panel_path, "panel.json"),
        (wrapper_path, "judge-wrapper.md"),
        (policy_path, "judge-policy.md"),
        (continuation_prompt_path, "continuation-prompt.md"),
    ):
        shutil.copy2(source_path, contract / name)
    if solver_condition.capability is not None:
        shutil.copytree(solver_condition.capability, contract / "capability")
    write_json(
        contract / "source.json",
        {
            "path": str(source),
            "bundle_sha256": sha256_file(source / "bundle.json"),
            "tree_sha256": sha256_tree(source),
        },
    )


def run_iterative_coverage(
    judge_condition_path: Path,
    solver_condition_path: Path,
    panel_path: Path,
    source: Path,
    wrapper_path: Path,
    policy_path: Path,
    continuation_prompt_path: Path,
    output: Path,
    parallel: int,
    max_continuations: int,
    judge_timeout: int | None,
    continuation_timeout: int | None,
    dry_run: bool,
) -> dict[str, Any]:
    judge_condition_path = judge_condition_path.resolve()
    solver_condition_path = solver_condition_path.resolve()
    panel_path = _manifest_path(panel_path)
    source = source.resolve()
    wrapper_path = wrapper_path.resolve()
    policy_path = policy_path.resolve()
    continuation_prompt_path = continuation_prompt_path.resolve()
    output = output.resolve()
    judge_condition = load_condition(judge_condition_path)
    solver_condition = load_condition(solver_condition_path)
    if judge_timeout is not None:
        judge_condition = dataclasses.replace(
            judge_condition, timeout_seconds=judge_timeout
        )
    if continuation_timeout is not None:
        solver_condition = dataclasses.replace(
            solver_condition, timeout_seconds=continuation_timeout
        )
    if judge_condition.adapter != "codex" or solver_condition.adapter != "codex":
        raise RuntimeError("iterative coverage requires Codex judge and solver adapters")
    if judge_condition.timeout_seconds is None or solver_condition.timeout_seconds is None:
        raise ValueError("judge and solver conditions require timeout_seconds")
    for condition_path in {judge_condition_path, solver_condition_path}:
        health = doctor(condition_path)
        if not health["valid"]:
            raise RuntimeError(
                f"condition preflight failed for {condition_path}: "
                + "; ".join(health["failures"])
            )
    problems = load_problem_collection(panel_path)
    by_problem = _source_attempts(source, {problem.problem_id for problem in problems})
    wrapper = wrapper_path.read_text(encoding="utf-8")
    policy = policy_path.read_text(encoding="utf-8")
    continuation_template = continuation_prompt_path.read_text(encoding="utf-8")
    if output.exists() and any(output.iterdir()):
        raise RuntimeError(f"refusing to overwrite nonempty run: {output}")
    (output / "attempts").mkdir(parents=True, exist_ok=True)
    _copy_contract(
        output,
        judge_condition_path,
        solver_condition_path,
        panel_path,
        source,
        wrapper_path,
        policy_path,
        continuation_prompt_path,
        solver_condition,
    )
    write_json(
        output / "run.json",
        {
            "schema_version": "iterative-coverage-run-v1",
            "created_at": now(),
            "mode": "replay-alternating-review-continuation",
            "problem_count": len(problems),
            "parallel_problem_chains": parallel,
            "max_continuations_per_problem": max_continuations,
            "max_judges_per_problem": max_continuations + 1,
            "judge_condition": judge_condition.condition_id,
            "solver_condition": solver_condition.condition_id,
            "judge_timeout_seconds": judge_condition.timeout_seconds,
            "continuation_timeout_seconds": solver_condition.timeout_seconds,
            "model": {
                "judge": judge_condition.model,
                "solver": solver_condition.model,
            },
            "reasoning_effort": {
                "judge": judge_condition.reasoning_effort,
                "solver": solver_condition.reasoning_effort,
            },
            "auth_method": {
                "judge": judge_condition.auth_method,
                "solver": solver_condition.auth_method,
            },
            "source_bundle_sha256": sha256_file(source / "bundle.json"),
            "panel_sha256": sha256_file(panel_path),
            "judge_wrapper_sha256": sha256_file(wrapper_path),
            "judge_policy_sha256": sha256_file(policy_path),
            "continuation_prompt_sha256": sha256_file(continuation_prompt_path),
            "dry_run": dry_run,
            "oracle_available_to_agents": False,
        },
    )
    states = {
        problem.problem_id: {
            "problem_id": problem.problem_id,
            "status": "pending",
            "stage": "pending",
            "continuations": 0,
        }
        for problem in problems
    }
    write_json(output / "progress.json", {"attempts": list(states.values())})
    if dry_run:
        for problem in problems:
            attempt, snapshot = _stage_case(
                output,
                problem,
                by_problem[problem.problem_id],
                judge_condition,
                solver_condition,
            )
            _, judge_home, _, _ = _stage_review(
                attempt,
                judge_condition,
                problem,
                snapshot,
                0,
                wrapper,
                policy,
            )
            _remove_auth_links(judge_home)
            preview_stage = attempt / "continuation-preview"
            preview_evidence = preview_stage / "evidence"
            preview_decision = preview_stage / "decision.json"
            preview_decision.parent.mkdir(parents=True, exist_ok=True)
            write_json(
                preview_decision,
                {
                    "decision": "continue",
                    "reason": "dry-run schema placeholder",
                    "proposed_branch": "dry-run schema placeholder",
                },
            )
            preview_candidates, copied_decision = _copy_continuation_evidence(
                problem, snapshot, preview_decision, preview_evidence
            )
            preview_workspace = preview_stage / "workspace"
            preview_workspace.mkdir()
            capability = preview_workspace / ".vpbench-capability"
            if solver_condition.capability is not None:
                shutil.copytree(solver_condition.capability, capability)
            preview_prompt = render_continuation_prompt(
                continuation_template,
                solver_condition,
                problem,
                preview_evidence,
                copied_decision,
                preview_candidates,
            )
            (preview_stage / "prompt.md").write_text(preview_prompt, encoding="utf-8")
            states[problem.problem_id].update({"status": "staged", "stage": "review-00"})
        write_json(output / "progress.json", {"attempts": list(states.values())})
        return {"staged": len(problems), "output": str(output)}
    lock = threading.Lock()

    def update(problem_id: str, values: dict[str, Any]) -> None:
        with lock:
            states[problem_id].update(values)
            write_json(output / "progress.json", {"attempts": list(states.values())})

    def one(problem: Problem) -> dict[str, Any]:
        update(problem.problem_id, {"status": "running", "started_at": now()})
        try:
            result = _run_chain_attempt(
                output,
                judge_condition,
                solver_condition,
                problem,
                by_problem[problem.problem_id],
                wrapper,
                policy,
                continuation_template,
                max_continuations,
                int(judge_condition.timeout_seconds),
                int(solver_condition.timeout_seconds),
                lambda values: update(problem.problem_id, values),
            )
        except Exception as error:
            result = {
                "problem_id": problem.problem_id,
                "status": "failed",
                "valid_output": False,
                "error": f"{type(error).__name__}: {error}",
                "ended_at": now(),
            }
        update(problem.problem_id, result)
        return result

    with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as executor:
        futures = [executor.submit(one, problem) for problem in problems]
        for future in concurrent.futures.as_completed(futures):
            future.result()
    evaluation = evaluate_iterative_coverage(output)
    write_json(
        output / "summary.json",
        {
            "attempts": len(problems),
            "archived": sum(row["status"] == "archived" for row in states.values()),
            "failed": sum(row["status"] == "failed" for row in states.values()),
            "evaluation": evaluation,
        },
    )
    return evaluation
