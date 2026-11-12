"""Blind LLM stop/continue review for completed pXRD solver attempts."""

from __future__ import annotations

import concurrent.futures
import dataclasses
import hashlib
import shutil
import threading
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
from .matching import evaluate_candidates
from .run import _remove_auth_links, doctor, now
from .util import load_json, sha256_file, sha256_tree, write_json


def _manifest_path(path: Path) -> Path:
    path = path.resolve()
    return path / "manifest.json" if path.is_dir() else path


def render_review_prompt(
    wrapper: str,
    policy: str,
    problem: Problem,
    evidence: Path,
    candidates: tuple[Path, ...],
) -> str:
    candidate_text = "\n".join(f"- {path}" for path in candidates) or "- None submitted."
    values = {
        "formula": problem.formula,
        "pattern_path": str(evidence / "pattern.csv"),
        "wavelength": f"{problem.wavelength} angstrom ({problem.radiation})",
        "trace_path": str(evidence / "first-pass-trace.jsonl"),
        "final_response_path": str(evidence / "first-pass-final.md"),
        "submitted_cifs": candidate_text,
        "rwp_report_path": str(evidence / "comparable-rwp-report.json"),
        "judge_policy": policy.strip(),
    }
    prompt = wrapper
    for key, value in values.items():
        prompt = prompt.replace("{" + key + "}", value)
    unresolved = [key for key in values if "{" + key + "}" in prompt]
    if unresolved:
        raise ValueError(f"unresolved LLM-verifier prompt fields: {unresolved}")
    return prompt.rstrip() + "\n"


