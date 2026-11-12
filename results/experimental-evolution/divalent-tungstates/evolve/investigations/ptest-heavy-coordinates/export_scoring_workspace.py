#!/usr/bin/env python3
"""Synchronize CIFs, fractions, result.json and fit.csv from final.gpx."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np
from GSASII import GSASIIscriptable as G2sc


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: export_scoring_workspace.py WORKSPACE")
    root = Path(sys.argv[1]).resolve()
    result_path = root / "result.json"
    result = json.loads(result_path.read_text())
    project = G2sc.G2Project(str(root / "final.gpx"))
    histogram = project.histogram(0)
    phases = project.phases()
    submitted = result["phases"]
    if len(phases) != len(submitted):
        raise RuntimeError("project/result phase-count mismatch")

    fractions = histogram.ComputeMassFracs()
    for phase, record in zip(phases, submitted):
        cif_path = root / record["cif_path"]
        phase.export_CIF(str(cif_path))
        value, esd = fractions[phase.name]
        record["weight_fraction"] = float(value)
        for key in (
            "weight_fraction_esd",
            "weight_fraction_formal_esd",
            "weight_fraction_esd_statistical",
        ):
            if key in record:
                record[key] = float(esd)
        record["space_group"] = phase.data["General"]["SGData"]["SpGrp"].strip()
        if "cell" in record:
            cell = phase.get_cell()
            for key in record["cell"]:
                if key in cell:
                    record["cell"][key] = float(cell[key])
        for key, suffix in (
            ("bragg_R_percent", "Rf"),
            ("bragg_R_F2_percent", "Rf^2"),
        ):
            if key in record:
                record[key] = float(histogram.residuals[f"{phase.id}:0:{suffix}"])

    data = np.asarray(histogram.data["data"][1], dtype=float)
    x, observed, _weight, calculated, background, _stored_difference = data
    lower, upper = (float(value) for value in histogram.data["Limits"][1])
    first = int(np.searchsorted(x, lower))
    last = int(np.searchsorted(x, upper)) + 1
    use = slice(first, last)
    with (root / "fit.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(
            ["two_theta_deg", "observed", "calculated", "difference", "background"]
        )
        writer.writerows(
            (
                f"{xx:.8f}",
                f"{yo:.8f}",
                f"{yc:.8f}",
                f"{yo - yc:.8f}",
                f"{yb:.8f}",
            )
            for xx, yo, yc, yb in zip(
                x[use], observed[use], calculated[use], background[use]
            )
        )

    covariance = project.data["Covariance"]["data"]
    rvals = covariance["Rvals"]
    stats = result.setdefault("fit_statistics", {})
    updates = {
        "Rwp_percent": float(histogram.residuals["wR"]),
        "Rp_percent": float(histogram.residuals["R"]),
        "Rexp_percent": float(histogram.residuals["wRmin"]),
        "R_expected_percent": float(histogram.residuals["wRmin"]),
        "R_background_percent": float(histogram.residuals["Rb"]),
        "weighted_R_background_percent": float(histogram.residuals["wRb"]),
        "goodness_of_fit": float(rvals["GOF"]),
        "GOF": float(rvals["GOF"]),
        "chi_squared": float(rvals["chisq"]),
        "chi_square": float(rvals["chisq"]),
        "reduced_chi_squared": float(rvals["GOF"] ** 2),
        "n_observations": int(rvals["Nobs"]),
        "N_observations": int(rvals["Nobs"]),
        "n_refined_parameters": int(rvals["Nvars"]),
        "N_variables": int(rvals["Nvars"]),
        "profile_rows": int(last - first),
        "two_theta_fit_range_deg": [lower, upper],
        "converged": bool(rvals.get("converged", True)),
    }
    for key, value in updates.items():
        if key in stats or key in {"Rwp_percent", "Rp_percent", "goodness_of_fit"}:
            stats[key] = value
    for key in ("profile_path", "fit_path"):
        if key in result:
            result[key] = "fit.csv"
    for key in ("gsas_project_path", "project_path"):
        if key in result:
            result[key] = "final.gpx"
    result_path.write_text(json.dumps(result, indent=2) + "\n")
    print(
        json.dumps(
            {
                "Rwp": histogram.residuals["wR"],
                "fractions": fractions,
                "phases": [phase.name for phase in phases],
            },
            indent=2,
            default=float,
        )
    )


if __name__ == "__main__":
    main()
