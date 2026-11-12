#!/usr/bin/env python3
"""Test a size-dominant profile decomposition after a structural rollback.

Called as: size_dominant_restart.py INPUT.gpx OUTPUT.gpx INPUTS_DIR

Atomic coordinates and already-active phase-size models are preserved. When
one or more phases lack active size broadening, the procedure compares the
stabilized project with a small grid in which missing isotropic sizes replace
part of the correlated common Lorentzian-width subspace. Starts are derived
only from the saved project; no case or generator values are used.
"""

from __future__ import annotations

import json
import math
import shutil
import sys
from pathlib import Path

import numpy as np
from GSASII import GSASIIscriptable as G2


G2.SetPrintLevel("warn")


def prepare(project: G2.G2Project) -> None:
    project.set_Controls("cycles", 24)
    project.data["Controls"]["data"]["shift factor"] = 0.25
    project.data["Controls"]["data"]["parmFrozen"] = {"FrozenList": []}
    for phase in project.phases():
        for atom in phase.atoms():
            atom.refinement_flags = (
                atom.refinement_flags.replace("X", "").replace("U", "")
            )


def phase_fractions(project: G2.G2Project) -> list[float]:
    histogram = project.histograms()[0]
    products = np.asarray(
        [
            phase.data["General"]["Mass"]
            * phase.data["Histograms"][histogram.name]["Scale"][0]
            for phase in project.phases()
        ],
        dtype=float,
    )
    return (products / products.sum()).tolist()


def metrics(project: G2.G2Project) -> dict:
    histogram = project.histograms()[0]
    covariance = project.data.get("Covariance", {}).get("data", {})
    fit = covariance.get("Rvals", {})
    arrays = np.asarray(histogram.data["data"][1], dtype=float)
    return {
        "rwp": float(histogram.get_wR()),
        "parameters": len(covariance.get("varyList", [])),
        "n": int(arrays.shape[1]),
        "fractions": phase_fractions(project),
        "converged": bool(fit.get("converged", False)),
        "max_shift_over_sigma": float(fit.get("Max shft/sig", math.inf)),
    }


def physical(project: G2.G2Project) -> tuple[bool, str]:
    histogram = project.histograms()[0]
    fit = project.data.get("Covariance", {}).get("data", {}).get("Rvals", {})
    if not fit.get("converged", False):
        return False, "not_converged"
    if float(fit.get("Max shft/sig", math.inf)) > 1.0:
        return False, "nonstationary"

    arrays = np.asarray(histogram.data["data"][1], dtype=float)
    x, _observed, _weight, calculated = arrays[:4]
    if np.any(~np.isfinite(calculated)) or np.any(calculated < 0):
        return False, "nonfinite_or_negative_profile"

    instrument = histogram.data["Instrument Parameters"][0]
    theta = np.deg2rad(x / 2.0)
    tangent = np.tan(theta)
    gaussian = (
        float(instrument["U"][1]) * tangent**2
        + float(instrument["V"][1]) * tangent
        + float(instrument["W"][1])
    )
    lorentzian = (
        float(instrument["X"][1]) / np.cos(theta)
        + float(instrument["Y"][1]) * tangent
        + float(instrument["Z"][1])
    )
    if np.min(gaussian) <= 0 or np.min(lorentzian) < 0:
        return False, "nonpositive_analytic_width"

    frozen = project.data.get("Controls", {}).get("data", {}).get("parmFrozen", {})
    if frozen.get("FrozenList"):
        return False, "frozen_variables"

    sample = histogram.data["Sample Parameters"]
    for key in ("SurfRoughA", "SurfRoughB"):
        value = float(sample[key][0])
        if not 0 <= value < 5:
            return False, f"roughness_outside_physical_domain:{key}"

    for phase in project.phases():
        hap = phase.data["Histograms"][histogram.name]
        if not hap.get("Use", True) or float(hap["Scale"][0]) <= 0:
            return False, "nonpositive_or_disabled_phase"
        for value, active in zip(hap["Size"][1], hap["Size"][2]):
            if active and not 1e-4 < float(value) < 100:
                return False, "size_at_physical_bound"
        for value, active in zip(hap["Mustrain"][1], hap["Mustrain"][2]):
            if active and not 0 < float(value) < 50000:
                return False, "strain_at_physical_bound"
    return True, "pass"


def delta_aic(old: dict, new: dict) -> float:
    if old["rwp"] <= 0 or new["rwp"] <= 0:
        return math.inf
    return (
        old["n"] * math.log((new["rwp"] / old["rwp"]) ** 2)
        + 2 * (new["parameters"] - old["parameters"])
    )


