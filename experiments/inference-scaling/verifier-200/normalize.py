#!/usr/bin/env python3
"""Normalize and validate the full-200 inference-time verifier evidence."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import re
import tomllib
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG = Path(__file__).with_name("experiment.toml")
DEFAULT_OUTPUT = (
    REPO_ROOT / "results/inference-scaling/verifier-200/adapted-codex-r1"
)
FORBIDDEN_TEXT = ("/home/", "/Users/")
SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)aws_secret_access_key\s*[=:]\s*[^\s]+"),
)
LAUNCH_FIELDS = (
    "elapsed_seconds",
    "ended_at",
    "model",
    "reasoning_effort",
    "returncode",
    "started_at",
    "timed_out",
    "timeout_seconds",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--raw-root", type=Path)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", type=Path)
    return parser.parse_args()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_config(path: Path) -> dict[str, Any]:
    with path.open("rb") as stream:
        return tomllib.load(stream)


def source_paths(config: dict[str, Any], raw_root: Path) -> dict[str, Path]:
    return {key: raw_root / value for key, value in config["sources"].items()}


def portable_path(value: str) -> str:
    if not value.startswith("/"):
        return value
    path = Path(value)
    parts = path.parts
    if "pxrd-bench" in parts:
        return Path(*parts[parts.index("pxrd-bench") :]).as_posix()
    if "submission" in parts:
        index = parts.index("submission")
        if index >= 2:
            case_id = parts[index - 1]
            return (
                Path("results/agent-adaptation/adapted-codex")
                / "full-200-chatgpt-sol-high-r1/attempts"
                / case_id
                / "submission"
                / path.name
            ).as_posix()
    if "pattern" in path.name.lower() or path.suffix == ".csv":
        return f"<BENCHMARK_PATTERN>/{path.name}"
    return "<EXTERNAL_PATH>"


def sanitize_text(text: str) -> str:
    text = re.sub(
        r"/(?:home|Users)/[^\s\"'<>),\]]+",
        lambda match: portable_path(match.group(0)),
        text,
    )
    return re.sub(
        r"(?i)%2f(?:home|users)%2f[^\s<>)]*", "<EXTERNAL_PATH>", text
    )


def sanitize_value(value: Any) -> Any:
    if isinstance(value, str):
        return sanitize_text(value)
    if isinstance(value, list):
        return [sanitize_value(item) for item in value]
    if isinstance(value, dict):
        return {key: sanitize_value(item) for key, item in value.items()}
    return value


def copy_text(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        sanitize_text(source.read_text(encoding="utf-8", errors="replace")),
        encoding="utf-8",
    )


def copy_json(source: Path, destination: Path) -> None:
    write_json(destination, sanitize_value(read_json(source)))


def copy_trace(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    records = []
    with source.open("r", encoding="utf-8", errors="replace") as stream:
        for line in stream:
            if not line.strip():
                continue
            record = json.loads(line)
            record.pop("thread_id", None)
            records.append(
                json.dumps(sanitize_value(record), separators=(",", ":"))
            )
    payload = ("\n".join(records) + "\n").encode()
    with (
        destination.open("wb") as raw,
        gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed,
    ):
        compressed.write(payload)


def copy_launch(source: Path, destination: Path) -> None:
    launch = read_json(source)
    write_json(destination, {key: launch[key] for key in LAUNCH_FIELDS if key in launch})


def copy_attempt(source: Path, destination: Path, *, canonical: bool = True) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for name in ("decision.json", "prompt.md"):
        path = source / name
        if path.is_file():
            (copy_json if path.suffix == ".json" else copy_text)(
                path, destination / name
            )
    run = source / "run"
    if (run / "codex-events.jsonl").is_file():
        copy_trace(run / "codex-events.jsonl", destination / "codex-events.jsonl.gz")
    if (run / "final-answer.md").is_file():
        copy_text(run / "final-answer.md", destination / "final-answer.md")
    if (run / "launch.json").is_file():
        copy_launch(run / "launch.json", destination / "launch.json")
    report = source / "evidence/comparable-rwp-report.json"
    if report.is_file():
        copy_json(report, destination / "comparable-rwp-report.json")
    write_json(
        destination / "manifest.json",
        {
            "schema_version": "verifier-200-attempt-v1",
            "canonical_decision": canonical,
            "source_artifacts": {
                path.relative_to(source).as_posix(): sha256(path)
                for path in sorted(source.rglob("*"))
                if path.is_file()
                and (
                    path.name
                    in {
                        "codex-events.jsonl",
                        "decision.json",
                        "final-answer.md",
                        "launch.json",
                        "prompt.md",
                        "comparable-rwp-report.json",
                    }
                )
            },
        },
    )


def evaluation_rows(path: Path) -> dict[str, dict[str, Any]]:
    evaluation = read_json(path / "evaluation.json")
    return {str(row["problem_id"]): row for row in evaluation["results"]}


def decision_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    false_stops = sum(
        row["decision"] == "stop" and not row["candidate_set_exact"] for row in rows
    )
    false_continues = sum(
        row["decision"] == "continue" and row["candidate_set_exact"] for row in rows
    )
    true_stops = sum(
        row["decision"] == "stop" and row["candidate_set_exact"] for row in rows
    )
    true_continues = sum(
        row["decision"] == "continue" and not row["candidate_set_exact"] for row in rows
    )
    correct = true_stops + true_continues
    return {
        "accuracy": correct / len(rows),
        "correct": correct,
        "false_continue_rate": false_continues / 141,
        "false_continues": false_continues,
        "false_stop_rate": false_stops / 59,
        "false_stops": false_stops,
        "true_continues": true_continues,
        "true_stops": true_stops,
    }


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def normalize_rwp(
    source: Path,
    exact_by_case: dict[str, bool],
) -> tuple[dict[str, float], list[dict[str, Any]], dict[str, Any]]:
    summary = read_json(source / "summary.json")
    best: dict[str, float] = {}
    candidate_rows = []
    protocol = None
    for case in summary["cases"]:
        case_id = str(case["case_id"])
        if case.get("selected"):
            best[case_id] = float(case["selected"]["rwp_percent"])
        report_path = source / "cases" / case_id / "report.json"
        if not report_path.is_file():
            continue
        report = read_json(report_path)
        if protocol is None and report.get("protocol"):
            protocol = sanitize_value(report["protocol"])
        for rank, result in enumerate(report.get("results", []), start=1):
            candidate_rows.append(
                {
                    "case_id": case_id,
                    "candidate": Path(str(result.get("candidate", ""))).name,
                    "rank": rank,
                    "rwp_percent": result.get("rwp_percent", ""),
                    "sha256": result.get("sha256", ""),
                    "status": result.get("status", ""),
                    "structure_group": result.get("structure_group", ""),
                }
            )
    if set(best) - set(exact_by_case):
        raise AssertionError("Rwp run contains cases absent from the solver bundle")
    if protocol is None:
        raise AssertionError("Rwp protocol is missing")
    return best, candidate_rows, protocol


def copy_source_metadata(source: Path, destination: Path) -> None:
    for name in ("condition.toml", "panel.json", "policy.md", "source.json", "wrapper.md"):
        path = source / "contract" / name
        if path.is_file():
            (copy_json if path.suffix == ".json" else copy_text)(
                path, destination / name
            )
    run = read_json(source / "run.json")
    keep = {
        key: run[key]
        for key in (
            "auth_method",
            "condition",
            "created_at",
            "model",
            "oracle_available_to_reviewer",
            "parallel",
            "policy_sha256",
            "problem_count",
            "reasoning_effort",
            "schema_version",
            "source_bundle_sha256",
            "timeout_seconds",
            "wrapper_sha256",
        )
        if key in run
    }
    write_json(destination / "run.json", sanitize_value(keep))


def figure_row(name: str, metrics: dict[str, Any], threshold: float | None = None) -> dict[str, Any]:
    return {
        "method": name,
        "threshold_percent": "" if threshold is None else threshold,
        "correct": metrics["correct"],
        "accuracy_percent": metrics["accuracy"] * 100,
        "false_stops": metrics["false_stops"],
        "false_stop_percent": metrics["false_stop_rate"] * 100,
        "false_continues": metrics["false_continues"],
        "false_continue_percent": metrics["false_continue_rate"] * 100,
    }


def build(config_path: Path, raw_root: Path, output: Path) -> None:
    config = load_config(config_path)
    sources = source_paths(config, raw_root.resolve())
    missing = [str(path) for path in sources.values() if not path.is_dir()]
    if missing:
        raise FileNotFoundError(f"missing raw sources: {missing}")
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"output directory is not empty: {output}")
    output.mkdir(parents=True, exist_ok=True)

    solver_path = REPO_ROOT / config["solver_bundle"]
    solver = read_json(solver_path)
    cases = solver["cases"]
    exact_by_case = {str(row["case_id"]): bool(row["candidates_exact"]) for row in cases}
    formula_by_case = {
        case_id: str(
            read_json(
                solver_path.parent / "attempts" / case_id / "assignment.json"
            )["formula"]
        )
        for case_id in exact_by_case
    }
    seed = evaluation_rows(sources["seed"])
    judge = evaluation_rows(sources["judge_v1"])
    retry = evaluation_rows(sources["judge_v1_retry"])
    retry_id = str(config["judge_v1_retry"]["problem_id"])
    initial_invalid = judge[retry_id]
    if initial_invalid.get("decision") is not None:
        raise AssertionError("configured judge-v1 retry did not replace an invalid call")
    judge[retry_id] = retry[retry_id]
    expected_ids = set(exact_by_case)
    for name, rows in (("seed", seed), ("judge-v1", judge)):
        if set(rows) != expected_ids:
            raise AssertionError(f"{name} case IDs do not match the solver bundle")

    rwp, rwp_candidates, protocol = normalize_rwp(sources["rwp"], exact_by_case)
    case_rows = []
    seed_metric_rows = []
    judge_metric_rows = []
    cutoff_metric_rows: dict[str, list[dict[str, Any]]] = {
        item["id"]: [] for item in config["rwp_cutoffs"]
    }
    for case in cases:
        case_id = str(case["case_id"])
        is_exact = exact_by_case[case_id]
        seed_decision = str(seed[case_id]["decision"])
        judge_decision = str(judge[case_id]["decision"])
        if seed_decision not in {"stop", "continue"} or judge_decision not in {
            "stop",
            "continue",
        }:
            raise AssertionError(f"invalid canonical decision for {case_id}")
        value = rwp.get(case_id)
        row: dict[str, Any] = {
            "case_id": case_id,
            "formula": formula_by_case[case_id],
            "candidate_set_exact": is_exact,
            "oracle_decision": "stop" if is_exact else "continue",
            "rwp_available": value is not None,
            "best_rwp_percent": "" if value is None else value,
            "seed_decision": seed_decision,
            "seed_correct": (seed_decision == "stop") == is_exact,
            "judge_v1_decision": judge_decision,
            "judge_v1_correct": (judge_decision == "stop") == is_exact,
            "judge_v1_retry": case_id == retry_id,
        }
        seed_metric_rows.append({"decision": seed_decision, "candidate_set_exact": is_exact})
        judge_metric_rows.append({"decision": judge_decision, "candidate_set_exact": is_exact})
        for cutoff in config["rwp_cutoffs"]:
            decision = (
                "continue"
                if value is None or value > float(cutoff["threshold_percent"])
                else "stop"
            )
            row[f"{cutoff['id']}_decision"] = decision
            row[f"{cutoff['id']}_correct"] = (decision == "stop") == is_exact
            cutoff_metric_rows[cutoff["id"]].append(
                {"decision": decision, "candidate_set_exact": is_exact}
            )
        case_rows.append(row)

        copy_attempt(
            sources["seed"] / "attempts" / case_id,
            output / "attempts" / case_id / "seed",
        )
        judge_source = sources["judge_v1_retry"] if case_id == retry_id else sources["judge_v1"]
        copy_attempt(
            judge_source / "attempts" / case_id,
            output / "attempts" / case_id / "judge-v1",
        )
        if case_id == retry_id:
            copy_attempt(
                sources["judge_v1"] / "attempts" / case_id,
                output / "attempts" / case_id / "judge-v1-initial-invalid",
                canonical=False,
            )

    seed_metrics = decision_metrics(seed_metric_rows)
    judge_metrics = decision_metrics(judge_metric_rows)
    cutoff_metrics = {
        key: decision_metrics(rows) for key, rows in cutoff_metric_rows.items()
    }
    figure = []
    first_cutoff = config["rwp_cutoffs"][0]
    second_cutoff = config["rwp_cutoffs"][1]
    figure.append(
        figure_row(
            f"Rwp <= {first_cutoff['threshold_percent']}%",
            cutoff_metrics[first_cutoff["id"]],
            float(first_cutoff["threshold_percent"]),
        )
    )
    figure.append(figure_row("102-word seed", seed_metrics))
    figure.append(
        figure_row(
            f"Rwp <= {second_cutoff['threshold_percent']}%",
            cutoff_metrics[second_cutoff["id"]],
            float(second_cutoff["threshold_percent"]),
        )
    )
    figure.append(figure_row("Final judge-v1", judge_metrics))

    fields = list(case_rows[0])
    write_csv(output / "case-results.csv", case_rows, fields)
    write_csv(output / "figure-3a.csv", figure, list(figure[0]))
    write_csv(
        output / "rwp-candidate-scores.csv",
        rwp_candidates,
        ["case_id", "candidate", "rank", "rwp_percent", "sha256", "status", "structure_group"],
    )
    write_json(output / "source-metadata/rwp-protocol.json", protocol)
    copy_source_metadata(sources["seed"], output / "source-metadata/seed")
    copy_source_metadata(sources["judge_v1"], output / "source-metadata/judge-v1")
    copy_source_metadata(
        sources["judge_v1_retry"], output / "source-metadata/judge-v1-retry"
    )
    copy_text(config_path, output / "source-metadata/experiment.toml")
    write_json(
        output / "source-metadata/rwp-source.json",
        {
            "schema_version": "verifier-200-rwp-source-v1",
            "case_count": len(exact_by_case),
            "cases_with_candidates": len(rwp),
            "cases_without_candidates": len(exact_by_case) - len(rwp),
            "candidate_fit_count": len(rwp_candidates),
            "summary_sha256": sha256(sources["rwp"] / "summary.json"),
        },
    )
    write_json(
        output / "source-metadata/solver-bundle.json",
        {
            "path": config["solver_bundle"],
            "result_id": solver["result_id"],
            "sha256": sha256(solver_path),
            "candidate_set_exact_count": sum(exact_by_case.values()),
            "candidate_set_miss_count": len(exact_by_case) - sum(exact_by_case.values()),
        },
    )
    summary = {
        "schema_version": "verifier-200-result-v1",
        "result_id": config["result_id"],
        "case_count": len(case_rows),
        "candidate_set_exact_count": sum(exact_by_case.values()),
        "candidate_set_miss_count": len(exact_by_case) - sum(exact_by_case.values()),
        "judge_v1_retry": {
            "problem_id": retry_id,
            "reason": config["judge_v1_retry"]["reason"],
            "initial_returncode": read_json(
                sources["judge_v1"] / "attempts" / retry_id / "run/launch.json"
            )["returncode"],
        },
        "input_conditions": {
            "seed": {"comparable_rwp_report_supplied": False},
            "judge_v1": {"comparable_rwp_report_supplied": False},
            "comparison_is_prompt_only_ablation": True,
        },
        "metrics": {
            "seed": seed_metrics,
            "judge_v1": judge_metrics,
            **{key: value for key, value in cutoff_metrics.items()},
        },
        "figure_3a": figure,
        "judge_trace_count": 401,
    }
    write_json(output / "summary.json", summary)
    write_readme(output, summary)
    write_checksums(output)
    check(output, config)


def write_readme(output: Path, summary: dict[str, Any]) -> None:
    figure = summary["figure_3a"]
    rows = "\n".join(
        f"| {row['method']} | {row['correct']}/200 ({row['accuracy_percent']:.1f}%) "
        f"| {row['false_stops']}/59 ({row['false_stop_percent']:.1f}%) "
        f"| {row['false_continues']}/141 ({row['false_continue_percent']:.1f}%) |"
        for row in figure
    )
    text = f"""# Full-200 inference-time verifier results

