from __future__ import annotations

import datetime as dt
import os
import re
import shlex
import shutil
import subprocess
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .benchmark import Problem, load_problem_collection
from .condition import load_condition
from .matching import exact_outcomes
from .run import doctor as condition_doctor
from .run import run_panel
from .util import expand_path, load_json, sha256_file, sha256_tree, write_json


def _now() -> str:
    return dt.datetime.now(dt.UTC).isoformat()


@dataclass(frozen=True, slots=True)
class HarnessConfig:
    config_path: Path
    project_id: str
    curriculum: Path
    order: Path
    condition: Path
    baseline_condition: Path | None
    capability: Path
    runtime_environment: Path | None
    state_dir: Path
    run_root: Path
    bootstrap_size: int
    wave_size: int
    parallel: int


def load_harness_config(path: Path) -> HarnessConfig:
    path = path.resolve()
    with path.open("rb") as stream:
        raw = tomllib.load(stream)
    base = path.parent
    return HarnessConfig(
        config_path=path,
        project_id=str(raw["id"]),
        curriculum=expand_path(str(raw["curriculum"]), base),
        order=expand_path(str(raw["order"]), base),
        condition=expand_path(str(raw["condition"]), base),
        baseline_condition=(
            expand_path(str(raw["baseline_condition"]), base)
            if raw.get("baseline_condition")
            else None
        ),
        capability=expand_path(str(raw["capability"]), base),
        runtime_environment=(
            expand_path(str(raw["runtime_environment"]), base)
            if raw.get("runtime_environment")
            else None
        ),
        state_dir=expand_path(str(raw.get("state_dir", ".state")), base),
        run_root=expand_path(str(raw.get("run_root", ".runs")), base),
        bootstrap_size=int(raw.get("bootstrap_size", 20)),
        wave_size=int(raw.get("wave_size", 4)),
        parallel=int(raw.get("parallel", 4)),
    )


def _activate_runtime_environment(config: HarnessConfig) -> None:
    path = config.runtime_environment
    if path is None or not path.is_file():
        return
    for number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line.removeprefix("export ").lstrip()
        if "=" not in line:
            raise ValueError(f"invalid runtime environment line {number}: {path}")
        key, value = line.split("=", 1)
        key = key.strip()
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
            raise ValueError(f"invalid environment name on line {number}: {key}")
        words = shlex.split(value.strip())
        if len(words) != 1:
            raise ValueError(f"invalid environment value on line {number}: {path}")
        os.environ[key] = os.path.expanduser(os.path.expandvars(words[0]))


