#!/usr/bin/env python3
"""Build portable GEPA examples from a curriculum and normalized first-pass bundle."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def relative(path: Path, output: Path) -> str:
    return os.path.relpath(path.resolve(), output.resolve().parent)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--curriculum", type=Path, required=True)
    result.add_argument("--source", type=Path, required=True)
    result.add_argument("--output", type=Path, required=True)
    result.add_argument("--wavelength", type=float, default=1.5406)
    return result


def main() -> int:
    args = parser().parse_args()
    curriculum_path = args.curriculum.resolve()
    curriculum_root = curriculum_path.parent
    source = args.source.resolve()
    output = args.output.resolve()
    curriculum = load(curriculum_path)
    bundle = load(source / "bundle.json")
    by_problem = {
        str(record.get("problem_id", record.get("case_id"))): record
        for record in bundle["cases"]
    }
    rows = []
    for problem in sorted(curriculum["problems"], key=lambda item: int(item["order"])):
        problem_id = str(problem["problem_id"])
        if problem_id not in by_problem:
            raise ValueError(f"source bundle has no attempt for {problem_id}")
        attempt = source / "attempts" / problem_id
        candidates = [attempt / "submission/selected.cif"]
        candidates.extend(sorted((attempt / "submission").glob("alternative-*.cif")))
        candidates = [path for path in candidates if path.is_file()]
        trace = attempt / "codex-events.jsonl.gz"
        if not trace.is_file():
            trace = attempt / "codex-events.jsonl"
        final_response = attempt / "final-answer.md"
        if not final_response.is_file():
            final_response = output.parent / "no-final-response.md"
        row = {
            "example_id": f"{problem_id}-r1",
            "problem_id": problem_id,
            "formula": str(problem["metadata"]["formula"]),
            "wavelength": args.wavelength,
            "pattern": relative(
                curriculum_root / "problems" / problem_id / "problem_input/pattern.csv",
                output,
            ),
            "trace": relative(trace, output),
            "final_response": relative(final_response, output),
            "candidates": [relative(path, output) for path in candidates],
            "reference": relative(
                curriculum_root / "problems" / problem_id / "solution/reference.cif",
                output,
            ),
        }
        rows.append(row)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        "".join(json.dumps(row, separators=(",", ":")) + "\n" for row in rows),
        encoding="utf-8",
    )
    print(json.dumps({"examples": len(rows), "output": str(output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
