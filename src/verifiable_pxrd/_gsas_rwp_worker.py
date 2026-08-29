#!/usr/bin/env python3
"""Internal GSAS-II worker for the blind comparable-fit Rwp protocol.

This file is launched with the dedicated GSAS-II Python environment.  The public
orchestration and CLI live in :mod:`verifiable_pxrd.rwp_verifier`.
"""

from __future__ import annotations

import json
import math
import sys
import tempfile
from importlib.metadata import version
from pathlib import Path
from typing import Any

import numpy as np


def _write_inputs(root: Path, request: dict[str, Any]) -> tuple[Path, Path, Path]:
    pattern = root / "pattern.xye"
    two_theta = np.asarray(request["two_theta"], dtype=float)
    intensity = np.asarray(request["intensity"], dtype=float)
    np.savetxt(
        pattern,
        np.column_stack((two_theta, intensity, np.ones_like(intensity))),
        fmt="%.12g",
    )

    candidate = root / "candidate.cif"
    candidate.write_text(str(request["candidate_cif"]), encoding="utf-8")

    profile = request["initial_profile"]
    instrument = root / "blind-comparable.instprm"
    instrument.write_text(
        "#GSAS-II blind comparable-fit baseline; initialized from observed widths\n"
        "Type:PXC;Bank:1\n"
        f"Lam:{float(request['wavelength_angstrom']):.12g};"
        "Zero:0.0;Polariz.:0.5;Azimuth:0.0\n"
        f"U:{float(profile['u']):.12g};V:0.0;W:{float(profile['w']):.12g};"
        "X:0.0;Y:0.0;Z:0.0;SH/L:0.0\n",
        encoding="utf-8",
    )
    return pattern, candidate, instrument


def _set_bounds(project: Any) -> None:
    bounds = {
        ":0:Zero": (-0.15, 0.15),
        ":0:U": (0.01, 200.0),
        ":0:W": (0.05, 400.0),
    }
    for variable, (minimum, maximum) in bounds.items():
        project.set_Controls("parmMin", minimum, variable=variable)
        project.set_Controls("parmMax", maximum, variable=variable)


def _instrument_values(histogram: Any) -> dict[str, float]:
    instrument = histogram.data["Instrument Parameters"][0]
    values: dict[str, float] = {}
    for name in ("Lam", "Zero", "Polariz.", "U", "V", "W", "X", "Y", "SH/L"):
        value = instrument.get(name)
        if isinstance(value, (list, tuple)) and len(value) > 1:
            values[name] = float(value[1])
    return values


def _uniform_rwp(histogram: Any) -> tuple[float, int]:
    _x, observed, _weights, calculated, _background, _residual = histogram.data["data"][1]
    observed_array = np.asarray(observed, dtype=float)
    calculated_array = np.asarray(calculated, dtype=float)
    if not np.all(np.isfinite(observed_array)) or not np.all(np.isfinite(calculated_array)):
        raise RuntimeError("GSAS-II produced a non-finite profile")
    denominator = float(np.sum(np.square(observed_array)))
    if denominator <= 0:
        raise RuntimeError("observed profile has zero squared intensity")
    value = math.sqrt(
        float(np.sum(np.square(observed_array - calculated_array))) / denominator
    ) * 100.0
    return value, len(observed_array)


def run(request: dict[str, Any]) -> dict[str, Any]:
    from GSASII import GSASIIscriptable as scriptable

    with tempfile.TemporaryDirectory(prefix="vpbench-rwp-") as temporary:
        root = Path(temporary)
        pattern, candidate, instrument = _write_inputs(root, request)
        project = scriptable.G2Project(newgpx=str(root / "comparable-fit.gpx"))
        project.add_phase(str(candidate), phasename="candidate", fmthint="CIF")
        histogram = project.add_powder_histogram(
            str(pattern),
            str(instrument),
            phases=project.phases(),
            fmthint="xye",
        )
        sample_scale = histogram.SampleParameters.get("Scale")
        if isinstance(sample_scale, list) and len(sample_scale) > 1:
            sample_scale[1] = False

        project.set_Controls("cycles", 8)
        _set_bounds(project)
        background_start = float(request.get("background_start", 0.0))
        recipes = [
            {
                "set": {
                    "Background": {
                        "type": "chebyschev-1",
                        "refine": True,
                        "no. coeffs": 4,
                        "coeffs": [background_start, 0.0, 0.0, 0.0],
                    },
                    "PhaseFraction": True,
                }
            },
            {"set": {"Instrument Parameters": ["Zero", "W"]}},
            {"set": {"Instrument Parameters": ["U"]}},
        ]
        project.do_refinements(recipes)
        histogram = project.histogram(0)
        rwp, point_count = _uniform_rwp(histogram)
        covariance = project.data.get("Covariance", {})
        covariance_data = covariance.get("data", covariance)
        vary_list = [str(value) for value in covariance_data.get("varyList", [])]
        forbidden = [
            value
            for value in vary_list
            if any(token in value for token in ("::A", "::dA", "::AU", "::Afrac"))
        ]
        if forbidden:
            raise RuntimeError(f"structural parameters were unexpectedly refined: {forbidden}")

        gsas_residuals = {
            str(key): float(value)
            for key, value in histogram.residuals.items()
            if isinstance(value, (int, float, np.number)) and np.isfinite(float(value))
        }
        return {
            "status": "completed",
            "rwp_percent": rwp,
            "point_count": point_count,
            "gsas_residuals": gsas_residuals,
            "instrument_parameters": _instrument_values(histogram),
            "refined_parameters": vary_list,
            "frozen_structure": True,
            "gsas_ii_version": version("GSAS-II"),
        }


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: _gsas_rwp_worker.py REQUEST.json RESULT.json")
    request_path = Path(sys.argv[1])
    result_path = Path(sys.argv[2])
    try:
        result = run(json.loads(request_path.read_text(encoding="utf-8")))
    except Exception as error:
        result = {"status": "failed", "error": f"{type(error).__name__}: {error}"}
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if result["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
