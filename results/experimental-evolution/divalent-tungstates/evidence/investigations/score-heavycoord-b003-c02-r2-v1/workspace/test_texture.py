#!/usr/bin/env python3
"""Challenge low-index preferred-orientation axes under a common profile."""

from pathlib import Path

from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
AXES = {
    "100": [1, 0, 0],
    "010": [0, 1, 0],
    "001": [0, 0, 1],
    "110": [1, 1, 0],
    "101": [1, 0, 1],
    "011": [0, 1, 1],
    "111": [1, 1, 1],
}


def main() -> None:
    for label, axis in AXES.items():
        output = ROOT / f"texture_WO3_{label}.gpx"
        project = G2sc.G2Project(str(ROOT / "profile_UX.gpx"), newgpx=str(output))
        hist = project.histogram(0)
        phase = project.phase("WO3_monoclinic")
        hap = phase.getHAPvalues(hist)
        hap["Pref.Ori."][0] = "MD"
        hap["Pref.Ori."][1] = 1.0
        hap["Pref.Ori."][2] = True
        hap["Pref.Ori."][3] = axis
        project.set_Controls("cycles", 10)
        try:
            project.refine(makeBack=False)
            project.save()
            po = phase.getHAPvalues(hist)["Pref.Ori."]
            print(
                label,
                "wR", hist.get_wR(),
                "MD", po[1],
                "axis", po[3],
                "mass", hist.ComputeMassFracs(),
            )
        except Exception as exc:
            print(label, "FAILED", repr(exc))


if __name__ == "__main__":
    main()
