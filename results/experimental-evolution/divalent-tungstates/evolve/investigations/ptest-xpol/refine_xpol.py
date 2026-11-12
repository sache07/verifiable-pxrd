#!/usr/bin/env python3
"""Diagnostic staged refinement of uncalibrated X-ray profile X and polarization.

Called as: refine_xpol.py INPUT.gpx OUTPUT.gpx INPUTS_DIR
The source project is copied through GSAS-II's newgpx interface. Existing refinement
flags remain active. A small positive X seed is used only when the saved value is at
the nonnegative boundary; all values are then determined from the observed pattern.
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
    hid = hist.id

    instrument = hist.InstrumentParameters
    if instrument["X"][1] <= 0:
        instrument["X"][1] = 0.1
    project.set_Controls("parmMin", 0.0, variable=f":{hid}:X")
    hist.set_refinements({"Instrument Parameters": ["X"]})
    project.do_refinements([{}])

    project.set_Controls("parmMin", 0.0, variable=f":{hid}:Polariz.")
    project.set_Controls("parmMax", 1.0, variable=f":{hid}:Polariz.")
    hist.set_refinements({"Instrument Parameters": ["Polariz."]})
    project.do_refinements([{}])
    project.do_refinements([{}])
    project.save(str(destination))


if __name__ == "__main__":
    main()
