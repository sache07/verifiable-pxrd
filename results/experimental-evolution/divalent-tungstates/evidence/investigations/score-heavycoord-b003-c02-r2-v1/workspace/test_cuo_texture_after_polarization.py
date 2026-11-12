#!/usr/bin/env python3
"""Re-challenge CuO texture after polarization and Cu3WO6 texture."""

from pathlib import Path

from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "polar_texture_Cu3_110.gpx"
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
        output = ROOT / f"polar_texture_CuO_{label}.gpx"
        project = G2sc.G2Project(str(BASE), newgpx=str(output))
        hist = project.histogram(0)
        phase = project.phase("CuO_ambient_1011194")
        po = phase.getHAPvalues(hist)["Pref.Ori."]
        po[0], po[1], po[2], po[3] = "MD", 1.05, True, axis
        project.set_Controls("cycles", 16)
        try:
            project.refine(makeBack=False)
            project.save()
            replay = G2sc.G2Project(str(output))
            replay.set_Controls("cycles", 16)
            replay.refine(makeBack=False)
            replay.save()
            rhist = replay.histogram(0)
            print(
                label,
                "wR", rhist.get_wR(),
                "PO", replay.phase("CuO_ambient_1011194").getHAPvalues(rhist)["Pref.Ori."],
                "polar", rhist.InstrumentParameters["Polariz."],
                "mass", rhist.ComputeMassFracs(),
            )
        except Exception as exc:
            print(label, "FAILED", repr(exc))


if __name__ == "__main__":
    main()
