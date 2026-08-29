from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from gepa.core.adapter import EvaluationBatch

from .models import Example
from .runner import CodexRuntime


class PXRDJudgeAdapter:
    # GEPA checks this optional protocol attribute before consulting the custom
    # candidate proposer supplied by the driver.
    propose_new_texts = None

    def __init__(self, runtime: CodexRuntime):
        self.runtime = runtime

    def evaluate(
        self,
        batch: list[Example],
        candidate: dict[str, str],
        capture_traces: bool = False,
    ) -> EvaluationBatch[dict[str, Any], dict[str, Any]]:
        policy = candidate["judge_policy"]
        results = self.runtime.review_batch(batch, policy)
        outputs = [
            {
                "example_id": item["example_id"],
                "decision": item["decision"],
                "oracle_decision": item["oracle_decision"],
                "run_root": item["run_root"],
            }
            for item in results
        ]
        scores = [float(item["score"]) for item in results]
        trajectories = results if capture_traces else None
        return EvaluationBatch(
            outputs=outputs,
            scores=scores,
            trajectories=trajectories,
            num_metric_calls=len(batch),
        )

    def make_reflective_dataset(
        self,
        candidate: dict[str, str],
        eval_batch: EvaluationBatch[dict[str, Any], dict[str, Any]],
        components_to_update: list[str],
    ) -> Mapping[str, Sequence[Mapping[str, Any]]]:
        if eval_batch.trajectories is None:
            raise ValueError("reflective evaluation did not capture trajectories")
        records = []
        for trajectory in eval_batch.trajectories:
            records.append(
                {
                    "Inputs": {
                        "example_id": trajectory["example_id"],
                        "problem_id": trajectory["problem_id"],
                        "artifact_directories": trajectory["reflection_artifacts"],
                    },
                    "Generated Outputs": {
                        "decision": trajectory["decision"],
                        "decision_error": trajectory["decision_error"],
                    },
                    "Feedback": trajectory["feedback"],
                    "score": trajectory["score"],
                }
            )
        return {component: records for component in components_to_update}


class CodexPolicyProposer:
    def __init__(self, runtime: CodexRuntime):
        self.runtime = runtime

    def __call__(
        self,
        candidate: dict[str, str],
        reflective_dataset: Mapping[str, Sequence[Mapping[str, Any]]],
        components_to_update: list[str],
    ) -> dict[str, str]:
        if components_to_update != ["judge_policy"]:
            raise ValueError(f"unexpected mutable components: {components_to_update}")
        return {
            "judge_policy": self.runtime.reflect(
                candidate["judge_policy"],
                reflective_dataset["judge_policy"],
            )
        }
