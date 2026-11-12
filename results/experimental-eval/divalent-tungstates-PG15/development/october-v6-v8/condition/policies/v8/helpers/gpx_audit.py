#!/usr/bin/env python3
"""Read-only final-state audit for a GSAS-II powder project.

Run with GSAS-II's Python. This checks model integrity and numerical warning
signs; it does not decide whether the scientific model is uniquely correct.
"""

from __future__ import annotations

import argparse
import copy
import json
import math
from pathlib import Path

import numpy as np
from scipy.interpolate import interp1d
from GSASII import GSASIIlattice as G2lat
from GSASII import GSASIIscriptable as G2sc
from GSASII import GSASIIstrIO as G2io
from GSASII import GSASIIstrMath as G2math


def fitted(parameter, default=0.0) -> float:
    if isinstance(parameter, (list, tuple)) and len(parameter) > 1:
        return float(parameter[1])
    return float(default)


def empirical_background(kind: str, coefficients: list[float], x, domain):
    """Evaluate fit-range-dependent GSAS-II empirical backgrounds."""
    lower, upper = domain
    transformed = 2.0 * (x - lower) / (upper - lower) - 1.0
    if kind == "chebyschev":
        return np.polynomial.polynomial.polyval(transformed, coefficients)
    if kind == "chebyschev-1":
        return np.polynomial.chebyshev.chebval(transformed, coefficients)
    if kind == "cosine":
        return sum(
            coefficient * np.cos(np.pi * x * index / upper)
            for index, coefficient in enumerate(coefficients)
        )
    if kind in {"lin interpolate", "inv interpolate", "log interpolate"}:
        if len(coefficients) == 1:
            return np.full_like(x, coefficients[0])
        if len(coefficients) == 2:
            return coefficients[0] + (coefficients[1] - coefficients[0]) * (
                x - lower
            ) / (upper - lower)
        if kind == "lin interpolate":
            knots = np.linspace(lower, upper, len(coefficients))
        elif kind == "inv interpolate":
            knots = 1.0 / np.linspace(1.0 / upper, 1.0 / lower, len(coefficients))
        else:
            knots = np.exp(
                np.linspace(np.log(lower), np.log(upper), len(coefficients))
            )
        knots[0], knots[-1] = lower, upper
        return interp1d(
            knots, coefficients, bounds_error=False, fill_value="extrapolate"
        )(x)
    return None


def rwp_percent(observed, calculated, weights) -> float:
    valid = (
        np.isfinite(observed)
        & np.isfinite(calculated)
        & np.isfinite(weights)
        & (weights > 0.0)
    )
    denominator = float(np.sum(weights[valid] * observed[valid] ** 2))
    if denominator <= 0.0:
        return math.nan
    numerator = float(
        np.sum(weights[valid] * (observed[valid] - calculated[valid]) ** 2)
    )
    return 100.0 * math.sqrt(numerator / denominator)


