from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class Example:
    example_id: str
    problem_id: str
    formula: str
    wavelength: float
    pattern: Path
    trace: Path
    final_response: Path
    candidates: tuple[Path, ...]
    reference: Path
    rwp_report: Path | None


@dataclass(frozen=True, slots=True)
class PromptPaths:
    wrapper: Path
    seed_policy: Path
    reflection: Path
    feedback: Path
    continuation: Path


@dataclass(frozen=True, slots=True)
class ExperimentConfig:
    root: Path
    experiment_id: str
    benchmark_repo: Path
    condition: Path
    examples: Path
    splits: Path
    run_root: Path
    prompts: PromptPaths
    reviewer: dict[str, Any]
    reflection: dict[str, Any]
    objective: dict[str, Any]
    gepa: dict[str, Any]
    finalist_evaluation: dict[str, Any]
