from __future__ import annotations

import concurrent.futures
import csv
import gzip
import hashlib
import os
import shutil
import signal
import subprocess
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .benchmark import Problem, load_problem_collection
from .condition import Condition, load_condition
from .matching import declared_candidates, evaluate_selected, evaluate_workspace
from .run import (
    _clean_environment,
    _config_text,
    _launch_command,
    _remove_auth_links,
    doctor,
    now,
)
from .run import (
    _render_prompt as _render_solve_prompt,
)
from .util import load_json, sha256_file, sha256_tree, write_json


@dataclass(frozen=True, slots=True)
class FirstPassAttempt:
    problem_id: str
    root: Path
    trace: Path
    final_response: Path | None
    candidates: tuple[Path, ...]


def _manifest_path(path: Path) -> Path:
    path = path.resolve()
    return path / "manifest.json" if path.is_dir() else path


def _source_attempts(source: Path, problem_ids: set[str]) -> dict[str, FirstPassAttempt]:
    source = source.resolve()
    bundle_path = source / "bundle.json"
    if not bundle_path.is_file():
        raise FileNotFoundError(
            f"{source} is not a normalized result bundle (bundle.json is missing)"
        )
    bundle = load_json(bundle_path)
    records = bundle.get("cases")
    if not isinstance(records, list):
        raise ValueError(f"{bundle_path} has no cases list")
    by_case: dict[str, FirstPassAttempt] = {}
    for record in records:
        problem_id = str(record.get("problem_id", record.get("case_id", "")))
        if problem_id not in problem_ids:
            continue
        attempt = source / "attempts" / problem_id
        if not attempt.is_dir():
            raise FileNotFoundError(attempt)
        trace_options = (attempt / "codex-events.jsonl.gz", attempt / "codex-events.jsonl")
        trace = next((path for path in trace_options if path.is_file()), None)
        if trace is None:
            raise FileNotFoundError(f"no chronological trace for {problem_id}")
        final_response = attempt / "final-answer.md"
        candidates = tuple(declared_candidates(attempt / "submission"))
        by_case[problem_id] = FirstPassAttempt(
            problem_id=problem_id,
            root=attempt,
            trace=trace,
            final_response=final_response if final_response.is_file() else None,
            candidates=candidates,
        )
    missing = sorted(problem_ids - set(by_case))
    extras = sorted(set(by_case) - problem_ids)
    if missing or extras:
        raise ValueError(f"source/panel mismatch: missing={missing}, extras={extras}")
    return by_case


def _copy_trace(source: Path, destination: Path) -> None:
    if source.suffix == ".gz":
        with gzip.open(source, "rb") as input_stream, destination.open("wb") as output_stream:
            shutil.copyfileobj(input_stream, output_stream)
    else:
        shutil.copy2(source, destination)


def _prepare_agent_home(
    condition: Condition,
    workspace: Path,
    codex_home: Path,
    extra_read_paths: tuple[Path, ...] = (),
) -> None:
    for path in (
        workspace / ".tmp",
        workspace / ".cache/matplotlib",
        codex_home,
    ):
        path.mkdir(parents=True, exist_ok=True)
    if condition.capability:
        shutil.copytree(condition.capability, workspace / ".vpbench-capability")
    for name in ("auth.json", "models_cache.json"):
        source = condition.auth_home / name
        if source.exists():
            (codex_home / name).symlink_to(source)
    (codex_home / "config.toml").write_text(
        _config_text(condition, workspace, extra_read_paths), encoding="utf-8"
    )


