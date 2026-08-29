#!/usr/bin/env python3
"""Run the frozen S0 -> J0 -> C1 -> J1 -> S2 -> J2 -> S3 schedule."""

from __future__ import annotations

import argparse
import concurrent.futures
import dataclasses
import hashlib
import shutil
import threading
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from verifiable_pxrd.benchmark import Problem, load_problem_collection
from verifiable_pxrd.condition import Condition, load_condition
from verifiable_pxrd.coverage import (
    FirstPassAttempt,
    _copy_trace,
    _prepare_agent_home,
    _run_agent,
)
from verifiable_pxrd.iterative_coverage import (
    Snapshot,
    _archive_review,
    _stage_case,
    _stage_continuation,
    _stage_review,
)
from verifiable_pxrd.matching import declared_candidates, evaluate_candidates
from verifiable_pxrd.run import _render_prompt as render_solve_prompt
from verifiable_pxrd.run import doctor, now
from verifiable_pxrd.util import sha256_file, sha256_tree, write_json

STAGE_ORDER = ("s0", "j0", "c1", "j1", "s2", "j2", "s3")


@dataclass(frozen=True, slots=True)
class Contract:
    root: Path
    panel: Path
    initial_source: Path
    judge_condition: Path
    solver_condition: Path
    wrapper: Path
    policy: Path
    continuation_prompt: Path
    parallel: int
    judge_timeout: int
    solver_timeout: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(__file__).with_name("experiment.toml"),
    )
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def load_contract(path: Path) -> Contract:
    path = path.resolve()
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    root = Path(__file__).resolve().parents[3]

    def resolve(key: str) -> Path:
        return (root / str(data[key])).resolve()

    schedule = tuple(data["schedule"])
    if schedule != STAGE_ORDER:
        raise ValueError(f"unsupported schedule: {schedule}")
    parallel = int(data["parallel_agent_calls"])
    if not 1 <= parallel <= 16:
        raise ValueError("parallel_agent_calls must be between 1 and 16")
    return Contract(
        root=root,
        panel=resolve("panel"),
        initial_source=resolve("initial_source"),
        judge_condition=resolve("judge_condition"),
        solver_condition=resolve("solver_condition"),
        wrapper=resolve("judge_wrapper"),
        policy=resolve("judge_policy"),
        continuation_prompt=resolve("continuation_prompt"),
        parallel=parallel,
        judge_timeout=int(data["judge_timeout_seconds"]),
        solver_timeout=int(data["solver_timeout_seconds"]),
    )


def initial_attempts(source: Path, problem_ids: set[str]) -> dict[str, FirstPassAttempt]:
    attempts: dict[str, FirstPassAttempt] = {}
    for problem_id in sorted(problem_ids):
        root = source / "attempts" / problem_id / "initial"
        trace = root / "codex-events.jsonl.gz"
        if not trace.is_file():
            raise FileNotFoundError(trace)
        final_response = root / "final-answer.md"
        candidates = tuple(declared_candidates(root / "submission"))
        attempts[problem_id] = FirstPassAttempt(
            problem_id=problem_id,
            root=root,
            trace=trace,
            final_response=final_response if final_response.is_file() else None,
            candidates=candidates,
        )
    return attempts


def snapshot_from_stage(stage: Path, label: str) -> Snapshot:
    return Snapshot(
        label=label,
        root=stage,
        trace=stage / "trace.jsonl",
        final_response=stage / "final-response.md",
        candidates=tuple(declared_candidates(stage / "submitted")),
    )


def archive_solver(stage: Path, label: str) -> Snapshot:
    workspace = stage / "workspace"
    submitted = stage / "submitted"
    submitted.mkdir(exist_ok=False)
    records = []
    for candidate in declared_candidates(workspace):
        destination = submitted / candidate.name
        shutil.copy2(candidate, destination)
        records.append({"file": destination.name, "sha256": sha256_file(destination)})
    trace = stage / "trace.jsonl"
    _copy_trace(stage / "run/codex-events.jsonl", trace)
    final_response = stage / "final-response.md"
    captured = stage / "run/final-answer.md"
    if captured.is_file():
        shutil.copy2(captured, final_response)
    else:
        final_response.write_text("No final response was captured.\n", encoding="utf-8")
    write_json(
        stage / "manifest.json",
        {
            "schema_version": "verifier-gated-snapshot-v1",
            "label": label,
            "workspace_sha256": sha256_tree(workspace),
            "trace_sha256": sha256_file(trace),
            "final_response_sha256": sha256_file(final_response),
            "candidates": records,
        },
    )
    return snapshot_from_stage(stage, label)


