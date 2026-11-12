#!/usr/bin/env python3
"""Audit fitted constant-wavelength profile states in GSAS-II projects.

This utility does not refine, rank, or modify a project. It reports both the
raw histogram contributions and the saved effective per-reflection widths,
which include phase HAP size/strain terms and GSAS-II's positive floor. Raw
component signs and covariance thresholds are comparison notices; they are not
automatic model-selection rules.
"""

from __future__ import annotations

import argparse
import json
import math
import warnings as python_warnings
from pathlib import Path
from typing import Any

import numpy as np
from GSASII import GSASIIpwd as G2pwd
from GSASII import GSASIIscriptable as G2


PROFILE_KEYS = ("Zero", "U", "V", "W", "X", "Y", "Z", "SH/L", "Polariz.")
SIGMA_FLOOR_CENTIDEG2 = 0.001
GAMMA_FLOOR_CENTIDEG = 0.001


def plain(value: Any) -> Any:
    if isinstance(value, np.generic):
        return plain(value.item())
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain(item) for item in value]
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    return repr(value)


def fitted_range(histogram: G2.G2PwdrData) -> tuple[float, float]:
    limits = histogram.data.get("Limits")
    if limits and len(limits) > 1 and len(limits[1]) == 2:
        return float(limits[1][0]), float(limits[1][1])
    x_values = np.asarray(histogram.getdata("x"), dtype=float)
    return float(np.min(x_values)), float(np.max(x_values))


def value(instrument: dict[str, list[Any]], key: str, default: float = 0.0) -> float:
    entry = instrument.get(key)
    if not entry or len(entry) < 2:
        return default
    return float(entry[1])


def extrema(values: np.ndarray, angles: np.ndarray) -> dict[str, Any]:
    finite = np.flatnonzero(np.isfinite(values))
    if not len(finite):
        return {
            "minimum": None,
            "minimum_at_two_theta_deg": None,
            "maximum": None,
            "maximum_at_two_theta_deg": None,
        }
    minimum = int(finite[np.argmin(values[finite])])
    maximum = int(finite[np.argmax(values[finite])])
    return {
        "minimum": float(values[minimum]),
        "minimum_at_two_theta_deg": float(angles[minimum]),
        "maximum": float(values[maximum]),
        "maximum_at_two_theta_deg": float(angles[maximum]),
    }


def top_correlations(project: G2.G2Project, count: int) -> list[dict[str, Any]]:
    covariance = project.data.get("Covariance", {}).get("data", {})
    matrix = np.asarray(covariance.get("covMatrix", []), dtype=float)
    names = list(covariance.get("varyList", []))
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1] or not names:
        return []
    standard_deviations = np.sqrt(np.maximum(np.diag(matrix), 0.0))
    denominator = np.outer(standard_deviations, standard_deviations)
    correlation = np.divide(
        matrix,
        denominator,
        out=np.zeros_like(matrix),
        where=denominator > 0,
    )
    pairs: list[tuple[float, int, int]] = []
    for row in range(len(names)):
        for column in range(row + 1, len(names)):
            pairs.append((abs(float(correlation[row, column])), row, column))
    pairs.sort(reverse=True)
    return [
        {
            "absolute_correlation": coefficient,
            "parameter_1": names[row],
            "parameter_2": names[column],
        }
        for coefficient, row, column in pairs[:count]
    ]


def phase_profile_state(
    project: G2.G2Project, histogram: G2.G2PwdrData
) -> list[dict[str, Any]]:
    records = []
    for phase in project.phases():
        hap = phase.data.get("Histograms", {}).get(histogram.name, {})
        record: dict[str, Any] = {"phase": phase.name}
        for key in ("Size", "Mustrain"):
            entry = hap.get(key)
            if isinstance(entry, (list, tuple)) and len(entry) >= 3:
                record[key] = {
                    "model": plain(entry[0]),
                    "values": plain(entry[1]),
                    "refined": plain(entry[2]),
                }
            elif entry is not None:
                record[key] = plain(entry)
        records.append(record)
    return records


