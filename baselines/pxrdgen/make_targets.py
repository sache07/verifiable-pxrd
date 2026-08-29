"""Build and audit PXRDGen-native deterministic pXRD targets for a corpus.

PXRDGen's published Code Ocean capsule calculates a GSAS-II ``ycalc`` profile
on a 5--80 degree 2theta range at 0.01 degree spacing, max-normalizes it, drops
the final inclusive endpoint, and supplies the resulting 7,500 intensities to
the CNN encoder. This script follows that implementation rather than replacing
it with a Pymatgen stick-pattern approximation.

The exact capsule source and GSAS-II runtime are prepared as documented in
``baselines/pxrdgen/README.md``. Typical use::

    python baselines/pxrdgen/make_targets.py validate-reference
    python baselines/pxrdgen/make_targets.py build
    python baselines/pxrdgen/make_targets.py audit
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib
import json
import math
import os
import re
import subprocess
import sys
import tempfile
from collections import OrderedDict
from pathlib import Path, PurePosixPath
from typing import Any

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
SOURCE_MANIFEST = CORPUS / "manifest.json"
OUTPUT = configure_paths(CORPUS, "pxrdgen")["output"]
PATTERNS = OUTPUT / "patterns"
OUTPUT_MANIFEST = OUTPUT / "manifest.json"
PARAMETERS_PATH = OUTPUT / "parameters.json"
INPUTS_PATH = OUTPUT / "inputs.csv"
PRIMARY_INPUTS_PATH = OUTPUT / "inputs-reduced-formula.csv"
ORACLE_INPUTS_PATH = OUTPUT / "inputs-primitive-cell-formula-oracle.csv"
DATASET_ID: str | None = None
CASE_PREFIX: str | None = None
SUPPORT_POLICY = "manifest"

UPSTREAM = ROOT / ".upstream" / "PXRDGen"
UPSTREAM_INSTRUMENT = UPSTREAM / "code" / "Rietveld" / "INST_XRY_Cu.PRM"
DEFAULT_GSASII_DIR = ROOT / ".runs" / "envs" / "pxrdgen-gsas2full" / "GSAS-II" / "GSASII"

EXPECTED_CASES = 100
POINT_COUNT = 7500
TWO_THETA_START = 5.0
TWO_THETA_STOP = 80.0
TWO_THETA_STEP = 0.01
REFERENCE_TOLERANCE = 1.0e-4
UPSTREAM_INSTRUMENT_SHA256 = "364f124b53f956f2d1f876134d1df1dff6c6cabdd612fc5d8272c1de3ae9c9e8"
CAPSULE_UUID = "75fac1ae-f64b-41ef-9680-ef896215fa3c"
CAPSULE_DOI = "10.24433/CO.6347299.v1"

FORMULA_TOKEN = re.compile(r"[A-Z][a-z]?|\(|\)|(?:\d+(?:\.\d*)?|\.\d+)")
FORMULA_SUM = re.compile(r"^_chemical_formula_sum\s+(?:'([^']+)'|\"([^\"]+)\"|(\S+))", re.MULTILINE)


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


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    temporary = path.with_suffix(path.suffix + ".partial")
    with temporary.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def configure_dataset(args: argparse.Namespace) -> None:
    global CORPUS, SOURCE_MANIFEST, OUTPUT, PATTERNS, OUTPUT_MANIFEST
    global PARAMETERS_PATH, INPUTS_PATH, PRIMARY_INPUTS_PATH, ORACLE_INPUTS_PATH
    global DATASET_ID, CASE_PREFIX, SUPPORT_POLICY
    paths = configure_paths(args.corpus_root, "pxrdgen", args.output_root)
    CORPUS = paths["corpus"]
    SOURCE_MANIFEST = paths["source_manifest"]
    OUTPUT = paths["output"]
    PATTERNS = paths["patterns"]
    OUTPUT_MANIFEST = paths["output_manifest"]
    PARAMETERS_PATH = OUTPUT / "parameters.json"
    INPUTS_PATH = OUTPUT / "inputs.csv"
    PRIMARY_INPUTS_PATH = OUTPUT / "inputs-reduced-formula.csv"
    ORACLE_INPUTS_PATH = OUTPUT / "inputs-primitive-cell-formula-oracle.csv"
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


def parse_formula(formula: str) -> OrderedDict[str, float]:
    """Parse the corpus's integer/decimal, optionally parenthesized formulas."""

    compact = formula.replace(" ", "")
    tokens = FORMULA_TOKEN.findall(compact)
    if "".join(tokens) != compact:
        raise ValueError(f"unsupported formula syntax: {formula}")
    stack: list[OrderedDict[str, float]] = [OrderedDict()]
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token == "(":
            stack.append(OrderedDict())
            index += 1
            continue
        if token == ")":
            if len(stack) == 1:
                raise ValueError(f"unbalanced formula: {formula}")
            group = stack.pop()
            multiplier = 1.0
            if index + 1 < len(tokens) and re.fullmatch(r"\d+(?:\.\d*)?|\.\d+", tokens[index + 1]):
                multiplier = float(tokens[index + 1])
                index += 1
            for element, amount in group.items():
                stack[-1][element] = stack[-1].get(element, 0.0) + amount * multiplier
            index += 1
            continue
        if re.fullmatch(r"\d+(?:\.\d*)?|\.\d+", token):
            raise ValueError(f"orphan number in formula: {formula}")
        amount = 1.0
        if index + 1 < len(tokens) and re.fullmatch(r"\d+(?:\.\d*)?|\.\d+", tokens[index + 1]):
            amount = float(tokens[index + 1])
            index += 1
        stack[-1][token] = stack[-1].get(token, 0.0) + amount
        index += 1
    if len(stack) != 1:
        raise ValueError(f"unbalanced formula: {formula}")
    return stack[0]


