#!/usr/bin/env python3
"""Package a blind Rwp-selector run with post-hoc exact-match evaluation."""

from __future__ import annotations

import argparse
import copy
import csv
import json
import shutil
from pathlib import Path
from typing import Any

from pymatgen.core import Structure

from verifiable_pxrd.matching import MATCHER_PARAMETERS, matcher


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--panel", type=Path, required=True)
    parser.add_argument("--selector-run", type=Path, required=True)
    parser.add_argument("--source-campaign", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def portable_path(value: str, repo_root: Path, selector_run: Path) -> str:
    path = Path(value)
    if not path.is_absolute():
        return value
    try:
        return path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        pass
    try:
        suffix = path.resolve().relative_to(selector_run)
        return (Path("selector-run") / suffix).as_posix()
    except ValueError:
        return value


def sanitize_paths(value: Any, repo_root: Path, selector_run: Path) -> Any:
    if isinstance(value, dict):
        return {
            key: sanitize_paths(item, repo_root, selector_run)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [sanitize_paths(item, repo_root, selector_run) for item in value]
    if isinstance(value, str) and value.startswith("/"):
        return portable_path(value, repo_root, selector_run)
    return value


def source_stats(source_campaign: Path) -> tuple[int, int]:
    attempts = 0
    attempts_with_candidates = 0
    for bundle_path in sorted(source_campaign.glob("replicate-*/bundle.json")):
        replicate = bundle_path.parent
        bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
        for record in bundle.get("cases", []):
            attempts += 1
            case_id = str(record.get("case_id") or record.get("problem_id"))
            source_name = str(record.get("source_attempt_name") or case_id)
            options = [
                replicate / "attempts" / case_id / "submission",
                replicate / "attempts" / source_name / "submission",
            ]
            submission = next((path for path in options if path.is_dir()), None)
            if submission is not None and any(submission.glob("*.cif")):
                attempts_with_candidates += 1
    return attempts, attempts_with_candidates


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    panel = args.panel.resolve()
    selector_run = args.selector_run.resolve()
    source_campaign = args.source_campaign.resolve()
    output = args.output.resolve()
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"output directory is not empty: {output}")
    output.mkdir(parents=True, exist_ok=True)

    manifest = json.loads((panel / "manifest.json").read_text(encoding="utf-8"))
    problems = sorted(manifest["problems"], key=lambda item: int(item["order"]))
    active_matcher = matcher()
    case_rows: list[dict[str, Any]] = []
    candidate_rows: list[dict[str, Any]] = []
    protocol: dict[str, Any] | None = None

    for problem in problems:
        case_id = str(problem["problem_id"])
        reference_path = panel / "problems" / case_id / "solution" / "reference.cif"
        report_path = selector_run / "cases" / case_id / "report.json"
        report = json.loads(report_path.read_text(encoding="utf-8"))
        reference = Structure.from_file(reference_path, primitive=False)
        formula = reference.composition.reduced_formula
        if protocol is None:
            protocol = copy.deepcopy(report["protocol"])

        exact_by_sha: dict[str, bool] = {}
        ranked: list[dict[str, Any]] = []
        for rank, result in enumerate(report.get("results", []), start=1):
            candidate_path = Path(result["candidate"])
            is_exact = False
            if result.get("status") == "completed":
                candidate = Structure.from_file(candidate_path, primitive=False)
                is_exact = bool(active_matcher.fit(reference, candidate, symmetric=True))
            exact_by_sha[str(result["sha256"])] = is_exact
            occurrences = result.get("occurrences") or [str(candidate_path)]
            row = {
                "case_id": case_id,
                "formula": formula,
                "rank": rank,
                "rwp_percent": result.get("rwp_percent", ""),
                "exact": is_exact,
                "status": result.get("status", ""),
                "structure_group": result.get("structure_group", ""),
                "sha256": result.get("sha256", ""),
                "occurrence_count": len(occurrences),
                "source_candidate": portable_path(str(candidate_path), repo_root, selector_run),
            }
            candidate_rows.append(row)
            ranked.append({**result, "rank": rank, "exact": is_exact})

        completed = [item for item in ranked if item.get("status") == "completed"]
        exact = [item for item in completed if item["exact"]]
        misses = [item for item in completed if not item["exact"]]
        selected = completed[0] if completed else None
        selected_exact = bool(selected and selected["exact"])
        oracle_exact = bool(exact)
        top2_exact = any(item["exact"] for item in completed[:2])
        best_exact = exact[0] if exact else None
        best_miss = misses[0] if misses else None

        selected_source = (
            portable_path(str(selected["candidate"]), repo_root, selector_run)
            if selected
            else ""
        )
        selected_replicate = next(
            (part for part in Path(selected_source).parts if part.startswith("replicate-")),
            "",
        )
        case_row = {
            "case_id": case_id,
            "formula": formula,
            "declared_candidates": report.get("candidate_count", 0),
            "unique_candidates": report.get("unique_candidate_count", 0),
            "completed_fits": report.get("completed_fit_count", 0),
            "oracle_exact": oracle_exact,
            "selected_exact": selected_exact,
            "top2_exact": top2_exact,
            "best_exact_rank": best_exact["rank"] if best_exact else "",
            "selected_rwp_percent": selected.get("rwp_percent", "") if selected else "",
            "best_exact_rwp_percent": best_exact.get("rwp_percent", "") if best_exact else "",
            "best_miss_rwp_percent": best_miss.get("rwp_percent", "") if best_miss else "",
            "selected_replicate": selected_replicate,
            "selected_source": selected_source,
        }
        case_rows.append(case_row)

        sanitized = sanitize_paths(copy.deepcopy(report), repo_root, selector_run)
        sanitized["gsas_python"] = "$VPBENCH_GSAS_ENV/bin/python"
        sanitized["posthoc_reference_evaluation"] = {
            "reference": portable_path(str(reference_path), repo_root, selector_run),
            "selected_exact": selected_exact,
            "oracle_exact": oracle_exact,
            "top2_exact": top2_exact,
            "best_exact_rank": best_exact["rank"] if best_exact else None,
            "matcher": {
                **MATCHER_PARAMETERS,
                "comparator": "ElementComparator",
                "symmetric": True,
            },
        }
        for result in sanitized.get("results", []):
            result["posthoc_exact"] = exact_by_sha.get(str(result.get("sha256")), False)
        write_json(output / "cases" / case_id / "report.json", sanitized)
        (output / "selected").mkdir(parents=True, exist_ok=True)
        shutil.copy2(selected["candidate"], output / "selected" / f"{case_id}.cif")

    attempts, attempts_with_candidates = source_stats(source_campaign)
    declared_candidates = sum(int(row["declared_candidates"]) for row in case_rows)
    unique_candidates = sum(int(row["unique_candidates"]) for row in case_rows)
    completed_fits = sum(int(row["completed_fits"]) for row in case_rows)
    oracle_count = sum(bool(row["oracle_exact"]) for row in case_rows)
    selected_count = sum(bool(row["selected_exact"]) for row in case_rows)
    top2_count = sum(bool(row["top2_exact"]) for row in case_rows)
    no_exact_cases = [str(row["case_id"]) for row in case_rows if not row["oracle_exact"]]

    summary = {
        "schema_version": "1",
        "protocol_id": "blind-comparable-gsas-rwp-v1",
        "source_campaign": portable_path(str(source_campaign), repo_root, selector_run),
        "panel": portable_path(str(panel), repo_root, selector_run),
        "source_attempt_count": attempts,
        "attempts_with_declared_candidates": attempts_with_candidates,
        "declared_candidate_count": declared_candidates,
        "unique_candidate_fit_count": unique_candidates,
        "completed_fit_count": completed_fits,
        "case_count": len(case_rows),
        "oracle_exact_count": oracle_count,
        "selected_exact_count": selected_count,
        "top2_exact_count": top2_count,
        "conditional_selection_count": selected_count,
        "conditional_oracle_count": oracle_count,
        "no_exact_candidate_case_ids": no_exact_cases,
    }
    write_json(output / "summary.json", summary)
    assert protocol is not None
    protocol = sanitize_paths(protocol, repo_root, selector_run)
    protocol["posthoc_evaluator"] = {
        **MATCHER_PARAMETERS,
        "comparator": "ElementComparator",
        "symmetric": True,
    }
    write_json(output / "protocol.json", protocol)
    write_csv(
        output / "case-summary.csv",
        case_rows,
        list(case_rows[0]),
    )
    write_csv(
        output / "candidate-rankings.csv",
        candidate_rows,
        list(candidate_rows[0]),
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
