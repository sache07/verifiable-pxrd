#!/usr/bin/env python3
"""Check replay-stable interactions among accepted width/texture terms."""

from pathlib import Path

from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "texture_Cu3_110.gpx"


def replay_and_report(project: G2sc.G2Project, output: Path, label: str) -> None:
    project.set_Controls("cycles", 14)
    project.refine(makeBack=False)
    project.save()
    replay = G2sc.G2Project(str(output))
    replay.set_Controls("cycles", 14)
    replay.refine(makeBack=False)
    replay.save()
    hist = replay.histogram(0)
    print(label, "wR", hist.get_wR(), "mass", hist.ComputeMassFracs())
    for name in ("Cu3WO6_cubic", "CuO_ambient_1011194"):
        hap = replay.phase(name).getHAPvalues(hist)
        print(name, "size", hap["Size"], "strain", hap["Mustrain"], "PO", hap["Pref.Ori."])


def main() -> None:
    # Is Cu3WO6 anisotropic size still supported after [110] texture?
    output = ROOT / "interaction_Cu3_isotropic_size.gpx"
    project = G2sc.G2Project(str(BASE), newgpx=str(output))
    hist = project.histogram(0)
    phase = project.phase("Cu3WO6_cubic")
    phase.setSampleProfile(hist, "size", "isotropic", 0.165, LGmix=1.0)
    phase.set_HAP_refinements(
        {"Size": {"type": "isotropic", "refine": True}}, [hist]
    )
    replay_and_report(project, output, "Cu3 isotropic size")

    # Is CuO strain still supported after Cu3WO6 texture?
    output = ROOT / "interaction_no_CuO_strain.gpx"
    project = G2sc.G2Project(str(BASE), newgpx=str(output))
    hist = project.histogram(0)
    phase = project.phase("CuO_ambient_1011194")
    phase.setSampleProfile(hist, "microstrain", "isotropic", 1.0, LGmix=1.0)
    phase.clear_HAP_refinements({"Mustrain": True}, [hist])
    replay_and_report(project, output, "no CuO strain")

    # Re-challenge the two competing CuO texture axes under the accepted
    # Cu3WO6 texture model.
    for label, axis in (("010", [0, 1, 0]), ("110", [1, 1, 0])):
        output = ROOT / f"interaction_CuO_texture_{label}.gpx"
        project = G2sc.G2Project(str(BASE), newgpx=str(output))
        hist = project.histogram(0)
        phase = project.phase("CuO_ambient_1011194")
        po = phase.getHAPvalues(hist)["Pref.Ori."]
        po[0], po[1], po[2], po[3] = "MD", 1.05, True, axis
        replay_and_report(project, output, f"CuO texture {label}")


if __name__ == "__main__":
    main()
