#!/usr/bin/env python3
"""Diagnostic: challenge bounded common axial asymmetry after convergence.

Called as SCRIPT INPUT.gpx OUTPUT.gpx INPUTS_DIR. Inventory, structures,
background, angular correction, widths, and phase terms are retained. SH/L is
released from a modest positive start and the full submitted model is
reconverged for independent fresh replay.
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


def top_correlations(project, limit=20):
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
before = float(inst["SH/L"][1])
if before <= 0.002:
    inst["SH/L"][0:2] = [0.01, 0.01]
inst["SH/L"][2] = True
project.set_Controls("parmMin", 0.002, variable=f":{hist.id}:SH/L")
project.set_Controls("parmMax", 0.2, variable=f":{hist.id}:SH/L")
project.data["Controls"]["data"].update(
    {"max cyc": 12, "min dM/M": 0.0001, "parmFrozen": {"FrozenList": []}}
)
project.set_Frozen()

history = []
for iteration in range(1, 5):
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

project.save()
diagnostics = {
    "initial_sh_l": before,
    "final_sh_l": float(inst["SH/L"][1]),
    "history": history,
    "mass_fractions": {
        str(key): {"fraction": float(value[0]), "esd": float(value[1])}
        for key, value in hist.ComputeMassFracs().items()
    },
    "top_correlations": top_correlations(project),
}
(destination.parent / "asymmetry_diagnostics.json").write_text(
    json.dumps(diagnostics, indent=2) + "\n"
)
