"""Modal inference for the pinned deCIFer pXRD-100 baseline."""

from __future__ import annotations

import json
import platform
import random
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
LOCAL_SOURCE = BASELINES_ROOT / ".upstream" / "deCIFer"
LOCAL_CHECKPOINT = BASELINES_ROOT / ".runs" / "decifer-model" / "decifer_v1_ckpt.pt"
LOCAL_TARGETS = DATASET.target_root("decifer")

REMOTE_ROOT = Path("/opt/decifer")
REMOTE_SOURCE = REMOTE_ROOT / "source"
REMOTE_CHECKPOINT = REMOTE_ROOT / "decifer_v1_ckpt.pt"
REMOTE_TARGETS = REMOTE_ROOT / "targets"

APP_NAME = f"verifiable-pxrd-decifer-{DATASET.slug}"
SOURCE_COMMIT = "91ace18de9aa118f1174942fbe1ec85f127c7864"
CHECKPOINT_SHA256 = "6d97e352f99dc6dbc5ced102ed10ee0693651a81f429f20ea50c2bc1fe18b78b"
DEFAULT_GPU = "L4"
DEFAULT_MAX_NEW_TOKENS = 3076
DEFAULT_SAMPLES = 8
DEFAULT_TEMPERATURE = 1.0
DEFAULT_TOP_K = 50
COMPOSITION_MODES = ("reduced", "full-cell-oracle")