def total_width_audit(path: Path) -> list[dict]:
    """Regenerate reflection lists and inspect instrument + sample widths."""
    all_histograms, all_phases = G2io.GetUsedHistogramsAndPhases(str(path))
    reports = []
    for name, source_histogram in all_histograms.items():
        if not name.startswith("PWDR"):
            continue
        histogram = copy.deepcopy(source_histogram)
        histograms = {name: histogram}
        phases = {
            phase_name: copy.deepcopy(phase)
            for phase_name, phase in all_phases.items()
            if name in phase.get("Histograms", {})
            and phase["Histograms"][name].get("Use", True)
            and phase["Histograms"][name]["Scale"][0] != 0
        }
        instrument = histogram["Instrument Parameters"][0]
        if instrument["Type"][0] != "PXC" or not phases:
            reports.append({"histogram": name, "status": "unsupported_or_no_phases"})
            continue

        x = np.asarray(histogram["Data"][0], dtype=float)
        observed = np.asarray(histogram["Data"][1], dtype=float)
        weights = np.asarray(histogram["Data"][2], dtype=float)
        saved_calculated = np.asarray(histogram["Data"][3], dtype=float).copy()
        old_limits = copy.deepcopy(histogram["Limits"])
        lower_index, upper_index = np.searchsorted(x, old_limits[1])
        upper_index = min(len(x) - 1, upper_index)
        background_domain = [
            float(x[lower_index]),
            float(x[upper_index]),
        ]
        histogram["Limits"] = [[float(x[0]), float(x[-1])], [float(x[0]), float(x[-1])]]
        controls = dict(G2io.GetControls(str(path)))
        controls.pop("PhasePartials", None)
        rigid = G2io.GetRigidBodies(str(path))
        rigid_ids = rigid.get("RBIds", {"Vector": [], "Residue": []})
        _, rigid_parameters = G2io.GetRigidBodyModels(rigid, Print=False)
        (
            atom_count,
            atom_index,
            _,
            phase_parameters,
            pawley_lookup,
            form_factors,
            electron_factors,
            orbital_factors,
            bond_lengths,
            magnetic_factors,
            maximum_wave,
        ) = G2io.GetPhaseData(phases, {}, rigid_ids, Print=False)
        controls.update(
            atomIndx=atom_index,
            Natoms=atom_count,
            FFtables=form_factors,
            EFtables=electron_factors,
            ORBtables=orbital_factors,
            BLtables=bond_lengths,
            MFtables=magnetic_factors,
            maxSSwave=maximum_wave,
        )
        _, hap_parameters, updates = G2io.GetHistogramPhaseData(
            phases, histograms, Controls=controls, Print=False
        )
        controls.update(updates)
        _, histogram_parameters, histogram_controls, updates = G2io.GetHistogramData(
            histograms, Print=False
        )
        controls.update(updates)
        parameters = {
            **rigid_parameters,
            **phase_parameters,
            **hap_parameters,
            **histogram_parameters,
        }
        G2io.GetFprime(controls, histograms)
        signal, background = G2math.getPowderProfile(
            parameters,
            histogram_controls,
            x,
            [],
            histogram,
            phases,
            controls,
            pawley_lookup,
            name,
        )

        histogram_prefix = f":{histogram['hId']}:"
        background_kind = controls[histogram_prefix + "bakType"]
        background_coefficients = []
        while histogram_prefix + f"Back;{len(background_coefficients)}" in parameters:
            background_coefficients.append(
                parameters[
                    histogram_prefix + f"Back;{len(background_coefficients)}"
                ]
            )
        saved_domain_background = empirical_background(
            background_kind, background_coefficients, x, background_domain
        )
        if saved_domain_background is not None:
            full_domain_background = empirical_background(
                background_kind,
                background_coefficients,
                x,
                [float(x[0]), float(x[-1])],
            )
            background = background + saved_domain_background - full_domain_background
        regenerated_calculated = np.asarray(signal + background, dtype=float)
        delta = regenerated_calculated - saved_calculated
        finite_regeneration = bool(
            np.all(np.isfinite(regenerated_calculated))
            and np.all(np.isfinite(saved_calculated))
        )
        maximum_observed = float(np.max(np.abs(observed)))
        maximum_difference = (
            float(np.max(np.abs(delta))) if finite_regeneration else math.inf
        )
        rms_difference = (
            float(np.sqrt(np.mean(delta**2))) if finite_regeneration else math.inf
        )
        saved_rwp = rwp_percent(observed, saved_calculated, weights)
        regenerated_rwp = rwp_percent(observed, regenerated_calculated, weights)
        profile_regeneration = {
            "status": "pass",
            "saved_rwp_percent": saved_rwp,
            "regenerated_rwp_percent": regenerated_rwp,
            "absolute_rwp_difference_percent": abs(regenerated_rwp - saved_rwp),
            "maximum_absolute_profile_difference_counts": maximum_difference,
            "rms_profile_difference_counts": rms_difference,
            "maximum_difference_fraction_of_maximum_observed": (
                maximum_difference / maximum_observed
                if maximum_observed > 0.0
                else math.inf
            ),
        }
        if (
            not finite_regeneration
            or abs(regenerated_rwp - saved_rwp) > 0.05
            or (
                maximum_observed > 0.0
                and rms_difference / maximum_observed > 1.0e-4
            )
        ):
            profile_regeneration["status"] = "needs_review"
        phase_reports = []
        for phase_name, phase in phases.items():
            phase_prefix = f"{phase['pId']}::"
            hap_prefix = f"{phase['pId']}:{histogram['hId']}:"
            symmetry = phase["General"]["SGData"]
            dij = G2math.GetDij(hap_prefix, symmetry, parameters)
            reciprocal_cell = [
                parameters[phase_prefix + f"A{index}"] + dij[index]
                for index in range(6)
            ]
            metric, _ = G2lat.A2Gmat(reciprocal_cell)
            _, reciprocal_basis = G2lat.Gmat2AB(metric)
            wavelength = parameters.get(
                histogram_prefix + "Lam1", parameters.get(histogram_prefix + "Lam")
            )
            minimum_sigma = [math.inf, None]
            minimum_gamma = [math.inf, None]
            nonfinite_reflections = 0
            reflections = histogram["Reflection Lists"][phase_name]["RefList"]
            for reflection in reflections:
                position = float(reflection[5])
                tangent = math.tan(math.radians(position / 2.0))
                sample_sigma, sample_gamma = G2math.GetSampleSigGam(
                    reflection,
                    0,
                    wavelength,
                    metric,
                    reciprocal_basis,
                    symmetry,
                    histogram_prefix,
                    hap_prefix,
                    controls,
                    parameters,
                )
                sigma = (
                    parameters[histogram_prefix + "U"] * tangent**2
                    + parameters[histogram_prefix + "V"] * tangent
                    + parameters[histogram_prefix + "W"]
                    + sample_sigma
                )
                gamma = (
                    parameters[histogram_prefix + "X"]
                    / math.cos(math.radians(position / 2.0))
                    + parameters[histogram_prefix + "Y"] * tangent
                    + parameters[histogram_prefix + "Z"]
                    + sample_gamma
                )
                if not math.isfinite(float(sigma)) or not math.isfinite(float(gamma)):
                    nonfinite_reflections += 1
                    continue
                if sigma < minimum_sigma[0]:
                    minimum_sigma = [float(sigma), position]
                if gamma < minimum_gamma[0]:
                    minimum_gamma = [float(gamma), position]
            status = (
                "pass"
                if len(reflections) > 0
                and nonfinite_reflections == 0
                and minimum_sigma[0] >= 0.0
                and minimum_gamma[0] >= 0.0
                else "needs_review"
            )
            phase_reports.append(
                {
                    "phase": phase_name,
                    "status": status,
                    "reflection_count": len(reflections),
                    "nonfinite_width_reflections": nonfinite_reflections,
                    "minimum_total_gaussian_variance_centideg2": minimum_sigma[0],
                    "gaussian_minimum_at_2theta_deg": minimum_sigma[1],
                    "minimum_total_lorentzian_width_centideg": minimum_gamma[0],
                    "lorentzian_minimum_at_2theta_deg": minimum_gamma[1],
                }
            )
        reports.append(
            {
                "histogram": name,
                "status": "needs_review"
                if profile_regeneration["status"] != "pass"
                or any(report["status"] != "pass" for report in phase_reports)
                else "pass",
                "saved_profile_regeneration": profile_regeneration,
                "phases": phase_reports,
            }
        )
    return reports


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--compact", action="store_true")
    parser.add_argument(
        "--summary",
        action="store_true",
        help="print only the overall flags, width audit and convergence summary",
    )
    args = parser.parse_args()

    path = args.project.resolve()
    project = G2sc.G2Project(str(path))
    warnings = []
    histograms = []

    for histogram in project.histograms():
        limits = histogram.data.get("Limits", [None, [None, None]])[1]
        instrument = histogram.InstrumentParameters
        instrument_type = str(instrument.get("Type", [""])[0])
        width_audit = {"status": "not_constant_wavelength"}
        if "C" in instrument_type and limits[0] is not None and limits[1] is not None:
            two_theta = np.linspace(float(limits[0]), float(limits[1]), 2001)
            theta = np.radians(two_theta / 2.0)
            tangent = np.tan(theta)
            cosine = np.cos(theta)
            gaussian_variance = (
                fitted(instrument.get("U")) * tangent**2
                + fitted(instrument.get("V")) * tangent
                + fitted(instrument.get("W"))
            )
            lorentzian_width = (
                fitted(instrument.get("Z"))
                + fitted(instrument.get("X")) / cosine
                + fitted(instrument.get("Y")) * tangent
            )
            gaussian_index = int(np.argmin(gaussian_variance))
            lorentzian_index = int(np.argmin(lorentzian_width))
            width_audit = {
                "status": "instrument_component_diagnostic_only",
                "minimum_gaussian_variance_centideg2": float(
                    gaussian_variance[gaussian_index]
                ),
                "gaussian_minimum_at_2theta_deg": float(two_theta[gaussian_index]),
                "minimum_lorentzian_width_centideg": float(
                    lorentzian_width[lorentzian_index]
                ),
                "lorentzian_minimum_at_2theta_deg": float(two_theta[lorentzian_index]),
            }

        histograms.append(
            {
                "name": histogram.name,
                "limits_2theta_deg": limits,
                "residuals": histogram.residuals,
                "sample_parameters": histogram.SampleParameters,
                "instrument_parameters": instrument,
                "analytic_width_audit": width_audit,
            }
        )

    phases = []
    for phase in project.phases():
        pawley = bool(phase.data.get("General", {}).get("doPawley", False))
        lebail_histograms = [
            histogram_name
            for histogram_name, hap in phase.data.get("Histograms", {}).items()
            if bool(hap.get("LeBail", False))
        ]
        if pawley or lebail_histograms:
            warnings.append(
                {
                    "reason": "pawley_or_lebail_phase",
                    "phase": phase.name,
                    "pawley": pawley,
                    "lebail_histograms": lebail_histograms,
                }
            )
        linked = []
        for histogram_name, hap in phase.data.get("Histograms", {}).items():
            scale = hap.get("Scale", [None, False])
            linked.append({"histogram": histogram_name, "scale": scale})
            if scale[0] is not None and (not math.isfinite(float(scale[0])) or float(scale[0]) <= 0):
                warnings.append(
                    {
                        "reason": "nonpositive_or_nonfinite_phase_scale",
                        "phase": phase.name,
                        "histogram": histogram_name,
                        "scale": scale,
                    }
                )
        phases.append(
            {
                "name": phase.name,
                "composition": phase.composition,
                "pawley_or_lebail": bool(pawley or lebail_histograms),
                "lebail_histograms": lebail_histograms,
                "histograms": linked,
            }
        )

    covariance = project.data.get("Covariance", {}).get("data", {})
    rvalues = covariance.get("Rvals", {})
    if not rvalues.get("converged", False):
        warnings.append({"reason": "last_refinement_not_converged"})
    if int(rvalues.get("SVD0", 0) or 0) > 0:
        warnings.append({"reason": "svd_dropped_variables", "count": rvalues.get("SVD0")})
    if rvalues.get("msg"):
        warnings.append({"reason": "refinement_message", "message": rvalues.get("msg")})

    try:
        total_widths = total_width_audit(path)
        for histogram_report in total_widths:
            regeneration = histogram_report.get("saved_profile_regeneration", {})
            if regeneration.get("status") == "needs_review":
                warnings.append(
                    {
                        "reason": "saved_profile_differs_from_fresh_regeneration",
                        "histogram": histogram_report["histogram"],
                        **regeneration,
                    }
                )
            for phase_report in histogram_report.get("phases", []):
                if phase_report.get("status") != "pass":
                    warnings.append(
                        {
                            "reason": "invalid_or_nonpositive_total_peak_width_over_reflections",
                            "histogram": histogram_report["histogram"],
                            **phase_report,
                        }
                    )
    except Exception as error:
        total_widths = [{"status": "audit_error", "error": str(error)}]
        warnings.append({"reason": "total_width_audit_error", "error": str(error)})

    result = {
        "project": str(path),
        "status": "needs_review" if warnings else "no_audit_flags",
        "warnings": warnings,
        "histograms": histograms,
        "phases": phases,
        "total_peak_width_audit": total_widths,
        "convergence": {
            "converged": rvalues.get("converged"),
            "svd_dropped_variables": rvalues.get("SVD0"),
            "reported_max_shift_over_esd": rvalues.get("Max shft/sig"),
            "message": rvalues.get("msg"),
        },
        "scope": (
            "Read-only numerical/model-integrity audit; full-pattern residuals, "
            "chemistry, parameter plausibility and export consistency still require review."
        ),
    }
    if args.summary:
        result = {
            key: result[key]
            for key in (
                "project",
                "status",
                "warnings",
                "total_peak_width_audit",
                "convergence",
                "scope",
            )
        }
    print(json.dumps(result, indent=None if args.compact else 2, default=str))


if __name__ == "__main__":
    main()
