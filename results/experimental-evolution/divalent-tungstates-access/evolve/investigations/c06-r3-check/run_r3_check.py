#!/usr/bin/env python3
"""Diagnostic: execute the previously unrun R-3 Mn3TeO6-derived branch."""

from __future__ import annotations

import json
from pathlib import Path

from GSASII import GSASIIscriptable as G2
from GSASII import GSASIIlattice as G2lat

from refine_controlled import ROOT, export_profile, run, set_bound
from refine_intensity_effects import AXES, clear_flags


def configure(project, phase, hist, initial_scale):
    for atom in phase.atoms():
        atom.data[atom.cia] = "I"
        atom.uiso = 0.005
        atom.refinement_flags = " "
    hap = phase.data["Histograms"][hist.name]
    hap["Scale"] = [float(initial_scale), True]
    hap["Size"][0] = "isotropic"
    hap["Size"][1][0] = 0.35
    hap["Size"][2] = [False, False, False]
    hap["Mustrain"][0] = "isotropic"
    hap["Mustrain"][1][0] = 5000.0
    hap["Mustrain"][2] = [False, False, False]
    hap["Pref.Ori."][:4] = ["MD", 1.0, False, [0, 0, 1]]
    set_bound(project, f"{phase.id}:0:Scale", 0.0, 2000.0)
    set_bound(project, f"{phase.id}:0:Size;i", 0.04, 1.5)
    set_bound(project, f"{phase.id}:0:Mustrain;i", 0.0, 8000.0)
    for index, value in enumerate(G2lat.cell2A(phase.data["General"]["Cell"][1:7])):
        if abs(value) >= 0.005:
            # The parent-to-target mismatch is anisotropic: the candidate's
            # c axis needs about 1.6% movement, outside the original 1.2% box.
            low, high = sorted((0.97 * value, 1.03 * value))
        else:
            low, high = value - 0.001, value + 0.001
        set_bound(project, f"{phase.id}::A{index}", low, high)


def disable_legacy_candidates(project, hist, keep):
    """Disable every phase after the two secure phases except ``keep``."""
    for legacy in project.phases()[2:]:
        if legacy.id == keep.id:
            continue
        hap = legacy.data["Histograms"][hist.name]
        hap["Scale"] = [0.0, False]
        hap["Use"] = False


def build_candidate(cif: Path, outdir: Path):
    source = ROOT / ".tmp" / "lattice_profile" / "model.gpx"
    project = G2.G2Project(gpxfile=str(source))
    hist = project.histograms()[0]
    active_legacy = [
        phase
        for phase in project.phases()[2:]
        if phase.data["Histograms"][hist.name].get("Use", True)
        and phase.data["Histograms"][hist.name]["Scale"][0] > 0
    ]
    if not active_legacy:
        raise RuntimeError("no active legacy candidate supplies a neutral initial mass scale")
    incumbent = active_legacy[-1]
    incumbent_hap = incumbent.data["Histograms"][hist.name]
    target_mass_scale = incumbent.data["General"]["Mass"] * incumbent_hap["Scale"][0]
    label = cif.stem
    phase = project.add_phase(
        str(cif), phasename=label, histograms=[hist], fmthint="CIF"
    )
    configure(project, phase, hist, target_mass_scale / phase.data["General"]["Mass"])
    clear_flags(project)
    disable_legacy_candidates(project, hist, phase)
    phase.set_HAP_refinements({"Scale": True})
    path = outdir / f"{label}_base.gpx"
    project.save(str(path))

    run(project, f"{label} scales", 18)
    phase.set_refinements({"Cell": True})
    project.set_Frozen()
    run(project, f"{label} cell", 22)
    phase.clear_refinements({"Cell": True})
    phase.set_HAP_refinements(
        {"Mustrain": {"type": "isotropic", "refine": True}}
    )
    project.set_Frozen()
    run(project, f"{label} strain", 20)
    phase.clear_HAP_refinements({"Mustrain": True})
    phase.set_HAP_refinements({"Size": {"type": "isotropic", "refine": True}})
    project.set_Frozen()
    run(project, f"{label} size", 20)
    phase.clear_HAP_refinements({"Size": True})
    hist.set_refinements({"Instrument Parameters": ["U", "W", "X", "SH/L"]})
    project.set_Frozen()
    run(project, f"{label} shared profile", 20)
    hist.clear_refinements({"Instrument Parameters": ["U", "W", "X", "SH/L"]})
    clear_flags(project)
    disable_legacy_candidates(project, hist, phase)
    project.save(str(path))
    project.set_Controls("cycles", 0)
    project.refine()
    project.save()
    return path, float(project.histograms()[0].get_wR())


def main() -> None:
    G2.SetPrintLevel("warn")
    outdir = ROOT / ".tmp" / "alternative_formulas"
    outdir.mkdir(parents=True, exist_ok=True)
    cifs = [ROOT / ".tmp" / "candidates" / "Mn3WO6_from_Mn3TeO6.cif"]
    records = []
    for cif in cifs:
        base_path, baseline = build_candidate(cif, outdir)
        trials = []
        for index, axis in enumerate(AXES):
            trial = G2.G2Project(gpxfile=str(base_path))
            clear_flags(trial)
            hist = trial.histograms()[0]
            phase = trial.phases()[-1]
            disable_legacy_candidates(trial, hist, phase)
            hap = phase.data["Histograms"][hist.name]
            hap["Pref.Ori."][:4] = ["MD", 1.0, False, list(axis)]
            phase.set_HAP_refinements({"Pref.Ori.": True})
            set_bound(trial, f"{phase.id}:0:MD", 0.7, 1.4)
            trial.set_Frozen()
            path = outdir / f"{cif.stem}_texture_{index}.gpx"
            trial.save(str(path))
            trial.set_Controls("cycles", 18)
            trial.refine()
            trial.save()
            trials.append(
                {
                    "axis": list(axis),
                    "ratio": float(hap["Pref.Ori."][1]),
                    "Rwp": float(hist.get_wR()),
                    "path": str(path),
                }
            )
        best = min(trials, key=lambda row: row["Rwp"])
        selected = Path(best["path"]) if baseline - best["Rwp"] > 0.015 else base_path
        final = G2.G2Project(gpxfile=str(selected))
        clear_flags(final)
        hist = final.histograms()[0]
        phase = final.phases()[-1]
        disable_legacy_candidates(final, hist, phase)
        out = outdir / f"{cif.stem}_final.gpx"
        final.save(str(out))
        record = {
            "candidate": cif.stem,
            "baseline_Rwp": baseline,
            "texture_trials": [
                {k: v for k, v in row.items() if k != "path"} for row in trials
            ],
            "final_Rwp": float(final.histograms()[0].get_wR()),
            "path": str(out),
        }
        records.append(record)
        print(json.dumps(record), flush=True)
    records.sort(key=lambda row: row["final_Rwp"])
    (outdir / "comparison.json").write_text(json.dumps(records, indent=2) + "\n")


if __name__ == "__main__":
    main()
