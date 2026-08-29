"""Verify the pinned deCIFer checkpoint, source, and pXRD-100 inputs.

The checkpoint pickles ``TrainConfig`` under ``__main__``. Importing that
class into this script's global namespace before ``torch.load`` is the
byte-preserving portability workaround used here; no checkpoint bytes change.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np

from verifiable_pxrd.baselines.targets import framework_target_root

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = ROOT.parent
CHECKOUT = ROOT / ".upstream" / "deCIFer"
CHECKPOINT = ROOT / ".runs" / "decifer-model" / "decifer_v1_ckpt.pt"
TARGET_ROOT = framework_target_root(
    REPOSITORY_ROOT,
    "decifer",
    REPOSITORY_ROOT / "pxrd-bench" / "pXRD-100",
)
EXPECTED_CHECKPOINT_SHA256 = "6d97e352f99dc6dbc5ced102ed10ee0693651a81f429f20ea50c2bc1fe18b78b"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def portable_load_checkpoint(torch: Any, train_config: Any) -> dict[str, Any]:
    # torch serialized the class as __main__.TrainConfig. This assignment makes
    # that exact name available without rewriting the published archive.
    globals()["TrainConfig"] = train_config
    try:
        return torch.load(CHECKPOINT, map_location="cpu", weights_only=False, mmap=True)
    except TypeError:
        return torch.load(CHECKPOINT, map_location="cpu")


def main() -> None:
    if sha256_file(CHECKPOINT) != EXPECTED_CHECKPOINT_SHA256:
        raise RuntimeError("official deCIFer checkpoint is missing or has a digest mismatch")

    sys.path.insert(0, str(CHECKOUT))
    import torch
    from bin.train import TrainConfig as UpstreamTrainConfig
    from decifer.decifer_model import Decifer, DeciferConfig
    from decifer.tokenizer import ATOMS, UNK_TOKEN, Tokenizer

    checkpoint = portable_load_checkpoint(torch, UpstreamTrainConfig)
    model_args = checkpoint["model_args"]
    expected_model_args = {
        "block_size": 3076,
        "condition": True,
        "condition_size": 1000,
        "n_embd": 512,
        "n_head": 8,
        "n_layer": 8,
        "vocab_size": 372,
    }
    for key, expected in expected_model_args.items():
        if model_args.get(key) != expected:
            raise RuntimeError(f"checkpoint {key}={model_args.get(key)!r}, expected {expected!r}")

    training_config = checkpoint["config"]
    expected_training_xrd = {
        "eta_range_max": 0.5,
        "eta_range_min": 0.5,
        "fwhm_range_max": 0.1,
        "fwhm_range_min": 0.001,
        "mask_prob": 0.0,
        "noise_range_max": 0.05,
        "noise_range_min": 0.001,
        "qmax": 10.0,
        "qmin": 0.0,
        "qstep": 0.01,
        "wavelength": "CuKa",
    }
    for key, expected in expected_training_xrd.items():
        if training_config.get(key) != expected:
            raise RuntimeError(
                f"checkpoint training config {key}={training_config.get(key)!r}, "
                f"expected {expected!r}"
            )

    model = Decifer(DeciferConfig(**model_args)).to("cpu")
    state_result = model.load_state_dict(checkpoint["best_model_state"], strict=True)
    if state_result.missing_keys or state_result.unexpected_keys:
        raise RuntimeError(
            f"checkpoint state mismatch: missing={state_result.missing_keys}, "
            f"unexpected={state_result.unexpected_keys}"
        )
    model.eval()

    tokenizer = Tokenizer()
    manifest = json.loads((TARGET_ROOT / "manifest.json").read_text(encoding="utf-8"))
    if manifest["pattern_count"] != 100 or len(manifest["cases"]) != 100:
        raise RuntimeError("expected 100 deCIFer targets")
    known_atoms = set(ATOMS)
    for case in manifest["cases"]:
        unknown_elements = set(case["elements"]) - known_atoms
        if unknown_elements:
            raise RuntimeError(f"{case['case_id']}: unsupported elements {unknown_elements}")
        prompt = f"data_{case['composition']}\n"
        if UNK_TOKEN in tokenizer.tokenize_cif(prompt):
            raise RuntimeError(f"{case['case_id']}: composition prompt contains unknown tokens")
        for field in ("source_cell_formula_sum", "primitive_cell_formula_sum"):
            oracle_prompt = f"data_{case[field]}\n"
            if UNK_TOKEN in tokenizer.tokenize_cif(oracle_prompt):
                raise RuntimeError(f"{case['case_id']}: {field} prompt contains unknown tokens")
        pattern = np.loadtxt(TARGET_ROOT / case["pattern_path"], delimiter=",", skiprows=1)
        if pattern.shape != (1000, 2):
            raise RuntimeError(f"{case['case_id']}: target shape is {pattern.shape}")

    first = manifest["cases"][0]
    first_pattern = np.loadtxt(TARGET_ROOT / first["pattern_path"], delimiter=",", skiprows=1)[:, 1]
    condition = torch.from_numpy(first_pattern).to(dtype=torch.float32).unsqueeze(0)
    with torch.inference_mode():
        embedding = model.transformer.cond_embedding(condition)
    if tuple(embedding.shape) != (1, 512) or not torch.isfinite(embedding).all():
        raise RuntimeError("checkpoint conditioning encoder rejected the benchmark vector")

    prompt_text = f"data_{first['composition']}\n"
    prompt_ids = tokenizer.encode(tokenizer.tokenize_cif(prompt_text))
    prompt = torch.tensor(prompt_ids, dtype=torch.long).unsqueeze(0)
    torch.manual_seed(0)
    generated = model.generate_batched_reps(
        prompt,
        max_new_tokens=1,
        cond_vec=condition,
        start_indices_batch=[[0]],
        temperature=1.0,
        top_k=None,
        disable_pbar=True,
    )
    if generated.shape[0] != 1 or generated.shape[1] <= prompt.shape[1]:
        raise RuntimeError("checkpoint failed a one-token conditioned generation smoke test")

    report = {
        "checkpoint_config_xrd": expected_training_xrd,
        "checkpoint_load": "OK",
        "checkpoint_sha256": EXPECTED_CHECKPOINT_SHA256,
        "conditioning_embedding_shape": list(embedding.shape),
        "conditioned_generation_smoke": "OK",
        "cuda_available": torch.cuda.is_available(),
        "model_class": model.__class__.__name__,
        "model_parameter_count": sum(parameter.numel() for parameter in model.parameters()),
        "pymatgen_cuka_angstrom": 1.54184,
        "python": sys.version.split()[0],
        "target_count": manifest["pattern_count"],
        "tokenizer_vocab_size": tokenizer.vocab_size,
        "torch": torch.__version__,
    }
    if not math.isclose(float(first_pattern.max()), 1.0, abs_tol=5e-10):
        raise RuntimeError("first target is not max-normalized")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