def _run_agent(
    condition: Condition,
    workspace: Path,
    codex_home: Path,
    run_dir: Path,
    prompt: str,
    token: str,
    timeout_seconds: float,
) -> dict[str, Any]:
    if timeout_seconds <= 0:
        raise TimeoutError("no time remains in the coverage-directed budget")
    run_dir.mkdir(parents=True, exist_ok=True)
    command, unit = _launch_command(condition, workspace, codex_home, run_dir, token)
    launch: dict[str, Any] = {
        "started_at": now(),
        "command": command,
        "systemd_unit": unit,
        "model": condition.model,
        "reasoning_effort": condition.reasoning_effort,
        "timeout_seconds": timeout_seconds,
    }
    write_json(run_dir / "launch.json", launch)
    process: subprocess.Popen[str] | None = None
    timed_out = False
    started = time.monotonic()
    stdout = ""
    stderr = ""
    try:
        process = subprocess.Popen(
            command,
            cwd=workspace,
            env=_clean_environment(codex_home),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
        try:
            stdout, stderr = process.communicate(prompt, timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            timed_out = True
            if unit:
                subprocess.run(
                    ["systemctl", "--user", "stop", unit],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                )
            else:
                os.killpg(process.pid, signal.SIGINT)
            try:
                stdout, stderr = process.communicate(timeout=30)
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
    finally:
        _remove_auth_links(codex_home)
    elapsed = time.monotonic() - started
    (run_dir / "codex-events.jsonl").write_text(stdout, encoding="utf-8")
    (run_dir / "codex-stderr.log").write_text(stderr, encoding="utf-8")
    launch.update(
        {
            "ended_at": now(),
            "elapsed_seconds": elapsed,
            "returncode": process.returncode if process else None,
            "timed_out": timed_out,
        }
    )
    write_json(run_dir / "launch.json", launch)
    return launch


def _render_prompt(
    condition: Condition,
    problem: Problem,
    first_pass: Path,
) -> str:
    candidate_text = "\n".join(
        f"- {path}" for path in declared_candidates(first_pass / "submitted")
    ) or "- None submitted"
    values = {
        "formula": problem.formula,
        "pattern_path": str(first_pass / "pattern.csv"),
        "wavelength": f"{problem.wavelength} angstrom ({problem.radiation})",
        "trace_path": str(first_pass / "trace.jsonl"),
        "final_response_path": str(first_pass / "final-response.md"),
        "submitted_cifs": candidate_text,
    }
    review_prompt = getattr(condition, "review_prompt", None) or condition.prompt
    prompt = review_prompt.read_text(encoding="utf-8")
    for key, value in values.items():
        prompt = prompt.replace("{" + key + "}", value)
    unresolved = [key for key in values if "{" + key + "}" in prompt]
    if unresolved:
        raise ValueError(f"unresolved coverage prompt fields: {unresolved}")
    return prompt.rstrip() + "\n"


def _stage_attempt(
    run_root: Path,
    condition: Condition,
    problem: Problem,
    source: FirstPassAttempt,
) -> tuple[Path, Path, Path, str]:
    attempt = run_root / "attempts" / problem.problem_id
    if attempt.exists():
        raise FileExistsError(attempt)
    first_pass = attempt / "first-pass"
    submitted = first_pass / "submitted"
    workspace = attempt / "workspace"
    run_dir = attempt / "run"
    control = attempt / "control"
    codex_home = attempt / "codex-home"
    for path in (submitted, run_dir, control):
        path.mkdir(parents=True, exist_ok=True)
    shutil.copy2(problem.pattern, first_pass / "pattern.csv")
    _copy_trace(source.trace, first_pass / "trace.jsonl")
    if source.final_response:
        shutil.copy2(source.final_response, first_pass / "final-response.md")
    else:
        (first_pass / "final-response.md").write_text(
            "No final response was captured for the first pass.\n", encoding="utf-8"
        )
    source_candidates: list[dict[str, str]] = []
    for candidate in source.candidates:
        destination = submitted / candidate.name
        shutil.copy2(candidate, destination)
        source_candidates.append(
            {
                "file": candidate.name,
                "sha256": sha256_file(destination),
            }
        )
    write_json(
        first_pass / "manifest.json",
        {
            "schema_version": "1",
            "pattern_sha256": sha256_file(first_pass / "pattern.csv"),
            "trace_sha256": sha256_file(first_pass / "trace.jsonl"),
            "final_response_sha256": sha256_file(first_pass / "final-response.md"),
            "candidates": source_candidates,
        },
    )
    shutil.copy2(problem.reference, control / "reference.cif")
    prompt = _render_prompt(condition, problem, first_pass)
    (attempt / "prompt.txt").write_text(prompt, encoding="utf-8")
    _prepare_agent_home(condition, workspace, codex_home, (first_pass,))
    write_json(
        control / "assignment.json",
        {
            "problem_id": problem.problem_id,
            "formula": problem.formula,
            "reference": "reference.cif",
            "reference_sha256": sha256_file(problem.reference),
            "pattern_sha256": sha256_file(problem.pattern),
            "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
            "first_pass_manifest_sha256": sha256_file(first_pass / "manifest.json"),
            "condition": condition.condition_id,
            "source_attempt": str(source.root),
        },
    )
    return attempt, workspace, codex_home, prompt


def _stage_fresh_first_pass(
    run_root: Path,
    condition: Condition,
    problem: Problem,
) -> tuple[Path, Path, Path, str]:
    attempt = run_root / "attempts" / problem.problem_id
    if attempt.exists():
        raise FileExistsError(attempt)
    first_pass = attempt / "first-pass"
    workspace = first_pass / "workspace"
    run_dir = first_pass / "run"
    codex_home = first_pass / "codex-home"
    control = attempt / "control"
    for path in (run_dir, control):
        path.mkdir(parents=True, exist_ok=True)
    _prepare_agent_home(condition, workspace, codex_home)
    shutil.copy2(problem.pattern, workspace / "pattern.csv")
    prompt = _render_solve_prompt(condition, problem, workspace)
    (first_pass / "prompt.txt").write_text(prompt, encoding="utf-8")
    shutil.copy2(problem.reference, control / "reference.cif")
    review_prompt = condition.review_prompt
    write_json(
        control / "assignment.json",
        {
            "problem_id": problem.problem_id,
            "formula": problem.formula,
            "reference": "reference.cif",
            "reference_sha256": sha256_file(problem.reference),
            "pattern_sha256": sha256_file(problem.pattern),
            "condition": condition.condition_id,
            "first_pass_prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
            "review_prompt_sha256": sha256_file(review_prompt) if review_prompt else None,
            "source_attempt": None,
        },
    )
    return attempt, workspace, codex_home, prompt


def _archive_fresh_first_pass(attempt: Path, problem: Problem) -> FirstPassAttempt:
    first_pass = attempt / "first-pass"
    workspace = first_pass / "workspace"
    run_dir = first_pass / "run"
    submitted = first_pass / "submitted"
    submitted.mkdir()
    shutil.copy2(problem.pattern, first_pass / "pattern.csv")
    _copy_trace(run_dir / "codex-events.jsonl", first_pass / "trace.jsonl")
    captured_response = run_dir / "final-answer.md"
    final_response = first_pass / "final-response.md"
    if captured_response.is_file():
        shutil.copy2(captured_response, final_response)
    else:
        final_response.write_text(
            "No final response was captured for the first pass.\n", encoding="utf-8"
        )
    candidate_records: list[dict[str, str]] = []
    for candidate in declared_candidates(workspace):
        destination = submitted / candidate.name
        shutil.copy2(candidate, destination)
        candidate_records.append({"file": destination.name, "sha256": sha256_file(destination)})
    write_json(
        first_pass / "manifest.json",
        {
            "schema_version": "2",
            "origin": "fresh-first-pass",
            "pattern_sha256": sha256_file(first_pass / "pattern.csv"),
            "trace_sha256": sha256_file(first_pass / "trace.jsonl"),
            "final_response_sha256": sha256_file(final_response),
            "workspace_sha256": sha256_tree(workspace),
            "candidates": candidate_records,
        },
    )
    return FirstPassAttempt(
        problem_id=problem.problem_id,
        root=first_pass,
        trace=first_pass / "trace.jsonl",
        final_response=final_response,
        candidates=tuple(declared_candidates(submitted)),
    )


def _stage_review(
    attempt: Path,
    condition: Condition,
    problem: Problem,
) -> tuple[Path, Path, str]:
    first_pass = attempt / "first-pass"
    workspace = attempt / "workspace"
    run_dir = attempt / "run"
    codex_home = attempt / "codex-home"
    run_dir.mkdir()
    prompt = _render_prompt(condition, problem, first_pass)
    (attempt / "prompt.txt").write_text(prompt, encoding="utf-8")
    _prepare_agent_home(condition, workspace, codex_home, (first_pass,))
    assignment_path = attempt / "control/assignment.json"
    assignment = load_json(assignment_path)
    assignment.update(
        {
            "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
            "first_pass_manifest_sha256": sha256_file(first_pass / "manifest.json"),
        }
    )
    write_json(assignment_path, assignment)
    return workspace, codex_home, prompt


def _validate_decision(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError("decision.json missing")
    value = load_json(path)
    decision = value.get("decision")
    if decision not in {"stop", "continue"}:
        raise ValueError("decision must be stop or continue")
    if not isinstance(value.get("reason"), str) or not value["reason"].strip():
        raise ValueError("decision reason is missing")
    fields = ("proposed_branch", "continuation_plan")
    supplied = [name for name in fields if name in value]
    if len(supplied) != 1:
        raise ValueError("decision must contain exactly one continuation field")
    field = supplied[0]
    continuation = value[field]
    if decision == "stop" and continuation is not None:
        raise ValueError(f"stop decision must use null {field}")
    if decision == "continue" and (
        not isinstance(continuation, str) or not continuation.strip()
    ):
        raise ValueError(f"continue decision requires {field}")
    return value


def _materialize_submission(attempt: Path, decision: dict[str, Any]) -> dict[str, Any]:
    destination = attempt / "submission"
    if destination.exists():
        raise FileExistsError(destination)
    destination.mkdir()
    source_dir = (
        attempt / "first-pass/submitted"
        if decision["decision"] == "stop"
        else attempt / "workspace"
    )
    candidates = declared_candidates(source_dir)
    if not candidates or candidates[0].name != "selected.cif":
        raise ValueError(
            f"{decision['decision']} output has no canonical selected.cif in {source_dir}"
        )
    first_pass = {
        sha256_file(path): path.name
        for path in declared_candidates(attempt / "first-pass/submitted")
    }
    records = []
    for candidate in candidates:
        output = destination / candidate.name
        shutil.copy2(candidate, output)
        digest = sha256_file(output)
        records.append(
            {
                "file": output.name,
                "sha256": digest,
                "origin": (
                    "first-pass-byte-identical"
                    if digest in first_pass
                    else "continuation-output"
                ),
                "first_pass_file": first_pass.get(digest),
            }
        )
    manifest = {
        "schema_version": "1",
        "decision": decision["decision"],
        "candidates": records,
    }
    write_json(destination / "manifest.json", manifest)
    write_json(attempt / "decision.json", decision)
    return manifest


def _run_replay_attempt(
    run_root: Path,
    condition: Condition,
    problem: Problem,
    source: FirstPassAttempt,
) -> dict[str, Any]:
    attempt, workspace, codex_home, prompt = _stage_attempt(
        run_root, condition, problem, source
    )
    run_dir = attempt / "run"
    token = "coverage-" + hashlib.sha256(str(attempt).encode()).hexdigest()[:10]
    if condition.timeout_seconds is None:
        raise ValueError("coverage replay requires timeout_seconds")
    launch = _run_agent(
        condition,
        workspace,
        codex_home,
        run_dir,
        prompt,
        token,
        condition.timeout_seconds,
    )
    decision_error = None
    submission_error = None
    decision: dict[str, Any] | None = None
    try:
        decision = _validate_decision(workspace / "decision.json")
    except Exception as error:
        decision_error = f"{type(error).__name__}: {error}"
    if decision is not None:
        try:
            _materialize_submission(attempt, decision)
        except Exception as error:
            submission_error = f"{type(error).__name__}: {error}"
    launch.update(
        {
            "decision": decision.get("decision") if decision else None,
            "decision_error": decision_error,
            "submission_error": submission_error,
        }
    )
    write_json(run_dir / "launch.json", launch)
    return {
        "problem_id": problem.problem_id,
        "status": "archived",
        "decision": decision.get("decision") if decision else None,
        "valid_output": decision_error is None and submission_error is None,
        "decision_error": decision_error,
        "submission_error": submission_error,
        "timed_out": launch["timed_out"],
        "returncode": launch["returncode"],
        "ended_at": now(),
    }


def _run_end_to_end_attempt(
    run_root: Path,
    condition: Condition,
    problem: Problem,
    stage_update: Callable[[dict[str, Any]], None],
) -> dict[str, Any]:
    if condition.timeout_seconds is None or condition.first_pass_timeout_seconds is None:
        raise ValueError(
            "end-to-end coverage requires timeout_seconds and first_pass_timeout_seconds"
        )
    started = time.monotonic()
    deadline = started + condition.timeout_seconds
    attempt, first_workspace, first_codex_home, first_prompt = _stage_fresh_first_pass(
        run_root, condition, problem
    )
    first_run = attempt / "first-pass/run"
    first_timeout = min(
        float(condition.first_pass_timeout_seconds),
        max(0.0, deadline - time.monotonic()),
    )
    stage_update(
        {
            "status": "running",
            "stage": "first-pass",
            "first_pass_timeout_seconds": first_timeout,
        }
    )
    first_launch = _run_agent(
        condition,
        first_workspace,
        first_codex_home,
        first_run,
        first_prompt,
        "coverage-first-" + hashlib.sha256(str(attempt).encode()).hexdigest()[:10],
        first_timeout,
    )
    first_source = _archive_fresh_first_pass(attempt, problem)
    remaining = max(0.0, deadline - time.monotonic())
    stage_update(
        {
            "status": "running",
            "stage": "review",
            "first_pass_timed_out": first_launch["timed_out"],
            "first_pass_returncode": first_launch["returncode"],
            "first_pass_candidate_count": len(first_source.candidates),
            "remaining_seconds": remaining,
        }
    )
    workspace, codex_home, prompt = _stage_review(attempt, condition, problem)
    remaining = max(0.0, deadline - time.monotonic())
    stage_update({"status": "running", "stage": "review", "remaining_seconds": remaining})
    review_launch = _run_agent(
        condition,
        workspace,
        codex_home,
        attempt / "run",
        prompt,
        "coverage-review-" + hashlib.sha256(str(attempt).encode()).hexdigest()[:10],
        remaining,
    )
    decision_error = None
    submission_error = None
    decision: dict[str, Any] | None = None
    try:
        decision = _validate_decision(workspace / "decision.json")
    except Exception as error:
        decision_error = f"{type(error).__name__}: {error}"
    if decision is not None:
        try:
            _materialize_submission(attempt, decision)
        except Exception as error:
            submission_error = f"{type(error).__name__}: {error}"
    review_launch.update(
        {
            "decision": decision.get("decision") if decision else None,
            "decision_error": decision_error,
            "submission_error": submission_error,
            "total_elapsed_seconds": time.monotonic() - started,
            "total_timeout_seconds": condition.timeout_seconds,
        }
    )
    write_json(attempt / "run/launch.json", review_launch)
    return {
        "problem_id": problem.problem_id,
        "status": "archived",
        "stage": "complete",
        "decision": decision.get("decision") if decision else None,
        "valid_output": decision_error is None and submission_error is None,
        "decision_error": decision_error,
        "submission_error": submission_error,
        "first_pass_timed_out": first_launch["timed_out"],
        "review_timed_out": review_launch["timed_out"],
        "timed_out": bool(first_launch["timed_out"] or review_launch["timed_out"]),
        "first_pass_returncode": first_launch["returncode"],
        "review_returncode": review_launch["returncode"],
        "total_elapsed_seconds": time.monotonic() - started,
        "ended_at": now(),
    }


def _copy_contract(
    run_root: Path,
    condition_path: Path,
    panel_path: Path,
    condition: Condition,
    source: Path | None = None,
) -> None:
    contract = run_root / "contract"
    contract.mkdir()
    shutil.copy2(condition_path, contract / "condition.toml")
    shutil.copy2(condition.prompt, contract / "first-pass-prompt.md")
    if condition.review_prompt:
        shutil.copy2(condition.review_prompt, contract / "review-prompt.md")
    shutil.copy2(panel_path, contract / "panel.json")
    if source is not None:
        write_json(
            contract / "source.json",
            {
                "path": str(source),
                "bundle_sha256": sha256_file(source / "bundle.json"),
                "tree_sha256": sha256_tree(source),
            },
        )
    if condition.capability:
        shutil.copytree(condition.capability, contract / "capability")


def run_coverage_replay(
    condition_path: Path,
    panel_path: Path,
    source: Path,
    output: Path,
    parallel: int,
    dry_run: bool,
) -> dict[str, Any]:
    condition_path = condition_path.resolve()
    panel_path = _manifest_path(panel_path)
    source = source.resolve()
    output = output.resolve()
    condition = load_condition(condition_path)
    if condition.adapter != "codex":
        raise RuntimeError("coverage-directed execution requires the Codex adapter")
    health = doctor(condition_path)
    if not health["valid"]:
        raise RuntimeError("condition preflight failed: " + "; ".join(health["failures"]))
    problems = load_problem_collection(panel_path)
    source_attempts = _source_attempts(source, {problem.problem_id for problem in problems})
    if output.exists() and any(output.iterdir()):
        raise RuntimeError(f"refusing to overwrite nonempty run: {output}")
    output.mkdir(parents=True, exist_ok=True)
    (output / "attempts").mkdir()
    _copy_contract(output, condition_path, panel_path, condition, source)
    write_json(
        output / "run.json",
        {
            "schema_version": "coverage-directed-v1",
            "mode": "replay-existing-first-pass",
            "created_at": now(),
            "condition": condition.condition_id,
            "condition_sha256": sha256_file(condition_path),
            "prompt_sha256": sha256_file(condition.review_prompt or condition.prompt),
            "panel_sha256": sha256_file(panel_path),
            "source_bundle_sha256": sha256_file(source / "bundle.json"),
            "problem_count": len(problems),
            "parallel": parallel,
            "dry_run": dry_run,
            "model": condition.model,
            "reasoning_effort": condition.reasoning_effort,
            "auth_method": condition.auth_method,
            "resource_limits": {
                "cpu_quota": condition.cpu_quota,
                "memory_max": condition.memory_max,
                "tasks_max": condition.tasks_max,
                "timeout_seconds": condition.timeout_seconds,
            },
        },
    )
    states = {
        problem.problem_id: {"problem_id": problem.problem_id, "status": "pending"}
        for problem in problems
    }
    write_json(output / "progress.json", {"attempts": list(states.values())})
    if dry_run:
        for problem in problems:
            _, _, codex_home, _ = _stage_attempt(
                output, condition, problem, source_attempts[problem.problem_id]
            )
            _remove_auth_links(codex_home)
            states[problem.problem_id].update({"status": "staged"})
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
            result = _run_replay_attempt(
                output, condition, problem, source_attempts[problem.problem_id]
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
    evaluation = evaluate_coverage_run(output)
    write_json(
        output / "summary.json",
        {
            "attempts": len(problems),
            "archived": sum(row["status"] == "archived" for row in states.values()),
            "failed": sum(row["status"] == "failed" for row in states.values()),
            "valid_outputs": sum(bool(row.get("valid_output")) for row in states.values()),
            "evaluation": evaluation,
        },
    )
    return evaluation


def run_coverage(
    condition_path: Path,
    panel_path: Path,
    output: Path,
    parallel: int,
    dry_run: bool,
) -> dict[str, Any]:
    """Run a fresh solve, review it, and conditionally continue it for every problem."""
    condition_path = condition_path.resolve()
    panel_path = _manifest_path(panel_path)
    output = output.resolve()
    condition = load_condition(condition_path)
    if condition.adapter != "codex":
        raise RuntimeError("coverage-directed execution requires the Codex adapter")
    health = doctor(condition_path)
    if not health["valid"]:
        raise RuntimeError("condition preflight failed: " + "; ".join(health["failures"]))
    if condition.review_prompt is None:
        raise ValueError("coverage condition requires review_prompt")
    if condition.timeout_seconds is None or condition.first_pass_timeout_seconds is None:
        raise ValueError(
            "coverage condition requires a total timeout and a first-pass timeout cap"
        )
    problems = load_problem_collection(panel_path)
    if output.exists() and any(output.iterdir()):
        raise RuntimeError(f"refusing to overwrite nonempty run: {output}")
    output.mkdir(parents=True, exist_ok=True)
    (output / "attempts").mkdir()
    _copy_contract(output, condition_path, panel_path, condition)
    write_json(
        output / "run.json",
        {
            "schema_version": "coverage-directed-v2",
            "mode": "fresh-end-to-end",
            "created_at": now(),
            "condition": condition.condition_id,
            "condition_sha256": sha256_file(condition_path),
            "first_pass_prompt_sha256": sha256_file(condition.prompt),
            "review_prompt_sha256": sha256_file(condition.review_prompt),
            "panel_sha256": sha256_file(panel_path),
            "problem_count": len(problems),
            "parallel": parallel,
            "dry_run": dry_run,
            "model": condition.model,
            "reasoning_effort": condition.reasoning_effort,
            "auth_method": condition.auth_method,
            "resource_limits": {
                "cpu_quota": condition.cpu_quota,
                "memory_max": condition.memory_max,
                "tasks_max": condition.tasks_max,
                "total_timeout_seconds": condition.timeout_seconds,
                "first_pass_timeout_seconds": condition.first_pass_timeout_seconds,
                "review_timeout_policy": "remaining-total-budget",
            },
        },
    )
    states = {
        problem.problem_id: {
            "problem_id": problem.problem_id,
            "status": "pending",
            "stage": "pending",
        }
        for problem in problems
    }
    write_json(output / "progress.json", {"attempts": list(states.values())})
    if dry_run:
        for problem in problems:
            _, _, codex_home, _ = _stage_fresh_first_pass(output, condition, problem)
            _remove_auth_links(codex_home)
            states[problem.problem_id].update(
                {"status": "staged", "stage": "first-pass"}
            )
        write_json(output / "progress.json", {"attempts": list(states.values())})
        return {"staged": len(problems), "output": str(output)}
    lock = threading.Lock()

    def update(problem_id: str, values: dict[str, Any]) -> None:
        with lock:
            states[problem_id].update(values)
            write_json(output / "progress.json", {"attempts": list(states.values())})

    def one(problem: Problem) -> dict[str, Any]:
        update(
            problem.problem_id,
            {"status": "running", "stage": "starting", "started_at": now()},
        )
        try:
            result = _run_end_to_end_attempt(
                output,
                condition,
                problem,
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
    evaluation = evaluate_coverage_run(output)
    write_json(
        output / "summary.json",
        {
            "attempts": len(problems),
            "archived": sum(row["status"] == "archived" for row in states.values()),
            "failed": sum(row["status"] == "failed" for row in states.values()),
            "valid_outputs": sum(bool(row.get("valid_output")) for row in states.values()),
            "evaluation": evaluation,
        },
    )
    return evaluation


def _reference(assignment_path: Path) -> Path:
    assignment = load_json(assignment_path)
    value = Path(str(assignment["reference"]))
    return value.resolve() if value.is_absolute() else (assignment_path.parent / value).resolve()


def evaluate_coverage_run(run_root: Path) -> dict[str, Any]:
    run_root = run_root.resolve()
    rows: list[dict[str, Any]] = []
    for assignment_path in sorted((run_root / "attempts").glob("*/control/assignment.json")):
        assignment = load_json(assignment_path)
        attempt = assignment_path.parents[1]
        problem_id = str(assignment["problem_id"])
        reference = _reference(assignment_path)
        if not reference.is_file():
            raise FileNotFoundError(reference)
        first_pass = attempt / "first-pass/submitted"
        submission = attempt / "submission"
        source_selected = evaluate_selected(reference, first_pass, problem_id)
        source_any = evaluate_workspace(reference, first_pass, problem_id)
        final_selected = evaluate_selected(reference, submission, problem_id)
        final_any = evaluate_workspace(reference, submission, problem_id)
        source_matches = source_any["metrics"]["matched_candidates"]
        final_matches = final_any["metrics"]["matched_candidates"]
        source_selected_exact = bool(source_selected["selected_exact"])
        source_declared_exact = bool(source_any["candidates_exact"])
        final_selected_exact = bool(final_selected["selected_exact"])
        final_declared_exact = bool(final_any["candidates_exact"])
        source_alternative = any(name.startswith("alternative-") for name in source_matches)
        final_alternative = any(name.startswith("alternative-") for name in final_matches)
        decision = load_json(attempt / "decision.json") if (attempt / "decision.json").is_file() else {}
        manifest = (
            load_json(submission / "manifest.json")
            if (submission / "manifest.json").is_file()
            else None
        )
        first_launch = (
            load_json(attempt / "first-pass/run/launch.json")
            if (attempt / "first-pass/run/launch.json").is_file()
            else {}
        )
        review_launch = (
            load_json(attempt / "run/launch.json")
            if (attempt / "run/launch.json").is_file()
            else {}
        )
        row = {
            "problem_id": problem_id,
            "decision": decision.get("decision"),
            "first_pass_selected_exact": source_selected_exact,
            "first_pass_alternative_exact": source_alternative,
            "first_pass_declared_exact": source_declared_exact,
            "source_selected_exact": source_selected_exact,
            "source_alternative_exact": source_alternative,
            "source_declared_exact": source_declared_exact,
            "final_selected_exact": final_selected_exact,
            "final_alternative_exact": final_alternative,
            "final_declared_exact": final_declared_exact,
            "alternative_only_exact": final_declared_exact and not final_selected_exact,
            "selected_only_exact": final_selected_exact and not final_alternative,
            "selected_and_alternative_exact": final_selected_exact and final_alternative,
            "recovered": final_declared_exact and not source_declared_exact,
            "regressed": source_declared_exact and not final_declared_exact,
            "first_pass_elapsed_seconds": first_launch.get("elapsed_seconds"),
            "review_elapsed_seconds": review_launch.get("elapsed_seconds"),
            "total_elapsed_seconds": review_launch.get("total_elapsed_seconds"),
            "first_pass_timed_out": first_launch.get("timed_out"),
            "review_timed_out": review_launch.get("timed_out"),
            "matched_final_candidates": final_any["metrics"]["matched_candidates"],
            "submission_manifest": manifest,
        }
        write_json(attempt / "run/coverage-evaluation.json", row)
        rows.append(row)
    count = len(rows)
    source_misses = sum(not row["source_declared_exact"] for row in rows)
    source_exact = count - source_misses
    summary = {
        "schema_version": "coverage-directed-evaluation-v2",
        "attempts": count,
        "first_pass_selected_exact": sum(row["first_pass_selected_exact"] for row in rows),
        "first_pass_alternative_exact": sum(
            row["first_pass_alternative_exact"] for row in rows
        ),
        "first_pass_declared_exact": sum(row["first_pass_declared_exact"] for row in rows),
        "source_selected_exact": sum(row["source_selected_exact"] for row in rows),
        "source_alternative_exact": sum(row["source_alternative_exact"] for row in rows),
        "source_declared_exact": sum(row["source_declared_exact"] for row in rows),
        "final_selected_exact": sum(row["final_selected_exact"] for row in rows),
        "final_alternative_exact": sum(row["final_alternative_exact"] for row in rows),
        "final_declared_exact": sum(row["final_declared_exact"] for row in rows),
        "alternative_only_exact": sum(row["alternative_only_exact"] for row in rows),
        "selected_only_exact": sum(row["selected_only_exact"] for row in rows),
        "selected_and_alternative_exact": sum(
            row["selected_and_alternative_exact"] for row in rows
        ),
        "selected_to_declared_gain": sum(row["final_declared_exact"] for row in rows)
        - sum(row["final_selected_exact"] for row in rows),
        "recoveries": sum(row["recovered"] for row in rows),
        "regressions": sum(row["regressed"] for row in rows),
        "decisions": {
            "stop": sum(row["decision"] == "stop" for row in rows),
            "continue": sum(row["decision"] == "continue" for row in rows),
            "missing": sum(row["decision"] not in {"stop", "continue"} for row in rows),
        },
        "routing": {
            "source_misses": source_misses,
            "continued_source_misses": sum(
                row["decision"] == "continue" and not row["source_declared_exact"]
                for row in rows
            ),
            "source_exact": source_exact,
            "stopped_source_exact": sum(
                row["decision"] == "stop" and row["source_declared_exact"] for row in rows
            ),
        },
        "rates": {
            "final_selected": (sum(row["final_selected_exact"] for row in rows) / count if count else 0),
            "final_alternative": (
                sum(row["final_alternative_exact"] for row in rows) / count if count else 0
            ),
            "final_declared": (sum(row["final_declared_exact"] for row in rows) / count if count else 0),
        },
        "compute": {
            "first_pass_agent_seconds": sum(
                float(row["first_pass_elapsed_seconds"] or 0) for row in rows
            ),
            "review_agent_seconds": sum(
                float(row["review_elapsed_seconds"] or 0) for row in rows
            ),
            "total_agent_seconds": sum(
                float(row["first_pass_elapsed_seconds"] or 0)
                + float(row["review_elapsed_seconds"] or 0)
                for row in rows
            ),
        },
        "cases": rows,
    }
    evaluation = run_root / "evaluation"
    write_json(evaluation / "summary.json", summary)
    evaluation.mkdir(parents=True, exist_ok=True)
    with (evaluation / "cases.csv").open("w", encoding="utf-8", newline="") as stream:
        fields = [
            "problem_id",
            "decision",
            "first_pass_selected_exact",
            "first_pass_alternative_exact",
            "first_pass_declared_exact",
            "source_selected_exact",
            "source_alternative_exact",
            "source_declared_exact",
            "final_selected_exact",
            "final_alternative_exact",
            "final_declared_exact",
            "alternative_only_exact",
            "selected_only_exact",
            "selected_and_alternative_exact",
            "recovered",
            "regressed",
            "first_pass_elapsed_seconds",
            "review_elapsed_seconds",
            "total_elapsed_seconds",
            "first_pass_timed_out",
            "review_timed_out",
            "matched_final_candidates",
        ]
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            output = {key: row[key] for key in fields}
            output["matched_final_candidates"] = ";".join(row["matched_final_candidates"])
            writer.writerow(output)
    return summary


def coverage_status(run_root: Path) -> dict[str, Any]:
    run_root = run_root.resolve()
    progress_path = run_root / "progress.json"
    if not progress_path.is_file():
        raise FileNotFoundError(progress_path)
    attempts = load_json(progress_path).get("attempts", [])
    result: dict[str, Any] = {
        "run": str(run_root),
        "attempts": len(attempts),
        "pending": sum(row.get("status") == "pending" for row in attempts),
        "running": sum(row.get("status") == "running" for row in attempts),
        "staged": sum(row.get("status") == "staged" for row in attempts),
        "archived": sum(row.get("status") == "archived" for row in attempts),
        "failed": sum(row.get("status") == "failed" for row in attempts),
        "in_first_pass": sum(
            row.get("status") == "running" and row.get("stage") == "first-pass"
            for row in attempts
        ),
        "in_review": sum(
            row.get("status") == "running" and row.get("stage") == "review"
            for row in attempts
        ),
        "in_continuation": sum(
            row.get("status") == "running" and row.get("stage") == "continuation"
            for row in attempts
        ),
        "solver_continuations": sum(int(row.get("continuations", 0)) for row in attempts),
    }
    evaluation = run_root / "evaluation/summary.json"
    if evaluation.is_file():
        summary = load_json(evaluation)
        result["first_pass_selected_exact"] = summary.get(
            "first_pass_selected_exact", summary["source_selected_exact"]
        )
        result["first_pass_declared_exact"] = summary.get(
            "first_pass_declared_exact", summary["source_declared_exact"]
        )
        result["final_selected_exact"] = summary["final_selected_exact"]
        result["final_alternative_exact"] = summary["final_alternative_exact"]
        result["final_declared_exact"] = summary["final_declared_exact"]
        result["alternative_only_exact"] = summary["alternative_only_exact"]
    iterative_evaluation = run_root / "evaluation.json"
    if iterative_evaluation.is_file():
        summary = load_json(iterative_evaluation)
        if summary.get("schema_version") == "iterative-coverage-evaluation-v1":
            for name in (
                "initial_selected_exact",
                "initial_candidates_exact",
                "final_selected_exact",
                "final_candidates_exact",
                "recoveries",
                "regressions",
                "judge_stops",
                "continuation_limits",
                "judge_calls",
            ):
                result[name] = summary[name]
    return result
