#!/usr/bin/env python3
"""Recheck angular, asymmetry, polarization and roughness nuisance terms."""

from pathlib import Path

from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "interaction_CuO_texture_010.gpx"


def setup_shift(hist) -> None:
    hist.clear_refinements({"Instrument Parameters": ["Zero"]})
    hist.InstrumentParameters["Zero"][1] = 0.0
    hist.SampleParameters["Shift"] = [-100.0, True]


def setup_shl(hist) -> None:
    hist.InstrumentParameters["SH/L"][1] = 0.01
    hist.set_refinements({"Instrument Parameters": ["SH/L"]})


def setup_polarization(hist) -> None:
    hist.set_refinements({"Instrument Parameters": ["Polariz."]})


def setup_roughness(hist) -> None:
    hist.SampleParameters["SurfRoughA"] = [0.5, True]
    hist.SampleParameters["SurfRoughB"] = [0.05, True]


def main() -> None:
    trials = {
        "shift": setup_shift,
        "shl": setup_shl,
        "polarization": setup_polarization,
        "roughness": setup_roughness,
    }
    for label, setup in trials.items():
        output = ROOT / f"final_term_{label}.gpx"
        project = G2sc.G2Project(str(BASE), newgpx=str(output))
        hist = project.histogram(0)
        setup(hist)
        project.set_Controls("cycles", 16)
        try:
            project.refine(makeBack=False)
            project.save()
            replay = G2sc.G2Project(str(output))
            replay.set_Controls("cycles", 16)
            replay.refine(makeBack=False)
            replay.save()
            rhist = replay.histogram(0)
            print(
                label,
                "wR", rhist.get_wR(),
                "zero", rhist.InstrumentParameters["Zero"],
                "shift", rhist.SampleParameters["Shift"],
                "shl", rhist.InstrumentParameters["SH/L"],
                "polar", rhist.InstrumentParameters["Polariz."],
                "rough", rhist.SampleParameters["SurfRoughA"], rhist.SampleParameters["SurfRoughB"],
                "mass", rhist.ComputeMassFracs(),
            )
        except Exception as exc:
            print(label, "FAILED", repr(exc))


if __name__ == "__main__":
    main()
