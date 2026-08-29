#!/usr/bin/env python3
"""Grade declared CIF candidates with the pXRD benchmark report matcher."""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from pathlib import Path

from pymatgen.analysis.structure_matcher import ElementComparator, StructureMatcher
from pymatgen.core import Structure

MATCHER_PARAMETERS = {
    "ltol": 0.2,
    "stol": 0.3,
    "angle_tol": 5,
    "primitive_cell": True,
    "scale": False,
    "attempt_supercell": True,
    "allow_subset": False,
}
GRADER_VERSION = "pxrd-benchmark-structurematcher-v1"


def matcher() -> StructureMatcher:
    return StructureMatcher(**MATCHER_PARAMETERS, comparator=ElementComparator())


def feasible(left: Structure, right: Structure) -> bool:
    left_vps = left.volume / len(left)
    right_vps = right.volume / len(right)
    left_shape = left.volume / math.prod(left.lattice.abc)
    right_shape = right.volume / math.prod(right.lattice.abc)
    ratio = left_vps / right_vps
    factor = (1 + MATCHER_PARAMETERS["ltol"]) ** 3
    return bool(
        all(math.isfinite(value) and value > 0 for value in (left_vps, right_vps, left_shape, right_shape, ratio))
        and ratio <= factor / right_shape
        and 1 / ratio <= factor / left_shape
    )


def candidates(workspace: Path) -> list[Path]:
    paths = [workspace / "selected.cif"] if (workspace / "selected.cif").is_file() else []
    alternatives = [path for path in workspace.glob("alternative-*.cif") if path.is_file()]
    def key(path: Path) -> tuple[int, str]:
        match = re.fullmatch(r"alternative-(\d+)\.cif", path.name)
        return (int(match.group(1)) if match else 10**9, path.name)
    return paths + sorted(alternatives, key=key)


def evaluate(problem: Path, workspace: Path, task_id: str | None = None) -> dict[str, object]:
    record = json.loads((problem / "problem.json").read_text(encoding="utf-8"))
    problem_id = str(record["problem_id"])
    if task_id and task_id != problem_id:
        raise ValueError(f"task id {task_id!r} does not match problem {problem_id!r}")
    reference = Structure.from_file(problem / record["solution"]["path"], primitive=False)
    active = matcher()
    paths = candidates(workspace)
    parsed: list[str] = []
    matched: list[str] = []
    rms: dict[str, dict[str, float]] = {}
    diagnostics: list[str] = []
    for path in paths:
        try:
            candidate = Structure.from_file(path, primitive=False)
            parsed.append(path.name)
            if feasible(reference, candidate) and active.fit(reference, candidate, symmetric=True):
                matched.append(path.name)
                distances = active.get_rms_dist(reference, candidate)
                if distances is not None:
                    rms[path.name] = {"rms": float(distances[0]), "max": float(distances[1])}
        except Exception as error:
            diagnostics.append(f"could not parse {path.name}: {type(error).__name__}: {error}")
    if not paths:
        diagnostics.append("no selected.cif or alternative-<n>.cif was submitted")
    elif parsed and not matched:
        diagnostics.append("no declared candidate matched the hidden reference")
    if matched:
        diagnostics.append("at least one declared candidate matched the hidden reference")
    return {
        "schema_version": "1",
        "task_id": problem_id,
        "success": bool(matched),
        "reward": 1.0 if matched else 0.0,
        "metrics": {
            "candidate_count": len(paths),
            "parseable_candidate_count": len(parsed),
            "exact_match_count": len(matched),
            "matched_candidates": matched,
            "matched_displacements": rms,
            "matcher": {**MATCHER_PARAMETERS, "comparator": "ElementComparator", "symmetric": True},
        },
        "diagnostics": diagnostics,
        "artifacts": parsed,
        "grader_version": GRADER_VERSION,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--problem", type=Path)
    parser.add_argument("--workspace", type=Path, default=os.environ.get("CHARLEARN_WORKSPACE"))
    parser.add_argument("--output", type=Path, default=os.environ.get("CHARLEARN_VERIFIER_OUTPUT"))
    args = parser.parse_args()
    if args.problem is None:
        record_path = os.environ.get("CHARLEARN_TASK_RECORD")
        if not record_path:
            parser.error("--problem or CHARLEARN_TASK_RECORD is required")
        task_record = json.loads(Path(record_path).read_text(encoding="utf-8"))
        value = (task_record.get("metadata") or {}).get("problem_dir")
        if not value:
            parser.error("task metadata.problem_dir is required when --problem is omitted")
        args.problem = Path(value)
    if args.workspace is None:
        parser.error("--workspace or CHARLEARN_WORKSPACE is required")
    result = evaluate(args.problem.resolve(), args.workspace.resolve(), os.environ.get("CHARLEARN_TASK_ID"))
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
