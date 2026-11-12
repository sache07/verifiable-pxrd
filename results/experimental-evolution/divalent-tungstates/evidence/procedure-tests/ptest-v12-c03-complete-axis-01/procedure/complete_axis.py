#!/usr/bin/env python3
"""Diagnostic: challenge the dominant active March term on a complete axis set.

Called as SCRIPT INPUT.gpx OUTPUT.gpx INPUTS_DIR. The dominant phase with an
active March--Dollase term is selected from public-project mass fractions. Each
axis starts from the same mature project, and all existing nuisance flags remain
open. Signed and unequal diagonals are included because they need not share an
orbit in lower symmetry and one generic "diagonal" is not a complete basis.
"""

from pathlib import Path
import json
import math
import shutil
import sys

import numpy as np
from GSASII import GSASIIscriptable as G2sc


AXES = (
    (1, 0, 0), (0, 1, 0), (0, 0, 1),
    (1, 1, 0), (1, -1, 0),
    (1, 0, 1), (1, 0, -1),
    (0, 1, 1), (0, 1, -1),
    (1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1),
    (1, 1, 2), (1, 1, -2), (1, -1, 2), (-1, 1, 2),
)


def matching_histogram(project, inputs):
    observed = np.loadtxt(Path(inputs) / "pattern.csv", delimiter=",", skiprows=1)
    matches = []
    for hist in project.histograms():
        if not hist.name.startswith("PWDR"):
            continue
        x = np.asarray(hist.getdata("X"))
        y = np.asarray(hist.getdata("Yobs"))
        if (x.shape == observed[:, 0].shape
                and np.allclose(x, observed[:, 0], rtol=0, atol=1e-7)
                and np.allclose(y, observed[:, 1], rtol=0, atol=1e-5)):
            matches.append(hist)
    if len(matches) != 1:
        raise ValueError(f"Expected one matching histogram, found {len(matches)}")
    return matches[0]


def refine_to_stability(project, hist, rounds=3):
    history = []
    for iteration in range(1, rounds + 1):
        project.refine(makeBack=False)
        rvals = project.data["Covariance"]["data"].get("Rvals", {})
        history.append({
            "iteration": iteration,
            "rwp_percent": float(hist.get_wR()),
            "max_shift_over_esd": rvals.get("Max shft/sig"),
            "converged": rvals.get("converged"),
        })
        if (history[-1]["converged"]
                and history[-1]["max_shift_over_esd"] is not None
                and abs(history[-1]["max_shift_over_esd"]) < 0.2):
            break
    return history


def axis_label(axis):
    return "_".join(("m" + str(abs(v))) if v < 0 else ("p" + str(v)) for v in axis)


source, destination, inputs = map(Path, sys.argv[1:4])
probe = G2sc.G2Project(str(source))
probe_hist = matching_histogram(probe, inputs)
fractions = probe_hist.ComputeMassFracs()
active = []
for phase in probe.phases():
    preferred = phase.getHAPvalues(probe_hist.name)["Pref.Ori."]
    if preferred[0] == "MD" and bool(preferred[2]):
        fraction = float(fractions.get(phase.name, (0.0, 0.0))[0])
        active.append((fraction, phase.name, float(preferred[1]), list(preferred[3])))
if not active:
    raise ValueError("No active March--Dollase phase")
_, target_name, initial_ratio, initial_axis = max(active)
if not math.isfinite(initial_ratio) or initial_ratio <= 0:
    raise ValueError(f"Invalid starting ratio {initial_ratio}")

candidate_dir = destination.parent / "complete_axis_candidates"
candidate_dir.mkdir(exist_ok=True)
branches = [("none", None)] + [("axis_" + axis_label(axis), axis) for axis in AXES]
records = []
paths = []

for label, axis in branches:
    candidate = candidate_dir / f"{label}.gpx"
    project = G2sc.G2Project(str(source), newgpx=str(candidate))
    hist = matching_histogram(project, inputs)
    phase = project.phase(target_name)
    preferred = phase.getHAPvalues(hist.name)["Pref.Ori."]
    preferred[0] = "MD"
    preferred[1] = 1.0 if axis is None else initial_ratio
    preferred[2] = axis is not None
    if axis is not None:
        preferred[3] = list(axis)
    project.data["Controls"]["data"].update({
        "max cyc": 12,
        "min dM/M": 0.0001,
        "parmFrozen": {"FrozenList": []},
    })
    project.set_Controls("parmMin", 0.5, variable=f"{phase.id}:{hist.id}:MD")
    project.set_Controls("parmMax", 2.0, variable=f"{phase.id}:{hist.id}:MD")
    project.set_Frozen()
    history = refine_to_stability(project, hist)
    project.save()
    frozen = project.get_Frozen()
    converged = bool(history[-1].get("converged"))
    ratio = float(preferred[1])
    valid = converged and not frozen and 0.5 < ratio < 2.0
    records.append({
        "label": label,
        "axis": axis,
        "ratio": ratio,
        "rwp_percent": float(hist.get_wR()),
        "valid": valid,
        "frozen": frozen,
        "history": history,
        "mass_fractions": {
            str(key): {"fraction": float(value[0]), "esd": float(value[1])}
            for key, value in hist.ComputeMassFracs().items()
        },
    })
    paths.append(candidate)

valid_indices = [i for i, record in enumerate(records) if record["valid"]]
if not valid_indices:
    raise RuntimeError("No valid texture-axis branch")
selected = min(valid_indices, key=lambda i: records[i]["rwp_percent"])
shutil.copyfile(paths[selected], destination)
(destination.parent / "complete_axis_diagnostics.json").write_text(
    json.dumps({
        "target_phase": target_name,
        "initial_axis": initial_axis,
        "initial_ratio": initial_ratio,
        "selected": selected,
        "candidates": records,
    }, indent=2) + "\n"
)
