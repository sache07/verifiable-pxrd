from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from pymatgen.core import Lattice, Structure
from pymatgen.io.cif import CifWriter

from verifiable_pxrd import rwp_verifier


def _write_pattern(path: Path) -> None:
    x = np.linspace(5.0, 30.0, 501)
    y = 100.0 * np.exp(-0.5 * np.square((x - 15.0) / 0.08))
    np.savetxt(path, np.column_stack((x, y)), delimiter=",", header="two_theta,intensity", comments="")


def _write_cif(path: Path, lattice_scale: float) -> None:
    structure = Structure(
        Lattice.cubic(lattice_scale),
        ["Na", "Cl"],
        [[0.0, 0.0, 0.0], [0.5, 0.5, 0.5]],
    )
    path.write_text(str(CifWriter(structure)), encoding="utf-8")


def test_estimate_profile_uses_observed_widths() -> None:
    x = np.linspace(5.0, 80.0, 7501)
    y = sum(
        100.0 * np.exp(-0.5 * np.square((x - center) / 0.04))
        for center in (12.0, 24.0, 38.0, 55.0, 70.0)
    )

    result = rwp_verifier.estimate_profile(x, y)

    assert result["method"] == "observed-peak-width regression"
    assert result["peak_count_used"] == 5
    assert result["w"] > 0
    assert result["u"] > 0


def test_score_case_ranks_and_materializes_selected(tmp_path: Path, monkeypatch) -> None:
    pattern = tmp_path / "pattern.csv"
    _write_pattern(pattern)
    worse = tmp_path / "worse.cif"
    better = tmp_path / "better.cif"
    _write_cif(worse, 5.8)
    _write_cif(better, 5.6)

    def fake_fit(candidate: Path, *_args, **_kwargs):
        return {
            "candidate": str(candidate),
            "sha256": rwp_verifier.sha256_file(candidate),
            "status": "completed",
            "rwp_percent": 3.0 if candidate.name == "better.cif" else 7.0,
            "frozen_structure": True,
        }

    monkeypatch.setattr(rwp_verifier, "_fit_candidate", fake_fit)
    output = tmp_path / "result"

    report = rwp_verifier.score_case(
        pattern,
        1.5406,
        [worse, better],
        output,
        gsas_python=Path(sys.executable),
        parallel=2,
    )

    assert report["valid"] is True
    assert report["selected"]["candidate"] == str(better)
    assert (output / "submission/selected.cif").read_bytes() == better.read_bytes()
    assert (output / "scores.csv").is_file()


def test_source_candidates_understands_normalized_bundle(tmp_path: Path) -> None:
    source = tmp_path / "replicate-01"
    submission = source / "attempts/vh-001/submission"
    submission.mkdir(parents=True)
    _write_cif(submission / "selected.cif", 5.6)
    (source / "bundle.json").write_text(
        json.dumps(
            {
                "cases": [
                    {
                        "case_id": "vh-001",
                        "source_attempt_name": "001-vh-001-source-name",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    found = rwp_verifier._source_candidates(source)

    assert [path.name for path in found["vh-001"]] == ["selected.cif"]


def test_expand_sources_accepts_campaign_root(tmp_path: Path) -> None:
    campaign = tmp_path / "campaign"
    for number in (1, 2):
        replicate = campaign / f"replicate-{number:02d}"
        replicate.mkdir(parents=True)
        (replicate / "bundle.json").write_text("{}", encoding="utf-8")

    assert rwp_verifier._expand_sources([campaign]) == [
        campaign / "replicate-01",
        campaign / "replicate-02",
    ]


def test_wavelength_is_read_from_public_problem_prompt(tmp_path: Path) -> None:
    problem = tmp_path / "vh-001"
    prompt = problem / "problem_input/prompt.md"
    prompt.parent.mkdir(parents=True)
    prompt.write_text("Measured with monochromatic radiation at 1.5406 angstrom.", encoding="utf-8")

    assert rwp_verifier._wavelength(problem, None) == 1.5406
