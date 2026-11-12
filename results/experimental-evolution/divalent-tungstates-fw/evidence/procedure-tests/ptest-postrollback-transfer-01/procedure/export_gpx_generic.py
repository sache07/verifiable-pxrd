#!/usr/bin/env python3
"""Export a GSAS-II project for researcher-only scorer diagnostics."""

from __future__ import annotations

import argparse
import json
import math
import re
from functools import reduce
from pathlib import Path

import numpy as np
from GSASII import GSASIIscriptable as G2


def element_symbol(label: str) -> str:
    match = re.match(r"([A-Z][a-z]?)", label)
    if not match:
        raise ValueError(f"Cannot parse element label {label!r}")
    return match.group(1)


def formula_for(phase) -> str:
    counts: dict[str, float] = {}
    for label, amount in phase.data["General"]["NoAtoms"].items():
        symbol = element_symbol(str(label))
        counts[symbol] = counts.get(symbol, 0.0) + float(amount)
    rounded = {key: int(round(value)) for key, value in counts.items()}
    if any(abs(counts[key] - rounded[key]) > 1e-5 for key in counts):
        raise ValueError(f"Nonintegral composition for {phase.name}: {counts}")
    divisor = reduce(math.gcd, rounded.values())
    reduced = {key: value // divisor for key, value in rounded.items()}
    order = sorted(reduced, key=lambda key: (key == "O", key))
    return "".join(key + (str(reduced[key]) if reduced[key] != 1 else "") for key in order)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    final_path = args.output / "final.gpx"
    G2.SetPrintLevel("warn")
    project = G2.G2Project(
        gpxfile=str(args.input.resolve()), newgpx=str(final_path.resolve())
    )
    histogram = project.histograms()[0]
    phases = [
        phase
        for phase in project.phases()
        if phase.data["Histograms"][histogram.name].get("Use", True)
    ]
    if len(phases) != len(project.phases()):
        raise RuntimeError("Remove disabled phases before generic export")
    project.data["Controls"]["data"]["parmFrozen"] = {"FrozenList": []}
    project.save()

    project = G2.G2Project(gpxfile=str(final_path.resolve()))
    histogram = project.histograms()[0]
    phases = project.phases()
    products = np.asarray(
        [
            phase.data["General"]["Mass"]
            * phase.data["Histograms"][histogram.name]["Scale"][0]
            for phase in phases
        ],
        dtype=float,
    )
    fractions = products / products.sum()

    rows = []
    for index, (phase, fraction) in enumerate(zip(phases, fractions)):
        cif_name = f"phase_{index}.cif"
        phase.export_CIF(str((args.output / cif_name).resolve()))
        rows.append(
            {
                "name": phase.name,
                "formula": formula_for(phase),
                "cif_path": cif_name,
                "weight_fraction": float(fraction),
                "weight_fraction_esd": None,
                "space_group": phase.data["General"]["SGData"]["SpGrp"].strip(),
                "cell": {key: float(value) for key, value in phase.get_cell().items()},
                "structural_source": "researcher diagnostic saved branch",
                "project_phase_index": index,
            }
        )

    arrays = np.asarray(histogram.data["data"][1], dtype=float)
    x, observed, _weights, calculated, _background, _difference = arrays
    np.savetxt(
        args.output / "fit.csv",
        np.column_stack([x, observed, calculated, observed - calculated]),
        delimiter=",",
        header="two_theta,observed,calculated,difference",
        comments="",
        fmt="%.10g",
    )
    rvals = project.data.get("Covariance", {}).get("data", {}).get("Rvals", {})
    residuals = histogram.residuals
    result = {
        "phases": rows,
        "fraction_normalization": "normalized over the modeled crystalline phases",
        "unresolved_components": [],
        "refinement_histogram": histogram.name,
        "fit_statistics": {
            "rwp_percent": float(rvals.get("Rwp", histogram.get_wR())),
            "rp_percent": float(residuals.get("R", np.nan)),
            "background_subtracted_rwp_percent": float(residuals.get("wRb", np.nan)),
            "minimum_expected_rwp_percent": float(residuals.get("wRmin", np.nan)),
            "goodness_of_fit": float(rvals.get("GOF", np.nan)),
            "chi_squared": float(rvals.get("chisq", np.nan)),
            "n_observations": int(rvals.get("Nobs", len(x))),
            "n_refined_parameters": int(rvals.get("Nvars", 0)),
            "converged": bool(rvals.get("converged", False)),
        },
        "profile_files": {
            "observed_calculated_difference": "fit.csv",
            "gsasii_project": "final.gpx",
        },
        "notes": ["Researcher-only saved-branch diagnostic."],
    }
    (args.output / "result.json").write_text(
        json.dumps(result, indent=2, allow_nan=False) + "\n"
    )


if __name__ == "__main__":
    main()
