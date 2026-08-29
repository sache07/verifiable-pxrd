from pathlib import Path

from pymatgen.core import Lattice, Structure

from verifiable_pxrd.matching import evaluate_selected, evaluate_workspace, exact_outcomes


def write_structure(path: Path, species: list[str], coordinates: list[list[float]]) -> None:
    Structure(Lattice.cubic(4), species, coordinates).to(filename=str(path), fmt="cif")


def test_exact_alternative_is_candidate_recovery_not_selected_recovery(tmp_path: Path) -> None:
    reference = tmp_path / "reference.cif"
    write_structure(reference, ["Na", "Cl"], [[0, 0, 0], [0.5, 0.5, 0.5]])
    write_structure(tmp_path / "selected.cif", ["Na", "F"], [[0, 0, 0], [0.5, 0.5, 0.5]])
    write_structure(tmp_path / "alternative-1.cif", ["Na", "Cl"], [[0, 0, 0], [0.5, 0.5, 0.5]])
    result = evaluate_workspace(reference, tmp_path, "test")
    assert result["selected_exact"] is False
    assert result["candidates_exact"] is True
    assert result["metrics"]["matched_candidates"] == ["alternative-1.cif"]
    selected = evaluate_selected(reference, tmp_path, "test")
    assert selected["selected_exact"] is False
    assert selected["candidates_exact"] is False


def test_exact_selected_counts_as_both_outcomes(tmp_path: Path) -> None:
    reference = tmp_path / "reference.cif"
    write_structure(reference, ["Na", "Cl"], [[0, 0, 0], [0.5, 0.5, 0.5]])
    write_structure(tmp_path / "selected.cif", ["Na", "Cl"], [[0, 0, 0], [0.5, 0.5, 0.5]])
    result = evaluate_workspace(reference, tmp_path, "test")
    assert result["selected_exact"] is True
    assert result["candidates_exact"] is True


def test_wrong_species_does_not_match(tmp_path: Path) -> None:
    reference = tmp_path / "reference.cif"
    write_structure(reference, ["Na", "Cl"], [[0, 0, 0], [0.5, 0.5, 0.5]])
    write_structure(tmp_path / "selected.cif", ["K", "Cl"], [[0, 0, 0], [0.5, 0.5, 0.5]])
    result = evaluate_workspace(reference, tmp_path, "test")
    assert result["selected_exact"] is False
    assert result["candidates_exact"] is False


def test_stored_candidate_result_recovers_both_outcomes() -> None:
    assert exact_outcomes(
        {"exact_success": True, "metrics": {"matched_candidates": ["alternative-1.cif"]}}
    ) == (False, True)
    assert exact_outcomes({"exact_success": True}) == (True, True)
