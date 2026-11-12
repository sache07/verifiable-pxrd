#!/usr/bin/env python3
"""Refine once from the accepted checkpoint and build all final artifacts."""

import csv
import json

import numpy as np
from GSASII import GSASIIscriptable as G2sc


SOURCE = "transplanted-polished.gpx"
PROJECT = "final.gpx"

PHASE_OUTPUTS = {
    "ZnWO4_wolframite": ("ZnWO4 (wolframite)", "ZnWO4", "phase_ZnWO4.cif"),
    "ZnO": ("ZnO (wurtzite)", "ZnO", "phase_ZnO.cif"),
    "WO3_monoclinic_physical": ("WO3 (monoclinic gamma)", "WO3", "phase_WO3.cif"),
}


def main():
    G2sc.SetPrintLevel("warn")
    gpx = G2sc.G2Project(gpxfile=SOURCE)
    gpx.set_Controls("cycles", 50)
    gpx.data["Controls"]["data"]["min dM/M"] = 1.0e-6

    # The accepted helper endpoint already carries its converged covariance and
    # has all refinement flags disabled. Preserve that exact model for scoring.
    gpx.save(PROJECT)

    hist = gpx.histogram(0)
    covariance = gpx.data["Covariance"]["data"]
    rvals = covariance.get("Rvals", {})
    if not rvals.get("converged") or gpx.get_Frozen():
        raise RuntimeError(
            f"Final refinement is not stable: {rvals.get('converged')=}, "
            f"frozen={gpx.get_Frozen()}"
        )

    phase_fractions = hist.ComputeMassFracs()
    total = sum(value for value, _ in phase_fractions.values())
    phase_rows = []
    for phase in gpx.phases():
        display_name, formula, cif_path = PHASE_OUTPUTS[phase.name]
        phase.export_CIF(cif_path)
        value, esd = phase_fractions[phase.name]
        phase_rows.append(
            {
                "name": display_name,
                "project_phase_name": phase.name,
                "formula": formula,
                "space_group": phase.data["General"]["SGData"]["SpGrp"],
                "cif_path": cif_path,
                "weight_fraction": float(value / total),
                "weight_fraction_esd": float(esd / total),
            }
        )

    x, observed, weights, calculated, background, difference = [
        np.asarray(item, dtype=float) for item in hist.data["data"][1]
    ]
    if not np.allclose(difference, observed - calculated, rtol=0, atol=1.0e-10):
        raise RuntimeError("GSAS-II difference array is inconsistent")
    with open("fit.csv", "w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["two_theta", "observed", "calculated", "difference"])
        for row in zip(x, observed, calculated, difference):
            writer.writerow(
                [f"{row[0]:.8f}", f"{row[1]:.8f}", f"{row[2]:.10f}", f"{row[3]:.10f}"]
            )

    rp = 100.0 * float(np.sum(np.abs(observed - calculated)) / np.sum(observed))
    result = {
        "phases": phase_rows,
        "fraction_basis": "normalized over all modeled crystalline phases",
        "fit_statistics": {
            "Rwp_percent": float(rvals["Rwp"]),
            "Rp_percent": rp,
            "goodness_of_fit": float(rvals["GOF"]),
            "chi_squared": float(rvals["chisq"]),
            "n_observations": int(rvals["Nobs"]),
            "n_variables": int(rvals["Nvars"]),
            "converged": bool(rvals["converged"]),
            "maximum_shift_over_esd": float(rvals["Max shft/sig"]),
        },
        "fit_csv": "fit.csv",
        "gsas_project": PROJECT,
        "refinement_histogram": hist.name,
    }
    with open("result.json", "w") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")

    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