This bundle contains the case-level evidence behind Figure 3a for the 200 frozen
`adapted-codex` pXRD-Bench candidate sets. A reference match anywhere in the declared
candidate set is the positive class: `stop` is correct for the 141 exact candidate sets,
and `continue` is correct for the 59 misses.

| Method | Accuracy | False stops | False continues |
| --- | ---: | ---: | ---: |
{rows}

The two Rwp cutoffs were selected retrospectively to match the LLM policies' false-stop
counts. Missing candidate CIFs are assigned `continue`. These rows are descriptive
comparators, not held-out threshold estimates.

## Inputs and provenance

Both reviewers received the composition, wavelength, observed pattern, chronological
solver trace, final response, and submitted CIF set; neither received the hidden
reference or StructureMatcher result. Both received an explicit `not supplied`
sentinel for the precomputed blind comparable-Rwp report and could perform their own
calculations. The comparison is therefore a prompt-only ablation between the seed and
final policies.

The initial judge-v1 call for `pxrdood-tn-css-014` ended with a model-capacity error and
no decision. Its fresh retry supplied the canonical `stop` decision; both sanitized
traces are retained.

## Files

- `case-results.csv`: all labels, Rwp values, decisions, and correctness flags.
- `figure-3a.csv` and `summary.json`: the aggregate values reported above.
- `attempts/<case>/seed/` and `judge-v1/`: sanitized prompts, decisions, final answers,
  launch metadata, comparable-Rwp input, and compressed chronological judge traces.
