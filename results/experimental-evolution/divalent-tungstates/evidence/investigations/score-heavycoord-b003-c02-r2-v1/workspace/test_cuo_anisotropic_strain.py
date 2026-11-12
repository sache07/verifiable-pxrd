#!/usr/bin/env python3
"""Challenge isotropic CuO strain with low-parameter uniaxial models."""

from pathlib import Path

from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "three_phase_broadening_Cu3WO6_size.gpx"
AXES = {
    "100": [1, 0, 0],
    "010": [0, 1, 0],
    "001": [0, 0, 1],
    "101": [1, 0, 1],
    "10m1": [1, 0, -1],
    "110": [1, 1, 0],
    "011": [0, 1, 1],
    "111": [1, 1, 1],
}


def main() -> None:
    for label, axis in AXES.items():
        output = ROOT / f"cuo_strain_axis_{label}.gpx"
        project = G2sc.G2Project(str(BASE), newgpx=str(output))
        hist = project.histogram(0)
        phase = project.phase("CuO_ambient_1011194")
        phase.setSampleProfile(
            hist, "microstrain", "uniaxial", 5670.0, 5670.0, axis, LGmix=1.0
        )
        phase.set_HAP_refinements(
            {"Mustrain": {"type": "uniaxial", "refine": True}}, [hist]
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
            hap = replay.phase("CuO_ambient_1011194").getHAPvalues(rhist)
            print(
                label,
                "wR", rhist.get_wR(),
                "strain", hap["Mustrain"],
                "mass", rhist.ComputeMassFracs(),
            )
        except Exception as exc:
            print(label, "FAILED", repr(exc))


if __name__ == "__main__":
    main()
