from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
RUNNER_PATH = REPOSITORY_ROOT / "baselines" / "ab-pxrd-solver" / "run_cpu.py"
SPEC = importlib.util.spec_from_file_location("ab_pxrd_solver_cpu", RUNNER_PATH)
assert SPEC is not None and SPEC.loader is not None
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


@pytest.mark.parametrize(
    ("formula", "expected"),
    [
        ("Na2ScIn(SiO3)4", "Na2ScInSi4O12"),
        ("LiBi(BO3)2", "LiBiB2O6"),
        ("KMg3AlGe3(O5F)2", "KMg3AlGe3O10F2"),
        ("AlBi2Se2BrCl4", "AlBi2Se2BrCl4"),
    ],
)
def test_formula_serialization(formula: str, expected: str) -> None:
    assert RUNNER.expanded_integer_formula(formula) == expected


@pytest.mark.parametrize("formula", ["Li(BO3", "Li0.5O", "Li+O"])
def test_formula_serialization_rejects_unsupported(formula: str) -> None:
    with pytest.raises(ValueError):
        RUNNER.expanded_integer_formula(formula)
