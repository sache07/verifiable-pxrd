"""Blind, candidate-comparable GSAS-II Rwp ranking.

The verifier consumes only the observed pattern, its wavelength, and submitted CIFs.
Crystal structures remain fixed. Every candidate receives the same bounded nuisance
refinement, making this suitable as a test-time selector rather than an oracle replay.
"""

from __future__ import annotations

import concurrent.futures
import csv
import json
import os
import re
import shutil
import subprocess
import tempfile
import warnings
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import numpy as np
from pymatgen.core import Structure
from pymatgen.io.cif import CifWriter
from scipy.signal import find_peaks, peak_widths

from .matching import matcher
from .util import load_json, sha256_file, write_json

PROTOCOL_ID = "blind-comparable-gsas-rwp-v1"
warnings.filterwarnings("ignore", message=r"Site labels are not unique.*", category=UserWarning)
WAVELENGTH_PATTERN = re.compile(
    r"(?:at|wavelength(?:\s+of)?)\s+([0-9]+(?:\.[0-9]+)?)\s*(?:angstrom|ångström|Å)",
    re.IGNORECASE,
)


def _load_pattern(path: Path) -> tuple[np.ndarray, np.ndarray]:
    values = np.loadtxt(path, delimiter=",", skiprows=1)
    if values.ndim != 2 or values.shape[1] < 2 or len(values) < 20:
        raise ValueError(f"expected a two-column powder pattern, got {values.shape}")
    two_theta = np.asarray(values[:, 0], dtype=float)
    intensity = np.asarray(values[:, 1], dtype=float)
    if not np.all(np.isfinite(two_theta)) or not np.all(np.isfinite(intensity)):
        raise ValueError("pattern contains non-finite values")
    if np.any(np.diff(two_theta) <= 0):
        raise ValueError("two-theta values must be strictly increasing")
    return two_theta, intensity


def estimate_profile(two_theta: np.ndarray, intensity: np.ndarray) -> dict[str, Any]:
    """Estimate neutral Caglioti U/W starts from observed peak widths only."""
    step = float(np.median(np.diff(two_theta)))
    differences = np.diff(intensity)
    centered = differences - float(np.median(differences))
    noise = float(np.median(np.abs(centered)) / 0.6744897501960817 / np.sqrt(2.0))
    span = float(np.percentile(intensity, 99.9) - np.percentile(intensity, 10.0))
    prominence = max(6.0 * noise, 0.02 * span, np.finfo(float).eps)
    minimum_distance = max(2, round(0.04 / step))
    peaks, properties = find_peaks(
        intensity,
        prominence=prominence,
        distance=minimum_distance,
    )
    widths = peak_widths(intensity, peaks, rel_height=0.5)[0] * step if len(peaks) else []
    widths_array = np.asarray(widths, dtype=float)
    centers = two_theta[peaks] if len(peaks) else np.asarray([], dtype=float)
    prominences = np.asarray(properties.get("prominences", []), dtype=float)
    keep = (
        (widths_array >= 1.5 * step)
        & (widths_array <= 0.5)
        & (centers >= two_theta[0] + 0.5)
        & (centers <= two_theta[-1] - 0.5)
    )
    centers = centers[keep]
    widths_array = widths_array[keep]
    prominences = prominences[keep]
    if len(centers) > 30:
        selected = np.argsort(prominences)[-30:]
        centers = centers[selected]
        widths_array = widths_array[selected]

    if len(centers) >= 3:
        variance = np.square(100.0 * widths_array / 2.355)
        tangent_squared = np.square(np.tan(np.radians(centers / 2.0)))
        design = np.column_stack((tangent_squared, np.ones_like(tangent_squared)))
        u_value, w_value = np.linalg.lstsq(design, variance, rcond=None)[0]
        u_value = float(np.clip(u_value, 0.1, 100.0))
        w_value = float(np.clip(w_value, 0.25, 200.0))
        median_fwhm = float(np.median(widths_array))
        method = "observed-peak-width regression"
    else:
        fallback_fwhm = max(6.0 * step, 0.08)
        u_value = 5.0
        w_value = float(np.clip((100.0 * fallback_fwhm / 2.355) ** 2, 0.25, 200.0))
        median_fwhm = fallback_fwhm
        method = "grid-derived fallback"
    return {
        "u": u_value,
        "v": 0.0,
        "w": w_value,
        "median_fwhm_deg": median_fwhm,
        "peak_count_used": len(centers),
        "noise_estimate": noise,
        "prominence_threshold": prominence,
        "method": method,
    }


