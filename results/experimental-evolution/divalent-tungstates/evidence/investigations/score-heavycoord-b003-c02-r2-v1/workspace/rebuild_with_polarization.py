#!/usr/bin/env python3
"""Rebuild the common profile with polarization before extra texture terms."""

from pathlib import Path

from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "cu3_size_axis_110.gpx"
OUTPUT = ROOT / "baseline_polarization.gpx"


def main() -> None:
    project = G2sc.G2Project(str(BASE), newgpx=str(OUTPUT))
    hist = project.histogram(0)
    hist.InstrumentParameters["Polariz."][1] = 0.55
    hist.set_refinements({"Instrument Parameters": ["Polariz."]})
    project.set_Controls("cycles", 16)
    project.refine(makeBack=False)
    project.save()
    replay = G2sc.G2Project(str(OUTPUT))
    replay.set_Controls("cycles", 16)
    replay.refine(makeBack=False)
    replay.save()
    rhist = replay.histogram(0)
    print(
        "wR", rhist.get_wR(),
        "polar", rhist.InstrumentParameters["Polariz."],
        "profile", {key: rhist.InstrumentParameters[key] for key in ("U", "W", "X")},
        "mass", rhist.ComputeMassFracs(),
    )


if __name__ == "__main__":
    main()
