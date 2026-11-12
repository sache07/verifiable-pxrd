#!/usr/bin/env python3
"""Rebuild the common instrumental profile after accepting CuO."""

from pathlib import Path

from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "three_phase_CuO_ambient.gpx"
MODELS = {
    "X": {"X": 13.2},
    "U": {"U": 40.0},
    "W": {"W": 16.0},
    "UX": {"U": 39.5, "X": 13.2},
    "WX": {"W": 2.0, "X": 13.2},
    "UWX": {"U": 39.5, "W": 0.5, "X": 13.2},
}


def main() -> None:
    for label, parameters in MODELS.items():
        output = ROOT / f"three_phase_profile_{label}.gpx"
        project = G2sc.G2Project(str(BASE), newgpx=str(output))
        hist = project.histogram(0)
        hist.clear_refinements(
            {"Instrument Parameters": ["U", "V", "W", "X", "Y", "Z"]}
        )
        for key in ("U", "V", "W", "X", "Y", "Z"):
            hist.InstrumentParameters[key][1] = 0.0
        for key, value in parameters.items():
            hist.InstrumentParameters[key][1] = value
        hist.set_refinements({"Instrument Parameters": list(parameters)})
        project.set_Controls("cycles", 12)
        try:
            project.refine(makeBack=False)
            project.save()
            replay = G2sc.G2Project(str(output))
            replay.set_Controls("cycles", 12)
            replay.refine(makeBack=False)
            replay.save()
            rhist = replay.histogram(0)
            print(
                label,
                "wR", rhist.get_wR(),
                "profile",
                {key: rhist.InstrumentParameters[key][1] for key in parameters},
                "mass", rhist.ComputeMassFracs(),
            )
        except Exception as exc:
            print(label, "FAILED", repr(exc))


if __name__ == "__main__":
    main()
