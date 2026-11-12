#!/usr/bin/env python3
"""Diagnostic: refine the saved isotropic phase microstrain terms.

Called as: refine_isotropic_strain.py INPUT.gpx OUTPUT.gpx INPUTS_DIR
This deliberately tests one mechanism. It preserves the model inventory and all
existing flags, changes no hidden inputs, and constrains microstrain nonnegative.
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
        if x.shape == observed[:, 0].shape and np.allclose(x, observed[:, 0], rtol=0, atol=1e-7) and np.allclose(y, observed[:, 1], rtol=0, atol=1e-5):
            matches.append(hist)
    if len(matches) != 1:
        raise ValueError(f"Expected one histogram matching public observations, found {len(matches)}")
    return matches[0]


def main():
    source, destination, inputs = map(Path, sys.argv[1:4])
    project = G2sc.G2Project(gpxfile=str(source), newgpx=str(destination))
    hist = matching_histogram(project, inputs)
    project.set_Controls("cycles", 20)
    for phase in project.phases():
        if hist.name not in phase.data.get("Histograms", {}):
            continue
        hap = phase.getHAPvalues(hist.name)
        if hap["Mustrain"][0] != "isotropic":
            continue
        phase.set_HAP_refinements({"Mustrain": {"type": "isotropic", "refine": True}}, [hist])
        project.set_Controls("parmMin", 0.0, variable=f"{phase.id}:{hist.id}:Mustrain;i")
    project.do_refinements([{}])
    project.do_refinements([{}])
    project.save(str(destination))


if __name__ == "__main__":
    main()
