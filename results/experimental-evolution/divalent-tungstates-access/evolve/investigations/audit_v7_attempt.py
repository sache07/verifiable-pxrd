#!/usr/bin/env python3
"""Summarize v7 five-pass polish use and final scorer consistency."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


EXPECTED_HELPER_SHA256 = "954ecebf0bbb6445cdac938860abb83f8c0c55ba4789fcdd9c87af0a8349d6fe"
EVIDENCE = Path(__file__).resolve().parents[2] / "evidence" / "attempts"


def load(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def last_stage(branch: dict) -> dict:
    stages = branch.get("stages") or []
    return stages[-1] if stages else {}


def audit(attempt_id: str) -> dict:
    root = EVIDENCE / attempt_id
    workspace = root / "workspace"
    collection = load(root / "collection.json")
    score = load(root / "score.json")
    result = load(workspace / "result.json")

    helper_paths = sorted(workspace.rglob("staged_polish.py"))
    helper_hashes = {str(path.relative_to(workspace)): sha256(path) for path in helper_paths}
    audit_paths = sorted(workspace.rglob("*.staged_polish.json"))
    polish_audits = []
    for path in audit_paths:
        record = load(path)
        branches = record.get("branches") or []
        baseline = next((item for item in branches if item.get("name") == "baseline"), {})
        selected = record.get("selected") or {}
        selected_branch = next(
            (item for item in branches if item.get("name") == selected.get("name")), {}
        )
        final_stage = last_stage(selected_branch)
        polish_audits.append(
            {
                "path": str(path.relative_to(workspace)),
                "baseline_Rwp_percent": baseline.get("Rwp_percent"),
                "selected": selected,
                "selected_eligible": selected_branch.get("eligible"),
                "selected_violations": selected_branch.get("violations"),
                "selected_fractions": selected_branch.get("fractions"),
                "final_stage": {
                    "stage": final_stage.get("stage"),
                    "converged": final_stage.get("converged"),
                    "max_shift_esd": final_stage.get("max_shift_esd"),
                    "frozen": final_stage.get("frozen"),
                },
                "eligible_branches": [
                    item.get("name") for item in branches if item.get("eligible")
                ],
            }
        )

    result_rwp = (result.get("fit_statistics") or {}).get("Rwp_percent")
    selected_rwp = None
    baseline_rwp = None
    if polish_audits:
        selected_rwp = (polish_audits[-1].get("selected") or {}).get("Rwp_percent")
        baseline_rwp = polish_audits[-1].get("baseline_Rwp_percent")

    final_path = workspace / "final.gpx"
    final_hash = sha256(final_path)
    artifact_hashes = load(root / "artifact_hashes.json")
    collected_hash = artifact_hashes.get("final.gpx")
    fingerprint_values = [
        value
        for key, value in (score.get("submission_fingerprints") or {}).items()
        if key.endswith("/final.gpx")
    ]

    text_hits = []
    for relative in ("report.md", "run/final-answer.md", "run/messages.log"):
        path = root / relative if relative.startswith("run/") else workspace / relative
        if not path.exists():
            continue
        for number, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
            if "staged_polish" in line or "staged polish" in line.lower():
                text_hits.append(f"{relative}:{number}:{line.strip()[:300]}")

    strict = score.get("strict_diagnostics") or {}
    recovered = bool(
        score.get("physical_validity") == "pass"
        and strict.get("full_framework_inventory")
        and strict.get("phase_f1") == 1.0
        and strict.get("quantification_complete")
        and score.get("D_poisson") is not None
        and score["D_poisson"] <= 1.0
    )
    at_floor = bool(recovered and score["D_poisson"] <= 0.1)
    result_fractions = {
        phase.get("project_phase_name") or phase.get("name"): phase.get("weight_fraction")
        for phase in result.get("phases") or []
    }

    return {
        "attempt": attempt_id,
        "job": collection.get("job"),
        "score": {
            "score_100": score.get("score_100"),
            "provisional": score.get("score_100_is_provisional"),
            "D_poisson": score.get("D_poisson"),
            "independent_atomic_rwp": score.get("independent_atomic_rwp"),
            "physical_validity": score.get("physical_validity"),
            "profile_status": score.get("profile_status"),
            "full_framework_inventory": strict.get("full_framework_inventory"),
            "max_fraction_error": strict.get("max_matched_fraction_error"),
            "recovered": recovered,
            "at_floor": at_floor,
            "site_accuracies": [
                assignment.get("site_accuracy")
                for assignment in (score.get("structural_components") or {}).get("assignment", [])
            ],
        },
        "helper": {
            "paths_and_hashes": helper_hashes,
            "expected_hash": EXPECTED_HELPER_SHA256,
            "hash_ok": bool(helper_hashes)
            and all(value == EXPECTED_HELPER_SHA256 for value in helper_hashes.values()),
            "audit_count": len(polish_audits),
            "single_invocation": len(polish_audits) == 1,
            "invocation_text_hits": text_hits,
            "audits": polish_audits,
        },
        "final_export": {
            "result_Rwp_percent": result_rwp,
            "selected_Rwp_percent": selected_rwp,
            "baseline_Rwp_percent": baseline_rwp,
            "result_matches_selected_Rwp": selected_rwp is not None
            and result_rwp is not None
            and abs(selected_rwp - result_rwp) <= 1e-4,
            "result_fractions": result_fractions,
            "final_gpx_sha256": final_hash,
            "collected_sha256": collected_hash,
            "scorer_fingerprints": fingerprint_values,
            "hashes_consistent": collected_hash == final_hash
            and bool(fingerprint_values)
            and all(value == final_hash for value in fingerprint_values),
        },
        "physical_flags": [
            audit
            for audit in score.get("physical_audit") or []
            if audit.get("status") != "pass" or audit.get("flagged_contact_count")
        ],
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} ATTEMPT_ID")
    print(json.dumps(audit(sys.argv[1]), indent=2, sort_keys=True))
