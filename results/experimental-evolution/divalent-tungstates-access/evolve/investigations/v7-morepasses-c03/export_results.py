#!/usr/bin/env python3
"""Export diagnostic files from the exact five-pass helper endpoint."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np
from GSASII import GSASIIscriptable as G2


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT / "final.gpx"
REFERENCE_IDS = {
    "CuWO4": "COD 4000806",
    "WO3": "COD 2311041",
    "CuO": "COD 1011194",
    "Cu3WO6": "COD 1527404",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    before = sha256(PROJECT)
    G2.SetPrintLevel("warn")
    project = G2.G2Project(gpxfile=str(PROJECT))
    hist = project.histogram(0)

    x, observed, weights, calculated, background, difference = (
        np.asarray(item, dtype=float) for item in hist.data["data"][1][:6]
    )
    public = np.loadtxt(ROOT / "inputs" / "pattern.csv", delimiter=",", skiprows=1)
    if public.shape != (len(x), 2):
        raise RuntimeError("project and public pattern have different sizes")
    if not np.allclose(x, public[:, 0], atol=1e-8, rtol=0):
        raise RuntimeError("project and public two-theta grids differ")
    if not np.allclose(observed, public[:, 1], atol=1e-8, rtol=0):
        raise RuntimeError("project and public observed intensities differ")
    # Write the public grid/observations verbatim and the saved GSAS calculation.
    with (ROOT / "fit.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["two_theta", "observed", "calculated", "difference"])
        for xx, yy, yc in zip(public[:, 0], public[:, 1], calculated):
            writer.writerow([f"{xx:.8f}", f"{yy:.1f}", f"{yc:.10g}", f"{yy-yc:.10g}"])

    mass_fractions = hist.ComputeMassFracs()
    phase_rows = []
    for phase in project.phases():
        filename = f"{phase.name}.cif"
        phase.export_CIF(str(ROOT / filename))
        fraction, formal_esd = mass_fractions[phase.name]
        general = phase.data["General"]
        phase_rows.append({
            "name": phase.name,
            "cif_path": filename,
            "weight_fraction": float(fraction),
            "weight_fraction_formal_esd": float(formal_esd),
            "space_group": str(general["SGData"]["SpGrp"]).strip(),
            "reference_structure": REFERENCE_IDS[phase.name],
            "model_status": (
                "phase identity, lattice, and bounded coordinates refined; the selected "
                "phasewise branch met the five-pass convergence and physicality gates"
            ),
        })

    rvals = project.data["Covariance"]["data"]["Rvals"]
    use = weights > 0
    rp = 100.0 * np.sum(np.abs(observed[use] - calculated[use])) / np.sum(np.abs(observed[use]))
    rwp_direct = 100.0 * np.sqrt(
        np.sum(weights[use] * (observed[use] - calculated[use]) ** 2)
        / np.sum(weights[use] * observed[use] ** 2)
    )
    gof = float(rvals["GOF"])
    result = {
        "project_path": "final.gpx",
        "fit_profile_path": "fit.csv",
        "crystalline_weight_fraction_basis": (
            "normalized over the four modeled crystalline phases; no amorphous fraction determined"
        ),
        "phases": phase_rows,
        "fit_statistics": {
            "Rwp_percent": float(hist.get_wR()),
            "Rwp_percent_direct_check": float(rwp_direct),
            "Rp_percent": float(rp),
            "Rexp_percent": float(hist.get_wR() / gof),
            "goodness_of_fit": gof,
            "reduced_chi_square": float(gof * gof),
            "chi_square": float(rvals["chisq"]),
            "observations": int(rvals["Nobs"]),
            "variables_in_last_cycle": int(rvals["Nvars"]),
            "converged": bool(rvals["converged"]),
            "maximum_shift_over_esd": float(rvals["Max shft/sig"]),
            "two_theta_range_deg": [float(x[0]), float(x[-1])],
        },
        "calibration": {
            "zero_deg": float(hist.InstrumentParameters["Zero"][1]),
            "specimen_displacement_micrometers": float(hist.SampleParameters["Shift"][0]),
        },
        "uncertainty_note": (
            "Reported fraction esds are covariance-only formal values. Systematic uncertainty from "
            "reference-coordinate/profile correlation is larger, especially for minor CuO."
        ),
    }
    (ROOT / "result.json").write_text(json.dumps(result, indent=2) + "\n")

    after = sha256(PROJECT)
    if before != after:
        raise RuntimeError("export changed final.gpx")
    print(json.dumps({
        "project_sha256": after,
        "fit_statistics": result["fit_statistics"],
        "fractions": {row["name"]: row["weight_fraction"] for row in phase_rows},
    }))


if __name__ == "__main__":
    main()
