#!/usr/bin/env python3
"""Diagnostic: replace clamped CW widths with a simple nonnegative baseline.

Called as SCRIPT INPUT.gpx OUTPUT.gpx INPUTS_DIR.  Inventory and structures
are unchanged.  The test deliberately uses only W/X globally, then releases
nonnegative isotropic phase strain from a neutral zero rather than from GSAS's
fixed 1000 ppm default.
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
        x, y = np.asarray(hist.getdata("X")), np.asarray(hist.getdata("Yobs"))
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

# A deliberately low-dimensional, everywhere nonnegative starting profile.
for key in ("U", "V", "Y", "Z"):
    inst[key][1], inst[key][2] = 0.0, False
inst["W"][1], inst["W"][2] = 10.0, True
inst["X"][1], inst["X"][2] = 2.0, True
inst["SH/L"][1], inst["SH/L"][2] = 0.002, False
project.set_Controls("parmMin", 0.0, variable=f":{hist.id}:W")
project.set_Controls("parmMax", 300.0, variable=f":{hist.id}:W")
project.set_Controls("parmMin", 0.0, variable=f":{hist.id}:X")
project.set_Controls("parmMax", 100.0, variable=f":{hist.id}:X")

project.set_Controls("cycles", 20)
project.set_Frozen()
project.refine(makeBack=False)

for phase in project.phases():
    if hist.name not in phase.data.get("Histograms", {}):
        continue
    hap = phase.data["Histograms"][hist.name]
    hap["Mustrain"][0] = "isotropic"
    hap["Mustrain"][1][0] = 0.0
    phase.set_HAP_refinements(
        {"Mustrain": {"type": "isotropic", "refine": True}}, [hist]
    )
    project.set_Controls(
        "parmMin", 0.0, variable=f"{phase.id}:{hist.id}:Mustrain;i"
    )
    project.set_Controls(
        "parmMax", 30000.0, variable=f"{phase.id}:{hist.id}:Mustrain;i"
    )

project.set_Frozen()
project.refine(makeBack=False)
project.refine(makeBack=False)
project.save()
