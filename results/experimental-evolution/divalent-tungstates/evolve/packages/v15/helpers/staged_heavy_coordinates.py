#!/usr/bin/env python3
"""Greedily challenge high-scattering atom coordinates, one site at a time.

Called by the controller as SCRIPT INPUT.gpx OUTPUT.gpx INPUTS_DIR.  Selection
uses only the observed-profile Rwp and conservative geometry/step guards.
"""

from __future__ import annotations

import json
import math
import re
import shutil
import sys
from pathlib import Path

import numpy as np
from GSASII import GSASIIElem as G2elem
from GSASII import GSASIIscriptable as G2sc
from GSASII import GSASIIstrMain as G2str


MIN_RWP_GAIN = 0.003  # absolute Rwp percentage point
MAX_STEP_A = 0.15
MAX_REPLAYS = 3


def lattice_matrix(phase: G2sc.G2Phase) -> np.ndarray:
    cell = phase.get_cell()
    a, b, c = (cell[f"length_{axis}"] for axis in "abc")
    alpha, beta, gamma = (
        math.radians(cell[f"angle_{name}"])
        for name in ("alpha", "beta", "gamma")
    )
    avec = np.array([a, 0.0, 0.0])
    bvec = np.array([b * math.cos(gamma), b * math.sin(gamma), 0.0])
    cx = c * math.cos(beta)
    cy = c * (math.cos(alpha) - math.cos(beta) * math.cos(gamma)) / math.sin(gamma)
    cz = math.sqrt(max(0.0, c * c - cx * cx - cy * cy))
    return np.vstack([avec, bvec, np.array([cx, cy, cz])])


def coordinate_snapshot(project: G2sc.G2Project) -> dict[str, dict[str, np.ndarray]]:
    return {
        phase.name: {
            atom.label: np.asarray(atom.coordinates, dtype=float)
            for atom in phase.atoms()
        }
        for phase in project.phases()
    }


def maximum_step(project: G2sc.G2Project, before) -> float:
    largest = 0.0
    for phase in project.phases():
        matrix = lattice_matrix(phase)
        for atom in phase.atoms():
            delta = np.asarray(atom.coordinates, dtype=float) - before[phase.name][atom.label]
            delta -= np.round(delta)
            largest = max(largest, float(np.linalg.norm(delta @ matrix)))
    return largest


def minimum_distance(phase: G2sc.G2Phase) -> float:
    controls, data = phase.InitDisAgl(useAll=False)
    controls["Factors"][1] = 0
    _labels, distances, _angles = G2str.RetDistAngle(controls, data, dmin=0.01)
    values = []
    for entries in distances.values():
        for row in entries:
            values.append(float(row[-2]))
    return min(values) if values else float("inf")


def geometry_ok(project: G2sc.G2Project, baseline_minima) -> tuple[bool, dict]:
    minima = {}
    short = {}
    ok = True
    for phase in project.phases():
        value = minimum_distance(phase)
        minima[phase.name] = value
        short[phase.name] = phase.ShortDistances(useAll=False)
        # Preserve legitimately short starting motifs, but do not create a new
        # sub-1.65 A contact from an initially ordinary oxide framework.
        floor = min(1.65, baseline_minima[phase.name] - 0.05)
        if value < floor or short[phase.name]:
            ok = False
    return ok, {"minimum_distances_A": minima, "short_distances": short}


def rwp(project: G2sc.G2Project) -> float:
    return float(project.histogram(0).residuals["wR"])


def refine_reopened(path: Path) -> G2sc.G2Project:
    project = G2sc.G2Project(str(path))
    project.set_Controls("cycles", 16)
    for _ in range(MAX_REPLAYS):
        project.refine(makeBack=False)
        project.save()
        project = G2sc.G2Project(str(path))
        shift = project.data.get("Covariance", {}).get("data", {}).get("Rvals", {}).get(
            "Max shft/sig"
        )
        if shift is not None and abs(float(shift)) < 0.05:
            break
    return project


def heavy_unset_sites(project: G2sc.G2Project):
    rows = []
    fractions = project.histogram(0).ComputeMassFracs()
    phases = sorted(
        project.phases(),
        key=lambda phase: fractions.get(phase.name, (0.0, 0.0))[0],
        reverse=True,
    )
    for phase in phases:
        for atom in phase.atoms():
            try:
                z_number = int(G2elem.GetAtomInfo(atom.element)["Z"])
            except Exception:
                continue
            if z_number < 20 or "X" in atom.refinement_flags:
                continue
            rows.append((phase.name, atom.label, z_number))
    return rows


def safe_tag(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: SCRIPT INPUT.gpx OUTPUT.gpx INPUTS_DIR")
    source = Path(sys.argv[1]).resolve()
    output = Path(sys.argv[2]).resolve()
    _inputs = Path(sys.argv[3]).resolve()
    shutil.copy2(source, output)

    baseline = G2sc.G2Project(str(output))
    baseline_rwp = rwp(baseline)
    starting_minima = {phase.name: minimum_distance(phase) for phase in baseline.phases()}
    accepted = []
    rejected = []

    for index, (phase_name, atom_label, z_number) in enumerate(heavy_unset_sites(baseline)):
        current = G2sc.G2Project(str(output))
        before_rwp = rwp(current)
        before_coords = coordinate_snapshot(current)
        before_frozen = set(map(str, current.get_Frozen() or []))
        candidate = output.with_name(
            f"{output.stem}.coord_{index:02d}_{safe_tag(phase_name)}_{safe_tag(atom_label)}.gpx"
        )
        trial = G2sc.G2Project(str(output), newgpx=str(candidate))
        atom = trial.phase(phase_name).atom(atom_label)
        flags = atom.refinement_flags.strip()
        atom.refinement_flags = "X" + ("U" if "U" in flags else "")
        trial.save()

        row = {
            "phase": phase_name,
            "atom": atom_label,
            "atomic_number": z_number,
            "before_Rwp": before_rwp,
        }
        try:
            trial = refine_reopened(candidate)
            after_rwp = rwp(trial)
            step = maximum_step(trial, before_coords)
            new_frozen = sorted(set(map(str, trial.get_Frozen() or [])) - before_frozen)
            physical, geometry = geometry_ok(trial, starting_minima)
            gain = before_rwp - after_rwp
            row.update(
                {
                    "after_Rwp": after_rwp,
                    "gain": gain,
                    "maximum_coordinate_step_A": step,
                    "new_frozen_variables": new_frozen,
                    "geometry": geometry,
                }
            )
            if (
                math.isfinite(after_rwp)
                and gain >= MIN_RWP_GAIN
                and step <= MAX_STEP_A
                and not new_frozen
                and physical
            ):
                shutil.copy2(candidate, output)
                row["decision"] = "accept"
                accepted.append(row)
            else:
                row["decision"] = "reject"
                rejected.append(row)
        except Exception as exc:
            row.update({"decision": "reject_exception", "error": repr(exc)})
            rejected.append(row)

    final = refine_reopened(output)
    final.save(str(output))
    summary = {
        "starting_Rwp": baseline_rwp,
        "final_Rwp": rwp(final),
        "accepted": accepted,
        "rejected": rejected,
        "final_minimum_distances_A": {
            phase.name: minimum_distance(phase) for phase in final.phases()
        },
    }
    print("STAGED_HEAVY_COORDINATES " + json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
