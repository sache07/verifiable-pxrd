"""Build and audit Crystalyze-native deterministic pXRD targets for a corpus.

The calculation reproduces the non-augmented profile in the authors' data
pipeline: Pymatgen CuKa sticks, Gaussian Caglioti broadening with
U/V/W = 0.05/-0.06/0.07, a 5--90 degree 2theta grid at 0.01 degree spacing,
and max normalization.

Use the pinned upstream numerical environment documented in
``baselines/crystalyze/README.md``::

    python baselines/crystalyze/make_targets.py build
    python baselines/crystalyze/make_targets.py audit
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
import warnings
from importlib.metadata import version
from pathlib import Path, PurePosixPath
from typing import Any

import numpy as np
from pymatgen.analysis.diffraction.xrd import XRDCalculator
from pymatgen.core import Structure

from verifiable_pxrd.baselines.targets import (
    SUPPORT_POLICIES,
    configure_paths,
    framework_support,
    relative_reference,
    validate_source_manifest,
)

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = ROOT.parent
CORPUS = REPOSITORY_ROOT / "pxrd-bench" / "pXRD-100"
OUTPUT = configure_paths(CORPUS, "crystalyze")["output"]
PATTERNS = OUTPUT / "patterns"
SOURCE_MANIFEST = CORPUS / "manifest.json"
OUTPUT_MANIFEST = OUTPUT / "manifest.json"
PARAMETERS_PATH = OUTPUT / "parameters.json"
INPUTS_PATH = OUTPUT / "inputs.csv"
DATASET_ID: str | None = None
CASE_PREFIX: str | None = None
SUPPORT_POLICY = "manifest"

EXPECTED_CASES = 100
EXPECTED_VERSIONS = {
    "monty": "2023.9.25",
    "numpy": "1.24.3",
    "pymatgen": "2023.8.10",
    "scipy": "1.10.1",
    "spglib": "2.3.0",
}
EXPECTED_PYTHON = "3.8.18"
WAVELENGTH_ANGSTROM = 1.54184
U, V, W = 0.05, -0.06, 0.07
ETA = 0.0
TWO_THETA_START = 5.0
TWO_THETA_STOP = 90.0
TWO_THETA_STEP = 0.010
POINT_COUNT = 8500
MODEL_MASKED_BINS = 1000
PIPELINE_COMMIT = "4940d2c228e87acfe6fc7fef43b9d0bf18bd1374"
CHECKOUT_COMMIT = "d265e8b4687fda9586a73f3eb881bb881171b05b"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    temporary = path.with_suffix(path.suffix + ".partial")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def assert_numerical_environment() -> dict[str, str]:
    versions = {name: version(name) for name in EXPECTED_VERSIONS}
    versions["python"] = platform.python_version()
    expected = {**EXPECTED_VERSIONS, "python": EXPECTED_PYTHON}
    if versions != expected:
        raise RuntimeError(
            f"expected numerical environment {expected}, found {versions}; "
            "see baselines/crystalyze/README.md"
        )
    calculator = XRDCalculator(wavelength="CuKa")
    if not math.isclose(calculator.wavelength, WAVELENGTH_ANGSTROM, abs_tol=1e-12):
        raise RuntimeError(
            f"Pymatgen CuKa resolved to {calculator.wavelength}, expected {WAVELENGTH_ANGSTROM}"
        )
    return versions


def axis() -> np.ndarray:
    values = np.arange(TWO_THETA_START, TWO_THETA_STOP, TWO_THETA_STEP, dtype=np.float64)
    if len(values) != POINT_COUNT or not math.isclose(values[-1], 89.99, abs_tol=1e-10):
        raise RuntimeError(f"unexpected Crystalyze axis: {len(values)} points, last={values[-1]}")
    return values


def parameters() -> dict[str, Any]:
    return {
        "background": "none",
        "broadening": {
            "caglioti": {"U": U, "V": V, "W": W},
            "fwhm_equation": "sqrt(U*tan(theta)^2 + V*tan(theta) + W)",
            "profile": "gaussian",
            "pseudo_voigt_eta": ETA,
            "theta_definition": "theta = two_theta_peak / 2, in radians inside tan",
        },
        "debye_waller_factors": "none",
        "grid": {
            "point_count": POINT_COUNT,
            "start_deg": TWO_THETA_START,
            "step_deg": TWO_THETA_STEP,
            "stop_deg_exclusive": TWO_THETA_STOP,
            "last_point_deg": 89.99,
        },
        "intensity": {
            "normalization": "divide broadened profile by its maximum",
            "range": [0.0, 1.0],
        },
        "model_preprocessing": {
            "inference_resampling": "np.linspace(5, 90, 8500)",
            "masked_leading_bins": MODEL_MASKED_BINS,
            "effective_nonzero_range_deg": [15.0, 90.0],
            "note": (
                "Mask is applied by CrystDataset after loading; files retain the "
                "unmasked physical profile."
            ),
        },
        "preferred_orientation": "none",
        "stick_calculation": {
            "calculator": "pymatgen.analysis.diffraction.xrd.XRDCalculator",
            "pymatgen_version": EXPECTED_VERSIONS["pymatgen"],
            "scaled_maximum": 100.0,
            "symprec": 0.0,
            "two_theta_range_deg": [0.0, 90.0],
        },
        "wavelength": {
            "angstrom": WAVELENGTH_ANGSTROM,
            "pymatgen_key": "CuKa",
            "radiation": "Cu K-alpha",
        },
    }


def configure_dataset(args: argparse.Namespace) -> None:
    global CORPUS, OUTPUT, PATTERNS, SOURCE_MANIFEST, OUTPUT_MANIFEST
    global PARAMETERS_PATH, INPUTS_PATH, DATASET_ID, CASE_PREFIX, SUPPORT_POLICY
    paths = configure_paths(args.corpus_root, "crystalyze", args.output_root)
    CORPUS = paths["corpus"]
    OUTPUT = paths["output"]
    PATTERNS = paths["patterns"]
    SOURCE_MANIFEST = paths["source_manifest"]
    OUTPUT_MANIFEST = paths["output_manifest"]
    PARAMETERS_PATH = OUTPUT / "parameters.json"
    INPUTS_PATH = OUTPUT / "inputs.csv"
    DATASET_ID = args.dataset_id
    CASE_PREFIX = args.case_prefix
    SUPPORT_POLICY = args.support_policy


def load_source_cases() -> list[dict[str, Any]]:
    source = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
    _, cases = validate_source_manifest(
        source,
        expected_cases=EXPECTED_CASES,
        dataset_id=DATASET_ID,
        case_prefix=CASE_PREFIX,
    )
    return cases


def source_path(case: dict[str, Any]) -> Path:
    relative = PurePosixPath(case["path"])
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"unsafe source path: {relative}")
    path = CORPUS / relative
    if sha256_file(path) != case["sha256"]:
        raise RuntimeError(f"source CIF digest mismatch: {path}")
    return path


def simulate(structure: Structure, sample_axis: np.ndarray) -> tuple[np.ndarray, dict[str, Any]]:
    calculator = XRDCalculator(wavelength="CuKa", symprec=0)
    # The authors call get_pattern without a range, so use Pymatgen's (0, 90)
    # default rather than truncating sticks at the output grid's 5-degree start.
    sticks = calculator.get_pattern(structure)
    centers = np.asarray(sticks.x, dtype=np.float64)
    amplitudes = np.asarray(sticks.y, dtype=np.float64)
    if len(centers) != len(amplitudes):
        raise RuntimeError("Pymatgen returned mismatched stick positions and intensities")
    profile = np.zeros_like(sample_axis)
    fwhms: list[float] = []
    for center, amplitude in zip(centers, amplitudes):  # noqa: B905 - Python 3.8
        theta = math.radians(float(center) / 2.0)
        fwhm = math.sqrt(U * math.tan(theta) ** 2 + V * math.tan(theta) + W)
        sigma = fwhm / (2.0 * math.sqrt(2.0 * math.log(2.0)))
        profile += amplitude * np.exp(-np.square(sample_axis - center) / (2.0 * sigma**2))
        fwhms.append(fwhm)
    maximum = float(np.max(profile))
    if not math.isfinite(maximum) or maximum <= 0:
        raise RuntimeError("simulated profile is empty or non-finite")
    profile /= maximum
    metadata = {
        "broadened_intensity_max_before_normalization": maximum,
        "caglioti_fwhm_deg_max": max(fwhms),
        "caglioti_fwhm_deg_min": min(fwhms),
        "stick_peak_count": len(centers),
        "stick_two_theta_deg_max": float(np.max(centers)),
        "stick_two_theta_deg_min": float(np.min(centers)),
    }
    return profile, metadata


def write_pattern(path: Path, sample_axis: np.ndarray, profile: np.ndarray) -> None:
    if len(sample_axis) != len(profile):
        raise RuntimeError("pattern axis and profile lengths differ")
    temporary = path.with_suffix(path.suffix + ".partial")
    with temporary.open("w", encoding="utf-8", newline="") as stream:
        stream.write("two_theta_deg,intensity_normalized\n")
        for two_theta, intensity in zip(  # noqa: B905 - Python 3.8
            sample_axis, profile
        ):
            stream.write(f"{two_theta:.5f},{intensity:.10e}\n")
    temporary.replace(path)


def build() -> None:
    versions = assert_numerical_environment()
    cases = load_source_cases()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    PATTERNS.mkdir(parents=True, exist_ok=True)
    sample_axis = axis()
    output_cases: list[dict[str, Any]] = []
    input_rows: list[dict[str, Any]] = []
    for index, case in enumerate(cases, start=1):
        cif_path = source_path(case)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            structure = Structure.from_file(cif_path)
        profile, simulation_metadata = simulate(structure, sample_axis)
        relative_pattern = PurePosixPath("patterns") / f"{case['case_id']}.xy"
        pattern_path = OUTPUT / relative_pattern
        write_pattern(pattern_path, sample_axis, profile)
        exposure, supported = framework_support(
            case, framework_key="crystalyze", policy=SUPPORT_POLICY
        )
        output_cases.append(
            {
                "case_id": case["case_id"],
                "composition": case["formula"],
                "elements": case["elements"],
                "framework_applicability": exposure,
                "model_supported": supported,
                "panel": case["panel"],
                "pattern_path": relative_pattern.as_posix(),
                "pattern_sha256": sha256_file(pattern_path),
                "primitive_site_count": case["primitive_site_count"],
                "source_cif_path": case["path"],
                "source_cif_sha256": case["sha256"],
                **simulation_metadata,
            }
        )
        input_rows.append(
            {
                "case_id": case["case_id"],
                "panel": case["panel"],
                "composition": case["formula"],
                "elements": " ".join(case["elements"]),
                "pattern_path": relative_pattern.as_posix(),
                "crystalyze_applicability": exposure,
            }
        )
        if index % 10 == 0 or index == len(cases):
            print(f"generated {index}/{len(cases)} patterns")

    with INPUTS_PATH.with_suffix(".csv.partial").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(input_rows[0]))
        writer.writeheader()
        writer.writerows(input_rows)
    INPUTS_PATH.with_suffix(".csv.partial").replace(INPUTS_PATH)
    write_json(PARAMETERS_PATH, parameters())
    write_json(
        OUTPUT_MANIFEST,
        {
            "cases": output_cases,
            "framework": "Crystalyze",
            "framework_checkout_commit": CHECKOUT_COMMIT,
            "generator": "baselines/crystalyze/make_targets.py",
            "source_dataset_id": json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))[
                "dataset_id"
            ],
            "case_prefix": CASE_PREFIX,
            "support_policy": SUPPORT_POLICY,
            "numerical_environment": versions,
            "parameter_file": "parameters.json",
            "parameter_sources": {
                "article_doi": "10.1021/jacs.4c10244",
                "pymatgen_xrd_source": "https://github.com/materialsproject/pymatgen/blob/v2023.8.10/pymatgen/analysis/diffraction/xrd.py",
                "preprocessing_notebook_commit": PIPELINE_COMMIT,
                "preprocessing_notebook_sha256": (
                    "c71ef4246621f0c2dd5154d54a84e87ea4e200e0a009425761c6d224e02971e3"
                ),
                "supporting_information_doi": "10.1021/jacs.4c10244.s001",
                "supporting_information_pdf_sha256": (
                    "210ebfde40cb35854854f94ab780a2682a215c05c07e75e667325f80c0566c0a"
                ),
            },
            "pattern_count": len(output_cases),
            "schema_version": "1.0.0",
            "source_manifest": relative_reference(SOURCE_MANIFEST, from_directory=OUTPUT),
            "source_manifest_sha256": sha256_file(SOURCE_MANIFEST),
            "supported_case_count": sum(case["model_supported"] for case in output_cases),
            "unsupported_case_count": sum(not case["model_supported"] for case in output_cases),
        },
    )


def audit() -> None:
    assert_numerical_environment()
    source_cases = {case["case_id"]: case for case in load_source_cases()}
    manifest = json.loads(OUTPUT_MANIFEST.read_text(encoding="utf-8"))
    cases = manifest["cases"]
    errors: list[str] = []
    max_resimulation_error = 0.0
    expected_axis = axis()
    if len(cases) != EXPECTED_CASES:
        errors.append(f"pattern count {len(cases)} != {EXPECTED_CASES}")
    if manifest["source_manifest_sha256"] != sha256_file(SOURCE_MANIFEST):
        errors.append("source manifest digest mismatch")
    expected_supported = sum(
        framework_support(case, framework_key="crystalyze", policy=SUPPORT_POLICY)[1]
        for case in source_cases.values()
    )
    source_dataset_id = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))["dataset_id"]
    if manifest.get("source_dataset_id", source_dataset_id) != source_dataset_id:
        errors.append("source dataset ID mismatch")
    if manifest.get("case_prefix") != CASE_PREFIX:
        errors.append("case-prefix contract mismatch")
    if manifest.get("support_policy", "manifest") != SUPPORT_POLICY:
        errors.append("support-policy contract mismatch")
    if manifest["supported_case_count"] != expected_supported:
        errors.append("supported-case count does not match selected support policy")
    if manifest["unsupported_case_count"] != EXPECTED_CASES - expected_supported:
        errors.append("unsupported-case count does not match selected support policy")
    for case in cases:
        case_id = case["case_id"]
        source = source_cases.get(case_id)
        if source is None:
            errors.append(f"{case_id}: not in source manifest")
            continue
        pattern_path = OUTPUT / case["pattern_path"]
        if not pattern_path.is_file():
            errors.append(f"{case_id}: missing pattern")
            continue
        if sha256_file(pattern_path) != case["pattern_sha256"]:
            errors.append(f"{case_id}: pattern digest mismatch")
        try:
            data = np.loadtxt(pattern_path, delimiter=",", skiprows=1)
        except (OSError, ValueError) as exc:
            errors.append(f"{case_id}: cannot read pattern: {exc}")
            continue
        if data.shape != (POINT_COUNT, 2):
            errors.append(f"{case_id}: shape {data.shape} != {(POINT_COUNT, 2)}")
            continue
        if not np.allclose(data[:, 0], expected_axis, rtol=0, atol=5e-7):
            errors.append(f"{case_id}: two-theta axis mismatch")
        intensities = data[:, 1]
        if not np.all(np.isfinite(intensities)) or np.min(intensities) < 0:
            errors.append(f"{case_id}: invalid intensities")
        if not math.isclose(float(np.max(intensities)), 1.0, rel_tol=0, abs_tol=5e-10):
            errors.append(f"{case_id}: intensity maximum is not 1")
        if case["source_cif_sha256"] != source["sha256"]:
            errors.append(f"{case_id}: source CIF digest mismatch")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            structure = Structure.from_file(source_path(source))
        expected_profile, _ = simulate(structure, expected_axis)
        difference = float(np.max(np.abs(expected_profile - intensities)))
        max_resimulation_error = max(max_resimulation_error, difference)
        if difference > 5e-9:
            errors.append(f"{case_id}: resimulation error {difference:.12g} > 5e-9")
    if errors:
        raise RuntimeError("Crystalyze target audit failed:\n- " + "\n- ".join(errors))
    print(
        f"OK: {len(cases)} Crystalyze targets; "
        f"{manifest['supported_case_count']} supported, "
        f"{manifest['unsupported_case_count']} unsupported; "
        f"max resimulation error {max_resimulation_error:.12g}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build", "audit"))
    parser.add_argument("--corpus-root", type=Path, default=CORPUS)
    parser.add_argument(
        "--output-root",
        type=Path,
        help="override baselines/crystalyze/targets/<corpus>",
    )
    parser.add_argument("--dataset-id")
    parser.add_argument("--case-prefix")
    parser.add_argument("--support-policy", choices=SUPPORT_POLICIES, default="manifest")
    args = parser.parse_args()
    configure_dataset(args)
    if args.command == "build":
        build()
    audit()


if __name__ == "__main__":
    main()
