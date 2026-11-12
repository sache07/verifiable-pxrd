#!/usr/bin/env python3
"""Assess the prospective five-pass procedure-test criteria."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2] / "evidence" / "procedure-tests"
OLD = ROOT / "ptest-v6-staged-covfix-02" / "results.json"
NEW = ROOT / "ptest-v7-morepasses-04" / "results.json"
TARGET = "b001-v6-a8e159045358"
CORE = {
    "b003-v4-v5-a02e30914a71",
    "b003-v4-v5-92b88601b429",
    "b003-v4-v5-856dde72f4da",
    "b003-v4-v5-ad16ddf37d6f",
    "b002-v4-v5-99637c5841ce",
    "b002-v4-v5-8bda9314cb4f",
    "b001-v4-v5-b9e3a697c8a5",
    "b001-v4-v5-a49a4302f681",
}


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


old = load(OLD)
new = load(NEW)
old_by_id = {item["attempt"]: item for item in old["attempts"]}
new_by_id = {item["attempt"]: item for item in new["attempts"]}

rows = []
for attempt, item in new_by_id.items():
    after = item.get("after") or {}
    phases = after.get("phases") or []
    rows.append(
        {
            "attempt": attempt,
            "case": item.get("case_id"),
            "status": item.get("status"),
            "D_before": (item.get("before") or {}).get("D_poisson"),
            "D_after": after.get("D_poisson"),
            "delta_D": item.get("delta_D"),
            "profile_flags": after.get("profile_review_flags") or [],
            "phase_screens": [phase.get("physical_screen") for phase in phases],
        }
    )

all_scored = len(rows) == 18 and all(row["status"] == "scored" for row in rows)
all_physical = all(
    not row["profile_flags"]
    and all(status == "pass" for status in row["phase_screens"])
    for row in rows
)
no_worse = all(
    row["delta_D"] is not None and row["delta_D"] <= 0.10 for row in rows
)
core_retained = {
    attempt: new_by_id[attempt]["delta_D"]
    <= old_by_id[attempt]["delta_D"] + 0.05
    for attempt in sorted(CORE)
}
target_after = (new_by_id.get(TARGET, {}).get("after") or {}).get("D_poisson")

assessment = {
    "test": new.get("id"),
    "script_sha256": new.get("script_sha256"),
    "summary": new.get("summary"),
    "criteria": {
        "all_18_scored": all_scored,
        "all_outputs_physical": all_physical,
        "no_D_worsening_over_0.10": no_worse,
        "all_core_results_retained_within_0.05_D": all(core_retained.values()),
        "core_retention": core_retained,
        "c03_rep3_D_after": target_after,
        "c03_rep3_recovered_D_le_1": target_after is not None and target_after <= 1.0,
    },
    "rows": rows,
}
print(json.dumps(assessment, indent=2, sort_keys=True))
