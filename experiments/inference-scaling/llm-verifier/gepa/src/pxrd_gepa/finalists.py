from __future__ import annotations

import json
import math
import shutil
from pathlib import Path
from statistics import mean
from typing import Any

from gepa.core.result import GEPAResult

from .benchmark import evaluate_example
from .config import load_config
from .dataset import load_examples, load_splits, select_split
from .models import Example, ExperimentConfig
from .runner import CodexRuntime


def _score_at(scores: dict[Any, float], index: int) -> float:
    value = scores.get(index, scores.get(str(index)))
    return float("nan") if value is None else float(value)


def _metrics_from_scores(
    scores: dict[Any, float],
    examples: list[Example],
    exact_by_id: dict[str, bool],
    false_continue_credit: float,
) -> dict[str, Any]:
    true_continue = false_stop = true_stop = false_continue = invalid = 0
    for index, example in enumerate(examples):
        score = _score_at(scores, index)
        exact = exact_by_id[example.example_id]
        if not math.isfinite(score):
            invalid += 1
        elif exact and math.isclose(score, 1.0):
            true_stop += 1
        elif exact and math.isclose(score, false_continue_credit):
            false_continue += 1
        elif not exact and math.isclose(score, 1.0):
            true_continue += 1
        elif not exact and math.isclose(score, 0.0):
            false_stop += 1
        else:
            invalid += 1
    continue_total = sum(not exact_by_id[example.example_id] for example in examples)
    stop_total = sum(exact_by_id[example.example_id] for example in examples)
    continue_recall = true_continue / continue_total if continue_total else 1.0
    stop_recall = true_stop / stop_total if stop_total else 1.0
    count = len(examples)
    return {
        "correct": true_continue + true_stop,
        "count": count,
        "accuracy": (true_continue + true_stop) / count,
        "balanced_accuracy": (continue_recall + stop_recall) / 2,
        "continue_recall": continue_recall,
        "stop_recall": stop_recall,
        "false_stop_rate": false_stop / continue_total if continue_total else 0.0,
        "continuation_rate": (true_continue + false_continue) / count,
        "true_continue": true_continue,
        "false_stop": false_stop,
        "true_stop": true_stop,
        "false_continue": false_continue,
        "invalid": invalid,
    }


def _metrics_from_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    true_continue = false_stop = true_stop = false_continue = invalid = 0
    for result in results:
        predicted = (result.get("decision") or {}).get("decision")
        oracle = result["oracle_decision"]
        if predicted not in {"stop", "continue"}:
            invalid += 1
        elif predicted == "continue" and oracle == "continue":
            true_continue += 1
        elif predicted == "stop" and oracle == "continue":
            false_stop += 1
        elif predicted == "stop" and oracle == "stop":
            true_stop += 1
        else:
            false_continue += 1
    continue_total = sum(result["oracle_decision"] == "continue" for result in results)
    stop_total = sum(result["oracle_decision"] == "stop" for result in results)
    count = len(results)
    continue_recall = true_continue / continue_total if continue_total else 1.0
    stop_recall = true_stop / stop_total if stop_total else 1.0
    return {
        "correct": true_continue + true_stop,
        "count": count,
        "accuracy": (true_continue + true_stop) / count,
        "balanced_accuracy": (continue_recall + stop_recall) / 2,
        "continue_recall": continue_recall,
        "stop_recall": stop_recall,
        "false_stop_rate": false_stop / continue_total if continue_total else 0.0,
        "continuation_rate": (true_continue + false_continue) / count,
        "mean_utility": mean(float(result["score"]) for result in results),
        "true_continue": true_continue,
        "false_stop": false_stop,
        "true_stop": true_stop,
        "false_continue": false_continue,
        "invalid": invalid,
    }


def _selection_key(record: dict[str, Any], order: list[str]) -> tuple[Any, ...]:
    key: list[Any] = []
    for field in order:
        value = record[field]
        key.append(value if field in {"false_stop_rate", "continuation_rate", "word_count"} else -value)
    key.append(record["candidate_index"])
    return tuple(key)


def _repeated_selection_key(record: dict[str, Any], order: list[str]) -> tuple[Any, ...]:
    key: list[Any] = []
    for field in order:
        value = record[field] if field == "word_count" else record[f"mean_{field}"]
        key.append(value if field in {"false_stop_rate", "continuation_rate", "word_count"} else -value)
    key.append(record["candidate_index"])
    return tuple(key)


def _aggregate_repeats(
    evaluations: list[dict[str, Any]],
    indices: list[int],
    word_counts: dict[int, int],
) -> list[dict[str, Any]]:
    fields = (
        "accuracy",
        "balanced_accuracy",
        "continue_recall",
        "stop_recall",
        "false_stop_rate",
        "continuation_rate",
        "mean_utility",
    )
    aggregate = []
    for index in indices:
        rows = [row["metrics"] for row in evaluations if row["candidate_index"] == index]
        aggregate.append(
            {
                "candidate_index": index,
                "repeats": len(rows),
                "word_count": word_counts[index],
                **{f"mean_{field}": mean(float(row[field]) for row in rows) for field in fields},
            }
        )
    return aggregate


