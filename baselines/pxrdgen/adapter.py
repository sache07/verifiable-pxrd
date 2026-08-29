"""Modal inference for PXRDGen using the hidden-CIF primitive atom-count oracle."""

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
LOCAL_SOURCE = BASELINES_ROOT / ".upstream" / "PXRDGen"
LOCAL_MODEL_ROOT = BASELINES_ROOT / ".runs" / "pxrdgen-model"
LOCAL_TARGETS = DATASET.target_root("pxrdgen")

REMOTE_ROOT = Path("/opt/pxrdgen")
REMOTE_SOURCE = REMOTE_ROOT / "source"
REMOTE_MODEL_ROOT = REMOTE_ROOT / "model"
REMOTE_TARGETS = REMOTE_ROOT / "targets"
REMOTE_MODEL_SOURCE = REMOTE_SOURCE / "code" / "xrd2struc"
REMOTE_CONFIG = (
    REMOTE_SOURCE / "data" / "outs" / "xrd2struc" / "flow_CNN" / ".hydra" / "config.yaml"
)
REMOTE_CHECKPOINT = REMOTE_MODEL_ROOT / "flow_CNN" / "last_one.ckpt"
REMOTE_ENCODER = REMOTE_MODEL_ROOT / "pre_ckpt" / "CL_CNN_0_05.ckpt"

APP_NAME = f"verifiable-pxrd-pxrdgen-{DATASET.slug}"
CAPSULE_DOI = "10.24433/CO.6347299.v1"
CHECKPOINT_SHA256 = "a92b0194e167cfc654448d2f748785ca883ed3ffccbefcb69345e44d91acab91"
ENCODER_SHA256 = "f2bf33649a6417ebc0d3e7032d21dd1c2f0647d22f7b499e31d491704aa56eee"
DEFAULT_GPU = "L4"
DEFAULT_SAMPLES = 8
DEFAULT_TIMESTEPS = 200
DEFAULT_STEP_LR = 5.0


