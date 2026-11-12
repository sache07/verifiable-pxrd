#!/usr/bin/env python3
"""Replay the selected model and export all requested machine-readable files."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "polar_texture_CuO_010.gpx"
FINAL = ROOT / "final.gpx"
FIT = ROOT / "fit.csv"
RESULT = ROOT / "result.json"

PHASE_INFO = {
    "Cu3WO6_cubic": {
        "name": "Cu3WO6",
        "formula": "Cu3WO6",
        "space_group_number": 205,
        "source": "COD 1527404",
        "cif": ROOT / "phase_Cu3WO6.cif",
    },
    "WO3_2311041": {
        "name": "WO3",
        "formula": "WO3",
        "space_group_number": 14,
        "source": "COD 2311041",
        "cif": ROOT / "phase_WO3.cif",
    },
    "CuO_ambient_1011194": {
        "name": "CuO",
        "formula": "CuO",
        "space_group_number": 15,
        "source": "COD 1011194",
        "cif": ROOT / "phase_CuO.cif",
    },
}


def replay() -> G2sc.G2Project:
    project = G2sc.G2Project(str(SOURCE), newgpx=str(FINAL))
    project.set_Controls("cycles", 16)
    project.refine(makeBack=False)
    project.save()
    reopened = G2sc.G2Project(str(FINAL))
    reopened.set_Controls("cycles", 16)
    reopened.refine(makeBack=False)
    reopened.save()
    return G2sc.G2Project(str(FINAL))


def export_fit(hist: G2sc.G2PwdrData) -> int:
    values = np.asarray(hist.data["data"][1], dtype=float)
    two_theta, observed, _weight, calculated, background, _difference = values
    lower = float(hist.data["Limits"][1][0])
    upper = float(hist.data["Limits"][1][1])
    # GSAS-II uses the first grid point beyond the nominal upper limit in its
    # profile slice. Reproduce those exact indices so fit.csv has Nobs rows.
    first = int(np.searchsorted(two_theta, lower))
    last = int(np.searchsorted(two_theta, upper)) + 1
    use = slice(first, last)
    with FIT.open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(
            [
                "two_theta_deg",
                "observed",
                "calculated",
                "difference",
                "background",
            ]
        )
        for x, yo, yc, yb in zip(two_theta[use], observed[use], calculated[use], background[use]):
            writer.writerow(
                [f"{x:.8f}", f"{yo:.8f}", f"{yc:.8f}", f"{yo-yc:.8f}", f"{yb:.8f}"]
            )
    return int(last - first)


def export_result(project: G2sc.G2Project, n_profile_rows: int) -> None:
    hist = project.histogram(0)
    fractions = hist.ComputeMassFracs()
    cov = project.data["Covariance"]["data"]
    rvals = cov["Rvals"]
    phases = []
    for phase in project.phases():
        info = PHASE_INFO[phase.name]
        fraction, esd = fractions[phase.name]
        sg = phase.data["General"]["SGData"]
        phases.append(
            {
                "name": info["name"],
                "formula": info["formula"],
                "space_group": sg["SpGrp"].strip(),
                "space_group_number": info["space_group_number"],
                "source_structure": info["source"],
                "cif_path": info["cif"].name,
                "weight_fraction": float(fraction),
                "weight_fraction_formal_esd": float(esd),
                "cell": {key: float(value) for key, value in phase.get_cell().items()},
                "bragg_R_percent": float(hist.residuals[f"{phase.id}:0:Rf"]),
                "bragg_R_F2_percent": float(hist.residuals[f"{phase.id}:0:Rf^2"]),
            }
        )
    result = {
        "normalization": "modeled crystalline phases only; fractions sum to 1",
        "phases": phases,
        "fit_statistics": {
            "Rwp_percent": float(hist.residuals["wR"]),
            "Rp_percent": float(hist.residuals["R"]),
            "R_background_percent": float(hist.residuals["Rb"]),
            "weighted_R_background_percent": float(hist.residuals["wRb"]),
            "R_expected_percent": float(hist.residuals["wRmin"]),
            "goodness_of_fit": float(rvals["GOF"]),
            "chi_square": float(rvals["chisq"]),
            "durbin_watson": float(hist.data["data"][0]["Durbin-Watson"]),
            "N_observations": int(rvals["Nobs"]),
            "N_variables": int(rvals["Nvars"]),
            "profile_rows": n_profile_rows,
            "two_theta_fit_range_deg": [
                float(hist.data["Limits"][1][0]),
                float(hist.data["Limits"][1][1]),
            ],
        },
        "weighting": "sigma=sqrt(max(raw_count,1)); no pointwise uncertainties were supplied",
        "project_path": FINAL.name,
        "fit_path": FIT.name,
        "watch_list": [
            {
                "name": "CuWO4",
                "status": "not included; trace scale not reliable",
                "trial_weight_fraction": 0.00109,
                "trial_weight_fraction_formal_esd": 0.00051,
            }
        ],
    }
    RESULT.write_text(json.dumps(result, indent=2) + "\n")


def main() -> None:
    project = replay()
    hist = project.histogram(0)
    for phase in project.phases():
        phase.export_CIF(str(PHASE_INFO[phase.name]["cif"]))
    nrows = export_fit(hist)
    export_result(project, nrows)
    print("final wR", hist.get_wR())
    print("mass fractions", hist.ComputeMassFracs())
    print("fit rows", nrows)


if __name__ == "__main__":
    main()
