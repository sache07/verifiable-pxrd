#!/usr/bin/env python3
"""Build a per-case outcome matrix and order-invariant pass@k plot for one run family."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from pathlib import Path
from typing import Any


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_case_order(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    orders = [int(row["order"]) for row in rows]
    if orders != list(range(1, len(rows) + 1)):
        raise ValueError(f"non-contiguous case order in {path}: {orders}")
    return rows


def expected_pass_at_k(success_sets: list[set[str]], case_ids: list[str], k: int) -> float:
    """Expected oracle coverage for a uniform k-subset of observed replicates."""

    n = len(success_sets)
    if not 1 <= k <= n:
        raise ValueError(f"k must be between 1 and {n}, received {k}")
    denominator = math.comb(n, k)
    total = 0.0
    for case_id in case_ids:
        successes = sum(case_id in values for values in success_sets)
        misses = n - successes
        miss_probability = math.comb(misses, k) / denominator if misses >= k else 0.0
        total += 1.0 - miss_probability
    return total


def exact_outcome(case: dict[str, Any], metric: str) -> bool:
    if metric == "selected":
        return bool(case.get("selected_exact", case.get("selected_exact_success", False)))
    return bool(case.get("candidates_exact", case.get("exact_success", False)))


def exact_case_ids(bundle: dict[str, Any], metric: str) -> set[str]:
    return {str(case["case_id"]) for case in bundle["cases"] if exact_outcome(case, metric)}


def write_matrix_csv(
    path: Path,
    members: list[tuple[int, dict[str, Any]]],
    case_ids: list[str],
    metric: str,
) -> None:
    fields = ["replicate", *case_ids, "exact_count", "completed_count", "case_count"]
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for replicate, bundle in members:
            outcomes = {
                str(case["case_id"]): int(exact_outcome(case, metric)) for case in bundle["cases"]
            }
            writer.writerow(
                {
                    "replicate": replicate,
                    **outcomes,
                    "exact_count": sum(outcomes.values()),
                    "completed_count": int(bundle["completed_count"]),
                    "case_count": int(bundle["case_count"]),
                }
            )


def write_matrix_markdown(
    path: Path,
    title: str,
    members: list[tuple[int, dict[str, Any]]],
    cases: list[dict[str, str]],
    metric: str,
) -> None:
    case_ids = [row["problem_id"] for row in cases]
    labels = [f"{index:02d}" for index in range(1, len(cases) + 1)]
    lines = [
        f"# {title} outcome matrix",
        "",
        (
            "Each symbol is exact StructureMatcher recovery by the primary `selected.cif`."
            if metric == "selected"
            else "Each symbol is exact StructureMatcher recovery by `selected.cif` or a declared alternative."
        ),
        "`Complete` records closed attempts, independently of exactness.",
        "",
        "```text",
        "       " + "  ".join(labels) + "    Exact   Complete",
        "       " + "  ".join("──" for _ in labels) + "    ─────   ────────",
    ]
    for replicate, bundle in members:
        outcomes = {str(case["case_id"]): exact_outcome(case, metric) for case in bundle["cases"]}
        symbols = "  ".join(
            "✓ " if outcomes[case_id] else "× "  # noqa: RUF001
            for case_id in case_ids
        )
        lines.append(
            f"rep {replicate:<2} {symbols}   {sum(outcomes.values()):>2}/{len(case_ids)}"
            f"    {int(bundle['completed_count']):>2}/{len(case_ids)}"
        )
    lines.extend(
        [
            "```",
            "",
            "## Case key",
            "",
            "| # | ID | Formula | Category |",
            "| ---: | --- | --- | --- |",
        ]
    )
    for index, row in enumerate(cases, start=1):
        lines.append(
            f"| {index:02d} | `{row['problem_id']}` | {row['formula']} | {row['category']} |"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_curve_csv(
    path: Path,
    members: list[tuple[int, dict[str, Any]]],
    case_ids: list[str],
    metric: str,
) -> list[dict[str, float | int]]:
    success_sets = [exact_case_ids(bundle, metric) for _, bundle in members]
    prefix: set[str] = set()
    mean_pass1 = sum(map(len, success_sets)) / len(success_sets)
    rows: list[dict[str, float | int]] = []
    for (replicate, _bundle), current in zip(members, success_sets, strict=True):
        prefix.update(current)
        expected = expected_pass_at_k(success_sets, case_ids, replicate)
        rows.append(
            {
                "k": replicate,
                "replicate_exact": len(current),
                "mean_pass_at_1": mean_pass1,
                "expected_oracle_pass_at_k": expected,
                "expected_oracle_rate": expected / len(case_ids),
                "ordered_prefix_union": len(prefix),
                "ordered_prefix_rate": len(prefix) / len(case_ids),
            }
        )
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def write_plot(
    output: Path,
    title: str,
    rows: list[dict[str, float | int]],
    case_count: int,
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    x = [int(row["k"]) for row in rows]
    expected = [float(row["expected_oracle_pass_at_k"]) for row in rows]
    mean_pass1 = float(rows[0]["mean_pass_at_1"])

    plt.rcParams.update({"font.size": 10, "axes.titlesize": 13, "axes.labelsize": 11})
    figure, axis = plt.subplots(figsize=(7.2, 4.5), constrained_layout=True)
    axis.plot(
        x,
        expected,
        color="#2369bd",
        marker="o",
        linewidth=2.4,
        label="Expected oracle pass@k",
    )
    axis.axhline(
        mean_pass1,
        color="#5f6368",
        linewidth=1.4,
        linestyle=":",
        label=f"Mean pass@1 ({mean_pass1:.2f}/{case_count})",
    )
    axis.set_title(f"{title}: inference-time scaling")
    axis.set_xlabel("Independent samples, k")
    axis.set_ylabel(f"Exact cases out of {case_count}")
    axis.set_xticks(x)
    axis.set_ylim(0, case_count)
    axis.grid(axis="y", color="#d9dde3", linewidth=0.8, alpha=0.8)
    axis.spines[["top", "right"]].set_visible(False)
    axis.legend(loc="lower right", frameon=False)
    for suffix in ("png", "svg"):
        figure.savefig(output.with_suffix(f".{suffix}"), dpi=220 if suffix == "png" else None)
    plt.close(figure)


def main() -> int:
    repository = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--family", required=True, help="result_id prefix before -rN")
    parser.add_argument("--title", required=True)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument(
        "--metric",
        choices=("selected", "candidates"),
        default="candidates",
        help="score only selected.cif or selected.cif plus declared alternatives",
    )
    parser.add_argument(
        "--case-order",
        type=Path,
        default=repository / "pxrd-bench/panels/inference-scaling-20/problem-order.csv",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    output = (args.output_dir or root).resolve()
    output.mkdir(parents=True, exist_ok=True)
    pattern = re.compile(rf"^{re.escape(args.family)}-r(?P<replicate>[1-9][0-9]*)$")
    members = []
    for path in sorted(root.rglob("bundle.json")):
        bundle = load(path)
        match = pattern.fullmatch(str(bundle.get("result_id", "")))
        if match:
            members.append((int(match.group("replicate")), bundle))
    members.sort(key=lambda item: item[0])
    expected_replicates = list(range(1, len(members) + 1))
    if [replicate for replicate, _ in members] != expected_replicates:
        raise ValueError(f"non-contiguous or empty replicate set for {args.family}")

    cases = load_case_order(args.case_order.resolve())
    case_ids = [row["problem_id"] for row in cases]
    for replicate, bundle in members:
        observed = {str(case["case_id"]) for case in bundle["cases"]}
        if observed != set(case_ids):
            raise ValueError(f"replicate {replicate} does not match the frozen panel")

    write_matrix_csv(output / "outcome-matrix.csv", members, case_ids, args.metric)
    write_matrix_markdown(output / "outcome-matrix.md", args.title, members, cases, args.metric)
    curve = write_curve_csv(output / "scaling-curve.csv", members, case_ids, args.metric)
    write_plot(output / "scaling-curve", args.title, curve, len(case_ids))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
