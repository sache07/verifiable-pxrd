#!/usr/bin/env python3
"""Normalize and validate the paper-reported verifier-gated result."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import re
import shutil
import tomllib
from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG = Path(__file__).with_name("experiment.toml")
CASE_IDS = tuple(f"vh-{index:03d}" for index in range(1, 21))
SOLVER_STAGE = {
    "s0": "initial",
    "c1": "continuation-01",
    "s2": "fresh-02",
    "s3": "fresh-03",
}
ROUND_STAGE = {
    "review-00": "j0",
    "continuation-01": "c1",
    "review-01": "j1",
    "fresh-02": "s2",
    "review-02": "j2",
    "fresh-03": "s3",
}
CHECKPOINT_BLOCKS = {
    "S0": (),
    "C1": ("j0", "c1"),
    "S2": ("j0", "c1", "j1", "s2"),
    "S3": ("j0", "c1", "j1", "s2", "j2", "s3"),
}
EXPECTED_RECOVERY = {"S0": 13, "C1": 17, "S2": 18, "S3": 18}
EXPECTED_COST = {
    "S0": 62.9920,
    "C1": 140.5061,
    "S2": 184.1190,
    "S3": 216.5979,
}
FORBIDDEN_TEXT = (
    "/home/",
    "/Users/",
)
SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)aws_secret_access_key\s*[=:]\s*[^\s]+"),
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--raw-root", type=Path)
    parser.add_argument("--initial-source", type=Path)
    parser.add_argument("--output", type=Path)
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


def sanitize(text: str) -> str:
    home = str(Path.home().expanduser().resolve())
    sanitized = (
        text.replace(f"{home}/workspace/", "<WORKSPACE>/")
        .replace(f"{home}/", "<HOME>/")
    )
    sanitized = re.sub(
        r"/(?:home|Users)/[^\s\"'<>),\]]+", "<EXTERNAL_PATH>", sanitized
    )
    return re.sub(
        r"(?i)%2f(?:home|users)%2f[^\s<>)]*", "<EXTERNAL_PATH>", sanitized
    )


def sanitize_value(value: Any) -> Any:
    if isinstance(value, str):
        return sanitize(value)
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


def copy_initial_condition(source: Path, destination: Path) -> None:
    text = sanitize(source.read_text(encoding="utf-8", errors="replace"))
    text, count = re.subn(
        r'(?m)^id = "[^"]+"$',
        'id = "adapted-codex-sol-high-initial"',
        text,
        count=1,
    )
    if count != 1:
        raise ValueError(f"could not normalize initial condition id in {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text, encoding="utf-8")


def copy_text(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(sanitize(source.read_text(encoding="utf-8", errors="replace")), encoding="utf-8")


def copy_json(source: Path, destination: Path) -> None:
    write_json(destination, sanitize_metadata(read_json(source)))


def copy_trace(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    opener = gzip.open if source.suffix == ".gz" else open
    with opener(source, "rt", encoding="utf-8", errors="replace") as stream:
        records = [
            json.dumps(sanitize_trace_record(json.loads(line)), separators=(",", ":"))
            for line in stream
            if line.strip()
        ]
    text = "\n".join(records) + "\n"
    with (
        destination.open("wb") as raw,
        gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed,
    ):
        compressed.write(text.encode())


def copy_cifs(source: Path, destination: Path) -> list[dict[str, str]]:
    records = []
    if not source.is_dir():
        return records
    for path in sorted(source.glob("*.cif")):
        output = destination / path.name
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, output)
        records.append({"file": path.name, "sha256": sha256(output)})
    return records


def stage_snapshot(chain: dict[str, Any], label: str) -> dict[str, Any]:
    for snapshot in chain["snapshots"]:
        if snapshot["label"] == label:
            return snapshot
    raise KeyError(f"missing {label} in {chain['problem_id']}")


def solver_code(snapshot: dict[str, Any] | None) -> str:
    if snapshot is None:
        return "--"
    if snapshot["selected_exact"]:
        return "E"
    if snapshot["candidates_exact"]:
        return "A"
    return "M"


def judge_code(decision: str | None, input_exact: bool | None) -> str:
    if decision is None or input_exact is None:
        return "--"
    correct = (decision == "stop") == input_exact
    return ("S" if decision == "stop" else "C") + ("+" if correct else "!")


def normalize_initial(
    source: Path,
    destination: Path,
    chain: dict[str, Any],
) -> None:
    destination.mkdir(parents=True)
    for name, output in (
        ("prompt.txt", "prompt.md"),
        ("final-answer.md", "final-answer.md"),
    ):
        copy_text(source / name, destination / output)
    copy_trace(source / "codex-events.jsonl.gz", destination / "codex-events.jsonl.gz")
    for name in ("launch.json", "verifier-result.json"):
        copy_json(source / name, destination / name)
    records = copy_cifs(source / "submission", destination / "submission")
    snapshot = stage_snapshot(chain, "initial")
    write_json(
        destination / "manifest.json",
        {
            "schema_version": "verifier-gated-stage-v1",
            "stage": "s0",
            "candidate_count": len(records),
            "selected_exact": bool(snapshot["selected_exact"]),
            "candidates_exact": bool(snapshot["candidates_exact"]),
            "matched_candidates": snapshot["matched_candidates"],
            "candidates": records,
        },
    )


def normalize_round(
    source: Path,
    destination: Path,
    stage: str,
    chain: dict[str, Any],
) -> None:
    destination.mkdir(parents=True)
    for name in ("prompt.md", "input.json"):
        path = source / name
        if path.is_file():
            (copy_json if path.suffix == ".json" else copy_text)(path, destination / name)
    run = source / "run"
    if (run / "codex-events.jsonl").is_file():
        copy_trace(run / "codex-events.jsonl", destination / "codex-events.jsonl.gz")
    for name in ("final-answer.md", "codex-stderr.log"):
        path = run / name
        if path.is_file() and (name != "codex-stderr.log" or path.stat().st_size):
            copy_text(path, destination / name.replace("codex-", ""))
    if (run / "launch.json").is_file():
        copy_json(run / "launch.json", destination / "launch.json")

    if stage.startswith("j"):
        copy_json(source / "decision.json", destination / "decision.json")
        report = source / "evidence/comparable-rwp-report.json"
        if report.is_file():
            copy_json(report, destination / "comparable-rwp-report.json")
        return

    label = {"c1": "continuation-01", "s2": "fresh-02", "s3": "fresh-03"}[stage]
    records = copy_cifs(source / "submitted", destination / "submission")
    snapshot = stage_snapshot(chain, label)
    write_json(
        destination / "verifier-result.json",
        {
            "schema_version": "1",
            "grader_version": "pxrd-benchmark-structurematcher",
            "task_id": chain["problem_id"],
            "stage": stage,
            "selected_exact": bool(snapshot["selected_exact"]),
            "candidates_exact": bool(snapshot["candidates_exact"]),
            "matched_candidates": snapshot["matched_candidates"],
            "artifacts": [record["file"] for record in records],
        },
    )
    write_json(
        destination / "manifest.json",
        {
            "schema_version": "verifier-gated-stage-v1",
            "stage": stage,
            "candidate_count": len(records),
            "selected_exact": bool(snapshot["selected_exact"]),
            "candidates_exact": bool(snapshot["candidates_exact"]),
            "matched_candidates": snapshot["matched_candidates"],
            "candidates": records,
        },
    )


def last_usage(path: Path) -> dict[str, int] | None:
    if not path.is_file():
        return None
    opener = gzip.open if path.suffix == ".gz" else open
    usage = None
    with opener(path, "rt", encoding="utf-8", errors="replace") as stream:
        for line in stream:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") == "turn.completed" and isinstance(event.get("usage"), dict):
                usage = event["usage"]
    if usage is None:
        return None
    return {
        "input_tokens": int(usage.get("input_tokens", 0)),
        "cached_input_tokens": int(usage.get("cached_input_tokens", 0)),
        "cache_write_input_tokens": int(usage.get("cache_write_input_tokens", 0)),
        "output_tokens": int(usage.get("output_tokens", 0)),
        "reasoning_output_tokens": int(usage.get("reasoning_output_tokens", 0)),
    }


def token_cost(usage: dict[str, int], cost: dict[str, Any]) -> float:
    cached = usage["cached_input_tokens"]
    cache_write = usage["cache_write_input_tokens"]
    uncached = max(0, usage["input_tokens"] - cached - cache_write)
    return (
        uncached * float(cost["uncached_input_per_million_usd"]) / 1_000_000
        + cached * float(cost["cached_input_per_million_usd"]) / 1_000_000
        + cache_write * float(cost["cache_write_input_per_million_usd"]) / 1_000_000
        + usage["output_tokens"] * float(cost["output_per_million_usd"]) / 1_000_000
    )


def cost_report(
    output: Path,
    config: dict[str, Any],
    initial_source: Path,
    raw_root: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    pricing = config["cost"]
    calibration = float(pricing["base_cost_calibration_factor"])
    stage_costs: dict[str, float] = defaultdict(float)
    stage_calls: dict[str, int] = defaultdict(int)
    stage_tokens: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    missing: dict[str, list[str]] = defaultdict(list)

    for case_id in CASE_IDS:
        usage = last_usage(initial_source / "attempts" / case_id / "codex-events.jsonl.gz")
        if usage is None:
            raise ValueError(f"missing initial usage for {case_id}")
        stage_calls["s0"] += 1
        for key, value in usage.items():
            stage_tokens["s0"][key] += value

        rounds = raw_root / "attempts" / case_id / "rounds"
        for round_name, stage in ROUND_STAGE.items():
            events = rounds / round_name / "run/codex-events.jsonl"
            launch = rounds / round_name / "run/launch.json"
            if not events.is_file() and not launch.is_file():
                continue
            stage_calls[stage] += 1
            usage = last_usage(events)
            if usage is None:
                missing[stage].append(case_id)
                if stage != "s2":
                    raise ValueError(f"no frozen imputation for missing {stage} usage: {case_id}")
                base = float(pricing["s2_missing_usage_imputation_base_usd"])
                stage_costs[stage] += base * calibration
                continue
            stage_costs[stage] += token_cost(usage, pricing) * calibration
            for key, value in usage.items():
                stage_tokens[stage][key] += value

    # S0 is the actual first replicate, whose token mix differs from the
    # campaign average. Price its recorded usage and apply the same calibration
    # used for every other stage.
    stage_costs["s0"] = token_cost(dict(stage_tokens["s0"]), pricing) * calibration

    chain_by_case = {
        case_id: read_json(raw_root / "attempts" / case_id / "hybrid-chain.json")
        for case_id in CASE_IDS
    }
    rows = []
    for checkpoint, included in CHECKPOINT_BLOCKS.items():
        recovery_stage = checkpoint.lower()
        cumulative_exact = 0
        for chain in chain_by_case.values():
            labels = [SOLVER_STAGE[stage] for stage in ("s0", "c1", "s2", "s3")]
            stop = labels.index(SOLVER_STAGE[recovery_stage])
            exact = any(
                stage_snapshot(chain, label)["candidates_exact"]
                for label in labels[: stop + 1]
                if any(item["label"] == label for item in chain["snapshots"])
            )
            cumulative_exact += int(exact)
        rows.append(
            {
                "checkpoint": checkpoint,
                "cumulative_exact_candidates": cumulative_exact,
                "candidate_recovery": cumulative_exact / len(CASE_IDS),
                "cumulative_agent_calls": stage_calls["s0"]
                + sum(stage_calls[stage] for stage in included),
                "cumulative_token_cost_usd": stage_costs["s0"]
                + sum(stage_costs[stage] for stage in included),
            }
        )
    report = {
        "schema_version": "verifier-gated-cost-v1",
        "price_schedule_usd_per_million_tokens": {
            "uncached_input": float(pricing["uncached_input_per_million_usd"]),
            "cached_input": float(pricing["cached_input_per_million_usd"]),
            "cache_write_input": float(pricing["cache_write_input_per_million_usd"]),
            "output": float(pricing["output_per_million_usd"]),
        },
        "source_bill_usd": float(pricing["source_bill_usd"]),
        "initial_panel_cost_source": "recorded_usage_with_campaign_calibration",
        "initial_panel_cost_usd": stage_costs["s0"],
        "base_cost_calibration_factor": calibration,
        "stage_calls": dict(stage_calls),
        "stage_cost_usd": dict(stage_costs),
        "recorded_stage_tokens": {stage: dict(values) for stage, values in stage_tokens.items()},
        "missing_terminal_usage": dict(missing),
        "missing_s2_imputation_base_usd": float(
            pricing["s2_missing_usage_imputation_base_usd"]
        ),
        "local_preprocessing_charged": False,
    }
    write_json(output / "cost-method.json", report)
    return rows, report


def matrix_markdown(matrix: dict[str, list[str]]) -> str:
    lines = [
        "```text",
        "CASE " + " ".join(f"{index:02d}" for index in range(1, 21)),
    ]
    for stage in ("S0", "J0", "C1", "J1", "S2", "J2", "S3"):
        lines.append(f"{stage:<4} " + " ".join(f"{value:>2}" for value in matrix[stage]))
    lines.extend(
        [
            "status complete=20 running=0 failed=0; finalized cumulative exact=18/20",
            "```",
        ]
    )
    return "\n".join(lines)


def readme_text(matrix: dict[str, list[str]]) -> str:
    return f"""# Verifier-gated scaling

