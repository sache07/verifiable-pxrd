"""Durable Modal inference for the released RealPXRD-Solver generators."""

from __future__ import annotations

import json
import platform
import random
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import modal
from core import (
    DEFAULT_INPUT_MODE,
    INPUT_MODES,
    LATTICE_CONDITIONED_ORACLE,
    case_input,
    load_model_peaks,
    model_directory,
    output_structure,
)

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
LOCAL_SOURCE = BASELINES_ROOT / ".upstream" / "RealPXRD-Solver"
LOCAL_MODEL_ROOT = BASELINES_ROOT / ".runs" / "realpxrd-solver-model"
LOCAL_TARGETS = DATASET.target_root("realpxrd-solver")

REMOTE_ROOT = Path("/opt/realpxrd-solver")
REMOTE_SOURCE = REMOTE_ROOT / "source"
REMOTE_MODEL_ROOT = REMOTE_ROOT / "model"
REMOTE_TARGETS = REMOTE_ROOT / "targets"

APP_NAME = f"verifiable-pxrd-realpxrd-solver-{DATASET.slug}"
SOURCE_COMMIT = "5e7e60176e1875071a12fb4583a1f0112bc3bcad"
CHECKPOINT_SHA256 = {
    "pxrd-all": "804eca827d9135256df04a7629bbbc224ba1a79ad439279451537f35ba62dd71",
    "pxrd-all-L": "5ae34a5e36c71fca7fb1e88cbc30b9fac22424d4695f93e052b42143f0e5a376",
}
DEFAULT_GPU = "L4"
DEFAULT_SHARD_SIZE = 10
DEFAULT_SAMPLES = 20
MAX_SAMPLES = 100
DEFAULT_TIMESTEPS = 200
DEFAULT_STEP_LR = 5.0


def _assert_local_inputs() -> None:
    required = [
        LOCAL_SOURCE / "app" / "model" / "flow.py",
        LOCAL_TARGETS / "manifest.json",
    ]
    for directory in CHECKPOINT_SHA256:
        required.extend(
            [
                LOCAL_MODEL_ROOT / directory / ".hydra" / "config.yaml",
                LOCAL_MODEL_ROOT / directory / "last_one.ckpt",
            ]
        )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError("RealPXRD-Solver Modal inputs are not staged: " + ", ".join(missing))


if modal.is_local():
    _assert_local_inputs()

image = (
    modal.Image.from_registry("pytorch/pytorch:2.3.1-cuda12.1-cudnn8-runtime")
    .pip_install(
        "numpy==1.26.4",
        "scipy==1.13.1",
        "hydra-core==1.3.2",
        "lightning==2.3.3",
        "pytorch-lightning==2.3.3",
        "torchmetrics==1.4.0.post0",
        "torch-geometric==2.5.3",
        "pymatgen==2024.11.13",
        "tqdm==4.66.4",
        "setuptools==70.1.0",
    )
    .pip_install(
        "torch-scatter==2.1.2",
        find_links="https://data.pyg.org/whl/torch-2.3.0+cu121.html",
    )
    .add_local_dir(
        LOCAL_SOURCE,
        str(REMOTE_SOURCE),
        copy=True,
        ignore=["**/__pycache__/**", "**/*.pyc"],
    )
    .add_local_dir(LOCAL_MODEL_ROOT, str(REMOTE_MODEL_ROOT), copy=True)
    .add_local_dir(LOCAL_TARGETS, str(REMOTE_TARGETS), copy=True)
    .env(
        {
            "PYTHONPATH": str(REMOTE_SOURCE),
            "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True",
            **DATASET.environment(),
        }
    )
)

app = modal.App(APP_NAME)


def _seed_everything(seed: int) -> None:
    import numpy as np
    import torch

    random.seed(seed)
    np.random.seed(seed % (2**32 - 1))
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def _load_model(input_mode: str) -> Any:
    from omegaconf import OmegaConf  # type: ignore[reportMissingImports]

    directory = model_directory(input_mode)
    model_root = REMOTE_MODEL_ROOT / directory
    checkpoint = model_root / "last_one.ckpt"
    if sha256_file(checkpoint) != CHECKPOINT_SHA256[directory]:
        raise RuntimeError(f"RealPXRD-Solver {directory} checkpoint digest mismatch")
    if str(REMOTE_SOURCE) not in sys.path:
        sys.path.insert(0, str(REMOTE_SOURCE))
    from app.model.flow import CSPFlow  # type: ignore[reportMissingImports]

    cfg = OmegaConf.load(model_root / ".hydra" / "config.yaml")
    model = CSPFlow.load_from_checkpoint(
        str(checkpoint), map_location="cpu", strict=True, **cfg.model
    )
    model.eval().cuda(0)
    expected_keep_lattice = input_mode == LATTICE_CONDITIONED_ORACLE
    if bool(model.keep_lattice) != expected_keep_lattice:
        raise RuntimeError("RealPXRD-Solver checkpoint does not match the requested lattice mode")
    return model


