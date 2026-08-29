"""Small, testable helpers for the RealPXRD-Solver benchmark adapter."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import numpy as np
from pymatgen.core import Element, Lattice, Structure

LATTICE_FREE_ORACLE = "lattice-free-primitive-formula-oracle"
LATTICE_CONDITIONED_ORACLE = "lattice-conditioned-primitive-cell-oracle"
LATTICE_FREE_REDUCED = "lattice-free-reduced-formula"
INPUT_MODES = (LATTICE_FREE_ORACLE, LATTICE_CONDITIONED_ORACLE, LATTICE_FREE_REDUCED)
DEFAULT_INPUT_MODE = LATTICE_FREE_ORACLE


def model_directory(input_mode: str) -> str:
    if input_mode not in INPUT_MODES:
        raise ValueError(f"unknown RealPXRD-Solver input mode: {input_mode}")
    return "pxrd-all-L" if input_mode == LATTICE_CONDITIONED_ORACLE else "pxrd-all"


def case_input(case: dict[str, Any], input_mode: str) -> dict[str, Any]:
    model_directory(input_mode)
    reduced = input_mode == LATTICE_FREE_REDUCED
    composition_key = "reduced_composition" if reduced else "primitive_cell_composition"
    formula_key = "reduced_formula_explicit" if reduced else "primitive_cell_formula"
    count_key = "reduced_formula_atom_count" if reduced else "primitive_cell_atom_count"
    composition = {str(key): int(value) for key, value in case[composition_key].items()}
    atom_types: list[int] = []
    for symbol, count in composition.items():
        if count <= 0:
            raise ValueError(f"{case['case_id']}: non-positive count for {symbol}")
        atom_types.extend([int(Element(symbol).Z)] * count)
    if len(atom_types) != int(case[count_key]):
        raise RuntimeError(f"{case['case_id']}: formula count does not match target manifest")
    lattice = None
    if input_mode == LATTICE_CONDITIONED_ORACLE:
        lattice = np.asarray(case["primitive_cell_lattice_matrix_angstrom"], dtype=np.float64)
        if lattice.shape != (3, 3) or not np.isfinite(lattice).all():
            raise RuntimeError(f"{case['case_id']}: invalid primitive lattice")
    return {
        "formula": str(case[formula_key]),
        "atom_types": atom_types,
        "atom_count": len(atom_types),
        "lattice_matrix": lattice,
        "oracle_input": not reduced,
        "input_mode": input_mode,
    }


def load_model_peaks(path: Path, *, threshold: float = 5.0) -> np.ndarray:
    values = np.loadtxt(path, dtype=np.float64).reshape(-1, 2)
    if not np.isfinite(values).all():
        raise ValueError(f"non-finite RealPXRD-Solver peak target: {path}")
    retained = values[values[:, 1] > threshold]
    if not len(retained):
        raise ValueError(f"no peaks survive RealPXRD-Solver's >{threshold:g} rule: {path}")
    return retained


def lattice_parameters(matrix: np.ndarray) -> tuple[list[float], list[float]]:
    lattice = np.asarray(matrix, dtype=np.float64)
    if lattice.shape != (3, 3) or not np.isfinite(lattice).all():
        raise ValueError("predicted lattice must be one finite 3x3 matrix")
    lengths = np.linalg.norm(lattice, axis=1)
    if np.any(lengths <= 0):
        raise ValueError("predicted lattice has a non-positive vector length")
    angles: list[float] = []
    for first, second in ((1, 2), (0, 2), (0, 1)):
        cosine = float(np.dot(lattice[first], lattice[second]) / (lengths[first] * lengths[second]))
        angles.append(math.degrees(math.acos(float(np.clip(cosine, -1.0, 1.0)))))
    if any(not 0 < angle < 180 for angle in angles):
        raise ValueError("predicted lattice has a degenerate angle")
    return lengths.tolist(), angles


def output_structure(
    lattice_matrix: np.ndarray,
    atom_types: np.ndarray,
    fractional_coordinates: np.ndarray,
) -> Structure:
    lengths, angles = lattice_parameters(lattice_matrix)
    species = np.asarray(atom_types, dtype=np.int64)
    coordinates = np.asarray(fractional_coordinates, dtype=np.float64)
    if coordinates.shape != (len(species), 3) or not np.isfinite(coordinates).all():
        raise ValueError("predicted coordinates do not match the atom list")
    return Structure(
        Lattice.from_parameters(*lengths, *angles),
        species.tolist(),
        coordinates,
        coords_are_cartesian=False,
    )
