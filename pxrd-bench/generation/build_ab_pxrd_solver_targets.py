"""Build and audit Ab-PXRD-Solver-native targets for a locked pXRD corpus.

The released solver consumes two-column ``2theta,intensity`` CSV files.  Its
synthetic-data helper uses GSAS-II on an inclusive 10--80 degree grid at 0.02
degree spacing with Cu K-alpha-average radiation.  The paper describes the
preprocessing and refinement stages but leaves these numerical simulation
parameters to the code release.

The benchmark stores both the clean calculated profile and a deterministically
seeded realization of the released Poisson-plus-Gaussian noise recipe.  The
seeded profile is the inference input; the clean profile is retained for audit.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib
import io
import json
import math
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path, PurePosixPath
from typing import Any

from target_dataset import SUPPORT_POLICIES, configure_paths, validate_source_manifest

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CORPUS = ROOT / "pXRD-100"
DEFAULT_UPSTREAM = ROOT / "Ab-PXRD-Solver"
DEFAULT_GSASII_DIR = ROOT / ".runs" / "envs" / "pxrdgen-gsas2full" / "GSAS-II" / "GSASII"

EXPECTED_CASES = 100
FRAMEWORK_DIR = "ab-pxrd-solver"
FIXEDPARAMS_OUTPUT_DIR = "fixedparams-v1"
SOURCE_COMMIT = "0d67964dfcbd2e2fa09e79bbbac2f5d020a121e9"
GSASII_COMPATIBILITY_COMMIT = "1a0aeec6c61b54f68e6812704730a471187ac393"
PAPER_URL = "https://arxiv.org/abs/2605.24594"
REPOSITORY_URL = "https://github.com/MaterSim/Ab-PXRD-Solver"

WAVELENGTH = 1.54184
TWO_THETA_START = 10.0
TWO_THETA_STOP = 80.0
TWO_THETA_STEP = 0.02
POINT_COUNT = 3501
PROFILE = {"U": 0.2, "V": -0.2, "W": 2.0, "X": 0.5, "Y": 0.5}
CRYSTALLITE_SIZE_MICROMETER = 20.0
BACKGROUND_RATIO = 0.0
MAX_COUNTS = 5000
GAUSSIAN_NOISE_LEVEL = 0.001
DEFAULT_SEED_BASE = 20260721
RESIMULATION_TOLERANCE = 5.0e-10

# Explicit, framework-independent controlled profile. Unlike the released
# helper above, these values are written to the active GSAS-II parameter slots
# and the sample broadening model is set with valid GSAS-II data structures.
FIXEDPARAMS_PROFILE_KEY = "fixedparams-v1"
FIXEDPARAMS_DIR = "patterns-fixedparams"
FIXEDPARAMS_WAVELENGTH = 1.5406
FIXEDPARAMS_TWO_THETA_START = 5.0
FIXEDPARAMS_TWO_THETA_STOP = 90.0
FIXEDPARAMS_TWO_THETA_STEP = 0.01
FIXEDPARAMS_POINT_COUNT = 8501
FIXEDPARAMS_PROFILE = {"U": 2.0, "V": -2.0, "W": 5.0, "X": 0.0, "Y": 0.0}
FIXEDPARAMS_ZERO = 0.0
FIXEDPARAMS_POLARIZATION = 0.7
FIXEDPARAMS_SH_OVER_L = 0.002
FIXEDPARAMS_CRYSTALLITE_SIZE_MICROMETER = 1.0
FIXEDPARAMS_MICROSTRAIN = 1000.0
FIXEDPARAMS_SIZE_LORENTZIAN_FRACTION = 1.0
FIXEDPARAMS_MICROSTRAIN_LORENTZIAN_FRACTION = 1.0
FIXEDPARAMS_MAX_COUNTS = 5000
FIXEDPARAMS_GAUSSIAN_NOISE_COUNTS = 5.0
FIXEDPARAMS_GAUSSIAN_NOISE_LEVEL = FIXEDPARAMS_GAUSSIAN_NOISE_COUNTS / FIXEDPARAMS_MAX_COUNTS


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".partial")
    temporary.write_text(value, encoding="utf-8")
    temporary.replace(path)


def write_json(path: Path, value: Any) -> None:
    atomic_text(path, json.dumps(value, indent=2, sort_keys=True) + "\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".partial")
    with temporary.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def git_commit(path: Path) -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=path,
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def load_source(
    corpus: Path,
    dataset_id: str | None,
    case_prefix: str | None,
    expected_cases: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    source_path = corpus / "manifest.json"
    source = json.loads(source_path.read_text(encoding="utf-8"))
    _, cases = validate_source_manifest(
        source,
        expected_cases=expected_cases,
        dataset_id=dataset_id,
        case_prefix=case_prefix,
    )
    return source, cases


def source_cif(corpus: Path, case: dict[str, Any]) -> Path:
    relative = PurePosixPath(str(case["path"]))
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"unsafe source path: {relative}")
    path = corpus / relative
    if sha256_file(path) != case["sha256"]:
        raise RuntimeError(f"source CIF digest mismatch: {path}")
    return path


def applicability(case: dict[str, Any], policy: str) -> tuple[str, bool]:
    if policy not in SUPPORT_POLICIES:
        raise ValueError(f"unknown support policy: {policy}")
    envelope = case.get("baseline_support")
    if isinstance(envelope, dict):
        required = (
            "common_element_vocabulary",
            "ordered_full_occupancy",
            "primitive_site_count_at_most_20",
        )
        missing = [field for field in required if field not in envelope]
        if missing:
            raise RuntimeError(f"{case['case_id']}: baseline_support lacks {', '.join(missing)}")
        failed = [field for field in required if envelope[field] is not True]
        supported = not failed
        label = (
            "supported_common_envelope"
            if supported
            else "unsupported_common_envelope:" + ",".join(failed)
        )
    else:
        site_count = int(case.get("primitive_site_count", 0))
        supported = 1 <= site_count <= 20
        label = (
            "supported_ordered_mp20_native_defaults"
            if supported
            else "unsupported_native_max_atoms_20"
        )
    if policy == "require-all" and not supported:
        raise RuntimeError(f"{case['case_id']}: outside required support envelope ({label})")
    return label, supported


def validate_upstream(upstream: Path, gsasii_dir: Path) -> dict[str, Any]:
    required = {
        "constants.py": upstream / "pxrd_app" / "constants.py",
        "gsas.py": upstream / "pxrd_app" / "tools" / "gsas.py",
        "synthetic_recipe.py": (
            upstream / "pxrd_app" / "tools" / "peak_finder" / "predict_single.py"
        ),
        "instrument": upstream / "pxrd_app" / "tools" / "INST_XRY.PRM",
        "environment": upstream / "environment.yml",
    }
    missing = [str(path) for path in required.values() if not path.is_file()]
    if missing:
        raise RuntimeError("Ab-PXRD-Solver source is incomplete: " + ", ".join(missing))
    commit = git_commit(upstream)
    if commit != SOURCE_COMMIT:
        raise RuntimeError(f"expected Ab-PXRD-Solver {SOURCE_COMMIT}, found {commit}")
    if not (gsasii_dir / "GSASIIscriptable.py").is_file():
        raise RuntimeError(f"GSAS-II scripting runtime is missing: {gsasii_dir}")
    instrument_text = required["instrument"].read_text(encoding="utf-8")
    for token in (
        "INS   HTYPE   PXCR",
        "INS  1 IRAD     3",
        "1.541840",
        "2.000000E+00  -2.000000E+00   5.000000E+00",
    ):
        if token not in instrument_text:
            raise RuntimeError(f"released instrument file lacks {token!r}")
    return {
        "commit": commit,
        "files": {
            key: {"path": str(path.relative_to(upstream)), "sha256": sha256_file(path)}
            for key, path in required.items()
        },
    }


def native_noise(clean: Any, seed: int, np: Any) -> Any:
    maximum = float(np.max(clean))
    if not math.isfinite(maximum) or maximum <= 0:
        raise RuntimeError("clean profile has no positive finite maximum")
    counts = np.maximum(clean / maximum * MAX_COUNTS, 0.0)
    random_state = np.random.RandomState(seed)
    noisy_counts = random_state.poisson(counts).astype(float)
    noisy_counts += random_state.normal(
        0.0, GAUSSIAN_NOISE_LEVEL * MAX_COUNTS, size=len(noisy_counts)
    )
    noisy = noisy_counts * (maximum / MAX_COUNTS)
    noisy_maximum = float(np.max(noisy))
    if not math.isfinite(noisy_maximum) or noisy_maximum <= 0:
        raise RuntimeError("seeded noisy profile has no positive finite maximum")
    return noisy / noisy_maximum * 100.0


def fixedparams_noise(clean: Any, seed: int, np: Any) -> Any:
    maximum = float(np.max(clean))
    if not math.isfinite(maximum) or maximum <= 0:
        raise RuntimeError("fixed-parameter clean profile has no positive finite maximum")
    counts = np.maximum(clean / maximum * FIXEDPARAMS_MAX_COUNTS, 0.0)
    random_state = np.random.RandomState(seed)
    noisy_counts = random_state.poisson(counts).astype(float)
    noisy_counts += random_state.normal(
        0.0,
        FIXEDPARAMS_GAUSSIAN_NOISE_COUNTS,
        size=len(noisy_counts),
    )
    noisy_maximum = float(np.max(noisy_counts))
    if not math.isfinite(noisy_maximum) or noisy_maximum <= 0:
        raise RuntimeError("fixed-parameter noisy profile has no positive finite maximum")
    return noisy_counts / noisy_maximum * 100.0


def _set_active_instrument_parameter(instrument: dict[str, Any], name: str, value: float) -> None:
    record = instrument.get(name)
    if not isinstance(record, list) or len(record) < 2:
        raise RuntimeError(f"GSAS-II instrument parameter {name!r} is unavailable")
    record[0] = value
    record[1] = value
    if len(record) >= 3:
        record[2] = False


def _assert_close(actual: Any, expected: float, label: str) -> None:
    if not math.isclose(float(actual), expected, rel_tol=0.0, abs_tol=1.0e-12):
        raise RuntimeError(f"effective {label} is {actual!r}, expected {expected!r}")


def _simulate_fixedparams_job(job: tuple[str, str, str, int]) -> dict[str, Any]:
    case_id, cif_text, upstream_text, seed = job
    upstream = Path(upstream_text)
    for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ[name] = "1"
    sys.path.insert(0, str(upstream))
    np = importlib.import_module("numpy")
    from pxrd_app.tools.gsas import _load_gsas_scriptable

    with tempfile.TemporaryDirectory(prefix=f"fixedparams-{case_id}-") as temporary:
        os.environ["PXRD_TMP_ROOT"] = temporary
        output = io.StringIO()
        with redirect_stdout(output), redirect_stderr(output):
            G2sc = _load_gsas_scriptable()
            project = G2sc.G2Project(newgpx=str(Path(temporary) / "simulation.gpx"))
            phase = project.add_phase(cif_text, phasename="Target")
            histogram = project.add_simulated_powder_histogram(
                histname="FixedParams",
                iparams=str(upstream / "pxrd_app" / "tools" / "INST_XRY.PRM"),
                Tmin=FIXEDPARAMS_TWO_THETA_START,
                Tmax=FIXEDPARAMS_TWO_THETA_STOP,
                Tstep=FIXEDPARAMS_TWO_THETA_STEP,
                wavelength=FIXEDPARAMS_WAVELENGTH,
                scale=1.0,
                phases=[phase],
            )

            instrument = histogram.data["Instrument Parameters"][0]
            for parameter, value in {
                "Lam": FIXEDPARAMS_WAVELENGTH,
                "Zero": FIXEDPARAMS_ZERO,
                "Polariz.": FIXEDPARAMS_POLARIZATION,
                "SH/L": FIXEDPARAMS_SH_OVER_L,
                **FIXEDPARAMS_PROFILE,
            }.items():
                _set_active_instrument_parameter(instrument, parameter, value)

            background = histogram.data["Background"][0]
            if not isinstance(background, list) or len(background) < 4:
                raise RuntimeError("unexpected GSAS-II background parameter structure")
            background[1] = False
            for index in range(3, len(background)):
                background[index] = 0.0

            phase_histogram = phase.data["Histograms"][histogram.name]
            size = phase_histogram["Size"]
            size[0] = "isotropic"
            size[1][0] = FIXEDPARAMS_CRYSTALLITE_SIZE_MICROMETER
            size[1][1] = FIXEDPARAMS_CRYSTALLITE_SIZE_MICROMETER
            size[1][2] = FIXEDPARAMS_SIZE_LORENTZIAN_FRACTION
            size[2] = [False, False, False]

            microstrain = phase_histogram["Mustrain"]
            microstrain[0] = "isotropic"
            microstrain[1][0] = FIXEDPARAMS_MICROSTRAIN
            microstrain[1][1] = FIXEDPARAMS_MICROSTRAIN
            microstrain[1][2] = FIXEDPARAMS_MICROSTRAIN_LORENTZIAN_FRACTION
            microstrain[2] = [False, False, False]

            preferred_orientation = phase_histogram["Pref.Ori."]
            preferred_orientation[1] = 1.0
            preferred_orientation[2] = False
            histogram.data["Sample Parameters"]["DisplaceX"] = [0.0, False]
            histogram.data["Sample Parameters"]["DisplaceY"] = [0.0, False]

            project.do_refinements()

            for parameter, value in {
                "Lam": FIXEDPARAMS_WAVELENGTH,
                "Zero": FIXEDPARAMS_ZERO,
                "Polariz.": FIXEDPARAMS_POLARIZATION,
                "SH/L": FIXEDPARAMS_SH_OVER_L,
                **FIXEDPARAMS_PROFILE,
            }.items():
                _assert_close(instrument[parameter][1], value, parameter)
            if size[0] != "isotropic":
                raise RuntimeError(f"effective size model is {size[0]!r}")
            _assert_close(
                size[1][0],
                FIXEDPARAMS_CRYSTALLITE_SIZE_MICROMETER,
                "crystallite size",
            )
            if microstrain[0] != "isotropic":
                raise RuntimeError(f"effective microstrain model is {microstrain[0]!r}")
            _assert_close(microstrain[1][0], FIXEDPARAMS_MICROSTRAIN, "microstrain")

            data = histogram.data["data"][1]
            x = np.asarray(data[0], dtype=np.float64)
            clean = np.asarray(data[3], dtype=np.float64)
            calculated_background = np.asarray(data[4], dtype=np.float64)

    if float(np.max(np.abs(calculated_background))) > 1.0e-10:
        raise RuntimeError(
            f"{case_id}: fixed-parameter GSAS-II background is not zero "
            f"({float(np.max(np.abs(calculated_background))):.12g})"
        )
    expected_x = np.linspace(
        FIXEDPARAMS_TWO_THETA_START,
        FIXEDPARAMS_TWO_THETA_STOP,
        FIXEDPARAMS_POINT_COUNT,
    )
    if x.shape != (FIXEDPARAMS_POINT_COUNT,) or clean.shape != (FIXEDPARAMS_POINT_COUNT,):
        raise RuntimeError(f"{case_id}: unexpected fixed-parameter shape {x.shape}/{clean.shape}")
    if float(np.max(np.abs(x - expected_x))) > 1.0e-10:
        raise RuntimeError(f"{case_id}: unexpected fixed-parameter angle grid")
    if not np.all(np.isfinite(clean)) or float(np.max(clean)) <= 0:
        raise RuntimeError(f"{case_id}: invalid fixed-parameter clean profile")
    clean = clean / float(np.max(clean)) * 100.0
    noisy = fixedparams_noise(clean, seed, np)
    return {
        "case_id": case_id,
        "x": x,
        "clean": clean,
        "noisy": noisy,
        "seed": seed,
    }


def _simulate_job(job: tuple[str, str, str, int]) -> dict[str, Any]:
    case_id, cif_text, upstream_text, seed = job
    upstream = Path(upstream_text)
    for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ[name] = "1"
    sys.path.insert(0, str(upstream))
    np = importlib.import_module("numpy")
    from pxrd_app.tools.gsas import simulate_pxrd

    with tempfile.TemporaryDirectory(prefix=f"ab-pxrd-{case_id}-") as temporary:
        os.environ["PXRD_TMP_ROOT"] = temporary
        output = io.StringIO()
        with redirect_stdout(output), redirect_stderr(output):
            x, clean = simulate_pxrd(
                cif_text,
                U=PROFILE["U"],
                V=PROFILE["V"],
                W=PROFILE["W"],
                X=PROFILE["X"],
                Y=PROFILE["Y"],
                grainsize=CRYSTALLITE_SIZE_MICROMETER,
                bg_ratio=BACKGROUND_RATIO,
                add_noise=False,
                Tmin=TWO_THETA_START,
                Tmax=TWO_THETA_STOP,
                Tstep=TWO_THETA_STEP,
                wavelength=WAVELENGTH,
                max_counts=MAX_COUNTS,
                iparams=str(upstream / "pxrd_app" / "tools" / "INST_XRY.PRM"),
            )
    x = np.asarray(x, dtype=np.float64)
    clean = np.asarray(clean, dtype=np.float64)
    expected_x = np.linspace(TWO_THETA_START, TWO_THETA_STOP, POINT_COUNT)
    if x.shape != (POINT_COUNT,) or clean.shape != (POINT_COUNT,):
        raise RuntimeError(f"{case_id}: unexpected profile shape {x.shape}/{clean.shape}")
    if float(np.max(np.abs(x - expected_x))) > 1.0e-10:
        raise RuntimeError(f"{case_id}: GSAS-II returned an unexpected angle grid")
    if not np.all(np.isfinite(clean)) or not math.isclose(
        float(clean.max()), 100.0, abs_tol=1.0e-10
    ):
        raise RuntimeError(f"{case_id}: invalid clean profile")
    noisy = native_noise(clean, seed, np)
    return {
        "case_id": case_id,
        "x": x,
        "clean": clean,
        "noisy": noisy,
        "seed": seed,
    }


def simulate_cases(
    corpus: Path,
    cases: list[dict[str, Any]],
    upstream: Path,
    gsasii_dir: Path,
    seed_base: int,
    workers: int,
) -> list[dict[str, Any]]:
    os.environ["GSASII_PATH"] = str(gsasii_dir.resolve())
    jobs = [
        (
            str(case["case_id"]),
            str(source_cif(corpus, case).resolve()),
            str(upstream.resolve()),
            seed_base + index,
        )
        for index, case in enumerate(cases)
    ]
    if workers <= 1:
        return [_simulate_job(job) for job in jobs]
    with ProcessPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(_simulate_job, jobs, chunksize=1))


def simulate_fixedparams_cases(
    corpus: Path,
    cases: list[dict[str, Any]],
    upstream: Path,
    gsasii_dir: Path,
    seed_base: int,
    workers: int,
) -> list[dict[str, Any]]:
    os.environ["GSASII_PATH"] = str(gsasii_dir.resolve())
    jobs = [
        (
            str(case["case_id"]),
            str(source_cif(corpus, case).resolve()),
            str(upstream.resolve()),
            seed_base + index,
        )
        for index, case in enumerate(cases)
    ]
    if workers <= 1:
        return [_simulate_fixedparams_job(job) for job in jobs]
    with ProcessPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(_simulate_fixedparams_job, jobs, chunksize=1))


def write_pattern(path: Path, x: Any, y: Any, np: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".partial")
    with temporary.open("w", encoding="utf-8") as stream:
        stream.write("2theta,intensity\n")
        np.savetxt(stream, np.column_stack((x, y)), delimiter=",", fmt="%.17g")
    temporary.replace(path)


def runtime_record(gsasii_dir: Path) -> dict[str, Any]:
    sys.path.insert(0, str(gsasii_dir.resolve()))
    GSASIIpath = importlib.import_module("GSASIIpath")
    np = importlib.import_module("numpy")
    checkout = gsasii_dir.parent
    resolved_dir = gsasii_dir.resolve()
    try:
        displayed_dir = str(resolved_dir.relative_to(ROOT))
    except ValueError:
        displayed_dir = str(resolved_dir)
    return {
        "python_version": sys.version.split()[0],
        "numpy_version": np.__version__,
        "gsasii_revision": int(GSASIIpath.GetVersionNumber()),
        "gsasii_commit": git_commit(checkout),
        "gsasii_source_dir": displayed_dir,
        "compatibility_note": (
            "The Ab-PXRD-Solver release leaves GSAS-II unpinned. sim-bench uses this "
            "hash-pinned compatible runtime and records it rather than claiming a "
            "paper-era revision."
        ),
    }


def parameters(
    source_info: dict[str, Any], runtime: dict[str, Any], seed_base: int
) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "framework": "Ab-PXRD-Solver",
        "paper": {
            "citation": (
                "Su et al., Ab-initio Crystal Structure Determination from Powder "
                "X-Ray Diffraction (2026)"
            ),
            "url": PAPER_URL,
            "documented": [
                "Stage 1.1: adaptive background subtraction, smoothing, SciPy peak "
                "detection, and CNN filtering",
                "Stage 3.2: normalized cross-correlation screening",
                "Stage 3.3: GSAS-II Rietveld refinement",
            ],
            "parameter_gap": (
                "The paper does not report wavelength, angle grid, profile coefficients, "
                "crystallite size, or synthetic-noise values; these come from the released code."
            ),
        },
        "source": {
            "repository": REPOSITORY_URL,
            **source_info,
        },
        "engine": {
            "calculator": "released pxrd_app.tools.gsas.simulate_pxrd using GSAS-II ycalc",
            "runtime": runtime,
            "instrument_file": source_info["files"]["instrument"],
        },
        "radiation": {
            "label": "Cu Kalpha average",
            "wavelength_angstrom": WAVELENGTH,
        },
        "grid": {
            "axis": "2theta_deg",
            "start_deg": TWO_THETA_START,
            "stop_deg_inclusive": TWO_THETA_STOP,
            "step_deg": TWO_THETA_STEP,
            "point_count": POINT_COUNT,
        },
        "profile": {
            "family": "GSAS-II constant-wavelength type-3 profile with released Caglioti overrides",
            **PROFILE,
            "crystallite_size_micrometer": CRYSTALLITE_SIZE_MICROMETER,
        },
        "background": {
            "ratio_to_maximum": BACKGROUND_RATIO,
            "added_background": False,
        },
        "native_noise": {
            "consumed_by_benchmark": True,
            "seed_base": seed_base,
            "seed_rule": "seed_base + zero-based source-manifest case index",
            "poisson": True,
            "maximum_counts": MAX_COUNTS,
            "gaussian_relative_sigma": GAUSSIAN_NOISE_LEVEL,
            "generator": "numpy.random.RandomState",
        },
        "clean_profile": {
            "retained_for_audit": True,
            "noise": "none",
        },
        "intensity": {
            "native_normalization": "divide by the post-noise maximum and multiply by 100",
            "clean_normalization": "divide GSAS-II ycalc by its maximum and multiply by 100",
            "negative_native_values_possible": True,
        },
        "model_input": {
            "format": "two-column CSV with 2theta,intensity header",
            "formula": "benchmark reduced composition, passed explicitly with --formula",
            "space_group": "not supplied; --infer-spg is required",
            "one_process_per_case": (
                "required because the stock batch CLI has only one global --formula override"
            ),
        },
    }


def fixedparams_parameters(
    source_info: dict[str, Any], runtime: dict[str, Any], seed_base: int
) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "profile_key": FIXEDPARAMS_PROFILE_KEY,
        "purpose": (
            "A framework-independent controlled PXRD condition for comparing "
            "structure-determination ability while holding measurement parameters fixed."
        ),
        "engine": {
            "calculator": (
                "GSAS-II ycalc configured directly by sim-bench; does not call the "
                "released simulate_pxrd parameter-mutating helper"
            ),
            "runtime": runtime,
            "instrument_file": source_info["files"]["instrument"],
            "parameter_application": (
                "Both initial and active GSAS-II instrument slots are written and "
                "asserted after calculation. Size and microstrain use valid isotropic "
                "histogram/phase records."
            ),
        },
        "radiation": {
            "label": "monochromatic Cu Kalpha1",
            "wavelength_angstrom": FIXEDPARAMS_WAVELENGTH,
            "single_wavelength": True,
        },
        "grid": {
            "axis": "2theta_deg",
            "start_deg": FIXEDPARAMS_TWO_THETA_START,
            "stop_deg_inclusive": FIXEDPARAMS_TWO_THETA_STOP,
            "step_deg": FIXEDPARAMS_TWO_THETA_STEP,
            "point_count": FIXEDPARAMS_POINT_COUNT,
        },
        "instrument_profile": {
            "family": "GSAS-II constant-wavelength type-3 pseudo-Voigt/FCJ",
            **FIXEDPARAMS_PROFILE,
            "zero_shift_deg": FIXEDPARAMS_ZERO,
            "polarization": FIXEDPARAMS_POLARIZATION,
            "SH_over_L": FIXEDPARAMS_SH_OVER_L,
        },
        "sample_broadening": {
            "crystallite_size": {
                "model": "isotropic",
                "micrometer": FIXEDPARAMS_CRYSTALLITE_SIZE_MICROMETER,
                "lorentzian_fraction": FIXEDPARAMS_SIZE_LORENTZIAN_FRACTION,
            },
            "microstrain": {
                "model": "isotropic",
                "value_microstrain": FIXEDPARAMS_MICROSTRAIN,
                "lorentzian_fraction": FIXEDPARAMS_MICROSTRAIN_LORENTZIAN_FRACTION,
            },
        },
        "sample_effects": {
            "preferred_orientation": "none (March-Dollase ratio fixed at 1)",
            "sample_displacement_x": 0.0,
            "sample_displacement_y": 0.0,
            "hstrain": "zero",
        },
        "background": {
            "state": "background-subtracted",
            "GSAS_chebyshev_coefficients": [0.0, 0.0, 0.0],
            "asserted_calculated_background_max_abs": 1.0e-10,
        },
        "noise": {
            "seed_base": seed_base,
            "seed_rule": "seed_base + zero-based source-manifest case index",
            "poisson": True,
            "maximum_counts": FIXEDPARAMS_MAX_COUNTS,
            "gaussian_sigma_counts": FIXEDPARAMS_GAUSSIAN_NOISE_COUNTS,
            "gaussian_relative_sigma": FIXEDPARAMS_GAUSSIAN_NOISE_LEVEL,
            "generator": "numpy.random.RandomState",
        },
        "intensity": {
            "clean_normalization": "divide GSAS-II ycalc by its maximum and multiply by 100",
            "output_normalization": "divide post-noise counts by their maximum and multiply by 100",
            "negative_values_possible_after_noise": True,
        },
        "approximate_fwhm_deg_without_axial_asymmetry": {
            "10": 0.0594,
            "20": 0.0618,
            "40": 0.0680,
            "60": 0.0769,
            "80": 0.0900,
        },
        "source": {
            "upstream_repository": REPOSITORY_URL,
            **source_info,
        },
    }


def readme(dataset_id: str, case_count: int) -> str:
    return f"""# Ab-PXRD-Solver targets

