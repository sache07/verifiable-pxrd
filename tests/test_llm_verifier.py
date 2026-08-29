import json
from pathlib import Path

import pytest

from verifiable_pxrd.benchmark import Problem
from verifiable_pxrd.llm_verifier import (
    decision_metrics,
    render_review_prompt,
    validate_decision,
)
from verifiable_pxrd.util import sha256_file

ROOT = Path(__file__).resolve().parents[1]


def test_review_prompt_renders_blind_evidence_paths(tmp_path: Path) -> None:
    problem = Problem(
        problem_id="case",
        formula="NaCl",
        pattern=tmp_path / "pattern.csv",
        reference=tmp_path / "reference.cif",
        record=tmp_path / "problem.json",
    )
    evidence = tmp_path / "evidence"
    candidate = evidence / "selected.cif"
    prompt = render_review_prompt(
        "{formula}\n{pattern_path}\n{submitted_cifs}\n{judge_policy}\n{rwp_report_path}",
        "Audit it.",
        problem,
        evidence,
        (candidate,),
    )

    assert "NaCl" in prompt
    assert str(candidate) in prompt
    assert "Audit it." in prompt
    assert "reference.cif" not in prompt


def test_decision_contract(tmp_path: Path) -> None:
    path = tmp_path / "decision.json"
    path.write_text(
        json.dumps({"decision": "continue", "reason": "unresolved coordinates"}),
        encoding="utf-8",
    )
    assert validate_decision(path)["decision"] == "continue"

    path.write_text(
        json.dumps({"decision": "stop", "reason": "done", "proposed_branch": "P1"}),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="must be null"):
        validate_decision(path)


def test_asymmetric_decision_metrics() -> None:
    metrics = decision_metrics(
        [
            {"decision": "continue", "oracle_decision": "continue"},
            {"decision": "stop", "oracle_decision": "stop"},
            {"decision": "continue", "oracle_decision": "stop"},
            {"decision": "stop", "oracle_decision": "continue"},
        ]
    )
    assert metrics["accuracy"] == 0.5
    assert metrics["false_stop_rate"] == 0.5
    assert metrics["continuation_rate"] == 0.5


def test_frozen_judge_artifact_matches_manifest() -> None:
    root = ROOT / "experiments/inference-scaling/llm-verifier/judge-v1"
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    for name, expected in manifest["files"].items():
        assert sha256_file(root / name) == expected
    gepa = ROOT / "experiments/inference-scaling/llm-verifier/gepa"
    provenance = manifest["provenance"]
    assert sha256_file(gepa / "data/examples.jsonl") == provenance["examples_sha256"]
    assert sha256_file(gepa / "data/splits.json") == provenance["splits_sha256"]
    assert sha256_file(gepa / "provenance/result.json") == provenance["optimizer_result_sha256"]
    assert sha256_file(gepa / "provenance/finalist-summary.json") == provenance[
        "finalist_summary_sha256"
    ]
    assert (root / "policy.md").read_bytes() == (
        gepa / "provenance/candidate-policies/candidate-003.md"
    ).read_bytes()
