from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import Example


def _path(base: Path, value: str) -> Path:
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (base / path).resolve()


def load_examples(path: Path) -> list[Example]:
    base = path.resolve().parent
    examples: list[Example] = []
    seen: set[str] = set()
    with path.open(encoding="utf-8") as stream:
        for number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            raw: dict[str, Any] = json.loads(line)
            example_id = str(raw["example_id"])
            if example_id in seen:
                raise ValueError(f"duplicate example_id at line {number}: {example_id}")
            seen.add(example_id)
            report = raw.get("rwp_report")
            examples.append(
                Example(
                    example_id=example_id,
                    problem_id=str(raw["problem_id"]),
                    formula=str(raw["formula"]),
                    wavelength=float(raw["wavelength"]),
                    pattern=_path(base, str(raw["pattern"])),
                    trace=_path(base, str(raw["trace"])),
                    final_response=_path(base, str(raw["final_response"])),
                    candidates=tuple(_path(base, str(item)) for item in raw["candidates"]),
                    reference=_path(base, str(raw["reference"])),
                    rwp_report=_path(base, str(report)) if report else None,
                )
            )
    return examples


def load_splits(path: Path) -> dict[str, set[str]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if int(raw.get("schema_version", 0)) != 1:
        raise ValueError("split schema_version must be 1")
    names = ("train", "validation", "development_test")
    splits = {name: {str(item) for item in raw.get(name, [])} for name in names}
    for left_index, left in enumerate(names):
        for right in names[left_index + 1 :]:
            overlap = splits[left] & splits[right]
            if overlap:
                raise ValueError(f"problem leakage between {left} and {right}: {sorted(overlap)}")
    return splits


def validate_dataset(examples: list[Example], splits: dict[str, set[str]]) -> dict[str, Any]:
    failures: list[str] = []
    by_problem: dict[str, list[Example]] = {}
    for example in examples:
        by_problem.setdefault(example.problem_id, []).append(example)
        for label, path in (
            ("pattern", example.pattern),
            ("trace", example.trace),
            ("final_response", example.final_response),
            ("reference", example.reference),
        ):
            if not path.is_file():
                failures.append(f"{example.example_id}: missing {label}: {path}")
        failures.extend(
            f"{example.example_id}: missing candidate: {candidate}"
            for candidate in example.candidates
            if not candidate.is_file()
        )
        if example.rwp_report is not None and not example.rwp_report.is_file():
            failures.append(f"{example.example_id}: missing Rwp report: {example.rwp_report}")
    assigned = set().union(*splits.values())
    missing_assignments = sorted(set(by_problem) - assigned)
    unknown_assignments = sorted(assigned - set(by_problem))
    if missing_assignments:
        failures.append(f"problems absent from splits: {missing_assignments}")
    if unknown_assignments:
        failures.append(f"split problems absent from examples: {unknown_assignments}")
    counts = {
        name: sum(example.problem_id in problems for example in examples)
        for name, problems in splits.items()
    }
    return {
        "valid": not failures,
        "examples": len(examples),
        "problems": len(by_problem),
        "split_examples": counts,
        "split_problems": {name: len(items) for name, items in splits.items()},
        "failures": failures,
    }


def select_split(
    examples: list[Example], splits: dict[str, set[str]], split: str
) -> list[Example]:
    if split not in splits:
        raise KeyError(split)
    return [example for example in examples if example.problem_id in splits[split]]
