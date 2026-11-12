"""Shared primary exact-recovery metric for the pXRD benchmarks."""

from __future__ import annotations

import math
from typing import Any

from pymatgen.analysis.structure_matcher import ElementComparator, StructureMatcher
from pymatgen.core import Composition, Structure

PRIMARY_MATCHER_PARAMETERS: dict[str, Any] = {
    "ltol": 0.2,
    "stol": 0.3,
    "angle_tol": 5,
    "primitive_cell": True,
    "scale": False,
    "attempt_supercell": True,
    "allow_subset": False,
}
LEGACY_LOOSE_ML_MATCHER_PARAMETERS: dict[str, Any] = {
    "ltol": 0.3,
    "stol": 0.5,
    "angle_tol": 10,
    "primitive_cell": True,
    "scale": True,
    "attempt_supercell": False,
    "allow_subset": False,
}
FORMULA_RTOL = 1e-5
FORMULA_ATOL = 1e-8


def primary_matcher() -> StructureMatcher:
    """Build the benchmark's element-aware, exact-cell StructureMatcher."""

    return StructureMatcher(
        **PRIMARY_MATCHER_PARAMETERS,
        comparator=ElementComparator(),
    )


def legacy_loose_ml_matcher() -> StructureMatcher:
    """Build the loose matcher convention used by common crystal-ML reports."""

    return StructureMatcher(**LEGACY_LOOSE_ML_MATCHER_PARAMETERS)


def _composition(value: Composition | Structure) -> Composition:
    return value.composition if isinstance(value, Structure) else value


def element_composition_match(
    left: Composition | Structure,
    right: Composition | Structure,
    *,
    reduced: bool = True,
) -> bool:
    """Compare elemental stoichiometry while ignoring oxidation annotations.

    CIF serialization can introduce insignificant floating-point occupancy noise,
    so the comparison is tolerant rather than exact. Reduced comparison accepts
    crystallographically equivalent primitive, conventional, and supercell counts.
    """

    left_elemental = _composition(left).element_composition
    right_elemental = _composition(right).element_composition
    if reduced:
        left_elemental = left_elemental.fractional_composition
        right_elemental = right_elemental.fractional_composition
    return bool(
        left_elemental.almost_equals(
            right_elemental,
            rtol=FORMULA_RTOL,
            atol=FORMULA_ATOL,
        )
    )


def primary_structure_match(
    predicted: Structure,
    target: Structure,
    matcher: StructureMatcher | None = None,
) -> tuple[bool, tuple[float, float] | None]:
    """Return the symmetric Boolean fit and normalized displacement diagnostics."""

    # With scale=False, any accepted lattice mapping must preserve volume per
    # site up to the length tolerance.  This necessary (but deliberately not
    # sufficient) bound avoids pathological lattice-enumeration blowups for
    # obviously impossible cells while leaving StructureMatcher as the scoring
    # predicate for every feasible pair.
    left_vps = predicted.volume / len(predicted)
    right_vps = target.volume / len(target)
    left_shape = predicted.volume / math.prod(predicted.lattice.abc)
    right_shape = target.volume / math.prod(target.lattice.abc)
    length_volume_factor = (1 + float(PRIMARY_MATCHER_PARAMETERS["ltol"])) ** 3
    ratio = left_vps / right_vps
    if (
        not all(
            math.isfinite(value) and value > 0
            for value in (left_vps, right_vps, left_shape, right_shape, ratio)
        )
        or ratio > length_volume_factor / right_shape
        or 1 / ratio > length_volume_factor / left_shape
    ):
        return False, None

    active = matcher or primary_matcher()
    matched = bool(active.fit(predicted, target, symmetric=True))
    if not matched:
        return False, None
    distances = active.get_rms_dist(predicted, target)
    if distances is None:
        raise RuntimeError("StructureMatcher.fit succeeded without an RMS mapping")
    return True, (float(distances[0]), float(distances[1]))


def legacy_loose_ml_structure_match(
    predicted: Structure,
    target: Structure,
    matcher: StructureMatcher | None = None,
) -> tuple[bool, tuple[float, float] | None]:
    """Return the legacy loose ML Boolean fit and optional RMS diagnostics.

    This intentionally uses Pymatgen's default directional ``fit`` behavior to
    mirror the widespread PXRDGen/DiffCSP-style matcher construction. It remains
    a secondary literature-comparison metric, not the benchmark's primary score.
    """

    active = matcher or legacy_loose_ml_matcher()
    matched = bool(active.fit(predicted, target))
    if not matched:
        return False, None
    distances = active.get_rms_dist(predicted, target)
    if distances is None:
        raise RuntimeError("legacy loose StructureMatcher.fit succeeded without an RMS mapping")
    return True, (float(distances[0]), float(distances[1]))


def primary_metric_metadata() -> dict[str, Any]:
    """Return a JSON-serializable description of the primary metric."""

    return {
        **PRIMARY_MATCHER_PARAMETERS,
        "comparator": "ElementComparator",
        "symmetric": True,
        "boolean_predicate": "StructureMatcher.fit",
        "lattice_feasibility_prefilter": (
            "symmetric volume-per-site bound implied by ltol with scale=False"
        ),
        "rms_units": "normalized by (volume / site count) ** (1/3)",
    }


def formula_metric_metadata() -> dict[str, Any]:
    return {
        "basis": "reduced elemental composition",
        "oxidation_states": "ignored",
        "relative_tolerance": FORMULA_RTOL,
        "absolute_tolerance": FORMULA_ATOL,
    }


def legacy_loose_ml_metric_metadata() -> dict[str, Any]:
    return {
        **LEGACY_LOOSE_ML_MATCHER_PARAMETERS,
        "comparator": "SpeciesComparator (Pymatgen default)",
        "symmetric": False,
        "boolean_predicate": "StructureMatcher.fit",
        "label": "legacy loose ML match",
        "purpose": "PXRDGen/DiffCSP literature comparison only",
        "rms_units": "normalized by (volume / site count) ** (1/3)",
    }
