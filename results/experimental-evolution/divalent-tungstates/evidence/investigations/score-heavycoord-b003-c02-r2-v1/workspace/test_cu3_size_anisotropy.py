#!/usr/bin/env python3
"""Challenge isotropic Cu3WO6 size broadening along cubic directions."""

from pathlib import Path

from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "combined_CuO_strain.gpx"
AXES = {"100": [1, 0, 0], "110": [1, 1, 0], "111": [1, 1, 1]}


def main() -> None:
    for label, axis in AXES.items():
        output = ROOT / f"cu3_size_axis_{label}.gpx"
        project = G2sc.G2Project(str(BASE), newgpx=str(output))
        hist = project.histogram(0)
        phase = project.phase("Cu3WO6_cubic")
        phase.setSampleProfile(
            hist, "size", "uniaxial", 0.165, 0.165, axis, LGmix=1.0
        )
        phase.set_HAP_refinements(
            {"Size": {"type": "uniaxial", "refine": True}}, [hist]
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
            hap = replay.phase("Cu3WO6_cubic").getHAPvalues(rhist)
            print(
                label,
                "wR", rhist.get_wR(),
                "size", hap["Size"],
                "mass", rhist.ComputeMassFracs(),
            )
        except Exception as exc:
            print(label, "FAILED", repr(exc))


if __name__ == "__main__":
    main()