These {case_count} targets are native two-column `2theta,intensity` inputs for
Ab-PXRD-Solver, bound to dataset `{dataset_id}`. `patterns/` contains the seeded
native noisy profile consumed during inference; `patterns-clean/` retains the
noise-free GSAS-II calculation for deterministic audit.

The released numerical contract is Cu Kalpha-average at 1.54184 Angstrom, an
inclusive 10--80 degree two-theta grid at 0.02 degree spacing (3,501 points),
GSAS profile overrides U=0.2, V=-0.2, W=2.0, X=0.5, Y=0.5, 20 micrometer
crystallite size, no background, Poisson noise at 5,000 maximum counts, and
Gaussian noise with relative sigma 0.001. Intensities are normalized to a
maximum of 100.

The paper documents background subtraction, smoothing, peak extraction, PXRD
similarity screening, and GSAS-II refinement, but not the numerical simulation
parameters: [Stage 1.1 and Stage 3 in the paper]({PAPER_URL}) and the
[released implementation]({REPOSITORY_URL}/tree/{SOURCE_COMMIT}).
`parameters.json` separates paper statements from code-derived values and pins
all source/runtime hashes.

The benchmark supplies only the reduced formula and pXRD. Run each row of
`inputs.csv` independently with `--formula <formula> --infer-spg`; target space
groups are not embedded in filenames or supplied to the solver. The stock batch
CLI cannot attach a different formula override to each file, so the sim-bench
Modal adapter performs one upstream invocation per case.
"""


def fixedparams_readme(dataset_id: str, case_count: int) -> str:
    return f"""# Fixed-parameter PXRD targets

