#!/usr/bin/env python3
"""Conservative final profile replay for a saved GSAS-II powder project.

Called as: postrollback_profile.py INPUT.gpx OUTPUT.gpx INPUTS_DIR

The procedure never changes inventory or atomic coordinates. It auditions a
small set of ordinary profile mechanisms from independent starts and retains
only physical branches whose observed-profile gain pays for added parameters.
"""

from __future__ import annotations

import json
import math
import shutil
import sys
from pathlib import Path
from typing import Callable

import numpy as np
from GSASII import GSASIIscriptable as G2


G2.SetPrintLevel("warn")


def phase_fractions(project: G2.G2Project) -> np.ndarray:
    histogram = project.histograms()[0]
    products = np.asarray(
        [
            phase.data["General"]["Mass"]
            * phase.data["Histograms"][histogram.name]["Scale"][0]
            for phase in project.phases()
        ],
        dtype=float,
    )
    return products / products.sum()


def metrics(project: G2.G2Project) -> dict:
    histogram = project.histograms()[0]
    covariance = project.data.get("Covariance", {}).get("data", {})
    fit = covariance.get("Rvals", {})
    arrays = np.asarray(histogram.data["data"][1], dtype=float)
    return {
        "rwp": float(histogram.get_wR()),
        "parameters": len(covariance.get("varyList", [])),
        "n": int(arrays.shape[1]),
        "fractions": phase_fractions(project).tolist(),
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
        size = hap["Size"]
        for value, active in zip(size[1], size[2]):
            if active and not 1e-4 < float(value) < 100:
                return False, "size_at_physical_bound"
        strain = hap["Mustrain"]
        for value, active in zip(strain[1], strain[2]):
            if active and not 0 < float(value) < 50000:
                return False, "strain_at_physical_bound"
    return True, "pass"


def penalized_gain(old: dict, new: dict) -> float:
    """AIC(new)-AIC(old), using Rwp squared as proportional RSS."""
    if old["rwp"] <= 0 or new["rwp"] <= 0:
        return math.inf
    return (
        old["n"] * math.log((new["rwp"] / old["rwp"]) ** 2)
        + 2 * (new["parameters"] - old["parameters"])
    )


def prepare(project: G2.G2Project) -> None:
    project.set_Controls("cycles", 24)
    project.data["Controls"]["data"]["shift factor"] = 0.25
    project.data["Controls"]["data"]["parmFrozen"] = {"FrozenList": []}
    for phase in project.phases():
        for atom in phase.atoms():
            atom.refinement_flags = (
                atom.refinement_flags.replace("X", "").replace("U", "")
            )


def run_branch(
    source: Path,
    destination: Path,
    mutate: Callable[[G2.G2Project], None],
) -> tuple[dict | None, str]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    try:
        project = G2.G2Project(gpxfile=str(destination.resolve()))
        prepare(project)
        mutate(project)
        project.save()
        for _ in range(2):
            project.refine()
            project.save()
        project = G2.G2Project(gpxfile=str(destination.resolve()))
        valid, reason = physical(project)
        return (metrics(project) if valid else None), reason
    except Exception as exc:  # GSAS-II numerical failures are rejected branches.
        return None, f"{type(exc).__name__}:{exc}"


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: SCRIPT INPUT.gpx OUTPUT.gpx INPUTS_DIR")
    input_path = Path(sys.argv[1]).resolve()
    output_path = Path(sys.argv[2]).resolve()
    _inputs_dir = Path(sys.argv[3]).resolve()
    branch_dir = output_path.parent / f"{output_path.stem}_profile_branches"
    branch_dir.mkdir(parents=True, exist_ok=True)

    current = branch_dir / "baseline.gpx"
    shutil.copy2(input_path, current)
    baseline = G2.G2Project(gpxfile=str(current))
    prepare(baseline)
    baseline.save()
    # Refresh covariance metadata after removing atomic variables. Without this
    # stabilization, AIC would compare a stale pre-freeze parameter count with
    # the live parameter count from each candidate refinement.
    for _ in range(2):
        baseline.refine()
        baseline.save()
    baseline = G2.G2Project(gpxfile=str(current))
    baseline_valid, baseline_reason = physical(baseline)
    if not baseline_valid:
        raise RuntimeError(f"fixed-atom baseline failed: {baseline_reason}")
    current_metrics = metrics(baseline)
    ledger = [
        {
            "mechanism": "input_with_atoms_fixed",
            "accepted": True,
            "reason": baseline_reason,
            **current_metrics,
        }
    ]
    serial = 0

    def audition(
        mechanism: str,
        mutations: list[Callable[[G2.G2Project], None]],
    ) -> None:
        nonlocal current, current_metrics, serial
        candidates = []
        for mutation in mutations:
            serial += 1
            path = branch_dir / f"branch_{serial:03d}.gpx"
            result, reason = run_branch(current, path, mutation)
            row = {"mechanism": mechanism, "path": path.name, "reason": reason}
            if result is not None:
                row.update(result)
                row["delta_aic"] = penalized_gain(current_metrics, result)
                candidates.append((result["rwp"], path, result, row))
            ledger.append(row)
        if not candidates:
            return
        _rwp, path, result, row = min(candidates, key=lambda item: item[0])
        # Require a clear gain after paying for added flexibility.
        if row["delta_aic"] < -2.0:
            current = path
            current_metrics = result
            row["accepted"] = True
        else:
            row["accepted"] = False

    def roughness(start: float) -> Callable[[G2.G2Project], None]:
        def mutate(project: G2.G2Project) -> None:
            sample = project.histograms()[0].data["Sample Parameters"]
            sample["SurfRoughA"] = [start, True]
            sample["SurfRoughB"] = [start, True]
            project.set_Controls("parmMin", 0.0, ":0:SurfRoughA")
            project.set_Controls("parmMax", 5.0, ":0:SurfRoughA")
            project.set_Controls("parmMin", 0.0, ":0:SurfRoughB")
            project.set_Controls("parmMax", 5.0, ":0:SurfRoughB")

        return mutate

    audition("paired_surface_roughness", [roughness(0.05), roughness(0.2)])

    phase_count = len(G2.G2Project(gpxfile=str(current)).phases())
    for phase_index in range(phase_count):
        def isotropic_size(start: float, index: int = phase_index):
            def mutate(project: G2.G2Project) -> None:
                phase = project.phases()[index]
                phase.set_HAP_refinements(
                    {"Size": {"type": "isotropic", "value": start, "refine": True}}
                )
                project.set_Controls("parmMin", 1e-4, f"{index}:0:Size;i")
                project.set_Controls("parmMax", 100.0, f"{index}:0:Size;i")

            return mutate

        audition(
            f"phase_{phase_index}_isotropic_size",
            [isotropic_size(0.05), isotropic_size(0.2), isotropic_size(1.0)],
        )

    for phase_index in range(phase_count):
        project = G2.G2Project(gpxfile=str(current))
        histogram = project.histograms()[0]
        size = project.phases()[phase_index].data["Histograms"][histogram.name]["Size"]
        if not any(size[2]):
            continue
        start = max(1e-3, float(size[1][0]))

        def uniaxial_size(
            axis: tuple[int, int, int],
            index: int = phase_index,
            start_value: float = start,
        ):
            def mutate(project: G2.G2Project) -> None:
                phase = project.phases()[index]
                phase.set_HAP_refinements(
                    {
                        "Size": {
                            "type": "uniaxial",
                            "direction": list(axis),
                            "value": start_value,
                            "refine": True,
                        }
                    }
                )
                project.set_Controls("parmMin", 1e-4, f"{index}:0:Size;i")
                project.set_Controls("parmMax", 100.0, f"{index}:0:Size;i")
                project.set_Controls("parmMin", 1e-4, f"{index}:0:Size;a")
                project.set_Controls("parmMax", 100.0, f"{index}:0:Size;a")

            return mutate

        axes = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 1, 1)]
        audition(
            f"phase_{phase_index}_uniaxial_size",
            [uniaxial_size(axis) for axis in axes],
        )

    for phase_index in range(phase_count):
        project = G2.G2Project(gpxfile=str(current))
        histogram = project.histograms()[0]
        strain = project.phases()[phase_index].data["Histograms"][histogram.name]["Mustrain"]
        if any(strain[2]):
            continue

        def isotropic_strain(start: float, index: int = phase_index):
            def mutate(project: G2.G2Project) -> None:
                phase = project.phases()[index]
                hap = phase.data["Histograms"][project.histograms()[0].name]
                hap["Mustrain"][0] = "isotropic"
                hap["Mustrain"][1][0] = start
                phase.set_HAP_refinements(
                    {"Mustrain": {"type": "isotropic", "refine": True}}
                )
                project.set_Controls("parmMin", 0.0, f"{index}:0:Mustrain;i")
                project.set_Controls("parmMax", 50000.0, f"{index}:0:Mustrain;i")

            return mutate

        audition(
            f"phase_{phase_index}_isotropic_strain",
            [isotropic_strain(500.0), isotropic_strain(2000.0)],
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(current, output_path)
    ledger.append({"selected": current.name, **current_metrics})
    output_path.with_suffix(".profile_replay.json").write_text(
        json.dumps(ledger, indent=2) + "\n"
    )


if __name__ == "__main__":
    main()
