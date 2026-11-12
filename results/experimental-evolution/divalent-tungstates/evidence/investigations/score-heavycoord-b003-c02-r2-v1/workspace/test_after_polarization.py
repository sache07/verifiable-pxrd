#!/usr/bin/env python3
"""Re-challenge roughness and Cu3WO6 texture after polarization."""

from pathlib import Path

from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "baseline_polarization.gpx"


def replay(project: G2sc.G2Project, output: Path, label: str) -> None:
    project.set_Controls("cycles", 16)
    project.refine(makeBack=False)
    project.save()
    again = G2sc.G2Project(str(output))
    again.set_Controls("cycles", 16)
    again.refine(makeBack=False)
    again.save()
    hist = again.histogram(0)
    print(
        label,
        "wR", hist.get_wR(),
        "polar", hist.InstrumentParameters["Polariz."],
        "rough", hist.SampleParameters["SurfRoughA"], hist.SampleParameters["SurfRoughB"],
        "mass", hist.ComputeMassFracs(),
    )
    print("Cu3 PO", again.phase("Cu3WO6_cubic").getHAPvalues(hist)["Pref.Ori."])


def main() -> None:
    output = ROOT / "polar_term_roughness.gpx"
    project = G2sc.G2Project(str(BASE), newgpx=str(output))
    hist = project.histogram(0)
    hist.SampleParameters["SurfRoughA"] = [0.5, True]
    hist.SampleParameters["SurfRoughB"] = [0.05, True]
    replay(project, output, "roughness")

    for label, axis in (("100", [1, 0, 0]), ("110", [1, 1, 0]), ("111", [1, 1, 1])):
        output = ROOT / f"polar_texture_Cu3_{label}.gpx"
        project = G2sc.G2Project(str(BASE), newgpx=str(output))
        hist = project.histogram(0)
        po = project.phase("Cu3WO6_cubic").getHAPvalues(hist)["Pref.Ori."]
        po[0], po[1], po[2], po[3] = "MD", 0.95, True, axis
        replay(project, output, f"Cu3 texture {label}")


if __name__ == "__main__":
    main()
