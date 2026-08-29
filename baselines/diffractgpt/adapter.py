"""Modal inference for the immutable paper-era DiffractGPT adapter."""

from __future__ import annotations

import importlib.util
import json
import platform
import random
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
LOCAL_SOURCE = BASELINES_ROOT / ".upstream" / "atomgpt"
LOCAL_BASE = BASELINES_ROOT / ".runs" / "diffractgpt-model" / "base"
LOCAL_ADAPTER = BASELINES_ROOT / ".runs" / "diffractgpt-model" / "paper-formula"
LOCAL_TARGETS = DATASET.target_root("diffractgpt")

REMOTE_ROOT = Path("/opt/diffractgpt")
REMOTE_SOURCE = REMOTE_ROOT / "source"
REMOTE_BASE = REMOTE_ROOT / "base"
REMOTE_ADAPTER = REMOTE_ROOT / "adapter"
REMOTE_TARGETS = REMOTE_ROOT / "targets"

APP_NAME = f"verifiable-pxrd-diffractgpt-{DATASET.slug}"
SOURCE_COMMIT = "f2f4d58c4dcab9ae1a3cdd30c8f13d94f4da7928"
BASE_REVISION = "3c47be0aa392c058e26ede776ecd2d5416fa5d28"
ADAPTER_REVISION = "4080c1e4ece70b82f4defc622141fc733fc2dce2"
BASE_MODEL_SHA256 = "5dd9ab1b69aa46a86d5a62d030c9bf82af60ac6525aaa1c7b0d9d4419aecb37d"
ADAPTER_SHA256 = "82b0a486d083f374141287e7cbbd15e4142c3f63468bef618bffa1ae5d878855"
DEFAULT_GPU = "L4"
DEFAULT_MAX_NEW_TOKENS = 1024
DEFAULT_SAMPLES = 1
DEFAULT_SAMPLE_BATCH_SIZE = 1