One ordinary adapted-Codex solve per problem was followed by blind verifier
decisions and only the authorized solver calls. The schedule was
`S0 -> J0 -> C1 -> J1 -> S2 -> J2 -> S3`; `C1` received the initial trace,
CIFs, and review reason, while `S2` and `S3` were fresh ordinary solves.
Candidates were retained cumulatively and declared alternatives counted as
exact recoveries.

## Result

| Checkpoint | Cumulative exact candidates | Recovery | Cumulative agent calls | Token cost |
| --- | ---: | ---: | ---: | ---: |
| S0 | 13/20 | 65% | 20 | $62.9920 |
| C1 | 17/20 | 85% | 52 | $140.5061 |
| S2 | 18/20 | 90% | 73 | $184.1190 |
| S3 | 18/20 | 90% | 88 | $216.5979 |

Token costs use each stage's recorded token mix under the frozen price schedule,
then apply the campaign-wide calibration to the $446.15 source bill. In
particular, S0 is the measured cost of replicate 1, not one eighth of that bill.

## Case-level execution matrix

`E` means the primary CIF was exact, `A` means an alternative was exact, `M`
means no submitted CIF was exact, and `--` means the gate ended that case.
For reviews, `S`/`C` mean stop/continue; `+` marks a retrospectively correct
decision and `!` an incorrect decision.