`{FIXEDPARAMS_DIR}/` contains the seeded noisy patterns for all {case_count} structures
in `{dataset_id}` under one explicit, framework-independent measurement
condition. These files are separate from the released Ab-PXRD-Solver-style
`patterns/` and have not replaced inputs used by earlier inference runs.

The fixed condition uses monochromatic Cu Kalpha1 radiation at
{FIXEDPARAMS_WAVELENGTH} Angstrom. The inclusive two-theta grid spans
{FIXEDPARAMS_TWO_THETA_START:g}--{FIXEDPARAMS_TWO_THETA_STOP:g} degrees with
{FIXEDPARAMS_TWO_THETA_STEP:g} degree sampling
({FIXEDPARAMS_POINT_COUNT:,} points).

GSAS-II is configured directly with U={FIXEDPARAMS_PROFILE["U"]:g},
V={FIXEDPARAMS_PROFILE["V"]:g}, W={FIXEDPARAMS_PROFILE["W"]:g},
X={FIXEDPARAMS_PROFILE["X"]:g}, Y={FIXEDPARAMS_PROFILE["Y"]:g}, polarization
{FIXEDPARAMS_POLARIZATION:g}, SH/L={FIXEDPARAMS_SH_OVER_L:g}, and zero shift.
Sample broadening is explicitly isotropic: crystallite size
{FIXEDPARAMS_CRYSTALLITE_SIZE_MICROMETER:g} micrometer, microstrain
{FIXEDPARAMS_MICROSTRAIN:g}, and Lorentzian fraction 1 for both. Preferred
orientation and sample displacement are disabled, and the calculated
background is asserted to be zero.

