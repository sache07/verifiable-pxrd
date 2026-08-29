"""Build and audit deterministic deCIFer-native pXRD targets for a corpus.

The calculation reproduces the clean evaluation transformation described in
the accepted deCIFer paper and implemented by the released source: Pymatgen
``CuKa`` sticks on the full limiting sphere, conversion to momentum transfer,
a 50:50 pseudo-Voigt with constant 0.05 inverse-Angstrom FWHM, a 0--10
inverse-Angstrom grid at 0.01 spacing, and max normalization without noise.

Run with the benchmark lockfile environment::

    uv run python baselines/decifer/make_targets.py build
    uv run python baselines/decifer/make_targets.py audit
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
import torch
from pymatgen.analysis.diffraction.xrd import XRDCalculator
from pymatgen.core import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

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
OUTPUT = configure_paths(CORPUS, "decifer")["output"]
PATTERNS = OUTPUT / "patterns"
SOURCE_MANIFEST = CORPUS / "manifest.json"
OUTPUT_MANIFEST = OUTPUT / "manifest.json"
PARAMETERS_PATH = OUTPUT / "parameters.json"
INPUTS_PATH = OUTPUT / "inputs.csv"
PRIMARY_INPUTS_PATH = OUTPUT / "inputs-reduced-composition.csv"
ORACLE_INPUTS_PATH = OUTPUT / "inputs-full-cell-composition-oracle.csv"
DATASET_ID: str | None = None
CASE_PREFIX: str | None = None
SUPPORT_POLICY = "manifest"

EXPECTED_CASES = 100
EXPECTED_VERSIONS = {
    "numpy": "2.4.6",
    "pymatgen": "2026.5.4",
    "torch": "2.13.0+cpu",
}
EXPECTED_PYTHON = "3.11.15"

CHECKOUT_COMMIT = "91ace18de9aa118f1174942fbe1ec85f127c7864"
PAPER_VERSION = "arXiv:2502.02189v4"
PAPER_NOMINAL_WAVELENGTH_ANGSTROM = 1.5406
PYMATGEN_CUKA_WAVELENGTH_ANGSTROM = 1.54184
Q_MIN = 0.0
Q_MAX = 10.0
Q_STEP = 0.01
POINT_COUNT = 1000
FWHM = 0.05
ETA = 0.5


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
            "see baselines/decifer/README.md"
        )
    calculator = XRDCalculator(wavelength="CuKa")
    if not math.isclose(
        calculator.wavelength,
        PYMATGEN_CUKA_WAVELENGTH_ANGSTROM,
        rel_tol=0,
        abs_tol=1e-12,
    ):
        raise RuntimeError(
            "Pymatgen CuKa resolved to "
            f"{calculator.wavelength}, expected {PYMATGEN_CUKA_WAVELENGTH_ANGSTROM}"
        )
    return versions


def axis() -> torch.Tensor:
    values = torch.arange(Q_MIN, Q_MAX, Q_STEP, dtype=torch.float32)
    if len(values) != POINT_COUNT or not math.isclose(
        float(values[-1]), 9.99, rel_tol=0, abs_tol=1e-5
    ):
        raise RuntimeError(f"unexpected deCIFer Q axis: {len(values)} points, last={values[-1]}")
    return values


def parameters() -> dict[str, Any]:
    return {
        "background": "none",
        "broadening": {
            "fwhm_inv_angstrom": FWHM,
            "fwhm_type": "constant in Q",
            "gaussian_sigma_equation": "FWHM / (2*sqrt(2*ln(2)))",
            "lorentzian_half_width_equation": "FWHM / 2",
            "profile": "pseudo-Voigt (linear combination of height-normalized components)",
            "pseudo_voigt_eta": ETA,
        },
        "grid": {
            "last_point_inv_angstrom": 9.99,
            "point_count": POINT_COUNT,
            "quantity": "Q = 4*pi*sin(theta)/wavelength",
            "start_inv_angstrom": Q_MIN,
            "step_inv_angstrom": Q_STEP,
            "stop_inv_angstrom_exclusive": Q_MAX,
        },
        "intensity": {
            "clipping": "clip below zero after optional noise; no effect for clean profiles",
            "normalization": "divide summed broadened profile by its maximum",
            "range": [0.0, 1.0],
        },
        "noise": {
            "clean_evaluation_variance": 0.0,
            "distribution": "none for these deterministic targets",
            "paper_training_range": [0.001, 0.05],
            "paper_training_range_interpretation": (
                "paper labels this Gaussian-noise variance; released code uses the sampled "
                "value as torch.randn standard-deviation scale"
            ),
        },
        "preferred_orientation": "none",
        "stick_calculation": {
            "calculator": "pymatgen.analysis.diffraction.xrd.XRDCalculator",
            "debye_waller_factors": "none",
            "pymatgen_version": EXPECTED_VERSIONS["pymatgen"],
            "scaled_maximum": 100.0,
            "symprec": 0.0,
            "two_theta_range": None,
            "two_theta_range_note": (
                "released code selects Pymatgen's full limiting sphere because Qmax exceeds "
                "4*pi/wavelength"
            ),
        },
        "training_augmentation_not_applied": {
            "fwhm_uniform_inv_angstrom": [0.001, 0.10],
            "noise_uniform": [0.001, 0.05],
        },
        "wavelength": {
            "paper_nominal_angstrom": PAPER_NOMINAL_WAVELENGTH_ANGSTROM,
            "radiation": "Cu K-alpha",
            "released_code_pymatgen_key": "CuKa",
            "resolved_angstrom_for_targets": PYMATGEN_CUKA_WAVELENGTH_ANGSTROM,
        },
    }


def configure_dataset(args: argparse.Namespace) -> None:
    global CORPUS, OUTPUT, PATTERNS, SOURCE_MANIFEST, OUTPUT_MANIFEST
    global PARAMETERS_PATH, INPUTS_PATH, PRIMARY_INPUTS_PATH, ORACLE_INPUTS_PATH
    global DATASET_ID, CASE_PREFIX, SUPPORT_POLICY
    paths = configure_paths(args.corpus_root, "decifer", args.output_root)
    CORPUS = paths["corpus"]
    OUTPUT = paths["output"]
    PATTERNS = paths["patterns"]
    SOURCE_MANIFEST = paths["source_manifest"]
    OUTPUT_MANIFEST = paths["output_manifest"]
    PARAMETERS_PATH = OUTPUT / "parameters.json"
    INPUTS_PATH = OUTPUT / "inputs.csv"
    PRIMARY_INPUTS_PATH = OUTPUT / "inputs-reduced-composition.csv"
    ORACLE_INPUTS_PATH = OUTPUT / "inputs-full-cell-composition-oracle.csv"
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


def simulate(structure: Structure, sample_axis: torch.Tensor) -> tuple[np.ndarray, dict[str, Any]]:
    """Reproduce ``generate_continuous_xrd_from_cif`` for the clean setting."""

    calculator = XRDCalculator(wavelength="CuKa", symprec=0)
    # deCIFer's qmax=10 exceeds the CuKa limiting-sphere Q. Its released
    # source consequently passes two_theta_range=None to Pymatgen.
    sticks = calculator.get_pattern(structure, two_theta_range=None)
    theta_radians = torch.tensor(np.radians(sticks.x / 2), dtype=torch.float32)
    q_discrete = 4 * np.pi * torch.sin(theta_radians) / calculator.wavelength
    intensity_discrete = torch.tensor(sticks.y, dtype=torch.float32)

    sigma_gaussian = FWHM / (2 * torch.sqrt(2 * torch.log(torch.tensor(2.0))))
    gamma_lorentzian = FWHM / 2
    delta_q = sample_axis.unsqueeze(1) - q_discrete.unsqueeze(0)
    gaussian = torch.exp(-0.5 * (delta_q / sigma_gaussian) ** 2)
    lorentzian = 1 / (1 + (delta_q / gamma_lorentzian) ** 2)
    pseudo_voigt = ETA * lorentzian + (1 - ETA) * gaussian
    profile = (pseudo_voigt * intensity_discrete).sum(dim=1)
    maximum = float(profile.max())
    if not math.isfinite(maximum) or maximum <= 0:
        raise RuntimeError("simulated profile is empty or non-finite")
    profile /= profile.max() + 1e-16
    profile = torch.clamp(profile, min=0.0)

    result = profile.numpy()
    metadata = {
        "broadened_intensity_max_before_normalization": maximum,
        "stick_intensity_max": float(intensity_discrete.max()),
        "stick_peak_count": len(q_discrete),
        "stick_q_inv_angstrom_max": float(q_discrete.max()),
        "stick_q_inv_angstrom_min": float(q_discrete.min()),
        "stick_two_theta_deg_max": float(np.max(sticks.x)),
        "stick_two_theta_deg_min": float(np.min(sticks.x)),
    }
    return result, metadata


def integer_reduction_factor(structure: Structure) -> int:
    _, factor = structure.composition.get_reduced_composition_and_factor()
    rounded = round(factor)
    if not math.isclose(float(factor), rounded, rel_tol=0, abs_tol=1e-8):
        raise RuntimeError(f"non-integral composition reduction factor: {factor}")
    return int(rounded)


def formula_multiplicity_metadata(structure: Structure) -> dict[str, Any]:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        primitive = SpacegroupAnalyzer(structure, symprec=0.1, angle_tolerance=5).find_primitive()
    if primitive is None:
        primitive = structure
    return {
        "primitive_cell_formula_sum": primitive.composition.formula.replace(" ", ""),
        "primitive_cell_formula_units": integer_reduction_factor(primitive),
        "source_cell_formula_sum": structure.composition.formula.replace(" ", ""),
        "source_cell_formula_units": integer_reduction_factor(structure),
    }


def write_pattern(path: Path, sample_axis: torch.Tensor, profile: np.ndarray) -> None:
    q_values = sample_axis.numpy()
    if len(q_values) != len(profile):
        raise RuntimeError("pattern axis and profile lengths differ")
    temporary = path.with_suffix(path.suffix + ".partial")
    with temporary.open("w", encoding="utf-8", newline="") as stream:
        stream.write("q_inv_angstrom,intensity_normalized\n")
        for q_value, intensity in zip(q_values, profile, strict=True):
            stream.write(f"{q_value:.5f},{intensity:.10e}\n")
    temporary.replace(path)


def build() -> None:
    versions = assert_numerical_environment()
    cases = load_source_cases()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    PATTERNS.mkdir(parents=True, exist_ok=True)
    sample_axis = axis()
    output_cases: list[dict[str, Any]] = []
    input_rows: list[dict[str, Any]] = []
    primary_rows: list[dict[str, Any]] = []
    oracle_rows: list[dict[str, Any]] = []
    for index, case in enumerate(cases, start=1):
        cif_path = source_path(case)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            structure = Structure.from_file(cif_path)
        formula_metadata = formula_multiplicity_metadata(structure)
        source_cell_formula_sum = formula_metadata["source_cell_formula_sum"]
        primitive_cell_formula_sum = formula_metadata["primitive_cell_formula_sum"]
        source_cell_formula_units = formula_metadata["source_cell_formula_units"]
        primitive_cell_formula_units = formula_metadata["primitive_cell_formula_units"]
        profile, simulation_metadata = simulate(structure, sample_axis)
        relative_pattern = PurePosixPath("patterns") / f"{case['case_id']}.xy"
        pattern_path = OUTPUT / relative_pattern
        write_pattern(pattern_path, sample_axis, profile)
        exposure, supported = framework_support(
            case, framework_key="decifer", policy=SUPPORT_POLICY
        )
        source_dataset_id = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))["dataset_id"]
        output_cases.append(
            {
                "case_id": case["case_id"],
                "composition": case["formula"],
                "composition_contract": f"reduced composition from {source_dataset_id} manifest",
                "elements": case["elements"],
                "framework_applicability": exposure,
                "model_supported": supported,
                "panel": case["panel"],
                "paper_native_cell_composition": source_cell_formula_sum,
                "pattern_path": relative_pattern.as_posix(),
                "pattern_sha256": sha256_file(pattern_path),
                "primitive_cell_formula_sum": primitive_cell_formula_sum,
                "primitive_cell_formula_units": primitive_cell_formula_units,
                "primitive_site_count": case["primitive_site_count"],
                "source_cell_formula_sum": source_cell_formula_sum,
                "source_cell_formula_units": source_cell_formula_units,
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
                "composition_contract": "reduced",
                "elements": " ".join(case["elements"]),
                "source_cell_formula_sum_hidden_oracle": source_cell_formula_sum,
                "source_cell_formula_units_hidden_oracle": source_cell_formula_units,
                "primitive_cell_formula_sum_hidden_oracle": primitive_cell_formula_sum,
                "primitive_cell_formula_units_hidden_oracle": primitive_cell_formula_units,
                "pattern_path": relative_pattern.as_posix(),
                "decifer_applicability": exposure,
            }
        )
        common_input = {
            "case_id": case["case_id"],
            "panel": case["panel"],
            "pattern_path": relative_pattern.as_posix(),
            "decifer_applicability": exposure,
        }
        primary_rows.append(
            {
                **common_input,
                "composition": case["formula"],
                "input_mode": "reduced_composition",
            }
        )
        oracle_rows.append(
            {
                **common_input,
                "composition": source_cell_formula_sum,
                "input_mode": "full_source_cell_composition_oracle_from_hidden_cif",
                "formula_unit_multiplier": source_cell_formula_units,
            }
        )
        if index % 10 == 0 or index == len(cases):
            print(f"generated {index}/{len(cases)} patterns")

    for path, rows in (
        (INPUTS_PATH, input_rows),
        (PRIMARY_INPUTS_PATH, primary_rows),
        (ORACLE_INPUTS_PATH, oracle_rows),
    ):
        temporary_inputs = path.with_suffix(".csv.partial")
        with temporary_inputs.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        temporary_inputs.replace(path)
    write_json(PARAMETERS_PATH, parameters())
    write_json(
        OUTPUT_MANIFEST,
        {
            "cases": output_cases,
            "framework": "deCIFer",
            "framework_checkout_commit": CHECKOUT_COMMIT,
            "generator": "baselines/decifer/make_targets.py",
            "source_dataset_id": json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))[
                "dataset_id"
            ],
            "case_prefix": CASE_PREFIX,
            "support_policy": SUPPORT_POLICY,
            "numerical_environment": versions,
            "parameter_file": "parameters.json",
            "input_modes": {
                "primary": "inputs-reduced-composition.csv",
                "full_cell_oracle": "inputs-full-cell-composition-oracle.csv",
                "combined_audit": "inputs.csv",
            },
            "parameter_sources": {
                "accepted_paper": "https://arxiv.org/abs/2502.02189v4",
                "paper_version": PAPER_VERSION,
                "pymatgen_xrd_source": (
                    "https://github.com/materialsproject/pymatgen/blob/v2026.5.4/"
                    "src/pymatgen/analysis/diffraction/xrd.py"
                ),
                "released_utility_source": (
                    "https://github.com/FrederikLizakJohansen/deCIFer/blob/"
                    f"{CHECKOUT_COMMIT}/decifer/utility.py"
                ),
            },
            "pattern_count": len(output_cases),
            "schema_version": "1.0.0",
            "source_manifest": relative_reference(SOURCE_MANIFEST, from_directory=OUTPUT),
            "source_manifest_sha256": sha256_file(SOURCE_MANIFEST),
            "source_cell_formula_units_gt_one_count": sum(
                case["source_cell_formula_units"] > 1 for case in output_cases
            ),
            "primitive_cell_formula_units_gt_one_count": sum(
                case["primitive_cell_formula_units"] > 1 for case in output_cases
            ),
            "source_and_primitive_formula_sum_differ_count": sum(
                case["source_cell_formula_sum"] != case["primitive_cell_formula_sum"]
                for case in output_cases
            ),
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
    sample_axis = axis()
    expected_axis = sample_axis.numpy()
    if len(cases) != EXPECTED_CASES:
        errors.append(f"pattern count {len(cases)} != {EXPECTED_CASES}")
    if manifest["source_manifest_sha256"] != sha256_file(SOURCE_MANIFEST):
        errors.append("source manifest digest mismatch")
    for path in (INPUTS_PATH, PRIMARY_INPUTS_PATH, ORACLE_INPUTS_PATH):
        if not path.is_file():
            errors.append(f"missing input table: {path.name}")
            continue
        with path.open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
        if len(rows) != EXPECTED_CASES or len({row["case_id"] for row in rows}) != EXPECTED_CASES:
            errors.append(f"invalid input table: {path.name}")
    source_metadata: list[dict[str, Any]] = []
    for source in source_cases.values():
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            source_structure = Structure.from_file(source_path(source))
        source_metadata.append(formula_multiplicity_metadata(source_structure))
    expected_source_multiplicity = sum(
        item["source_cell_formula_units"] > 1 for item in source_metadata
    )
    expected_primitive_multiplicity = sum(
        item["primitive_cell_formula_units"] > 1 for item in source_metadata
    )
    expected_cell_difference = sum(
        item["source_cell_formula_sum"] != item["primitive_cell_formula_sum"]
        for item in source_metadata
    )
    expected_supported = sum(
        framework_support(case, framework_key="decifer", policy=SUPPORT_POLICY)[1]
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
    if manifest["source_cell_formula_units_gt_one_count"] != expected_source_multiplicity:
        errors.append("unexpected source-cell formula multiplicity count")
    if manifest["primitive_cell_formula_units_gt_one_count"] != expected_primitive_multiplicity:
        errors.append("unexpected primitive-cell formula multiplicity count")
    if manifest["source_and_primitive_formula_sum_differ_count"] != expected_cell_difference:
        errors.append("unexpected source/primitive-cell formula difference count")
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
        if not np.allclose(data[:, 0], expected_axis, rtol=0, atol=5e-6):
            errors.append(f"{case_id}: Q axis mismatch")
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
        expected_profile, _ = simulate(structure, sample_axis)
        difference = float(np.max(np.abs(expected_profile - intensities)))
        max_resimulation_error = max(max_resimulation_error, difference)
        if difference > 5e-10:
            errors.append(f"{case_id}: resimulation error {difference:.12g} > 5e-10")
    if errors:
        raise RuntimeError("deCIFer target audit failed:\n- " + "\n- ".join(errors))
    print(
        f"OK: {len(cases)} deCIFer targets; "
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
        help="override baselines/decifer/targets/<corpus>",
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
