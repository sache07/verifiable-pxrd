from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from verifiable_pxrd.baselines import runner

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
CORE_PATH = REPOSITORY_ROOT / "baselines" / "realpxrd-solver" / "core.py"
SPEC = importlib.util.spec_from_file_location("realpxrd_solver_core", CORE_PATH)
assert SPEC is not None and SPEC.loader is not None
CORE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CORE)


def _case() -> dict[str, object]:
    return {
        "case_id": "example-001",
        "primitive_cell_composition": {"Na": 2, "Cl": 2},
        "primitive_cell_formula": "Na2Cl2",
        "primitive_cell_atom_count": 4,
        "primitive_cell_lattice_matrix_angstrom": [
            [3.0, 0.0, 0.0],
            [0.0, 4.0, 0.0],
            [0.0, 0.0, 5.0],
        ],
        "reduced_composition": {"Na": 1, "Cl": 1},
        "reduced_formula_explicit": "Na1Cl1",
        "reduced_formula_atom_count": 2,
    }


def test_input_modes_are_explicit() -> None:
    assert CORE.DEFAULT_INPUT_MODE == CORE.LATTICE_FREE_ORACLE
    assert CORE.model_directory(CORE.LATTICE_FREE_ORACLE) == "pxrd-all"
    assert CORE.model_directory(CORE.LATTICE_CONDITIONED_ORACLE) == "pxrd-all-L"
    with pytest.raises(ValueError, match="unknown RealPXRD-Solver input mode"):
        CORE.model_directory("automatic")


def test_case_input_keeps_oracle_and_reduced_modes_separate() -> None:
    oracle = CORE.case_input(_case(), CORE.LATTICE_FREE_ORACLE)
    reduced = CORE.case_input(_case(), CORE.LATTICE_FREE_REDUCED)
    assert (oracle["formula"], oracle["atom_count"], oracle["oracle_input"]) == ("Na2Cl2", 4, True)
    assert (reduced["formula"], reduced["atom_count"], reduced["oracle_input"]) == (
        "Na1Cl1",
        2,
        False,
    )


def test_peak_filter_is_strict_and_preserves_order(tmp_path: Path) -> None:
    path = tmp_path / "peaks.xy"
    np.savetxt(path, np.asarray([[10.1, 5.0], [20.2, 5.01], [30.3, 100.0]]))
    np.testing.assert_allclose(CORE.load_model_peaks(path), [[20.2, 5.01], [30.3, 100.0]])


def test_artifact_lock_selects_two_general_models() -> None:
    lock_path = REPOSITORY_ROOT / "baselines" / "realpxrd-solver" / "artifacts.lock.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    checkpoints = [row for row in lock["artifacts"] if row["path"].endswith(".ckpt")]
    assert {row["path"] for row in checkpoints} == {
        "pxrd-all/last_one.ckpt",
        "pxrd-all-L/last_one.ckpt",
    }


def test_common_runner_passes_realpxrd_input_mode() -> None:
    adapter = SimpleNamespace(
        DEFAULT_INPUT_MODE=CORE.LATTICE_FREE_ORACLE,
        make_requests=lambda **kwargs: [kwargs],
    )
    requests = runner.production_requests(
        adapter,
        framework="realpxrd-solver",
        run_id="test-run",
        shard_size=10,
        seed_base=7,
        composition_mode="reduced",
        input_mode=CORE.LATTICE_CONDITIONED_ORACLE,
    )
    assert requests[0]["input_mode"] == CORE.LATTICE_CONDITIONED_ORACLE
