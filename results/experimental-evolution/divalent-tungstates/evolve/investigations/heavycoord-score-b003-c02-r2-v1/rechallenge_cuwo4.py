#!/usr/bin/env python3
"""Re-challenge ambient CuWO4 after establishing the three-phase profile."""

from pathlib import Path

from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "polar_texture_CuO_010.gpx"
OUTPUT = ROOT / "polar_final_watch_CuWO4.gpx"


def main() -> None:
    project = G2sc.G2Project(str(BASE), newgpx=str(OUTPUT))
    hist = project.histogram(0)
    phase = project.add_phase(
        str(ROOT / "candidates" / "cuwo4_ambient_prototype.cif"),
        phasename="CuWO4_ambient_prototype",
        histograms=[hist],
        fmthint="CIF",
    )
    phase.HAPvalue("Scale", 0.3, [hist])
    phase.setSampleProfile(hist, "size", "isotropic", 10.0, LGmix=1.0)
    phase.setSampleProfile(hist, "microstrain", "isotropic", 1.0, LGmix=1.0)
    phase.clear_HAP_refinements(
        {
            "Size": True,
            "Mustrain": True,
            "HStrain": True,
            "Pref.Ori.": True,
            "Babinet": ["BabA", "BabU"],
            "Extinction": True,
        },
        [hist],
    )
    phase.set_HAP_refinements({"Scale": True}, [hist])
    project.set_Controls("cycles", 14)
    project.refine(makeBack=False)
    project.save()
    replay = G2sc.G2Project(str(OUTPUT))
    replay.set_Controls("cycles", 14)
    replay.refine(makeBack=False)
    replay.save()
    rhist = replay.histogram(0)
    rphase = replay.phase("CuWO4_ambient_prototype")
    print(
        "wR", rhist.get_wR(),
        "scale", rphase.HAPvalue("Scale"),
        "cell", rphase.get_cell(),
        "mass", rhist.ComputeMassFracs(),
    )


if __name__ == "__main__":
    main()
