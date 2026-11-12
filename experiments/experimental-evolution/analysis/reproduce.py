"""Rebuild multiphase result tables from public attempt-level evidence.

No API calls, refinements, private archives, or manuscript checkout are required.
Use --figures to rebuild the paper plots from the bundled plotting inputs as well.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import statistics
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "results/experimental-eval/divalent-tungstates-PG15"
CONDITIONS = [
    "baseline",
    "evolved",
    "framework-access",
    "framework-plus-v6",
    "evolved-framework-v5",
]
LABELS = {
    "baseline": "Baseline",
    "evolved": "Evolved v6",
    "framework-access": "Framework access",
    "framework-plus-v6": "Framework + v6",
    "evolved-framework-v5": "Evolved framework v5",
    "baseline-sol-high": "Sol high",
    "baseline-opus": "Opus",
}
EXPECTED = {
    "baseline": 7.89888288683027,
    "evolved": 6.708885087581412,
    "framework-access": 5.978864,
    "framework-plus-v6": 6.487135,
    "evolved-framework-v5": 6.441631,
}


def load(path):
    return json.loads(path.read_text())


def residual(row):
    return row.get("replay_interior_rwp", row.get("replay_interior_rwp_percent"))


def recovered(row, formula="Sr2WO5"):
    for phase in row.get("phases", []):
        value = (phase.get("target_matches") or {}).get(formula, False)
        is_match = value.get("match", False) if isinstance(value, dict) else value is True
        if is_match:
            return True
    return False


def write_csv(path, rows):
    if not rows:
        return
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def summarize(rows):
    by = {}
    for row in rows:
        by.setdefault(row["case"], []).append(row)
    assert len(rows) in (15, 45) and len(by) == 15
    values = {case: [residual(r) for r in attempts] for case, attempts in by.items()}
    assert all(v is not None for group in values.values() for v in group)
    means = [statistics.mean(v) for v in values.values()]
    return dict(
        attempts=len(rows),
        measurements=len(by),
        mean_rwp=statistics.mean(means),
        median_rwp=statistics.median(means),
        mean_best_of_three_rwp=statistics.mean(min(v) for v in values.values())
        if len(rows) == 45
        else None,
        mean_minutes=statistics.mean(r["minutes"] for r in rows),
        aggregation="Mean/median of measurement-level means; best-of-three averages each measurement's minimum.",
    )


def validate_plot_inputs(panels):
    """Tie the compact manuscript plotting snapshots to released attempt records."""
    data = load(RESULTS / "paper-data/experimental_transfer/records.json")
    mapping = dict(
        P0="baseline",
        E="evolved",
        F="framework-access",
        FE="framework-plus-v6",
        Fv5="evolved-framework-v5",
    )
    for key, name in mapping.items():
        rows = {(r["case"], r["replicate"]): r for r in panels[name]}
        for case in data["cases"]:
            for item in case["attempts"][key]:
                row = rows[case["case"], item["replicate"]]
                assert abs(item["rwp"] - residual(row)) < 1e-8
                assert abs(item["minutes"] - row["minutes"]) < 1e-6
                assert recovered(item) == recovered(row)
                assert abs(case["pg_rwp"] - row["ceder_interior_rwp"]) < 1e-8
    models = load(RESULTS / "paper-data/experimental_transfer/model_comparison.json")
    high = {(r["case"], r["replicate"]): r for r in panels["baseline-sol-high"]}
    opus = {r["case"]: r for r in panels["baseline-opus"]}
    for case in models["cases"]:
        for item in case["sol_high"]:
            row = high[case["case"], item["replicate"]]
            assert abs(item["rwp"] - residual(row)) < 1e-8
            assert abs(item["minutes"] - row["minutes"]) < 1e-6
        assert abs(case["opus_rwp"] - residual(opus[case["case"]])) < 1e-8
        assert abs(case["opus_minutes"] - opus[case["case"]]["minutes"]) < 1e-6
    evolution = load(RESULTS / "paper-data/framework_evolution/records.json")
    for campaign in evolution["campaigns"].values():
        status = load(
            ROOT / "results/experimental-evolution" / campaign["run"] / "evidence/status.json"
        )
        actual = {j["id"]: j for j in status["jobs"]}
        assert len(actual) == len(campaign["jobs"])
        for job in campaign["jobs"]:
            for field in ("policy", "case_id", "status", "score_100", "score_interval"):
                assert job.get(field) == actual[job["id"]].get(field), (
                    campaign["run"],
                    job["id"],
                    field,
                )


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, default=ROOT / ".runs/multiphase-reproduction")
    p.add_argument("--figures", action="store_true")
    a = p.parse_args()
    a.output = a.output.resolve()
    if a.output.is_relative_to(RESULTS) or a.output.is_relative_to(ROOT / "pxrd-bench"):
        p.error("Write derived outputs outside the frozen input bundles")
    a.output.mkdir(parents=True, exist_ok=True)
    all_rows = []
    aggregates = []
    panels = {}
    for condition in [*CONDITIONS, "baseline-sol-high", "baseline-opus"]:
        rows = load(RESULTS / condition / "per_attempt.json")
        panels[condition] = rows
        summary = summarize(rows)
        if condition in EXPECTED:
            assert abs(summary["mean_rwp"] - EXPECTED[condition]) < 1e-6, (condition, summary)
        aggregates.append(dict(condition=condition, **summary))
        for row in rows:
            all_rows.append(
                dict(
                    condition=condition,
                    case=row["case"],
                    replicate=row["replicate"],
                    rwp=residual(row),
                    minutes=row["minutes"],
                    sr2wo5=recovered(row),
                    source_attempt_id=row.get("source_attempt_id", row["id"]),
                    evidence_status=row.get("evidence_status", "submission_and_trace_available"),
                )
            )
    pg = {r["case"]: r["ceder_interior_rwp"] for r in panels["baseline"]}
    aggregates.insert(
        0,
        dict(
            condition="deposited-pg",
            attempts=15,
            measurements=15,
            mean_rwp=statistics.mean(pg.values()),
            median_rwp=statistics.median(pg.values()),
            mean_best_of_three_rwp=None,
            mean_minutes=None,
            aggregation="One saved deposited calculated profile per measurement; no new refinement.",
        ),
    )
    write_csv(a.output / "aggregate_scores.csv", aggregates)
    write_csv(a.output / "initial_attempts.csv", all_rows)
    repeats = []
    repeat_summary = []
    for condition in CONDITIONS:
        initial = [r for r in panels[condition] if r["case"] == "case-014"]
        follow = [
            r
            for r in load(RESULTS / "followups" / condition / "per_attempt.json")
            if r["case"] == "case-014"
        ]
        indexed = {r["replicate"]: r for r in initial + follow}
        displayed = list(range(1, 10))
        if condition == "framework-access":
            assert residual(indexed[4]) is None and 10 in indexed
            displayed[3] = 10
        hits = 0
        for slot, actual in enumerate(displayed, 1):
            row = indexed[actual]
            hit = recovered(row)
            hits += hit
            repeats.append(
                dict(
                    condition=condition,
                    display_slot=slot,
                    actual_replicate=actual,
                    stage="initial" if actual <= 3 else "follow-up",
                    rwp=residual(row),
                    sr2wo5=hit,
                    replacement_for=4 if actual == 10 else None,
                )
            )
        assert (
            hits
            == {
                "baseline": 0,
                "evolved": 3,
                "framework-access": 0,
                "framework-plus-v6": 5,
                "evolved-framework-v5": 1,
            }[condition]
        )
        repeat_summary.append(
            dict(
                condition=condition,
                recovered=hits,
                displayed_completed=9,
                all_recorded_attempts=len(indexed),
                all_recorded_recovered=sum(recovered(r) for r in indexed.values()),
            )
        )
    write_csv(a.output / "sr_repeats.csv", repeats)
    write_csv(a.output / "sr_recovery_summary.csv", repeat_summary)
    (a.output / "tables").mkdir(exist_ok=True)
    sr_lines = []
    for summary in repeat_summary:
        cells = [LABELS[summary["condition"]]]
        for row in (r for r in repeats if r["condition"] == summary["condition"]):
            cell = f"{row['rwp']:.2f}"
            if row["sr2wo5"]:
                cell = r"\textbf{" + cell + "}"
            if row["replacement_for"] is not None:
                cell += r"\(^{\dagger}\)"
            cells.append(cell)
        cells.append(f"{summary['recovered']}/9")
        sr_lines.append(" & ".join(cells) + r" \\")
    (a.output / "tables/sr_repeats_rows.tex").write_text("\n".join(sr_lines) + "\n")
    evolution = []
    for name in ["divalent-tungstates", "divalent-tungstates-fw", "divalent-tungstates-access"]:
        status = load(ROOT / "results/experimental-evolution" / name / "evidence/status.json")
        for job in status["jobs"]:
            evolution.append(
                dict(
                    campaign=name,
                    id=job["id"],
                    case=job["case_id"],
                    package=job["policy"],
                    status=job["status"],
                    score=job.get("score_100"),
                    score_interval=json.dumps(job.get("score_interval")),
                    incumbent=status["current_package"],
                )
            )
    write_csv(a.output / "synthetic_attempts.csv", evolution)
    assert len(evolution) == 135 + 36 + 156
    validate_plot_inputs(panels)
    if a.figures:
        (a.output / "figures").mkdir(exist_ok=True)
        (a.output / "tables").mkdir(exist_ok=True)
        for script in sorted((Path(__file__).parent / "paper_figures").glob("plot_*.py")):
            subprocess.run(
                [sys.executable, str(script)],
                check=True,
                cwd=ROOT,
                env={**os.environ, "PXRD_RELEASE_OUTPUT": str(a.output)},
            )
    report = dict(
        initial_attempts=len(all_rows),
        synthetic_job_records=len(evolution),
        sr_displayed_attempts=len(repeats),
        status="passed",
        aggregates=aggregates,
    )
    (a.output / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
