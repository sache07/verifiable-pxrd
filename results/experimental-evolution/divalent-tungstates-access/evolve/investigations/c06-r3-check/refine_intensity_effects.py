#!/usr/bin/env python3
"""Refine angle-dependent intensity terms, then screen MD texture axes."""

from __future__ import annotations

import json
from pathlib import Path

from GSASII import GSASIIscriptable as G2

from refine_controlled import ROOT, export_profile, run, set_bound, state


AXES = ([0, 0, 1], [1, 0, 0], [0, 1, 0], [1, 1, 0], [1, 1, 1])


def clear_flags(project: G2.G2Project) -> None:
    hist = project.histograms()[0]
    hist.clear_refinements(
        {"Instrument Parameters": ["Zero", "U", "W", "X", "SH/L", "Polariz."]}
    )
    hist.clear_refinements({"Sample Parameters": ["Shift", "SurfRoughA", "SurfRoughB"]})
    for phase in project.phases():
        phase.clear_refinements({"Cell": True, "Atoms": [a.label for a in phase.atoms()]})
        phase.clear_HAP_refinements(
            {"Size": True, "Mustrain": True, "Pref.Ori.": True}
        )
        phase.set_HAP_refinements({"Scale": True})
    project.set_Frozen()


def main() -> None:
    source = ROOT / ".tmp" / "controlled" / "model.gpx"
    outdir = ROOT / ".tmp" / "intensity"
    outdir.mkdir(parents=True, exist_ok=True)
    project = G2.G2Project(gpxfile=str(source))
    project.save(str(outdir / "base.gpx"))
    clear_flags(project)

    hist = project.histograms()[0]
    hist.set_refinements({"Instrument Parameters": ["Polariz."]})
    run(project, "polarization", 15)
    hist.clear_refinements({"Instrument Parameters": ["Polariz."]})

    # Generator convention is one common isotropic Uiso per phase. Refine the
    # three common values, not independent atom ADPs.
    for phase in project.phases():
        phase.set_refinements({"Atoms": {"all": "U"}})
        project.add_EquivConstr(
            tuple(f"{phase.id}::AUiso:{i}" for i, _ in enumerate(phase.atoms()))
        )
        set_bound(project, f"{phase.id}::AUiso:0", 0.003, 0.020)
    run(project, "phase-common Uiso", 18)
    for phase in project.phases():
        phase.clear_refinements({"Atoms": [a.label for a in phase.atoms()]})
    project.save(str(outdir / "texture_base.gpx"))

    choices = []
    current = outdir / "texture_base.gpx"
    for phase_index in range(3):
        baseline_project = G2.G2Project(gpxfile=str(current))
        clear_flags(baseline_project)
        baseline_project.set_Controls("cycles", 0)
        baseline_project.refine()
        baseline = float(baseline_project.histograms()[0].get_wR())
        trials = [{"axis": None, "Rwp": baseline, "ratio": 1.0, "path": str(current)}]
        for axis_index, axis in enumerate(AXES):
            trial = G2.G2Project(gpxfile=str(current))
            clear_flags(trial)
            phase = trial.phases()[phase_index]
            hap = phase.data["Histograms"][trial.histograms()[0].name]
            hap["Pref.Ori."][0] = "MD"
            hap["Pref.Ori."][1] = 1.0
            hap["Pref.Ori."][3] = list(axis)
            phase.set_HAP_refinements({"Pref.Ori.": True})
            set_bound(trial, f"{phase.id}:0:MD", 0.7, 1.4)
            path = outdir / f"texture_p{phase_index}_a{axis_index}.gpx"
            trial.save(str(path))
            trial.set_Controls("cycles", 15)
            trial.refine()
            ratio = phase.data["Histograms"][trial.histograms()[0].name]["Pref.Ori."][1]
            trials.append(
                {
                    "axis": list(axis),
                    "Rwp": float(trial.histograms()[0].get_wR()),
                    "ratio": float(ratio),
                    "path": str(path),
                }
            )
        trials.sort(key=lambda row: row["Rwp"])
        best = trials[0]
        # Retain texture only when it gives a reproducible material reduction;
        # infinitesimal improvements around ratio=1 are just another variable.
        if best["axis"] is not None and baseline - best["Rwp"] > 0.015:
            selected = G2.G2Project(gpxfile=best["path"])
            selected.save(str(outdir / f"selected_p{phase_index}.gpx"))
            current = outdir / f"selected_p{phase_index}.gpx"
        else:
            best = next(row for row in trials if row["axis"] is None)
        choices.append(
            {
                "phase": baseline_project.phases()[phase_index].name,
                "baseline_Rwp": baseline,
                "trials": [{k: v for k, v in row.items() if k != "path"} for row in trials],
                "selected": {k: v for k, v in best.items() if k != "path"},
            }
        )
        print(json.dumps(choices[-1]), flush=True)

    final = G2.G2Project(gpxfile=str(current))
    clear_flags(final)
    final.save(str(outdir / "model.gpx"))
    final.set_Controls("cycles", 0)
    final.refine()
    final.save()
    state(final, "selected intensity effects")
    export_profile(final)
    (outdir / "texture_trials.json").write_text(json.dumps(choices, indent=2) + "\n")


if __name__ == "__main__":
    main()
