#!/usr/bin/env python3
"""Normalize one completed experiment into a compact public bundle."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import shutil
from pathlib import Path
from typing import Any

_HOME = Path.home().expanduser().resolve()
PATH_REDACTIONS = (
    (f"{_HOME}/workspace/", "<WORKSPACE>/"),
    (f"{_HOME}/", "<HOME>/"),
)
PUBLIC_METADATA_DROP_KEYS = {
    "auth",
    "command",
    "episode",
    "file_id",
    "memory_max_label",
    "response_id",
    "rollout_source",
    "source_attempt_name",
    "source_run",
    "systemd_result",
    "systemd_run_pid",
    "systemd_runtime_max_seconds",
    "systemd_unit",
    "worker_id",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sanitize_text(value: str) -> str:
    for source, replacement in PATH_REDACTIONS:
        value = value.replace(source, replacement)
    value = re.sub(
        r"<WORKSPACE>/[^\s\"'<>]+/attempts/[^/\s\"'<>]+/workspace",
        "<ATTEMPT_WORKSPACE>",
        value,
    )
    value = re.sub(
        r"<WORKSPACE>/[^\s\"'<>]+/attempts/[^/\s\"'<>]+/codex-home",
        "<AGENT_HOME>",
        value,
    )
    value = re.sub(
        r"<WORKSPACE>/[^\s\"'<>]+/attempts/[^/\s\"'<>]+/run",
        "<ATTEMPT_RUN>",
        value,
    )
    value = re.sub(
        r"<HOME>/\.codex/packages/standalone/releases/[^/\s\"'<>]+/bin/codex",
        "<CODEX_EXECUTABLE>",
        value,
    )
    value = re.sub(
        r"<WORKSPACE>/pxrd-benchmark-workspaces-[^/\s\"'<>]+/worker-\d+",
        "<ATTEMPT_WORKSPACE>",
        value,
    )
    value = value.replace(
        "<WORKSPACE>/verifiable-pxrd-problems/",
        "<REPOSITORY>/experiments/agent-adaptation/curriculum/train-50/",
    )
    value = value.replace(
        "<WORKSPACE>/verifiable-pxrd-benchmark-live/pxrd-bench/",
        "<REPOSITORY>/pxrd-bench/",
    )
    value = value.replace(
        "<WORKSPACE>/verifiable-pxrd/benchmarks/",
        "<REPOSITORY>/pxrd-bench/",
    )
    value = value.replace(
        "<WORKSPACE>/verifiable-pxrd/pxrd-bench/",
        "<REPOSITORY>/pxrd-bench/",
    )
    value = value.replace(
        "<WORKSPACE>/verifiable-pxrd/learned_harness/",
        "<REPOSITORY>/experiments/agent-adaptation/",
    )
    value = re.sub(r"<WORKSPACE>/[^\s\"'<>),\]]+", "<SOURCE_ARTIFACT>", value)
    value = re.sub(r"<HOME>/[^\s\"'<>),\]]+", "<MACHINE_RESOURCE>", value)
    value = re.sub(r"/(?:home|Users)/[^\s\"'<>),\]]+", "<EXTERNAL_PATH>", value)
    value = re.sub(
        r"(?i)%2f(?:home|users)%2f[^\s<>)]*", "<EXTERNAL_PATH>", value
    )
    return value


def sanitize_value(value: Any) -> Any:
    if isinstance(value, str):
        return sanitize_text(value)
    if isinstance(value, list):
        return [sanitize_value(item) for item in value]
    if isinstance(value, dict):
        return {key: sanitize_value(item) for key, item in value.items()}
    return value


def sanitize_metadata(value: Any) -> Any:
    if isinstance(value, list):
        return [sanitize_metadata(item) for item in value]
    if isinstance(value, dict):
        return {
            key: sanitize_metadata(item)
            for key, item in value.items()
            if key not in PUBLIC_METADATA_DROP_KEYS
        }
    return sanitize_value(value)


def sanitize_trace_record(value: dict[str, Any]) -> dict[str, Any]:
    return {
        key: sanitize_value(item)
        for key, item in value.items()
        if key != "thread_id"
    }


def copy_if(source: Path, destination: Path) -> None:
    if source.is_file():
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.suffix.lower() == ".json":
            write(destination, sanitize_metadata(load(source)))
        elif source.suffix.lower() == ".jsonl":
            records = [
                json.dumps(sanitize_trace_record(json.loads(line)), separators=(",", ":"))
                for line in source.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            destination.write_text("\n".join(records) + "\n", encoding="utf-8")
        elif source.suffix.lower() in {
            ".csv",
            ".log",
            ".md",
            ".toml",
            ".txt",
        }:
            destination.write_text(
                sanitize_text(source.read_text(encoding="utf-8")), encoding="utf-8"
            )
        else:
            shutil.copy2(source, destination)


def compress_if(source: Path, destination: Path) -> None:
    if not source.is_file():
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    records = []
    for line in source.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(
                json.dumps(sanitize_trace_record(json.loads(line)), separators=(",", ":"))
            )
    content = ("\n".join(records) + "\n").encode()
    with (
        destination.open("wb") as raw,
        gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=9, mtime=0) as out,
    ):
        out.write(content)


def locate_attempt(source: Path, row: dict[str, Any]) -> Path | None:
    # Some campaigns store attempts under raw/<dataset>/<case>/attempts/<attempt-id>
    # and record canonical retry order in each progress row. Prefer the last
    # declared attempt so infrastructure retries normalize deterministically.
    declared_attempts = row.get("attempts")
    if isinstance(declared_attempts, list):
        for declared in reversed(declared_attempts):
            if not isinstance(declared, dict):
                continue
            supplied_value = declared.get("archive_path")
            if supplied_value:
                supplied = Path(str(supplied_value))
                if supplied.is_dir():
                    return supplied
            attempt_id = declared.get("attempt_id")
            if attempt_id:
                candidates = sorted(
                    (source / "raw").glob(
                        f"*/{row['case_id']}/attempts/{attempt_id}"
                    )
                )
                if candidates:
                    return candidates[0]
    attempt_id = row.get("attempt_id")
    if attempt_id:
        candidate = source / "attempts" / str(attempt_id)
        if candidate.is_dir():
            return candidate
    supplied_value = row.get("attempt_dir")
    if supplied_value:
        supplied = Path(str(supplied_value))
        if supplied.is_dir():
            return supplied
    candidates = sorted((source / "attempts").glob(f"*-{row['case_id']}-*"))
    return candidates[-1] if candidates else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--id", required=True)
    parser.add_argument("--panel", required=True)
    parser.add_argument("--panel-manifest", type=Path)
    parser.add_argument("--replicate", type=int)
    parser.add_argument("--include-traces", action="store_true")
    args = parser.parse_args()
    source = args.source.resolve()
    destination = args.destination.resolve()
    if destination.exists():
        raise RuntimeError(f"refusing to overwrite {destination}")
    destination.mkdir(parents=True)
    progress_path = source / "progress.json"
    if not progress_path.is_file():
        progress_path = source / "summary.json"
    progress = load(progress_path)
    if isinstance(progress.get("cases"), list):
        rows = list(progress["cases"])
    elif isinstance(progress.get("attempts"), list):
        rows = [
            {**item, "case_id": item["problem_id"]}
            for item in progress["attempts"]
            if args.replicate is None or int(item["replicate"]) == args.replicate
        ]
    elif "records" in progress:
        rows = [
            {**item, "case_id": item.get("case_id", item["problem_id"])}
            for item in progress["records"]
            if args.replicate is None or int(item.get("replicate", 1)) == args.replicate
        ]
    else:
        raise RuntimeError(f"{progress_path.name} contains no cases, attempts, or records")
    case_ids = [str(item["case_id"]) for item in rows]
    if len(case_ids) != len(set(case_ids)):
        raise RuntimeError("multiple attempts per case; select one --replicate")
    problem_lookup: dict[str, Any] = {}
    if args.panel_manifest:
        from verifiable_pxrd.benchmark import load_problem_collection

        problem_lookup = {
            item.problem_id: item for item in load_problem_collection(args.panel_manifest.resolve())
        }
    source_digests: dict[str, str] = {}
    for name in (
        "experiment.json",
        "run.json",
        "progress.json",
        "summary.json",
        "roster.json",
        "panel.json",
        "condition.toml",
        "prompt-template.md",
        "runner.py",
        "input-manifest.json",
        "preflight.json",
        "candidate-provenance.json",
        "contract/prompt.md",
        "source-experiment.json",
        "source-progress.json",
        "source-roster.json",
        "source-run.json",
        "source-summary.json",
    ):
        item = source / name
        if item.is_file():
            source_digests[name] = digest(item)
            copy_if(item, destination / "source-metadata" / name)
    for name in (
        "summary.json",
        "fixedparams-rwp-candidates.csv",
        "fixedparams-rwp-summary.json",
    ):
        item = source / "evaluation" / name
        if item.is_file():
            source_digests[f"evaluation/{name}"] = digest(item)
            copy_if(item, destination / "evaluation" / name)
    normalized: list[dict[str, Any]] = []
    for row in rows:
        case_id = str(row["case_id"])
        attempt = locate_attempt(source, row)
        public = destination / "attempts" / case_id
        # Input runners may use generic success/reward aliases. Public bundles expose
        # only the verifier's two explicit outcomes.
        compatibility_fields = {
            "attempt_dir",
            "attempts",
            "success",
            "reward",
            "exact_success",
            "selected_exact_success",
            "candidates_exact_success",
        }
        record = {key: value for key, value in row.items() if key not in compatibility_fields}
        if attempt:
            declared_attempts = row.get("attempts")
            if isinstance(declared_attempts, list):
                declared = next(
                    (
                        item
                        for item in reversed(declared_attempts)
                        if isinstance(item, dict)
                        and str(item.get("attempt_id")) == attempt.name
                    ),
                    None,
                )
                if declared:
                    record.setdefault("attempt_id", attempt.name)
                    for key in (
                        "cancelled",
                        "infrastructure_failure",
                        "infrastructure_reason",
                        "returncode",
                        "scientific_work",
                        "timed_out",
                    ):
                        if key in declared:
                            record.setdefault(key, declared[key])
                    if "archived_at" in declared:
                        record.setdefault("ended_at", declared["archived_at"])
            launch_path = attempt / "run/launch.json"
            if not launch_path.is_file():
                launch_path = attempt / "launch.json"
            if launch_path.is_file():
                launch = load(launch_path)
                record.setdefault("attempt_id", launch.get("attempt_id", attempt.name))
                record.setdefault("problem_id", case_id)
                for key in ("started_at", "ended_at", "returncode", "timed_out"):
                    if key in launch:
                        record.setdefault(key, launch[key])
            verifier = attempt / "run/verifier-result.json"
            if verifier.is_file():
                evaluation = load(verifier)
                matches = list(evaluation.get("metrics", {}).get("matched_candidates", []))
                selected_exact = bool(evaluation.get("selected_exact", "selected.cif" in matches))
                candidates_exact = bool(evaluation.get("candidates_exact", bool(matches)))
                historical_exact = row.get("selected_exact", row.get("exact_success"))
                if historical_exact is not None and bool(historical_exact) != selected_exact:
                    raise RuntimeError(f"progress/verifier disagreement for {case_id}")
                record["selected_exact"] = selected_exact
                record["candidates_exact"] = candidates_exact
                record["matched_candidates"] = matches
            elif case_id in problem_lookup:
                from verifiable_pxrd.matching import evaluate_workspace

                evaluation = evaluate_workspace(
                    problem_lookup[case_id].reference, attempt / "workspace", case_id
                )
                record["selected_exact"] = bool(evaluation["selected_exact"])
                record["candidates_exact"] = bool(evaluation["candidates_exact"])
                record["matched_candidates"] = evaluation["metrics"]["matched_candidates"]
                write(public / "verifier-result.json", evaluation)
            for relative, public_name in (
                ("assignment.json", "assignment.json"),
                ("control/assignment.json", "assignment.json"),
                ("input/prompt.md", "prompt.md"),
                ("prompt.txt", "prompt.txt"),
                ("final-answer.md", "final-answer.md"),
                ("run/final-answer.md", "final-answer.md"),
                ("run/output.md", "final-answer.md"),
                ("launch.json", "launch.json"),
                ("run/launch.json", "launch.json"),
                ("run/request.json", "request.json"),
                ("run/response.json", "response.json"),
                ("run/verifier-result.json", "verifier-result.json"),
                ("run/adjudication.json", "adjudication.json"),
            ):
                copy_if(attempt / relative, public / public_name)
            for workspace in (attempt / "workspace", attempt / "run/top1-workspace"):
                if workspace.is_dir():
                    label = "submission" if workspace.name == "workspace" else "top1-submission"
                    for candidate in [
                        workspace / "selected.cif",
                        *sorted(workspace.glob("alternative-*.cif")),
                    ]:
                        copy_if(candidate, public / label / candidate.name)
            if args.include_traces:
                events = attempt / "run/codex-events.jsonl"
                if not events.is_file():
                    events = attempt / "codex-events.jsonl"
                compress_if(events, public / "codex-events.jsonl.gz")
            record["source_artifacts"] = {
                str(path.relative_to(attempt)): digest(path)
                for path in sorted(attempt.rglob("*"))
                if path.is_file()
                and (
                    path.name
                    in {
                        "assignment.json",
                        "prompt.md",
                        "prompt.txt",
                        "final-answer.md",
                        "output.md",
                        "launch.json",
                        "request.json",
                        "response.json",
                        "verifier-result.json",
                        "adjudication.json",
                        "selected.cif",
                        "codex-events.jsonl",
                    }
                    or path.name.startswith("alternative-")
                )
            }
        if "status" not in record:
            record["status"] = "archived" if attempt is not None else "missing"
        record = sanitize_metadata(record)
        replicate = int(record.get("replicate", args.replicate or 1))
        record["attempt_id"] = f"{case_id}-r{replicate}"
        # Schema v1 consumers use ``selected_exact_success`` for the primary CIF
        # and ``exact_success`` for any declared candidate.  Retain the explicit
        # verifier names as well so their semantics remain self-documenting.
        if "selected_exact" in record:
            record["selected_exact_success"] = bool(record["selected_exact"])
        if "candidates_exact" in record:
            record["exact_success"] = bool(record["candidates_exact"])
        write(public / "attempt.json", record)
        normalized.append(record)
    completed = [item for item in normalized if item.get("status") == "archived"]
    selected_exact = [item for item in completed if bool(item.get("selected_exact"))]
    candidates_exact = [item for item in completed if bool(item.get("candidates_exact"))]
    bundle = {
        "schema_version": "1",
        "result_id": args.id,
        "panel": args.panel,
        "source_metadata_sha256": source_digests,
        "traces_included": args.include_traces,
        "case_count": len(normalized),
        "completed_count": len(completed),
        "selected_exact_count": len(selected_exact),
        "selected_exact_case_ids": [str(item["case_id"]) for item in selected_exact],
        "exact_count": len(candidates_exact),
        "exact_case_ids": [str(item["case_id"]) for item in candidates_exact],
        "exact_rate_completed": len(candidates_exact) / len(completed) if completed else 0.0,
        "candidates_exact_count": len(candidates_exact),
        "candidates_exact_case_ids": [str(item["case_id"]) for item in candidates_exact],
        "cases": normalized,
    }
    if args.replicate is not None:
        bundle["replicate"] = args.replicate
    write(destination / "bundle.json", bundle)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
