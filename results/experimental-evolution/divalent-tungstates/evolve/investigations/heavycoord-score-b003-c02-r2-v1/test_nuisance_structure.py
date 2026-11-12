#!/usr/bin/env python3
"""Test angular/profile corrections, intensity trends, and coordinate updates."""

from pathlib import Path

from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "after_size_profile_UX.gpx"


def set_physical_uiso(project: G2sc.G2Project) -> None:
    for phase in project.phases():
        for atom in phase.atoms():
            atom.uiso = 0.010 if atom.element == "O" else 0.005


def run(label: str, setup) -> None:
    output = ROOT / f"term_{label}.gpx"
    project = G2sc.G2Project(str(BASE), newgpx=str(output))
    hist = project.histogram(0)
    setup(project, hist)
    project.set_Controls("cycles", 12)
    try:
        project.refine(makeBack=False)
        project.save()
        print(
            label,
            "wR", hist.get_wR(),
            "mass", hist.ComputeMassFracs(),
            "zero", hist.InstrumentParameters["Zero"],
            "shift", hist.SampleParameters["Shift"],
            "shl", hist.InstrumentParameters["SH/L"],
            "polar", hist.InstrumentParameters["Polariz."],
            "rough", hist.SampleParameters["SurfRoughA"], hist.SampleParameters["SurfRoughB"],
        )
        for phase in project.phases():
            print(
                "  ", phase.name, phase.get_cell(),
                [(a.label, a.element, a.coordinates, a.uiso, a.refinement_flags) for a in phase.atoms()],
            )
    except Exception as exc:
        print(label, "FAILED", repr(exc))


def shift(project, hist) -> None:
    hist.clear_refinements({"Instrument Parameters": ["Zero"]})
    hist.InstrumentParameters["Zero"][1] = 0.0
    hist.SampleParameters["Shift"] = [-100.0, True]


def shl(project, hist) -> None:
    hist.InstrumentParameters["SH/L"][1] = 0.02
    hist.set_refinements({"Instrument Parameters": ["SH/L"]})


def polar(project, hist) -> None:
    hist.set_refinements({"Instrument Parameters": ["Polariz."]})


def rough(project, hist) -> None:
    hist.SampleParameters["SurfRoughA"] = [0.5, True]
    hist.SampleParameters["SurfRoughB"] = [0.05, True]


def uiso(project, hist) -> None:
    set_physical_uiso(project)


def coords_wo3(project, hist) -> None:
    set_physical_uiso(project)
    project.phase("WO3_monoclinic").set_refinements({"Atoms": {"all": "X"}})


def coords_cu3wo6(project, hist) -> None:
    set_physical_uiso(project)
    project.phase("Cu3WO6_cubic").set_refinements({"Atoms": {"all": "X"}})


def main() -> None:
    for label, setup in [
        ("shift", shift),
        ("shl", shl),
        ("polarization", polar),
        ("roughness", rough),
        ("uiso_fixed", uiso),
        ("coords_WO3", coords_wo3),
        ("coords_Cu3WO6", coords_cu3wo6),
    ]:
        run(label, setup)


if __name__ == "__main__":
    main()