def formula_sum_from_cif(path: Path) -> tuple[str, OrderedDict[str, float]]:
    text = path.read_text(encoding="utf-8")
    match = FORMULA_SUM.search(text)
    if not match:
        raise RuntimeError(f"CIF has no _chemical_formula_sum: {path}")
    spaced = next(group for group in match.groups() if group is not None)
    amounts: OrderedDict[str, float] = OrderedDict()
    compact_parts: list[str] = []
    for token in spaced.split():
        parsed = re.fullmatch(r"([A-Z][a-z]?)(\d+(?:\.\d*)?|\.\d+)", token)
        if not parsed:
            raise RuntimeError(f"unsupported _chemical_formula_sum token {token!r}: {path}")
        element, amount_text = parsed.groups()
        amount = float(amount_text)
        amounts[element] = amounts.get(element, 0.0) + amount
        if not amount.is_integer():
            raise RuntimeError(f"PXRDGen sample parser requires integer occupancy: {path}")
        compact_parts.append(f"{element}{int(amount)}")
    return "".join(compact_parts), amounts


def formula_metadata(case: dict[str, Any], cif_path: Path) -> dict[str, Any]:
    reduced_formula = case["formula"]
    reduced = parse_formula(reduced_formula)
    target_cell_formula, target_cell = formula_sum_from_cif(cif_path)
    if set(reduced) != set(target_cell):
        raise RuntimeError(f"formula element mismatch: {case['case_id']}")
    target_ratios = [target_cell[element] / reduced[element] for element in reduced]
    if not target_ratios or any(
        not math.isclose(ratio, target_ratios[0], abs_tol=1e-8) for ratio in target_ratios
    ):
        raise RuntimeError(f"formula multiplicities are not proportional: {case['case_id']}")
    reduced_count = sum(reduced.values())
    target_cell_count = sum(target_cell.values())
    if not math.isclose(target_cell_count, case["cif_site_count"], abs_tol=1e-8):
        raise RuntimeError(f"target CIF cell atom count mismatch: {case['case_id']}")
    primitive_count = float(case["primitive_site_count"])
    primitive_multiplier = primitive_count / reduced_count
    target_cell_multiplier = target_cell_count / reduced_count
    if not math.isclose(primitive_multiplier, round(primitive_multiplier), abs_tol=1e-8):
        raise RuntimeError(f"noninteger primitive formula multiplier: {case['case_id']}")
    if not math.isclose(target_cell_multiplier, round(target_cell_multiplier), abs_tol=1e-8):
        raise RuntimeError(f"noninteger target-cell formula multiplier: {case['case_id']}")
    primitive_multiplier = round(primitive_multiplier)
    target_cell_multiplier = round(target_cell_multiplier)
    primitive_formula = "".join(
        f"{element}{int(amount * primitive_multiplier)}" for element, amount in reduced.items()
    )
    return {
        "reduced_formula": reduced_formula,
        "reduced_formula_atom_count": int(reduced_count),
        "primitive_cell_formula": primitive_formula,
        "primitive_cell_atom_count": int(primitive_count),
        "primitive_formula_unit_multiplier": primitive_multiplier,
        "primitive_formula_differs_from_reduced": primitive_multiplier != 1,
        "target_cif_cell_formula": target_cell_formula,
        "target_cif_cell_atom_count": int(target_cell_count),
        "target_cif_cell_formula_unit_multiplier": target_cell_multiplier,
        "target_cif_cell_formula_differs_from_reduced": target_cell_multiplier != 1,
    }


