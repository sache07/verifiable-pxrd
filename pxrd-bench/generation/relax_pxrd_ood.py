"""Run one locked MACE-MH-1 variable-cell relaxation for pXRD-ood.

This helper is intentionally separate from ``build_pxrd_ood.py`` because the
PyXtal generation environment and the sim-bench MACE runtime need not be the same
Python environment. It writes the relaxed CIF and a small JSON diagnostic record.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
from importlib.metadata import version
from pathlib import Path
from typing import Any

import numpy as np
from ase.constraints import FixSymmetry
from ase.filters import FrechetCellFilter
from ase.optimize import FIRE
from pymatgen.analysis.structure_matcher import StructureMatcher
from pymatgen.core import Structure
from pymatgen.io.ase import AseAtomsAdaptor

MODEL_NAME = "MACE-MH-1"
MODEL_URL = (
    "https://github.com/ACEsuit/mace-foundations/releases/download/"
    "mace_mh_1/mace-mh-1.model"
)
EXPECTED_MODEL_SHA256 = "a522eb7f59c7879963d41586528f4980baf33e086c94aa92e3eafdeccad3be47"
DEFAULT_MODEL = Path.home() / ".cache/mace/macemh1model"
DEFAULT_HEAD = "omat_pbe"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    temporary = path.with_suffix(path.suffix + ".partial")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("diagnostics", type=Path)
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--head", default=DEFAULT_HEAD)
    parser.add_argument("--fmax", type=float, default=0.10)
    parser.add_argument("--steps", type=int, default=1000)
    parser.add_argument("--maxstep", type=float, default=0.08)
    args = parser.parse_args()

    if sha256_file(args.model) != EXPECTED_MODEL_SHA256:
        raise RuntimeError(f"MACE checkpoint digest mismatch: {args.model}")
    os.environ.setdefault("TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD", "1")
    from mace.calculators import MACECalculator

    initial = Structure.from_file(args.input)
    atoms = AseAtomsAdaptor.get_atoms(initial)
    atoms.pbc = True
    calculator = MACECalculator(
        model_paths=str(args.model),
        device="cpu",
        default_dtype="float64",
        enable_cueq=False,
        head=args.head,
    )
    atoms.calc = calculator
    initial_energy = float(atoms.get_potential_energy())
    initial_forces = atoms.get_forces()
    atoms.set_constraint(FixSymmetry(atoms))
    filtered = FrechetCellFilter(atoms)
    optimizer = FIRE(filtered, logfile=None, maxstep=args.maxstep)
    converged = bool(optimizer.run(fmax=args.fmax, steps=args.steps))
    relaxed = AseAtomsAdaptor.get_structure(atoms)
    final_energy = float(atoms.get_potential_energy())
    final_forces = atoms.get_forces()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    relaxed.to(filename=str(args.output), fmt="cif", symprec=None)
    matcher = StructureMatcher(
        ltol=0.25,
        stol=0.35,
        angle_tol=7,
        primitive_cell=True,
        scale=True,
    )
    report = {
        "converged": converged,
        "energy_change_ev_per_atom": (final_energy - initial_energy) / len(initial),
        "final_energy_ev_per_atom": final_energy / len(initial),
        "final_max_force_ev_per_angstrom": float(np.linalg.norm(final_forces, axis=1).max()),
        "force_tolerance_ev_per_angstrom": args.fmax,
        "initial_energy_ev_per_atom": initial_energy / len(initial),
        "initial_max_force_ev_per_angstrom": float(np.linalg.norm(initial_forces, axis=1).max()),
        "mace_torch_version": version("mace-torch"),
        "ase_version": version("ase"),
        "numpy_version": version("numpy"),
        "pymatgen_version": version("pymatgen"),
        "torch_version": version("torch"),
        "model_path": str(args.model),
        "model_name": MODEL_NAME,
        "model_url": MODEL_URL,
        "model_sha256": EXPECTED_MODEL_SHA256,
        "model_head": args.head,
        "optimizer": "ASE FIRE + FrechetCellFilter + FixSymmetry",
        "python": platform.python_version(),
        "steps": int(optimizer.nsteps),
        "structure_match_after_relaxation": bool(matcher.fit(initial, relaxed)),
    }
    write_json(args.diagnostics, report)
    if not converged:
        raise RuntimeError(
            f"MACE relaxation did not converge in {args.steps} steps; diagnostics written"
        )


if __name__ == "__main__":
    main()
