#!/usr/bin/env python3
"""Diagnostic multi-start restart of profile allocation after inventory freeze.

Called as SCRIPT INPUT.gpx OUTPUT.gpx INPUTS_DIR.  The procedure uses only the
submitted project and public pattern.  It neutralizes intensity surrogates,
restarts a compact common profile, and challenges isotropic broadening on every
retained phase.  This is intentionally an investigation, not a shipped helper.
"""

from __future__ import annotations

import json
import math
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


def set_bound(project, variable, lower, upper):
    project.set_Controls("parmMin", lower, variable=variable)
    project.set_Controls("parmMax", upper, variable=variable)


def configure(project, hist, mode, shl_seed, size_seed, initialize):
    inst = hist.data["Instrument Parameters"][0]
    sample = hist.data["Sample Parameters"]

    hist.set_refinements(
        {
            "Background": {
                "type": "chebyschev-1",
                "refine": True,
                "no. coeffs": 8,
            }
        }
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
        # The first element is the generic starting value supplied with the
        # solver's project, not a hidden or fitted value.
        for key in ("U", "W", "X"):
            inst[key][1] = float(inst[key][0])
        inst["SH/L"][1] = shl_seed

    sample["Scale"][1] = False
    sample["Shift"][1] = True
    sample["Transparency"][1] = False
    for key in ("SurfRoughA", "SurfRoughB"):
        sample[key][0] = 0.0
        sample[key][1] = False

    set_bound(project, f":{hist.id}:U", 0.0, 250.0)
    set_bound(project, f":{hist.id}:W", 0.0, 250.0)
    set_bound(project, f":{hist.id}:X", 0.0, 40.0)
    set_bound(project, f":{hist.id}:SH/L", 0.002, 0.25)
    set_bound(project, f":{hist.id}:Shift", -2000.0, 2000.0)

    for phase in project.phases():
        phase.set_refinements({"Cell": True, "LeBail": False})
        phase.set_HAP_refinements({"Scale": True, "Pref.Ori.": False}, [hist])
        hap = phase.data["Histograms"][hist.name]
        po = hap["Pref.Ori."]
        po[1] = 1.0
        po[2] = False

        hap["Size"][0] = "isotropic"
        hap["Mustrain"][0] = "isotropic"
        if initialize:
            hap["Size"][1][:] = [size_seed, 1.0e6, 1.0]
            hap["Mustrain"][1][:] = [1000.0, 0.0, 1.0]
        hap["Size"][2][:] = [False] * len(hap["Size"][2])
        hap["Size"][5][:] = [False] * len(hap["Size"][5])
        hap["Mustrain"][2][:] = [False] * len(hap["Mustrain"][2])
        hap["Mustrain"][5][:] = [False] * len(hap["Mustrain"][5])
        hap["Size"][2][0] = True
        hap["Mustrain"][2][0] = mode == "size_strain"

        set_bound(project, f"{phase.id}:{hist.id}:Size;i", 0.02, 20.0)
        set_bound(project, f"{phase.id}:{hist.id}:Mustrain;i", 0.0, 20000.0)

    project.set_Controls("cycles", 12)
    project.set_Controls("shift factor", 0.25)
    project.data["Controls"]["data"]["parmFrozen"] = {"FrozenList": []}


def snapshot(project, hist, label):
    inst = hist.data["Instrument Parameters"][0]
    covariance = project.data.get("Covariance", {}).get("data", {})
    rvals = covariance.get("Rvals", {})
    phases = []
    for phase in project.phases():
        hap = phase.data["Histograms"][hist.name]
        phases.append(
            {
                "name": phase.name,
                "size_um": float(hap["Size"][1][0]),
                "microstrain_ppm": float(hap["Mustrain"][1][0]),
            }
        )
    return {
        "label": label,
        "rwp_percent": float(hist.get_wR()),
        "converged": bool(rvals.get("converged", False)),
        "max_shift_over_su": rvals.get("Max shft/sig"),
        "profile": {
            key: float(inst[key][1])
            for key in ("U", "V", "W", "X", "Y", "Z", "SH/L")
        },
        "shift_um": float(hist.data["Sample Parameters"]["Shift"][0]),
        "phases": phases,
        "frozen": [
            str(item)
            for item in project.data["Controls"]["data"]
            .get("parmFrozen", {})
            .get("FrozenList", [])
        ],
    }


source, destination, inputs = map(Path, sys.argv[1:4])
candidate_dir = destination.parent / "restart_candidates"
candidate_dir.mkdir(exist_ok=True)
records = []

for mode in ("size", "size_strain"):
    for shl_seed in (0.02, 0.08):
        for size_seed in (0.15, 0.8):
            label = f"{mode}_shl{shl_seed:.2f}_size{size_seed:.2f}"
            candidate = candidate_dir / f"{label}.gpx"
            try:
                project = G2sc.G2Project(str(source), newgpx=str(candidate))
                hist = matching_histogram(project, inputs)
                configure(project, hist, mode, shl_seed, size_seed, True)
                for _ in range(4):
                    project.refine(makeBack=False)
                    covariance = project.data.get("Covariance", {}).get("data", {})
                    rvals = covariance.get("Rvals", {})
                    if rvals.get("converged") and abs(rvals.get("Max shft/sig") or 0) < 0.5:
                        break
                project.save()

                # Selection uses a fresh native replay, not the stored fit.
                project = G2sc.G2Project(str(candidate))
                hist = matching_histogram(project, inputs)
                configure(project, hist, mode, shl_seed, size_seed, False)
                project.refine(makeBack=False)
                project.save()
                row = snapshot(project, hist, label)
                row["path"] = str(candidate)
                records.append(row)
            except Exception as exc:
                records.append({"label": label, "error": repr(exc)})

valid = [
    row
    for row in records
    if "rwp_percent" in row and math.isfinite(row["rwp_percent"])
]
if not valid:
    raise RuntimeError(f"No valid restart candidate: {records}")

best = min(valid, key=lambda row: (bool(row["frozen"]), row["rwp_percent"]))
shutil.copyfile(best["path"], destination)
(destination.parent / "restart_diagnostics.json").write_text(
    json.dumps({"selected": best["label"], "candidates": records}, indent=2) + "\n"
)
