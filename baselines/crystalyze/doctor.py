"""Verify that the pinned Crystalyze model can be constructed and loaded.

The published Lightning checkpoint embeds an author-machine path for GemNet's
scale file. Loading it through ``load_from_checkpoint`` therefore fails away
from that machine. This doctor instantiates the same model from the published,
portable ``hparams.yaml`` and then loads the checkpoint state dictionary. It
does not alter either source or artifact bytes.

Run with the isolated upstream environment::

    python baselines/crystalyze/doctor.py
"""

from __future__ import annotations

import json
import os
import sys
from importlib.metadata import version
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CHECKOUT = ROOT / ".upstream" / "Crystalyze"
MODEL_PATH = ROOT / ".runs" / "crystalyze-model" / "model_folder"
RUN_ROOT = ROOT / ".runs"


def configure_runtime() -> None:
    os.environ.setdefault("PROJECT_ROOT", str(CHECKOUT))
    os.environ.setdefault("HYDRA_JOBS", str(RUN_ROOT / "crystalyze-hydra"))
    # WABDB_DIR is the spelling used by the pinned upstream Hydra config.
    os.environ.setdefault("WABDB_DIR", str(RUN_ROOT / "crystalyze-wandb"))
    sys.path.insert(0, str(CHECKOUT))
    sys.path.insert(1, str(CHECKOUT / "scripts"))
    (RUN_ROOT / "crystalyze-hydra").mkdir(parents=True, exist_ok=True)
    (RUN_ROOT / "crystalyze-wandb").mkdir(parents=True, exist_ok=True)


def portable_load_model() -> tuple[Any, Any, Any]:
    """Load the published model without replaying its embedded absolute path."""

    configure_runtime()
    import hydra
    import numpy as np
    import torch
    from hydra import initialize_config_dir
    from hydra.experimental import compose

    with initialize_config_dir(str(MODEL_PATH)):
        cfg = compose(config_name="hparams")
        model = hydra.utils.instantiate(
            cfg.model,
            optim=cfg.optim,
            data=cfg.data,
            logging=cfg.logging,
            _recursive_=False,
        )
    checkpoints = list(MODEL_PATH.glob("*.ckpt"))
    if len(checkpoints) != 1:
        raise RuntimeError(f"expected one checkpoint, found {len(checkpoints)}")
    checkpoint = torch.load(checkpoints[0], map_location="cpu")
    state_result = model.load_state_dict(checkpoint["state_dict"], strict=False)
    if state_result.missing_keys or state_result.unexpected_keys:
        raise RuntimeError(
            "checkpoint state mismatch: "
            f"missing={state_result.missing_keys}, unexpected={state_result.unexpected_keys}"
        )
    model.lattice_scaler = torch.load(MODEL_PATH / "lattice_scaler.pt", map_location="cpu")
    model.scaler = torch.load(MODEL_PATH / "prop_scaler.pt", map_location="cpu")
    model.eval()
    return model, cfg, np


def main() -> None:
    configure_runtime()
    import torch
    import torch_geometric
    import torch_scatter
    import torch_sparse

    model, _, np = portable_load_model()
    report = {
        "checkpoint_load": "OK",
        "cuda_available": torch.cuda.is_available(),
        "device": str(next(model.parameters()).device),
        "in_dim": model.in_dim,
        "max_atoms": model.hparams.max_atoms,
        "model_class": model.__class__.__name__,
        "numpy": np.__version__,
        "parameter_count": sum(parameter.numel() for parameter in model.parameters()),
        "pymatgen": version("pymatgen"),
        "python": sys.version.split()[0],
        "torch": torch.__version__,
        "torch_geometric": torch_geometric.__version__,
        "torch_scatter": torch_scatter.__version__,
        "torch_sparse": torch_sparse.__version__,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