def load_gsasii(gsasii_dir: Path) -> tuple[Any, Any, dict[str, Any]]:
    directory = gsasii_dir.resolve()
    if not (directory / "GSASIIscriptable.py").is_file():
        raise RuntimeError(
            f"GSAS-II scripting source not found at {directory}; see baselines/pxrdgen/README.md"
        )
    sys.path.insert(0, str(directory))
    GSASIIpath = importlib.import_module("GSASIIpath")
    G2sc = importlib.import_module("GSASIIscriptable")
    # Importing GSASIIpwd directly first enters a circular import in the frozen
    # GSAS-II revision (GSASIIlattice -> GSASIImath -> GSASIIfiles ->
    # GSASIIstrIO -> partially initialized GSASIIlattice).  The supported
    # scripting entry point initializes those modules in a viable order.
    GSASIIpwd = importlib.import_module("GSASIIpwd")
    np = importlib.import_module("numpy")

    if getattr(GSASIIpwd, "pyd", None) is None:
        raise RuntimeError(
            "GSAS-II pypowder binary is unavailable; install the host Fortran "
            "runtime (libgfortran5 on Ubuntu) before native-profile simulation"
        )

    G2sc.SetPrintLevel("none")
    revision = int(GSASIIpath.GetVersionNumber())
    checkout = directory.parent
    commit = None
    if (checkout / ".git").exists():
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=checkout,
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            commit = result.stdout.strip()
    runtime = {
        "gsasii_commit": commit,
        "gsasii_revision": revision,
        "numpy_version": np.__version__,
        "python_version": sys.version.split()[0],
    }
    return G2sc, np, runtime


