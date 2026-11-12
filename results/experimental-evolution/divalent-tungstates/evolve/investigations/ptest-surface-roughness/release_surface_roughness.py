#!/usr/bin/env python3
"""Diagnostic: challenge Bragg--Brentano surface roughness in two stages.

Called as SCRIPT INPUT.gpx OUTPUT.gpx INPUTS_DIR. The submitted inventory,
structure, background, profile, texture, and polarization are retained. A and
then B of the Suortti surface-roughness correction are released from a common
physical start and the complete model is reconverged for fresh replay.
"""

from pathlib import Path
import json
import sys

import numpy as np
from GSASII import GSASIIscriptable as G2sc


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


def refine_stage(project, hist, label, history, rounds=4):
    for iteration in range(1, rounds + 1):
        project.refine(makeBack=False)
        rvals = project.data["Covariance"]["data"].get("Rvals", {})
        history.append(
            {
                "stage": label,
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


source, destination, inputs = map(Path, sys.argv[1:4])
project = G2sc.G2Project(str(source), newgpx=str(destination))
hist = matching_histogram(project, inputs)
sample = hist.data["Sample Parameters"]
initial = {
    key: {"value": float(sample[key][0]), "active": bool(sample[key][1])}
    for key in ("SurfRoughA", "SurfRoughB")
}

# These are generic Suortti starts, not values or limits from the generator.
sample["SurfRoughA"][:] = [0.5, False]
sample["SurfRoughB"][:] = [0.1, False]
project.set_Controls("parmMin", 0.0, variable=f":{hist.id}:SurfRoughA")
project.set_Controls("parmMax", 1.0, variable=f":{hist.id}:SurfRoughA")
project.set_Controls("parmMin", 0.0, variable=f":{hist.id}:SurfRoughB")
project.set_Controls("parmMax", 5.0, variable=f":{hist.id}:SurfRoughB")
project.data["Controls"]["data"].update(
    {"max cyc": 12, "min dM/M": 0.0001, "parmFrozen": {"FrozenList": []}}
)
project.set_Frozen()

history = []
sample["SurfRoughA"][1] = True
refine_stage(project, hist, "release_A", history)
sample["SurfRoughB"][1] = True
refine_stage(project, hist, "release_B", history)
project.save()

diagnostics = {
    "initial": initial,
    "final": {
        key: {"value": float(sample[key][0]), "active": bool(sample[key][1])}
        for key in ("SurfRoughA", "SurfRoughB")
    },
    "history": history,
    "mass_fractions": {
        str(key): {"fraction": float(value[0]), "esd": float(value[1])}
        for key, value in hist.ComputeMassFracs().items()
    },
}
(destination.parent / "surface_roughness_diagnostics.json").write_text(
    json.dumps(diagnostics, indent=2) + "\n"
)
