#!/usr/bin/env python3
"""Compare compact nonnegative common-profile parameterizations."""

from pathlib import Path

from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent

MODELS = {
    "W": {"W": 20.0},
    "X": {"X": 15.0},
    "UW": {"U": 10.0, "W": 10.0},
    "UX": {"U": 10.0, "X": 10.0},
    "UWX": {"U": 5.0, "W": 5.0, "X": 10.0},
    "WX": {"W": 5.0, "X": 10.0},
}


def run(name: str, parameters: dict[str, float]) -> None:
    output = ROOT / f"profile_{name}.gpx"
    project = G2sc.G2Project(str(ROOT / "initial.gpx"), newgpx=str(output))
    hist = project.histogram(0)

    # Fix the arbitrary overall histogram scale and transfer its magnitude to
    # the phase scales, removing the exact scale-factor degeneracy.
    overall = hist.SampleParameters["Scale"][0]
    hist.SampleParameters["Scale"] = [1.0, False]
    for phase in project.phases():
        phase.HAPvalue("Scale", phase.HAPvalue("Scale") * overall)

    hist.clear_refinements({"Instrument Parameters": ["U", "V", "W", "X", "Y", "Z"]})
    for key in ["U", "V", "W", "X", "Y", "Z"]:
        hist.InstrumentParameters[key][1] = 0.0
    for key, value in parameters.items():
        hist.InstrumentParameters[key][1] = value
    hist.set_refinements({"Instrument Parameters": list(parameters)})
    project.set_Controls("cycles", 10)
    project.refine(makeBack=False)
    project.save()

    mass = hist.ComputeMassFracs()
    values = {key: hist.InstrumentParameters[key][1] for key in parameters}
    print(
        name,
        "wR", hist.get_wR(),
        "profile", values,
        "mass", mass,
        "cells", {phase.name: phase.get_cell() for phase in project.phases()},
    )


def main() -> None:
    for name, parameters in MODELS.items():
        try:
            run(name, parameters)
        except Exception as exc:
            print(name, "FAILED", repr(exc))


if __name__ == "__main__":
    main()
