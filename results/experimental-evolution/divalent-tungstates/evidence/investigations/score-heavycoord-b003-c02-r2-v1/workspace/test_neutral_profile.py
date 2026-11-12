#!/usr/bin/env python3
"""Establish a common profile with every phase-width term neutral."""

from pathlib import Path

from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "three_phase_CuO_ambient.gpx"
MODELS = {
    "X": {"X": 13.2},
    "UX": {"U": 40.0, "X": 13.2},
    "WX": {"W": 4.0, "X": 13.2},
    "UWX": {"U": 32.0, "W": 4.0, "X": 12.6},
}


def neutralize_phase_widths(project: G2sc.G2Project) -> None:
    hist = project.histogram(0)
    for phase in project.phases():
        phase.setSampleProfile(hist, "size", "isotropic", 10.0, LGmix=1.0)
        phase.setSampleProfile(hist, "microstrain", "isotropic", 1.0, LGmix=1.0)
        phase.clear_HAP_refinements(
            {"Size": True, "Mustrain": True, "HStrain": True}, [hist]
        )


def main() -> None:
    for label, parameters in MODELS.items():
        output = ROOT / f"neutral_profile_{label}.gpx"
        project = G2sc.G2Project(str(BASE), newgpx=str(output))
        hist = project.histogram(0)
        neutralize_phase_widths(project)
        hist.clear_refinements(
            {"Instrument Parameters": ["U", "V", "W", "X", "Y", "Z"]}
        )
        for key in ("U", "V", "W", "X", "Y", "Z"):
            hist.InstrumentParameters[key][1] = 0.0
        for key, value in parameters.items():
            hist.InstrumentParameters[key][1] = value
        hist.set_refinements({"Instrument Parameters": list(parameters)})
        project.set_Controls("cycles", 14)
        try:
            project.refine(makeBack=False)
            project.save()
            replay = G2sc.G2Project(str(output))
            replay.set_Controls("cycles", 14)
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
