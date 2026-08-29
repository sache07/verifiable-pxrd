from __future__ import annotations

import importlib.util
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
EVALUATOR_PATH = REPOSITORY_ROOT / "baselines" / "evaluate.py"
SPEC = importlib.util.spec_from_file_location("baseline_evaluator", EVALUATOR_PATH)
assert SPEC is not None and SPEC.loader is not None
EVALUATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EVALUATOR)


def test_structural_summary_rolls_up_dynamic_panels_and_streams() -> None:
    cases = [
        {
            "panel": "topology-novel",
            "stream": "crystal-search",
            "best_of_1_structure_match": False,
            "best_of_1_formula_match": True,
            "best_of_k_structure_match": True,
            "best_of_k_formula_match": True,
        },
        {
            "panel": "topology-novel",
            "stream": "wyckoff-enumeration",
            "best_of_1_structure_match": False,
            "best_of_1_formula_match": False,
            "best_of_k_structure_match": False,
            "best_of_k_formula_match": True,
        },
    ]
    candidates = [
        {"status": "generated", "structure_valid": True},
        {"status": "invalid", "structure_valid": False},
    ]
    summary = EVALUATOR.summarize(cases, candidates, 8)
    assert summary["panels"]["topology-novel"]["case_count"] == 2
    assert summary["streams"]["crystal-search"]["best_of_k_structure_match_count"] == 1