def _gsas_python(value: Path | None) -> Path:
    if value is not None:
        selected = value.expanduser().absolute()
    elif os.environ.get("VPBENCH_GSAS_ENV"):
        selected = Path(os.environ["VPBENCH_GSAS_ENV"]).expanduser().absolute() / "bin/python"
    else:
        raise ValueError("provide --gsas-python or set VPBENCH_GSAS_ENV")
    if not selected.is_file():
        raise FileNotFoundError(f"GSAS-II Python not found: {selected}")
    return selected


def _canonical_cif(path: Path) -> str:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        structure = Structure.from_file(path, primitive=False)
        return str(CifWriter(structure, symprec=None))


def _read_structure(path: Path) -> Structure:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        return Structure.from_file(path, primitive=False)


def _fit_candidate(
    candidate: Path,
    two_theta: np.ndarray,
    intensity: np.ndarray,
    wavelength: float,
    profile: dict[str, Any],
    gsas_python: Path,
    timeout_seconds: int,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "candidate": str(candidate.resolve()),
        "sha256": sha256_file(candidate),
    }
    try:
        candidate_cif = _canonical_cif(candidate)
    except Exception as error:
        return {**record, "status": "failed", "error": f"CIF parse: {type(error).__name__}: {error}"}
    request = {
        "two_theta": two_theta.tolist(),
        "intensity": intensity.tolist(),
        "wavelength_angstrom": wavelength,
        "candidate_cif": candidate_cif,
        "initial_profile": profile,
        "background_start": float(np.percentile(intensity, 10.0)),
    }
    worker = Path(__file__).with_name("_gsas_rwp_worker.py")
    with tempfile.TemporaryDirectory(prefix="vpbench-rwp-driver-") as temporary:
        root = Path(temporary)
        request_path = root / "request.json"
        result_path = root / "result.json"
        request_path.write_text(json.dumps(request), encoding="utf-8")
        try:
            process = subprocess.run(
                [str(gsas_python), str(worker), str(request_path), str(result_path)],
                text=True,
                capture_output=True,
                check=False,
                timeout=timeout_seconds,
            )
        except subprocess.TimeoutExpired:
            return {**record, "status": "failed", "error": "GSAS-II fit timed out"}
        if result_path.is_file():
            result = load_json(result_path)
        else:
            detail = (process.stderr or process.stdout).strip()
            result = {"status": "failed", "error": detail or f"GSAS-II exited {process.returncode}"}
    return {**record, **result}


def _equivalence_groups(results: list[dict[str, Any]]) -> None:
    active = matcher()
    groups: list[tuple[str, Structure]] = []
    for result in sorted(
        (item for item in results if item.get("status") == "completed"),
        key=lambda item: (float(item["rwp_percent"]), str(item["candidate"])),
    ):
        try:
            structure = _read_structure(Path(result["candidate"]))
        except Exception:
            continue
        group_id = None
        for candidate_group, representative in groups:
            try:
                if active.fit(representative, structure, symmetric=True):
                    group_id = candidate_group
                    break
            except Exception:
                continue
        if group_id is None:
            group_id = f"structure-{len(groups) + 1:03d}"
            groups.append((group_id, structure))
        result["structure_group"] = group_id


def _protocol(profile: dict[str, Any], wavelength: float) -> dict[str, Any]:
    return {
        "id": PROTOCOL_ID,
        "inputs": ["observed pattern", "wavelength", "candidate CIFs"],
        "fixed": ["lattice", "atomic coordinates", "species", "occupancies"],
        "canonicalization": (
            "Candidates are expanded to an equivalent P1 CIF for backend robustness; "
            "the periodic structure is unchanged."
        ),
        "fitted_identically_per_candidate": [
            "phase scale",
            "four Chebyshev background coefficients",
            "zero shift bounded to +/-0.15 degrees",
            "Gaussian Caglioti U and W with V fixed at zero",
        ],
        "weighting": "uniform point weights because the supplied CSV has no uncertainties",
        "other_profile_terms": (
            "V, X, Y, polarization, and axial-asymmetry terms use the same neutral fixed "
            "baseline for every candidate."
        ),
        "rwp": "sqrt(sum((y_obs-y_calc)^2)/sum(y_obs^2))*100 after the bounded fit",
        "wavelength_angstrom": wavelength,
        "initial_profile": profile,
        "interpretation": (
            "A comparable profile-fit ranking, not proof of structural identity; wrong cells, "
            "orderings, or coordinate models can retain low Rwp."
        ),
    }


