#!/usr/bin/env python3
"""Build a blind reviewer manifest from one frozen inference-scaling replicate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument("--panel", type=Path, required=True)
    result.add_argument("--source", type=Path, required=True)
    result.add_argument("--replicate", type=int, required=True)
    result.add_argument("--output", type=Path, required=True)
    return result


def main() -> int:
    args = parser().parse_args()
    panel_path = args.panel.resolve()
    panel_root = panel_path.parent
    source = args.source.resolve()
    manifest = read_json(panel_path)
    rows = []
    for problem in sorted(manifest["problems"], key=lambda item: int(item["order"])):
        problem_id = str(problem["problem_id"])
        attempt = source / "attempts" / f"{problem_id}-r{args.replicate}"
        final_response = attempt / "run/final-answer.md"
        if not final_response.is_file():
            final_response = args.output.resolve().parent / "no-final-response.md"
        candidates = [attempt / "workspace/selected.cif"]
        candidates.extend(sorted((attempt / "workspace").glob("alternative-*.cif")))
        candidates = [path for path in candidates if path.is_file()]
        row = {
            "example_id": f"{problem_id}-r{args.replicate}",
            "problem_id": problem_id,
            "formula": str(problem["metadata"]["formula"]),
            "wavelength": 1.5406,
            "pattern": str(
                panel_root / "problems" / problem_id / problem["problem_input"]["files"][0]["path"]
            ),
            "trace": str(attempt / "run/codex-events.jsonl"),
            "final_response": str(final_response),
            "candidates": [str(path) for path in candidates],
            "reference": str(
                panel_root / "problems" / problem_id / problem["solution"]["path"]
            ),
        }
        rows.append(row)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(row, separators=(",", ":")) + "\n" for row in rows),
        encoding="utf-8",
    )
    print(json.dumps({"output": str(args.output), "examples": len(rows)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