def validate_decision(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError("decision.json missing")
    value = load_json(path)
    if not isinstance(value, dict):
        raise TypeError("decision.json must contain an object")
    decision = value.get("decision")
    if decision not in {"stop", "continue"}:
        raise ValueError("decision must be stop or continue")
    reason = value.get("reason")
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("reason must be a non-empty string")
    proposed = value.get("proposed_branch")
    if decision == "stop" and proposed is not None:
        raise ValueError("proposed_branch must be null when stopping")
    if proposed is not None and (not isinstance(proposed, str) or not proposed.strip()):
        raise ValueError("proposed_branch must be a non-empty string when supplied")
    return {
        "decision": decision,
        "reason": reason.strip(),
        "proposed_branch": proposed.strip() if isinstance(proposed, str) else None,
    }


def decision_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {
        "true_continue": 0,
        "false_stop": 0,
        "true_stop": 0,
        "false_continue": 0,
        "invalid": 0,
    }
    for row in rows:
        predicted = row.get("decision")
        oracle = row.get("oracle_decision")
        if predicted not in {"stop", "continue"}:
            counts["invalid"] += 1
        elif predicted == "continue" and oracle == "continue":
            counts["true_continue"] += 1
        elif predicted == "stop" and oracle == "continue":
            counts["false_stop"] += 1
        elif predicted == "stop" and oracle == "stop":
            counts["true_stop"] += 1
        else:
            counts["false_continue"] += 1
    misses = counts["true_continue"] + counts["false_stop"]
    exact = counts["true_stop"] + counts["false_continue"]
    correct = counts["true_continue"] + counts["true_stop"]
    total = len(rows)
    continue_recall = counts["true_continue"] / misses if misses else 1.0
    stop_recall = counts["true_stop"] / exact if exact else 1.0
    return {
        **counts,
        "count": total,
        "correct": correct,
        "accuracy": correct / total if total else 0.0,
        "balanced_accuracy": (continue_recall + stop_recall) / 2,
        "continue_recall": continue_recall,
        "stop_recall": stop_recall,
        "false_stop_rate": counts["false_stop"] / misses if misses else 0.0,
        "continuation_rate": (
            (counts["true_continue"] + counts["false_continue"]) / total if total else 0.0
        ),
    }


def _rwp_report(rwp_root: Path | None, problem_id: str) -> Path | None:
    if rwp_root is None:
        return None
    candidates = (
        rwp_root / "cases" / problem_id / "report.json",
        rwp_root / problem_id / "report.json",
        rwp_root / f"{problem_id}.json",
    )
    return next((path for path in candidates if path.is_file()), None)


def _stage_attempt(
    run_root: Path,
    condition: Condition,
    problem: Problem,
    source: FirstPassAttempt,
    wrapper: str,
    policy: str,
    rwp_root: Path | None,
) -> tuple[Path, Path, Path, str, tuple[Path, ...]]:
    attempt = run_root / "attempts" / problem.problem_id
    if attempt.exists():
        raise FileExistsError(attempt)
    evidence = attempt / "evidence"
    control = attempt / "control"
    workspace = attempt / "workspace"
    codex_home = attempt / "codex-home"
    run_dir = attempt / "run"
    for path in (evidence, control, run_dir):
        path.mkdir(parents=True, exist_ok=True)
    shutil.copy2(problem.pattern, evidence / "pattern.csv")
    _copy_trace(source.trace, evidence / "first-pass-trace.jsonl")
    if source.final_response is not None:
        shutil.copy2(source.final_response, evidence / "first-pass-final.md")
    else:
        (evidence / "first-pass-final.md").write_text(
            "No final response was captured for this first-pass attempt.\n",
            encoding="utf-8",
        )
    candidates = []
    for index, source_candidate in enumerate(source.candidates, start=1):
        name = source_candidate.name
        destination = evidence / name
        if destination.exists():
            destination = evidence / f"candidate-{index:03d}.cif"
        shutil.copy2(source_candidate, destination)
        candidates.append(destination)
    report = _rwp_report(rwp_root, problem.problem_id)
    if report is None:
        write_json(
            evidence / "comparable-rwp-report.json",
            {"available": False, "reason": "not supplied"},
        )
    else:
        shutil.copy2(report, evidence / "comparable-rwp-report.json")
    shutil.copy2(problem.reference, control / "reference.cif")
    prompt = render_review_prompt(wrapper, policy, problem, evidence, tuple(candidates))
    (attempt / "prompt.md").write_text(prompt, encoding="utf-8")
    _prepare_agent_home(condition, workspace, codex_home, (evidence,))
    write_json(
        control / "assignment.json",
        {
            "problem_id": problem.problem_id,
            "formula": problem.formula,
            "reference": "reference.cif",
            "reference_sha256": sha256_file(problem.reference),
            "pattern_sha256": sha256_file(problem.pattern),
            "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
            "source_attempt": str(source.root),
        },
    )
    return workspace, codex_home, run_dir, prompt, tuple(candidates)


def _evaluate_attempt(attempt: Path) -> dict[str, Any]:
    assignment = load_json(attempt / "control/assignment.json")
    problem_id = str(assignment["problem_id"])
    reference = attempt / "control/reference.cif"
    candidates = sorted((attempt / "evidence").glob("*.cif"))
    verifier = evaluate_candidates(reference, candidates, problem_id)
    decision_error = None
    try:
        decision = validate_decision(attempt / "workspace/decision.json")
    except Exception as error:
        decision = None
        decision_error = f"{type(error).__name__}: {error}"
    if decision is not None:
        write_json(attempt / "decision.json", decision)
    write_json(attempt / "control/verifier-result.json", verifier)
    oracle = "stop" if verifier["candidates_exact"] else "continue"
    predicted = decision["decision"] if decision else None
    return {
        "problem_id": problem_id,
        "decision": predicted,
        "reason": decision["reason"] if decision else None,
        "proposed_branch": decision["proposed_branch"] if decision else None,
        "decision_error": decision_error,
        "oracle_decision": oracle,
        "decision_correct": predicted == oracle,
        "candidates_exact": bool(verifier["candidates_exact"]),
    }


def evaluate_llm_verifier(run_root: Path) -> dict[str, Any]:
    run_root = run_root.resolve()
    rows = [
        _evaluate_attempt(attempt)
        for attempt in sorted((run_root / "attempts").iterdir())
        if (attempt / "control/assignment.json").is_file()
    ]
    summary = {
        "schema_version": "llm-verifier-evaluation-v1",
        "metrics": decision_metrics(rows),
        "results": rows,
    }
    write_json(run_root / "evaluation.json", summary)
    return summary


def run_llm_verifier(
    condition_path: Path,
    panel_path: Path,
    source: Path,
    wrapper_path: Path,
    policy_path: Path,
    output: Path,
    parallel: int,
    timeout_seconds: int | None,
    rwp_root: Path | None,
    dry_run: bool,
) -> dict[str, Any]:
    condition_path = condition_path.resolve()
    panel_path = _manifest_path(panel_path)
    source = source.resolve()
    wrapper_path = wrapper_path.resolve()
    policy_path = policy_path.resolve()
    output = output.resolve()
    rwp_root = rwp_root.resolve() if rwp_root is not None else None
    condition = load_condition(condition_path)
    if timeout_seconds is not None:
        condition = dataclasses.replace(condition, timeout_seconds=timeout_seconds)
    if condition.adapter != "codex":
        raise RuntimeError("LLM verification requires the Codex adapter")
    if condition.timeout_seconds is None:
        raise ValueError("LLM-verifier condition requires a timeout")
    health = doctor(condition_path)
    if not health["valid"]:
        raise RuntimeError("condition preflight failed: " + "; ".join(health["failures"]))
    problems = load_problem_collection(panel_path)
    by_problem = _source_attempts(source, {problem.problem_id for problem in problems})
    wrapper = wrapper_path.read_text(encoding="utf-8")
    policy = policy_path.read_text(encoding="utf-8")
    if output.exists() and any(output.iterdir()):
        raise RuntimeError(f"refusing to overwrite nonempty run: {output}")
    (output / "attempts").mkdir(parents=True, exist_ok=True)
    contract = output / "contract"
    contract.mkdir()
    for source_path, name in (
        (condition_path, "condition.toml"),
        (panel_path, "panel.json"),
        (wrapper_path, "wrapper.md"),
        (policy_path, "policy.md"),
    ):
        shutil.copy2(source_path, contract / name)
    if condition.capability is not None:
        shutil.copytree(condition.capability, contract / "capability")
    write_json(
        contract / "source.json",
        {
            "path": str(source),
            "bundle_sha256": sha256_file(source / "bundle.json"),
            "tree_sha256": sha256_tree(source),
        },
    )
    write_json(
        output / "run.json",
        {
            "schema_version": "llm-verifier-run-v1",
            "created_at": now(),
            "condition": condition.condition_id,
            "model": condition.model,
            "reasoning_effort": condition.reasoning_effort,
            "auth_method": condition.auth_method,
            "problem_count": len(problems),
            "parallel": parallel,
            "timeout_seconds": condition.timeout_seconds,
            "dry_run": dry_run,
            "oracle_available_to_reviewer": False,
            "condition_sha256": sha256_file(condition_path),
            "panel_sha256": sha256_file(panel_path),
            "wrapper_sha256": sha256_file(wrapper_path),
            "policy_sha256": sha256_file(policy_path),
            "source_bundle_sha256": sha256_file(source / "bundle.json"),
        },
    )
    states = {
        problem.problem_id: {"problem_id": problem.problem_id, "status": "pending"}
        for problem in problems
    }
    write_json(output / "progress.json", {"attempts": list(states.values())})
    lock = threading.Lock()

    def update(problem_id: str, values: dict[str, Any]) -> None:
        with lock:
            states[problem_id].update(values)
            scored = [
                row for row in states.values() if row.get("oracle_decision") is not None
            ]
            write_json(
                output / "progress.json",
                {
                    "attempts": list(states.values()),
                    "metrics": decision_metrics(scored),
                },
            )

    def one(problem: Problem) -> dict[str, Any]:
        update(problem.problem_id, {"status": "running", "started_at": now()})
        try:
            workspace, codex_home, run_dir, prompt, _ = _stage_attempt(
                output,
                condition,
                problem,
                by_problem[problem.problem_id],
                wrapper,
                policy,
                rwp_root,
            )
            if dry_run:
                _remove_auth_links(codex_home)
                result = {"problem_id": problem.problem_id, "status": "staged"}
            else:
                launch = _run_agent(
                    condition,
                    workspace,
                    codex_home,
                    run_dir,
                    prompt,
                    "llm-verifier-" + hashlib.sha256(str(run_dir).encode()).hexdigest()[:10],
                    float(condition.timeout_seconds),
                )
                result = {
                    "problem_id": problem.problem_id,
                    "status": "archived",
                    "timed_out": launch["timed_out"],
                    "returncode": launch["returncode"],
                    "ended_at": now(),
                }
                try:
                    result.update(_evaluate_attempt(output / "attempts" / problem.problem_id))
                except Exception as error:
                    result["evaluation_error"] = f"{type(error).__name__}: {error}"
        except Exception as error:
            result = {
                "problem_id": problem.problem_id,
                "status": "failed",
                "error": f"{type(error).__name__}: {error}",
                "ended_at": now(),
            }
        update(problem.problem_id, result)
        return result

    with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as executor:
        futures = [executor.submit(one, problem) for problem in problems]
        for future in concurrent.futures.as_completed(futures):
            future.result()
    if dry_run:
        return {"staged": sum(row["status"] == "staged" for row in states.values())}
    evaluation = evaluate_llm_verifier(output)
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
