from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import Example


def render_reviewer(wrapper: Path, policy: str, example: Example, staged: dict[str, Path]) -> str:
    candidates = "\n".join(f"- {path}" for path in staged["candidates"])
    if not candidates:
        candidates = "- None submitted."
    report = staged.get("rwp_report")
    values = {
        "formula": example.formula,
        "pattern_path": str(staged["pattern"]),
        "wavelength": f"{example.wavelength} angstrom",
        "trace_path": str(staged["trace"]),
        "final_response_path": str(staged["final_response"]),
        "submitted_cifs": candidates,
        "rwp_report_path": str(report) if report else "No comparable-fit report was available.",
        "judge_policy": policy.strip(),
    }
    text = wrapper.read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{" + key + "}", value)
    unresolved = [key for key in values if "{" + key + "}" in text]
    if unresolved:
        raise ValueError(f"unresolved reviewer prompt fields: {unresolved}")
    return text.rstrip() + "\n"


def render_reflection(
    template: Path,
    current_policy: str,
    reflective_examples: Any,
    max_policy_words: int,
) -> str:
    values = {
        "current_policy": current_policy.strip(),
        "reflective_examples": json.dumps(reflective_examples, indent=2, sort_keys=True),
        "max_policy_words": str(max_policy_words),
    }
    text = template.read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{" + key + "}", value)
    return text.rstrip() + "\n"


def render_feedback(template: Path, values: dict[str, Any]) -> str:
    text = template.read_text(encoding="utf-8")
    for key, value in values.items():
        rendered = value if isinstance(value, str) else json.dumps(value, indent=2, sort_keys=True)
        text = text.replace("{" + key + "}", rendered)
    return text.rstrip() + "\n"