def validate_instrument(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise RuntimeError(
            f"PXRDGen instrument file missing: {path}; run baselines/pxrdgen/prepare.py download"
        )
    digest = sha256_file(path)
    if path == UPSTREAM_INSTRUMENT and digest != UPSTREAM_INSTRUMENT_SHA256:
        raise RuntimeError(f"official instrument digest mismatch: {path}")
    text = path.read_text(encoding="utf-8")
    required = (
        "INS   HTYPE   PXCR",
        "INS  1 IRAD     3",
        "1.540560  1.544330",
        "2.000000E+00  -2.000000E+00   5.000000E+00",
        "0.000000E+00   0.000000E+00   0.100000E-01   0.100000E-01",
    )
    if any(item not in text for item in required):
        raise RuntimeError(f"instrument parameters do not match PXRDGen: {path}")
    try:
        displayed_path = str(path.relative_to(UPSTREAM))
        path_key = "upstream_path"
    except ValueError:
        displayed_path = str(path.relative_to(ROOT))
        path_key = "repository_path"
    return {path_key: displayed_path, "sha256": digest}


def simulate(
    G2sc: Any,
    np: Any,
    cif_path: Path,
    instrument_path: Path,
    case_id: str,
) -> tuple[Any, dict[str, Any]]:
    with tempfile.TemporaryDirectory(prefix=f"pxrdgen-{case_id}-") as directory:
        gpx_path = Path(directory) / "simulation.gpx"
        project = G2sc.G2Project(filename=str(gpx_path))
        project.add_phase(str(cif_path), fmthint="CIF", phasename="B")
        project.add_simulated_powder_histogram(
            "A simulation",
            str(instrument_path),
            TWO_THETA_START,
            TWO_THETA_STOP,
            TWO_THETA_STEP,
            phases=project.phases(),
            scale=1.0,
        )
        project.data["Controls"]["data"]["max cyc"] = 0
        project.do_refinements([{}])
        ycalc = np.asarray(project.histogram(0).getdata("ycalc"), dtype=np.float64)
    if ycalc.shape != (POINT_COUNT + 1,):
        raise RuntimeError(f"unexpected GSAS-II ycalc shape for {case_id}: {ycalc.shape}")
    maximum = float(np.max(ycalc))
    if not math.isfinite(maximum) or maximum <= 0:
        raise RuntimeError(f"empty/non-finite profile for {case_id}")
    # Match the capsule's order exactly: normalize the inclusive ycalc first,
    # then remove the 80-degree endpoint supplied by GSAS-II.
    intensity = (ycalc / maximum)[:-1]
    if intensity.shape != (POINT_COUNT,) or not np.all(np.isfinite(intensity)):
        raise RuntimeError(f"invalid normalized profile for {case_id}")
    return intensity, {
        "argmax_index": int(np.argmax(intensity)),
        "argmax_two_theta_deg": float(TWO_THETA_START + np.argmax(intensity) * TWO_THETA_STEP),
        "intensity_max_before_normalization": maximum,
        "intensity_min_after_normalization": float(np.min(intensity)),
    }


def write_pattern(path: Path, np: Any, intensity: Any) -> None:
    temporary = path.with_suffix(path.suffix + ".partial")
    np.savetxt(temporary, intensity, fmt="%.7f")
    temporary.replace(path)


def parameter_record(runtime: dict[str, Any], instrument: dict[str, Any]) -> dict[str, Any]:
    return {
        "background": {
            "explicit_background": "none",
            "profile_tail_note": (
                "Nonzero low baseline values are deterministic peak tails in GSAS-II ycalc."
            ),
        },
        "capsule": {
            "doi": CAPSULE_DOI,
            "uuid": CAPSULE_UUID,
            "version": "1.0",
        },
        "engine": {
            "calculator": "GSASIIscriptable.G2Project.add_simulated_powder_histogram",
            "data_channel": "ycalc",
            "max_refinement_cycles": 0,
            "runtime": runtime,
            "scale": 1.0,
        },
        "grid": {
            "gsasii_inclusive_point_count": POINT_COUNT + 1,
            "model_last_point_deg": 79.99,
            "model_point_count": POINT_COUNT,
            "start_deg": TWO_THETA_START,
            "step_deg": TWO_THETA_STEP,
            "stop_deg_gsasii_inclusive": TWO_THETA_STOP,
            "transformation": "normalize inclusive ycalc, then drop its final 80.00-degree point",
        },
        "instrument": {
            "azimuth_deg": 0.0,
            "geometry": "Bragg-Brentano constant-wavelength X-ray (PXCR)",
            "instrument_file": instrument,
            "polarization": 0.7,
            "profile": {
                "legacy_gsas_profile_function": 3,
                "U": 2.0,
                "V": -2.0,
                "W": 5.0,
                "X": 0.0,
                "Y": 0.0,
                "Z": 0.0,
                "SH_over_L": 0.002,
                "note": (
                    "Effective GSAS-II pseudo-Voigt/profile coefficients after loading the "
                    "legacy PRM file; retain the PRM rather than treating them as a constant "
                    "FWHM."
                ),
            },
            "radiation": {
                "Kalpha1_angstrom": 1.540560,
                "Kalpha2_angstrom": 1.544330,
                "I_Kalpha2_over_I_Kalpha1": 0.5,
                "source_code": "CuKa (IRAD=3)",
            },
            "zero_shift_deg": 0.0,
        },
        "intensity": {
            "file_format": "one normalized scalar per line, fixed to seven decimal places",
            "normalization": "ycalc / max(ycalc), before dropping the inclusive endpoint",
            "noise": "none (calculated ycalc is used, not noisy observed y)",
            "range": [0.0, 1.0],
        },
        "model_input": {
            "encoder": "published flow_CNN (CNN PXRD encoder)",
            "shape": [POINT_COUNT],
        },
    }


def build(args: argparse.Namespace) -> None:
    G2sc, np, runtime = load_gsasii(args.gsasii_dir)
    instrument = validate_instrument(args.instrument)
    cases = load_source_cases()
    PATTERNS.mkdir(parents=True, exist_ok=True)
    output_cases: list[dict[str, Any]] = []
    combined_rows: list[dict[str, Any]] = []
    primary_rows: list[dict[str, Any]] = []
    oracle_rows: list[dict[str, Any]] = []
    for index, case in enumerate(cases, start=1):
        cif_path = source_path(case)
        formulas = formula_metadata(case, cif_path)
        intensity, simulation = simulate(G2sc, np, cif_path, args.instrument, case["case_id"])
        relative_pattern = PurePosixPath("patterns") / f"{case['case_id']}.dat"
        pattern_path = OUTPUT / relative_pattern
        write_pattern(pattern_path, np, intensity)
        applicability, supported = framework_support(
            case, framework_key="pxrdgen", policy=SUPPORT_POLICY
        )
        common = {
            "case_id": case["case_id"],
            "panel": case["panel"],
            "pattern_path": relative_pattern.as_posix(),
            "framework_applicability": applicability,
            "model_supported": supported,
        }
        combined_rows.append(
            {
                **common,
                **formulas,
                "primary_mode": "reduced_formula",
                "oracle_mode": "primitive_cell_formula_from_hidden_cif",
                "site_count_domain": (
                    "executable_mp20_site_count_domain"
                    if formulas["primitive_cell_atom_count"] <= 20
                    else "executable_out_of_mp20_site_count_domain"
                ),
            }
        )
        primary_rows.append(
            {
                **common,
                "formula": formulas["reduced_formula"],
                "model_num_atoms": formulas["reduced_formula_atom_count"],
                "input_mode": "reduced_formula_strict_declared_composition",
                "primitive_multiplicity_matches": not formulas[
                    "primitive_formula_differs_from_reduced"
                ],
            }
        )
        oracle_rows.append(
            {
                **common,
                "formula": formulas["primitive_cell_formula"],
                "model_num_atoms": formulas["primitive_cell_atom_count"],
                "input_mode": "primitive_cell_formula_oracle_from_hidden_cif",
                "formula_unit_multiplier": formulas["primitive_formula_unit_multiplier"],
            }
        )
        output_cases.append(
            {
                **common,
                **formulas,
                "pattern_sha256": sha256_file(pattern_path),
                "source_cif_path": case["path"],
                "source_cif_sha256": case["sha256"],
                **simulation,
            }
        )
        if index % 10 == 0 or index == len(cases):
            print(f"generated {index}/{len(cases)} PXRDGen patterns")

    primitive_differing = sum(
        row["primitive_formula_differs_from_reduced"] for row in combined_rows
    )
    target_cell_differing = sum(
        row["target_cif_cell_formula_differs_from_reduced"] for row in combined_rows
    )
    write_csv(INPUTS_PATH, combined_rows)
    write_csv(PRIMARY_INPUTS_PATH, primary_rows)
    write_csv(ORACLE_INPUTS_PATH, oracle_rows)
    write_json(PARAMETERS_PATH, parameter_record(runtime, instrument))
    write_json(
        OUTPUT_MANIFEST,
        {
            "cases": output_cases,
            "framework": "PXRDGen",
            "generator": "baselines/pxrdgen/make_targets.py",
            "source_dataset_id": json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))[
                "dataset_id"
            ],
            "case_prefix": CASE_PREFIX,
            "support_policy": SUPPORT_POLICY,
            "input_modes": {
                "oracle_diagnostic": "inputs-primitive-cell-formula-oracle.csv",
                "primary": "inputs-reduced-formula.csv",
            },
            "numerical_environment": runtime,
            "parameter_file": "parameters.json",
            "pattern_count": len(output_cases),
            "primitive_formula_differs_from_reduced_count": primitive_differing,
            "target_cif_cell_formula_differs_from_reduced_count": target_cell_differing,
            "schema_version": "1.0.0",
            "source_manifest": relative_reference(SOURCE_MANIFEST, from_directory=OUTPUT),
            "source_manifest_sha256": sha256_file(SOURCE_MANIFEST),
            "supported_case_count": sum(case["model_supported"] for case in output_cases),
            "unsupported_case_count": sum(not case["model_supported"] for case in output_cases),
        },
    )


