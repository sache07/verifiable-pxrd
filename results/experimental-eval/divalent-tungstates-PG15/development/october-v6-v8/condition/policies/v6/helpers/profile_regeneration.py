#!/usr/bin/env python3
"""Regenerate a GSAS-II powder project's saved full-grid profile in place."""

from __future__ import annotations

import copy
import sys
from pathlib import Path

import numpy as np
from scipy.interpolate import interp1d
from GSASII import GSASIIscriptable as G2sc
from GSASII import GSASIIstrIO as G2io
from GSASII import GSASIIstrMath as G2math


def empirical_background(kind: str, coefficients: list[float], x, domain):
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
            knots = np.exp(np.linspace(np.log(lower), np.log(upper), len(coefficients)))
        knots[0], knots[-1] = lower, upper
        return interp1d(
            knots, coefficients, bounds_error=False, fill_value="extrapolate"
        )(x)
    return None


def regenerate_profile(path: Path) -> None:
    all_histograms, all_phases = G2io.GetUsedHistogramsAndPhases(str(path))
    powder_names = [name for name in all_histograms if name.startswith("PWDR")]
    if len(powder_names) != 1:
        raise ValueError(f"expected one powder histogram, found {len(powder_names)}")
    histogram_name = powder_names[0]
    source_histogram = all_histograms[histogram_name]
    histogram = copy.deepcopy(source_histogram)
    histograms = {histogram_name: histogram}
    phases = {
        phase_name: copy.deepcopy(phase)
        for phase_name, phase in all_phases.items()
        if histogram_name in phase.get("Histograms", {})
        and phase["Histograms"][histogram_name].get("Use", True)
        and phase["Histograms"][histogram_name]["Scale"][0] != 0
    }
    x = np.asarray(histogram["Data"][0], dtype=float)
    observed = np.asarray(histogram["Data"][1], dtype=float)
    old_limits = copy.deepcopy(histogram["Limits"])
    lower_index, upper_index = np.searchsorted(x, old_limits[1])
    upper_index = min(len(x) - 1, upper_index)
    background_domain = [float(x[lower_index]), float(x[upper_index])]
    histogram["Limits"] = [
        [float(x[0]), float(x[-1])],
        [float(x[0]), float(x[-1])],
    ]
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
        histogram_name,
    )
    histogram_prefix = f":{histogram['hId']}:"
    background_kind = controls[histogram_prefix + "bakType"]
    coefficients = []
    while histogram_prefix + f"Back;{len(coefficients)}" in parameters:
        coefficients.append(parameters[histogram_prefix + f"Back;{len(coefficients)}"])
    saved_background = empirical_background(
        background_kind, coefficients, x, background_domain
    )
    if saved_background is not None:
        full_background = empirical_background(
            background_kind, coefficients, x, [float(x[0]), float(x[-1])]
        )
        background = background + saved_background - full_background
    calculated = np.asarray(signal + background, dtype=float)

    project = G2sc.G2Project(str(path))
    wrapper = project.histogram(histogram_name)
    arrays = wrapper.data["data"][1]
    arrays[3][:] = calculated
    arrays[4][:] = np.asarray(background, dtype=float)
    arrays[5][:] = observed - calculated
    wrapper.data["Reflection Lists"] = copy.deepcopy(histogram["Reflection Lists"])
    project.save(str(path))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: profile_regeneration.py PROJECT.gpx")
    regenerate_profile(Path(sys.argv[1]).resolve())
