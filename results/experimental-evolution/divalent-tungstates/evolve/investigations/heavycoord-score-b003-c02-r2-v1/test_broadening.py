#!/usr/bin/env python3
"""Compare isotropic size and strain one phase at a time."""

from pathlib import Path

from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "post_texture_profile_UX.gpx"
PHASES = ["WO3_monoclinic", "Cu3WO6_cubic"]
TERMS = ["size", "strain"]


def main() -> None:
    for phase_name in PHASES:
        for term in TERMS:
            short = "WO3" if phase_name.startswith("WO3") else "Cu3WO6"
            output = ROOT / f"broadening_{short}_{term}.gpx"
            project = G2sc.G2Project(str(BASE), newgpx=str(output))
            hist = project.histogram(0)
            phase = project.phase(phase_name)
            if term == "size":
                phase.setSampleProfile(hist, "size", "isotropic", 1.0, LGmix=1.0)
                phase.set_HAP_refinements(
                    {"Size": {"type": "isotropic", "refine": True}}, [hist]
                )
            else:
                phase.setSampleProfile(
                    hist, "microstrain", "isotropic", 100.0, LGmix=1.0
                )
                phase.set_HAP_refinements(
                    {"Mustrain": {"type": "isotropic", "refine": True}}, [hist]
                )
            project.set_Controls("cycles", 10)
            try:
                project.refine(makeBack=False)
                project.save()
                hap = phase.getHAPvalues(hist)
                print(
                    short,
                    term,
                    "wR", hist.get_wR(),
                    "size", hap["Size"],
                    "strain", hap["Mustrain"],
                    "mass", hist.ComputeMassFracs(),
                )
            except Exception as exc:
                print(short, term, "FAILED", repr(exc))


if __name__ == "__main__":
    main()
