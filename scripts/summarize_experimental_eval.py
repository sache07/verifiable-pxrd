#!/usr/bin/env python3
"""Summarize two paired panels on a measured dataset from their public bundles.

Reads <root>/<condition>/per_attempt.json (default root:
results/experimental-eval/divalent-tungstates-PG15) and writes <root>/summary.json:
per-scan means of replayed observed-data Rwp (10.1-99.9 deg, weights 1/max(counts,1)),
the mean and median of per-scan means, paired tests over scans (exact two-sided Wilcoxon
signed-rank, two-sided sign test, seeded bootstrap CI of the mean paired difference) and
hidden-phase recovery counts. Pure standard library.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import random
import statistics as st
from pathlib import Path

HIDDEN = [("case-013", "Pb2WO5"), ("case-013", "Pb3WO6"), ("case-014", "Sr2WO5")]


def load(root: Path, condition: str) -> list[dict]:
    return json.loads((root / condition / "per_attempt.json").read_text())


def scan_means(rows: list[dict]) -> dict[str, dict]:
    by: dict[str, list[float]] = {}
    for row in rows:
        value = row.get("replay_interior_rwp")
        by.setdefault(row["case"], [])
        if isinstance(value, (int, float)):
            by[row["case"]].append(float(value))
    return {
        case: {"mean": st.mean(v) if v else None, "verified_attempts": len(v), "values": v}
        for case, v in sorted(by.items())
    }


def wilcoxon_exact(diffs: list[float]) -> float:
    d = [x for x in diffs if x != 0]
    n = len(d)
    order = sorted(range(n), key=lambda i: abs(d[i]))
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and abs(d[order[j + 1]]) == abs(d[order[i]]):
            j += 1
        for k in range(i, j + 1):
            ranks[order[k]] = (i + j) / 2 + 1
        i = j + 1
    w_plus = sum(r for r, x in zip(ranks, d) if x > 0)
    total = sum(ranks)
    count = extreme = 0
    for signs in itertools.product((0, 1), repeat=n):
        w = sum(r for r, s in zip(ranks, signs) if s)
        count += 1
        if min(w, total - w) <= min(w_plus, total - w_plus) + 1e-12:
            extreme += 1
    return min(1.0, extreme / count)


def sign_test(diffs: list[float]) -> float:
    d = [x for x in diffs if x != 0]
    n, k = len(d), sum(1 for x in d if x < 0)
    tail = sum(math.comb(n, i) for i in range(0, min(k, n - k) + 1)) / 2**n
    return min(1.0, 2 * tail)


def bootstrap_ci(diffs: list[float], seed: int = 20261104, resamples: int = 20000) -> list[float]:
    rng = random.Random(seed)
    means = sorted(st.mean(rng.choices(diffs, k=len(diffs))) for _ in range(resamples))
    return [means[int(0.025 * resamples)], means[int(0.975 * resamples) - 1]]


def hidden_recovery(rows: list[dict]) -> dict[str, str]:
    out = {}
    for case, phase in HIDDEN:
        attempts = [r for r in rows if r["case"] == case]
        hits = 0
        for r in attempts:
            matched = any(
                (p.get("target_matches") or {}).get(phase, {}).get("match") is True
                if isinstance((p.get("target_matches") or {}).get(phase), dict)
                else bool((p.get("target_matches") or {}).get(phase))
                for p in r.get("phases", [])
            )
            hits += matched
        out[f"{phase} on {case}"] = f"{hits}/{len(attempts)}"
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default="results/experimental-eval/divalent-tungstates-PG15")
    parser.add_argument("--baseline", default="baseline")
    parser.add_argument("--treatment", default="evolved")
    args = parser.parse_args()
    root = Path(args.root)
    base_rows, treat_rows = load(root, args.baseline), load(root, args.treatment)
    base, treat = scan_means(base_rows), scan_means(treat_rows)
    reference = {}
    for row in treat_rows:
        reference.setdefault(row["case"], row.get("ceder_interior_rwp"))
    cases = sorted(set(base) & set(treat))
    diffs = [treat[c]["mean"] - base[c]["mean"] for c in cases]
    summary = {
        "metric": "replayed observed-data Rwp (%), 10.1-99.9 deg 2theta, weights 1/max(counts,1); per-scan mean over verified attempts",
        "per_scan": {
            c: {
                args.baseline: base[c]["mean"], args.treatment: treat[c]["mean"],
                "difference": treat[c]["mean"] - base[c]["mean"],
                "deposited_reference": reference.get(c),
                f"{args.baseline}_verified": base[c]["verified_attempts"],
                f"{args.treatment}_verified": treat[c]["verified_attempts"],
            }
            for c in cases
        },
        "mean_of_scan_means": {args.baseline: st.mean(base[c]["mean"] for c in cases), args.treatment: st.mean(treat[c]["mean"] for c in cases)},
        "median_of_scan_means": {args.baseline: st.median(base[c]["mean"] for c in cases), args.treatment: st.median(treat[c]["mean"] for c in cases)},
        "paired_over_scans": {
            "mean_difference": st.mean(diffs),
            "scans_lower": sum(d < 0 for d in diffs),
            "scans": len(diffs),
            "wilcoxon_two_sided_exact_p": wilcoxon_exact(diffs),
            "sign_test_two_sided_p": sign_test(diffs),
            "bootstrap_95ci_mean_difference": bootstrap_ci(diffs),
        },
        "verified_attempts": {args.baseline: sum(base[c]["verified_attempts"] for c in cases), args.treatment: sum(treat[c]["verified_attempts"] for c in cases)},
        "hidden_phase_recovery": {args.baseline: hidden_recovery(base_rows), args.treatment: hidden_recovery(treat_rows)},
    }
    (root / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: summary[k] for k in ("mean_of_scan_means", "paired_over_scans", "verified_attempts", "hidden_phase_recovery")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