def stabilize(path: Path) -> tuple[G2.G2Project, tuple[bool, str]]:
    project = G2.G2Project(gpxfile=str(path.resolve()))
    prepare(project)
    project.save()
    for _ in range(2):
        project.refine()
        project.save()
    project = G2.G2Project(gpxfile=str(path.resolve()))
    return project, physical(project)


def run_candidate(
    source: Path,
    destination: Path,
    missing_indices: list[int],
    width_fraction: float,
    size_scale: float,
) -> tuple[dict | None, str]:
    shutil.copy2(source, destination)
    try:
        project = G2.G2Project(gpxfile=str(destination.resolve()))
        prepare(project)
        histogram = project.histograms()[0]
        instrument = histogram.data["Instrument Parameters"][0]

        # Competing common Lorentzian terms are held at a fraction of their
        # current nonnegative values while missing phase-size terms settle.
        for key in ("X", "Z"):
            instrument[key][1] = max(0.0, float(instrument[key][1])) * width_fraction
            instrument[key][2] = False

        for index in missing_indices:
            phase = project.phases()[index]
            hap = phase.data["Histograms"][histogram.name]
            saved = max(1e-3, float(hap["Size"][1][0]))
            phase.set_HAP_refinements(
                {
                    "Size": {
                        "type": "isotropic",
                        "value": saved * size_scale,
                        "refine": True,
                    }
                }
            )
            project.set_Controls("parmMin", 1e-4, f"{index}:0:Size;i")
            project.set_Controls("parmMax", 100.0, f"{index}:0:Size;i")

        project.save()
        for _ in range(2):
            project.refine()
            project.save()
        project = G2.G2Project(gpxfile=str(destination.resolve()))
        valid, reason = physical(project)
        return (metrics(project) if valid else None), reason
    except Exception as exc:
        return None, f"{type(exc).__name__}:{exc}"


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: SCRIPT INPUT.gpx OUTPUT.gpx INPUTS_DIR")
    input_path = Path(sys.argv[1]).resolve()
    output_path = Path(sys.argv[2]).resolve()
    _inputs_dir = Path(sys.argv[3]).resolve()
    branch_dir = output_path.parent / f"{output_path.stem}_size_restart"
    branch_dir.mkdir(parents=True, exist_ok=True)

    baseline_path = branch_dir / "baseline.gpx"
    shutil.copy2(input_path, baseline_path)
    baseline, (valid, reason) = stabilize(baseline_path)
    if not valid:
        raise RuntimeError(f"fixed-atom baseline failed: {reason}")
    baseline_metrics = metrics(baseline)
    histogram = baseline.histograms()[0]
    missing = [
        index
        for index, phase in enumerate(baseline.phases())
        if not any(phase.data["Histograms"][histogram.name]["Size"][2])
    ]
    ledger = [
        {
            "mechanism": "fixed_atom_baseline",
            "accepted": True,
            "reason": reason,
            "missing_size_phases": missing,
            **baseline_metrics,
        }
    ]

    candidates = []
    serial = 0
    for width_fraction in (0.0, 0.1):
        for size_scale in (0.2, 1.0):
            if not missing:
                continue
            serial += 1
            path = branch_dir / f"branch_{serial:03d}.gpx"
            result, branch_reason = run_candidate(
                baseline_path,
                path,
                missing,
                width_fraction,
                size_scale,
            )
            row = {
                "mechanism": "size_dominant_common_width_restart",
                "path": path.name,
                "width_fraction": width_fraction,
                "size_scale": size_scale,
                "reason": branch_reason,
            }
            if result is not None:
                row.update(result)
                row["delta_aic"] = delta_aic(baseline_metrics, result)
                candidates.append((result["rwp"], path, result, row))
            ledger.append(row)

    selected_path = baseline_path
    selected_metrics = baseline_metrics
    if candidates:
        _rwp, candidate_path, candidate_metrics, candidate_row = min(
            candidates, key=lambda item: item[0]
        )
        if candidate_row["delta_aic"] < -2.0:
            selected_path = candidate_path
            selected_metrics = candidate_metrics
            candidate_row["accepted"] = True
        else:
            candidate_row["accepted"] = False

    output_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(selected_path, output_path)
    ledger.append({"selected": selected_path.name, **selected_metrics})
    output_path.with_suffix(".size_restart.json").write_text(
        json.dumps(ledger, indent=2) + "\n"
    )


if __name__ == "__main__":
    main()
