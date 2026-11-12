#!/usr/bin/env python3
"""Compare matched zero-only, displacement-only, and joint angular branches.

Usage: procedure.py INPUT.gpx OUTPUT.gpx INPUTS_DIR

The alternative starting values are derived only from the submitted project's
current angular correction, goniometer radius, and scan midpoint.  The script
keeps the original phase inventory and restores the project's own refinement
flags in stages.  It rejects failed refinements and a highly correlated joint
Zero/Shift branch, and otherwise retains an alternative only when its saved
Rwp improves by more than numerical noise.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from GSASII import GSASIIscriptable as G2sc

from profile_regeneration import regenerate_profile


BRANCHES = ("zero-only", "shift-only", "joint")
NUMERICAL_RWP_MARGIN = 0.005
JOINT_CORRELATION_LIMIT = 0.98


def covariance_status(project: G2sc.G2Project) -> dict:
    return project.data.get("Covariance", {}).get("data", {}).get("Rvals", {})


def stable_refinement(project: G2sc.G2Project, maximum_cycles: int = 8) -> bool:
    for _ in range(maximum_cycles):
        try:
            project.refine()
        except Exception as error:
            print("refinement error:", repr(error))
            return False
        status = covariance_status(project)
        message = str(status.get("msg", "") or "").lower()
        if (
            status.get("Aborted")
            or status.get("SVD0", 0)
            or "dropped" in message
            or "error" in message
        ):
            return False
        if status.get("converged") and float(status.get("Max shft/sig") or 0.0) < 0.05:
            return True
    return False


def angular_pair_correlation(project: G2sc.G2Project) -> float | None:
    covariance = project.data.get("Covariance", {}).get("data", {})
    names = list(covariance.get("varyList", []))
    matrix = np.asarray(covariance.get("covMatrix", []), dtype=float)
    if matrix.shape != (len(names), len(names)):
        return None
    zero = next((i for i, name in enumerate(names) if name.endswith(":Zero")), None)
    shift = next((i for i, name in enumerate(names) if name.endswith(":Shift")), None)
    if zero is None or shift is None:
        return None
    denominator = math.sqrt(max(float(matrix[zero, zero]), 0.0)) * math.sqrt(
        max(float(matrix[shift, shift]), 0.0)
    )
    if denominator <= 0.0:
        return None
    return abs(float(matrix[zero, shift]) / denominator)


def freeze_nonangular(project: G2sc.G2Project) -> None:
    histogram = project.histograms()[0]
    histogram.Background[0][1] = False
    for parameter in histogram.InstrumentParameters.values():
        if isinstance(parameter, list) and len(parameter) >= 3:
            parameter[2] = False
    for parameter in histogram.SampleParameters.values():
        if isinstance(parameter, list) and len(parameter) == 2:
            parameter[1] = False
    for phase in project.phases():
        phase.data["General"]["Cell"][0] = False
        for atom in phase.data["Atoms"]:
            atom[2] = ""
        hap = phase.data["Histograms"][histogram.name]
        hap["Scale"][1] = False
        if "Pref.Ori." in hap:
            hap["Pref.Ori."][2] = False
        for key in ("Size", "Mustrain"):
            if key in hap:
                hap[key][2] = [False] * len(hap[key][2])
        if "HStrain" in hap:
            hap["HStrain"][1] = [False] * len(hap["HStrain"][1])
        if "Extinction" in hap:
            hap["Extinction"][1] = False
        for parameter in hap.get("Babinet", {}).values():
            parameter[1] = False


def restore_group(
    project: G2sc.G2Project, template: G2sc.G2Project, group: str
) -> None:
    histogram = project.histograms()[0]
    source_histogram = template.histograms()[0]
    if group == "cells-scales-background":
        histogram.Background[0][1] = source_histogram.Background[0][1]
        for phase, source in zip(project.phases(), template.phases()):
            phase.data["General"]["Cell"][0] = source.data["General"]["Cell"][0]
            phase.data["Histograms"][histogram.name]["Scale"][1] = source.data[
                "Histograms"
            ][source_histogram.name]["Scale"][1]
        return
    if group == "profile-microstructure":
        for key, source in source_histogram.InstrumentParameters.items():
            parameter = histogram.InstrumentParameters.get(key)
            if key != "Zero" and isinstance(parameter, list) and len(parameter) >= 3:
                parameter[2] = source[2]
        for key, source in source_histogram.SampleParameters.items():
            parameter = histogram.SampleParameters.get(key)
            if key != "Shift" and isinstance(parameter, list) and len(parameter) == 2:
                parameter[1] = source[1]
        for phase, source in zip(project.phases(), template.phases()):
            hap = phase.data["Histograms"][histogram.name]
            source_hap = source.data["Histograms"][source_histogram.name]
            if "Pref.Ori." in hap:
                hap["Pref.Ori."][2] = source_hap["Pref.Ori."][2]
            for key in ("Size", "Mustrain"):
                if key in hap:
                    hap[key][2] = list(source_hap[key][2])
            if "HStrain" in hap:
                hap["HStrain"][1] = list(source_hap["HStrain"][1])
            if "Extinction" in hap:
                hap["Extinction"][1] = source_hap["Extinction"][1]
            for key, source_parameter in source_hap.get("Babinet", {}).items():
                hap["Babinet"][key][1] = source_parameter[1]
        return
    if group == "coordinates":
        for phase, source in zip(project.phases(), template.phases()):
            for atom, source_atom in zip(phase.data["Atoms"], source.data["Atoms"]):
                atom[2] = source_atom[2]
        return
    raise ValueError(group)


def equivalent_angular_start(project: G2sc.G2Project) -> dict:
    histogram = project.histograms()[0]
    instrument = histogram.data["Instrument Parameters"][0]
    sample = histogram.SampleParameters
    zero = float(instrument["Zero"][1])
    shift = float(sample["Shift"][0])
    radius = float(sample["Gonio. radius"])
    lower, upper = histogram.data["Limits"][1]
    representative_two_theta = (float(lower) + float(upper)) / 2.0
    cosine = math.cos(math.radians(representative_two_theta / 2.0))
    shift_as_zero = -shift * 0.36 * cosine / (math.pi * radius)
    effective_zero = zero + shift_as_zero
    equivalent_shift = -effective_zero * math.pi * radius / (0.36 * cosine)
    return {
        "original_zero_deg": zero,
        "original_shift_um": shift,
        "effective_zero_deg_at_midscan": effective_zero,
        "equivalent_shift_um": equivalent_shift,
        "representative_two_theta_deg": representative_two_theta,
        "goniometer_radius_mm": radius,
    }


def configure(project: G2sc.G2Project, branch: str, start: dict) -> None:
    histogram = project.histograms()[0]
    instrument = histogram.data["Instrument Parameters"][0]
    sample = histogram.SampleParameters
    effective_zero = start["effective_zero_deg_at_midscan"]
    equivalent_shift = start["equivalent_shift_um"]
    if branch == "zero-only":
        instrument["Zero"][1:] = [effective_zero, True]
        sample["Shift"][:] = [0.0, False]
    elif branch == "shift-only":
        instrument["Zero"][1:] = [0.0, False]
        sample["Shift"][:] = [equivalent_shift, True]
    elif branch == "joint":
        instrument["Zero"][1:] = [effective_zero / 2.0, True]
        sample["Shift"][:] = [equivalent_shift / 2.0, True]
    else:
        raise ValueError(branch)


def run_branch(source: Path, branch: str, temporary: Path) -> tuple[G2sc.G2Project, dict]:
    project = G2sc.G2Project(str(source))
    template = G2sc.G2Project(str(source))
    start = equivalent_angular_start(project)
    freeze_nonangular(project)
    configure(project, branch, start)
    # GSAS-II writes .lst/.bak files beside the current project. Repoint the
    # branch before the first refinement because evidence inputs are read-only.
    project.save(str(temporary))
    valid = stable_refinement(project, maximum_cycles=5)
    if valid:
        for group in (
            "cells-scales-background",
            "profile-microstructure",
            "coordinates",
        ):
            restore_group(project, template, group)
            if not stable_refinement(project):
                valid = False
                break
    project.save(str(temporary))
    correlation = angular_pair_correlation(project) if branch == "joint" else None
    if branch == "joint" and (correlation is None or correlation >= JOINT_CORRELATION_LIMIT):
        valid = False
    summary = {
        "branch": branch,
        "valid": valid,
        "rwp_percent": float(project.histograms()[0].get_wR()),
        "zero": project.histograms()[0].InstrumentParameters["Zero"],
        "shift": project.histograms()[0].SampleParameters["Shift"],
        "joint_zero_shift_correlation": correlation,
        "convergence": {
            key: covariance_status(project).get(key)
            for key in ("converged", "SVD0", "Max shft/sig", "msg", "Rwp")
        },
        "start": start,
    }
    return project, summary


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: procedure.py INPUT.gpx OUTPUT.gpx INPUTS_DIR")
    source = Path(sys.argv[1]).resolve()
    destination = Path(sys.argv[2]).resolve()
    _inputs = Path(sys.argv[3]).resolve()
    baseline = G2sc.G2Project(str(source))
    baseline_rwp = float(baseline.histograms()[0].get_wR())
    summaries = []
    candidates = []
    for branch in BRANCHES:
        temporary = destination.with_name(destination.stem + f"-{branch}.gpx")
        project, summary = run_branch(source, branch, temporary)
        summaries.append(summary)
        if summary["valid"] and math.isfinite(summary["rwp_percent"]):
            candidates.append((summary["rwp_percent"], branch, project))
    candidates.sort(key=lambda item: item[0])
    if candidates and candidates[0][0] < baseline_rwp - NUMERICAL_RWP_MARGIN:
        selected_rwp, selected_branch, selected_project = candidates[0]
    else:
        selected_rwp, selected_branch, selected_project = baseline_rwp, "baseline", baseline
    selected_project.save(str(destination))
    regenerate_profile(destination)
    print(
        "ANGULAR_BRANCH_RESULT="
        + json.dumps(
            {
                "baseline_rwp_percent": baseline_rwp,
                "selected_branch": selected_branch,
                "selected_rwp_percent": selected_rwp,
                "numerical_rwp_margin": NUMERICAL_RWP_MARGIN,
                "joint_correlation_limit": JOINT_CORRELATION_LIMIT,
                "branches": summaries,
            },
            sort_keys=True,
            default=str,
        )
    )


if __name__ == "__main__":
    main()
