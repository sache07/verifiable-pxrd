"""Strict compatibility check for the published PXRDGen flow-CNN model.

This imports the immutable Code Ocean source, lets ``CSPFlow.__init__`` load
the authors' standalone CNN encoder exactly as released, strict-loads the full
Lightning checkpoint, and sends one native 7,500-value pXRD vector through the
conditioning encoder. It intentionally does not run the 200-step flow sampler.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from verifiable_pxrd.baselines.targets import framework_target_root

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = ROOT.parent
LOCK_PATH = Path(__file__).with_name("artifacts.lock.json")
SOURCE_ROOT = ROOT / ".upstream" / "PXRDGen"
MODEL_SOURCE = SOURCE_ROOT / "code" / "xrd2struc"
CONFIG_PATH = SOURCE_ROOT / "data" / "outs" / "xrd2struc" / "flow_CNN" / ".hydra" / "config.yaml"
CHECKPOINT = ROOT / ".runs" / "pxrdgen-model" / "flow_CNN" / "last_one.ckpt"
ENCODER_CHECKPOINT = ROOT / ".runs" / "pxrdgen-model" / "pre_ckpt" / "CL_CNN_0_05.ckpt"
TARGET_ROOT = framework_target_root(
    REPOSITORY_ROOT,
    "pxrdgen",
    REPOSITORY_ROOT / "pxrd-bench" / "pXRD-100",
)

EXPECTED_CASES = 100
EXPECTED_PANELS = {"challenge": 30, "polymorph": 40, "representative": 30}
EXPECTED_CHECKPOINT_SHA256 = "a92b0194e167cfc654448d2f748785ca883ed3ffccbefcb69345e44d91acab91"
EXPECTED_ENCODER_SHA256 = "f2bf33649a6417ebc0d3e7032d21dd1c2f0647d22f7b499e31d491704aa56eee"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_locked_artifacts() -> None:
    lock = read_json(LOCK_PATH)
    source_destination = ROOT / lock["source_destination"]
    for artifact in lock["source_artifacts"]:
        path = source_destination / artifact["capsule_path"]
        require(path.is_file(), f"missing capsule source: {artifact['capsule_path']}")
        require(path.stat().st_size == artifact["size_bytes"], f"source size: {path}")
        require(sha256_file(path) == artifact["sha256"], f"source digest: {path}")
    require(sha256_file(CHECKPOINT) == EXPECTED_CHECKPOINT_SHA256, "flow checkpoint digest")
    require(sha256_file(ENCODER_CHECKPOINT) == EXPECTED_ENCODER_SHA256, "encoder digest")


def verify_targets(np: Any) -> tuple[dict[str, Any], Any]:
    manifest = read_json(TARGET_ROOT / "manifest.json")
    cases = manifest["cases"]
    require(manifest["pattern_count"] == EXPECTED_CASES, "target pattern_count is not 100")
    require(len(cases) == EXPECTED_CASES, "target manifest is not 100 cases")
    require(len({case["case_id"] for case in cases}) == EXPECTED_CASES, "duplicate cases")
    require(Counter(case["panel"] for case in cases) == EXPECTED_PANELS, "panel counts")
    with (TARGET_ROOT / "inputs.csv").open(encoding="utf-8", newline="") as stream:
        combined_rows = list(csv.DictReader(stream))
    primitive_differing = sum(
        row["primitive_formula_differs_from_reduced"] == "True" for row in combined_rows
    )
    target_cell_differing = sum(
        row["target_cif_cell_formula_differs_from_reduced"] == "True" for row in combined_rows
    )
    require(
        manifest["primitive_formula_differs_from_reduced_count"] == primitive_differing,
        "reduced/primitive formula difference count",
    )
    require(
        manifest["target_cif_cell_formula_differs_from_reduced_count"] == target_cell_differing,
        "reduced/target-cell formula difference count",
    )
    for csv_name in (
        "inputs.csv",
        "inputs-reduced-formula.csv",
        "inputs-primitive-cell-formula-oracle.csv",
    ):
        with (TARGET_ROOT / csv_name).open(encoding="utf-8", newline="") as stream:
            require(sum(1 for _ in csv.DictReader(stream)) == EXPECTED_CASES, f"{csv_name} rows")
    first_vector = None
    for case in cases:
        path = TARGET_ROOT / case["pattern_path"]
        require(path.is_file(), f"missing pattern: {case['case_id']}")
        require(sha256_file(path) == case["pattern_sha256"], f"pattern digest: {case['case_id']}")
        values = np.loadtxt(path)
        require(values.shape == (7500,), f"pattern shape: {case['case_id']}")
        require(bool(np.isfinite(values).all()), f"non-finite pattern: {case['case_id']}")
        require(
            math.isclose(float(values.max()), 1.0, abs_tol=5e-8),
            f"normalization: {case['case_id']}",
        )
        if first_vector is None:
            first_vector = values
    return cases[0], first_vector


def strict_load_and_encode(
    torch: Any, OmegaConf: Any, vector: Any
) -> tuple[Any, Any, dict[str, Any]]:
    sys.path.insert(0, str(MODEL_SOURCE))
    from pxrdgen.model.flow_shift_align import CSPFlow

    cfg = OmegaConf.load(CONFIG_PATH)
    cfg.workpath = str(MODEL_SOURCE)
    # The capsule concatenates these two strings instead of joining paths.
    cfg.model.ckpt_path = str(ENCODER_CHECKPOINT.parent) + "/"
    model_kwargs = OmegaConf.to_container(cfg.model, resolve=True)
    require(isinstance(model_kwargs, dict), "model config did not resolve to a mapping")

    # CSPFlow.__init__ first strict-loads CL_CNN_0_05.ckpt. That artifact was
    # serialized from CUDA, and the released constructor omits ``map_location``.
    # Supply CPU mapping only for omitted calls while retaining the exact bytes
    # and upstream load_state_dict; Modal/CUDA needs no such portability shim.
    original_torch_load = torch.load

    def cpu_portable_torch_load(*args: Any, **kwargs: Any) -> Any:
        kwargs.setdefault("map_location", "cpu")
        return original_torch_load(*args, **kwargs)

    torch.load = cpu_portable_torch_load
    try:
        # Lightning strict-loads every tensor in last_one.ckpt into the model.
        model = CSPFlow.load_from_checkpoint(
            str(CHECKPOINT),
            map_location="cpu",
            strict=True,
            **model_kwargs,
        )
    finally:
        torch.load = original_torch_load
    model.eval()
    # PyG batches the per-case ``Data.xrd_array`` from (1, 7500) to
    # (batch_size, 7500); the CNN itself inserts the singleton channel axis.
    condition = torch.as_tensor(vector, dtype=torch.float32).reshape(1, 7500)
    with torch.inference_mode():
        embedding = model.xrd_encoder(condition)
        normalized = embedding / embedding.norm(dim=-1, keepdim=True)
    require(tuple(embedding.shape) == (1, 256), f"encoder shape: {tuple(embedding.shape)}")
    require(bool(torch.isfinite(embedding).all()), "encoder produced non-finite values")
    require(bool(torch.isfinite(normalized).all()), "normalized condition is non-finite")

    checkpoint_payload = torch.load(str(CHECKPOINT), map_location="cpu")
    metadata = {
        "checkpoint_epoch": int(checkpoint_payload["epoch"]),
        "checkpoint_global_step": int(checkpoint_payload["global_step"]),
        "checkpoint_lightning": checkpoint_payload["pytorch-lightning_version"],
        "state_tensor_count": len(checkpoint_payload["state_dict"]),
    }
    return model, embedding, metadata


def main() -> None:
    try:
        import numpy as np
        import torch
        from omegaconf import OmegaConf
    except ImportError as exc:
        raise SystemExit(
            "PXRDGen inference dependencies are missing; use the environment command in "
            "baselines/pxrdgen/README.md"
        ) from exc

    verify_locked_artifacts()
    first_case, vector = verify_targets(np)
    model, embedding, checkpoint_metadata = strict_load_and_encode(torch, OmegaConf, vector)
    report = {
        **checkpoint_metadata,
        "checkpoint_load": "strict OK",
        "conditioning_case": first_case["case_id"],
        "conditioning_embedding_l2_norm": float(embedding.norm().item()),
        "conditioning_embedding_shape": list(embedding.shape),
        "cuda_available": torch.cuda.is_available(),
        "inference_timesteps": 200,
        "model_parameter_count": sum(parameter.numel() for parameter in model.parameters()),
        "pXRD_vector_shape": [1, 7500],
        "python": sys.version.split()[0],
        "target_count": EXPECTED_CASES,
        "torch": torch.__version__,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