def _assert_local_inputs() -> None:
    required = [
        LOCAL_SOURCE / "atomgpt" / "inverse_models" / "utils.py",
        LOCAL_BASE / "model.safetensors",
        LOCAL_BASE / "config.json",
        LOCAL_ADAPTER / "adapter_model.safetensors",
        LOCAL_ADAPTER / "adapter_config.json",
        LOCAL_TARGETS / "manifest.json",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError("DiffractGPT Modal inputs are not staged: " + ", ".join(missing))


if modal.is_local():
    _assert_local_inputs()

image = (
    modal.Image.from_registry("pytorch/pytorch:2.2.2-cuda12.1-cudnn8-runtime")
    .pip_install(
        "numpy==1.26.4",
        "scipy==1.13.1",
        "transformers==4.41.2",
        "peft==0.11.1",
        "bitsandbytes==0.43.1",
        "accelerate==0.31.0",
        "safetensors==0.4.3",
        "sentencepiece==0.2.0",
        "jarvis-tools==2024.10.30",
        "pymatgen==2024.5.1",
        "pydantic==2.13.4",
    )
    .add_local_dir(
        LOCAL_SOURCE,
        str(REMOTE_SOURCE),
        copy=True,
        ignore=["**/.git/**", "**/__pycache__/**", "**/*.pyc"],
    )
    .add_local_dir(LOCAL_BASE, str(REMOTE_BASE), copy=True)
    .add_local_dir(LOCAL_ADAPTER, str(REMOTE_ADAPTER), copy=True)
    .add_local_dir(LOCAL_TARGETS, str(REMOTE_TARGETS), copy=True)
    .env(
        {
            "PYTHONPATH": str(REMOTE_SOURCE),
            "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True",
            "TOKENIZERS_PARALLELISM": "false",
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


def _load_model() -> tuple[Any, Any]:
    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer

    if sha256_file(REMOTE_BASE / "model.safetensors") != BASE_MODEL_SHA256:
        raise RuntimeError("DiffractGPT base-model digest mismatch")
    if sha256_file(REMOTE_ADAPTER / "adapter_model.safetensors") != ADAPTER_SHA256:
        raise RuntimeError("DiffractGPT adapter digest mismatch")
    tokenizer = AutoTokenizer.from_pretrained(REMOTE_ADAPTER, local_files_only=True)
    tokenizer.padding_side = "left"
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    base = AutoModelForCausalLM.from_pretrained(
        REMOTE_BASE,
        local_files_only=True,
        device_map={"": 0},
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True,
    )
    model = PeftModel.from_pretrained(base, REMOTE_ADAPTER, is_trainable=False)
    model.eval()
    return model, tokenizer


def _load_text2atoms() -> Any:
    """Load the pinned parser without importing AtomGPT's training stack."""

    parser_path = REMOTE_SOURCE / "atomgpt" / "inverse_models" / "utils.py"
    spec = importlib.util.spec_from_file_location("diffractgpt_paper_utils", parser_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load DiffractGPT parser: {parser_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.text2atoms


def _run_request(request: dict[str, Any]) -> Path:
    import torch
    from pymatgen.core import Lattice, Structure
    from pymatgen.io.cif import CifWriter

    text2atoms = _load_text2atoms()

    run_id = validate_run_id(str(request["run_id"]))
    shard_index = int(request["shard_index"])
    case_ids = [str(value) for value in request["case_ids"]]
    if not case_ids or len(case_ids) != len(set(case_ids)):
        raise ValueError("case_ids must be a non-empty deduplicated list")
    max_new_tokens = int(request.get("max_new_tokens", DEFAULT_MAX_NEW_TOKENS))
    samples = int(request.get("samples", DEFAULT_SAMPLES))
    sample_batch_size = int(request.get("sample_batch_size", DEFAULT_SAMPLE_BATCH_SIZE))
    if not 1 <= max_new_tokens <= DEFAULT_MAX_NEW_TOKENS:
        raise ValueError("max_new_tokens must be in [1, 1024]")
    if samples != DEFAULT_SAMPLES:
        raise ValueError("DiffractGPT's paper profile requires exactly one sample")
    if not 1 <= sample_batch_size <= samples:
        raise ValueError("sample_batch_size must be in [1, samples]")
    seed_base = int(request["seed_base"])

    payload = json.loads((REMOTE_TARGETS / "manifest.json").read_text(encoding="utf-8"))
    validate_target_payload(payload, DATASET)
    validate_request_identity(request, payload, DATASET)
    ordered = list(payload["cases"])
    targets = {str(case["case_id"]): case for case in ordered}
    order = {str(case["case_id"]): index for index, case in enumerate(ordered)}
    unknown = sorted(set(case_ids) - set(targets))
    if unknown:
        raise ValueError(f"unknown DiffractGPT cases: {unknown}")

    _seed_everything(seed_base)
    torch.cuda.reset_peak_memory_stats()
    started = time.perf_counter()
    model, tokenizer = _load_model()
    loaded = time.perf_counter()
    temporary = Path(tempfile.mkdtemp(prefix="diffractgpt-output-"))
    destination = temporary / run_id / f"shard-{shard_index:03d}"
    destination.mkdir(parents=True)
    records: list[dict[str, Any]] = []
    generation_seconds = 0.0

    for case_id in case_ids:
        case = targets[case_id]
        prompt_text = (REMOTE_TARGETS / str(case["prompt_path"])).read_text(encoding="utf-8")
        case_root = destination / "candidates" / case_id
        case_root.mkdir(parents=True)
        case_seed = seed_base + order[case_id] * 100
        for sample_start in range(0, samples, sample_batch_size):
            count = min(sample_batch_size, samples - sample_start)
            stream_seed = case_seed + sample_start
            _seed_everything(stream_seed)
            encoded = tokenizer([prompt_text] * count, return_tensors="pt", padding=True).to("cuda")
            prompt_width = int(encoded["input_ids"].shape[1])
            batch_started = time.perf_counter()
            with torch.inference_mode():
                outputs = model.generate(
                    **encoded,
                    max_new_tokens=max_new_tokens,
                    use_cache=True,
                    do_sample=False,
                    num_return_sequences=1,
                    pad_token_id=tokenizer.pad_token_id,
                    eos_token_id=tokenizer.eos_token_id,
                )
            torch.cuda.synchronize()
            batch_seconds = time.perf_counter() - batch_started
            generation_seconds += batch_seconds
            responses = tokenizer.batch_decode(
                outputs[:, prompt_width:],
                clean_up_tokenization_spaces=False,
                skip_special_tokens=True,
            )
            for offset, response in enumerate(responses):
                sample_index = sample_start + offset
                raw_path = case_root / f"candidate-{sample_index + 1:02d}.raw.txt"
                raw_path.write_text(response, encoding="utf-8")
                record: dict[str, Any] = {
                    "case_id": case_id,
                    "sample_index": sample_index,
                    "seed": stream_seed,
                    "sampling_stream_position": offset,
                    "runtime_seconds_batch_share": batch_seconds / count,
                    "raw_path": str(raw_path.relative_to(destination)),
                    "raw_sha256": sha256_file(raw_path),
                    "prompt_path": str(case["prompt_path"]),
                    "prompt_sha256": str(case["prompt_sha256"]),
                    "model_formula": str(case["model_formula"]),
                }
                try:
                    # The released helper splits a full decoded prompt on ``# Output:``,
                    # leaving the prompt's newline at the start of the parser input.
                    atoms = text2atoms("\n" + response)
                    structure = Structure(
                        Lattice(atoms.lattice_mat),
                        atoms.elements,
                        atoms.frac_coords,
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
        "framework": "DiffractGPT",
        "framework_commit": SOURCE_COMMIT,
        "base_model_revision": BASE_REVISION,
        "base_model_sha256": BASE_MODEL_SHA256,
        "adapter_revision": ADAPTER_REVISION,
        "adapter_sha256": ADAPTER_SHA256,
        "adapter_license": "not-specified; review-required",
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
            "composition": "reduced formula",
            "profile": "paper-aligned single greedy decode",
            "decoding": "greedy",
            "do_sample": False,
            "max_new_tokens": max_new_tokens,
            "samples": samples,
            "sample_batch_size": sample_batch_size,
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


@app.function(image=image, gpu=DEFAULT_GPU, cpu=4, memory=32768, timeout=3600)
def diffractgpt_doctor_remote() -> dict[str, Any]:
    payload = json.loads((REMOTE_TARGETS / "manifest.json").read_text(encoding="utf-8"))
    validate_target_payload(payload, DATASET)
    request = {
        "run_id": "doctor",
        "shard_index": 0,
        "case_ids": [str(payload["cases"][0]["case_id"])],
        "seed_base": 20260719,
        "max_new_tokens": 32,
        "samples": 1,
        "sample_batch_size": 1,
        **DATASET.request_identity(),
    }
    destination = _run_request(request)
    result = json.loads((destination / "results.json").read_text(encoding="utf-8"))
    return {
        "status": "OK",
        "base_model_sha256": BASE_MODEL_SHA256,
        "adapter_sha256": ADAPTER_SHA256,
        "device_name": result["runtime"]["device_name"],
        "torch": result["runtime"]["torch"],
        "generated_or_retained": result["candidate_count"],
    }


@app.function(
    image=image,
    gpu=DEFAULT_GPU,
    cpu=4,
    memory=32768,
    timeout=86_400,
    max_containers=4,
)
def diffractgpt_generate_remote(request_json: str) -> bytes:
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
            "max_new_tokens": DEFAULT_MAX_NEW_TOKENS,
            "samples": DEFAULT_SAMPLES,
            "sample_batch_size": DEFAULT_SAMPLE_BATCH_SIZE,
            **DATASET.request_identity(),
        }
        for shard_index, start in enumerate(range(0, len(ids), shard_size))
    ]


def modal_doctor(*, gpu_type: str = DEFAULT_GPU) -> dict[str, Any]:
    with modal.enable_output(), app.run():
        return dict(diffractgpt_doctor_remote.with_options(gpu=gpu_type).remote())


def modal_run(request: dict[str, Any], output_root: Path, *, gpu_type: str = DEFAULT_GPU) -> Path:
    with modal.enable_output(), app.run():
        payload = diffractgpt_generate_remote.with_options(gpu=gpu_type).remote(
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
        configured = diffractgpt_generate_remote.with_options(
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
        "framework": "DiffractGPT",
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