def audit(args: argparse.Namespace) -> None:
    G2sc, np, runtime = load_gsasii(args.gsasii_dir)
    validate_instrument(args.instrument)
    source_cases = {case["case_id"]: case for case in load_source_cases()}
    expected_primitive_differing = 0
    expected_target_cell_differing = 0
    for source in source_cases.values():
        formulas = formula_metadata(source, source_path(source))
        expected_primitive_differing += formulas["primitive_formula_differs_from_reduced"]
        expected_target_cell_differing += formulas["target_cif_cell_formula_differs_from_reduced"]
    manifest = json.loads(OUTPUT_MANIFEST.read_text(encoding="utf-8"))
    errors: list[str] = []
    max_resimulation_error = 0.0
    cases = manifest.get("cases", [])
    if len(cases) != EXPECTED_CASES:
        errors.append(f"pattern count {len(cases)} != {EXPECTED_CASES}")
    if manifest.get("source_manifest_sha256") != sha256_file(SOURCE_MANIFEST):
        errors.append("source manifest digest mismatch")
    expected_supported = sum(
        framework_support(case, framework_key="pxrdgen", policy=SUPPORT_POLICY)[1]
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
    if manifest.get("primitive_formula_differs_from_reduced_count") != expected_primitive_differing:
        errors.append("unexpected reduced/primitive formula difference count")
    if (
        manifest.get("target_cif_cell_formula_differs_from_reduced_count")
        != expected_target_cell_differing
    ):
        errors.append("unexpected reduced/target-cell formula difference count")
    for case in cases:
        case_id = case["case_id"]
        source = source_cases.get(case_id)
        if source is None:
            errors.append(f"{case_id}: absent from source manifest")
            continue
        path = OUTPUT / case["pattern_path"]
        if not path.is_file():
            errors.append(f"{case_id}: missing pattern")
            continue
        if sha256_file(path) != case["pattern_sha256"]:
            errors.append(f"{case_id}: pattern digest mismatch")
        try:
            values = np.loadtxt(path)
        except Exception as exc:
            errors.append(f"{case_id}: cannot parse pattern: {exc}")
            continue
        if values.shape != (POINT_COUNT,):
            errors.append(f"{case_id}: pattern shape {values.shape}")
        elif not math.isclose(float(values.max()), 1.0, abs_tol=5e-8):
            errors.append(f"{case_id}: pattern maximum {values.max()}")
        if case["source_cif_sha256"] != source["sha256"]:
            errors.append(f"{case_id}: source CIF digest mismatch in target manifest")
        expected_values, _ = simulate(G2sc, np, source_path(source), args.instrument, case_id)
        difference = float(np.max(np.abs(expected_values - values)))
        max_resimulation_error = max(max_resimulation_error, difference)
        if difference > 5e-8:
            errors.append(f"{case_id}: resimulation error {difference:.12g} > 5e-8")
    for csv_path in (INPUTS_PATH, PRIMARY_INPUTS_PATH, ORACLE_INPUTS_PATH):
        with csv_path.open(encoding="utf-8", newline="") as stream:
            if sum(1 for _ in csv.DictReader(stream)) != EXPECTED_CASES:
                errors.append(f"{csv_path.name}: expected {EXPECTED_CASES} rows")
    if errors:
        raise RuntimeError("PXRDGen target audit failed:\n- " + "\n- ".join(errors))
    print(
        f"OK: {EXPECTED_CASES} PXRDGen targets; "
        f"{expected_primitive_differing} reduced/primitive and "
        f"{expected_target_cell_differing} reduced/target-cell differences; "
        f"GSAS-II r{runtime['gsasii_revision']}; "
        f"max resimulation error {max_resimulation_error:.12g}"
    )


def validate_reference(args: argparse.Namespace) -> None:
    G2sc, np, runtime = load_gsasii(args.gsasii_dir)
    validate_instrument(args.instrument)
    references = (
        "Ba2Mg1Os1O6",
        "Ca2La2Fe2Sn2O12",
    )
    errors: list[str] = []
    for stem in references:
        target = UPSTREAM / "code" / "xrd2struc" / "samples" / f"{stem}_target.cif"
        expected_path = UPSTREAM / "code" / "xrd2struc" / "samples" / f"{stem}_XRD.dat"
        if not target.is_file() or not expected_path.is_file():
            raise RuntimeError(
                "capsule reference files are missing; run baselines/pxrdgen/prepare.py download"
            )
        observed, _ = simulate(G2sc, np, target, args.instrument, f"reference-{stem}")
        expected = np.loadtxt(expected_path)
        maximum_error = float(np.max(np.abs(observed - expected)))
        peak_match = int(np.argmax(observed)) == int(np.argmax(expected))
        print(
            f"{stem}: max_abs_error={maximum_error:.9g}, "
            f"peak_index={int(np.argmax(observed))}, "
            f"reference_peak_index={int(np.argmax(expected))}"
        )
        if (
            expected.shape != (POINT_COUNT,)
            or maximum_error > REFERENCE_TOLERANCE
            or not peak_match
        ):
            errors.append(f"{stem}: reference validation failed")
    if errors:
        raise RuntimeError("\n".join(errors))
    print(
        f"OK: capsule references reproduced within {REFERENCE_TOLERANCE:g} "
        f"using GSAS-II r{runtime['gsasii_revision']}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build", "audit", "validate-reference"))
    parser.add_argument("--corpus-root", type=Path, default=CORPUS)
    parser.add_argument(
        "--output-root",
        type=Path,
        help="override baselines/pxrdgen/targets/<corpus>",
    )
    parser.add_argument("--dataset-id")
    parser.add_argument("--case-prefix")
    parser.add_argument("--support-policy", choices=SUPPORT_POLICIES, default="manifest")
    parser.add_argument(
        "--gsasii-dir",
        type=Path,
        default=Path(os.environ.get("PXRDGEN_GSASII_DIR", DEFAULT_GSASII_DIR)),
    )
    parser.add_argument("--instrument", type=Path, default=UPSTREAM_INSTRUMENT)
    args = parser.parse_args()
    configure_dataset(args)
    if args.command == "build":
        build(args)
    elif args.command == "audit":
        audit(args)
    else:
        validate_reference(args)


if __name__ == "__main__":
    main()
