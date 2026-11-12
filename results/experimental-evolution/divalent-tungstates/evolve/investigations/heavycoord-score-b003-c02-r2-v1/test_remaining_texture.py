#!/usr/bin/env python3
"""Challenge symmetry-distinct texture axes for Cu3WO6 and CuO."""

from pathlib import Path

from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "cu3_size_axis_110.gpx"
TRIALS = {
    "Cu3_100": ("Cu3WO6_cubic", [1, 0, 0]),
    "Cu3_110": ("Cu3WO6_cubic", [1, 1, 0]),
    "Cu3_111": ("Cu3WO6_cubic", [1, 1, 1]),
    "CuO_100": ("CuO_ambient_1011194", [1, 0, 0]),
    "CuO_010": ("CuO_ambient_1011194", [0, 1, 0]),
    "CuO_001": ("CuO_ambient_1011194", [0, 0, 1]),
    "CuO_101": ("CuO_ambient_1011194", [1, 0, 1]),
    "CuO_10m1": ("CuO_ambient_1011194", [1, 0, -1]),
    "CuO_110": ("CuO_ambient_1011194", [1, 1, 0]),
    "CuO_011": ("CuO_ambient_1011194", [0, 1, 1]),
    "CuO_111": ("CuO_ambient_1011194", [1, 1, 1]),
}


def main() -> None:
    for label, (phase_name, axis) in TRIALS.items():
        output = ROOT / f"texture_{label}.gpx"
        project = G2sc.G2Project(str(BASE), newgpx=str(output))
        hist = project.histogram(0)
        phase = project.phase(phase_name)
        po = phase.getHAPvalues(hist)["Pref.Ori."]
        po[0], po[1], po[2], po[3] = "MD", 0.95, True, axis
        project.set_Controls("cycles", 14)
        try:
            project.refine(makeBack=False)
            project.save()
            replay = G2sc.G2Project(str(output))
            replay.set_Controls("cycles", 14)
            replay.refine(makeBack=False)
            replay.save()
            rhist = replay.histogram(0)
            rphase = replay.phase(phase_name)
            print(
                label,
                "wR", rhist.get_wR(),
                "PO", rphase.getHAPvalues(rhist)["Pref.Ori."],
                "mass", rhist.ComputeMassFracs(),
            )
        except Exception as exc:
            print(label, "FAILED", repr(exc))


if __name__ == "__main__":
    main()
