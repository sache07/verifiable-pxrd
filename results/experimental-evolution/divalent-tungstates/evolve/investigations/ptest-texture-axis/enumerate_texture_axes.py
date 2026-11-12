#!/usr/bin/env python3
"""Diagnostic: compare low-index March--Dollase axes under one nuisance model.

Called as SCRIPT INPUT.gpx OUTPUT.gpx INPUTS_DIR. Exactly one phase must have
an active March--Dollase term. A texture-free branch and all primitive first-
shell directions are refined from the same submitted state; the lowest stored
Rwp branch is returned for independent fresh replay.
"""

from pathlib import Path
import json
import math
import shutil
import sys

import numpy as np
from GSASII import GSASIIscriptable as G2sc


AXES = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 1, 0),
    (1, 0, 1),
    (0, 1, 1),
    (1, 1, 1),
)


def matching_histogram(project, inputs):
    observed = np.loadtxt(Path(inputs) / "pattern.csv", delimiter=",", skiprows=1)
    matches = []
    for hist in project.histograms():
        if not hist.name.startswith("PWDR"):
            continue
        x = np.asarray(hist.getdata("X"))
        y = np.asarray(hist.getdata("Yobs"))
        if (
            x.shape == observed[:, 0].shape
            and np.allclose(x, observed[:, 0], rtol=0, atol=1e-7)
            and np.allclose(y, observed[:, 1], rtol=0, atol=1e-5)
        ):
            matches.append(hist)
    if len(matches) != 1:
        raise ValueError(f"Expected one matching histogram, found {len(matches)}")
    return matches[0]


def refine_to_stability(project, hist, rounds=3):
    history = []
    for iteration in range(1, rounds + 1):
        project.refine(makeBack=False)
        rvals = project.data["Covariance"]["data"].get("Rvals", {})
        history.append(
            {
                "iteration": iteration,
                "rwp_percent": float(hist.get_wR()),
                "max_shift_over_esd": rvals.get("Max shft/sig"),
                "converged": rvals.get("converged"),
            }
        )
        if (
            history[-1]["converged"]
            and history[-1]["max_shift_over_esd"] is not None
            and history[-1]["max_shift_over_esd"] < 0.2
        ):
            break
    return history


source, destination, inputs = map(Path, sys.argv[1:4])
probe = G2sc.G2Project(str(source))
probe_hist = matching_histogram(probe, inputs)
active = []
for phase in probe.phases():
    preferred = phase.data["Histograms"][probe_hist.name]["Pref.Ori."]
    if preferred[0] == "MD" and bool(preferred[2]):
        active.append((phase.name, float(preferred[1])))
if len(active) != 1:
    raise ValueError(f"Expected one active March-Dollase phase, found {active}")
target_name, initial_ratio = active[0]
if not math.isfinite(initial_ratio) or initial_ratio <= 0.0:
    raise ValueError(f"Invalid starting March-Dollase ratio {initial_ratio}")

candidate_dir = destination.parent / "texture_candidates"
candidate_dir.mkdir(exist_ok=True)
branches = [("none", None)] + [
    ("axis_" + "".join(str(value) for value in axis), axis) for axis in AXES
]
records = []
paths = []

for label, axis in branches:
    candidate = candidate_dir / f"{label}.gpx"
    project = G2sc.G2Project(str(source), newgpx=str(candidate))
    hist = matching_histogram(project, inputs)
    phase = project.phase(target_name)
    preferred = phase.data["Histograms"][hist.name]["Pref.Ori."]
    preferred[0] = "MD"
    preferred[1] = 1.0 if axis is None else initial_ratio
    preferred[2] = axis is not None
    if axis is not None:
        preferred[3] = list(axis)

    project.data["Controls"]["data"].update(
        {"max cyc": 12, "min dM/M": 0.0001, "parmFrozen": {"FrozenList": []}}
    )
    project.set_Controls(
        "parmMin", 0.5, variable=f"{phase.id}:{hist.id}:MD"
    )
    project.set_Controls(
        "parmMax", 2.0, variable=f"{phase.id}:{hist.id}:MD"
    )
    project.set_Frozen()
    history = refine_to_stability(project, hist)
    project.save()
    records.append(
        {
            "label": label,
            "axis": axis,
            "ratio": float(preferred[1]),
            "active": bool(preferred[2]),
            "rwp_percent": float(hist.get_wR()),
            "history": history,
            "mass_fractions": {
                str(key): {"fraction": float(value[0]), "esd": float(value[1])}
                for key, value in hist.ComputeMassFracs().items()
            },
        }
    )
    paths.append(candidate)

selected = min(range(len(records)), key=lambda index: records[index]["rwp_percent"])
shutil.copyfile(paths[selected], destination)
(destination.parent / "texture_axis_diagnostics.json").write_text(
    json.dumps(
        {
            "target_phase": target_name,
            "initial_ratio": initial_ratio,
            "selected": selected,
            "candidates": records,
        },
        indent=2,
    )
    + "\n"
)
