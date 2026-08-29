from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from verifiable_pxrd.baselines.candidates import materialize_case_candidates


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def synthetic_run(tmp_path: Path) -> Path:
    run = tmp_path / "example-run"
    shard = run / "shard-000"
    source = shard / "candidates" / "case-001"
    source.mkdir(parents=True)
    valid = b"data_example\n_cell_length_a 1\n"
    invalid = b"not a parseable cif\n"
    (source / "candidate-01.cif").write_bytes(valid)
    (source / "candidate-02.raw.cif").write_bytes(invalid)
    (shard / "results.json").write_text(
        json.dumps(
            {
                "candidates": [
                    {
                        "case_id": "case-001",
                        "sample_index": 0,
                        "status": "generated",
                        "candidate_path": "candidates/case-001/candidate-01.cif",
                        "candidate_sha256": digest(valid),
                    },
                    {
                        "case_id": "case-001",
                        "sample_index": 1,
                        "status": "invalid",
                        "candidate_path": "candidates/case-001/candidate-02.raw.cif",
                        "candidate_sha256": digest(invalid),
                    },
                ]
            }
        ),
        encoding="utf-8",
    )
    return run


def verifier_rows() -> list[dict[str, object]]:
    return [
        {
            "case_id": "case-001",
            "sample_index": 0,
            "status": "generated",
            "target_formula": "Si",
            "predicted_formula": "Si",
            "formula_match": True,
            "structure_valid": True,
            "structure_match": True,
            "matcher_rms": 0.01,
            "matcher_max_dist": 0.02,
        },
        {
            "case_id": "case-001",
            "sample_index": 1,
            "status": "invalid",
            "target_formula": "Si",
            "predicted_formula": None,
            "formula_match": False,
            "structure_valid": False,
            "structure_match": False,
            "evaluation_error": "invalid CIF",
        },
    ]


def test_materializes_case_first_cifs_and_verifier_results(tmp_path: Path) -> None:
    run = synthetic_run(tmp_path)
    summary = materialize_case_candidates(
        run,
        verifier_rows=verifier_rows(),
        verifier_metadata={"structure_matcher": {"ltol": 0.2}},
    )

    root = run / "candidates"
    assert summary["candidate_record_count"] == 2
    assert summary["candidate_cif_count"] == 1
    assert summary["verifier_result_file_count"] == 1
    assert (root / "case-001" / "candidate-01.cif").is_file()
    assert not (root / "case-001" / "candidate-02.raw.cif").exists()
    verifier = json.loads((root / "case-001" / "verifier-results.json").read_text())
    assert verifier["verifier"]["structure_matcher"]["ltol"] == 0.2
    assert verifier["candidates"][0]["structure_match"] is True
    assert verifier["candidates"][1]["evaluation_error"] == "invalid CIF"

    repeated = materialize_case_candidates(
        run,
        verifier_rows=verifier_rows(),
        verifier_metadata={"structure_matcher": {"ltol": 0.2}},
    )
    assert repeated["manifest_sha256"] == summary["manifest_sha256"]


def test_can_publish_verifier_results_without_cifs(tmp_path: Path) -> None:
    run = synthetic_run(tmp_path)
    output = tmp_path / "withheld"
    summary = materialize_case_candidates(
        run,
        output,
        verifier_rows=verifier_rows(),
        publish_cifs=False,
    )

    assert summary["candidate_cif_count"] == 0
    assert (output / "case-001" / "verifier-results.json").is_file()
    assert not list(output.rglob("*.cif"))


def test_auto_detects_evaluation_from_input_run(tmp_path: Path) -> None:
    run = synthetic_run(tmp_path)
    (run / "evaluation-candidates.csv").write_text(
        "case_id,sample_index,status,target_formula,predicted_formula,formula_match,"
        "structure_valid,structure_match,evaluation_error\n"
        "case-001,0,generated,Si,Si,true,true,true,\n"
        "case-001,1,invalid,Si,,false,false,false,invalid CIF\n",
        encoding="utf-8",
    )
    (run / "evaluation.json").write_text(
        json.dumps({"metric": {"structure_matcher": {"ltol": 0.2}}}),
        encoding="utf-8",
    )

    summary = materialize_case_candidates(run)
    verifier = json.loads(
        (run / "candidates" / "case-001" / "verifier-results.json").read_text()
    )
    assert summary["verifier_result_file_count"] == 1
    assert verifier["verifier"]["structure_matcher"]["ltol"] == 0.2


def test_rejects_incomplete_verifier_results(tmp_path: Path) -> None:
    run = synthetic_run(tmp_path)
    with pytest.raises(RuntimeError, match="verifier/candidate key mismatch"):
        materialize_case_candidates(run, verifier_rows=verifier_rows()[:1])
