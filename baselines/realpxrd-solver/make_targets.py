"""Build RealPXRD-Solver's native discrete-peak targets.

The released theoretical data store contains Pymatgen ``CuKa`` stick positions
and intensities; the dataset class then keeps rows whose normalized intensity is
strictly greater than five.  This builder reproduces that contract directly
from each hidden CIF and records the primitive-cell composition and lattice
needed by the two paper-native inference modes.
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
from pymatgen.core import Composition, Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

from verifiable_pxrd.baselines.targets import (
    COMMON_SUPPORT_FIELDS,
    configure_paths,
    validate_source_manifest,
)

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = ROOT.parent
DEFAULT_CORPUS = REPOSITORY_ROOT / "pxrd-bench" / "pXRD-100"
EXPECTED_CASES = 100
EXPECTED_VERSIONS = {
    "numpy": "2.4.6",
    "pymatgen": "2026.5.4",
    "python": "3.11.15",
}
WAVELENGTH_KEY = "CuKa"
WAVELENGTH_ANGSTROM = 1.54184
PAPER_NOMINAL_WAVELENGTH_ANGSTROM = 1.5406
TWO_THETA_RANGE = (5.0, 80.0)
INTENSITY_THRESHOLD = 5.0
PRIMITIVE_SYMPREC = 0.1
PRIMITIVE_ANGLE_TOLERANCE = 5.0
DEFAULT_INPUT_MODE = "lattice-free-primitive-formula-oracle"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: Any) -> None:
    temporary = path.with_suffix(path.suffix + ".partial")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def numerical_environment() -> dict[str, str]:
    actual = {
        "numpy": version("numpy"),
        "pymatgen": version("pymatgen"),
        "python": platform.python_version(),
    }
    if actual != EXPECTED_VERSIONS:
        raise RuntimeError(
            f"expected target environment {EXPECTED_VERSIONS}, found {actual}; "
            "use the repository uv environment"
        )
    calculator = XRDCalculator(wavelength=WAVELENGTH_KEY)
    if not math.isclose(calculator.wavelength, WAVELENGTH_ANGSTROM, abs_tol=1e-12):
        raise RuntimeError(
            f"Pymatgen {WAVELENGTH_KEY} resolved to {calculator.wavelength}, "
            f"expected {WAVELENGTH_ANGSTROM}"
        )
    return actual


def integral_counts(composition: Composition) -> list[tuple[str, int]]:
    counts: list[tuple[str, int]] = []
    for element in composition.elements:
        amount = float(composition[element])
        integer = round(amount)
        if not math.isclose(amount, integer, rel_tol=0, abs_tol=1e-8):
            raise RuntimeError(f"non-integral composition is unsupported: {composition}")
        counts.append((element.symbol, int(integer)))
    return counts


def explicit_formula(composition: Composition) -> str:
    return "".join(f"{symbol}{count}" for symbol, count in integral_counts(composition))


def atom_count(composition: Composition) -> int:
    return sum(count for _, count in integral_counts(composition))


def primitive_structure(structure: Structure) -> Structure:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        primitive = SpacegroupAnalyzer(
            structure,
            symprec=PRIMITIVE_SYMPREC,
            angle_tolerance=PRIMITIVE_ANGLE_TOLERANCE,
        ).find_primitive()
    return primitive if primitive is not None else structure.copy()


def primitive_metadata(structure: Structure) -> tuple[Structure, dict[str, Any]]:
    primitive = primitive_structure(structure)
    reduced, factor = primitive.composition.get_reduced_composition_and_factor()
    rounded_factor = round(float(factor))
    if not math.isclose(float(factor), rounded_factor, rel_tol=0, abs_tol=1e-8):
        raise RuntimeError(f"non-integral primitive formula multiplier: {factor}")
    lengths = [float(value) for value in primitive.lattice.abc]
    angles = [float(value) for value in primitive.lattice.angles]
    return primitive, {
        "primitive_cell_atom_count": atom_count(primitive.composition),
        "primitive_cell_composition": dict(integral_counts(primitive.composition)),
        "primitive_cell_formula": explicit_formula(primitive.composition),
        "primitive_cell_formula_unit_multiplier": int(rounded_factor),
        "primitive_cell_lattice_matrix_angstrom": [
            [float(value) for value in row] for row in primitive.lattice.matrix
        ],
        "primitive_cell_parameters": lengths + angles,
        "primitive_cell_volume_angstrom3": float(primitive.volume),
        "reduced_composition": dict(integral_counts(reduced)),
        "reduced_formula_explicit": explicit_formula(reduced),
        "reduced_formula_atom_count": atom_count(reduced),
    }


def simulate_native_peaks(structure: Structure) -> np.ndarray:
    pattern = XRDCalculator(wavelength=WAVELENGTH_KEY, symprec=0).get_pattern(
        structure, two_theta_range=TWO_THETA_RANGE
    )
    values = np.column_stack(
        [np.asarray(pattern.x, dtype=np.float64), np.asarray(pattern.y, dtype=np.float64)]
    )
    if values.ndim != 2 or values.shape[1] != 2 or not len(values):
        raise RuntimeError("native Pymatgen diffraction pattern is empty")
    if not np.isfinite(values).all() or not math.isclose(
        float(values[:, 1].max()), 100.0, abs_tol=1e-8
    ):
        raise RuntimeError("native Pymatgen diffraction pattern is invalid")
    return values


def model_peak_rows(values: np.ndarray) -> np.ndarray:
    retained = values[values[:, 1] > INTENSITY_THRESHOLD]
    if not len(retained):
        raise RuntimeError("no RealPXRD-Solver peaks survive the >5 intensity rule")
    return retained


def write_pattern(path: Path, values: np.ndarray) -> None:
    temporary = path.with_suffix(path.suffix + ".partial")
    np.savetxt(temporary, values, fmt=("%.10f", "%.10f"))
    temporary.replace(path)


def validate_support(case: dict[str, Any], policy: str) -> tuple[str, bool]:
    support = case.get("baseline_support")
    if policy in {"common-envelope", "require-all"} and isinstance(support, dict):
        failed = [field for field in COMMON_SUPPORT_FIELDS if support.get(field) is not True]
        if failed and policy == "require-all":
            raise RuntimeError(
                f"{case['case_id']}: outside required support envelope ({', '.join(failed)})"
            )
        if failed:
            return "unsupported_common_envelope:" + ",".join(failed), False
    if int(case.get("primitive_site_count", case.get("cif_site_count", 0))) <= 0:
        return "unsupported_missing_site_count", False
    return "supported_input_envelope_training_overlap_unresolved", True


def parameters() -> dict[str, Any]:
    return {
        "model_input": {
            "encoder_behavior": (
                "released BertModel casts two-theta values to integer degree bins and uses "
                "them as position-embedding indices"
            ),
            "intensity_filter": "strictly greater than 5 after max=100 normalization",
            "representation": "discrete two-theta/intensity list",
        },
        "primitive_cell": {
            "angle_tolerance_degrees": PRIMITIVE_ANGLE_TOLERANCE,
            "implementation": "pymatgen SpacegroupAnalyzer.find_primitive",
            "symprec_angstrom": PRIMITIVE_SYMPREC,
        },
        "simulation": {
            "background": "none",
            "broadening": "none; Pymatgen sticks",
            "calculator": "pymatgen.analysis.diffraction.xrd.XRDCalculator",
            "intensity_normalization": "Pymatgen maximum=100",
            "pymatgen_radiation_key": WAVELENGTH_KEY,
            "resolved_wavelength_angstrom": WAVELENGTH_ANGSTROM,
            "paper_nominal_wavelength_angstrom": PAPER_NOMINAL_WAVELENGTH_ANGSTROM,
            "two_theta_range_degrees_inclusive": list(TWO_THETA_RANGE),
        },
        "released_inference_defaults": {
            "candidates_per_case": 20,
            "infer_timesteps": 200,
            "step_lr": 5.0,
        },
    }


def source_path(corpus: Path, case: dict[str, Any]) -> Path:
    relative = PurePosixPath(str(case["path"]))
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"unsafe source path: {relative}")
    path = corpus / relative
    if sha256_file(path) != case["sha256"]:
        raise RuntimeError(f"source CIF digest mismatch: {path}")
    return path


def input_row(case: dict[str, Any], mode: str) -> dict[str, Any]:
    oracle = mode != "lattice-free-reduced-formula"
    lattice = mode == "lattice-conditioned-primitive-cell-oracle"
    return {
        "case_id": case["case_id"],
        "input_mode": mode,
        "pattern_path": case["pattern_path"],
        "formula": (case["primitive_cell_formula"] if oracle else case["reduced_formula_explicit"]),
        "atom_count": (
            case["primitive_cell_atom_count"] if oracle else case["reduced_formula_atom_count"]
        ),
        "cell_parameters": (
            json.dumps(case["primitive_cell_parameters"], separators=(",", ":")) if lattice else ""
        ),
        "oracle_input": oracle,
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    temporary = path.with_suffix(path.suffix + ".partial")
    with temporary.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def build(args: argparse.Namespace) -> None:
    versions = numerical_environment()
    paths = configure_paths(args.corpus_root, "realpxrd-solver", args.output_root)
    source_manifest = json.loads(paths["source_manifest"].read_text(encoding="utf-8"))
    dataset_id, cases = validate_source_manifest(
        source_manifest,
        expected_cases=args.expected_cases,
        dataset_id=args.dataset_id,
        case_prefix=args.case_prefix,
    )
    paths["output"].mkdir(parents=True, exist_ok=True)
    paths["patterns"].mkdir(parents=True, exist_ok=True)
    output_cases: list[dict[str, Any]] = []
    for case in cases:
        path = source_path(paths["corpus"], case)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            structure = Structure.from_file(path)
        primitive, metadata = primitive_metadata(structure)
        supplied_reduced = Composition(str(case["formula"])).reduced_composition
        if supplied_reduced != primitive.composition.reduced_composition:
            raise RuntimeError(f"{case['case_id']}: manifest formula and CIF disagree")
        peaks = simulate_native_peaks(primitive)
        retained = model_peak_rows(peaks)
        relative_pattern = PurePosixPath("patterns") / f"{case['case_id']}.xy"
        pattern_path = paths["output"] / relative_pattern
        write_pattern(pattern_path, peaks)
        applicability, supported = validate_support(case, args.support_policy)
        output_cases.append(
            {
                "case_id": case["case_id"],
                "framework_applicability": applicability,
                "model_supported": supported,
                "panel": case.get("panel"),
                "stream": case.get("stream"),
                "pattern_path": relative_pattern.as_posix(),
                "pattern_sha256": sha256_file(pattern_path),
                "native_peak_count": len(peaks),
                "model_peak_count": len(retained),
                "model_peak_two_theta_min_deg": float(retained[:, 0].min()),
                "model_peak_two_theta_max_deg": float(retained[:, 0].max()),
                "source_cif_path": case["path"],
                "source_cif_sha256": case["sha256"],
                "training_exposure": (
                    "unresolved; the authors release structures without a compact source-ID "
                    "or topology index"
                ),
                **metadata,
            }
        )
    manifest = {
        "schema_version": "1.0.0",
        "framework": "RealPXRD-Solver",
        "source_dataset_id": dataset_id,
        "case_prefix": args.case_prefix or str(cases[0]["case_id"]).split("-", 1)[0],
        "support_policy": args.support_policy,
        "source_manifest_sha256": sha256_file(paths["source_manifest"]),
        "pattern_count": len(output_cases),
        "supported_case_count": sum(case["model_supported"] for case in output_cases),
        "default_input_mode": DEFAULT_INPUT_MODE,
        "target_environment": versions,
        "parameters_sha256": "",
        "cases": output_cases,
    }
    parameters_path = paths["output"] / "parameters.json"
    write_json(parameters_path, parameters())
    manifest["parameters_sha256"] = sha256_file(parameters_path)
    write_json(paths["output_manifest"], manifest)

    modes = (
        "lattice-free-primitive-formula-oracle",
        "lattice-conditioned-primitive-cell-oracle",
        "lattice-free-reduced-formula",
    )
    rows_by_mode = {mode: [input_row(case, mode) for case in output_cases] for mode in modes}
    write_csv(paths["output"] / "inputs.csv", rows_by_mode[DEFAULT_INPUT_MODE])
    for mode, rows in rows_by_mode.items():
        write_csv(paths["output"] / f"inputs-{mode}.csv", rows)
    print(paths["output_manifest"])


def audit(args: argparse.Namespace) -> None:
    numerical_environment()
    paths = configure_paths(args.corpus_root, "realpxrd-solver", args.output_root)
    manifest = json.loads(paths["output_manifest"].read_text(encoding="utf-8"))
    source = json.loads(paths["source_manifest"].read_text(encoding="utf-8"))
    dataset_id, source_cases = validate_source_manifest(
        source,
        expected_cases=args.expected_cases,
        dataset_id=args.dataset_id,
        case_prefix=args.case_prefix,
    )
    if manifest["source_dataset_id"] != dataset_id:
        raise RuntimeError("target dataset identity mismatch")
    if manifest["source_manifest_sha256"] != sha256_file(paths["source_manifest"]):
        raise RuntimeError("target manifest is stale")
    if len(manifest["cases"]) != args.expected_cases:
        raise RuntimeError("target case count mismatch")
    source_by_id = {str(case["case_id"]): case for case in source_cases}
    for case in manifest["cases"]:
        source_case = source_by_id[str(case["case_id"])]
        path = paths["output"] / case["pattern_path"]
        if sha256_file(path) != case["pattern_sha256"]:
            raise RuntimeError(f"{case['case_id']}: pattern digest mismatch")
        values = np.loadtxt(path, dtype=np.float64)
        if values.ndim == 1:
            values = values.reshape(1, 2)
        if values.shape != (case["native_peak_count"], 2):
            raise RuntimeError(f"{case['case_id']}: native peak shape mismatch")
        if len(model_peak_rows(values)) != case["model_peak_count"]:
            raise RuntimeError(f"{case['case_id']}: model peak count mismatch")
        if sha256_file(source_path(paths["corpus"], source_case)) != case["source_cif_sha256"]:
            raise RuntimeError(f"{case['case_id']}: source digest mismatch")
    for name in (
        "inputs.csv",
        "inputs-lattice-free-primitive-formula-oracle.csv",
        "inputs-lattice-conditioned-primitive-cell-oracle.csv",
        "inputs-lattice-free-reduced-formula.csv",
    ):
        with (paths["output"] / name).open(encoding="utf-8", newline="") as stream:
            if sum(1 for _ in csv.DictReader(stream)) != args.expected_cases:
                raise RuntimeError(f"{name}: row count mismatch")
    print(f"OK: {args.expected_cases} RealPXRD-Solver targets for {dataset_id}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build", "audit"))
    parser.add_argument("--corpus-root", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument(
        "--output-root",
        type=Path,
        help="override baselines/realpxrd-solver/targets/<corpus>",
    )
    parser.add_argument("--dataset-id")
    parser.add_argument("--case-prefix")
    parser.add_argument(
        "--support-policy",
        choices=("manifest", "common-envelope", "require-all"),
        default="manifest",
    )
    parser.add_argument("--expected-cases", type=int, default=EXPECTED_CASES)
    args = parser.parse_args()
    if args.command == "build":
        build(args)
    else:
        audit(args)


if __name__ == "__main__":
    main()
