#!/usr/bin/env python3
"""Rank mapped oxide prototypes against an observed-minus-calculated profile.

The input JSON is produced by prototype_routes.py. This is a research
prototype: its approximate Cu K-alpha1 fingerprint search is for shortlisting,
not phase rejection or quantitative refinement.
"""

from __future__ import annotations

import argparse
import json
import warnings
from pathlib import Path

import numpy as np
from pymatgen.analysis.diffraction.xrd import XRDCalculator
from pymatgen.core import Structure
from scipy.ndimage import gaussian_filter1d, maximum_filter1d


def cod_path(root: Path, record_id: str) -> Path:
    return root / record_id[0] / record_id[1:3] / record_id[3:5] / f"{record_id}.cif"


def load_profile(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    data = np.genfromtxt(path, delimiter=",", names=True)
    if not data.dtype.names:
        raise ValueError("profile must have a CSV header")
    names = {name.lower(): name for name in data.dtype.names}

    def pick(options: tuple[str, ...]) -> str:
        for option in options:
            if option in names:
                return names[option]
        raise ValueError(f"missing one of profile columns {options}; found {data.dtype.names}")

    def pick_optional(options: tuple[str, ...]) -> str | None:
        for option in options:
            if option in names:
                return names[option]
        return None

    x_name = pick(("two_theta_deg", "two_theta", "x"))
    observed_name = pick(("observed", "intensity", "obs"))
    calculated_name = pick_optional(("calculated", "calc"))
    x = np.asarray(data[x_name], dtype=float)
    observed = np.asarray(data[observed_name], dtype=float)
    calculated = (
        np.zeros_like(observed)
        if calculated_name is None
        else np.asarray(data[calculated_name], dtype=float)
    )
    return x, observed, observed - calculated


def score_pattern(
    x: np.ndarray,
    evidence: np.ndarray,
    positions: np.ndarray,
    intensities: np.ndarray,
    scales: np.ndarray,
    shifts: np.ndarray,
) -> tuple[float, float, float]:
    best = (-np.inf, float("nan"), float("nan"))
    theta = np.deg2rad(positions / 2.0)
    for scale in scales:
        sine = np.sin(theta) / scale
        valid = (sine > 0.0) & (sine < 1.0)
        if np.count_nonzero(valid) < 3:
            continue
        base = 2.0 * np.rad2deg(np.arcsin(sine[valid]))
        weights = intensities[valid]
        for shift in shifts:
            transformed = base + shift
            inside = (transformed >= x[0]) & (transformed <= x[-1])
            if np.count_nonzero(inside) < 3:
                continue
            values = np.interp(transformed[inside], x, evidence)
            ww = weights[inside]
            score = float(np.sum(ww * values) / (np.sqrt(np.sum(ww * ww)) + 1e-12))
            if score > best[0]:
                best = (score, float(scale), float(shift))
    return best


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("routes", type=Path, help="JSON from prototype_routes.py")
    parser.add_argument("profile", type=Path, help="CSV with two_theta, observed and calculated")
    parser.add_argument("--cif-root", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--prelimit", type=int, default=400, help="routes scored (default: 400)")
    parser.add_argument("--limit", type=int, default=40, help="ranked routes returned (default: 40)")
    parser.add_argument("--max-sites", type=int, default=160)
    parser.add_argument("--scale-min", type=float, default=0.75)
    parser.add_argument("--scale-max", type=float, default=1.30)
    parser.add_argument("--scale-steps", type=int, default=221)
    parser.add_argument("--shift-min", type=float, default=-0.5)
    parser.add_argument("--shift-max", type=float, default=0.5)
    parser.add_argument("--shift-steps", type=int, default=21)
    parser.add_argument("--smooth-deg", type=float, default=0.04)
    parser.add_argument("--peak-tolerance-deg", type=float, default=0.12)
    parser.add_argument("--minimum-relative-intensity", type=float, default=0.0075)
    args = parser.parse_args()

    source = json.loads(args.routes.read_text())
    routes = source["routes"][: max(0, args.prelimit)]
    x, observed, residual = load_profile(args.profile)
    step = float(np.median(np.diff(x)))
    evidence = residual / np.sqrt(np.maximum(observed, 1.0))
    evidence = gaussian_filter1d(evidence, max(args.smooth_deg / step, 0.0))
    evidence = maximum_filter1d(
        evidence, size=max(1, int(round(args.peak_tolerance_deg / step)))
    )
    middle = (x >= np.quantile(x, 0.05)) & (x <= np.quantile(x, 0.95))
    evidence -= float(np.median(evidence[middle]))

    scales = np.linspace(args.scale_min, args.scale_max, args.scale_steps)
    shifts = np.linspace(args.shift_min, args.shift_max, args.shift_steps)
    calculator = XRDCalculator(wavelength=1.540598)
    ranked: list[dict[str, object]] = []
    for number, route in enumerate(routes, 1):
        record_id = str(route["record_id"])
        candidate = dict(route)
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                structure = Structure.from_file(cod_path(args.cif_root, record_id), primitive=False)
            if len(structure) > args.max_sites:
                continue
            structure.remove_oxidation_states()
            structure.replace_species(route["mapping"])
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                pattern = calculator.get_pattern(
                    structure, two_theta_range=(max(1.0, x[0] - 5.0), x[-1] + 15.0), scaled=True
                )
            positions = np.asarray(pattern.x, dtype=float)
            intensities = np.asarray(pattern.y, dtype=float) / 100.0
            keep = intensities >= args.minimum_relative_intensity
            positions, intensities = positions[keep], intensities[keep]
            if len(positions) < 3:
                continue
            score, scale, shift = score_pattern(
                x, evidence, positions, intensities, scales, shifts
            )
            candidate.update(
                {
                    "powder_score": score,
                    "best_isotropic_lattice_scale": scale,
                    "best_shift_deg": shift,
                    "sites": len(structure),
                    "calculated_lines_used": len(positions),
                }
            )
            ranked.append(candidate)
        except Exception as exc:
            candidate["ranking_error"] = f"{type(exc).__name__}: {exc}"
        if number % 50 == 0:
            print(f"scored {number}/{len(routes)}", flush=True)

    ranked.sort(key=lambda row: (-row["powder_score"], row["substitution_count"], row["record_id"]))
    result = {
        "target_formula": source.get("target_formula"),
        "profile": str(args.profile),
        "routes_considered": len(routes),
        "routes_scored": len(ranked),
        "warning": (
            "Approximate isotropic powder matching is a shortlist only. Complete common-state "
            "Rietveld trials and physical screening before accepting or rejecting a structure."
        ),
        "ranking": ranked[: max(0, args.limit)],
    }
    rendered = json.dumps(result, indent=2) + "\n"
    if args.out:
        args.out.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
