from __future__ import annotations

from pymatgen.analysis.structure_matcher import StructureMatcher
from pymatgen.core import Composition, Lattice, Species, Structure

from verifiable_pxrd.baselines.matching import (
    element_composition_match,
    legacy_loose_ml_metric_metadata,
    legacy_loose_ml_structure_match,
    primary_metric_metadata,
    primary_structure_match,
)


def _rocksalt(lattice_constant: float = 4.0) -> Structure:
    return Structure(
        Lattice.cubic(lattice_constant),
        ["Na", "Cl"],
        [[0, 0, 0], [0.5, 0.5, 0.5]],
    )


def test_formula_match_ignores_oxidation_annotations() -> None:
    annotated = Composition({Species("Fe", 2): 2, Species("O", -2): 3})
    assert element_composition_match(annotated, Composition("Fe2O3"))


def test_primary_match_rejects_uniform_lattice_rescaling() -> None:
    target = _rocksalt(4.0)
    rescaled = _rocksalt(6.0)
    loose = StructureMatcher(
        ltol=0.3,
        stol=0.5,
        angle_tol=10,
        primitive_cell=True,
        scale=True,
        attempt_supercell=False,
    )
    assert loose.fit(target, rescaled)
    assert primary_structure_match(target, rescaled) == (False, None)
    assert legacy_loose_ml_structure_match(target, rescaled)[0]


def test_primary_match_accepts_commensurate_supercells_symmetrically() -> None:
    primitive = _rocksalt()
    supercell = primitive.copy()
    supercell.make_supercell([2, 1, 1])
    assert primary_structure_match(primitive, supercell)[0]
    assert primary_structure_match(supercell, primitive)[0]


def test_metric_metadata_records_primary_and_secondary_policies() -> None:
    primary = primary_metric_metadata()
    assert primary["scale"] is False
    assert primary["attempt_supercell"] is True
    assert primary["symmetric"] is True
    secondary = legacy_loose_ml_metric_metadata()
    assert secondary["label"] == "legacy loose ML match"
    assert secondary["scale"] is True
    assert secondary["symmetric"] is False