def _run_request(request: dict[str, Any]) -> Path:
    import numpy as np
    import torch
    from pymatgen.io.cif import CifWriter
    from torch_geometric.data import Batch, Data  # type: ignore[reportMissingImports]

    run_id = validate_run_id(str(request["run_id"]))
    shard_index = int(request["shard_index"])
    case_ids = [str(value) for value in request["case_ids"]]
    if not case_ids or len(case_ids) != len(set(case_ids)):
        raise ValueError("case_ids must be a non-empty deduplicated list")
    input_mode = str(request.get("input_mode", DEFAULT_INPUT_MODE))
    if input_mode not in INPUT_MODES:
        raise ValueError(f"unsupported RealPXRD-Solver input mode: {input_mode}")
    samples = int(request.get("samples", DEFAULT_SAMPLES))
    timesteps = int(request.get("infer_timesteps", DEFAULT_TIMESTEPS))
    step_lr = float(request.get("step_lr", DEFAULT_STEP_LR))
    if not 1 <= samples <= MAX_SAMPLES:
        raise ValueError(f"samples must be in [1, {MAX_SAMPLES}]")
    if timesteps <= 0 or 1000 % timesteps:
        raise ValueError("infer_timesteps must be a positive divisor of 1000")
    seed_base = int(request["seed_base"])

    payload = json.loads((REMOTE_TARGETS / "manifest.json").read_text(encoding="utf-8"))
    validate_target_payload(payload, DATASET)
    validate_request_identity(request, payload, DATASET)
    ordered = list(payload["cases"])
    targets = {str(case["case_id"]): case for case in ordered}
    order = {str(case["case_id"]): index for index, case in enumerate(ordered)}
    unknown = sorted(set(case_ids) - set(targets))
    if unknown:
        raise ValueError(f"unknown RealPXRD-Solver cases: {unknown}")

    torch.cuda.reset_peak_memory_stats()
    started = time.perf_counter()
    model = _load_model(input_mode)
    loaded = time.perf_counter()
    temporary = Path(tempfile.mkdtemp(prefix="realpxrd-solver-output-"))
    destination = temporary / run_id / f"shard-{shard_index:03d}"
    destination.mkdir(parents=True)
    records: list[dict[str, Any]] = []
    generation_seconds = 0.0

    for case_id in case_ids:
        case = targets[case_id]
        case_seed = seed_base + order[case_id]
        _seed_everything(case_seed)
        conditioning = case_input(case, input_mode)
        peaks = load_model_peaks(REMOTE_TARGETS / str(case["pattern_path"]))
        data_list = []
        for _ in range(samples):
            fields: dict[str, Any] = {
                "atom_types": torch.tensor(conditioning["atom_types"], dtype=torch.long),
                "pxrd_x": torch.tensor(peaks[:, 0], dtype=torch.float32).view(-1, 1),
                "pxrd_y": torch.tensor(peaks[:, 1], dtype=torch.float32).view(-1, 1),
                "peak_num": len(peaks),
                "num_atoms": conditioning["atom_count"],
                "num_nodes": conditioning["atom_count"],
            }
            if conditioning["lattice_matrix"] is not None:
                fields["lattice_matrix"] = torch.tensor(
                    conditioning["lattice_matrix"], dtype=torch.float32
                ).view(1, 3, 3)
            data_list.append(Data(**fields))
        batch = Batch.from_data_list(data_list).cuda(0)
        case_started = time.perf_counter()
        with torch.inference_mode():
            output = model.sample(batch, step_lr=step_lr, infer_timesteps=timesteps)
        torch.cuda.synchronize()
        case_seconds = time.perf_counter() - case_started
        generation_seconds += case_seconds

        predicted_counts = output["num_atoms"].detach().cpu().to(torch.long).tolist()
        predicted_types = output["atom_types"].detach().cpu().to(torch.long).numpy()
        frac_coords = output["frac_coords"].detach().cpu().numpy()
        lattices = output["lattices"].detach().cpu().numpy()
        if len(predicted_counts) != samples or len(lattices) != samples:
            raise RuntimeError(f"{case_id}: model returned the wrong candidate count")
        atom_offset = 0
        case_root = destination / "candidates" / case_id
        case_root.mkdir(parents=True)
        for sample_index, site_count in enumerate(predicted_counts):
            species = predicted_types[atom_offset : atom_offset + site_count]
            coordinates = frac_coords[atom_offset : atom_offset + site_count]
            atom_offset += site_count
            raw_path = case_root / f"candidate-{sample_index + 1:02d}.raw.npz"
            np.savez_compressed(
                raw_path,
                atom_types=species,
                frac_coords=coordinates,
                lattice_matrix=lattices[sample_index],
                num_atoms=np.asarray([site_count], dtype=np.int64),
            )
            record: dict[str, Any] = {
                "case_id": case_id,
                "sample_index": sample_index,
                "seed": case_seed,
                "input_mode": input_mode,
                "input_formula": conditioning["formula"],
                "input_atom_count": conditioning["atom_count"],
                "oracle_input": conditioning["oracle_input"],
                "input_lattice_conditioned": conditioning["lattice_matrix"] is not None,
                "model_peak_count": len(peaks),
                "predicted_site_count": int(site_count),
                "runtime_seconds_case_batch": case_seconds,
                "raw_path": str(raw_path.relative_to(destination)),
                "raw_sha256": sha256_file(raw_path),
            }
            try:
                structure = output_structure(lattices[sample_index], species, coordinates)
                cif_path = case_root / f"candidate-{sample_index + 1:02d}.cif"
                cif_path.write_text(str(CifWriter(structure, symprec=None)), encoding="utf-8")
                record.update(
                    {
                        "status": "generated",
                        "candidate_path": str(cif_path.relative_to(destination)),
                        "candidate_sha256": sha256_file(cif_path),
                        "predicted_formula": structure.composition.reduced_formula,
                        "volume_angstrom3": float(structure.volume),
                    }
                )
            except Exception as exc:
                error_path = case_root / f"candidate-{sample_index + 1:02d}.invalid.json"
                error_path.write_text(
                    json.dumps({"error": f"{type(exc).__name__}: {exc}"}, indent=2) + "\n",
                    encoding="utf-8",
                )
                record.update(
                    {
                        "status": "invalid",
                        "candidate_path": str(error_path.relative_to(destination)),
                        "candidate_sha256": sha256_file(error_path),
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )
            records.append(record)
        if atom_offset != len(predicted_types):
            raise RuntimeError(f"{case_id}: atom tensor did not split cleanly")

    completed = time.perf_counter()
    result = {
        "schema_version": "1.0.0",
        "framework": "RealPXRD-Solver",
        "source_commit": SOURCE_COMMIT,
        "checkpoint_sha256": CHECKPOINT_SHA256[model_directory(input_mode)],
        **DATASET.request_identity(),
        "run_id": run_id,
        "shard_index": shard_index,
        "case_ids": case_ids,
        "case_count": len(case_ids),
        "samples_per_case": samples,
        "candidate_count": len(records),
        "generated_candidate_count": sum(row["status"] == "generated" for row in records),
        "invalid_candidate_count": sum(row["status"] == "invalid" for row in records),
        "inference": {
            "input_mode": input_mode,
            "oracle_input": input_mode != "lattice-free-reduced-formula",
            "candidate_order": "released sampler order; no unreleased Rietveld ranking",
            "infer_timesteps": timesteps,
            "step_lr": step_lr,
            "seed_base": seed_base,
        },
        "runtime": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "cuda_runtime": str(torch.version.cuda),
            "device_name": torch.cuda.get_device_name(0),
            "model_load_seconds": loaded - started,
            "generation_seconds": generation_seconds,
            "serialization_seconds": completed - loaded - generation_seconds,
            "total_seconds": completed - started,
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
    return destination


@app.function(image=image, gpu=DEFAULT_GPU, cpu=4, memory=16384, timeout=1800)
def realpxrd_solver_doctor_remote() -> dict[str, Any]:
    payload = json.loads((REMOTE_TARGETS / "manifest.json").read_text(encoding="utf-8"))
    validate_target_payload(payload, DATASET)
    reports: dict[str, Any] = {}
    for input_mode in ("lattice-free-primitive-formula-oracle", LATTICE_CONDITIONED_ORACLE):
        request = {
            "run_id": "doctor-" + model_directory(input_mode).lower(),
            "shard_index": 0,
            "case_ids": [str(payload["cases"][0]["case_id"])],
            "seed_base": 20260809,
            "samples": 1,
            "infer_timesteps": 1,
            "step_lr": DEFAULT_STEP_LR,
            "input_mode": input_mode,
            **DATASET.request_identity(),
        }
        destination = _run_request(request)
        result = json.loads((destination / "results.json").read_text(encoding="utf-8"))
        reports[input_mode] = {
            "checkpoint_sha256": result["checkpoint_sha256"],
            "candidate_count": result["candidate_count"],
            "generated_candidate_count": result["generated_candidate_count"],
        }
    return {
        "status": "OK",
        "device_name": __import__("torch").cuda.get_device_name(0),
        "source_commit": SOURCE_COMMIT,
        "modes": reports,
        "smoke_infer_timesteps": 1,
        "production_infer_timesteps": DEFAULT_TIMESTEPS,
        "benchmark_started": False,
    }


@app.function(
    image=image,
    gpu=DEFAULT_GPU,
    cpu=2,
    memory=16384,
    timeout=86_400,
    max_containers=4,
)
def realpxrd_solver_generate_remote(request_json: str) -> bytes:
    return archive_directory(_run_request(json.loads(request_json)))


def case_ids() -> list[str]:
    payload = json.loads((LOCAL_TARGETS / "manifest.json").read_text(encoding="utf-8"))
    return [str(case["case_id"]) for case in payload["cases"]]


def make_requests(
    *,
    run_id: str,
    shard_size: int = DEFAULT_SHARD_SIZE,
    seed_base: int = 20260809,
    input_mode: str = DEFAULT_INPUT_MODE,
) -> list[dict[str, Any]]:
    if input_mode not in INPUT_MODES:
        raise ValueError(f"unsupported RealPXRD-Solver input mode: {input_mode}")
    ids = case_ids()
    return [
        {
            "run_id": validate_run_id(run_id),
            "shard_index": shard_index,
            "case_ids": ids[start : start + shard_size],
            "seed_base": seed_base,
            "samples": DEFAULT_SAMPLES,
            "infer_timesteps": DEFAULT_TIMESTEPS,
            "step_lr": DEFAULT_STEP_LR,
            "input_mode": input_mode,
            **DATASET.request_identity(),
        }
        for shard_index, start in enumerate(range(0, len(ids), shard_size))
    ]


def modal_doctor(*, gpu_type: str = DEFAULT_GPU) -> dict[str, Any]:
    with modal.enable_output(), app.run():
        return dict(realpxrd_solver_doctor_remote.with_options(gpu=gpu_type).remote())


def modal_run(request: dict[str, Any], output_root: Path, *, gpu_type: str = DEFAULT_GPU) -> Path:
    with modal.enable_output(), app.run():
        payload = realpxrd_solver_generate_remote.with_options(gpu=gpu_type).remote(
            json.dumps(request, sort_keys=True)
        )
    return materialize_archive(payload, output_root)


def modal_submit(
    requests: list[dict[str, Any]],
    handle_path: Path,
    *,
    gpu_type: str = DEFAULT_GPU,
    max_containers: int = 4,
) -> Path:
    calls: list[dict[str, Any]] = []
    with modal.enable_output(), app.run(detach=True):
        configured = realpxrd_solver_generate_remote.with_options(
            gpu=gpu_type, max_containers=max_containers, timeout=86_400
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
        "framework": "RealPXRD-Solver",
        "app_name": APP_NAME,
        "created_at": datetime.now(timezone.utc).isoformat(),  # noqa: UP017 (remote 3.10)
        "gpu_type": gpu_type,
        "max_containers": max_containers,
        "run_id": requests[0]["run_id"],
        "input_mode": requests[0]["input_mode"],
        **DATASET.request_identity(),
        "completed_shards": [],
        "calls": calls,
    }
    write_atomic(handle_path, json.dumps(handle, indent=2, sort_keys=True) + "\n")
    return handle_path


def modal_collect(handle_path: Path, output_root: Path, *, timeout: float = 0) -> dict[str, Any]:
    return collect_handle(handle_path, output_root, timeout=timeout)
