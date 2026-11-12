#!/usr/bin/env python3
"""Rebuild and replay the three-phase model for alternate CuO records."""

from pathlib import Path

from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
MODELS = {
    "ambient": ("watch_CuO_ambient_1011194.gpx", "CuO_ambient_1011194"),
    "196K": ("watch_CuO_196K_9016057.gpx", "CuO_196K_9016057"),
}


def summarize(project: G2sc.G2Project, label: str) -> None:
    hist = project.histogram(0)
    print(label, "wR", hist.get_wR(), "mass", hist.ComputeMassFracs())
    print(
        "profile",
        {
            key: hist.InstrumentParameters[key][1]
            for key in ("U", "V", "W", "X", "Y", "Z", "Zero")
        },
    )
    for phase in project.phases():
        hap = phase.getHAPvalues(hist)
        print(
            phase.name,
            "cell", phase.get_cell(),
            "scale", hap["Scale"],
            "size", hap["Size"],
            "strain", hap["Mustrain"],
            "PO", hap["Pref.Ori."],
        )


def main() -> None:
    for label, (source_name, cuo_name) in MODELS.items():
        output = ROOT / f"three_phase_CuO_{label}.gpx"
        project = G2sc.G2Project(str(ROOT / source_name), newgpx=str(output))
        # After changing the inventory, reconverge the background, all scales,
        # one angular correction, every cell and the accepted common U/X
        # profile. Existing flags for these terms are retained from the base.
        for phase in project.phases():
            phase.set_refinements({"Cell": True})
        project.phase(cuo_name).set_HAP_refinements(
            {"Scale": True}, [project.histogram(0)]
        )
        project.set_Controls("cycles", 14)
        project.refine(makeBack=False)
        project.save()

        # Reopen and replay to catch any transient or nonpersistent solution.
        replay = G2sc.G2Project(str(output))
        replay.set_Controls("cycles", 14)
        replay.refine(makeBack=False)
        replay.save()
        summarize(replay, label)


if __name__ == "__main__":
    main()