def validation_ranking(
    config: ExperimentConfig,
    result: GEPAResult[Any, Any],
    validation: list[Example],
) -> list[dict[str, Any]]:
    exact_by_id = {
        example.example_id: bool(evaluate_example(config, example)["candidates_exact"])
        for example in validation
    }
    credit = float(config.objective["false_continue_credit"])
    records = []
    for index, (candidate, scores) in enumerate(
        zip(result.candidates, result.val_subscores, strict=True)
    ):
        policy = candidate["judge_policy"]
        record = _metrics_from_scores(scores, validation, exact_by_id, credit)
        record.update(
            {
                "candidate_index": index,
                "validation_utility": float(result.val_aggregate_scores[index]),
                "word_count": len(policy.split()),
            }
        )
        records.append(record)
    order = [str(item) for item in config.finalist_evaluation["selection_order"]]
    return sorted(records, key=lambda record: _selection_key(record, order))


def evaluate_finalists(config_path: Path, optimization_root: Path) -> dict[str, Any]:
    config = load_config(config_path)
    optimization_root = optimization_root.resolve()
    result_path = optimization_root / "result.json"
    if not result_path.is_file():
        raise FileNotFoundError(f"optimization result is missing: {result_path}")
    result = GEPAResult.from_dict(json.loads(result_path.read_text(encoding="utf-8")))
    examples = load_examples(config.examples)
    splits = load_splits(config.splits)
    validation = select_split(examples, splits, "validation")
    development = select_split(examples, splits, "development_test")
    ranking = validation_ranking(config, result, validation)
    requested = int(config.finalist_evaluation["candidate_count"])
    nonseed = [record for record in ranking if record["candidate_index"] != 0][:requested]
    indices = [0, *(record["candidate_index"] for record in nonseed)]
    # If GEPA found fewer than requested nonseed candidates, evaluate everything available once.
    indices = list(dict.fromkeys(indices))
    output = optimization_root / "finalist-evaluation"
    if output.exists():
        raise FileExistsError(output)
    output.mkdir()
    policies = output / "policies"
    policies.mkdir()
    word_counts: dict[int, int] = {}
    for index in indices:
        word_counts[index] = len(result.candidates[index]["judge_policy"].split())
        (policies / f"candidate-{index:03d}.md").write_text(
            result.candidates[index]["judge_policy"].rstrip() + "\n", encoding="utf-8"
        )
    runtime = CodexRuntime(config, output / "agent-runs")

    # GEPA's validation scores are single stochastic rollouts. Re-evaluate a small
    # validation-only shortlist before freezing a policy; never use development
    # outcomes to choose among policies.
    validation_repeats = int(config.finalist_evaluation["validation_repeats"])
    validation_evaluations = []
    for index in indices:
        policy = result.candidates[index]["judge_policy"]
        for repeat in range(1, validation_repeats + 1):
            results = runtime.review_batch(validation, policy)
            decisions = [
                {
                    "example_id": item["example_id"],
                    "decision": item["decision"],
                    "oracle_decision": item["oracle_decision"],
                    "decision_correct": item["decision_correct"],
                    "score": item["score"],
                    "run_root": item["run_root"],
                }
                for item in results
            ]
            validation_evaluations.append(
                {
                    "candidate_index": index,
                    "repeat": repeat,
                    "metrics": _metrics_from_results(results),
                    "decisions": decisions,
                }
            )
            (output / "validation-progress.json").write_text(
                json.dumps(validation_evaluations, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
    validation_aggregate = _aggregate_repeats(validation_evaluations, indices, word_counts)
    selection_order = [str(item) for item in config.finalist_evaluation["selection_order"]]
    selected = min(
        validation_aggregate,
        key=lambda record: _repeated_selection_key(record, selection_order),
    )
    selected_index = int(selected["candidate_index"])
    shutil.copy2(
        policies / f"candidate-{selected_index:03d}.md",
        output / "validation-selected-policy.md",
    )

    development_indices = list(dict.fromkeys([0, selected_index]))
    development_repeats = int(config.finalist_evaluation["development_repeats"])
    development_evaluations = []
    for index in development_indices:
        policy = result.candidates[index]["judge_policy"]
        for repeat in range(1, development_repeats + 1):
            results = runtime.review_batch(development, policy)
            decisions = [
                {
                    "example_id": item["example_id"],
                    "decision": item["decision"],
                    "oracle_decision": item["oracle_decision"],
                    "decision_correct": item["decision_correct"],
                    "score": item["score"],
                    "run_root": item["run_root"],
                }
                for item in results
            ]
            development_evaluations.append(
                {
                    "candidate_index": index,
                    "repeat": repeat,
                    "metrics": _metrics_from_results(results),
                    "decisions": decisions,
                }
            )
            (output / "development-progress.json").write_text(
                json.dumps(development_evaluations, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
    development_aggregate = _aggregate_repeats(
        development_evaluations,
        development_indices,
        word_counts,
    )
    payload = {
        "schema_version": 1,
        "optimization_root": str(optimization_root),
        "validation_selected_candidate": selected_index,
        "finalist_candidate_indices": indices,
        "validation_ranking": ranking,
        "validation_repeats": validation_repeats,
        "validation_evaluations": validation_evaluations,
        "validation_aggregate": validation_aggregate,
        "development_candidate_indices": development_indices,
        "development_repeats": development_repeats,
        "development_evaluations": development_evaluations,
        "development_aggregate": development_aggregate,
        "selection_note": (
            "Finalists were freshly re-evaluated and the policy was selected using validation only. "
            "It was frozen before development evaluation; development outcomes did not alter selection."
        ),
    }
    (output / "summary.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return {
        "output": str(output),
        "validation_selected_candidate": selected_index,
        "finalist_candidate_indices": indices,
        "validation_aggregate": validation_aggregate,
        "development_aggregate": development_aggregate,
    }
