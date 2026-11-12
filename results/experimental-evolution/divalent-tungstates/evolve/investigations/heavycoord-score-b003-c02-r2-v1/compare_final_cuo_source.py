#!/usr/bin/env python3
"""Compare the 196 K CuO record under the provisional final nuisance model."""

from pathlib import Path

from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "polar_texture_CuO_010.gpx"
OUTPUT = ROOT / "polar_final_cuo_source_196K.gpx"
COD_CIF = Path(
    "<HOME>/.local/share/characterizagent/backends/dara/"
    "cod-filtered-2024/cif/9/01/60/9016057.cif"
)


def remove_phase(project: G2sc.G2Project, name: str) -> None:
    del project.data["Phases"][name]
    for entry in project.names:
        if entry and entry[0] == "Phases" and name in entry:
            entry.remove(name)
    for hist in project.histograms():
        hist.data["Reflection Lists"].pop(name, None)
    project.update_ids()


def main() -> None:
    project = G2sc.G2Project(str(BASE), newgpx=str(OUTPUT))
    hist = project.histogram(0)
    remove_phase(project, "CuO_ambient_1011194")
    phase = project.add_phase(
        str(COD_CIF),
        phasename="CuO_196K_9016057",
        histograms=[hist],
        fmthint="CIF",
    )
    phase.HAPvalue("Scale", 16.0, [hist])
    phase.set_refinements({"Cell": True})
    phase.setSampleProfile(hist, "size", "isotropic", 10.0, LGmix=1.0)
    phase.setSampleProfile(hist, "microstrain", "isotropic", 5800.0, LGmix=1.0)
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
    phase.set_HAP_refinements(
        {"Scale": True, "Mustrain": {"type": "isotropic", "refine": True}},
        [hist],
    )
    po = phase.getHAPvalues(hist)["Pref.Ori."]
    po[0], po[1], po[2], po[3] = "MD", 1.13, True, [0, 1, 0]
    project.set_Controls("cycles", 16)
    project.refine(makeBack=False)
    project.save()
    replay = G2sc.G2Project(str(OUTPUT))
    replay.set_Controls("cycles", 16)
    replay.refine(makeBack=False)
    replay.save()
    rhist = replay.histogram(0)
    rphase = replay.phase("CuO_196K_9016057")
    print(
        "wR", rhist.get_wR(),
        "mass", rhist.ComputeMassFracs(),
        "cell", rphase.get_cell(),
        "HAP", rphase.getHAPvalues(rhist),
    )


if __name__ == "__main__":
    main()