def stage_fresh(
    attempt: Path,
    condition: Condition,
    problem: Problem,
    index: int,
) -> tuple[Path, Path, Path, str]:
    stage = attempt / "rounds" / f"fresh-{index:02d}"
    workspace = stage / "workspace"
    codex_home = stage / "codex-home"
    run_dir = stage / "run"
    run_dir.mkdir(parents=True)
    _prepare_agent_home(condition, workspace, codex_home)
    shutil.copy2(problem.pattern, workspace / "pattern.csv")
    prompt = render_solve_prompt(condition, problem, workspace)
    (stage / "prompt.md").write_text(prompt, encoding="utf-8")
    write_json(
        stage / "input.json",
        {
            "schema_version": "verifier-gated-fresh-input-v1",
            "fresh_index": index,
            "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
            "receives_prior_trace": False,
            "receives_prior_candidates": False,
            "receives_review": False,
        },
    )
    return workspace, codex_home, run_dir, prompt


def run_review(
    attempt: Path,
    condition: Condition,
    problem: Problem,
    snapshot: Snapshot,
    index: int,
    wrapper: str,
    policy: str,
    timeout: int,
) -> dict[str, Any]:
    for retry in range(2):
        if retry:
            original = attempt / "rounds" / f"review-{index:02d}"
            failed = attempt / "rounds" / f"review-{index:02d}-failed-{retry:02d}"
            if original.exists():
                original.rename(failed)
        workspace, codex_home, run_dir, prompt = _stage_review(
            attempt, condition, problem, snapshot, index, wrapper, policy
        )
        _run_agent(
            condition,
            workspace,
            codex_home,
            run_dir,
            prompt,
            f"verifier-gated-review-{problem.problem_id}-{index}-{retry}",
            float(timeout),
        )
        try:
            return _archive_review(attempt / "rounds" / f"review-{index:02d}")
        except Exception:
            if retry:
                raise
    raise AssertionError("unreachable")


def run_continuation(
    attempt: Path,
    condition: Condition,
    problem: Problem,
    snapshot: Snapshot,
    decision_path: Path,
    template: str,
    timeout: int,
) -> Snapshot:
    workspace, codex_home, run_dir, prompt = _stage_continuation(
        attempt, condition, problem, snapshot, 1, decision_path, template
    )
    _run_agent(
        condition,
        workspace,
        codex_home,
        run_dir,
        prompt,
        f"verifier-gated-continuation-{problem.problem_id}",
        float(timeout),
    )
    return archive_solver(attempt / "rounds/continuation-01", "continuation-01")


def run_fresh(
    attempt: Path,
    condition: Condition,
    problem: Problem,
    index: int,
    timeout: int,
) -> Snapshot:
    workspace, codex_home, run_dir, prompt = stage_fresh(attempt, condition, problem, index)
    _run_agent(
        condition,
        workspace,
        codex_home,
        run_dir,
        prompt,
        f"verifier-gated-fresh-{problem.problem_id}-{index}",
        float(timeout),
    )
    return archive_solver(attempt / "rounds" / f"fresh-{index:02d}", f"fresh-{index:02d}")


def evaluate_snapshot(reference: Path, problem_id: str, snapshot: Snapshot) -> dict[str, Any]:
    result = evaluate_candidates(reference, snapshot.candidates, problem_id)
    return {
        "label": snapshot.label,
        "selected_exact": bool(result["selected_exact"]),
        "candidates_exact": bool(result["candidates_exact"]),
        "candidate_count": len(snapshot.candidates),
        "matched_candidates": result["metrics"]["matched_candidates"],
    }