{matrix_markdown(matrix)}

## Artifact layout

- `scaling-curve.csv` contains the plotted recovery/cost points.
- `outcomes.csv` and `stage-matrix.csv` contain the per-case outcomes.
- `attempts/vh-*/` contains every applicable prompt, decision, compressed
  chronological trace, response, submitted CIF, verifier result, and launch.
- `candidate-pool/` under each case preserves all structures cumulatively.
- `source-metadata/` freezes the panel, conditions, prompts, policy, and hashes.
- `cost-method.json` records token counts, prices, calibration, and imputation.
- `SHA256SUMS` authenticates every normalized artifact.

The hidden references are not included. Agents never received a reference CIF
or verifier result; those were applied only after each solver stage for
retrospective evaluation.
"""


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def normalize(raw_root: Path, initial_source: Path, output: Path, config_path: Path) -> None:
    raw_root = raw_root.resolve()
    initial_source = initial_source.resolve()
    output = output.resolve()
    config_path = config_path.resolve()
    if output.exists() and any(output.iterdir()):
        raise RuntimeError(f"refusing to overwrite nonempty output: {output}")
    output.mkdir(parents=True, exist_ok=True)
    config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    panel_path = (REPO_ROOT / config["panel"]).resolve()
    panel = read_json(panel_path)
    problems = {item["problem_id"]: item for item in panel["problems"]}
    if tuple(sorted(problems)) != CASE_IDS:
        raise ValueError("panel is not the frozen 20-case roster")

    source_metadata = output / "source-metadata"
    copy_text(config_path, source_metadata / "experiment.toml")
    copy_json(panel_path, source_metadata / "panel.json")
    initial_condition = initial_source / "source-metadata/condition.toml"
    if initial_condition.is_file():
        copy_initial_condition(initial_condition, source_metadata / "initial-condition.toml")
    for source, name in (
        (REPO_ROOT / config["judge_condition"], "judge-condition.toml"),
        (REPO_ROOT / config["solver_condition"], "solver-condition.toml"),
        (REPO_ROOT / config["judge_wrapper"], "judge-wrapper.md"),
        (REPO_ROOT / config["judge_policy"], "judge-policy.md"),
        (REPO_ROOT / config["continuation_prompt"], "continuation-prompt.md"),
        (REPO_ROOT / "experiments/inference-scaling/llm-verifier/judge-v1/manifest.json", "judge-manifest.json"),
        (REPO_ROOT / "experiments/agent-adaptation/artifacts/adapted-codex/manifest.json", "capability-manifest.json"),
    ):
        if source.is_file():
            (copy_json if source.suffix == ".json" else copy_text)(source, source_metadata / name)

    matrix = {stage: [] for stage in ("S0", "J0", "C1", "J1", "S2", "J2", "S3")}
    outcome_rows = []
    bundle_cases = []
    for case_id in CASE_IDS:
        raw_attempt = raw_root / "attempts" / case_id
        initial_attempt = initial_source / "attempts" / case_id
        chain = read_json(raw_attempt / "hybrid-chain.json")
        destination = output / "attempts" / case_id
        problem = problems[case_id]
        metadata = problem["metadata"]
        write_json(
            destination / "assignment.json",
            {
                "schema_version": "verifier-gated-assignment-v1",
                "problem_id": case_id,
                "formula": metadata["formula"],
                "source_case_id": metadata["source"]["case_id"],
                "pattern_sha256": problem["problem_input"]["files"][0]["sha256"],
                "reference_sha256": problem["solution"]["sha256"],
                "initial_condition": "adapted-codex",
                "judge": "pxrd-stop-continue-judge-v1",
            },
        )
        normalize_initial(initial_attempt, destination / "initial", chain)

        for round_name, stage in ROUND_STAGE.items():
            source = raw_attempt / "rounds" / round_name
            if source.is_dir():
                normalize_round(source, destination / round_name, stage, chain)
        copy_cifs(raw_attempt / "candidate-pool", destination / "candidate-pool")
        sanitized_chain = json.loads(sanitize(json.dumps(chain)))
        write_json(destination / "chain.json", sanitized_chain)

        snapshots = {item["label"]: item for item in chain["snapshots"]}
        decisions = {item["review_index"]: item for item in chain["reviews"]}
        s0 = snapshots.get("initial")
        c1 = snapshots.get("continuation-01")
        s2 = snapshots.get("fresh-02")
        s3 = snapshots.get("fresh-03")
        codes = {
            "S0": solver_code(s0),
            "J0": judge_code(decisions.get(0, {}).get("decision"), s0["candidates_exact"] if s0 else None),
            "C1": solver_code(c1),
            "J1": judge_code(decisions.get(1, {}).get("decision"), c1["candidates_exact"] if c1 else None),
            "S2": solver_code(s2),
            "J2": judge_code(decisions.get(2, {}).get("decision"), s2["candidates_exact"] if s2 else None),
            "S3": solver_code(s3),
        }
        for stage, code in codes.items():
            matrix[stage].append(code)

        cumulative = []
        first_exact = None
        for stage, snapshot in (("S0", s0), ("C1", c1), ("S2", s2), ("S3", s3)):
            if snapshot and snapshot["candidates_exact"] and first_exact is None:
                first_exact = stage
            cumulative.append(bool(snapshot and snapshot["candidates_exact"]))
        row = {
            "problem_id": case_id,
            "source_case_id": metadata["source"]["case_id"],
            "formula": metadata["formula"],
            "s0": codes["S0"],
            "j0": codes["J0"],
            "c1": codes["C1"],
            "j1": codes["J1"],
            "s2": codes["S2"],
            "j2": codes["J2"],
            "s3": codes["S3"],
            "first_exact_stage": first_exact or "",
            "cumulative_candidates_exact": any(cumulative),
            "termination": chain["termination"],
        }
        outcome_rows.append(row)
        bundle_cases.append(
            {
                "problem_id": case_id,
                "source_case_id": row["source_case_id"],
                "formula": row["formula"],
                "stage_codes": codes,
                "first_exact_stage": first_exact,
                "cumulative_candidates_exact": any(cumulative),
                "termination": chain["termination"],
                "chain_sha256": sha256(destination / "chain.json"),
            }
        )

    curve, _cost = cost_report(output, config, initial_source, raw_root)
    write_csv(
        output / "scaling-curve.csv",
        [
            "checkpoint",
            "cumulative_exact_candidates",
            "candidate_recovery",
            "cumulative_agent_calls",
            "cumulative_token_cost_usd",
        ],
        curve,
    )
    outcome_fields = list(outcome_rows[0])
    write_csv(output / "outcomes.csv", outcome_fields, outcome_rows)
    write_csv(
        output / "stage-matrix.csv",
        ["stage", *[f"case_{index:02d}" for index in range(1, 21)]],
        [
            {"stage": stage, **{f"case_{index:02d}": value for index, value in enumerate(matrix[stage], 1)}}
            for stage in ("S0", "J0", "C1", "J1", "S2", "J2", "S3")
        ],
    )
    (output / "README.md").write_text(readme_text(matrix), encoding="utf-8")
    write_json(
        source_metadata / "run.json",
        {
            "schema_version": "verifier-gated-run-v1",
            "schedule": config["schedule"],
            "problem_count": 20,
            "parallel_agent_calls": int(config["parallel_agent_calls"]),
            "judge_timeout_seconds": int(config["judge_timeout_seconds"]),
            "solver_timeout_seconds": int(config["solver_timeout_seconds"]),
            "model": "gpt-5.6-sol",
            "reasoning_effort": "high",
            "oracle_available_to_agents": False,
            "alternatives_count_as_exact": True,
        },
    )
    write_json(
        output / "bundle.json",
        {
            "schema_version": "verifier-gated-result-v1",
            "result_id": "verifier-gated-scaling",
            "panel": "inference-scaling-20",
            "case_count": 20,
            "completed_count": 20,
            "cumulative_candidates_exact_count": 18,
            "recovery_curve": {row["checkpoint"]: row["cumulative_exact_candidates"] for row in curve},
            "cost_curve_usd": {row["checkpoint"]: row["cumulative_token_cost_usd"] for row in curve},
            "cases": bundle_cases,
            "contract_sha256": {
                path.name: sha256(path)
                for path in sorted(source_metadata.iterdir())
                if path.is_file()
            },
        },
    )
    write_checksums(output)
    check(output)


def iter_text(path: Path) -> str:
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="utf-8", errors="replace") as stream:
            return stream.read()
    return path.read_text(encoding="utf-8", errors="replace")


def write_checksums(root: Path) -> None:
    paths = [path for path in sorted(root.rglob("*")) if path.is_file() and path.name != "SHA256SUMS"]
    text = "".join(f"{sha256(path)}  {path.relative_to(root)}\n" for path in paths)
    (root / "SHA256SUMS").write_text(text, encoding="utf-8")


def check(root: Path) -> None:
    root = root.resolve()
    bundle = read_json(root / "bundle.json")
    if bundle["case_count"] != 20 or bundle["completed_count"] != 20:
        raise AssertionError("bundle is not complete")
    if set(item["problem_id"] for item in bundle["cases"]) != set(CASE_IDS):
        raise AssertionError("case roster mismatch")
    if bundle["recovery_curve"] != EXPECTED_RECOVERY:
        raise AssertionError(f"recovery mismatch: {bundle['recovery_curve']}")
    for checkpoint, expected in EXPECTED_COST.items():
        actual = float(bundle["cost_curve_usd"][checkpoint])
        if abs(actual - expected) > 0.001:
            raise AssertionError(f"{checkpoint} cost mismatch: {actual} != {expected}")

    sums = {}
    for line in (root / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        sums[relative] = digest
    current = {
        str(path.relative_to(root)): sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.name != "SHA256SUMS"
    }
    if sums != current:
        raise AssertionError("SHA256SUMS does not match the normalized tree")

    if list(root.rglob("reference.cif")):
        raise AssertionError("hidden reference CIF found in result")
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix == ".cif":
            continue
        text = iter_text(path)
        for forbidden in FORBIDDEN_TEXT:
            if forbidden in text:
                raise AssertionError(f"forbidden text {forbidden!r} in {path}")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                raise AssertionError(f"possible secret in {path}: {pattern.pattern}")

    try:
        from pymatgen.core import Structure
    except ImportError as error:
        raise RuntimeError("pymatgen is required for CIF integrity checking") from error
    cifs = list(root.rglob("*.cif"))
    if not cifs:
        raise AssertionError("normalized result contains no CIFs")
    for path in cifs:
        Structure.from_file(path)


def main() -> int:
    args = parse_args()
    if args.check:
        if any(value is not None for value in (args.raw_root, args.initial_source, args.output)):
            raise SystemExit("--check cannot be combined with normalization arguments")
        check(args.check)
        print(f"validated {args.check.resolve()}")
        return 0
    if not args.raw_root or not args.initial_source or not args.output:
        raise SystemExit("normalization requires --raw-root, --initial-source, and --output")
    normalize(args.raw_root, args.initial_source, args.output, args.config)
    print(f"normalized and validated {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
