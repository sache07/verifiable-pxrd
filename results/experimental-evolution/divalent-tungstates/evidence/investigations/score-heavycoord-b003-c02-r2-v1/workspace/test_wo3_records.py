#!/usr/bin/env python3
"""Compare physical WO3 records under the accepted common nuisance model."""

from pathlib import Path

from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
COD_ROOT = Path(
    "<HOME>/.local/share/characterizagent/backends/dara/cod-filtered-2024/cif"
)
BASE = ROOT / "after_size_profile_UX.gpx"
RECORDS = {
    # 1966 neutron monoclinic model; [10-1] is equivalent to [001] in the
    # P21/n setting used in the initial room-temperature record.
    "2311041": [1, 0, -1],
    # 1978 single-crystal triclinic WO3 model.
    "2106293": [0, 0, 1],
}


def cod_path(cod_id: str) -> Path:
    return COD_ROOT / cod_id[0] / cod_id[1:3] / cod_id[3:5] / f"{cod_id}.cif"


def remove_phase(project: G2sc.G2Project, name: str) -> None:
    del project.data["Phases"][name]
    for entry in project.names:
        if entry and entry[0] == "Phases" and name in entry:
            entry.remove(name)
    for hist in project.histograms():
        hist.data["Reflection Lists"].pop(name, None)
    project.update_ids()


def main() -> None:
    for cod_id, axis in RECORDS.items():
        output = ROOT / f"wo3_record_{cod_id}.gpx"
        project = G2sc.G2Project(str(BASE), newgpx=str(output))
        hist = project.histogram(0)
        remove_phase(project, "WO3_monoclinic")
        phase = project.add_phase(
            str(cod_path(cod_id)),
            phasename=f"WO3_{cod_id}",
            histograms=[hist],
            fmthint="CIF",
        )
        phase.HAPvalue("Scale", 18.0, [hist])
        phase.set_refinements({"Cell": True})
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
        po = phase.getHAPvalues(hist)["Pref.Ori."]
        po[0], po[1], po[2], po[3] = "MD", 0.72, True, axis
        project.set_Controls("cycles", 14)
        try:
            project.refine(makeBack=False)
            project.save()
            print(
                cod_id,
                "wR", hist.get_wR(),
                "cell", phase.get_cell(),
                "PO", phase.getHAPvalues(hist)["Pref.Ori."],
                "mass", hist.ComputeMassFracs(),
            )
        except Exception as exc:
            print(cod_id, "FAILED", repr(exc))


if __name__ == "__main__":
    main()
