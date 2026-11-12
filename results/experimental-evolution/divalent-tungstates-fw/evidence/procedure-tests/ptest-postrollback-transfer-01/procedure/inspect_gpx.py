#!/usr/bin/env python3
"""Print compact diagnostics from a saved GSAS-II powder project."""

from __future__ import annotations

import json
import sys

import numpy as np
from GSASII import GSASIIscriptable as G2


def main() -> None:
    project = G2.G2Project(gpxfile=sys.argv[1])
    hist = project.histogram(0)
    inst = hist.data["Instrument Parameters"][0]
    sample = hist.data["Sample Parameters"]
    output = {
        "histogram": hist.name,
        "instrument": {
            key: {"value": value[1], "refine": value[2]}
            for key, value in inst.items()
            if isinstance(value, list) and len(value) > 2
        },
        "sample": {
            key: (value[:2] if isinstance(value, list) else value)
            for key, value in sample.items()
        },
        "phases": {},
        "vary_list": [str(value) for value in (project.get_VaryList() or [])],
    }
    for phase in project.phases():
        hap = phase.data["Histograms"][hist.name]
        uiso = []
        for atom in phase.atoms():
            try:
                uiso.append(float(atom.uiso))
            except Exception:
                uiso.append(None)
        output["phases"][phase.name] = {
            "cell": phase.get_cell(),
            "scale": hap.get("Scale"),
            "size": hap.get("Size"),
            "mustrain": hap.get("Mustrain"),
            "preferred_orientation": hap.get("Pref.Ori."),
            "uiso": uiso,
            "atom_flags": [atom.refinement_flags for atom in phase.atoms()],
        }
    covariance = project.data.get("Covariance", {}).get("data", {})
    vary = [str(value) for value in covariance.get("varyList", [])]
    matrix = np.asarray(covariance.get("covMatrix", []), dtype=float)
    correlations = []
    if matrix.shape == (len(vary), len(vary)) and len(vary) > 1:
        sigma = np.sqrt(np.maximum(np.diag(matrix), 0.0))
        denominator = np.outer(sigma, sigma)
        with np.errstate(divide="ignore", invalid="ignore"):
            corr = np.where(denominator > 0, matrix / denominator, 0.0)
        for i in range(len(vary)):
            for j in range(i + 1, len(vary)):
                if abs(corr[i, j]) >= 0.9:
                    correlations.append({
                        "a": vary[i], "b": vary[j],
                        "correlation": float(corr[i, j]),
                    })
    output["high_correlations"] = sorted(
        correlations, key=lambda item: abs(item["correlation"]), reverse=True
    )
    output["frozen"] = project.data.get("Controls", {}).get("data", {}).get(
        "parmFrozen", {}
    )
    print(json.dumps(output, indent=2, default=str))


if __name__ == "__main__":
    main()
