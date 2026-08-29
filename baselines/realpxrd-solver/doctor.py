"""Strict, generation-free compatibility check for RealPXRD-Solver."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from importlib.metadata import version
from pathlib import Path
from typing import Any

from verifiable_pxrd.baselines.targets import framework_target_root

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = ROOT.parent
SOURCE = ROOT / ".upstream" / "RealPXRD-Solver"
MODEL_ROOT = ROOT / ".runs" / "realpxrd-solver-model"
LOCK_PATH = Path(__file__).with_name("artifacts.lock.json")
SOURCE_COMMIT = "5e7e60176e1875071a12fb4583a1f0112bc3bcad"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def verify_source() -> str:
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=SOURCE,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    require(revision == SOURCE_COMMIT, "RealPXRD-Solver source revision mismatch")
    dirty_lines = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=SOURCE,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    dirty = "\n".join(line for line in dirty_lines if "__pycache__/" not in line)
    require(not dirty, "RealPXRD-Solver source checkout is dirty")
    return revision


def verify_artifacts() -> dict[str, str]:
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    digests: dict[str, str] = {}
    for artifact in lock["artifacts"]:
        path = ROOT / lock["destination"] / artifact["path"]
        require(path.is_file(), f"missing RealPXRD-Solver artifact: {artifact['path']}")
        require(path.stat().st_size == artifact["size_bytes"], f"size mismatch: {path}")
        digest = sha256_file(path)
        require(digest == artifact["sha256"], f"digest mismatch: {path}")
        digests[artifact["path"]] = digest
    return digests


def verify_target(corpus: Path) -> tuple[dict[str, Any], Any]:
    import numpy as np

    target = framework_target_root(REPOSITORY_ROOT, "realpxrd-solver", corpus)
    manifest = json.loads((target / "manifest.json").read_text(encoding="utf-8"))
    source_manifest = corpus / "manifest.json"
    require(
        manifest["source_manifest_sha256"] == sha256_file(source_manifest),
        f"stale RealPXRD-Solver targets: {corpus}",
    )
    require(len(manifest["cases"]) == 100, f"target case count: {corpus}")
    for case in manifest["cases"]:
        path = target / case["pattern_path"]
        require(sha256_file(path) == case["pattern_sha256"], f"target digest: {path}")
    first = manifest["cases"][0]
    peaks = np.loadtxt(target / first["pattern_path"], dtype=np.float64)
    peaks = peaks.reshape(-1, 2)
    peaks = peaks[peaks[:, 1] > 5.0]
    require(len(peaks) == first["model_peak_count"], "model peak count mismatch")
    return first, peaks


def strict_load_and_encode(
    torch: Any, mode: str, first: dict[str, Any], peaks: Any
) -> dict[str, Any]:
    from omegaconf import OmegaConf
    from pymatgen.core import Element
    from torch_geometric.data import Batch, Data

    if str(SOURCE) not in sys.path:
        sys.path.insert(0, str(SOURCE))
    from app.model.flow import CSPFlow

    directory = "pxrd-all-L" if mode == "lattice-conditioned" else "pxrd-all"
    model_dir = MODEL_ROOT / directory
    cfg = OmegaConf.load(model_dir / ".hydra" / "config.yaml")
    model = CSPFlow.load_from_checkpoint(
        str(model_dir / "last_one.ckpt"), map_location="cpu", strict=True, **cfg.model
    )
    model.eval()
    atom_types: list[int] = []
    for symbol, count in first["primitive_cell_composition"].items():
        atom_types.extend([int(Element(symbol).Z)] * int(count))
    data = Data(
        atom_types=torch.tensor(atom_types, dtype=torch.long),
        pxrd_x=torch.tensor(peaks[:, 0], dtype=torch.float32).view(-1, 1),
        pxrd_y=torch.tensor(peaks[:, 1], dtype=torch.float32).view(-1, 1),
        peak_num=len(peaks),
        num_atoms=len(atom_types),
        num_nodes=len(atom_types),
    )
    batch = Batch.from_data_list([data])
    with torch.inference_mode():
        embedding = model.xrd_encoder(batch.pxrd_x, batch.pxrd_y, batch.peak_num)
    require(tuple(embedding.shape) == (1, 512), f"unexpected encoder shape: {embedding.shape}")
    require(bool(torch.isfinite(embedding).all()), "encoder produced non-finite values")
    checkpoint = torch.load(model_dir / "last_one.ckpt", map_location="cpu")
    return {
        "checkpoint_epoch": int(checkpoint["epoch"]),
        "checkpoint_global_step": int(checkpoint["global_step"]),
        "checkpoint_lightning": checkpoint["pytorch-lightning_version"],
        "conditioning_embedding_l2_norm": float(embedding.norm()),
        "conditioning_embedding_shape": list(embedding.shape),
        "keep_lattice": bool(model.keep_lattice),
        "parameter_count": sum(parameter.numel() for parameter in model.parameters()),
        "state_tensor_count": len(checkpoint["state_dict"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", type=Path, action="append")
    args = parser.parse_args()
    corpora = args.corpus_root or [
        REPOSITORY_ROOT / "pxrd-bench" / "pXRD-100",
        REPOSITORY_ROOT / "pxrd-bench" / "pXRD-ood",
    ]
    try:
        import lightning
        import numpy as np
        import torch
        import torch_geometric
    except ImportError as exc:
        raise SystemExit(
            "RealPXRD-Solver inference dependencies are missing; use the environment "
            "commands in baselines/realpxrd-solver/README.md"
        ) from exc

    revision = verify_source()
    digests = verify_artifacts()
    targets: dict[str, Any] = {}
    first_case: dict[str, Any] | None = None
    first_peaks = None
    for corpus in corpora:
        case, peaks = verify_target(corpus.resolve())
        targets[corpus.name] = {
            "case_count": 100,
            "conditioning_case": case["case_id"],
            "conditioning_peak_count": len(peaks),
        }
        if first_case is None:
            first_case, first_peaks = case, peaks
    assert first_case is not None and first_peaks is not None
    models = {
        mode: strict_load_and_encode(torch, mode, first_case, first_peaks)
        for mode in ("lattice-free", "lattice-conditioned")
    }
    report = {
        "status": "OK",
        "source_commit": revision,
        "artifact_count": len(digests),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "pymatgen": version("pymatgen"),
        "torch": torch.__version__,
        "lightning": lightning.__version__,
        "torch_geometric": torch_geometric.__version__,
        "models": models,
        "targets": targets,
        "generation_performed": False,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