def _write_scores(path: Path, results: list[dict[str, Any]]) -> None:
    fields = ["rank", "status", "rwp_percent", "structure_group", "sha256", "candidate", "error"]
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        rank = 0
        for result in results:
            if result.get("status") == "completed":
                rank += 1
            writer.writerow(
                {
                    "rank": rank if result.get("status") == "completed" else "",
                    "status": result.get("status"),
                    "rwp_percent": result.get("rwp_percent", ""),
                    "structure_group": result.get("structure_group", ""),
                    "sha256": result.get("sha256", ""),
                    "candidate": result.get("candidate", ""),
                    "error": result.get("error", ""),
                }
            )


def score_case(
    pattern: Path,
    wavelength: float,
    candidates: Iterable[Path],
    output: Path,
    gsas_python: Path | None = None,
    parallel: int = 1,
    timeout_seconds: int = 300,
) -> dict[str, Any]:
    pattern = pattern.resolve()
    output = output.resolve()
    if output.is_file() or (output.exists() and any(output.iterdir())):
        raise FileExistsError(f"output directory is not empty: {output}")
    output.mkdir(parents=True, exist_ok=True)
    paths = [path.resolve() for path in candidates]
    if not paths:
        raise ValueError("no candidate CIFs were supplied")
    missing = [path for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"candidate CIF not found: {missing[0]}")
    if parallel < 1:
        raise ValueError("parallel must be positive")
    two_theta, intensity = _load_pattern(pattern)
    profile = estimate_profile(two_theta, intensity)
    interpreter = _gsas_python(gsas_python)

    by_digest: dict[str, Path] = {}
    occurrences: dict[str, list[str]] = {}
    for path in paths:
        digest = sha256_file(path)
        by_digest.setdefault(digest, path)
        occurrences.setdefault(digest, []).append(str(path))
    unique = list(by_digest.values())

    def fit(path: Path) -> dict[str, Any]:
        return _fit_candidate(
            path,
            two_theta,
            intensity,
            wavelength,
            profile,
            interpreter,
            timeout_seconds,
        )

    with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as executor:
        results = list(executor.map(fit, unique))
    for result in results:
        result["occurrences"] = occurrences[result["sha256"]]
    results.sort(
        key=lambda item: (
            item.get("status") != "completed",
            float(item.get("rwp_percent", float("inf"))),
            str(item["candidate"]),
        )
    )
    _equivalence_groups(results)
    completed = [item for item in results if item.get("status") == "completed"]
    selected = completed[0] if completed else None
    submission = output / "submission"
    if selected is not None:
        submission.mkdir(parents=True, exist_ok=True)
        shutil.copy2(selected["candidate"], submission / "selected.cif")

    report = {
        "schema_version": "1",
        "valid": selected is not None,
        "pattern": str(pattern),
        "pattern_sha256": sha256_file(pattern),
        "candidate_count": len(paths),
        "unique_candidate_count": len(unique),
        "completed_fit_count": len(completed),
        "gsas_python": str(interpreter),
        "selected": None
        if selected is None
        else {
            "candidate": selected["candidate"],
            "sha256": selected["sha256"],
            "rwp_percent": selected["rwp_percent"],
            "structure_group": selected.get("structure_group"),
        },
        "protocol": _protocol(profile, wavelength),
        "results": results,
    }
    write_json(output / "report.json", report)
    _write_scores(output / "scores.csv", results)
    return report


