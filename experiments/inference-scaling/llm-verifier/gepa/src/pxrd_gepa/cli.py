from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .benchmark import import_vpbench
from .config import load_config
from .dataset import load_examples, load_splits, validate_dataset
from .driver import optimization_plan, optimize
from .finalists import evaluate_finalists
from .prompting import render_reviewer


def _doctor(config_path: Path) -> dict[str, Any]:
    config = load_config(config_path)
    failures: list[str] = []
    required = [
        config.benchmark_repo,
        config.condition,
        config.prompts.wrapper,
        config.prompts.seed_policy,
        config.prompts.reflection,
        config.prompts.feedback,
        config.prompts.continuation,
    ]
    failures.extend(f"missing required path: {path}" for path in required if not path.exists())
    auth = None
    condition_health = None
    if not failures:
        modules = import_vpbench(config)
        condition_health = modules["run"].doctor(config.condition)
        base = modules["condition"].load_condition(config.condition)
        unused_prompt_failure = f"missing prompt: {base.prompt}"
        condition_failures = [
            failure
            for failure in condition_health["failures"]
            if failure != unused_prompt_failure
        ]
        condition_health["source_prompt_used"] = False
        condition_health["reviewer_prompt_override"] = str(config.prompts.wrapper)
        condition_health["failures"] = condition_failures
        condition_health["valid"] = not condition_failures
        failures.extend(condition_failures)
        auth = condition_health.get("auth")
    return {
        "experiment": config.experiment_id,
        "valid": not failures,
        "failures": failures,
        "condition": condition_health,
        "auth": auth,
        "data_manifest_present": config.examples.is_file(),
        "splits_present": config.splits.is_file(),
    }


def _validate(config_path: Path) -> dict[str, Any]:
    config = load_config(config_path)
    return validate_dataset(load_examples(config.examples), load_splits(config.splits))


def _render(config_path: Path, example_id: str) -> str:
    config = load_config(config_path)
    examples = {example.example_id: example for example in load_examples(config.examples)}
    example = examples[example_id]
    staged = {
        "pattern": example.pattern,
        "trace": example.trace,
        "final_response": example.final_response,
        "candidates": list(example.candidates),
        "rwp_report": example.rwp_report,
    }
    policy = config.prompts.seed_policy.read_text(encoding="utf-8")
    return render_reviewer(config.prompts.wrapper, policy, example, staged)


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="pxrd-gepa")
    commands = root.add_subparsers(dest="command", required=True)
    for name in ("doctor", "validate-data"):
        command = commands.add_parser(name)
        command.add_argument("--config", type=Path, required=True)
    render = commands.add_parser("render")
    render.add_argument("--config", type=Path, required=True)
    render.add_argument("--example", required=True)
    optimize_command = commands.add_parser("optimize")
    optimize_command.add_argument("--config", type=Path, required=True)
    optimize_command.add_argument("--dry-run", action="store_true")
    optimize_command.add_argument("--confirm-run", action="store_true")
    finalists = commands.add_parser("evaluate-finalists")
    finalists.add_argument("--config", type=Path, required=True)
    finalists.add_argument("--optimization-root", type=Path, required=True)
    finalists.add_argument("--confirm-run", action="store_true")
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "doctor":
            result = _doctor(args.config)
        elif args.command == "validate-data":
            result = _validate(args.config)
        elif args.command == "render":
            print(_render(args.config, args.example), end="")
            return 0
        elif args.command == "optimize":
            if args.dry_run:
                result = optimization_plan(args.config)
            else:
                if not args.confirm_run:
                    raise RuntimeError(
                        "optimization launches paid agent work; pass --confirm-run after reviewing prompts"
                    )
                result = optimize(args.config)
        elif args.command == "evaluate-finalists":
            if not args.confirm_run:
                raise RuntimeError(
                    "finalist evaluation launches paid agent work; pass --confirm-run"
                )
            result = evaluate_finalists(args.config, args.optimization_root)
        else:
            raise AssertionError(args.command)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result.get("valid", True) else 1
    except Exception as error:
        print(json.dumps({"error": f"{type(error).__name__}: {error}"}, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
