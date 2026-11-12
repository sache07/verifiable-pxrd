#!/usr/bin/env python3
"""Diagnostic: release a nonnegative common U/W/X trend in stages.

Called as SCRIPT INPUT.gpx OUTPUT.gpx INPUTS_DIR. The submitted inventory,
structures, phase broadening, angular model, and background are retained. The
existing common-profile values are first held fixed, then W, U, and X are
released sequentially with physical bounds. This tests whether a frozen narrow
common profile, rather than absent phase complexity, limits the fresh fit.
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


def refine_stage(project, label, history, rounds=3):
    for iteration in range(1, rounds + 1):
        project.refine(makeBack=False)
        hist = project.histogram(0)
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


def correlations(project, limit=20):
    covariance = project.data["Covariance"]["data"]
    names = [str(value) for value in covariance.get("varyList", [])]
    matrix = covariance.get("covMatrix")
    if matrix is None or not names:
        return []
    matrix = np.asarray(matrix, float)
    sigma = np.sqrt(np.maximum(np.diag(matrix), 0.0))
    denominator = np.outer(sigma, sigma)
    matrix = np.divide(
        matrix, denominator, out=np.zeros_like(matrix), where=denominator > 0
    )
    rows = []
    for left in range(len(names)):
        for right in range(left + 1, len(names)):
            rows.append(
                {
                    "left": names[left],
                    "right": names[right],
                    "correlation": float(matrix[left, right]),
                }
            )
    rows.sort(key=lambda row: abs(row["correlation"]), reverse=True)
    return rows[:limit]


source, destination, inputs = map(Path, sys.argv[1:4])
project = G2sc.G2Project(str(source), newgpx=str(destination))
hist = matching_histogram(project, inputs)
inst = hist.data["Instrument Parameters"][0]

# Preserve the submitted numerical profile as the branch point, but stage its
# freedom. A zero-valued inactive term receives a small positive start only at
# the moment it is challenged; this is not a reset of the accepted fit.
for key in ("U", "W", "X"):
    inst[key][2] = False
for key, low, high in (
    ("U", 0.0, 400.0),
    ("W", 0.1, 400.0),
    ("X", 0.0, 100.0),
):
    project.set_Controls("parmMin", low, variable=f":{hist.id}:{key}")
    project.set_Controls("parmMax", high, variable=f":{hist.id}:{key}")

project.data["Controls"]["data"].update(
    {"max cyc": 12, "min dM/M": 0.0001, "parmFrozen": {"FrozenList": []}}
)
project.set_Frozen()
history = []

inst["W"][2] = True
refine_stage(project, "release_W", history)

hist = matching_histogram(project, inputs)
inst = hist.data["Instrument Parameters"][0]
if float(inst["U"][1]) <= 0.0:
    inst["U"][0:2] = [5.0, 5.0]
inst["U"][2] = True
refine_stage(project, "release_U", history)

hist = matching_histogram(project, inputs)
inst = hist.data["Instrument Parameters"][0]
if float(inst["X"][1]) <= 0.0:
    inst["X"][0:2] = [0.5, 0.5]
inst["X"][2] = True
refine_stage(project, "release_X", history)

project.save()
hist = matching_histogram(project, inputs)
inst = hist.data["Instrument Parameters"][0]
diagnostics = {
    "history": history,
    "profile": {
        key: {"value": float(inst[key][1]), "active": bool(inst[key][2])}
        for key in ("U", "V", "W", "X", "Y", "Z", "SH/L")
    },
    "mass_fractions": {
        str(key): float(value) for key, value in hist.ComputeMassFracs().items()
    },
    "top_correlations": correlations(project),
}
(destination.parent / "common_profile_diagnostics.json").write_text(
    json.dumps(diagnostics, indent=2) + "\n"
)