def _wavelength(problem_dir: Path, fallback: float | None) -> float:
    prompt = problem_dir / "problem_input/prompt.md"
    if prompt.is_file():
        match = WAVELENGTH_PATTERN.search(prompt.read_text(encoding="utf-8"))
        if match:
            return float(match.group(1))
    if fallback is not None:
        return float(fallback)
    raise ValueError(f"could not determine wavelength for {problem_dir.name}")


def _source_candidates(source: Path) -> dict[str, list[Path]]:
    source = source.resolve()
    bundle_path = source / "bundle.json"
    found: dict[str, list[Path]] = {}
    if bundle_path.is_file():
        for record in load_json(bundle_path).get("cases", []):
            case_id = str(record.get("case_id") or record.get("problem_id"))
            options = [
                source / "attempts" / case_id / "submission",
                source / "attempts" / str(record.get("source_attempt_name")) / "submission",
            ]
            directory = next((path for path in options if path.is_dir()), None)
            if directory is not None:
                found.setdefault(case_id, []).extend(sorted(directory.glob("*.cif")))
        return found
    for directory in sorted(source.glob("attempts/*/submission")):
        match = re.search(r"(?:^|[^a-z0-9])(vh-\d{3})(?:[^a-z0-9]|$)", directory.parent.name)
        if match:
            found.setdefault(match.group(1), []).extend(sorted(directory.glob("*.cif")))
    return found


def _expand_sources(sources: Iterable[Path]) -> list[Path]:
    expanded: list[Path] = []
    for raw in sources:
        source = raw.resolve()
        replicate_bundles = sorted(source.glob("replicate-*/bundle.json"))
        if not (source / "bundle.json").is_file() and replicate_bundles:
            expanded.extend(path.parent for path in replicate_bundles)
        else:
            expanded.append(source)
    return list(dict.fromkeys(expanded))


def score_monkey_bundles(
    panel: Path,
    sources: Iterable[Path],
    output: Path,
    gsas_python: Path | None = None,
    parallel: int = 1,
    wavelength: float | None = None,
    timeout_seconds: int = 300,
) -> dict[str, Any]:
    panel = panel.resolve()
    if panel.is_file():
        manifest_path = panel
        panel = panel.parent
    else:
        manifest_path = panel / "manifest.json"
    manifest = load_json(manifest_path)
    output = output.resolve()
    if output.is_file() or (output.exists() and any(output.iterdir())):
        raise FileExistsError(f"output directory is not empty: {output}")
    output.mkdir(parents=True, exist_ok=True)

    candidate_map: dict[str, list[Path]] = {}
    source_paths = _expand_sources(sources)
    if not source_paths:
        raise ValueError("at least one monkey result bundle is required")
    for source in source_paths:
        for case_id, paths in _source_candidates(source).items():
            candidate_map.setdefault(case_id, []).extend(paths)

    cases: list[dict[str, Any]] = []
    for problem in sorted(manifest["problems"], key=lambda item: int(item["order"])):
        case_id = str(problem["problem_id"])
        problem_dir = panel / "problems" / case_id
        pattern = problem_dir / "problem_input/pattern.csv"
        candidates = candidate_map.get(case_id, [])
        case_output = output / "cases" / case_id
        if not candidates:
            case_output.mkdir(parents=True, exist_ok=True)
            report = {
                "schema_version": "1",
                "valid": False,
                "case_id": case_id,
                "error": "no submitted candidate CIFs found",
            }
            write_json(case_output / "report.json", report)
        else:
            report = score_case(
                pattern,
                _wavelength(problem_dir, wavelength),
                candidates,
                case_output,
                gsas_python=gsas_python,
                parallel=parallel,
                timeout_seconds=timeout_seconds,
            )
            report["case_id"] = case_id
            write_json(case_output / "report.json", report)
        cases.append(
            {
                "case_id": case_id,
                "valid": bool(report.get("valid")),
                "candidate_count": len(candidates),
                "selected": report.get("selected"),
            }
        )
    summary = {
        "schema_version": "1",
        "valid": all(item["valid"] for item in cases),
        "protocol_id": PROTOCOL_ID,
        "panel": str(panel),
        "sources": [str(path) for path in source_paths],
        "case_count": len(cases),
        "selected_case_count": sum(item["valid"] for item in cases),
        "cases": cases,
    }
    write_json(output / "summary.json", summary)
    return summary
