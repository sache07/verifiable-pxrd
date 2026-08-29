from __future__ import annotations

import os
import tomllib
from pathlib import Path
from typing import Any

from .models import ExperimentConfig, PromptPaths


def _resolve(root: Path, value: str) -> Path:
    expanded = Path(os.path.expanduser(os.path.expandvars(value)))
    return expanded.resolve() if expanded.is_absolute() else (root / expanded).resolve()


def load_config(path: Path) -> ExperimentConfig:
    path = path.resolve()
    root = path.parent
    with path.open("rb") as stream:
        raw: dict[str, Any] = tomllib.load(stream)
    if int(raw.get("schema_version", 0)) != 1:
        raise ValueError("experiment config schema_version must be 1")
    paths = raw["paths"]
    prompts = raw["prompts"]
    return ExperimentConfig(
        root=root,
        experiment_id=str(raw["id"]),
        benchmark_repo=_resolve(root, str(paths["benchmark_repo"])),
        condition=_resolve(root, str(paths["condition"])),
        examples=_resolve(root, str(paths["examples"])),
        splits=_resolve(root, str(paths["splits"])),
        run_root=_resolve(root, str(paths["run_root"])),
        prompts=PromptPaths(
            wrapper=_resolve(root, str(prompts["wrapper"])),
            seed_policy=_resolve(root, str(prompts["seed_policy"])),
            reflection=_resolve(root, str(prompts["reflection"])),
            feedback=_resolve(root, str(prompts["feedback"])),
            continuation=_resolve(root, str(prompts["continuation"])),
        ),
        reviewer=dict(raw["reviewer"]),
        reflection=dict(raw["reflection"]),
        objective=dict(raw["objective"]),
        gepa=dict(raw["gepa"]),
        finalist_evaluation=dict(raw["finalist_evaluation"]),
    )