- `attempts/pxrdood-tn-css-014/judge-v1-initial-invalid/`: the superseded failed call.
- `rwp-candidate-scores.csv` and `source-metadata/rwp-protocol.json`: deterministic
  blind comparable-fit evidence and its shared fitting protocol.
- `source-metadata/`: frozen policies, wrapper, conditions, run contracts, solver-bundle
  identity, and the normalization contract.
- `SHA256SUMS`: hashes for every normalized artifact.

The source solver trajectories, verifier outputs, and CIFs are not duplicated here.
They are keyed by the same case IDs in
`results/agent-adaptation/adapted-codex/full-200-chatgpt-sol-high-r1/`.
"""
    (output / "README.md").write_text(text, encoding="utf-8")


def write_checksums(root: Path) -> None:
    paths = [
        path
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.name != "SHA256SUMS"
    ]
    text = "".join(f"{sha256(path)}  {path.relative_to(root).as_posix()}\n" for path in paths)
    (root / "SHA256SUMS").write_text(text, encoding="utf-8")


def check(root: Path, config: dict[str, Any]) -> None:
    summary = read_json(root / "summary.json")
    if summary["case_count"] != 200:
        raise AssertionError("expected 200 cases")
    if (summary["candidate_set_exact_count"], summary["candidate_set_miss_count"]) != (141, 59):
        raise AssertionError("unexpected adapted-codex labels")
    for name in ("seed", "judge_v1"):
        actual = summary["metrics"][name]
        expected = config["expected"][name]
        for field in ("correct", "false_stops", "false_continues"):
            if actual[field] != expected[field]:
                raise AssertionError(f"{name} {field}: {actual[field]} != {expected[field]}")
    for cutoff in config["rwp_cutoffs"]:
        actual = summary["metrics"][cutoff["id"]]
        for field in ("correct", "false_stops", "false_continues"):
            expected = cutoff[f"expected_{field}"]
            if actual[field] != expected:
                raise AssertionError(
                    f"{cutoff['id']} {field}: {actual[field]} != {expected}"
                )
    attempts = root / "attempts"
    if len(list(attempts.glob("*/seed/decision.json"))) != 200:
        raise AssertionError("expected 200 seed decisions")
    if len(list(attempts.glob("*/judge-v1/decision.json"))) != 200:
        raise AssertionError("expected 200 judge-v1 decisions")
    if len(list(attempts.rglob("codex-events.jsonl.gz"))) != 401:
        raise AssertionError("expected 401 judge traces, including the retry")
    checksums = {}
    for line in (root / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", maxsplit=1)
        checksums[relative] = digest
    actual_paths = {
        path.relative_to(root).as_posix(): sha256(path)
        for path in root.rglob("*")
        if path.is_file() and path.name != "SHA256SUMS"
    }
    if checksums != actual_paths:
        raise AssertionError("SHA256SUMS does not match the normalized tree")
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        opener = gzip.open if path.suffix == ".gz" else open
        try:
            with opener(path, "rt", encoding="utf-8", errors="replace") as stream:
                text = stream.read()
        except (OSError, UnicodeError):
            continue
        if any(token in text for token in FORBIDDEN_TEXT):
            raise AssertionError(f"private absolute path in {path}")
        if any(pattern.search(text) for pattern in SECRET_PATTERNS):
            raise AssertionError(f"possible secret in {path}")


def main() -> int:
    args = parse_args()
    config = load_config(args.config)
    if args.check:
        check(args.check.resolve(), config)
        print(json.dumps({"valid": True, "bundle": str(args.check.resolve())}, indent=2))
        return 0
    if args.raw_root is None:
        raise SystemExit("--raw-root is required unless --check is used")
    build(args.config.resolve(), args.raw_root.resolve(), args.output.resolve())
    print(json.dumps({"valid": True, "bundle": str(args.output.resolve())}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
