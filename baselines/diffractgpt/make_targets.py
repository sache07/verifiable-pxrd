"""Build and audit paper-checkpoint DiffractGPT inputs for a corpus.

The published checkpoint consumes a reduced composition and a 180-value,
newline-separated XRD vector: 0 <= 2theta < 90 degrees on a 0.5-degree grid,
formatted to three decimal places. Stick peaks come from the paper-era
JARVIS-Tools XRD calculator. Nearest-bin replacement follows the first later
public AtomGPT helper, but no released code revision exactly implements all of
the paper's 180-bin, 0.5-degree, three-decimal preprocessing contract.

Run this script in the isolated numerical environment documented in
``baselines/diffractgpt/README.md``::

    .runs/envs/diffractgpt-targets/bin/python \
      baselines/diffractgpt/make_targets.py build
    .runs/envs/diffractgpt-targets/bin/python \
      baselines/diffractgpt/make_targets.py audit

The article says that a Gaussian broadening function was applied, but neither
the article nor SI gives a width and no paper-era preprocessing code was
released. The first later public helper contains no Gaussian operation. This
builder therefore does not invent a width; the reconciliation is recorded in
the target README and parameters.json.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
import re
import shlex
from collections import Counter
from importlib.metadata import version
from pathlib import Path, PurePosixPath
from typing import Any

import numpy as np
from jarvis.analysis.diffraction import xrd as jarvis_xrd_module
from jarvis.analysis.diffraction.xrd import XRD
from jarvis.core.atoms import Atoms
from jarvis.core.composition import Composition
from jarvis.core.lattice import Lattice

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
OUTPUT = configure_paths(CORPUS, "diffractgpt")["output"]
PATTERNS = OUTPUT / "patterns"
VECTORS = OUTPUT / "vectors"
PROMPTS = OUTPUT / "prompts"
SOURCE_MANIFEST = CORPUS / "manifest.json"
OUTPUT_MANIFEST = OUTPUT / "manifest.json"
PARAMETERS_PATH = OUTPUT / "parameters.json"
INPUTS_PATH = OUTPUT / "inputs.csv"
DATASET_ID: str | None = None
CASE_PREFIX: str | None = None
SUPPORT_POLICY = "manifest"

EXPECTED_CASES = 100
EXPECTED_PYTHON = "3.10.20"
EXPECTED_VERSIONS = {
    "jarvis-tools": "2024.10.30",
    "numpy": "1.26.4",
    "pandas": "2.2.2",
    "scipy": "1.13.1",
    "spglib": "2.4.0",
}
JARVIS_COMMIT = "ac16eb5e6b5eb89360bcada5b1356e8144510422"
JARVIS_XRD_SHA256 = "486897f96b5d6d34028b6518afed8661b9645d8ce9b7a69b64751c062dde89cd"
SCATTERING_PARAMETERS_SHA256 = "c675301248bb86ea359428f20c3987d719b1ac1a779166ef27e1d0f652467d93"
ATOMGPT_CHECKOUT_COMMIT = "f2f4d58c4dcab9ae1a3cdd30c8f13d94f4da7928"
ATOMGPT_BINNING_REFERENCE_COMMIT = "6ceecec86c7ae5e16776deca54b0fcf8027311ca"
MODEL_REVISION = "4080c1e4ece70b82f4defc622141fc733fc2dce2"

WAVELENGTH_ANGSTROM = 1.54184
TWO_THETA_START = 0.0
TWO_THETA_STOP = 90.0
TWO_THETA_STEP = 0.5
POINT_COUNT = 180
SCALING_FACTOR = 100.0
TWO_THETA_TOL = 1e-5
INTENSITY_TOL = 0.5
MAX_INDEX = 5
DECIMAL_PLACES = 3

INSTRUCTION = "Below is a description of a material."
OUTPUT_REQUEST = (
    " Generate atomic structure description with lattice lengths, angles, "
    "coordinates and atom types."
)
ALPACA_TEMPLATE = "### Instruction:\n{}\n### Input:\n{}\n### Output:\n{}"


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
            "see baselines/diffractgpt/README.md"
        )
    xrd_source = Path(jarvis_xrd_module.__file__).resolve()
    if sha256_file(xrd_source) != JARVIS_XRD_SHA256:
        raise RuntimeError(f"unexpected JARVIS XRD source: {xrd_source}")
    scattering = xrd_source.with_name("atomic_scattering_params.json")
    if sha256_file(scattering) != SCATTERING_PARAMETERS_SHA256:
        raise RuntimeError(f"unexpected scattering parameter table: {scattering}")
    calculator = xrd_calculator()
    if not math.isclose(calculator.wavelength, WAVELENGTH_ANGSTROM, abs_tol=1e-12):
        raise RuntimeError("JARVIS XRD wavelength default does not match the paper")
    return versions


def axis() -> np.ndarray:
    values = np.arange(TWO_THETA_START, TWO_THETA_STOP, TWO_THETA_STEP, dtype=np.float64)
    if (
        len(values) != POINT_COUNT
        or not math.isclose(values[0], 0.0, abs_tol=1e-12)
        or not math.isclose(values[-1], 89.5, abs_tol=1e-12)
    ):
        raise RuntimeError(
            f"unexpected DiffractGPT axis: {len(values)} points, "
            f"first={values[0]}, last={values[-1]}"
        )
    return values


def xrd_calculator() -> XRD:
    return XRD(
        wavelength=WAVELENGTH_ANGSTROM,
        thetas=[TWO_THETA_START, TWO_THETA_STOP],
        scaling_factor=SCALING_FACTOR,
        two_theta_tol=TWO_THETA_TOL,
        intensity_tol=INTENSITY_TOL,
        max_index=MAX_INDEX,
    )


def parameters() -> dict[str, Any]:
    source_dataset_id = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))["dataset_id"]
    return {
        "background": "none for deterministic simulated benchmark inputs",
        "broadening": {
            "applied_in_reproducible_transform": False,
            "article_claim": (
                "The article states that a Gaussian broadening function was applied."
            ),
            "profile": "Gaussian (article claim)",
            "width": None,
            "reconciliation": (
                "No Gaussian width is reported in the article or SI, and no paper-era "
                "preprocessing implementation was released. The first later AtomGPT "
                "helper bins JARVIS sticks without a Gaussian operation. No unreported "
                "width is invented here."
            ),
        },
        "format": {
            "decimal_places": DECIMAL_PLACES,
            "separator": "newline",
            "vector_length": POINT_COUNT,
        },
        "grid": {
            "last_point_deg": 89.5,
            "point_count": POINT_COUNT,
            "start_deg": TWO_THETA_START,
            "step_deg": TWO_THETA_STEP,
            "stop_deg_exclusive": TWO_THETA_STOP,
        },
        "intensity": {
            "jarvis_native_filter": (
                "retain native integrated intensities strictly greater than 0.5 "
                "after scaling their sum to 100"
            ),
            "normalization": (
                "divide JARVIS sticks by their maximum, assign each retained stick "
                "to its nearest grid point with replacement semantics, then divide "
                "the binned vector by its maximum"
            ),
            "range": [0.0, 1.0],
            "rounding_for_model": "round-half-even through Python format .3f",
        },
        "noise": "none",
        "preferred_orientation": "none (JARVIS po factor is 1)",
        "prompt": {
            "alpaca_template": ALPACA_TEMPLATE,
            "benchmark_composition": (
                f"reduced composition supplied by {source_dataset_id} manifest.json; the model "
                "formula is a flattened serialization of that composition"
            ),
            "formula_template": (
                "The chemical formula is {formula} . The  XRD is {vector}." + OUTPUT_REQUEST
            ),
            "instruction": INSTRUCTION,
        },
        "stick_calculation": {
            "calculator": "jarvis.analysis.diffraction.xrd.XRD",
            "intensity_tol": INTENSITY_TOL,
            "jarvis_commit": JARVIS_COMMIT,
            "jarvis_tools_version": EXPECTED_VERSIONS["jarvis-tools"],
            "lorentz_polarization": True,
            "max_miller_index_seed": MAX_INDEX,
            "scaling_factor": SCALING_FACTOR,
            "structure_factor": "atomic scattering factors and fractional coordinates",
            "two_theta_tolerance_deg": TWO_THETA_TOL,
        },
        "threshold_note": (
            "The SI's 0.04 cutoff is an experimental-pattern preprocessing step. "
            "It is not added to ideal simulations; JARVIS's native intensity_tol "
            "already defines the simulated training sparsity."
        ),
        "wavelength": {
            "angstrom": WAVELENGTH_ANGSTROM,
            "radiation": "Cu K-alpha",
        },
        "preprocessing_reproducibility": {
            "exact_released_implementation_available": False,
            "paper_is_authoritative_for": [
                "180 values",
                "0.5-degree interval",
                "three-decimal serialization",
            ],
            "later_code_reference": (
                "AtomGPT commit 6ceecec86c7ae5e16776deca54b0fcf8027311ca "
                "discloses nearest-bin replacement and max normalization, but emits "
                "two decimals; it is not an exact executable match for the paper."
            ),
        },
    }


def configure_dataset(args: argparse.Namespace) -> None:
    global CORPUS, OUTPUT, PATTERNS, VECTORS, PROMPTS, SOURCE_MANIFEST
    global OUTPUT_MANIFEST, PARAMETERS_PATH, INPUTS_PATH
    global DATASET_ID, CASE_PREFIX, SUPPORT_POLICY
    paths = configure_paths(args.corpus_root, "diffractgpt", args.output_root)
    CORPUS = paths["corpus"]
    OUTPUT = paths["output"]
    PATTERNS = paths["patterns"]
    VECTORS = OUTPUT / "vectors"
    PROMPTS = OUTPUT / "prompts"
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


def model_formula_from_reduced_composition(case: dict[str, Any]) -> str:
    """Serialize only the benchmark-supplied reduced composition for the model."""
    amounts: dict[str, int | float] = {}
    for item in case["reduced_formula_key"].split():
        match = re.fullmatch(r"([A-Z][a-z]?)(\d+(?:\.\d*)?|\.\d+)", item)
        if match is None:
            raise ValueError(f"{case['case_id']}: invalid reduced_formula_key item {item!r}")
        element, raw_amount = match.groups()
        amount = float(raw_amount)
        amounts[element] = int(amount) if amount.is_integer() else amount
    if set(amounts) != set(case["elements"]):
        raise ValueError(f"{case['case_id']}: reduced composition elements do not match")
    return Composition(amounts).reduced_formula


def source_path(case: dict[str, Any]) -> Path:
    relative = PurePosixPath(case["path"])
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"unsafe source path: {relative}")
    path = CORPUS / relative
    if sha256_file(path) != case["sha256"]:
        raise RuntimeError(f"source CIF digest mismatch: {path}")
    return path


def cif_number(token: str) -> float:
    """Parse a simple CIF number, stripping a parenthesized uncertainty."""

    value = token.strip().strip("'\"")
    if "(" in value:
        value = value.split("(", 1)[0]
    return float(value)


def parse_p1_cif(path: Path) -> Atoms:
    """Read the explicit P1 CIFs emitted by the benchmark selector.

    The benchmark CIFs intentionally contain every primitive site in a P1 loop.
    Requiring that contract avoids introducing another structure standardizer or
    symmetry-expansion implementation into the forward calculation.
    """

    lines = path.read_text(encoding="utf-8").splitlines()
    scalar_tokens: dict[str, list[str]] = {}
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("_"):
            continue
        tokens = shlex.split(stripped, comments=False, posix=True)
        if len(tokens) >= 2:
            scalar_tokens[tokens[0]] = tokens[1:]

    required_cell = (
        "_cell_length_a",
        "_cell_length_b",
        "_cell_length_c",
        "_cell_angle_alpha",
        "_cell_angle_beta",
        "_cell_angle_gamma",
    )
    try:
        cell = [cif_number(scalar_tokens[key][0]) for key in required_cell]
    except (KeyError, IndexError) as exc:
        raise ValueError(f"{path}: incomplete unit-cell data") from exc
    if scalar_tokens.get("_symmetry_Int_Tables_number", [None])[0] != "1":
        raise ValueError(f"{path}: expected an explicit P1 CIF")

    atom_headers: list[str] | None = None
    atom_start: int | None = None
    for index, line in enumerate(lines):
        if line.strip() != "loop_":
            continue
        headers: list[str] = []
        cursor = index + 1
        while cursor < len(lines) and lines[cursor].strip().startswith("_"):
            headers.append(lines[cursor].strip())
            cursor += 1
        if "_atom_site_type_symbol" in headers:
            atom_headers = headers
            atom_start = cursor
            break
    if atom_headers is None or atom_start is None:
        raise ValueError(f"{path}: atom-site loop not found")

    rows: list[dict[str, str]] = []
    for line in lines[atom_start:]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "loop_" or stripped.startswith("_"):
            break
        tokens = shlex.split(stripped, comments=False, posix=True)
        if len(tokens) != len(atom_headers):
            raise ValueError(
                f"{path}: atom row has {len(tokens)} values for {len(atom_headers)} columns"
            )
        rows.append(dict(zip(atom_headers, tokens, strict=True)))
    if not rows:
        raise ValueError(f"{path}: atom-site loop is empty")

    coordinate_keys = (
        "_atom_site_fract_x",
        "_atom_site_fract_y",
        "_atom_site_fract_z",
    )
    elements: list[str] = []
    coordinates: list[list[float]] = []
    for row in rows:
        if not math.isclose(cif_number(row["_atom_site_occupancy"]), 1.0, abs_tol=1e-12):
            raise ValueError(f"{path}: partial occupancy is outside this benchmark")
        if row.get("_atom_site_symmetry_multiplicity", "1") != "1":
            raise ValueError(f"{path}: expected explicit multiplicity-one P1 sites")
        elements.append(row["_atom_site_type_symbol"])
        coordinates.append([cif_number(row[key]) for key in coordinate_keys])

    lattice = Lattice.from_parameters(*cell)
    return Atoms(
        lattice_mat=lattice.matrix,
        coords=coordinates,
        elements=elements,
        cartesian=False,
    )


def simulate(atoms: Atoms, sample_axis: np.ndarray) -> tuple[np.ndarray, dict[str, Any]]:
    centers_list, _d_hkls, intensities_list = xrd_calculator().simulate(atoms=atoms)
    centers = np.asarray(centers_list, dtype=np.float64)
    intensities = np.asarray(intensities_list, dtype=np.float64)
    if not len(centers) or len(centers) != len(intensities):
        raise RuntimeError("JARVIS returned an empty or malformed stick pattern")
    if not np.all(np.isfinite(centers)) or not np.all(np.isfinite(intensities)):
        raise RuntimeError("JARVIS returned non-finite diffraction values")

    # Use the nearest-bin replacement semantics disclosed in AtomGPT's first
    # later public helper. No released revision matches the complete paper
    # contract: that helper uses 0.5-degree bins but serializes two decimals.
    normalized_sticks = intensities / np.max(intensities)
    profile = np.zeros_like(sample_axis, dtype=np.float64)
    assigned_bins: list[int] = []
    for center, intensity in zip(centers, normalized_sticks):  # noqa: B905
        closest = int(np.abs(sample_axis - center).argmin())
        profile[closest] = intensity
        assigned_bins.append(closest)
    maximum = float(np.max(profile))
    if not math.isfinite(maximum) or maximum <= 0:
        raise RuntimeError("binned XRD profile is empty or non-finite")
    profile /= maximum

    bin_counts = Counter(assigned_bins)
    metadata = {
        "binned_nonzero_count_before_rounding": int(np.count_nonzero(profile)),
        "collision_bin_count": sum(count > 1 for count in bin_counts.values()),
        "overwritten_stick_count": sum(count - 1 for count in bin_counts.values()),
        "stick_intensity_max_after_jarvis_scaling": float(np.max(intensities)),
        "stick_peak_count": len(centers),
        "stick_two_theta_deg_max": float(np.max(centers)),
        "stick_two_theta_deg_min": float(np.min(centers)),
    }
    return profile, metadata


def rounded_profile(profile: np.ndarray) -> np.ndarray:
    return np.asarray([float(f"{value:.{DECIMAL_PLACES}f}") for value in profile])


def vector_text(profile: np.ndarray) -> str:
    return "\n".join(f"{value:.{DECIMAL_PLACES}f}" for value in profile) + "\n"


def prompt_input(formula: str, vector: str) -> str:
    values = vector.rstrip("\n")
    return f"The chemical formula is {formula} . The  XRD is {values}.{OUTPUT_REQUEST}"


def full_prompt(formula: str, vector: str) -> str:
    return ALPACA_TEMPLATE.format(INSTRUCTION, prompt_input(formula, vector), "")


def write_pattern(path: Path, sample_axis: np.ndarray, profile: np.ndarray) -> None:
    temporary = path.with_suffix(path.suffix + ".partial")
    with temporary.open("w", encoding="utf-8", newline="") as stream:
        stream.write("two_theta_deg,intensity_model_input\n")
        for two_theta, intensity in zip(sample_axis, profile):  # noqa: B905
            stream.write(f"{two_theta:.1f},{intensity:.{DECIMAL_PLACES}f}\n")
    temporary.replace(path)


def write_text(path: Path, content: str) -> None:
    temporary = path.with_suffix(path.suffix + ".partial")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def build() -> None:
    versions = assert_numerical_environment()
    source_manifest_sha256 = sha256_file(SOURCE_MANIFEST)
    cases = load_source_cases()
    for directory in (OUTPUT, PATTERNS, VECTORS, PROMPTS):
        directory.mkdir(parents=True, exist_ok=True)
    sample_axis = axis()
    output_cases: list[dict[str, Any]] = []
    input_rows: list[dict[str, Any]] = []

    for index, case in enumerate(cases, start=1):
        cif_path = source_path(case)
        atoms = parse_p1_cif(cif_path)
        if len(atoms.elements) != case["cif_site_count"]:
            raise RuntimeError(
                f"{case['case_id']}: parsed {len(atoms.elements)} sites, "
                f"expected {case['cif_site_count']}"
            )
        profile, simulation_metadata = simulate(atoms, sample_axis)
        model_profile = rounded_profile(profile)
        vector = vector_text(model_profile)
        model_formula = model_formula_from_reduced_composition(case)
        if model_formula != atoms.composition.reduced_formula:
            raise RuntimeError(
                f"{case['case_id']}: benchmark reduced composition does not match CIF"
            )

        pattern_relative = PurePosixPath("patterns") / f"{case['case_id']}.xy"
        vector_relative = PurePosixPath("vectors") / f"{case['case_id']}.txt"
        prompt_relative = PurePosixPath("prompts") / f"{case['case_id']}.txt"
        pattern_path = OUTPUT / pattern_relative
        vector_path = OUTPUT / vector_relative
        prompt_path = OUTPUT / prompt_relative
        write_pattern(pattern_path, sample_axis, model_profile)
        write_text(vector_path, vector)
        write_text(prompt_path, full_prompt(model_formula, vector))
        applicability, supported = framework_support(
            case, framework_key="diffractgpt", policy=SUPPORT_POLICY
        )

        output_cases.append(
            {
                "case_id": case["case_id"],
                "composition": case["formula"],
                "composition_kind": "reduced_formula",
                "elements": case["elements"],
                "framework_applicability": applicability,
                "model_supported": supported,
                "model_formula": model_formula,
                "panel": case["panel"],
                "pattern_path": pattern_relative.as_posix(),
                "pattern_sha256": sha256_file(pattern_path),
                "primitive_site_count": case["primitive_site_count"],
                "prompt_path": prompt_relative.as_posix(),
                "diffractgpt_applicability": applicability,
                "prompt_sha256": sha256_file(prompt_path),
                "rounded_nonzero_count": int(np.count_nonzero(model_profile)),
                "reduced_composition": case["formula"],
                "reduced_formula_key": case["reduced_formula_key"],
                "source_cif_path": case["path"],
                "source_cif_sha256": case["sha256"],
                "vector_path": vector_relative.as_posix(),
                "vector_sha256": sha256_file(vector_path),
                **simulation_metadata,
            }
        )
        input_rows.append(
            {
                "case_id": case["case_id"],
                "panel": case["panel"],
                "composition": case["formula"],
                "composition_kind": "reduced_formula",
                "reduced_composition": case["formula"],
                "model_formula": model_formula,
                "elements": " ".join(case["elements"]),
                "framework_applicability": applicability,
                "model_supported": supported,
                "pattern_path": pattern_relative.as_posix(),
                "vector_path": vector_relative.as_posix(),
                "prompt_path": prompt_relative.as_posix(),
            }
        )
        if index % 10 == 0 or index == len(cases):
            print(f"generated {index}/{len(cases)} DiffractGPT inputs")

    csv_temporary = INPUTS_PATH.with_suffix(".csv.partial")
    with csv_temporary.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(input_rows[0]))
        writer.writeheader()
        writer.writerows(input_rows)
    csv_temporary.replace(INPUTS_PATH)
    if sha256_file(SOURCE_MANIFEST) != source_manifest_sha256:
        raise RuntimeError("source manifest changed during target generation")
    write_json(PARAMETERS_PATH, parameters())
    write_json(
        OUTPUT_MANIFEST,
        {
            "atomgpt_checkout_commit": ATOMGPT_CHECKOUT_COMMIT,
            "atomgpt_binning_reference": {
                "commit": ATOMGPT_BINNING_REFERENCE_COMMIT,
                "exact_paper_preprocessing_match": False,
                "mismatch": (
                    "The helper uses nearest-bin replacement and a 0.5-degree "
                    "default, but actively serializes two decimals. The article is "
                    "authoritative for 180 values, 0.5 degrees, and three decimals."
                ),
            },
            "benchmark_input": {
                "composition": (
                    "reduced composition from the selected corpus manifest.json, recorded per "
                    "case as reduced_composition; model_formula is only its "
                    "checkpoint-specific flattened serialization"
                ),
                "pxrd": (
                    "180 max-normalized intensity values on [0, 90) degrees 2theta "
                    "at 0.5-degree spacing"
                ),
            },
            "cases": output_cases,
            "framework": "DiffractGPT",
            "generator": "baselines/diffractgpt/make_targets.py",
            "source_dataset_id": json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))[
                "dataset_id"
            ],
            "case_prefix": CASE_PREFIX,
            "support_policy": SUPPORT_POLICY,
            "model": {
                "base_model": "unsloth/mistral-7b-bnb-4bit",
                "checkpoint": "knc6/diffractgpt_mistral_chemical_formula",
                "revision": MODEL_REVISION,
            },
            "numerical_environment": versions,
            "parameter_file": "parameters.json",
            "parameter_sources": {
                "article_doi": "10.1021/acs.jpclett.4c03137",
                "article_nist_pdf": (
                    "https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=958965"
                ),
                "article_nist_pdf_sha256": (
                    "51d7e440f11261e509ed4ed8396e26f52a025d25d4d5b7a56f9e5f9555c9484f"
                ),
                "jarvis_xrd_source": (
                    "https://github.com/usnistgov/jarvis/blob/"
                    f"{JARVIS_COMMIT}/jarvis/analysis/diffraction/xrd.py"
                ),
                "supporting_information_pdf": (
                    "https://pubs.acs.org/doi/suppl/10.1021/"
                    "acs.jpclett.4c03137/suppl_file/jz4c03137_si_001.pdf"
                ),
                "supporting_information_pdf_sha256": (
                    "e72c60429c2ce2f3f8b76d624ba52ac1602f6f92427af5457e87e4f2bd92cbb8"
                ),
                "later_binning_reference_source": (
                    "https://github.com/usnistgov/atomgpt/blob/"
                    f"{ATOMGPT_BINNING_REFERENCE_COMMIT}/atomgpt/inverse_models/utils.py"
                ),
            },
            "pattern_count": len(output_cases),
            "schema_version": "1.0.0",
            "source_manifest": relative_reference(SOURCE_MANIFEST, from_directory=OUTPUT),
            "source_manifest_sha256": source_manifest_sha256,
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
        framework_support(case, framework_key="diffractgpt", policy=SUPPORT_POLICY)[1]
        for case in source_cases.values()
    )
    source_dataset_id = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))["dataset_id"]
    if manifest.get("source_dataset_id", source_dataset_id) != source_dataset_id:
        errors.append("source dataset ID mismatch")
    if manifest.get("case_prefix") != CASE_PREFIX:
        errors.append("case-prefix contract mismatch")
    if manifest.get("support_policy", "manifest") != SUPPORT_POLICY:
        errors.append("support-policy contract mismatch")
    if manifest.get("supported_case_count", expected_supported) != expected_supported:
        errors.append("supported-case count does not match selected support policy")
    if (
        manifest.get("unsupported_case_count", EXPECTED_CASES - expected_supported)
        != EXPECTED_CASES - expected_supported
    ):
        errors.append("unsupported-case count does not match selected support policy")
    if manifest["model"]["revision"] != MODEL_REVISION:
        errors.append("model revision is not the paper-era immutable checkpoint")
    if "reduced composition" not in manifest["benchmark_input"]["composition"]:
        errors.append("benchmark input does not declare reduced composition")
    if manifest["atomgpt_binning_reference"]["exact_paper_preprocessing_match"]:
        errors.append("later AtomGPT helper is incorrectly marked as an exact match")

    for case in cases:
        case_id = case["case_id"]
        source = source_cases.get(case_id)
        if source is None:
            errors.append(f"{case_id}: not in source manifest")
            continue
        if case.get("composition_kind") != "reduced_formula":
            errors.append(f"{case_id}: composition is not declared reduced")
        if case.get("reduced_composition") != source["formula"]:
            errors.append(f"{case_id}: reduced composition mismatch")
        if case.get("reduced_formula_key") != source["reduced_formula_key"]:
            errors.append(f"{case_id}: reduced formula key mismatch")
        if case.get("model_formula") != model_formula_from_reduced_composition(source):
            errors.append(f"{case_id}: model formula is not from reduced composition")
        paths = {
            "pattern": OUTPUT / case["pattern_path"],
            "vector": OUTPUT / case["vector_path"],
            "prompt": OUTPUT / case["prompt_path"],
        }
        for kind, path in paths.items():
            if not path.is_file():
                errors.append(f"{case_id}: missing {kind}")
            elif sha256_file(path) != case[f"{kind}_sha256"]:
                errors.append(f"{case_id}: {kind} digest mismatch")
        if any(not path.is_file() for path in paths.values()):
            continue
        try:
            data = np.loadtxt(paths["pattern"], delimiter=",", skiprows=1)
            vector_values = np.loadtxt(paths["vector"])
        except (OSError, ValueError) as exc:
            errors.append(f"{case_id}: cannot read target: {exc}")
            continue
        if data.shape != (POINT_COUNT, 2):
            errors.append(f"{case_id}: pattern shape {data.shape}")
            continue
        if vector_values.shape != (POINT_COUNT,):
            errors.append(f"{case_id}: vector shape {vector_values.shape}")
            continue
        if not np.array_equal(data[:, 0], expected_axis):
            errors.append(f"{case_id}: two-theta axis mismatch")
        if not np.array_equal(data[:, 1], vector_values):
            errors.append(f"{case_id}: XY and model vector differ")
        if not np.all(np.isfinite(vector_values)) or np.min(vector_values) < 0:
            errors.append(f"{case_id}: invalid intensities")
        if not math.isclose(float(np.max(vector_values)), 1.0, abs_tol=1e-12):
            errors.append(f"{case_id}: intensity maximum is not 1")
        expected_vector = vector_text(vector_values)
        if paths["vector"].read_text(encoding="utf-8") != expected_vector:
            errors.append(f"{case_id}: vector formatting is not exactly .3f/newline")
        prompt = paths["prompt"].read_text(encoding="utf-8")
        if prompt != full_prompt(case["model_formula"], expected_vector):
            errors.append(f"{case_id}: prompt does not match the paper template")
        if case["source_cif_sha256"] != source["sha256"]:
            errors.append(f"{case_id}: source CIF digest mismatch")
        source_cif = CORPUS / source["path"]
        if not source_cif.is_file() or sha256_file(source_cif) != source["sha256"]:
            errors.append(f"{case_id}: current source CIF does not match source manifest")
            continue
        expected_profile = rounded_profile(simulate(parse_p1_cif(source_cif), expected_axis)[0])
        difference = float(np.max(np.abs(expected_profile - vector_values)))
        max_resimulation_error = max(max_resimulation_error, difference)
        if difference > 5e-12:
            errors.append(f"{case_id}: resimulation error {difference:.12g} > 5e-12")

    if errors:
        raise RuntimeError("DiffractGPT target audit failed:\n- " + "\n- ".join(errors))
    panel_counts = Counter(case["panel"] for case in cases)
    print(
        f"OK: {len(cases)} DiffractGPT inputs; "
        f"panels={dict(sorted(panel_counts.items()))}; "
        f"{POINT_COUNT} bins each at {TWO_THETA_STEP} degree; "
        f"max resimulation error {max_resimulation_error:.12g}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build", "audit"))
    parser.add_argument("--corpus-root", type=Path, default=CORPUS)
    parser.add_argument(
        "--output-root",
        type=Path,
        help="override baselines/diffractgpt/targets/<corpus>",
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
