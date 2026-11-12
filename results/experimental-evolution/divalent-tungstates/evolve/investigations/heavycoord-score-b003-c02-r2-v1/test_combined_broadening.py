#!/usr/bin/env python3
"""Test complementary strain terms after accepting Cu3WO6 size."""

from pathlib import Path

from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "three_phase_broadening_Cu3WO6_size.gpx"
TRIALS = {
    "Cu3WO6_strain": "Cu3WO6_cubic",
    "CuO_strain": "CuO_ambient_1011194",
    "WO3_strain": "WO3_2311041",
}


def main() -> None:
    for label, phase_name in TRIALS.items():
        output = ROOT / f"combined_{label}.gpx"
        project = G2sc.G2Project(str(BASE), newgpx=str(output))
        hist = project.histogram(0)
        phase = project.phase(phase_name)
        phase.setSampleProfile(hist, "microstrain", "isotropic", 100.0, LGmix=1.0)
        phase.set_HAP_refinements(
            {"Mustrain": {"type": "isotropic", "refine": True}}, [hist]
        )
        project.set_Controls("cycles", 14)
        try:
            project.refine(makeBack=False)
            project.save()
            replay = G2sc.G2Project(str(output))
            replay.set_Controls("cycles", 14)
            replay.refine(makeBack=False)
            replay.save()
            rhist = replay.histogram(0)
            rhap = replay.phase(phase_name).getHAPvalues(rhist)
            print(
                label,
                "wR", rhist.get_wR(),
                "size", rhap["Size"],
                "strain", rhap["Mustrain"],
                "mass", rhist.ComputeMassFracs(),
            )
        except Exception as exc:
            print(label, "FAILED", repr(exc))


if __name__ == "__main__":
    main()
