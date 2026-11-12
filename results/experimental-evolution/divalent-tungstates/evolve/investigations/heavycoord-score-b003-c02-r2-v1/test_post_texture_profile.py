#!/usr/bin/env python3
"""Rebuild the common profile after accepting WO3 [001] texture."""

from pathlib import Path

from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
MODELS = {
    "X": {"X": 14.0},
    "UX": {"U": 50.0, "X": 14.0},
    "WX": {"W": 2.0, "X": 14.0},
    "UWX": {"U": 25.0, "W": 2.0, "X": 14.0},
    "W": {"W": 100.0},
}


def main() -> None:
    for label, parameters in MODELS.items():
        output = ROOT / f"post_texture_profile_{label}.gpx"
        project = G2sc.G2Project(
            str(ROOT / "texture_WO3_001.gpx"), newgpx=str(output)
        )
        hist = project.histogram(0)
        hist.clear_refinements(
            {"Instrument Parameters": ["U", "V", "W", "X", "Y", "Z"]}
        )
        for key in ["U", "V", "W", "X", "Y", "Z"]:
            hist.InstrumentParameters[key][1] = 0.0
        for key, value in parameters.items():
            hist.InstrumentParameters[key][1] = value
        hist.set_refinements({"Instrument Parameters": list(parameters)})
        project.set_Controls("cycles", 10)
        try:
            project.refine(makeBack=False)
            project.save()
            print(
                label,
                "wR", hist.get_wR(),
                "profile", {
                    key: hist.InstrumentParameters[key][1] for key in parameters
                },
                "mass", hist.ComputeMassFracs(),
            )
        except Exception as exc:
            print(label, "FAILED", repr(exc))


if __name__ == "__main__":
    main()
