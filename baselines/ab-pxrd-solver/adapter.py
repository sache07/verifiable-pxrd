"""Durable Modal execution for the pinned Ab-PXRD-Solver baseline."""

from __future__ import annotations

import csv
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import modal

from verifiable_pxrd.baselines.dataset import (
    load_dataset_binding,
    validate_request_identity,
    validate_target_payload,
)
from verifiable_pxrd.baselines.modal import (
    archive_directory,
    collect_handle,
    materialize_archive,
    sha256_file,
    validate_run_id,
    write_atomic,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BASELINES_ROOT = PROJECT_ROOT / "baselines"
DATASET = load_dataset_binding(PROJECT_ROOT)
LOCAL_SOURCE = BASELINES_ROOT / ".upstream" / "Ab-PXRD-Solver"
LOCAL_TARGETS = DATASET.target_root("ab-pxrd-solver")
LOCAL_LOCK = Path(__file__).with_name("artifacts.lock.json")
LOCAL_MACE_MODEL = (
    BASELINES_ROOT
    / ".runs"
    / "cache"
    / "ab-pxrd-solver"
    / "mace"
    / "20231210mace128L0_energy_epoch249model"
)
LOCAL_GSASII_BIN = (
    BASELINES_ROOT
    / ".runs"
    / "envs"
    / "pxrdgen-gsas2full"
    / "GSAS-II"
    / "GSASII-bin"
    / "linux_64_p3.11_n1.26"
)

REMOTE_ROOT = Path("/opt/ab-pxrd-solver")
REMOTE_SOURCE = REMOTE_ROOT / "source"
REMOTE_TARGETS = REMOTE_ROOT / "targets"
REMOTE_LOCK = REMOTE_ROOT / "artifacts.lock.json"
REMOTE_CACHE = REMOTE_ROOT / "cache"
REMOTE_MACE_MODEL = REMOTE_CACHE / "mace" / LOCAL_MACE_MODEL.name

APP_NAME = f"verifiable-pxrd-ab-pxrd-solver-{DATASET.slug}"
SOURCE_COMMIT = "0d67964dfcbd2e2fa09e79bbbac2f5d020a121e9"
MACE_MODEL_SHA256 = "2ddb079cee0e131eaaf6912ba581b394551ead283e95c99cfe78c605d10b5736"
GSASII_COMMIT = "1a0aeec6c61b54f68e6812704730a471187ac393"
REMOTE_GSASII_CHECKOUT = Path("/opt/gsas-ii")
REMOTE_GSASII_PATH = REMOTE_GSASII_CHECKOUT / "GSASII"
REMOTE_GSASII_BIN = (
    REMOTE_GSASII_CHECKOUT / "GSASII-bin" / LOCAL_GSASII_BIN.name
)
GSASII_REPOSITORY = "https://github.com/AdvancedPhotonSource/GSAS-II.git"
GSASII_PYSPG_SHA256 = "546be345775bcce0250e9fb714bad15a4995ca2f9764ed9519e3edf5816facfa"
GSASII_PYPOWDER_SHA256 = "c1cc9be96060a397baadea8a9536b69c8d4ada8035a7d3fda8e6d09b4a41efa4"
DEFAULT_GPU = "L4"
DEFAULT_SAMPLES = 1
DEFAULT_SHARD_SIZE = 1
DEFAULT_CASE_TIMEOUT = 82_800


def _assert_local_inputs() -> None:
    required = [
        LOCAL_SOURCE / "PXRD_solve.py",
        LOCAL_SOURCE / "pxrd_app" / "constants.py",
        LOCAL_SOURCE / "pxrd_app" / "tools" / "models" / "peaks" / "best_model.pth",
        LOCAL_SOURCE / "pxrd_app" / "tools" / "models" / "density" / "checkpoint-r0.pth.tar",
        LOCAL_TARGETS / "manifest.json",
        LOCAL_TARGETS / "parameters.json",
        LOCAL_LOCK,
        LOCAL_MACE_MODEL,
        LOCAL_GSASII_BIN / "pyspg.cpython-311-x86_64-linux-gnu.so",
        LOCAL_GSASII_BIN / "pypowder.cpython-311-x86_64-linux-gnu.so",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError("Ab-PXRD-Solver Modal inputs are not staged: " + ", ".join(missing))
    if sha256_file(LOCAL_MACE_MODEL) != MACE_MODEL_SHA256:
        raise RuntimeError("local MACE-MP small artifact digest mismatch")
    if sha256_file(required[-2]) != GSASII_PYSPG_SHA256:
        raise RuntimeError("local GSAS-II pyspg binary digest mismatch")
    if sha256_file(required[-1]) != GSASII_PYPOWDER_SHA256:
        raise RuntimeError("local GSAS-II pypowder binary digest mismatch")


if modal.is_local():
    _assert_local_inputs()

image = (
    modal.Image.from_registry("pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime")
    .apt_install("git", "build-essential", "gfortran", "libgfortran5")
    .pip_install(
        "numpy==1.26.4",
        "pandas==2.2.3",
        "scipy==1.13.1",
        "matplotlib==3.9.2",
        "tqdm==4.67.1",
        "scikit-learn==1.5.2",
        "pymatgen==2025.5.28",
        "pyxtal==1.1.4",
        "ase==3.25.0",
        "monty==2025.3.3",
        "spglib==2.6.0",
        "wandb==0.19.11",
        "tensorboard==2.19.0",
        "mace-torch==0.3.14",
    )
    # GSAS-II's packaging metadata at this revision references a file absent from
    # the repository. Use its supported source-tree import path, as the validated
    # local runtime does, while retaining an exact commit pin.
    .run_commands(
        f"git clone --filter=blob:none {GSASII_REPOSITORY} {REMOTE_GSASII_CHECKOUT}",
        f"git -C {REMOTE_GSASII_CHECKOUT} checkout --detach {GSASII_COMMIT}",
        f"test -f {REMOTE_GSASII_PATH / 'GSASIIscriptable.py'}",
    )
    .add_local_dir(
        LOCAL_SOURCE,
        str(REMOTE_SOURCE),
        copy=True,
        ignore=[
            ".git/**",
            "GSAS_PXRD/**",
            "Examples/**",
            "Figs/**",
            "**/__pycache__/**",
            "**/*.pyc",
        ],
    )
    .add_local_dir(LOCAL_GSASII_BIN, str(REMOTE_GSASII_BIN), copy=True)
    .add_local_dir(LOCAL_TARGETS, str(REMOTE_TARGETS), copy=True)
    .add_local_file(LOCAL_LOCK, str(REMOTE_LOCK), copy=True)
    .add_local_file(LOCAL_MACE_MODEL, str(REMOTE_MACE_MODEL), copy=True)
    .env(
        {
            "PYTHONPATH": str(REMOTE_SOURCE),
            "GSASII_PATH": str(REMOTE_GSASII_PATH),
            "XDG_CACHE_HOME": str(REMOTE_CACHE),
            "OMP_NUM_THREADS": "1",
            "OPENBLAS_NUM_THREADS": "1",
            "MKL_NUM_THREADS": "1",
            "NUMEXPR_NUM_THREADS": "1",
            "PXRD_SILENCE_MACE": "1",
            **DATASET.environment(),
        }
    )
)

app = modal.App(APP_NAME)


def _target_payload() -> dict[str, Any]:
    payload = json.loads((REMOTE_TARGETS / "manifest.json").read_text(encoding="utf-8"))
    validate_target_payload(payload, DATASET)
    return payload


def _read_summary(path: Path) -> dict[str, str] | None:
    if not path.is_file() or path.stat().st_size == 0:
        return None
    with path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    return rows[-1] if rows else None


def _copy_upstream_evidence(case_output: Path, evidence: Path) -> list[Path]:
    evidence.mkdir(parents=True, exist_ok=True)
    retained: list[Path] = []
    for source in sorted((case_output / "cifs").glob("*.cif")):
        destination = evidence / "cifs" / source.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        retained.append(destination)
    for source in sorted((case_output / "logs").glob("*")):
        if not source.is_file():
            continue
        destination = evidence / "logs" / source.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    summary = case_output / "summary.csv"
    if summary.is_file():
        shutil.copy2(summary, evidence / "summary.csv")
    return retained


def _select_candidate(cifs: list[Path], summary: dict[str, str] | None) -> Path | None:
    if not cifs:
        return None
    if summary:
        spg = str(summary.get("SPG") or "").strip()
        if spg:
            matching = [path for path in cifs if path.stem.endswith(f"_{spg}")]
            if matching:
                return matching[-1]
    return cifs[-1]


def _run_request(request: dict[str, Any]) -> Path:
    run_id = validate_run_id(str(request["run_id"]))
    shard_index = int(request["shard_index"])
    case_ids = [str(value) for value in request["case_ids"]]
    if not case_ids or len(case_ids) != len(set(case_ids)):
        raise ValueError("case_ids must be a non-empty deduplicated list")
    if int(request.get("samples", DEFAULT_SAMPLES)) != 1:
        raise ValueError("Ab-PXRD-Solver is deterministic and supports one selected output")
    case_timeout = int(request.get("case_timeout_seconds", DEFAULT_CASE_TIMEOUT))
    if not 60 <= case_timeout <= DEFAULT_CASE_TIMEOUT:
        raise ValueError(f"case_timeout_seconds must be in [60, {DEFAULT_CASE_TIMEOUT}]")
    seed_base = int(request["seed_base"])

    payload = _target_payload()
    validate_request_identity(request, payload, DATASET)
    ordered = list(payload["cases"])
    targets = {str(case["case_id"]): case for case in ordered}
    order = {str(case["case_id"]): index for index, case in enumerate(ordered)}
    unknown = sorted(set(case_ids) - set(targets))
    if unknown:
        raise ValueError(f"unknown Ab-PXRD-Solver cases: {unknown}")
    if sha256_file(REMOTE_MACE_MODEL) != MACE_MODEL_SHA256:
        raise RuntimeError("remote MACE-MP small artifact digest mismatch")

    temporary = Path(tempfile.mkdtemp(prefix="ab-pxrd-output-"))
    destination = temporary / run_id / f"shard-{shard_index:03d}"
    destination.mkdir(parents=True)
    work_root = temporary / "work"
    records: list[dict[str, Any]] = []
    started = time.perf_counter()

    for case_id in case_ids:
        case = targets[case_id]
        case_seed = seed_base + order[case_id]
        case_output = work_root / case_id / "Results"
        case_output.mkdir(parents=True)
        stdout_path = destination / "logs" / f"{case_id}.stdout.txt"
        stderr_path = destination / "logs" / f"{case_id}.stderr.txt"
        stdout_path.parent.mkdir(parents=True, exist_ok=True)
        command = [
            sys.executable,
            str(REMOTE_SOURCE / "PXRD_solve.py"),
            "--input",
            str(REMOTE_TARGETS / str(case["pattern_path"])),
            "--formula",
            str(case["formula"]),
            "--infer-spg",
            "--output",
            str(case_output),
            "--workers",
            "1",
            "--max-vol",
            "1500",
            "--max-wp",
            "18",
            "--max-dof",
            "25",
            "--max-z",
            "24",
            "--qrs",
            "halton",
        ]
        environment = dict(os.environ)
        environment["PXRD_SEED_BASE"] = str(case_seed)
        case_started = time.perf_counter()
        timed_out = False
        try:
            completed = subprocess.run(
                command,
                cwd=REMOTE_SOURCE,
                env=environment,
                check=False,
                capture_output=True,
                text=True,
                timeout=case_timeout,
            )
            returncode = completed.returncode
            stdout = completed.stdout
            stderr = completed.stderr
        except subprocess.TimeoutExpired as exc:
            timed_out = True
            returncode = 124
            stdout = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
            stderr = exc.stderr.decode() if isinstance(exc.stderr, bytes) else (exc.stderr or "")
            stderr += f"\nTimed out after {case_timeout} seconds.\n"
        case_seconds = time.perf_counter() - case_started
        stdout_path.write_text(stdout, encoding="utf-8")
        stderr_path.write_text(stderr, encoding="utf-8")
        evidence = destination / "upstream" / case_id
        retained_cifs = _copy_upstream_evidence(case_output, evidence)
        summary = _read_summary(case_output / "summary.csv")
        selected = _select_candidate(retained_cifs, summary)
        record: dict[str, Any] = {
            "case_id": case_id,
            "sample_index": 0,
            "seed": case_seed,
            "input_formula": str(case["formula"]),
            "input_mode": "reduced_formula_and_pxrd_infer_spacegroup",
            "command": command,
            "returncode": returncode,
            "timed_out": timed_out,
            "runtime_seconds": case_seconds,
            "solver_summary": summary,
            "raw_candidate_count": len(retained_cifs),
            "stdout_path": str(stdout_path.relative_to(destination)),
            "stdout_sha256": sha256_file(stdout_path),
            "stderr_path": str(stderr_path.relative_to(destination)),
            "stderr_sha256": sha256_file(stderr_path),
        }
        if selected is not None:
            normalized = destination / "candidates" / case_id / "candidate-01.cif"
            normalized.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(selected, normalized)
            record.update(
                {
                    "status": "generated",
                    "candidate_path": str(normalized.relative_to(destination)),
                    "candidate_sha256": sha256_file(normalized),
                    "selected_upstream_path": str(selected.relative_to(destination)),
                    "selected_upstream_sha256": sha256_file(selected),
                }
            )
        else:
            error_path = destination / "candidates" / case_id / "candidate-01.invalid.json"
            error_path.parent.mkdir(parents=True, exist_ok=True)
            error = {
                "returncode": returncode,
                "timed_out": timed_out,
                "solver_status": summary.get("Status") if summary else None,
                "message": "Ab-PXRD-Solver produced no selected CIF",
            }
            error_path.write_text(json.dumps(error, indent=2) + "\n", encoding="utf-8")
            record.update(
                {
                    "status": "invalid",
                    "candidate_path": str(error_path.relative_to(destination)),
                    "candidate_sha256": sha256_file(error_path),
                    "error": error["message"],
                }
            )
        records.append(record)

    completed_at = time.perf_counter()
    result = {
        "schema_version": "1.0.0",
        "framework": "Ab-PXRD-Solver",
        "source_commit": SOURCE_COMMIT,
        "mace_model_sha256": MACE_MODEL_SHA256,
        "gsasii_commit": GSASII_COMMIT,
        **DATASET.request_identity(),
        "run_id": run_id,
        "shard_index": shard_index,
        "case_ids": case_ids,
        "case_count": len(case_ids),
        "samples_per_case": 1,
        "candidate_count": len(records),
        "generated_candidate_count": sum(row["status"] == "generated" for row in records),
        "invalid_candidate_count": sum(row["status"] == "invalid" for row in records),
        "inference": {
            "input_mode": "reduced_formula_and_pxrd_infer_spacegroup",
            "space_group_supplied": False,
            "qrs": "halton",
            "seed_base": seed_base,
            "case_timeout_seconds": case_timeout,
        },
        "runtime": {
            "python": platform.python_version(),
            "total_seconds": completed_at - started,
        },
        "candidates": records,
    }
    (destination / "request.json").write_text(
        json.dumps(request, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (destination / "results.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return destination


@app.function(image=image, gpu=DEFAULT_GPU, cpu=4, memory=16384, timeout=1800)
def ab_pxrd_solver_doctor_remote() -> dict[str, Any]:
    import numpy as np
    import torch
    from ase import Atoms
    from mace.calculators import mace_mp

    payload = _target_payload()
    if len(payload["cases"]) != 100 or payload["supported_case_count"] != 100:
        raise RuntimeError("incomplete Ab-PXRD-Solver targets in Modal image")
    if sha256_file(REMOTE_MACE_MODEL) != MACE_MODEL_SHA256:
        raise RuntimeError("MACE model digest mismatch")
    if sha256_file(REMOTE_GSASII_BIN / "pyspg.cpython-311-x86_64-linux-gnu.so") != (
        GSASII_PYSPG_SHA256
    ):
        raise RuntimeError("GSAS-II pyspg binary digest mismatch")
    if sha256_file(
        REMOTE_GSASII_BIN / "pypowder.cpython-311-x86_64-linux-gnu.so"
    ) != GSASII_PYPOWDER_SHA256:
        raise RuntimeError("GSAS-II pypowder binary digest mismatch")
    sys.path.insert(0, str(REMOTE_SOURCE))
    from pxrd_app.tools.density import predict_density_ensemble
    from pxrd_app.tools.gsas import check_gsas_available
    from pxrd_app.tools.peak_prediction import _get_peak_model
    from pxrd_app.tools.solver import SmartCellSolver

    gsas_ok, gsas_message = check_gsas_available()
    if not gsas_ok:
        raise RuntimeError(gsas_message)
    model, window_size, device = _get_peak_model()
    with torch.inference_mode():
        logits = model(torch.zeros((1, window_size), dtype=torch.float32, device=device))
    density = predict_density_ensemble(str(payload["cases"][0]["formula"]), sigma=2.5)
    mace = mace_mp(model="small", device="cuda", default_dtype="float32")
    atoms = Atoms(
        "Si2",
        positions=[[0.0, 0.0, 0.0], [1.3575, 1.3575, 1.3575]],
        cell=[5.43, 5.43, 5.43],
        pbc=True,
    )
    atoms.calc = mace
    energy = float(atoms.get_potential_energy())
    if not np.isfinite(energy):
        raise RuntimeError("MACE smoke-test energy is non-finite")
    return {
        "status": "OK",
        "source_commit": SOURCE_COMMIT,
        "mace_model_sha256": MACE_MODEL_SHA256,
        "gsas": gsas_message,
        "torch": torch.__version__,
        "device": torch.cuda.get_device_name(0),
        "peak_logits_shape": list(logits.shape),
        "smart_cell_solver_import": SmartCellSolver.__name__,
        "density_bounds_finite": bool(
            np.isfinite(float(density["min"])) and np.isfinite(float(density["max"]))
        ),
        "mace_smoke_energy_ev": energy,
        "target_case_count": len(payload["cases"]),
    }


@app.function(
    image=image,
    gpu=DEFAULT_GPU,
    cpu=8,
    memory=32768,
    timeout=86_400,
    max_containers=10,
)
def ab_pxrd_solver_generate_remote(request_json: str) -> bytes:
    return archive_directory(_run_request(json.loads(request_json)))


def case_ids() -> list[str]:
    payload = json.loads((LOCAL_TARGETS / "manifest.json").read_text(encoding="utf-8"))
    return [str(case["case_id"]) for case in payload["cases"]]


def make_requests(
    *, run_id: str, shard_size: int = DEFAULT_SHARD_SIZE, seed_base: int = 20260721
) -> list[dict[str, Any]]:
    if not 1 <= shard_size <= 2:
        raise ValueError("Ab-PXRD-Solver shard_size must be 1 or 2")
    ids = case_ids()
    return [
        {
            "run_id": validate_run_id(run_id),
            "shard_index": shard_index,
            "case_ids": ids[start : start + shard_size],
            "seed_base": seed_base,
            "samples": 1,
            "case_timeout_seconds": DEFAULT_CASE_TIMEOUT,
            **DATASET.request_identity(),
        }
        for shard_index, start in enumerate(range(0, len(ids), shard_size))
    ]


def make_preflight_request(*, run_id: str, cpu_count: int | None = None) -> dict[str, Any]:
    """Select the smallest supported primitive cell for a bounded end-to-end smoke run."""

    del cpu_count
    source = json.loads((DATASET.corpus_root / "manifest.json").read_text(encoding="utf-8"))
    supported = set(case_ids())
    eligible = [case for case in source["cases"] if str(case["case_id"]) in supported]
    if not eligible:
        raise RuntimeError("no supported Ab-PXRD-Solver case is available for preflight")
    selected = min(
        eligible,
        key=lambda case: (int(case.get("primitive_site_count", 10**9)), str(case["case_id"])),
    )
    case_id = str(selected["case_id"])
    return {
        "run_id": validate_run_id(run_id),
        "shard_index": 0,
        "case_ids": [case_id],
        "seed_base": 20260721,
        "samples": 1,
        "case_timeout_seconds": DEFAULT_CASE_TIMEOUT,
        **DATASET.request_identity(),
    }


def modal_doctor(*, gpu_type: str = DEFAULT_GPU) -> dict[str, Any]:
    with modal.enable_output(), app.run():
        return dict(ab_pxrd_solver_doctor_remote.with_options(gpu=gpu_type).remote())


def modal_run(request: dict[str, Any], output_root: Path, *, gpu_type: str = DEFAULT_GPU) -> Path:
    payload: bytes | None = None
    with modal.enable_output(), app.run():
        payload = ab_pxrd_solver_generate_remote.with_options(gpu=gpu_type).remote(
            json.dumps(request, sort_keys=True)
        )
    if payload is None:
        raise RuntimeError("Modal preflight ended without returning an artifact archive")
    return materialize_archive(payload, output_root)


def modal_submit(
    requests: list[dict[str, Any]],
    handle_path: Path,
    *,
    gpu_type: str = DEFAULT_GPU,
    max_containers: int = 10,
) -> Path:
    calls: list[dict[str, Any]] = []
    with modal.enable_output(), app.run(detach=True):
        configured = ab_pxrd_solver_generate_remote.with_options(
            gpu=gpu_type,
            max_containers=max_containers,
            timeout=86_400,
        )
        for request in requests:
            call = configured.spawn(json.dumps(request, sort_keys=True))
            calls.append(
                {
                    "shard_index": request["shard_index"],
                    "case_ids": request["case_ids"],
                    "call_id": call.object_id,
                }
            )
    handle = {
        "schema_version": "1.0.0",
        "framework": "Ab-PXRD-Solver",
        "app_name": APP_NAME,
        "created_at": datetime.now(UTC).isoformat(),
        "gpu_type": gpu_type,
        "max_containers": max_containers,
        "run_id": requests[0]["run_id"],
        **DATASET.request_identity(),
        "completed_shards": [],
        "calls": calls,
    }
    write_atomic(handle_path, json.dumps(handle, indent=2, sort_keys=True) + "\n")
    return handle_path


def modal_collect(handle_path: Path, output_root: Path, *, timeout: float = 0) -> dict[str, Any]:
    return collect_handle(handle_path, output_root, timeout=timeout)