Each clean calculation is converted to a maximum of
{FIXEDPARAMS_MAX_COUNTS:,} counts, sampled with Poisson noise, augmented with
Gaussian noise of sigma {FIXEDPARAMS_GAUSSIAN_NOISE_COUNTS:g} counts, and
normalized to a maximum of 100. Seeds are deterministic and recorded per case.

See `parameters.json`, `manifest.json`, and `inputs.csv` for the complete
reproducibility record.
"""


def build_fixedparams(args: argparse.Namespace) -> None:
    corpus = args.corpus_root.expanduser().resolve()
    upstream = args.upstream_root.expanduser().resolve()
    gsasii_dir = args.gsasii_dir.expanduser().resolve()
    output = corpus / "targets" / FIXEDPARAMS_OUTPUT_DIR
    pattern_dir = output / FIXEDPARAMS_DIR
    source_info = validate_upstream(upstream, gsasii_dir)
    source, cases = load_source(
        corpus, args.dataset_id, args.case_prefix, args.expected_cases
    )
    simulated = simulate_fixedparams_cases(
        corpus, cases, upstream, gsasii_dir, args.seed_base, args.workers
    )
    import numpy as np

    by_id = {row["case_id"]: row for row in simulated}
    output_cases: list[dict[str, Any]] = []
    input_rows: list[dict[str, Any]] = []
    for case in cases:
        case_id = str(case["case_id"])
        result = by_id[case_id]
        pattern_path = pattern_dir / f"{case_id}.csv"
        write_pattern(pattern_path, result["x"], result["noisy"], np)
        label, supported = applicability(case, args.support_policy)
        formula = str(case["formula"])
        output_cases.append(
            {
                "case_id": case_id,
                "panel": case.get("panel"),
                "stream": case.get("stream"),
                "formula": formula,
                "source_cif_sha256": case["sha256"],
                "pattern_path": str(pattern_path.relative_to(output)),
                "pattern_sha256": sha256_file(pattern_path),
                "point_count": FIXEDPARAMS_POINT_COUNT,
                "noise_seed": result["seed"],
                "model_applicability": label,
                "model_supported": supported,
                "input_contract": "pXRD plus reduced composition",
            }
        )
        input_rows.append(
            {
                "case_id": case_id,
                "panel": case.get("panel", ""),
                "stream": case.get("stream") or "",
                "formula": formula,
                "pattern_path": str(pattern_path.relative_to(corpus)),
                "model_supported": supported,
                "model_applicability": label,
            }
        )

    parameter_path = output / "parameters.json"
    write_json(
        parameter_path,
        fixedparams_parameters(source_info, runtime_record(gsasii_dir), args.seed_base),
    )
    case_prefix = args.case_prefix or str(cases[0]["case_id"]).split("-", 1)[0]
    manifest = {
        "schema_version": "1.0.0",
        "profile_key": FIXEDPARAMS_PROFILE_KEY,
        "source_dataset_id": source["dataset_id"],
        "source_manifest": "../../manifest.json",
        "source_manifest_sha256": sha256_file(corpus / "manifest.json"),
        "case_prefix": case_prefix,
        "support_policy": args.support_policy,
        "case_count": len(output_cases),
        "supported_case_count": sum(bool(row["model_supported"]) for row in output_cases),
        "unsupported_case_count": sum(not bool(row["model_supported"]) for row in output_cases),
        "input_contract": "pXRD plus reduced composition; fixed measurement profile",
        "parameters_path": parameter_path.name,
        "parameters_sha256": sha256_file(parameter_path),
        "cases": output_cases,
    }
    write_json(output / "manifest.json", manifest)
    write_csv(output / "inputs.csv", input_rows)
    atomic_text(
        output / "README.md",
        fixedparams_readme(str(source["dataset_id"]), len(output_cases)),
    )
    print(
        f"Built {len(output_cases)} {FIXEDPARAMS_PROFILE_KEY} targets for "
        f"{source['dataset_id']} with {args.workers} worker(s)"
    )


def build(args: argparse.Namespace) -> None:
    corpus = args.corpus_root.expanduser().resolve()
    upstream = args.upstream_root.expanduser().resolve()
    gsasii_dir = args.gsasii_dir.expanduser().resolve()
    paths = configure_paths(corpus, FRAMEWORK_DIR)
    output = paths["output"]
    pattern_dir = output / "patterns"
    clean_dir = output / "patterns-clean"
    source_info = validate_upstream(upstream, gsasii_dir)
    source, cases = load_source(
        corpus, args.dataset_id, args.case_prefix, args.expected_cases
    )
    simulated = simulate_cases(corpus, cases, upstream, gsasii_dir, args.seed_base, args.workers)
    import numpy as np

    by_id = {row["case_id"]: row for row in simulated}
    output_cases: list[dict[str, Any]] = []
    input_rows: list[dict[str, Any]] = []
    for case in cases:
        case_id = str(case["case_id"])
        result = by_id[case_id]
        noisy_path = pattern_dir / f"{case_id}.csv"
        clean_path = clean_dir / f"{case_id}.csv"
        write_pattern(noisy_path, result["x"], result["noisy"], np)
        write_pattern(clean_path, result["x"], result["clean"], np)
        label, supported = applicability(case, args.support_policy)
        formula = str(case["formula"])
        output_cases.append(
            {
                "case_id": case_id,
                "panel": case.get("panel"),
                "stream": case.get("stream"),
                "formula": formula,
                "source_cif_sha256": case["sha256"],
                "pattern_path": str(noisy_path.relative_to(output)),
                "pattern_sha256": sha256_file(noisy_path),
                "clean_pattern_path": str(clean_path.relative_to(output)),
                "clean_pattern_sha256": sha256_file(clean_path),
                "point_count": POINT_COUNT,
                "noise_seed": result["seed"],
                "model_applicability": label,
                "model_supported": supported,
                "input_contract": "pXRD plus reduced composition; infer space group",
            }
        )
        input_rows.append(
            {
                "case_id": case_id,
                "panel": case.get("panel", ""),
                "stream": case.get("stream") or "",
                "formula": formula,
                "pattern_path": str(noisy_path.relative_to(corpus)),
                "clean_pattern_path": str(clean_path.relative_to(corpus)),
                "infer_spg": True,
                "model_supported": supported,
                "model_applicability": label,
            }
        )
    source_manifest_sha = sha256_file(corpus / "manifest.json")
    case_prefix = args.case_prefix or str(cases[0]["case_id"]).split("-", 1)[0]
    manifest = {
        "schema_version": "1.0.0",
        "framework": "Ab-PXRD-Solver",
        "source_dataset_id": source["dataset_id"],
        "source_manifest": "../../manifest.json",
        "source_manifest_sha256": source_manifest_sha,
        "case_prefix": case_prefix,
        "support_policy": args.support_policy,
        "case_count": len(output_cases),
        "supported_case_count": sum(bool(row["model_supported"]) for row in output_cases),
        "unsupported_case_count": sum(not bool(row["model_supported"]) for row in output_cases),
        "input_contract": "pXRD plus reduced composition; --infer-spg; no hidden space group",
        "parameters_path": "parameters.json",
        "parameters_sha256": "written-after-parameter-record",
        "cases": output_cases,
    }
    parameter_path = output / "parameters.json"
    write_json(parameter_path, parameters(source_info, runtime_record(gsasii_dir), args.seed_base))
    manifest["parameters_sha256"] = sha256_file(parameter_path)
    write_json(output / "manifest.json", manifest)
    write_csv(output / "inputs.csv", input_rows)
    atomic_text(output / "README.md", readme(str(source["dataset_id"]), len(output_cases)))
    print(
        f"Built {len(output_cases)} Ab-PXRD-Solver targets for {source['dataset_id']} "
        f"with {args.workers} worker(s)"
    )


def load_pattern(path: Path, np: Any) -> tuple[Any, Any]:
    values = np.loadtxt(path, delimiter=",", skiprows=1)
    if values.shape != (POINT_COUNT, 2):
        raise RuntimeError(f"unexpected pattern shape {values.shape}: {path}")
    return values[:, 0], values[:, 1]


def audit(args: argparse.Namespace) -> None:
    corpus = args.corpus_root.expanduser().resolve()
    upstream = args.upstream_root.expanduser().resolve()
    gsasii_dir = args.gsasii_dir.expanduser().resolve()
    output = corpus / "targets" / FRAMEWORK_DIR
    validate_upstream(upstream, gsasii_dir)
    source, cases = load_source(
        corpus, args.dataset_id, args.case_prefix, args.expected_cases
    )
    source_by_id = {str(case["case_id"]): case for case in cases}
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    parameter_record = json.loads((output / "parameters.json").read_text(encoding="utf-8"))
    errors: list[str] = []
    if manifest.get("source_dataset_id") != source["dataset_id"]:
        errors.append("source dataset ID mismatch")
    if manifest.get("source_manifest_sha256") != sha256_file(corpus / "manifest.json"):
        errors.append("source manifest digest mismatch")
    if manifest.get("parameters_sha256") != sha256_file(output / "parameters.json"):
        errors.append("parameter digest mismatch")
    if parameter_record.get("native_noise", {}).get("seed_base") != args.seed_base:
        errors.append("noise seed-base mismatch")
    output_cases = list(manifest.get("cases", []))
    if len(output_cases) != args.expected_cases:
        errors.append(
            f"target case count {len(output_cases)} != {args.expected_cases}"
        )
    if len({row.get("case_id") for row in output_cases}) != args.expected_cases:
        errors.append("target case IDs are not unique")
    with (output / "inputs.csv").open(encoding="utf-8", newline="") as stream:
        input_rows = list(csv.DictReader(stream))
    if len(input_rows) != args.expected_cases:
        errors.append(
            f"inputs.csv row count {len(input_rows)} != {args.expected_cases}"
        )
    if any(row.get("infer_spg") != "True" for row in input_rows):
        errors.append("inputs.csv does not require --infer-spg for every case")
    import numpy as np

    expected_x = np.linspace(TWO_THETA_START, TWO_THETA_STOP, POINT_COUNT)
    for index, row in enumerate(output_cases):
        case_id = str(row.get("case_id"))
        source_case = source_by_id.get(case_id)
        if source_case is None:
            errors.append(f"{case_id}: absent from source manifest")
            continue
        if row.get("source_cif_sha256") != source_case["sha256"]:
            errors.append(f"{case_id}: source CIF digest mismatch")
        for kind, path_key, hash_key in (
            ("native", "pattern_path", "pattern_sha256"),
            ("clean", "clean_pattern_path", "clean_pattern_sha256"),
        ):
            path = output / str(row[path_key])
            if not path.is_file():
                errors.append(f"{case_id}: missing {kind} pattern")
                continue
            if sha256_file(path) != row[hash_key]:
                errors.append(f"{case_id}: {kind} pattern digest mismatch")
                continue
            try:
                x, y = load_pattern(path, np)
            except Exception as exc:
                errors.append(f"{case_id}: cannot read {kind} pattern: {exc}")
                continue
            if not np.all(np.isfinite(y)):
                errors.append(f"{case_id}: non-finite {kind} intensity")
            if float(np.max(np.abs(x - expected_x))) > 1.0e-10:
                errors.append(f"{case_id}: unexpected {kind} angle grid")
            if not math.isclose(float(y.max()), 100.0, abs_tol=1.0e-9):
                errors.append(f"{case_id}: {kind} maximum is {float(y.max())}")
        expected_seed = args.seed_base + index
        if row.get("noise_seed") != expected_seed:
            errors.append(f"{case_id}: noise seed mismatch")

    if errors:
        raise RuntimeError("Ab-PXRD-Solver target audit failed:\n- " + "\n- ".join(errors))

    resimulated = simulate_cases(corpus, cases, upstream, gsasii_dir, args.seed_base, args.workers)
    by_id = {row["case_id"]: row for row in resimulated}
    max_clean_error = 0.0
    max_native_error = 0.0
    for row in output_cases:
        case_id = str(row["case_id"])
        _, observed_clean = load_pattern(output / row["clean_pattern_path"], np)
        _, observed_native = load_pattern(output / row["pattern_path"], np)
        expected = by_id[case_id]
        clean_error = float(np.max(np.abs(observed_clean - expected["clean"])))
        native_error = float(np.max(np.abs(observed_native - expected["noisy"])))
        max_clean_error = max(max_clean_error, clean_error)
        max_native_error = max(max_native_error, native_error)
        if clean_error > RESIMULATION_TOLERANCE:
            errors.append(f"{case_id}: clean resimulation error {clean_error:.12g}")
        if native_error > RESIMULATION_TOLERANCE:
            errors.append(f"{case_id}: native resimulation error {native_error:.12g}")
    if errors:
        raise RuntimeError("Ab-PXRD-Solver target audit failed:\n- " + "\n- ".join(errors))
    print(
        f"OK: {args.expected_cases} Ab-PXRD-Solver targets for {source['dataset_id']}; "
        f"max clean/native resimulation error "
        f"{max_clean_error:.12g}/{max_native_error:.12g}"
    )


def audit_fixedparams(args: argparse.Namespace) -> None:
    corpus = args.corpus_root.expanduser().resolve()
    upstream = args.upstream_root.expanduser().resolve()
    gsasii_dir = args.gsasii_dir.expanduser().resolve()
    output = corpus / "targets" / FIXEDPARAMS_OUTPUT_DIR
    validate_upstream(upstream, gsasii_dir)
    source, cases = load_source(
        corpus, args.dataset_id, args.case_prefix, args.expected_cases
    )
    source_by_id = {str(case["case_id"]): case for case in cases}
    manifest_path = output / "manifest.json"
    parameter_path = output / "parameters.json"
    input_path = output / "inputs.csv"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    parameter_record = json.loads(parameter_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    if manifest.get("profile_key") != FIXEDPARAMS_PROFILE_KEY:
        errors.append("fixed-parameter profile key mismatch")
    if manifest.get("source_dataset_id") != source["dataset_id"]:
        errors.append("source dataset ID mismatch")
    if manifest.get("source_manifest_sha256") != sha256_file(corpus / "manifest.json"):
        errors.append("source manifest digest mismatch")
    if manifest.get("parameters_sha256") != sha256_file(parameter_path):
        errors.append("fixed-parameter digest mismatch")
    if parameter_record.get("profile_key") != FIXEDPARAMS_PROFILE_KEY:
        errors.append("fixed-parameter record profile key mismatch")
    if parameter_record.get("noise", {}).get("seed_base") != args.seed_base:
        errors.append("fixed-parameter noise seed-base mismatch")

    output_cases = list(manifest.get("cases", []))
    if len(output_cases) != args.expected_cases:
        errors.append(
            f"fixed-parameter case count {len(output_cases)} != {args.expected_cases}"
        )
    if len({row.get("case_id") for row in output_cases}) != args.expected_cases:
        errors.append("fixed-parameter case IDs are not unique")
    with input_path.open(encoding="utf-8", newline="") as stream:
        input_rows = list(csv.DictReader(stream))
    if len(input_rows) != args.expected_cases:
        errors.append(
            f"inputs.csv row count {len(input_rows)} != {args.expected_cases}"
        )

    import numpy as np

    expected_x = np.linspace(
        FIXEDPARAMS_TWO_THETA_START,
        FIXEDPARAMS_TWO_THETA_STOP,
        FIXEDPARAMS_POINT_COUNT,
    )
    for index, row in enumerate(output_cases):
        case_id = str(row.get("case_id"))
        source_case = source_by_id.get(case_id)
        if source_case is None:
            errors.append(f"{case_id}: absent from source manifest")
            continue
        if row.get("source_cif_sha256") != source_case["sha256"]:
            errors.append(f"{case_id}: source CIF digest mismatch")
        path = output / str(row["pattern_path"])
        if path.parent.name != FIXEDPARAMS_DIR:
            errors.append(f"{case_id}: fixed-parameter path is outside {FIXEDPARAMS_DIR}")
            continue
        if not path.is_file():
            errors.append(f"{case_id}: missing fixed-parameter pattern")
            continue
        if sha256_file(path) != row["pattern_sha256"]:
            errors.append(f"{case_id}: fixed-parameter pattern digest mismatch")
            continue
        try:
            x, y = load_pattern_with_count(path, FIXEDPARAMS_POINT_COUNT, np)
        except Exception as exc:
            errors.append(f"{case_id}: cannot read fixed-parameter pattern: {exc}")
            continue
        if not np.all(np.isfinite(y)):
            errors.append(f"{case_id}: non-finite fixed-parameter intensity")
        if float(np.max(np.abs(x - expected_x))) > 1.0e-10:
            errors.append(f"{case_id}: unexpected fixed-parameter angle grid")
        if not math.isclose(float(y.max()), 100.0, abs_tol=1.0e-9):
            errors.append(f"{case_id}: fixed-parameter maximum is {float(y.max())}")
        if row.get("point_count") != FIXEDPARAMS_POINT_COUNT:
            errors.append(f"{case_id}: fixed-parameter point count mismatch")
        if row.get("noise_seed") != args.seed_base + index:
            errors.append(f"{case_id}: fixed-parameter noise seed mismatch")

    if errors:
        raise RuntimeError("fixed-parameter target audit failed:\n- " + "\n- ".join(errors))

    resimulated = simulate_fixedparams_cases(
        corpus, cases, upstream, gsasii_dir, args.seed_base, args.workers
    )
    by_id = {row["case_id"]: row for row in resimulated}
    max_error = 0.0
    for row in output_cases:
        case_id = str(row["case_id"])
        _, observed = load_pattern_with_count(
            output / row["pattern_path"], FIXEDPARAMS_POINT_COUNT, np
        )
        expected = by_id[case_id]["noisy"]
        error = float(np.max(np.abs(observed - expected)))
        max_error = max(max_error, error)
        if error > RESIMULATION_TOLERANCE:
            errors.append(f"{case_id}: fixed-parameter resimulation error {error:.12g}")
    if errors:
        raise RuntimeError("fixed-parameter target audit failed:\n- " + "\n- ".join(errors))
    print(
        f"OK: {args.expected_cases} {FIXEDPARAMS_PROFILE_KEY} targets for "
        f"{source['dataset_id']}; max resimulation error {max_error:.12g}"
    )


def load_pattern_with_count(path: Path, point_count: int, np: Any) -> tuple[Any, Any]:
    values = np.loadtxt(path, delimiter=",", skiprows=1)
    if values.shape != (point_count, 2):
        raise RuntimeError(f"unexpected pattern shape {values.shape}: {path}")
    return values[:, 0], values[:, 1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=("build", "audit", "build-fixedparams", "audit-fixedparams"),
    )
    parser.add_argument("--corpus-root", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--dataset-id")
    parser.add_argument("--case-prefix")
    parser.add_argument("--expected-cases", type=int, default=EXPECTED_CASES)
    parser.add_argument("--support-policy", choices=SUPPORT_POLICIES, default="require-all")
    parser.add_argument("--upstream-root", type=Path, default=DEFAULT_UPSTREAM)
    parser.add_argument("--gsasii-dir", type=Path, default=DEFAULT_GSASII_DIR)
    parser.add_argument("--seed-base", type=int, default=DEFAULT_SEED_BASE)
    parser.add_argument("--workers", type=int, default=1)
    args = parser.parse_args()
    if args.expected_cases < 1:
        parser.error("--expected-cases must be positive")
    if not 1 <= args.workers <= 3:
        parser.error("--workers must be in [1, 3] to bound local CPU use")
    if args.command == "build":
        build(args)
    elif args.command == "audit":
        audit(args)
    elif args.command == "build-fixedparams":
        build_fixedparams(args)
    else:
        audit_fixedparams(args)


if __name__ == "__main__":
    main()
