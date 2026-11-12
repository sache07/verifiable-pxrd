"""Primary exact-recovery metric used by pXRD-100 and pXRD-OOD."""

from __future__ import annotations

import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from pymatgen.analysis.structure_matcher import ElementComparator, StructureMatcher
from pymatgen.core import Structure

MATCHER_PARAMETERS: dict[str, Any] = {
    "ltol": 0.2,
    "stol": 0.3,
    "angle_tol": 5,
    "primitive_cell": True,
    "scale": False,
    "attempt_supercell": True,
    "allow_subset": False,
}
GRADER_VERSION = "pxrd-benchmark-structurematcher"


def exact_outcomes(result: Mapping[str, Any]) -> tuple[bool, bool]:
    """Read primary and candidate-set outcomes from a verifier result."""
    matched = (result.get("metrics") or {}).get("matched_candidates")
    legacy = bool(result.get("exact_success", False))
    selected_exact = result.get("selected_exact")
    candidates_exact = result.get("candidates_exact")
    if selected_exact is None:
        selected_exact = "selected.cif" in matched if isinstance(matched, list) else legacy
    if candidates_exact is None:
        candidates_exact = bool(matched) if isinstance(matched, list) else legacy
    return bool(selected_exact), bool(candidates_exact)


def matcher() -> StructureMatcher:
    return StructureMatcher(**MATCHER_PARAMETERS, comparator=ElementComparator())


def declared_candidates(workspace: Path) -> list[Path]:
    paths = [workspace / "selected.cif"] if (workspace / "selected.cif").is_file() else []

    def key(path: Path) -> tuple[int, str]:
        match = re.fullmatch(r"alternative-(\d+)\.cif", path.name)
        return (int(match.group(1)) if match else 10**9, path.name)

    return paths + sorted(workspace.glob("alternative-*.cif"), key=key)


def evaluate_candidates(
    reference_path: Path,
    paths: list[Path],
    task_id: str,
) -> dict[str, Any]:
    reference = Structure.from_file(reference_path, primitive=False)
    active = matcher()
    parsed: list[str] = []
    matched: list[str] = []
    rms: dict[str, dict[str, float]] = {}
    diagnostics: list[str] = []
    for path in paths:
        try:
            candidate = Structure.from_file(path, primitive=False)
            parsed.append(path.name)
            if active.fit(reference, candidate, symmetric=True):
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
    selected_exact = "selected.cif" in matched
    candidates_exact = bool(matched)
    if selected_exact:
        diagnostics.append("selected.cif matched the hidden reference")
    elif candidates_exact:
        diagnostics.append("an alternative matched, but selected.cif did not")
    return {
        "schema_version": "1",
        "task_id": task_id,
        "selected_exact": selected_exact,
        "candidates_exact": candidates_exact,
        "metrics": {
            "candidate_count": len(paths),
            "parseable_candidate_count": len(parsed),
            "exact_match_count": len(matched),
            "matched_candidates": matched,
            "matched_displacements": rms,
            "matcher": {
                **MATCHER_PARAMETERS,
                "comparator": "ElementComparator",
                "symmetric": True,
            },
        },
        "diagnostics": diagnostics,
        "artifacts": parsed,
        "grader_version": GRADER_VERSION,
    }


def evaluate_workspace(reference_path: Path, workspace: Path, task_id: str) -> dict[str, Any]:
    return evaluate_candidates(reference_path, declared_candidates(workspace), task_id)


def evaluate_selected(reference_path: Path, workspace: Path, task_id: str) -> dict[str, Any]:
    selected = workspace / "selected.cif"
    return evaluate_candidates(reference_path, [selected] if selected.is_file() else [], task_id)
