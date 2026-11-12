#!/usr/bin/env python3
"""Replay profile and complementary broadening trials after Cu3WO6 size."""

from pathlib import Path

from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "broadening_Cu3WO6_size.gpx"


def refine(project: G2sc.G2Project, output: Path) -> None:
    project.filename = str(output)
    project.set_Controls("cycles", 10)
    project.refine(makeBack=False)
    project.save()


def profile_trials() -> None:
    models = {
        "X": {"X": 13.0},
        "UX": {"U": 40.0, "X": 13.0},
        "WX": {"W": 5.0, "X": 13.0},
        "UWX": {"U": 30.0, "W": 2.0, "X": 13.0},
    }
    for label, parameters in models.items():
        output = ROOT / f"after_size_profile_{label}.gpx"
        project = G2sc.G2Project(str(BASE), newgpx=str(output))
        hist = project.histogram(0)
        hist.clear_refinements(
            {"Instrument Parameters": ["U", "V", "W", "X", "Y", "Z"]}
        )
        for key in ["U", "V", "W", "X", "Y", "Z"]:
            hist.InstrumentParameters[key][1] = 0.0
        for key, value in parameters.items():
            hist.InstrumentParameters[key][1] = value
        hist.set_refinements({"Instrument Parameters": list(parameters)})
        refine(project, output)
        print(
            "profile", label,
            "wR", hist.get_wR(),
            {key: hist.InstrumentParameters[key][1] for key in parameters},
            hist.ComputeMassFracs(),
        )


def extra_term(phase_name: str, term: str) -> None:
    short = "WO3" if phase_name.startswith("WO3") else "Cu3WO6"
    output = ROOT / f"after_size_{short}_{term}.gpx"
    project = G2sc.G2Project(str(BASE), newgpx=str(output))
    hist = project.histogram(0)
    phase = project.phase(phase_name)
    if term == "size":
        phase.setSampleProfile(hist, "size", "isotropic", 1.0, LGmix=1.0)
        phase.set_HAP_refinements(
            {"Size": {"type": "isotropic", "refine": True}}, [hist]
        )
    else:
        phase.setSampleProfile(hist, "microstrain", "isotropic", 100.0, LGmix=1.0)
        phase.set_HAP_refinements(
            {"Mustrain": {"type": "isotropic", "refine": True}}, [hist]
        )
    refine(project, output)
    hap = phase.getHAPvalues(hist)
    print(
        "extra", short, term,
        "wR", hist.get_wR(),
        "size", hap["Size"],
        "strain", hap["Mustrain"],
        hist.ComputeMassFracs(),
    )


def main() -> None:
    profile_trials()
    extra_term("WO3_monoclinic", "size")
    extra_term("WO3_monoclinic", "strain")
    extra_term("Cu3WO6_cubic", "strain")


if __name__ == "__main__":
    main()
