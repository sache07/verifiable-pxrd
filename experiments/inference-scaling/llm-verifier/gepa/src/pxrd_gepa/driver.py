from __future__ import annotations

import datetime as dt
import json
import shutil
from pathlib import Path
from typing import Any

import gepa

from .adapter import CodexPolicyProposer, PXRDJudgeAdapter
from .config import load_config
from .dataset import load_examples, load_splits, select_split, validate_dataset
from .runner import CodexRuntime


def optimization_plan(config_path: Path) -> dict[str, Any]:
    config = load_config(config_path)
    examples = load_examples(config.examples)
    splits = load_splits(config.splits)
    validation = validate_dataset(examples, splits)
    return {
        "experiment": config.experiment_id,
        "valid_data": validation["valid"],
        "data": validation,
        "model": config.reviewer["model"],
        "reasoning_effort": config.reviewer["reasoning_effort"],
        "parallel": config.reviewer["parallel"],
        "objective": config.objective,
        "gepa": config.gepa,
        "mutable_components": ["judge_policy"],
        "optimization_will_launch_agents": True,
    }


def optimize(config_path: Path) -> dict[str, Any]:
    config = load_config(config_path)
    examples = load_examples(config.examples)
    splits = load_splits(config.splits)
    validation = validate_dataset(examples, splits)
    if not validation["valid"]:
        raise RuntimeError("dataset validation failed: " + "; ".join(validation["failures"]))
    train = select_split(examples, splits, "train")
    val = select_split(examples, splits, "validation")
    if not train or not val:
        raise ValueError("GEPA requires non-empty train and validation splits")
    stamp = dt.datetime.now(dt.UTC).strftime("%Y%m%dT%H%M%SZ")
    run_root = config.run_root / f"{config.experiment_id}-{stamp}"
    if run_root.exists():
        raise FileExistsError(run_root)
    run_root.mkdir(parents=True)
    contract = run_root / "contract"
    contract.mkdir()
    shutil.copy2(config_path, contract / "experiment.toml")
    shutil.copy2(config.examples, contract / "examples.jsonl")
    shutil.copy2(config.splits, contract / "splits.json")
    shutil.copytree(config.root / "prompts", contract / "prompts")
    runtime = CodexRuntime(config, run_root / "agent-runs")
    adapter = PXRDJudgeAdapter(runtime)
    proposer = CodexPolicyProposer(runtime)
    settings = config.gepa
    result = gepa.optimize(
        seed_candidate={
            "judge_policy": config.prompts.seed_policy.read_text(encoding="utf-8").strip()
        },
        trainset=train,
        valset=val,
        adapter=adapter,
        reflection_lm=runtime.text_lm,
        custom_candidate_proposer=proposer,
        candidate_selection_strategy=str(settings["candidate_selection_strategy"]),
        frontier_type=str(settings["frontier_type"]),
        skip_perfect_score=bool(settings["skip_perfect_score"]),
        batch_sampler=str(settings["batch_sampler"]),
        reflection_minibatch_size=int(settings["reflection_minibatch_size"]),
        use_merge=bool(settings["use_merge"]),
        max_merge_invocations=int(settings["max_merge_invocations"]),
        max_metric_calls=int(settings["max_metric_calls"]),
        run_dir=str(run_root / "gepa-state"),
        cache_evaluation=bool(settings["cache_evaluation"]),
        seed=int(settings["seed"]),
        val_evaluation_policy=str(settings["val_evaluation_policy"]),
        acceptance_criterion=str(settings["acceptance_criterion"]),
        raise_on_exception=False,
    )
    payload = result.to_dict()
    (run_root / "result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    policies = run_root / "candidate-policies"
    policies.mkdir()
    for index, candidate in enumerate(result.candidates):
        (policies / f"candidate-{index:03d}.md").write_text(
            candidate["judge_policy"].rstrip() + "\n", encoding="utf-8"
        )
    (run_root / "best-policy.md").write_text(
        result.best_candidate["judge_policy"].rstrip() + "\n", encoding="utf-8"
    )
    return {
        "run_root": str(run_root),
        "best_candidate": result.best_idx,
        "best_validation_score": result.val_aggregate_scores[result.best_idx],
        "candidates": result.num_candidates,
        "metric_calls": result.total_metric_calls,
    }
