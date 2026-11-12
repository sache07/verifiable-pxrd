#!/usr/bin/env python3
"""Diagnostic: neutralize fixed GSAS-II default phase broadening only.

Called as SCRIPT INPUT.gpx OUTPUT.gpx INPUTS_DIR. The inventory, structures,
active profile terms and refinement flags are preserved. A fixed isotropic
size of exactly 1 micrometre is changed to 10 micrometres, and a fixed
isotropic strain of exactly 1000 ppm is changed to zero; these are the active
GSAS-II import defaults that two v7 reports mistakenly described as pruned.
"""

from pathlib import Path
import json
import math
import sys

import numpy as np
from GSASII import GSASIIscriptable as G2sc


def matching_histogram(project, inputs):
    observed = np.loadtxt(Path(inputs) / "pattern.csv", delimiter=",", skiprows=1)
    matches = []
    for histogram in project.histograms():
        if not histogram.name.startswith("PWDR"):
            continue
        x = np.asarray(histogram.getdata("X"))
        y = np.asarray(histogram.getdata("Yobs"))
        if (
            x.shape == observed[:, 0].shape
            and np.allclose(x, observed[:, 0], rtol=0, atol=1e-7)
            and np.allclose(y, observed[:, 1], rtol=0, atol=1e-5)
        ):
            matches.append(histogram)
    if len(matches) != 1:
        raise ValueError(f"Expected one matching histogram, found {len(matches)}")
    return matches[0]


def state(project, histogram):
    rows = []
    for phase in project.phases():
        if histogram.name not in phase.data.get("Histograms", {}):
            continue
        hap = phase.data["Histograms"][histogram.name]
        rows.append(
            {
                "phase": phase.name,
                "size_type": hap["Size"][0],
                "size_values": [float(value) for value in hap["Size"][1]],
                "size_flags": [bool(value) for value in hap["Size"][2]],
                "size_generalized_flags": [bool(value) for value in hap["Size"][5]],
                "strain_type": hap["Mustrain"][0],
                "strain_values": [float(value) for value in hap["Mustrain"][1]],
                "strain_flags": [bool(value) for value in hap["Mustrain"][2]],
                "strain_generalized_flags": [bool(value) for value in hap["Mustrain"][5]],
            }
        )
    return rows


def main():
    source, destination, inputs = map(Path, sys.argv[1:4])
    project = G2sc.G2Project(str(source), newgpx=str(destination))
    histogram = matching_histogram(project, inputs)
    before = state(project, histogram)
    changes = []

    for phase in project.phases():
        if histogram.name not in phase.data.get("Histograms", {}):
            continue
        hap = phase.data["Histograms"][histogram.name]

        size_inactive = not any(hap["Size"][2]) and not any(hap["Size"][5])
        if (
            size_inactive
            and hap["Size"][0] == "isotropic"
            and math.isclose(float(hap["Size"][1][0]), 1.0, abs_tol=1e-9)
        ):
            hap["Size"][1][:] = [10.0, 1.0e6, 1.0]
            changes.append({"phase": phase.name, "term": "Size", "from": 1.0, "to": 10.0})

        strain_inactive = not any(hap["Mustrain"][2]) and not any(
            hap["Mustrain"][5]
        )
        if (
            strain_inactive
            and hap["Mustrain"][0] == "isotropic"
            and math.isclose(
                float(hap["Mustrain"][1][0]), 1000.0, abs_tol=1e-7
            )
        ):
            hap["Mustrain"][1][:] = [0.0, 0.0, 1.0]
            changes.append(
                {"phase": phase.name, "term": "Mustrain", "from": 1000.0, "to": 0.0}
            )

    if not changes:
        raise ValueError("No fixed 1 micrometre/1000 ppm GSAS-II defaults found")

    project.data["Controls"]["data"].update(
        {"max cyc": 20, "min dM/M": 0.0001, "parmFrozen": {"FrozenList": []}}
    )
    project.set_Frozen()
    history = []
    for iteration in range(1, 6):
        project.refine(makeBack=False)
        histogram = matching_histogram(project, inputs)
        covariance = project.data["Covariance"]["data"].get("Rvals", {})
        row = {
            "iteration": iteration,
            "rwp_percent": float(histogram.get_wR()),
            "max_shift_over_esd": covariance.get("Max shft/sig"),
            "converged": covariance.get("converged"),
        }
        history.append(row)
        if (
            row["converged"]
            and row["max_shift_over_esd"] is not None
            and row["max_shift_over_esd"] < 0.2
        ):
            break

    project.save()
    histogram = matching_histogram(project, inputs)
    diagnostics = {
        "changes": changes,
        "before": before,
        "after": state(project, histogram),
        "history": history,
    }
    (destination.parent / "neutral_hap_diagnostics.json").write_text(
        json.dumps(diagnostics, indent=2) + "\n"
    )


if __name__ == "__main__":
    main()