def materialize_pool(
    attempt: Path,
    reference: Path,
    problem_id: str,
    snapshots: list[Snapshot],
    decisions: list[dict[str, Any]],
    termination: str,
) -> dict[str, Any]:
    pool = attempt / "candidate-pool"
    pool.mkdir()
    all_candidates: list[Path] = []
    records = []
    for snapshot in snapshots:
        for candidate in snapshot.candidates:
            destination = pool / f"{snapshot.label}--{candidate.name}"
            shutil.copy2(candidate, destination)
            all_candidates.append(candidate)
            records.append(
                {
                    "snapshot": snapshot.label,
                    "source_name": candidate.name,
                    "file": destination.name,
                    "sha256": sha256_file(destination),
                }
            )
    cumulative = evaluate_candidates(reference, all_candidates, problem_id)
    result = {
        "schema_version": "verifier-gated-case-v1",
        "problem_id": problem_id,
        "termination": termination,
        "snapshots": [evaluate_snapshot(reference, problem_id, item) for item in snapshots],
        "reviews": decisions,
        "candidate_pool": records,
        "cumulative_selected_exact": bool(cumulative["selected_exact"]),
        "cumulative_candidates_exact": bool(cumulative["candidates_exact"]),
        "cumulative_matched_candidates": cumulative["metrics"]["matched_candidates"],
    }
    write_json(attempt / "chain.json", result)
    return result


def copy_contract(output: Path, config: Path, contract: Contract, solver: Condition) -> None:
    destination = output / "contract"
    destination.mkdir()
    for source, name in (
        (config, "experiment.toml"),
        (contract.panel, "panel.json"),
        (contract.judge_condition, "judge-condition.toml"),
        (contract.solver_condition, "solver-condition.toml"),
        (contract.wrapper, "judge-wrapper.md"),
        (contract.policy, "judge-policy.md"),
        (contract.continuation_prompt, "continuation-prompt.md"),
        (Path(__file__).resolve(), "run.py"),
    ):
        shutil.copy2(source, destination / name)
    if solver.capability:
        shutil.copytree(solver.capability, destination / "capability")


