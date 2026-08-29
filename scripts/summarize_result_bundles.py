#!/usr/bin/env python3
"""Build case, overlap, and ordered pass@k tables from normalized result bundles."""

from __future__ import annotations

import argparse
import csv
import json
import re
from itertools import combinations
from pathlib import Path
from typing import Any


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def candidate_exact_case_ids(payload: dict[str, Any]) -> set[str]:
    """Return candidate-set coverage from either normalized bundle schema."""

    values = payload.get("candidates_exact_case_ids", payload.get("exact_case_ids"))
    if values is None:
        raise KeyError("bundle has neither candidates_exact_case_ids nor exact_case_ids")
    return set(map(str, values))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--baseline", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    output = (args.output_dir or root).resolve()
    output.mkdir(parents=True, exist_ok=True)
    bundles = {}
    bundle_paths = {}
    for path in sorted(root.rglob("bundle.json")):
        payload = load(path)
        name = str(payload.get("result_id") or path.parent.name)
        if name in bundles:
            raise ValueError(f"duplicate result_id {name}: {bundle_paths[name]} and {path}")
        bundles[name] = payload
        bundle_paths[name] = path
    successes = {name: candidate_exact_case_ids(payload) for name, payload in bundles.items()}
    case_ids = sorted(
        {str(item["case_id"]) for payload in bundles.values() for item in payload["cases"]}
    )
    if args.baseline:
        baseline = load(args.baseline.resolve())
        name = "matsci-codex-scale-true-reference"
        successes[name] = {
            str(item["problem_id"])
            for item in baseline["cases"]
            if bool(item["standardized_scale_false_success"])
        }
        case_ids = sorted({str(item["problem_id"]) for item in baseline["cases"]})
    names = sorted(successes)
    with (output / "inference-scaling-case-matrix.csv").open(
        "w", encoding="utf-8", newline=""
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=["problem_id", *names])
        writer.writeheader()
        for case_id in case_ids:
            writer.writerow(
                {"problem_id": case_id, **{name: int(case_id in successes[name]) for name in names}}
            )
    overlaps = []
    for left, right in combinations(names, 2):
        a, b = successes[left], successes[right]
        overlaps.append(
            {
                "left": left,
                "right": right,
                "intersection": len(a & b),
                "union": len(a | b),
                "left_only": len(a - b),
                "right_only": len(b - a),
            }
        )
    payload = {
        "schema_version": "1",
        "panel_case_count": len(case_ids),
        "runs": {
            name: {
                "exact": len(values),
                "rate": len(values) / len(case_ids),
                "exact_case_ids": sorted(values),
            }
            for name, values in successes.items()
        },
        "pairwise_overlaps": overlaps,
    }
    (output / "inference-scaling-summary.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    replicate_pattern = re.compile(r"^(?P<family>.+)-r(?P<replicate>[1-9][0-9]*)$")
    families: dict[str, list[tuple[int, str]]] = {}
    for name in bundles:
        match = replicate_pattern.fullmatch(name)
        if match:
            families.setdefault(match.group("family"), []).append(
                (int(match.group("replicate")), name)
            )
    curve_rows = []
    for family, members in sorted(families.items()):
        cumulative: set[str] = set()
        individual_counts = []
        expected = list(range(1, len(members) + 1))
        observed = [replicate for replicate, _ in sorted(members)]
        if observed != expected:
            raise ValueError(f"non-contiguous replicates for {family}: {observed}")
        for replicate, name in sorted(members):
            current = successes[name]
            cumulative.update(current)
            individual_counts.append(len(current))
            curve_rows.append(
                {
                    "family": family,
                    "k": replicate,
                    "replicate_exact": len(current),
                    "mean_individual_exact_through_k": sum(individual_counts)
                    / len(individual_counts),
                    "cumulative_pass_at_k": len(cumulative),
                    "cumulative_rate": len(cumulative) / len(case_ids),
                }
            )
    with (output / "inference-scaling-curve.csv").open("w", encoding="utf-8", newline="") as stream:
        fields = [
            "family",
            "k",
            "replicate_exact",
            "mean_individual_exact_through_k",
            "cumulative_pass_at_k",
            "cumulative_rate",
        ]
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(curve_rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
