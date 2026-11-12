#!/usr/bin/env python3
"""Diagnostic: enumerate a sharp-phase anchor for common/profile allocation.

Called as SCRIPT INPUT.gpx OUTPUT.gpx INPUTS_DIR. Inventory and structures are
unchanged. For each phase in turn, the common U/W/X/SH-L profile is rebuilt from
a narrow physical start while that phase has no sample broadening; isotropic
size and strain are released for every other phase. The lowest-Rwp converged
anchor is returned. No case identity, truth, or source lookup is used.
"""

from pathlib import Path
import json
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


def configure_candidate(project, hist, anchor_index):
    inst = hist.data["Instrument Parameters"][0]
    for key, value, active in (
        ("U", 10.0, True),
        ("V", 0.0, False),
        ("W", 5.0, True),
        ("X", 1.0, True),
        ("Y", 0.0, False),
        ("Z", 0.0, False),
        ("SH/L", 0.01, True),
    ):
        inst[key][0:2] = [value, value]
        inst[key][2] = active

    for key, low, high in (
        ("U", 0.0, 400.0),
        ("W", 0.1, 400.0),
        ("X", 0.0, 100.0),
        ("SH/L", 0.002, 0.1),
    ):
        project.set_Controls("parmMin", low, variable=f":{hist.id}:{key}")
        project.set_Controls("parmMax", high, variable=f":{hist.id}:{key}")

    for index, phase in enumerate(project.phases()):
        hap = phase.data["Histograms"][hist.name]
        hap["Size"][0] = "isotropic"
        hap["Size"][1][0] = 10.0 if index == anchor_index else 0.2
        hap["Size"][2][:] = [False] * len(hap["Size"][2])
        hap["Size"][5][:] = [False] * len(hap["Size"][5])
        hap["Size"][2][0] = index != anchor_index

        hap["Mustrain"][0] = "isotropic"
        hap["Mustrain"][1][0] = 0.0 if index == anchor_index else 500.0
        hap["Mustrain"][2][:] = [False] * len(hap["Mustrain"][2])
        hap["Mustrain"][5][:] = [False] * len(hap["Mustrain"][5])
        hap["Mustrain"][2][0] = index != anchor_index

        project.set_Controls(
            "parmMin", 0.02, variable=f"{phase.id}:{hist.id}:Size;i"
        )
        project.set_Controls(
            "parmMax", 10.0, variable=f"{phase.id}:{hist.id}:Size;i"
        )
        project.set_Controls(
            "parmMin", 0.0, variable=f"{phase.id}:{hist.id}:Mustrain;i"
        )
        project.set_Controls(
            "parmMax", 30000.0, variable=f"{phase.id}:{hist.id}:Mustrain;i"
        )

    project.set_Controls("cycles", 20)
    project.set_Frozen()


def summarize(project, hist, anchor_index):
    inst = hist.data["Instrument Parameters"][0]
    phases = []
    for phase in project.phases():
        hap = phase.data["Histograms"][hist.name]
        phases.append(
            {
                "name": phase.name,
                "size_um": float(hap["Size"][1][0]),
                "size_active": bool(hap["Size"][2][0]),
                "microstrain_ppm": float(hap["Mustrain"][1][0]),
                "microstrain_active": bool(hap["Mustrain"][2][0]),
            }
        )
    return {
        "anchor_index": anchor_index,
        "anchor_name": project.phases()[anchor_index].name,
        "rwp_percent": float(hist.residuals["wR"]),
        "profile": {
            key: float(inst[key][1])
            for key in ("U", "V", "W", "X", "Y", "Z", "SH/L")
        },
        "phases": phases,
    }


source, destination, inputs = map(Path, sys.argv[1:4])
candidate_dir = destination.parent / "anchor_candidates"
candidate_dir.mkdir(exist_ok=True)
probe = G2sc.G2Project(str(source))
phase_count = len(probe.phases())
if phase_count < 1:
    raise ValueError("No phases in source project")

records = []
paths = []
for anchor_index in range(phase_count):
    candidate = candidate_dir / f"anchor_{anchor_index}.gpx"
    project = G2sc.G2Project(str(source), newgpx=str(candidate))
    hist = matching_histogram(project, inputs)
    configure_candidate(project, hist, anchor_index)
    for _ in range(3):
        project.refine(makeBack=False)
    project.save()
    records.append(summarize(project, hist, anchor_index))
    paths.append(candidate)

best_index = min(range(phase_count), key=lambda i: records[i]["rwp_percent"])
shutil.copyfile(paths[best_index], destination)
(destination.parent / "anchor_diagnostics.json").write_text(
    json.dumps({"selected": best_index, "candidates": records}, indent=2) + "\n"
)