def main() -> int:
    args = parse_args()
    config = args.config.resolve()
    contract = load_contract(config)
    for path in (
        contract.panel,
        contract.initial_source,
        contract.judge_condition,
        contract.solver_condition,
        contract.wrapper,
        contract.policy,
        contract.continuation_prompt,
    ):
        if not path.exists():
            raise FileNotFoundError(path)

    output = args.output.resolve()
    if output.exists() and any(output.iterdir()):
        raise RuntimeError(f"refusing to overwrite nonempty output: {output}")
    output.mkdir(parents=True, exist_ok=True)

    judge = dataclasses.replace(
        load_condition(contract.judge_condition), timeout_seconds=contract.judge_timeout
    )
    solver = dataclasses.replace(
        load_condition(contract.solver_condition), timeout_seconds=contract.solver_timeout
    )
    for condition_path in (contract.judge_condition, contract.solver_condition):
        health = doctor(condition_path)
        if not health["valid"]:
            raise RuntimeError(f"condition preflight failed: {health['failures']}")

    problems = load_problem_collection(contract.panel)
    problem_ids = {problem.problem_id for problem in problems}
    sources = initial_attempts(contract.initial_source, problem_ids)
    wrapper = contract.wrapper.read_text(encoding="utf-8")
    policy = contract.policy.read_text(encoding="utf-8")
    continuation_template = contract.continuation_prompt.read_text(encoding="utf-8")
    copy_contract(output, config, contract, solver)
    write_json(
        output / "run.json",
        {
            "schema_version": "verifier-gated-run-v1",
            "created_at": now(),
            "schedule": list(STAGE_ORDER),
            "problem_count": len(problems),
            "parallel_agent_calls": contract.parallel,
            "judge_timeout_seconds": contract.judge_timeout,
            "solver_timeout_seconds": contract.solver_timeout,
            "judge_condition": judge.condition_id,
            "solver_condition": solver.condition_id,
            "judge_model": judge.model,
            "solver_model": solver.model,
            "oracle_available_to_agents": False,
            "initial_source_sha256": sha256_file(contract.initial_source / "bundle.json"),
        },
    )

    states = {
        problem.problem_id: {
            "problem_id": problem.problem_id,
            "status": "pending",
            "stage": "pending",
            "stages": {},
        }
        for problem in problems
    }
    lock = threading.Lock()

    def flush() -> None:
        write_json(output / "progress.json", {"updated_at": now(), "attempts": list(states.values())})

    def update(problem_id: str, values: dict[str, Any]) -> None:
        with lock:
            states[problem_id].update(values)
            flush()

    def stage_result(problem_id: str, stage: str, value: dict[str, Any]) -> None:
        with lock:
            states[problem_id]["stages"][stage] = value
            states[problem_id]["stage"] = stage
            flush()

    flush()

    def one(problem: Problem) -> None:
        problem_id = problem.problem_id
        update(problem_id, {"status": "running", "started_at": now()})
        try:
            attempt, current = _stage_case(
                output, problem, sources[problem_id], judge, solver
            )
            reference = attempt / "control/reference.cif"
            snapshots = [current]
            decisions: list[dict[str, Any]] = []
            stage_result(problem_id, "s0", {"status": "complete", **evaluate_snapshot(reference, problem_id, current)})

            j0 = run_review(attempt, judge, problem, current, 0, wrapper, policy, contract.judge_timeout)
            decisions.append({"review_index": 0, "snapshot": current.label, **j0})
            stage_result(problem_id, "j0", {"status": "complete", **j0})
            if j0["decision"] == "stop":
                result = materialize_pool(attempt, reference, problem_id, snapshots, decisions, "judge-stop-j0")
                update(problem_id, {"status": "complete", "stage": "complete", "result": result, "ended_at": now()})
                return

            current = run_continuation(
                attempt,
                solver,
                problem,
                current,
                attempt / "rounds/review-00/decision.json",
                continuation_template,
                contract.solver_timeout,
            )
            snapshots.append(current)
            stage_result(problem_id, "c1", {"status": "complete", **evaluate_snapshot(reference, problem_id, current)})

            j1 = run_review(attempt, judge, problem, current, 1, wrapper, policy, contract.judge_timeout)
            decisions.append({"review_index": 1, "snapshot": current.label, **j1})
            stage_result(problem_id, "j1", {"status": "complete", **j1})
            if j1["decision"] == "stop":
                result = materialize_pool(attempt, reference, problem_id, snapshots, decisions, "judge-stop-j1")
                update(problem_id, {"status": "complete", "stage": "complete", "result": result, "ended_at": now()})
                return

            current = run_fresh(attempt, solver, problem, 2, contract.solver_timeout)
            snapshots.append(current)
            stage_result(problem_id, "s2", {"status": "complete", **evaluate_snapshot(reference, problem_id, current)})

            j2 = run_review(attempt, judge, problem, current, 2, wrapper, policy, contract.judge_timeout)
            decisions.append({"review_index": 2, "snapshot": current.label, **j2})
            stage_result(problem_id, "j2", {"status": "complete", **j2})
            if j2["decision"] == "stop":
                result = materialize_pool(attempt, reference, problem_id, snapshots, decisions, "judge-stop-j2")
                update(problem_id, {"status": "complete", "stage": "complete", "result": result, "ended_at": now()})
                return

            current = run_fresh(attempt, solver, problem, 3, contract.solver_timeout)
            snapshots.append(current)
            stage_result(problem_id, "s3", {"status": "complete", **evaluate_snapshot(reference, problem_id, current)})
            result = materialize_pool(attempt, reference, problem_id, snapshots, decisions, "solver-limit")
            update(problem_id, {"status": "complete", "stage": "complete", "result": result, "ended_at": now()})
        except Exception as error:
            update(
                problem_id,
                {
                    "status": "failed",
                    "error": f"{type(error).__name__}: {error}",
                    "ended_at": now(),
                },
            )

    with concurrent.futures.ThreadPoolExecutor(max_workers=contract.parallel) as executor:
        futures = [executor.submit(one, problem) for problem in problems]
        for future in concurrent.futures.as_completed(futures):
            future.result()

    summary = {
        "schema_version": "verifier-gated-summary-v1",
        "ended_at": now(),
        "cases": len(states),
        "complete": sum(item["status"] == "complete" for item in states.values()),
        "failed": sum(item["status"] == "failed" for item in states.values()),
        "results": list(states.values()),
    }
    write_json(output / "summary.json", summary)
    flush()
    return 0 if summary["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