def _order(config: HarnessConfig) -> list[str]:
    return [
        line.strip()
        for line in config.order.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def _problem_map(config: HarnessConfig) -> dict[str, Problem]:
    return {problem.problem_id: problem for problem in load_problem_collection(config.curriculum)}


def _ledger_path(config: HarnessConfig) -> Path:
    return config.state_dir / "ledger.json"


def _load_ledger(config: HarnessConfig) -> dict[str, Any]:
    path = _ledger_path(config)
    if path.is_file():
        return load_json(path)
    return {
        "schema_version": "1",
        "project_id": config.project_id,
        "created_at": _now(),
        "imports": [],
        "waves": [],
    }


def _save_ledger(config: HarnessConfig, ledger: dict[str, Any]) -> None:
    ledger["updated_at"] = _now()
    write_json(_ledger_path(config), ledger)


def _git_state(path: Path) -> dict[str, Any]:
    process = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
        text=True,
        capture_output=True,
        check=False,
    )
    if process.returncode:
        return {"repository": None, "commit": None, "dirty": None}
    repository = Path(process.stdout.strip())
    commit = subprocess.run(
        ["git", "-C", str(repository), "rev-parse", "HEAD"],
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()
    status = subprocess.run(
        ["git", "-C", str(repository), "status", "--porcelain"],
        text=True,
        capture_output=True,
        check=True,
    ).stdout
    return {"repository": str(repository), "commit": commit, "dirty": bool(status.strip())}


def harness_doctor(config_path: Path) -> dict[str, Any]:
    config = load_harness_config(config_path)
    _activate_runtime_environment(config)
    failures: list[str] = []
    required = [config.curriculum, config.order, config.condition, config.capability]
    if config.baseline_condition is not None:
        required.append(config.baseline_condition)
    for item in required:
        if not item.exists():
            failures.append(f"missing required path: {item}")
    order: list[str] = []
    problems: dict[str, Problem] = {}
    if config.order.is_file():
        order = _order(config)
        if len(order) != len(set(order)):
            failures.append("training order contains duplicate identifiers")
    if config.curriculum.is_file():
        try:
            problems = _problem_map(config)
        except Exception as error:
            failures.append(f"invalid curriculum: {type(error).__name__}: {error}")
    if problems and set(order) != set(problems):
        failures.append("training order and curriculum identifiers differ")
    if config.capability.is_dir() and not (config.capability / "SKILL.md").is_file():
        failures.append(f"active capability has no SKILL.md: {config.capability}")
    condition_result: dict[str, Any] | None = None
    baseline_result: dict[str, Any] | None = None
    if config.condition.is_file():
        try:
            condition = load_condition(config.condition)
            if condition.capability != config.capability:
                failures.append("condition capability does not match continual-harness capability")
            condition_result = condition_doctor(config.condition)
            failures.extend(
                f"condition: {message}" for message in condition_result.get("failures", [])
            )
        except Exception as error:
            failures.append(f"invalid condition: {type(error).__name__}: {error}")
    if config.baseline_condition is not None and config.baseline_condition.is_file():
        try:
            baseline = load_condition(config.baseline_condition)
            if baseline.capability is not None:
                failures.append("baseline condition must not include a capability")
            if config.condition.is_file():
                learned = load_condition(config.condition)
                comparable_fields = (
                    "model",
                    "reasoning_effort",
                    "prompt",
                    "path_entries",
                    "read_paths",
                    "optional_read_paths",
                    "deny_paths",
                    "variables",
                    "cpu_quota",
                    "memory_max",
                    "tasks_max",
                    "timeout_seconds",
                    "network",
                    "systemd_scope",
                    "auth_method",
                )
                differing = [
                    name
                    for name in comparable_fields
                    if getattr(baseline, name) != getattr(learned, name)
                ]
                if differing:
                    failures.append(
                        "baseline and learned conditions differ beyond capability: "
                        + ", ".join(differing)
                    )
            baseline_result = condition_doctor(config.baseline_condition)
            failures.extend(
                f"baseline condition: {message}" for message in baseline_result.get("failures", [])
            )
        except Exception as error:
            failures.append(f"invalid baseline condition: {type(error).__name__}: {error}")
    return {
        "project_id": config.project_id,
        "curriculum_problems": len(problems),
        "ordered_problems": len(order),
        "bootstrap_size": config.bootstrap_size,
        "wave_size": config.wave_size,
        "parallel": config.parallel,
        "condition": condition_result,
        "baseline_condition": baseline_result,
        "git": _git_state(config.config_path.parent),
        "valid": not failures,
        "failures": failures,
    }


def _assignment_for_attempt(attempt: Path) -> tuple[Path, dict[str, Any]]:
    for path in (attempt / "control/assignment.json", attempt / "assignment.json"):
        if path.is_file():
            return path, load_json(path)
    raise FileNotFoundError(f"no assignment record under {attempt}")


def _result_for_attempt(attempt: Path) -> tuple[Path, dict[str, Any]]:
    for path in (attempt / "run/verifier-result.json", attempt / "verifier/result.json"):
        if path.is_file():
            return path, load_json(path)
    raise FileNotFoundError(f"no verifier result under {attempt}")


def _attempt_records(run_root: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for attempt in sorted((run_root / "attempts").glob("*")):
        if not attempt.is_dir():
            continue
        try:
            assignment_path, assignment = _assignment_for_attempt(attempt)
            result_path, result = _result_for_attempt(attempt)
        except FileNotFoundError:
            continue
        problem_id = str(assignment.get("problem_id", assignment.get("case_id", "")))
        if not problem_id:
            raise ValueError(f"assignment has no problem identifier: {assignment_path}")
        launch_path = attempt / "run/launch.json"
        launch = load_json(launch_path) if launch_path.is_file() else {}
        selected_exact, candidates_exact = exact_outcomes(result)
        records.append(
            {
                "problem_id": problem_id,
                "attempt_id": str(assignment.get("attempt_id", attempt.name)),
                "attempt": attempt,
                "assignment": assignment_path,
                "result": result_path,
                "exact_success": selected_exact,
                "selected_exact": selected_exact,
                "candidates_exact": candidates_exact,
                "timed_out": bool(launch.get("timed_out", False)),
            }
        )
    return records


def _safe_label(value: str) -> str:
    label = re.sub(r"[^a-zA-Z0-9._-]+", "-", value).strip("-.")
    if not label:
        raise ValueError("label must contain at least one alphanumeric character")
    return label


def _copy_workspace(source: Path, destination: Path) -> None:
    if not source.is_dir():
        return
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns(".cache", ".tmp", ".git", "__pycache__", "*.pyc"),
    )


def import_training_run(config_path: Path, source: Path, label: str) -> dict[str, Any]:
    config = load_harness_config(config_path)
    source = source.resolve()
    label = _safe_label(label)
    destination = config.run_root / "imports" / label
    if destination.exists():
        raise FileExistsError(destination)
    problems = _problem_map(config)
    records = _attempt_records(source)
    if not records:
        raise ValueError(f"no closed attempts found in {source}")
    problem_ids = [str(record["problem_id"]) for record in records]
    if len(problem_ids) != len(set(problem_ids)):
        raise ValueError("import contains repeated problem identifiers")
    unknown = sorted(set(problem_ids) - set(problems))
    if unknown:
        raise ValueError(f"import contains problems outside the curriculum: {unknown}")
    destination.mkdir(parents=True)
    normalized: list[dict[str, Any]] = []
    for record in records:
        problem = problems[str(record["problem_id"])]
        source_attempt = Path(record["attempt"])
        target = destination / "attempts" / source_attempt.name
        (target / "control").mkdir(parents=True)
        (target / "run").mkdir()
        shutil.copy2(record["assignment"], target / "control/source-assignment.json")
        if (source_attempt / "run").is_dir():
            shutil.copytree(
                source_attempt / "run",
                target / "run",
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns("*.sqlite", "*.sqlite-shm", "*.sqlite-wal"),
            )
        shutil.copy2(record["result"], target / "run/verifier-result.json")
        if (source_attempt / "prompt.txt").is_file():
            shutil.copy2(source_attempt / "prompt.txt", target / "prompt.txt")
        _copy_workspace(source_attempt / "workspace", target / "workspace")
        shutil.copy2(problem.reference, target / "control/reference.cif")
        write_json(
            target / "control/assignment.json",
            {
                "attempt_id": record["attempt_id"],
                "problem_id": problem.problem_id,
                "formula": problem.formula,
                "reference": "reference.cif",
                "reference_sha256": sha256_file(problem.reference),
                "pattern_sha256": sha256_file(problem.pattern),
                "source_run": str(source),
            },
        )
        write_json(
            target / "episode.json",
            {
                "schema_version": "1",
                "attempt_id": record["attempt_id"],
                "problem_id": problem.problem_id,
                "exact_success": record["exact_success"],
                "selected_exact": record["selected_exact"],
                "candidates_exact": record["candidates_exact"],
                "timed_out": record["timed_out"],
                "closed": True,
                "paths": {
                    "prompt": "prompt.txt",
                    "events": "run/codex-events.jsonl",
                    "final_answer": "run/final-answer.md",
                    "verifier": "run/verifier-result.json",
                    "workspace": "workspace",
                    "reference": "control/reference.cif",
                },
            },
        )
        normalized.append(
            {
                "attempt_id": record["attempt_id"],
                "problem_id": problem.problem_id,
                "exact_success": record["exact_success"],
                "selected_exact": record["selected_exact"],
                "candidates_exact": record["candidates_exact"],
                "timed_out": record["timed_out"],
                "episode": str((target / "episode.json").relative_to(config.run_root)),
            }
        )
    for name in ("experiment.json", "progress.json", "roster.json", "run.json", "summary.json"):
        if (source / name).is_file():
            shutil.copy2(source / name, destination / f"source-{name}")
    summary = {
        "schema_version": "1",
        "label": label,
        "role": "baseline",
        "imported_at": _now(),
        "source": str(source),
        "attempts": len(normalized),
        "exact": sum(bool(item["selected_exact"]) for item in normalized),
        "selected_exact": sum(bool(item["selected_exact"]) for item in normalized),
        "candidates_exact": sum(bool(item["candidates_exact"]) for item in normalized),
        "records": normalized,
    }
    write_json(destination / "summary.json", summary)
    ledger = _load_ledger(config)
    ledger["imports"].append(
        {
            "label": label,
            "role": "baseline",
            "path": str(destination.relative_to(config.run_root)),
            "attempts": len(normalized),
            "exact": summary["exact"],
            "selected_exact": summary["selected_exact"],
            "candidates_exact": summary["candidates_exact"],
            "problem_ids": problem_ids,
            "imported_at": summary["imported_at"],
        }
    )
    _save_ledger(config, ledger)
    return summary


def _seen_problem_ids(ledger: dict[str, Any]) -> set[str]:
    seen: set[str] = set()
    for item in ledger.get("imports", []):
        seen.update(str(value) for value in item.get("problem_ids", []))
    for item in ledger.get("waves", []):
        seen.update(str(value) for value in item.get("problem_ids", []))
    return seen


def _baseline_problem_ids(config: HarnessConfig, ledger: dict[str, Any]) -> set[str]:
    seen: set[str] = set()
    for item in ledger.get("imports", []):
        if item.get("role") == "baseline":
            seen.update(str(value) for value in item.get("problem_ids", []))
    for item in ledger.get("waves", []):
        if item.get("role") != "baseline" or item.get("dry_run"):
            continue
        output = config.config_path.parent / str(item.get("output", ""))
        summary = output / "summary.json"
        progress = output / "progress.json"
        payload = (
            load_json(summary)
            if summary.is_file()
            else load_json(progress)
            if progress.is_file()
            else {}
        )
        records = payload.get("results", payload.get("attempts", []))
        seen.update(
            str(record["problem_id"])
            for record in records
            if record.get("status") == "archived" and record.get("problem_id")
        )
    return seen


def select_wave_ids(
    config: HarnessConfig,
    *,
    next_count: int | None = None,
    problem_ids: list[str] | None = None,
) -> list[str]:
    problems = _problem_map(config)
    if problem_ids:
        unknown = [problem_id for problem_id in problem_ids if problem_id not in problems]
        if unknown:
            raise ValueError(f"unknown problem identifiers: {unknown}")
        if len(problem_ids) != len(set(problem_ids)):
            raise ValueError("wave contains duplicate problem identifiers")
        return problem_ids
    count = next_count if next_count is not None else config.wave_size
    if count < 1:
        raise ValueError("next count must be positive")
    seen = _seen_problem_ids(_load_ledger(config))
    return [problem_id for problem_id in _order(config) if problem_id not in seen][:count]


def select_baseline_ids(
    config: HarnessConfig,
    *,
    next_count: int | None = None,
    problem_ids: list[str] | None = None,
    all_missing: bool = False,
) -> list[str]:
    problems = _problem_map(config)
    if problem_ids:
        unknown = [problem_id for problem_id in problem_ids if problem_id not in problems]
        if unknown:
            raise ValueError(f"unknown problem identifiers: {unknown}")
        if len(problem_ids) != len(set(problem_ids)):
            raise ValueError("baseline wave contains duplicate problem identifiers")
        requested = problem_ids
    else:
        missing = [
            problem_id
            for problem_id in _order(config)
            if problem_id not in _baseline_problem_ids(config, _load_ledger(config))
        ]
        if all_missing:
            return missing
        count = next_count if next_count is not None else config.bootstrap_size
        if count < 1:
            raise ValueError("next count must be positive")
        requested = missing[:count]
    already_closed = _baseline_problem_ids(config, _load_ledger(config))
    return [problem_id for problem_id in requested if problem_id not in already_closed]


def _write_panel(config: HarnessConfig, problem_ids: list[str], path: Path) -> None:
    problems = _problem_map(config)
    cases = []
    for problem_id in problem_ids:
        problem = problems[problem_id]
        problem_root = path.parent / "problems" / problem_id
        problem_root.mkdir(parents=True, exist_ok=True)
        pattern = problem_root / "pattern.csv"
        reference = problem_root / "reference.cif"
        shutil.copy2(problem.pattern, pattern)
        shutil.copy2(problem.reference, reference)
        cases.append(
            {
                "case_id": problem.problem_id,
                "formula": problem.formula,
                "pattern_path": os.path.relpath(pattern, path.parent),
                "reference_path": os.path.relpath(reference, path.parent),
                "wavelength": problem.wavelength,
                "radiation": problem.radiation,
            }
        )
    write_json(
        path,
        {
            "schema_version": "1",
            "panel_id": path.stem,
            "description": "Frozen continual-harness training wave.",
            "path_root": ".",
            "cases": cases,
        },
    )


def _launch_training_run(
    config: HarnessConfig,
    *,
    condition_path: Path,
    selected: list[str],
    role: str,
    parallel: int | None,
    label: str | None,
    dry_run: bool,
) -> dict[str, Any]:
    if not selected:
        kind = "baseline" if role == "baseline" else "training"
        raise RuntimeError(f"no unattempted {kind} problems remain")
    ledger = _load_ledger(config)
    sequence = len(ledger.get("waves", [])) + 1
    default_label = f"baseline-{sequence:03d}" if role == "baseline" else f"wave-{sequence:03d}"
    label = _safe_label(label or default_label)
    output = config.run_root / ("baselines" if role == "baseline" else "waves") / label
    panel = config.state_dir / "panels" / f"{label}.json"
    if output.exists() or panel.exists():
        raise FileExistsError(f"wave label already exists: {label}")
    _write_panel(config, selected, panel)
    git = _git_state(config.config_path.parent)
    condition = load_condition(condition_path)
    record = {
        "label": label,
        "role": role,
        "status": "launching",
        "problem_ids": selected,
        "panel": str(panel.relative_to(config.config_path.parent)),
        "output": str(output.relative_to(config.config_path.parent)),
        "condition": str(condition_path),
        "capability_sha256": (
            sha256_tree(condition.capability) if condition.capability is not None else None
        ),
        "git_commit": git["commit"],
        "git_dirty": git["dirty"],
        "started_at": _now(),
        "dry_run": dry_run,
    }
    ledger["waves"].append(record)
    _save_ledger(config, ledger)
    try:
        result = run_panel(
            condition_path,
            panel,
            output,
            parallel or config.parallel,
            1,
            1,
            dry_run,
        )
    except BaseException as error:
        record["status"] = "interrupted" if isinstance(error, KeyboardInterrupt) else "failed"
        record["error"] = f"{type(error).__name__}: {error}"
        record["ended_at"] = _now()
        _save_ledger(config, ledger)
        raise
    record["status"] = "staged" if dry_run else "closed"
    record["ended_at"] = _now()
    attempts = result.get("attempts", result.get("staged", 0))
    record["attempts"] = len(attempts) if isinstance(attempts, list) else int(attempts)
    record["exact"] = int(result.get("exact", 0))
    record["selected_exact"] = int(result.get("selected_exact", record["exact"]))
    record["candidates_exact"] = int(result.get("candidates_exact", record["exact"]))
    _save_ledger(config, ledger)
    return {"wave": record, "result": result}


def launch_training_baseline(
    config_path: Path,
    *,
    problem_ids: list[str] | None,
    next_count: int | None,
    all_missing: bool,
    parallel: int | None,
    label: str | None,
    dry_run: bool,
) -> dict[str, Any]:
    config = load_harness_config(config_path)
    _activate_runtime_environment(config)
    health = harness_doctor(config_path)
    if not health["valid"]:
        raise RuntimeError("harness preflight failed: " + "; ".join(health["failures"]))
    if config.baseline_condition is None:
        raise RuntimeError("harness has no baseline_condition")
    selected = select_baseline_ids(
        config,
        next_count=next_count,
        problem_ids=problem_ids,
        all_missing=all_missing,
    )
    return _launch_training_run(
        config,
        condition_path=config.baseline_condition,
        selected=selected,
        role="baseline",
        parallel=parallel,
        label=label,
        dry_run=dry_run,
    )


def launch_training_wave(
    config_path: Path,
    *,
    problem_ids: list[str] | None,
    next_count: int | None,
    parallel: int | None,
    label: str | None,
    dry_run: bool,
) -> dict[str, Any]:
    config = load_harness_config(config_path)
    _activate_runtime_environment(config)
    health = harness_doctor(config_path)
    if not health["valid"]:
        raise RuntimeError("harness preflight failed: " + "; ".join(health["failures"]))
    selected = select_wave_ids(config, next_count=next_count, problem_ids=problem_ids)
    return _launch_training_run(
        config,
        condition_path=config.condition,
        selected=selected,
        role="learned",
        parallel=parallel,
        label=label,
        dry_run=dry_run,
    )


def _stored_exact_outcomes(
    record: dict[str, Any], result_path: Path | None = None
) -> tuple[bool, bool]:
    if "selected_exact" in record and "candidates_exact" in record:
        return bool(record["selected_exact"]), bool(record["candidates_exact"])
    if result_path is not None and result_path.is_file():
        return exact_outcomes(load_json(result_path))
    legacy = bool(record.get("exact_success", False))
    return legacy, legacy


def training_status(config_path: Path) -> dict[str, Any]:
    config = load_harness_config(config_path)
    ledger = _load_ledger(config)
    order = _order(config)
    baseline_attempts = 0
    baseline_selected_exact = 0
    baseline_candidates_exact = 0
    learned_attempts = 0
    learned_selected_exact = 0
    learned_candidates_exact = 0
    attempt_counts: dict[str, int] = {}
    selected_exact_ids: set[str] = set()
    candidates_exact_ids: set[str] = set()
    evidence: list[dict[str, Any]] = []
    wave_views: list[dict[str, Any]] = []
    for item in ledger.get("imports", []):
        summary_path = config.run_root / str(item["path"]) / "summary.json"
        if not summary_path.is_file():
            continue
        summary = load_json(summary_path)
        for record in summary.get("records", []):
            problem_id = str(record["problem_id"])
            attempt_counts[problem_id] = attempt_counts.get(problem_id, 0) + 1
            baseline_attempts += 1
            result_path = None
            if record.get("episode"):
                episode_path = config.run_root / str(record["episode"])
                if episode_path.is_file():
                    episode = load_json(episode_path)
                    verifier = (episode.get("paths") or {}).get("verifier")
                    if verifier:
                        result_path = episode_path.parent / str(verifier)
            selected_exact, candidates_exact = _stored_exact_outcomes(record, result_path)
            baseline_selected_exact += int(selected_exact)
            baseline_candidates_exact += int(candidates_exact)
            if selected_exact:
                selected_exact_ids.add(problem_id)
            if candidates_exact:
                candidates_exact_ids.add(problem_id)
            evidence.append(
                {
                    "role": "baseline",
                    **record,
                    "exact_success": selected_exact,
                    "selected_exact": selected_exact,
                    "candidates_exact": candidates_exact,
                }
            )
    for wave in ledger.get("waves", []):
        output = config.config_path.parent / str(wave["output"])
        progress = output / "summary.json"
        if not progress.is_file():
            progress = output / "progress.json"
        if not progress.is_file():
            wave_views.append(wave)
            continue
        payload = load_json(progress)
        records = payload.get("results", payload.get("attempts", []))
        wave_selected_exact = 0
        wave_candidates_exact = 0
        for record in records:
            if record.get("status") not in {"archived", "failed"}:
                continue
            problem_id = str(record["problem_id"])
            result_path = (
                output / "attempts" / str(record.get("attempt_id")) / "run/verifier-result.json"
            )
            selected_exact, candidates_exact = _stored_exact_outcomes(record, result_path)
            wave_selected_exact += int(selected_exact)
            wave_candidates_exact += int(candidates_exact)
            attempt_counts[problem_id] = attempt_counts.get(problem_id, 0) + 1
            role = "baseline" if wave.get("role") == "baseline" else "learned"
            if role == "baseline":
                baseline_attempts += 1
                baseline_selected_exact += int(selected_exact)
                baseline_candidates_exact += int(candidates_exact)
            else:
                learned_attempts += 1
                learned_selected_exact += int(selected_exact)
                learned_candidates_exact += int(candidates_exact)
            if selected_exact:
                selected_exact_ids.add(problem_id)
            if candidates_exact:
                candidates_exact_ids.add(problem_id)
            evidence.append(
                {
                    "role": role,
                    "wave": wave["label"],
                    "problem_id": problem_id,
                    "attempt_id": record.get("attempt_id"),
                    "exact_success": selected_exact,
                    "selected_exact": selected_exact,
                    "candidates_exact": candidates_exact,
                    "attempt": str(output / "attempts" / str(record.get("attempt_id"))),
                }
            )
        wave_views.append(
            {
                **wave,
                "exact": wave_selected_exact,
                "selected_exact": wave_selected_exact,
                "candidates_exact": wave_candidates_exact,
            }
        )
    seen = set(attempt_counts)
    baseline_ids = _baseline_problem_ids(config, ledger)
    return {
        "project_id": config.project_id,
        "curriculum": len(order),
        "baseline": {
            "attempts": baseline_attempts,
            "exact": baseline_selected_exact,
            "selected_exact": baseline_selected_exact,
            "candidates_exact": baseline_candidates_exact,
            "problems": len(baseline_ids),
            "remaining": len(set(order) - baseline_ids),
            "next_missing": [problem_id for problem_id in order if problem_id not in baseline_ids][
                : config.wave_size
            ],
        },
        "learned": {
            "attempts": learned_attempts,
            "exact": learned_selected_exact,
            "selected_exact": learned_selected_exact,
            "candidates_exact": learned_candidates_exact,
        },
        "problems_seen": len(seen),
        "problems_exact_at_least_once": len(selected_exact_ids),
        "problems_selected_exact_at_least_once": len(selected_exact_ids),
        "problems_candidates_exact_at_least_once": len(candidates_exact_ids),
        "retries": sum(max(0, count - 1) for count in attempt_counts.values()),
        "next_unseen": [problem_id for problem_id in order if problem_id not in seen][
            : config.wave_size
        ],
        "remaining_unseen": len(set(order) - seen),
        "waves": wave_views,
        "evidence": evidence,
    }
