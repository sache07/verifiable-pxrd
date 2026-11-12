#!/usr/bin/env python3
"""Oracle-informed c04 diagnostic: fix generating width terms, retain structure.

This investigation-only script contains synthetic profile values and must never
be packaged. Called as SCRIPT INPUT.gpx OUTPUT.gpx INPUTS_DIR.
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

profile = {
    "U": 31.75902530976706,
    "V": 0.0,
    "W": 3.566115919668989,
    "X": 0.33799032354502895,
    "Y": 0.0,
    "Z": 0.0,
    "SH/L": 0.09793517547361105,
}
for key, value in profile.items():
    inst[key][0:2] = [value, value]
    inst[key][2] = False

phase_profile = {
    "MnWO4": (0.6902644718229473, 0.0),
    "Mn3O4": (0.11516438563349155, 2865.6286437705626),
    "WO3": (0.08758978638788843, 0.0),
}
matched = set()
for phase in project.phases():
    key = next((name for name in phase_profile if name in phase.name), None)
    if key is None:
        raise ValueError(f"Unexpected phase {phase.name}")
    matched.add(key)
    size, strain = phase_profile[key]
    hap = phase.data["Histograms"][hist.name]
    hap["Size"][0] = "isotropic"
    hap["Size"][1][0] = size
    hap["Size"][2][:] = [False] * len(hap["Size"][2])
    hap["Size"][5][:] = [False] * len(hap["Size"][5])
    hap["Mustrain"][0] = "isotropic"
    hap["Mustrain"][1][0] = strain
    hap["Mustrain"][2][:] = [False] * len(hap["Mustrain"][2])
    hap["Mustrain"][5][:] = [False] * len(hap["Mustrain"][5])
if matched != set(phase_profile):
    raise ValueError(f"Incomplete phase match: {matched}")

project.set_Controls("cycles", 20)
project.set_Frozen()
for _ in range(3):
    project.refine(makeBack=False)
project.save()