def phase_adp_state(project: G2.G2Project) -> list[dict[str, Any]]:
    """Report isotropic ADPs and explicit all-site equality constraints.

    Equal saved values alone do not show that a grouped ADP was refined: they
    can also be coincident fixed defaults. GSAS-II stores atom and phase random
    IDs in equality constraints, so match those IDs without changing or
    resolving the project's constraint objects.
    """

    groups_by_phase: dict[Any, list[set[Any]]] = {}
    constraints = (
        project.data.get("Constraints", {})
        .get("data", {})
        .get("Phase", [])
    )
    for constraint in constraints:
        if not isinstance(constraint, (list, tuple)) or not constraint:
            continue
        if constraint[-1] != "e":
            continue
        variables = []
        for term in constraint:
            if not isinstance(term, (list, tuple)) or len(term) < 2:
                continue
            variable = term[1]
            if getattr(variable, "name", None) != "AUiso":
                continue
            phase_id = getattr(variable, "phase", None)
            atom_id = getattr(variable, "atom", None)
            if phase_id is not None and atom_id is not None:
                variables.append((phase_id, atom_id))
        phase_ids = {phase_id for phase_id, _ in variables}
        if len(variables) >= 2 and len(phase_ids) == 1:
            phase_id = next(iter(phase_ids))
            groups_by_phase.setdefault(phase_id, []).append(
                {atom_id for _, atom_id in variables}
            )

    records = []
    for phase in project.phases():
        atoms = list(phase.atoms())
        isotropic_atoms = [atom for atom in atoms if atom.adp_flag == "I"]
        isotropic_ids = {atom.ranId for atom in isotropic_atoms}
        label_by_id = {atom.ranId: atom.label for atom in atoms}
        groups = groups_by_phase.get(phase.ranId, [])
        values = np.asarray([atom.uiso for atom in isotropic_atoms], dtype=float)
        finite = bool(len(values) and np.all(np.isfinite(values)))
        equal = bool(
            finite
            and np.allclose(values, values[0], rtol=1e-8, atol=1e-10)
        )
        complete_constraint = bool(
            len(isotropic_ids) <= 1
            or any(group == isotropic_ids for group in groups)
        )
        records.append(
            {
                "phase": phase.name,
                "atom_count": len(atoms),
                "isotropic_atom_count": len(isotropic_atoms),
                "all_sites_isotropic": len(isotropic_atoms) == len(atoms),
                "all_isotropic_Uiso_values_equal": equal,
                "complete_phase_AUiso_equivalence_constraint": (
                    complete_constraint
                ),
                "AUiso_equivalence_groups": [
                    sorted(label_by_id.get(atom_id, str(atom_id)) for atom_id in group)
                    for group in groups
                ],
                "atoms": [
                    {
                        "label": atom.label,
                        "element": atom.element,
                        "ADP_model": atom.adp_flag,
                        "Uiso_A2": (
                            plain(atom.uiso) if atom.adp_flag == "I" else None
                        ),
                        "Uij_A2": (
                            None if atom.adp_flag == "I" else plain(atom.ADP)
                        ),
                        "refinement_flags": atom.refinement_flags,
                    }
                    for atom in atoms
                ],
            }
        )
    return records


def background_state(histogram: G2.G2PwdrData) -> dict[str, Any]:
    """Return the saved smooth/background-peak model without interpreting it."""

    background = histogram.data.get("Background", [])
    smooth = background[0] if background and isinstance(background[0], list) else []
    extras = background[1] if len(background) > 1 and isinstance(background[1], dict) else {}
    count = int(smooth[2]) if len(smooth) >= 3 else 0
    return {
        "type": plain(smooth[0]) if smooth else None,
        "refined": bool(smooth[1]) if len(smooth) >= 2 else None,
        "coefficient_count": count,
        "coefficients": plain(smooth[3 : 3 + count]),
        "Debye_term_count": int(extras.get("nDebye", 0)),
        "background_peak_count": int(extras.get("nPeaks", 0)),
    }