def _assert_local_inputs() -> None:
    required = [
        LOCAL_SOURCE / "decifer" / "decifer_model.py",
        LOCAL_SOURCE / "bin" / "train.py",
        LOCAL_CHECKPOINT,
        LOCAL_TARGETS / "manifest.json",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError("deCIFer Modal inputs are not staged: " + ", ".join(missing))


if modal.is_local():
    _assert_local_inputs()

image = (
    modal.Image.debian_slim(python_version="3.11")
    .uv_pip_install(
        "torch==2.13.0",
        index_url="https://download.pytorch.org/whl/cu130",
    )
    .uv_pip_install(
        "numpy==2.4.6",
        "pymatgen==2026.5.4",
        "omegaconf==2.3.0",
        "periodictable==2.0.2",
        "h5py==3.16.0",
        "pydantic==2.13.4",
        "seaborn==0.13.2",
        "tqdm==4.67.3",
    )
    .add_local_dir(
        LOCAL_SOURCE,
        str(REMOTE_SOURCE),
        copy=True,
        ignore=["**/.git/**", "**/__pycache__/**", "**/*.pyc"],
    )
    .add_local_file(LOCAL_CHECKPOINT, str(REMOTE_CHECKPOINT), copy=True)
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


def _target_payload() -> dict[str, Any]:
    payload = json.loads((REMOTE_TARGETS / "manifest.json").read_text(encoding="utf-8"))
    validate_target_payload(payload, DATASET)
    return payload


def _seed_everything(seed: int) -> None:
    import numpy as np
    import torch

    random.seed(seed)
    np.random.seed(seed % (2**32 - 1))
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def _load_model() -> tuple[Any, Any]:
    import torch
    from bin.train import TrainConfig
    from decifer.decifer_model import Decifer, DeciferConfig
    from decifer.tokenizer import Tokenizer

    if sha256_file(REMOTE_CHECKPOINT) != CHECKPOINT_SHA256:
        raise RuntimeError("deCIFer checkpoint digest mismatch")
    # The published pickle names this class ``__main__.TrainConfig``.
    sys.modules["__main__"].__dict__["TrainConfig"] = TrainConfig
    try:
        checkpoint = torch.load(
            REMOTE_CHECKPOINT,
            map_location="cpu",
            weights_only=False,
            mmap=True,
        )
    except TypeError:
        checkpoint = torch.load(REMOTE_CHECKPOINT, map_location="cpu")
    model = Decifer(DeciferConfig(**checkpoint["model_args"]))
    state = model.load_state_dict(checkpoint["best_model_state"], strict=True)
    if state.missing_keys or state.unexpected_keys:
        raise RuntimeError(
            f"checkpoint state mismatch: missing={state.missing_keys}, "
            f"unexpected={state.unexpected_keys}"
        )
    del checkpoint
    model.eval().cuda(0)
    model.device = torch.device("cuda:0")
    return model, Tokenizer()


def _postprocess_cif(raw_cif: str) -> str:
    from decifer.utility import (
        extract_space_group_symbol,
        reinstate_symmetry_loop,
        replace_symmetry_loop_with_P1,
    )

    processed = replace_symmetry_loop_with_P1(raw_cif)
    spacegroup = extract_space_group_symbol(processed)
    if spacegroup != "P 1":
        processed = reinstate_symmetry_loop(processed, spacegroup)
    return processed


def _run_request(request: dict[str, Any]) -> Path:
    import numpy as np
    import torch
    from decifer.tokenizer import UNK_TOKEN
    from pymatgen.core import Structure

    run_id = validate_run_id(str(request["run_id"]))
    shard_index = int(request["shard_index"])
    case_ids = [str(value) for value in request["case_ids"]]
    if not case_ids or len(case_ids) != len(set(case_ids)):
        raise ValueError("case_ids must be a non-empty deduplicated list")
    max_new_tokens = int(request.get("max_new_tokens", DEFAULT_MAX_NEW_TOKENS))
    samples = int(request.get("samples", DEFAULT_SAMPLES))
    if not 1 <= max_new_tokens <= DEFAULT_MAX_NEW_TOKENS:
        raise ValueError("max_new_tokens is outside the checkpoint context")
    if not 1 <= samples <= DEFAULT_SAMPLES:
        raise ValueError("samples must be in [1, 8]")
    seed_base = int(request["seed_base"])
    composition_mode = str(request.get("composition_mode", "reduced"))
    if composition_mode not in COMPOSITION_MODES:
        raise ValueError(
            f"composition_mode must be one of {COMPOSITION_MODES}, found {composition_mode!r}"
        )

    payload = _target_payload()
    validate_request_identity(request, payload, DATASET)
    ordered = list(payload["cases"])
    targets = {str(case["case_id"]): case for case in ordered}
    order = {str(case["case_id"]): index for index, case in enumerate(ordered)}
    unknown = sorted(set(case_ids) - set(targets))
    if unknown:
        raise ValueError(f"unknown deCIFer cases: {unknown}")

    torch.cuda.reset_peak_memory_stats()
    started = time.perf_counter()
    model, tokenizer = _load_model()
    loaded = time.perf_counter()
    temporary = Path(tempfile.mkdtemp(prefix="decifer-output-"))
    destination = temporary / run_id / f"shard-{shard_index:03d}"
    destination.mkdir(parents=True)
    records: list[dict[str, Any]] = []
    generation_seconds = 0.0

    for case_id in case_ids:
        case = targets[case_id]
        case_seed = seed_base + order[case_id]
        _seed_everything(case_seed)
        pattern = np.loadtxt(REMOTE_TARGETS / str(case["pattern_path"]), delimiter=",", skiprows=1)[
            :, 1
        ]
        condition = torch.as_tensor(pattern, dtype=torch.float32, device="cuda").repeat(samples, 1)
        if composition_mode == "full-cell-oracle":
            input_formula = str(case["paper_native_cell_composition"])
            input_mode = "full_cell_formula_oracle_from_hidden_cif"
        else:
            input_formula = str(case["composition"])
            input_mode = "reduced_formula"
        prompt_text = f"data_{input_formula}\n"
        prompt_tokens = tokenizer.tokenize_cif(prompt_text)
        if UNK_TOKEN in prompt_tokens:
            raise RuntimeError(f"{case_id}: prompt contains unknown tokens")
        prompt = (
            torch.tensor(tokenizer.encode(prompt_tokens), dtype=torch.long, device="cuda")
            .unsqueeze(0)
            .repeat(samples, 1)
        )
        case_started = time.perf_counter()
        with torch.inference_mode():
            generated = model.generate_batched_reps(
                prompt,
                max_new_tokens=max_new_tokens,
                cond_vec=condition,
                start_indices_batch=[[0]] * samples,
                temperature=DEFAULT_TEMPERATURE,
                top_k=DEFAULT_TOP_K,
                disable_pbar=True,
            )
        torch.cuda.synchronize()
        case_seconds = time.perf_counter() - case_started
        generation_seconds += case_seconds
        case_root = destination / "candidates" / case_id
        case_root.mkdir(parents=True)
        for sample_index, token_row in enumerate(generated.detach().cpu().tolist()):
            ids = [int(value) for value in token_row if int(value) != tokenizer.padding_id]
            raw_cif = tokenizer.decode(ids)
            raw_path = case_root / f"candidate-{sample_index + 1:02d}.raw.cif"
            raw_path.write_text(raw_cif, encoding="utf-8")
            record: dict[str, Any] = {
                "case_id": case_id,
                "sample_index": sample_index,
                "seed": case_seed,
                "sampling_stream_position": sample_index,
                "runtime_seconds_case_batch": case_seconds,
                "raw_path": str(raw_path.relative_to(destination)),
                "raw_sha256": sha256_file(raw_path),
                "prompt": prompt_text,
                "input_mode": input_mode,
                "input_formula": input_formula,
            }
            try:
                processed = _postprocess_cif(raw_cif)
                structure = Structure.from_str(processed, fmt="cif")
                cif_path = case_root / f"candidate-{sample_index + 1:02d}.cif"
                cif_path.write_text(processed, encoding="utf-8")
                record.update(
                    {
                        "status": "generated",
                        "candidate_path": str(cif_path.relative_to(destination)),
                        "candidate_sha256": sha256_file(cif_path),
                        "predicted_formula": structure.composition.reduced_formula,
                        "predicted_site_count": len(structure),
                        "volume_angstrom3": float(structure.volume),
                    }
                )
            except Exception as exc:
                record.update(
                    {
                        "status": "invalid",
                        "candidate_path": str(raw_path.relative_to(destination)),
                        "candidate_sha256": sha256_file(raw_path),
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )
            records.append(record)

    completed = time.perf_counter()
    result = {
        "schema_version": "1.0.0",
        "framework": "deCIFer",
        "framework_commit": SOURCE_COMMIT,
        "checkpoint_sha256": CHECKPOINT_SHA256,
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
            "composition": (
                "paper-native full-cell formula oracle from hidden CIF"
                if composition_mode == "full-cell-oracle"
                else "reduced formula"
            ),
            "composition_mode": composition_mode,
            "space_group_conditioning": False,
            "temperature": DEFAULT_TEMPERATURE,
            "top_k": DEFAULT_TOP_K,
            "max_new_tokens": max_new_tokens,
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
def decifer_doctor_remote() -> dict[str, Any]:
    payload = _target_payload()
    request = {
        "run_id": "doctor",
        "shard_index": 0,
        "case_ids": [str(payload["cases"][0]["case_id"])],
        "seed_base": 20260719,
        "max_new_tokens": 8,
        "samples": 1,
        **DATASET.request_identity(),
    }
    destination = _run_request(request)
    result = json.loads((destination / "results.json").read_text(encoding="utf-8"))
    return {
        "status": "OK",
        "checkpoint_sha256": CHECKPOINT_SHA256,
        "device_name": result["runtime"]["device_name"],
        "torch": result["runtime"]["torch"],
        "generated_or_retained": result["candidate_count"],
    }


@app.function(
    image=image,
    gpu=DEFAULT_GPU,
    cpu=2,
    memory=8192,
    timeout=86_400,
    max_containers=5,
)
def decifer_generate_remote(request_json: str) -> bytes:
    destination = _run_request(json.loads(request_json))
    return archive_directory(destination)


def case_ids() -> list[str]:
    payload = json.loads((LOCAL_TARGETS / "manifest.json").read_text(encoding="utf-8"))
    return [str(case["case_id"]) for case in payload["cases"]]


def make_requests(
    *,
    run_id: str,
    shard_size: int = 10,
    seed_base: int = 20260719,
    composition_mode: str = "reduced",
) -> list[dict[str, Any]]:
    if composition_mode not in COMPOSITION_MODES:
        raise ValueError(
            f"composition_mode must be one of {COMPOSITION_MODES}, found {composition_mode!r}"
        )
    ids = case_ids()
    return [
        {
            "run_id": validate_run_id(run_id),
            "shard_index": shard_index,
            "case_ids": ids[start : start + shard_size],
            "seed_base": seed_base,
            "max_new_tokens": DEFAULT_MAX_NEW_TOKENS,
            "samples": DEFAULT_SAMPLES,
            "composition_mode": composition_mode,
            **DATASET.request_identity(),
        }
        for shard_index, start in enumerate(range(0, len(ids), shard_size))
    ]


def modal_doctor(*, gpu_type: str = DEFAULT_GPU) -> dict[str, Any]:
    with modal.enable_output(), app.run():
        return dict(decifer_doctor_remote.with_options(gpu=gpu_type).remote())


def modal_run(request: dict[str, Any], output_root: Path, *, gpu_type: str = DEFAULT_GPU) -> Path:
    with modal.enable_output(), app.run():
        payload = decifer_generate_remote.with_options(gpu=gpu_type).remote(
            json.dumps(request, sort_keys=True)
        )
    return materialize_archive(payload, output_root)


def modal_submit(
    requests: list[dict[str, Any]],
    handle_path: Path,
    *,
    gpu_type: str = DEFAULT_GPU,
    max_containers: int = 5,
) -> Path:
    calls: list[dict[str, Any]] = []
    with modal.enable_output(), app.run(detach=True):
        configured = decifer_generate_remote.with_options(
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
        "framework": "deCIFer",
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
