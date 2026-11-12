#!/usr/bin/env python3
"""Diagnostic clean common-profile restart followed by sequential HAP tests.

Called as SCRIPT INPUT.gpx OUTPUT.gpx INPUTS_DIR. No phase identities, case
lookups, hidden values, or external references are used.
"""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import sys

import numpy as np
from GSASII import GSASIIscriptable as G2sc


def matching_histogram(project, inputs):
    observed = np.loadtxt(Path(inputs) / "pattern.csv", delimiter=",", skiprows=1)
    matches = []
    for hist in project.histograms():
        if not hist.name.startswith("PWDR"):
            continue
        x = np.asarray(hist.getdata("X"))
        y = np.asarray(hist.getdata("Yobs"))
        if (
            x.shape == observed[:, 0].shape
            and np.allclose(x, observed[:, 0], rtol=0, atol=1e-7)
            and np.allclose(y, observed[:, 1], rtol=0, atol=1e-5)
        ):
            matches.append(hist)
    if len(matches) != 1:
        raise ValueError(f"Expected one matching histogram, found {len(matches)}")
    return matches[0]


def bound(project, variable, low, high):
    project.set_Controls("parmMin", low, variable=variable)
    project.set_Controls("parmMax", high, variable=variable)


def common_setup(project, hist, initialize=False):
    inst = hist.data["Instrument Parameters"][0]
    sample = hist.data["Sample Parameters"]
    hist.set_refinements(
        {"Background": {"type": "chebyschev-1", "refine": True, "no. coeffs": 8}}
    )
    for key, entry in inst.items():
        if len(entry) >= 3:
            entry[2] = key in {"U", "W", "X", "SH/L"}
    for key in ("V", "Y", "Z"):
        inst[key][1] = 0.0
        inst[key][2] = False
    inst["Zero"][2] = False
    inst["Polariz."][2] = False
    if initialize:
        for key in ("U", "W", "X"):
            inst[key][1] = float(inst[key][0])
        inst["SH/L"][1] = 0.08

    sample["Scale"][1] = False
    sample["Shift"][1] = True
    sample["Transparency"][1] = False
    for key in ("SurfRoughA", "SurfRoughB"):
        sample[key][0] = 0.0
        sample[key][1] = False

    for variable, low, high in (
        (f":{hist.id}:U", 0.0, 250.0),
        (f":{hist.id}:W", 0.0, 250.0),
        (f":{hist.id}:X", 0.0, 40.0),
        (f":{hist.id}:SH/L", 0.002, 0.25),
        (f":{hist.id}:Shift", -2000.0, 2000.0),
    ):
        bound(project, variable, low, high)

    for phase in project.phases():
        phase.set_refinements({"Cell": True, "LeBail": False})
        phase.set_HAP_refinements({"Scale": True, "Pref.Ori.": False}, [hist])
        hap = phase.data["Histograms"][hist.name]
        hap["Pref.Ori."][1] = 1.0
        hap["Pref.Ori."][2] = False
        if initialize:
            hap["Size"][0] = "isotropic"
            hap["Size"][1][:] = [10.0, 1.0e6, 1.0]
            hap["Size"][2][:] = [False] * len(hap["Size"][2])
            hap["Size"][5][:] = [False] * len(hap["Size"][5])
            hap["Mustrain"][0] = "isotropic"
            hap["Mustrain"][1][:] = [0.0, 0.0, 1.0]
            hap["Mustrain"][2][:] = [False] * len(hap["Mustrain"][2])
            hap["Mustrain"][5][:] = [False] * len(hap["Mustrain"][5])
        bound(project, f"{phase.id}:{hist.id}:Size;i", 0.02, 20.0)
        bound(project, f"{phase.id}:{hist.id}:Mustrain;i", 0.0, 20000.0)

    project.set_Controls("cycles", 8)
    project.data["Controls"]["data"]["shift factor"] = 0.25
    project.data["Controls"]["data"]["parmFrozen"] = {"FrozenList": []}


def activate(project, hist, phase_name, mode, initialize):
    phase = project.phase(phase_name)
    hap = phase.data["Histograms"][hist.name]
    if mode == "size":
        hap["Size"][0] = "isotropic"
        if initialize:
            hap["Size"][1][0] = 0.2
        hap["Size"][2][0] = True
    else:
        hap["Mustrain"][0] = "isotropic"
        if initialize:
            hap["Mustrain"][1][0] = 1000.0
        hap["Mustrain"][2][0] = True


def refine(project, hist, label):
    for _ in range(3):
        project.refine(makeBack=False)
        rvals = project.data.get("Covariance", {}).get("data", {}).get("Rvals", {})
        if rvals.get("converged") and abs(rvals.get("Max shft/sig") or 0.0) < 0.5:
            break
    project.save()
    inst = hist.data["Instrument Parameters"][0]
    return {
        "label": label,
        "rwp_percent": float(hist.get_wR()),
        "profile": {key: float(inst[key][1]) for key in ("U", "W", "X", "SH/L")},
        "phases": {
            phase.name: {
                "size_um": float(phase.data["Histograms"][hist.name]["Size"][1][0]),
                "size_active": bool(phase.data["Histograms"][hist.name]["Size"][2][0]),
                "microstrain_ppm": float(
                    phase.data["Histograms"][hist.name]["Mustrain"][1][0]
                ),
                "strain_active": bool(
                    phase.data["Histograms"][hist.name]["Mustrain"][2][0]
                ),
            }
            for phase in project.phases()
        },
        "frozen": [
            str(item)
            for item in project.data["Controls"]["data"]
            .get("parmFrozen", {})
            .get("FrozenList", [])
        ],
    }


source, destination, inputs = map(Path, sys.argv[1:4])
work = destination.parent / "staged_candidates"
work.mkdir(exist_ok=True)
baseline = work / "baseline.gpx"
project = G2sc.G2Project(str(source), newgpx=str(baseline))
hist = matching_histogram(project, inputs)
common_setup(project, hist, initialize=True)
records = [refine(project, hist, "clean_common_baseline")]
current = baseline
current_rwp = records[-1]["rwp_percent"]
phase_names = [phase.name for phase in project.phases()]

for phase_index, phase_name in enumerate(phase_names):
    for mode in ("size", "strain"):
        candidate = work / f"p{phase_index}_{mode}.gpx"
        project = G2sc.G2Project(str(current), newgpx=str(candidate))
        hist = matching_histogram(project, inputs)
        common_setup(project, hist, initialize=False)
        activate(project, hist, phase_name, mode, initialize=True)
        row = refine(project, hist, f"{phase_name}:{mode}")

        # Require a fresh reopen/replay before accepting the branch.
        project = G2sc.G2Project(str(candidate))
        hist = matching_histogram(project, inputs)
        common_setup(project, hist, initialize=False)
        activate(project, hist, phase_name, mode, initialize=False)
        replay = refine(project, hist, f"{phase_name}:{mode}:fresh_replay")
        row["fresh_replay"] = replay
        records.append(row)
        if not replay["frozen"] and replay["rwp_percent"] + 1e-4 < current_rwp:
            current = candidate
            current_rwp = replay["rwp_percent"]

shutil.copyfile(current, destination)
(destination.parent / "staged_restart_diagnostics.json").write_text(
    json.dumps({"selected_rwp_percent": current_rwp, "trials": records}, indent=2) + "\n"
)
