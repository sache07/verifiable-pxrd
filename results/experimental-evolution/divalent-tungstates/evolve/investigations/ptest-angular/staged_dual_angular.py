#!/usr/bin/env python3
"""Diagnostic: release the second angular correction after model convergence.

Called as SCRIPT INPUT.gpx OUTPUT.gpx INPUTS_DIR. The existing inventory,
structures, background, and profile model are retained. Both constant zero and
Bragg--Brentano specimen displacement are then refined from the converged state.
"""

from pathlib import Path
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


source, destination, inputs = map(Path, sys.argv[1:4])
project = G2sc.G2Project(str(source), newgpx=str(destination))
hist = matching_histogram(project, inputs)
inst = hist.data["Instrument Parameters"][0]
sample = hist.data["Sample Parameters"]

# Retain fitted values. Only release whichever angular term had been held fixed.
inst["Zero"][2] = True
sample["Shift"][1] = True
project.set_Controls("parmMin", -0.5, variable=f":{hist.id}:Zero")
project.set_Controls("parmMax", 0.5, variable=f":{hist.id}:Zero")
project.set_Controls("parmMin", -2000.0, variable=f":{hist.id}:Shift")
project.set_Controls("parmMax", 2000.0, variable=f":{hist.id}:Shift")

project.set_Controls("cycles", 20)
project.set_Frozen()
for _ in range(3):
    project.refine(makeBack=False)
project.save()
