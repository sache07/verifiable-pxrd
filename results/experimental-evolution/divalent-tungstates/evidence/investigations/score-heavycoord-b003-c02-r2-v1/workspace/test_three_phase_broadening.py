#!/usr/bin/env python3
"""Compare isotropic size and strain from a neutral three-phase baseline."""

from pathlib import Path

from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "neutral_profile_UWX.gpx"
PHASES = ["Cu3WO6_cubic", "WO3_2311041", "CuO_ambient_1011194"]


def short_name(name: str) -> str:
    if name.startswith("Cu3"):
        return "Cu3WO6"
    if name.startswith("WO3"):
        return "WO3"
    return "CuO"


def main() -> None:
    for phase_name in PHASES:
        for term in ("size", "strain"):
            short = short_name(phase_name)
            output = ROOT / f"three_phase_broadening_{short}_{term}.gpx"
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
                    short,
                    term,
                    "wR", rhist.get_wR(),
                    "size", rhap["Size"],
                    "strain", rhap["Mustrain"],
                    "mass", rhist.ComputeMassFracs(),
                )
            except Exception as exc:
                print(short, term, "FAILED", repr(exc))


if __name__ == "__main__":
    main()