def effective_reflection_widths(
    histogram: G2.G2PwdrData,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Summarize saved effective widths for reflections in the fitted range.

    For constant-wavelength powder data, GSAS-II stores position, effective
    Gaussian variance and effective Lorentzian gamma in each phase's saved
    Reflection List. These values include phase HAP size/strain contributions
    and the positive floors applied by ``GetReflSigGamCW``.
    """

    low, high = fitted_range(histogram)
    records: list[dict[str, Any]] = []
    all_sigma: list[np.ndarray] = []
    all_gamma: list[np.ndarray] = []
    all_fwhm: list[np.ndarray] = []
    sigma_floor_count = 0
    gamma_floor_count = 0

    reflection_lists = histogram.data.get("Reflection Lists", {})
    for phase_name, reflection_data in reflection_lists.items():
        if not isinstance(reflection_data, dict):
            continue
        reflections = np.asarray(reflection_data.get("RefList", []), dtype=float)
        modulation_offset = int(bool(reflection_data.get("Super", False)))
        position_column = 5 + modulation_offset
        sigma_column = 6 + modulation_offset
        gamma_column = 7 + modulation_offset
        required_columns = gamma_column + 1
        if reflections.ndim != 2 or reflections.shape[1] < required_columns:
            continue

        positions = reflections[:, position_column]
        in_range = np.isfinite(positions) & (positions >= low) & (positions <= high)
        positions = positions[in_range]
        sigma = reflections[in_range, sigma_column]
        gamma = reflections[in_range, gamma_column]
        if not len(positions):
            continue

        fwhm = np.full(len(positions), np.nan, dtype=float)
        valid = np.isfinite(sigma) & np.isfinite(gamma) & (sigma >= 0.0)
        with np.errstate(all="ignore"):
            fwhm[valid] = [
                G2pwd.getgamFW(float(g), math.sqrt(float(s))) / 100.0
                for s, g in zip(sigma[valid], gamma[valid])
            ]
        sigma_at_floor = sigma <= SIGMA_FLOOR_CENTIDEG2 * (1.0 + 1e-6)
        gamma_at_floor = gamma <= GAMMA_FLOOR_CENTIDEG * (1.0 + 1e-6)
        sigma_floor_count += int(np.count_nonzero(sigma_at_floor))
        gamma_floor_count += int(np.count_nonzero(gamma_at_floor))
        all_sigma.append(sigma)
        all_gamma.append(gamma)
        all_fwhm.append(fwhm)
        records.append(
            {
                "phase": str(phase_name),
                "reflection_count": int(len(positions)),
                "gaussian_variance_centideg2": extrema(sigma, positions),
                "lorentzian_gamma_centideg": extrema(gamma, positions),
                "total_pseudovoigt_fwhm_deg": extrema(fwhm, positions),
                "gaussian_variance_at_GSAS_floor_count": int(
                    np.count_nonzero(sigma_at_floor)
                ),
                "gaussian_variance_at_GSAS_floor_fraction": float(
                    np.mean(sigma_at_floor)
                ),
                "lorentzian_gamma_at_GSAS_floor_count": int(
                    np.count_nonzero(gamma_at_floor)
                ),
                "lorentzian_gamma_at_GSAS_floor_fraction": float(
                    np.mean(gamma_at_floor)
                ),
            }
        )

    if all_sigma:
        sigma = np.concatenate(all_sigma)
        gamma = np.concatenate(all_gamma)
        fwhm = np.concatenate(all_fwhm)
    else:
        sigma = np.asarray([], dtype=float)
        gamma = np.asarray([], dtype=float)
        fwhm = np.asarray([], dtype=float)

    count = int(len(sigma))
    summary = {
        "source": (
            "saved GSAS-II Reflection Lists; includes phase HAP size/strain "
            "terms and GSAS-II positive floors"
        ),
        "reflection_count": count,
        "gaussian_variance_floor_centideg2": SIGMA_FLOOR_CENTIDEG2,
        "gamma_floor_centideg": GAMMA_FLOOR_CENTIDEG,
        "gaussian_variance_at_GSAS_floor_count": sigma_floor_count,
        "gaussian_variance_at_GSAS_floor_fraction": (
            float(sigma_floor_count / count) if count else None
        ),
        "lorentzian_gamma_at_GSAS_floor_count": gamma_floor_count,
        "lorentzian_gamma_at_GSAS_floor_fraction": (
            float(gamma_floor_count / count) if count else None
        ),
        "available": bool(count),
        "finite": bool(
            count
            and np.all(np.isfinite(sigma))
            and np.all(np.isfinite(gamma))
            and np.all(np.isfinite(fwhm))
        ),
        "positive_gaussian_variance": bool(count and np.min(sigma) > 0.0),
        "positive_lorentzian_gamma": bool(count and np.min(gamma) > 0.0),
        "positive_total_fwhm": bool(count and np.min(fwhm) > 0.0),
    }
    return records, summary


def audit_project(
    project_path: Path,
    histogram_index: int = 0,
    grid_points: int = 1001,
    correlation_count: int = 10,
) -> dict[str, Any]:
    project = G2.G2Project(str(project_path))
    histogram = project.histogram(histogram_index)
    instrument = histogram.InstrumentParameters
    instrument_type = str(instrument.get("Type", [""])[0])
    if "C" not in instrument_type:
        raise ValueError(
            f"{project_path}: expected a constant-wavelength instrument, "
            f"found Type={instrument_type!r}"
        )

    low, high = fitted_range(histogram)
    two_theta = np.linspace(low, high, grid_points)
    theta = np.deg2rad(two_theta / 2.0)
    tangent = np.tan(theta)
    cosine = np.cos(theta)

    gaussian_variance = (
        value(instrument, "U") * tangent**2
        + value(instrument, "V") * tangent
        + value(instrument, "W")
    )
    lorentzian_gamma = (
        value(instrument, "Z")
        + value(instrument, "X") / cosine
        + value(instrument, "Y") * tangent
    )
    with python_warnings.catch_warnings(), np.errstate(all="ignore"):
        python_warnings.simplefilter("ignore", RuntimeWarning)
        total_fwhm = np.asarray(
            [G2pwd.getFWHM(float(angle), instrument, 1) for angle in two_theta],
            dtype=float,
        )

    covariance = project.data.get("Covariance", {}).get("data", {})
    rvalues = covariance.get("Rvals", {})
    correlations = top_correlations(project, correlation_count)
    effective_widths, effective_summary = effective_reflection_widths(histogram)
    finite_raw_histogram_components = bool(
        np.all(np.isfinite(gaussian_variance))
        and np.all(np.isfinite(lorentzian_gamma))
        and np.all(np.isfinite(total_fwhm))
    )
    checks = {
        "effective_reflections_available": effective_summary["available"],
        "finite_effective_reflection_widths": effective_summary["finite"],
        "positive_effective_gaussian_variance": effective_summary[
            "positive_gaussian_variance"
        ],
        "positive_effective_lorentzian_gamma": effective_summary[
            "positive_lorentzian_gamma"
        ],
        "positive_effective_total_fwhm": effective_summary["positive_total_fwhm"],
    }
    warnings = [name for name, passed in checks.items() if not passed]
    notices = []
    if not finite_raw_histogram_components:
        notices.append("nonfinite_raw_histogram_component_calculation")
    if np.min(gaussian_variance) < 0.0:
        notices.append("negative_raw_histogram_gaussian_variance")
        if effective_summary["positive_gaussian_variance"]:
            notices.append("raw_HAP_gaussian_compensation")
    if np.min(lorentzian_gamma) < 0.0:
        notices.append("negative_raw_histogram_lorentzian_gamma")
        if effective_summary["positive_lorentzian_gamma"]:
            notices.append("raw_HAP_lorentzian_compensation")
    if effective_summary["gaussian_variance_at_GSAS_floor_count"]:
        notices.append("effective_gaussian_variance_at_GSAS_floor")
    if effective_summary["lorentzian_gamma_at_GSAS_floor_count"]:
        notices.append("effective_lorentzian_gamma_at_GSAS_floor")
    if correlations and correlations[0]["absolute_correlation"] >= 0.95:
        notices.append("correlation_at_or_above_0p95")
    if rvalues.get("converged") is False:
        notices.append("refinement_not_converged")
    result = {
        "project": str(project_path.resolve()),
        "histogram_index": histogram_index,
        "histogram_name": histogram.name,
        "two_theta_range_deg": [low, high],
        "instrument": {
            key: {
                "value": plain(instrument[key][1]),
                "refined": bool(instrument[key][2]),
            }
            for key in PROFILE_KEYS
            if key in instrument and len(instrument[key]) >= 3
        },
        "background_state": background_state(histogram),
        "phase_profile_state": phase_profile_state(project, histogram),
        "phase_ADP_state": phase_adp_state(project),
        "raw_gaussian_variance_centideg2": extrema(gaussian_variance, two_theta),
        "raw_lorentzian_gamma_centideg": extrema(lorentzian_gamma, two_theta),
        "raw_histogram_total_pseudovoigt_fwhm_deg": extrema(
            total_fwhm, two_theta
        ),
        "effective_reflection_widths": effective_widths,
        "effective_reflection_summary": effective_summary,
        "finite_raw_histogram_components": finite_raw_histogram_components,
        "checks": checks,
        "warnings": warnings,
        "notices": notices,
        "fit": {
            "Rwp_percent": plain(float(histogram.residuals.get("wR", math.nan))),
            "Rp_percent": plain(float(histogram.residuals.get("R", math.nan))),
            "Rexp_percent": plain(float(histogram.residuals.get("wRmin", math.nan))),
            "converged": plain(rvalues.get("converged")),
            "maximum_shift_over_esd": plain(rvalues.get("Max shft/sig")),
            "refined_variable_count": len(covariance.get("varyList", [])),
        },
        "top_absolute_correlations": correlations,
    }
    return result


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("projects", nargs="+", type=Path, help="GSAS-II .gpx files")
    parser.add_argument(
        "--histogram", type=int, default=0, help="zero-based powder histogram index"
    )
    parser.add_argument(
        "--grid-points", type=int, default=1001, help="angular audit grid size"
    )
    parser.add_argument(
        "--top-correlations", type=int, default=10, help="correlation pairs to report"
    )
    parser.add_argument("--json", type=Path, help="optional JSON output path")
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    if arguments.grid_points < 3:
        raise SystemExit("--grid-points must be at least 3")
    records = [
        audit_project(
            path,
            histogram_index=arguments.histogram,
            grid_points=arguments.grid_points,
            correlation_count=max(arguments.top_correlations, 0),
        )
        for path in arguments.projects
    ]
    output: Any = records[0] if len(records) == 1 else records
    text = json.dumps(output, indent=2, allow_nan=False) + "\n"
    if arguments.json:
        arguments.json.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