def _assert_local_inputs() -> None:
    required = [
        LOCAL_SOURCE / "code" / "xrd2struc" / "pxrdgen" / "model" / "flow_shift_align.py",
        LOCAL_SOURCE / "data" / "outs" / "xrd2struc" / "flow_CNN" / ".hydra" / "config.yaml",
        LOCAL_MODEL_ROOT / "flow_CNN" / "last_one.ckpt",
        LOCAL_MODEL_ROOT / "pre_ckpt" / "CL_CNN_0_05.ckpt",
        LOCAL_TARGETS / "manifest.json",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError("PXRDGen Modal inputs are not staged: " + ", ".join(missing))


if modal.is_local():
    _assert_local_inputs()

image = (
    modal.Image.from_registry("pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime")
    .pip_install(
        "numpy==1.26.4",
        "scipy==1.11.4",
        "hydra-core==1.3.2",
        "lightning==2.1.4",
        "pytorch-lightning==2.1.4",
        "torchmetrics==1.3.0.post0",
        "torch-geometric==2.4.0",
        "pymatgen==2023.8.10",
        "chemparse==0.3.1",
        "tqdm==4.66.1",
        "setuptools==69.5.1",
    )
    .pip_install(
        "torch-scatter==2.1.2",
        find_links="https://data.pyg.org/whl/torch-2.1.0+cu118.html",
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
            "PYTHONPATH": str(REMOTE_MODEL_SOURCE),
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


def _load_model() -> Any:
    from omegaconf import OmegaConf

    if sha256_file(REMOTE_CHECKPOINT) != CHECKPOINT_SHA256:
        raise RuntimeError("PXRDGen flow checkpoint digest mismatch")
    if sha256_file(REMOTE_ENCODER) != ENCODER_SHA256:
        raise RuntimeError("PXRDGen encoder checkpoint digest mismatch")
    sys.path.insert(0, str(REMOTE_MODEL_SOURCE))
    from pxrdgen.model.flow_shift_align import CSPFlow

    cfg = OmegaConf.load(REMOTE_CONFIG)
    cfg.workpath = str(REMOTE_MODEL_SOURCE)
    cfg.model.ckpt_path = str(REMOTE_ENCODER.parent) + "/"
    model_kwargs = OmegaConf.to_container(cfg.model, resolve=True)
    if not isinstance(model_kwargs, dict):
        raise RuntimeError("PXRDGen model configuration did not resolve to a mapping")
    model = CSPFlow.load_from_checkpoint(
        str(REMOTE_CHECKPOINT),
        map_location="cpu",
        strict=True,
        **model_kwargs,
    )
    model.eval().cuda(0)
    return model


def _run_request(request: dict[str, Any]) -> Path:
    import chemparse
    import numpy as np
    import torch
    from pymatgen.core import Element, Lattice, Structure
    from pymatgen.io.cif import CifWriter
    from torch_geometric.data import Batch, Data

    run_id = validate_run_id(str(request["run_id"]))
    shard_index = int(request["shard_index"])
    case_ids = [str(value) for value in request["case_ids"]]
    if not case_ids or len(case_ids) != len(set(case_ids)):
        raise ValueError("case_ids must be a non-empty deduplicated list")
    samples = int(request.get("samples", DEFAULT_SAMPLES))
    timesteps = int(request.get("infer_timesteps", DEFAULT_TIMESTEPS))
    step_lr = float(request.get("step_lr", DEFAULT_STEP_LR))
    if not 1 <= samples <= DEFAULT_SAMPLES:
        raise ValueError("samples must be in [1, 8]")
    if not 1 <= timesteps <= 200:
        raise ValueError("infer_timesteps must be in [1, 200]")
    seed_base = int(request["seed_base"])

    payload = json.loads((REMOTE_TARGETS / "manifest.json").read_text(encoding="utf-8"))
    validate_target_payload(payload, DATASET)
    validate_request_identity(request, payload, DATASET)
    ordered = list(payload["cases"])
    targets = {str(case["case_id"]): case for case in ordered}
    order = {str(case["case_id"]): index for index, case in enumerate(ordered)}
    unknown = sorted(set(case_ids) - set(targets))
    if unknown:
        raise ValueError(f"unknown PXRDGen cases: {unknown}")

    torch.cuda.reset_peak_memory_stats()
    started = time.perf_counter()
    model = _load_model()
    loaded = time.perf_counter()
    temporary = Path(tempfile.mkdtemp(prefix="pxrdgen-output-"))
    destination = temporary / run_id / f"shard-{shard_index:03d}"
    destination.mkdir(parents=True)
    records: list[dict[str, Any]] = []
    generation_seconds = 0.0

    for case_id in case_ids:
        case = targets[case_id]
        case_seed = seed_base + order[case_id]
        _seed_everything(case_seed)
        formula = str(case["primitive_cell_formula"])
        composition = chemparse.parse_formula(formula)
        atom_types: list[int] = []
        for symbol, count in composition.items():
            integer_count = int(count)
            if float(count) != integer_count:
                raise ValueError(f"{case_id}: non-integral primitive formula {formula}")
            atom_types.extend([int(Element(symbol).Z)] * integer_count)
        if len(atom_types) != int(case["primitive_cell_atom_count"]):
            raise RuntimeError(f"{case_id}: primitive formula count does not match manifest")
        xrd = np.loadtxt(REMOTE_TARGETS / str(case["pattern_path"]))
        if xrd.shape != (7500,):
            raise RuntimeError(f"{case_id}: expected a 7,500-value PXRD vector")
        data_list = [
            Data(
                atom_types=torch.tensor(atom_types, dtype=torch.long),
                xrd_array=torch.tensor(xrd, dtype=torch.float32).view(1, -1),
                num_atoms=len(atom_types),
                num_nodes=len(atom_types),
            )
            for _ in range(samples)
        ]
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
        if len(predicted_counts) != samples:
            raise RuntimeError(f"{case_id}: model returned the wrong candidate count")
        atom_offset = 0
        case_root = destination / "candidates" / case_id
        case_root.mkdir(parents=True)
        for sample_index, site_count in enumerate(predicted_counts):
            species = predicted_types[atom_offset : atom_offset + site_count]
            coords = frac_coords[atom_offset : atom_offset + site_count]
            atom_offset += site_count
            raw_path = case_root / f"candidate-{sample_index + 1:02d}.raw.npz"
            np.savez_compressed(
                raw_path,
                atom_types=species,
                frac_coords=coords,
                lattice=lattices[sample_index],
                num_atoms=np.asarray([site_count], dtype=np.int64),
            )
            record: dict[str, Any] = {
                "case_id": case_id,
                "sample_index": sample_index,
                "seed": case_seed,
                "input_formula": formula,
                "input_atom_count": len(atom_types),
                "input_mode": "primitive_cell_formula_oracle_from_hidden_cif",
                "predicted_site_count": int(site_count),
                "runtime_seconds_case_batch": case_seconds,
                "raw_path": str(raw_path.relative_to(destination)),
                "raw_sha256": sha256_file(raw_path),
            }
            try:
                structure = Structure(
                    Lattice(lattices[sample_index]),
                    species.tolist(),
                    coords,
                    coords_are_cartesian=False,
                )
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
        "framework": "PXRDGen",
        "capsule_doi": CAPSULE_DOI,
        "checkpoint_sha256": CHECKPOINT_SHA256,
        "encoder_checkpoint_sha256": ENCODER_SHA256,
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
            "input_mode": "primitive_cell_formula_oracle_from_hidden_cif",
            "atom_count_source": "hidden target CIF primitive cell",
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


@app.function(image=image, gpu=DEFAULT_GPU, cpu=4, memory=32768, timeout=1800)
def pxrdgen_doctor_remote() -> dict[str, Any]:
    payload = json.loads((REMOTE_TARGETS / "manifest.json").read_text(encoding="utf-8"))
    validate_target_payload(payload, DATASET)
    request = {
        "run_id": "doctor",
        "shard_index": 0,
        "case_ids": [str(payload["cases"][0]["case_id"])],
        "seed_base": 20260719,
        "samples": 1,
        "infer_timesteps": 1,
        "step_lr": DEFAULT_STEP_LR,
        **DATASET.request_identity(),
    }
    destination = _run_request(request)
    result = json.loads((destination / "results.json").read_text(encoding="utf-8"))
    return {
        "status": "OK",
        "checkpoint_sha256": CHECKPOINT_SHA256,
        "encoder_checkpoint_sha256": ENCODER_SHA256,
        "device_name": result["runtime"]["device_name"],
        "torch": result["runtime"]["torch"],
        "generated_or_retained": result["candidate_count"],
    }


@app.function(
    image=image,
    gpu=DEFAULT_GPU,
    cpu=2,
    memory=16384,
    timeout=86_400,
    max_containers=4,
)
def pxrdgen_generate_remote(request_json: str) -> bytes:
    return archive_directory(_run_request(json.loads(request_json)))


def case_ids() -> list[str]:
    payload = json.loads((LOCAL_TARGETS / "manifest.json").read_text(encoding="utf-8"))
    return [str(case["case_id"]) for case in payload["cases"]]


def make_requests(
    *, run_id: str, shard_size: int = 10, seed_base: int = 20260719
) -> list[dict[str, Any]]:
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
            **DATASET.request_identity(),
        }
        for shard_index, start in enumerate(range(0, len(ids), shard_size))
    ]


def modal_doctor(*, gpu_type: str = DEFAULT_GPU) -> dict[str, Any]:
    with modal.enable_output(), app.run():
        return dict(pxrdgen_doctor_remote.with_options(gpu=gpu_type).remote())


def modal_run(request: dict[str, Any], output_root: Path, *, gpu_type: str = DEFAULT_GPU) -> Path:
    with modal.enable_output(), app.run():
        payload = pxrdgen_generate_remote.with_options(gpu=gpu_type).remote(
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
        configured = pxrdgen_generate_remote.with_options(
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
        "framework": "PXRDGen",
        "app_name": APP_NAME,
        "created_at": datetime.now(timezone.utc).isoformat(),  # noqa: UP017 (remote Python 3.10)
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
