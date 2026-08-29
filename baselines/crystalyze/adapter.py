# ruff: noqa: UP006, UP017, UP031, UP035, UP045
"""Pinned Modal inference for the Crystalyze pXRD-100 baseline.

The published checkpoint uses a Python 3.8 / PyTorch 1.8.1 / CUDA 10.2
environment.  CUDA 10.2 predates Ampere and newer accelerators, so the default
accelerator here is a T4 (compute capability 7.5), matching the architectures
supported by the published PyTorch binary.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import re
import subprocess
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

try:
    import modal
except ImportError as exc:  # pragma: no cover - optional dependency boundary
    raise RuntimeError("Crystalyze Modal support requires the 'modal' extra") from exc

from verifiable_pxrd.baselines.dataset import (
    load_dataset_binding,
    validate_request_identity,
    validate_target_payload,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BASELINES_ROOT = PROJECT_ROOT / "baselines"
DATASET = load_dataset_binding(PROJECT_ROOT)
CHECKOUT_ROOT = BASELINES_ROOT / ".upstream" / "Crystalyze"
LOCAL_MODEL_ROOT = BASELINES_ROOT / ".runs" / "crystalyze-model" / "model_folder"
LOCAL_TARGET_ROOT = DATASET.target_root("crystalyze")
LOCAL_WORKER = Path(__file__).with_name("worker.py")

REMOTE_ROOT = Path("/opt/crystalyze")
REMOTE_MODEL_ROOT = REMOTE_ROOT / "model_folder"
REMOTE_TARGET_ROOT = REMOTE_ROOT / "targets"
REMOTE_ENV_FILE = REMOTE_ROOT / "env.yml"
REMOTE_WORKER = REMOTE_ROOT / "modal_worker.py"
REMOTE_PYTHON = Path("/opt/conda/envs/crystalyze/bin/python")

APP_NAME = f"verifiable-pxrd-crystalyze-{DATASET.slug}"
CRYSTALYZE_COMMIT = "d265e8b4687fda9586a73f3eb881bb881171b05b"
CHECKPOINT_FILENAME = "epoch=804-step=57154.ckpt"
CHECKPOINT_SHA256 = "ee95964d8ca104cdc9fbb55ce54f9e52d891154d35ee1a47031fe01b0d523ee0"
CHECKPOINT_SIZE = 414_720_000
HPARAMS_SHA256 = "d1053e8bbaa5a0d1dbfe528c28d2750dc29b193f75046028ae06a3ec3051af3f"
DEFAULT_GPU = "T4"
DEFAULT_SAMPLES = 8
DEFAULT_N_STEP_EACH = 100
DEFAULT_STEP_LR = 1e-4
DEFAULT_MIN_SIGMA = 0.0


def _assert_local_inputs() -> None:
    required = [
        CHECKOUT_ROOT / "env.yml",
        CHECKOUT_ROOT / "cdvae" / "pl_modules" / "model.py",
        LOCAL_MODEL_ROOT / CHECKPOINT_FILENAME,
        LOCAL_MODEL_ROOT / "hparams.yaml",
        LOCAL_MODEL_ROOT / "lattice_scaler.pt",
        LOCAL_MODEL_ROOT / "prop_scaler.pt",
        LOCAL_TARGET_ROOT / "manifest.json",
        LOCAL_TARGET_ROOT / "inputs.csv",
        LOCAL_WORKER,
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError("Crystalyze Modal inputs are not staged: " + ", ".join(missing))


if modal.is_local():
    _assert_local_inputs()

image = (
    modal.Image.micromamba(python_version="3.11")
    .add_local_file(CHECKOUT_ROOT / "env.yml", str(REMOTE_ENV_FILE), copy=True)
    .run_commands(
        f"micromamba create --yes --name crystalyze --file {REMOTE_ENV_FILE}"
    )
    .uv_pip_install("pydantic==2.13.4")
    .add_local_dir(
        CHECKOUT_ROOT / "cdvae",
        str(REMOTE_ROOT / "cdvae"),
        copy=True,
        ignore=["**/__pycache__/**", "**/*.pyc"],
    )
    .add_local_dir(LOCAL_MODEL_ROOT, str(REMOTE_MODEL_ROOT), copy=True)
    .add_local_dir(LOCAL_TARGET_ROOT, str(REMOTE_TARGET_ROOT), copy=True)
    .add_local_file(LOCAL_WORKER, str(REMOTE_WORKER), copy=True)
    .env(
        {
            "PROJECT_ROOT": str(REMOTE_ROOT),
            "HYDRA_JOBS": "/tmp/crystalyze-hydra",
            "WABDB_DIR": "/tmp/crystalyze-wandb",
            "PYTHONPATH": str(REMOTE_ROOT),
            **DATASET.environment(),
        }
    )
)

app = modal.App(APP_NAME)


def _invoke_legacy_worker(request: Mapping[str, Any]) -> Tuple[bytes, Dict[str, Any]]:
    """Run the exact Python 3.8 stack beneath Modal's supported Python 3.11 host."""

    with tempfile.TemporaryDirectory(prefix="crystalyze-worker-") as temporary:
        root = Path(temporary)
        archive_path = root / "result.tar.gz"
        summary_path = root / "summary.json"
        completed = subprocess.run(
            [
                str(REMOTE_PYTHON),
                str(REMOTE_WORKER),
                "--request-json",
                json.dumps(dict(request), sort_keys=True),
                "--archive",
                str(archive_path),
                "--summary",
                str(summary_path),
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=85_800,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                "Crystalyze legacy worker failed (exit %d). stdout=%s stderr=%s"
                % (completed.returncode, completed.stdout[-8000:], completed.stderr[-8000:])
            )
        if not archive_path.is_file() or not summary_path.is_file():
            raise RuntimeError("Crystalyze legacy worker did not produce its declared outputs")
        return archive_path.read_bytes(), json.loads(summary_path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            chunk = stream.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def _configure_remote_runtime() -> None:
    import sys

    os.environ.setdefault("PROJECT_ROOT", str(REMOTE_ROOT))
    os.environ.setdefault("HYDRA_JOBS", "/tmp/crystalyze-hydra")
    os.environ.setdefault("WABDB_DIR", "/tmp/crystalyze-wandb")
    if str(REMOTE_ROOT) not in sys.path:
        sys.path.insert(0, str(REMOTE_ROOT))
    Path(os.environ["HYDRA_JOBS"]).mkdir(parents=True, exist_ok=True)
    Path(os.environ["WABDB_DIR"]).mkdir(parents=True, exist_ok=True)


def _portable_load_model() -> Tuple[Any, Any]:
    """Instantiate from portable YAML, then load the published state dictionary."""

    _configure_remote_runtime()
    import hydra
    import torch
    from hydra import initialize_config_dir
    from hydra.experimental import compose

    checkpoint = REMOTE_MODEL_ROOT / CHECKPOINT_FILENAME
    if checkpoint.stat().st_size != CHECKPOINT_SIZE or _sha256(checkpoint) != CHECKPOINT_SHA256:
        raise RuntimeError("Crystalyze checkpoint failed its locked size or SHA-256")
    if _sha256(REMOTE_MODEL_ROOT / "hparams.yaml") != HPARAMS_SHA256:
        raise RuntimeError("Crystalyze hparams failed its locked SHA-256")

    with initialize_config_dir(str(REMOTE_MODEL_ROOT)):
        cfg = compose(config_name="hparams")
        model = hydra.utils.instantiate(
            cfg.model,
            optim=cfg.optim,
            data=cfg.data,
            logging=cfg.logging,
            _recursive_=False,
        )
    payload = torch.load(str(checkpoint), map_location="cpu")
    state_result = model.load_state_dict(payload["state_dict"], strict=False)
    if state_result.missing_keys or state_result.unexpected_keys:
        raise RuntimeError(
            "checkpoint state mismatch: missing=%s unexpected=%s"
            % (state_result.missing_keys, state_result.unexpected_keys)
        )
    model.lattice_scaler = torch.load(
        str(REMOTE_MODEL_ROOT / "lattice_scaler.pt"), map_location="cpu"
    )
    model.scaler = torch.load(str(REMOTE_MODEL_ROOT / "prop_scaler.pt"), map_location="cpu")
    model.eval()
    model.cuda(0)
    return model, cfg


def _load_target_manifest() -> Dict[str, Dict[str, Any]]:
    payload = json.loads((REMOTE_TARGET_ROOT / "manifest.json").read_text(encoding="utf-8"))
    validate_target_payload(payload, DATASET)
    return {str(case["case_id"]): case for case in payload["cases"]}


def _validate_request(payload: Mapping[str, Any]) -> Dict[str, Any]:
    target_payload = json.loads(
        (LOCAL_TARGET_ROOT / "manifest.json").read_text(encoding="utf-8")
    )
    validate_request_identity(payload, target_payload, DATASET)
    case_ids = [str(value) for value in payload.get("case_ids", [])]
    if not case_ids or len(case_ids) != len(set(case_ids)):
        raise ValueError("case_ids must be a non-empty, deduplicated list")
    samples = int(payload.get("samples", DEFAULT_SAMPLES))
    n_step_each = int(payload.get("n_step_each", DEFAULT_N_STEP_EACH))
    if not 1 <= samples <= 32:
        raise ValueError("samples must be in [1, 32]")
    if not 1 <= n_step_each <= 100:
        raise ValueError("n_step_each must be in [1, 100]")
    run_id = str(payload.get("run_id", "crystalyze-run"))
    shard_index = int(payload.get("shard_index", 0))
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", run_id) is None:
        raise ValueError("run_id must be a filesystem-safe identifier")
    if shard_index < 0:
        raise ValueError("shard_index must be non-negative")
    return {
        "case_ids": case_ids,
        "samples": samples,
        "n_step_each": n_step_each,
        "step_lr": float(payload.get("step_lr", DEFAULT_STEP_LR)),
        "min_sigma": float(payload.get("min_sigma", DEFAULT_MIN_SIGMA)),
        "seed": int(payload.get("seed", 42)),
        "run_id": run_id,
        "shard_index": shard_index,
        **DATASET.request_identity(),
    }


def _prepare_inputs(
    case_ids: Sequence[str], samples: int, manifest: Mapping[str, Mapping[str, Any]]
) -> Tuple[Any, Any, List[Dict[str, Any]]]:
    """Reproduce upstream interpolation, normalization, and 15-degree mask."""

    import numpy as np
    import torch
    from pymatgen.core import Element
    from scipy.interpolate import interp1d

    profiles = []
    element_rows = []
    metadata: List[Dict[str, Any]] = []
    for case_id in case_ids:
        if case_id not in manifest:
            raise ValueError("unknown Crystalyze target case: %s" % case_id)
        case = dict(manifest[case_id])
        if not bool(case["model_supported"]):
            raise ValueError("case exceeds the checkpoint's 20-site domain: %s" % case_id)
        pattern_path = REMOTE_TARGET_ROOT / str(case["pattern_path"])
        values = np.loadtxt(str(pattern_path), delimiter=",")
        interpolator = interp1d(
            values[:, 0], values[:, 1], kind="cubic", bounds_error=False, fill_value=0
        )
        intensity = np.asarray(interpolator(np.linspace(5, 90, 8500)), dtype=np.float32)
        maximum = float(np.max(intensity))
        if not np.isfinite(maximum) or maximum <= 0:
            raise RuntimeError("target has a non-positive interpolation maximum: %s" % case_id)
        intensity /= maximum
        intensity[:1000] = 0.0
        profiles.append(intensity)

        atomic_numbers = [int(Element(symbol).Z) for symbol in case["elements"]]
        if any(number > 100 for number in atomic_numbers):
            raise ValueError("Crystalyze supports elements only through fermium: %s" % case_id)
        padded = np.zeros(256, dtype=np.int64)
        padded[: len(atomic_numbers)] = atomic_numbers
        element_rows.append(padded)
        metadata.append(case)

    profile_tensor = torch.tensor(np.stack(profiles), dtype=torch.float32)
    profile_tensor = profile_tensor.repeat_interleave(samples, dim=0).unsqueeze(1).cuda(0)
    element_tensor = torch.tensor(np.stack(element_rows), dtype=torch.long)
    element_tensor = element_tensor.repeat_interleave(samples, dim=0).cuda(0)
    return profile_tensor, element_tensor, metadata


def _seed_everything(seed: int) -> None:
    import random

    import numpy as np
    import torch

    random.seed(seed)
    np.random.seed(seed % (2**32 - 1))
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def _candidate_records(
    output: Mapping[str, Any],
    case_metadata: Sequence[Mapping[str, Any]],
    samples: int,
    destination: Path,
) -> List[Dict[str, Any]]:
    import numpy as np
    from pymatgen.core import Lattice, Structure
    from pymatgen.io.cif import CifWriter

    num_atoms = output["num_atoms"].detach().cpu().numpy().astype(int)
    lengths = output["lengths"].detach().cpu().numpy()
    angles = output["angles"].detach().cpu().numpy()
    frac_coords = output["frac_coords"].detach().cpu().numpy()
    atom_types = output["atom_types"].detach().cpu().numpy().astype(int)
    expected = len(case_metadata) * samples
    if len(num_atoms) != expected:
        raise RuntimeError("model returned %d crystals, expected %d" % (len(num_atoms), expected))

    records: List[Dict[str, Any]] = []
    atom_offset = 0
    for flat_index, site_count in enumerate(num_atoms.tolist()):
        case_index = flat_index // samples
        sample_index = flat_index % samples
        case_id = str(case_metadata[case_index]["case_id"])
        case_root = destination / "candidates" / case_id
        case_root.mkdir(parents=True, exist_ok=True)
        candidate_name = "candidate-%02d" % (sample_index + 1)
        coords = frac_coords[atom_offset : atom_offset + site_count]
        species = atom_types[atom_offset : atom_offset + site_count]
        atom_offset += site_count
        record: Dict[str, Any] = {
            "case_id": case_id,
            "sample_index": sample_index,
            "best_of_1_member": sample_index == 0,
            "predicted_site_count": site_count,
            "predicted_atomic_numbers": species.tolist(),
            "predicted_lengths_angstrom": lengths[flat_index].tolist(),
            "predicted_angles_deg": angles[flat_index].tolist(),
        }
        try:
            finite = bool(
                site_count > 0
                and np.isfinite(coords).all()
                and np.isfinite(lengths[flat_index]).all()
                and np.isfinite(angles[flat_index]).all()
                and np.all(lengths[flat_index] > 0)
                and np.all(angles[flat_index] > 0)
                and np.all(angles[flat_index] < 180)
            )
            if not finite:
                raise ValueError("non-physical or non-finite predicted lattice")
            lattice = Lattice.from_parameters(
                *lengths[flat_index].tolist(), *angles[flat_index].tolist()
            )
            structure = Structure(lattice, species.tolist(), coords, coords_are_cartesian=False)
            cif_path = case_root / (candidate_name + ".cif")
            cif_path.write_text(str(CifWriter(structure, symprec=None)), encoding="utf-8")
            record.update(
                {
                    "status": "generated",
                    "candidate_path": str(cif_path.relative_to(destination)),
                    "candidate_sha256": _sha256(cif_path),
                    "predicted_formula": structure.composition.reduced_formula,
                    "volume_angstrom3": float(structure.volume),
                }
            )
        except Exception as exc:
            error_path = case_root / (candidate_name + ".invalid.json")
            error_path.write_text(
                json.dumps({"error": str(exc), **record}, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            record.update(
                {
                    "status": "invalid",
                    "error": str(exc),
                    "candidate_path": str(error_path.relative_to(destination)),
                    "candidate_sha256": _sha256(error_path),
                }
            )
        records.append(record)
    if atom_offset != len(atom_types):
        raise RuntimeError("model atom tensor did not split cleanly")
    return records


def _run_request(request_payload: Mapping[str, Any]) -> Tuple[Path, Dict[str, Any]]:
    import platform
    import time
    from types import SimpleNamespace

    import torch

    request = _validate_request(request_payload)
    manifest = _load_target_manifest()
    _seed_everything(int(request["seed"]))
    torch.cuda.reset_peak_memory_stats()
    started = time.perf_counter()
    model, cfg = _portable_load_model()
    torch.cuda.synchronize()
    loaded = time.perf_counter()
    profiles, elements, metadata = _prepare_inputs(
        request["case_ids"], int(request["samples"]), manifest
    )
    ld_kwargs = SimpleNamespace(
        n_step_each=int(request["n_step_each"]),
        step_lr=float(request["step_lr"]),
        min_sigma=float(request["min_sigma"]),
        save_traj=False,
        disable_bar=True,
    )
    with torch.no_grad():
        _, _, latent = model.encode(
            None,
            None,
            None,
            elements,
            None,
            testing=False,
            pv_xrd=profiles,
            multi_hot_encode=None,
        )
        generated = model.langevin_dynamics(
            latent,
            ld_kwargs,
            gt_num_atoms=None,
            gt_atom_types=None,
            gt_elements_input=elements,
        )
    torch.cuda.synchronize()
    generated_at = time.perf_counter()

    run_id = str(request["run_id"])
    shard_name = "shard-%03d" % int(request["shard_index"])
    temporary_root = Path(tempfile.mkdtemp(prefix="crystalyze-output-"))
    destination = temporary_root / run_id / shard_name
    destination.mkdir(parents=True, exist_ok=False)
    records = _candidate_records(
        generated, metadata, int(request["samples"]), destination
    )
    completed_at = time.perf_counter()
    result = {
        "schema_version": "1.0.0",
        "framework": "Crystalyze",
        "framework_commit": CRYSTALYZE_COMMIT,
        "checkpoint_sha256": CHECKPOINT_SHA256,
        **DATASET.request_identity(),
        "run_id": run_id,
        "shard_index": int(request["shard_index"]),
        "case_ids": request["case_ids"],
        "case_count": len(request["case_ids"]),
        "samples_per_case": int(request["samples"]),
        "candidate_count": len(records),
        "generated_candidate_count": sum(r["status"] == "generated" for r in records),
        "invalid_candidate_count": sum(r["status"] == "invalid" for r in records),
        "inference": {
            "force_num_atoms": False,
            "force_atom_types": False,
            "composition_constraint": "allowed_elements_only",
            "n_step_each": int(request["n_step_each"]),
            "noise_levels": int(cfg.model.num_noise_level),
            "step_lr": float(request["step_lr"]),
            "min_sigma": float(request["min_sigma"]),
            "seed": int(request["seed"]),
        },
        "preprocessing": {
            "upstream_interpolation": "cubic to np.linspace(5, 90, 8500)",
            "normalization": "divide by interpolated maximum",
            "masked_leading_bins": 1000,
        },
        "runtime": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "cuda_runtime": str(torch.version.cuda),
            "device_name": torch.cuda.get_device_name(0),
            "device_capability": list(torch.cuda.get_device_capability(0)),
            "model_load_seconds": loaded - started,
            "generation_seconds": generated_at - loaded,
            "serialization_seconds": completed_at - generated_at,
            "total_seconds": completed_at - started,
            "peak_cuda_memory_bytes": int(torch.cuda.max_memory_allocated()),
        },
        "candidates": records,
    }
    (destination / "request.json").write_text(
        json.dumps(request, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (destination / "results.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return destination, result


def _archive_directory(destination: Path) -> bytes:
    payload = io.BytesIO()
    with tarfile.open(fileobj=payload, mode="w:gz") as archive:
        archive.add(destination, arcname="/".join(destination.parts[-2:]))
    return payload.getvalue()


@app.function(image=image, gpu=DEFAULT_GPU, cpu=4, memory=32768, timeout=1800)
def crystalyze_doctor_remote() -> Dict[str, Any]:
    """Load the checkpoint and run one full decoder step on the published stack."""

    manifest = json.loads((REMOTE_TARGET_ROOT / "manifest.json").read_text(encoding="utf-8"))
    validate_target_payload(manifest, DATASET)
    request = {
        "case_ids": [str(manifest["cases"][0]["case_id"])],
        "samples": 1,
        "n_step_each": 1,
        "step_lr": DEFAULT_STEP_LR,
        "min_sigma": 9.99,
        "seed": 42,
        "run_id": "doctor",
        "shard_index": 0,
        **DATASET.request_identity(),
    }
    _, result = _invoke_legacy_worker(request)
    return {
        "status": "OK",
        "checkpoint_sha256": CHECKPOINT_SHA256,
        "device_name": result["runtime"]["device_name"],
        "device_capability": result["runtime"]["device_capability"],
        "cuda_runtime": result["runtime"]["cuda_runtime"],
        "torch": result["runtime"]["torch"],
        "python": result["runtime"]["python"],
        "peak_cuda_memory_bytes": result["runtime"]["peak_cuda_memory_bytes"],
    }


@app.function(
    image=image,
    gpu=DEFAULT_GPU,
    cpu=2,
    memory=8192,
    timeout=86_400,
    max_containers=4,
)
def crystalyze_generate_remote(request_json: str) -> bytes:
    """Generate one durable shard and return its complete CIF archive."""

    payload, _ = _invoke_legacy_worker(json.loads(request_json))
    return payload


def make_request(
    case_ids: Sequence[str],
    *,
    run_id: str,
    shard_index: int,
    samples: int = DEFAULT_SAMPLES,
    seed: int = 42,
    n_step_each: int = DEFAULT_N_STEP_EACH,
    step_lr: float = DEFAULT_STEP_LR,
    min_sigma: float = DEFAULT_MIN_SIGMA,
) -> Dict[str, Any]:
    """Build a JSON-safe, paper-faithful inference request."""

    return _validate_request(
        {
            "case_ids": list(case_ids),
            "samples": samples,
            "n_step_each": n_step_each,
            "step_lr": step_lr,
            "min_sigma": min_sigma,
            "seed": seed,
            "run_id": run_id,
            "shard_index": shard_index,
            **DATASET.request_identity(),
        }
    )


def supported_case_ids() -> List[str]:
    """Return the 100 model-eligible cases in committed manifest order."""

    payload = json.loads((LOCAL_TARGET_ROOT / "manifest.json").read_text(encoding="utf-8"))
    return [str(case["case_id"]) for case in payload["cases"] if bool(case["model_supported"])]


def shard_cases(case_ids: Sequence[str], shard_size: int) -> List[List[str]]:
    if shard_size < 1:
        raise ValueError("shard_size must be positive")
    return [
        list(case_ids[index : index + shard_size])
        for index in range(0, len(case_ids), shard_size)
    ]


def make_requests(
    *, run_id: str, shard_size: int = 10, seed_base: int = 20260718
) -> List[Dict[str, Any]]:
    """Build deterministic production requests in manifest order."""

    shards = shard_cases(supported_case_ids(), shard_size)
    return [
        make_request(
            case_ids,
            run_id=run_id,
            shard_index=shard_index,
            samples=DEFAULT_SAMPLES,
            seed=seed_base + shard_index,
        )
        for shard_index, case_ids in enumerate(shards)
    ]


def modal_crystalyze_doctor(*, gpu_type: str = DEFAULT_GPU) -> Dict[str, Any]:
    """Run the GPU preflight using the user's existing Modal authentication."""

    with modal.enable_output(), app.run():
        configured = crystalyze_doctor_remote.with_options(gpu=gpu_type, timeout=1800)
        return dict(configured.remote())


def modal_crystalyze_run(
    request: Mapping[str, Any], output_root: Path, *, gpu_type: str = DEFAULT_GPU
) -> Tuple[Path, Dict[str, Any]]:
    """Run one synchronous shard and safely materialize its CIFs."""

    request_json = json.dumps(dict(request), sort_keys=True)
    with modal.enable_output(), app.run():
        configured = crystalyze_generate_remote.with_options(gpu=gpu_type, timeout=86_400)
        payload = configured.remote(request_json)
    destination = _materialize_archive(payload, output_root)
    result = json.loads((destination / "results.json").read_text(encoding="utf-8"))
    return destination, result


def modal_crystalyze_submit(
    requests: Sequence[Mapping[str, Any]],
    handle_path: Path,
    *,
    gpu_type: str = DEFAULT_GPU,
    max_containers: int = 4,
    completed_shards: Optional[Sequence[int]] = None,
) -> Path:
    """Submit durable generation shards and atomically save every call ID."""

    if not requests:
        raise ValueError("at least one generation request is required")
    calls: List[Dict[str, Any]] = []
    with modal.enable_output(), app.run(detach=True):
        configured = crystalyze_generate_remote.with_options(
            gpu=gpu_type, max_containers=max_containers, timeout=86_400
        )
        for request in requests:
            payload = dict(request)
            call = configured.spawn(json.dumps(payload, sort_keys=True))
            calls.append(
                {
                    "shard_index": int(payload["shard_index"]),
                    "case_ids": list(payload["case_ids"]),
                    "call_id": call.object_id,
                }
            )
    handle = {
        "schema_version": "1.0.0",
        "app_name": APP_NAME,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "gpu_type": gpu_type,
        "max_containers": max_containers,
        "run_id": str(requests[0]["run_id"]),
        **DATASET.request_identity(),
        "samples_per_case": int(requests[0]["samples"]),
        "completed_shards": list(completed_shards or []),
        "calls": calls,
    }
    _write_atomic(handle_path, json.dumps(handle, indent=2, sort_keys=True) + "\n")
    return handle_path


def modal_crystalyze_collect(
    handle_path: Path, output_root: Path, *, timeout: float = 0
) -> Tuple[Path, Dict[str, Any]]:
    """Collect all finished calls and update the local durable handle."""

    handle = json.loads(handle_path.read_text(encoding="utf-8"))
    completed = {int(value) for value in handle.get("completed_shards", [])}
    failures = []
    for call in handle["calls"]:
        shard_index = int(call["shard_index"])
        if shard_index in completed:
            continue
        try:
            payload = modal.FunctionCall.from_id(str(call["call_id"])).get(timeout=timeout)
            _materialize_archive(payload, output_root)
            completed.add(shard_index)
        except TimeoutError:
            continue
        except Exception as exc:  # preserve other completed shards and record evidence
            failures.append({"shard_index": shard_index, "error": repr(exc)})
    handle["completed_shards"] = sorted(completed)
    handle["failures"] = failures
    handle["updated_at"] = datetime.now(timezone.utc).isoformat()
    _write_atomic(handle_path, json.dumps(handle, indent=2, sort_keys=True) + "\n")
    return output_root / str(handle["run_id"]), handle


def _write_atomic(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".partial")
    with temporary.open("w", encoding="utf-8") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def _materialize_archive(payload: bytes, output_root: Path) -> Path:
    """Safely extract exactly one run/shard archive."""

    output_root.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as archive:
        members = archive.getmembers()
        roots = {tuple(Path(member.name).parts[:2]) for member in members if member.name}
        if len(roots) != 1:
            raise RuntimeError("Crystalyze result archive has an invalid root")
        run_name, shard_name = next(iter(roots))
        if not run_name or not shard_name:
            raise RuntimeError("Crystalyze result archive has an empty root")
        output_resolved = output_root.resolve()
        for member in members:
            if member.issym() or member.islnk():
                raise RuntimeError("Crystalyze result archive contains a link")
            target = (output_root / member.name).resolve()
            if target != output_resolved and output_resolved not in target.parents:
                raise RuntimeError("Crystalyze result archive contains an unsafe path")
        archive.extractall(output_root, members=members)
    return output_root / run_name / shard_name


def summarize_run(run_root: Path) -> Dict[str, Any]:
    """Aggregate completed shard manifests without performing scientific scoring."""

    results = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(run_root.glob("shard-*/results.json"))
    ]
    return {
        "run_id": run_root.name,
        "shard_count": len(results),
        "case_count": sum(int(result["case_count"]) for result in results),
        "candidate_count": sum(int(result["candidate_count"]) for result in results),
        "generated_candidate_count": sum(
            int(result["generated_candidate_count"]) for result in results
        ),
        "invalid_candidate_count": sum(
            int(result["invalid_candidate_count"]) for result in results
        ),
        "generation_gpu_seconds": sum(
            float(result["runtime"]["generation_seconds"]) for result in results
        ),
    }


# Common runner interface shared with the other three framework modules.
def modal_doctor(*, gpu_type: str = DEFAULT_GPU) -> Dict[str, Any]:
    return modal_crystalyze_doctor(gpu_type=gpu_type)


def modal_run(
    request: Mapping[str, Any], output_root: Path, *, gpu_type: str = DEFAULT_GPU
) -> Path:
    destination, _ = modal_crystalyze_run(request, output_root, gpu_type=gpu_type)
    return destination


def modal_submit(
    requests: Sequence[Mapping[str, Any]],
    handle_path: Path,
    *,
    gpu_type: str = DEFAULT_GPU,
    max_containers: int = 4,
) -> Path:
    return modal_crystalyze_submit(
        requests,
        handle_path,
        gpu_type=gpu_type,
        max_containers=max_containers,
    )


def modal_collect(
    handle_path: Path, output_root: Path, *, timeout: float = 0
) -> Dict[str, Any]:
    _, handle = modal_crystalyze_collect(handle_path, output_root, timeout=timeout)
    return handle
