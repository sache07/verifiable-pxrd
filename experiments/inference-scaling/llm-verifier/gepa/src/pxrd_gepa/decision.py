from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def validate_decision(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError("decision.json missing")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError("decision.json must contain an object")
    decision = value.get("decision")
    if decision not in {"stop", "continue"}:
        raise ValueError("decision must be stop or continue")
    reason = value.get("reason")
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("reason must be a non-empty string")
    proposed = value.get("proposed_branch")
    if decision == "stop" and proposed is not None:
        raise ValueError("proposed_branch must be null when stopping")
    if proposed is not None and (not isinstance(proposed, str) or not proposed.strip()):
        raise ValueError("proposed_branch must be a non-empty string when supplied")
    return {"decision": decision, "reason": reason.strip(), "proposed_branch": proposed}


def score_decision(
    predicted: str | None,
    candidates_exact: bool,
    *,
    false_continue_credit: float = 0.0,
) -> tuple[str, float]:
    if not 0.0 <= false_continue_credit < 1.0:
        raise ValueError("false_continue_credit must be in [0, 1)")
    oracle = "stop" if candidates_exact else "continue"
    if predicted == oracle:
        return oracle, 1.0
    if predicted == "continue" and oracle == "stop":
        return oracle, false_continue_credit
    return oracle, 0.0
