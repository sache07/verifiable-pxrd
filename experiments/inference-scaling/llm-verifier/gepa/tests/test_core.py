from __future__ import annotations

import json
from pathlib import Path

import pytest

from pxrd_gepa.dataset import load_splits
from pxrd_gepa.decision import score_decision, validate_decision
from pxrd_gepa.finalists import _metrics_from_results, _repeated_selection_key
from pxrd_gepa.models import Example
from pxrd_gepa.prompting import render_reflection, render_reviewer


def test_score_decision() -> None:
    assert score_decision("stop", True) == ("stop", 1.0)
    assert score_decision("continue", True) == ("stop", 0.0)
    assert score_decision("continue", False) == ("continue", 1.0)
    assert score_decision("continue", True, false_continue_credit=0.5) == ("stop", 0.5)
    assert score_decision("stop", False, false_continue_credit=0.5) == ("continue", 0.0)


def test_false_continue_credit_is_bounded() -> None:
    with pytest.raises(ValueError, match="false_continue_credit"):
        score_decision("continue", True, false_continue_credit=1.0)


def test_finalist_metrics_distinguish_false_stops() -> None:
    rows = [
        {"decision": {"decision": "continue"}, "oracle_decision": "continue", "score": 1.0},
        {"decision": {"decision": "stop"}, "oracle_decision": "continue", "score": 0.0},
        {"decision": {"decision": "stop"}, "oracle_decision": "stop", "score": 1.0},
        {"decision": {"decision": "continue"}, "oracle_decision": "stop", "score": 0.5},
    ]
    metrics = _metrics_from_results(rows)
    assert metrics["accuracy"] == 0.5
    assert metrics["balanced_accuracy"] == 0.5
    assert metrics["false_stop_rate"] == 0.5
    assert metrics["continuation_rate"] == 0.5


def test_repeated_finalist_selection_prioritizes_false_stop_safety() -> None:
    order = ["false_stop_rate", "balanced_accuracy", "continuation_rate", "word_count"]
    safe = {
        "candidate_index": 1,
        "mean_false_stop_rate": 0.0,
        "mean_balanced_accuracy": 0.80,
        "mean_continuation_rate": 0.50,
        "word_count": 200,
    }
    riskier = {
        "candidate_index": 2,
        "mean_false_stop_rate": 0.10,
        "mean_balanced_accuracy": 0.95,
        "mean_continuation_rate": 0.30,
        "word_count": 100,
    }
    assert _repeated_selection_key(safe, order) < _repeated_selection_key(riskier, order)


def test_validate_decision(tmp_path: Path) -> None:
    path = tmp_path / "decision.json"
    path.write_text(
        json.dumps({"decision": "continue", "reason": "gap", "proposed_branch": "ordering"}),
        encoding="utf-8",
    )
    assert validate_decision(path)["decision"] == "continue"


def test_stop_requires_null_branch(tmp_path: Path) -> None:
    path = tmp_path / "decision.json"
    path.write_text(
        json.dumps({"decision": "stop", "reason": "done", "proposed_branch": "ordering"}),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="must be null"):
        validate_decision(path)


def test_continue_does_not_require_branch(tmp_path: Path) -> None:
    path = tmp_path / "decision.json"
    path.write_text(
        json.dumps({"decision": "continue", "reason": "another solve is warranted"}),
        encoding="utf-8",
    )
    assert validate_decision(path) == {
        "decision": "continue",
        "reason": "another solve is warranted",
        "proposed_branch": None,
    }


def test_split_leakage_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "splits.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "train": ["a"],
                "validation": ["a"],
                "development_test": [],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="leakage"):
        load_splits(path)


def test_checked_in_reviewer_prompt_renders(tmp_path: Path) -> None:
    project = Path(__file__).parents[1]
    example = Example(
        example_id="example-r1",
        problem_id="example",
        formula="ABO2",
        wavelength=1.5406,
        pattern=tmp_path / "pattern.csv",
        trace=tmp_path / "events.jsonl",
        final_response=tmp_path / "final.md",
        candidates=(tmp_path / "selected.cif",),
        reference=tmp_path / "reference.cif",
        rwp_report=tmp_path / "rwp.json",
    )
    staged = {
        "pattern": example.pattern,
        "trace": example.trace,
        "final_response": example.final_response,
        "candidates": list(example.candidates),
        "rwp_report": example.rwp_report,
    }
    prompt = render_reviewer(
        project / "prompts/reviewer-wrapper.md",
        (project / "prompts/seed-judge-policy.md").read_text(encoding="utf-8"),
        example,
        staged,
    )
    assert "Composition: ABO2" in prompt
    assert '"decision": "stop|continue"' in prompt
    assert "{judge_policy}" not in prompt


def test_reviewer_prompt_represents_an_empty_submission(tmp_path: Path) -> None:
    project = Path(__file__).parents[1]
    example = Example(
        example_id="example-r1",
        problem_id="example",
        formula="ABO2",
        wavelength=1.5406,
        pattern=tmp_path / "pattern.csv",
        trace=tmp_path / "events.jsonl",
        final_response=tmp_path / "final.md",
        candidates=(),
        reference=tmp_path / "reference.cif",
        rwp_report=None,
    )
    prompt = render_reviewer(
        project / "prompts/reviewer-wrapper.md",
        (project / "prompts/seed-judge-policy.md").read_text(encoding="utf-8"),
        example,
        {
            "pattern": example.pattern,
            "trace": example.trace,
            "final_response": example.final_response,
            "candidates": [],
            "rwp_report": None,
        },
    )
    assert "Submitted CIFs:\n- None submitted." in prompt


def test_checked_in_reflection_prompt_exposes_artifact_directories() -> None:
    project = Path(__file__).parents[1]
    reflective_examples = [
        {
            "Inputs": {
                "example_id": "example-r1",
                "artifact_directories": {
                    "blind_evidence": "/runs/example/evidence",
                    "judge_record": "/runs/example/judge-record",
                    "oracle_record": "/runs/example/oracle-record",
                },
            },
            "Generated Outputs": {"decision": {"decision": "stop"}},
            "Feedback": "The oracle action was continue.",
            "score": 0.0,
        }
    ]
    prompt = render_reflection(
        project / "prompts/reflection.md",
        "Stop only when the submitted result is established.",
        reflective_examples,
        450,
    )
    assert "/runs/example/evidence" in prompt
    assert "/runs/example/judge-record" in prompt
    assert "/runs/example/oracle-record" in prompt
    assert "reference CIF" in prompt
    assert "{reflective_examples}" not in prompt
