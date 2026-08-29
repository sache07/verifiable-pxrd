from __future__ import annotations

import importlib
import json
import sys
import warnings
from pathlib import Path
from typing import Any

from pymatgen.core import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

from .models import Example, ExperimentConfig


def import_vpbench(config: ExperimentConfig) -> dict[str, Any]:
    source = config.benchmark_repo / "src"
    if not source.is_dir():
        raise FileNotFoundError(f"verifiable-pxrd source directory is missing: {source}")
    if str(source) not in sys.path:
        sys.path.insert(0, str(source))
    return {
        "condition": importlib.import_module("verifiable_pxrd.condition"),
        "coverage": importlib.import_module("verifiable_pxrd.coverage"),
        "matching": importlib.import_module("verifiable_pxrd.matching"),
        "run": importlib.import_module("verifiable_pxrd.run"),
    }

def evaluate_example(config: ExperimentConfig, example: Example) -> dict[str, Any]:
    modules = import_vpbench(config)
    return modules["matching"].evaluate_candidates(
        example.reference,
        list(example.candidates),
        example.problem_id,
    )


def _structure_summary(path: Path) -> dict[str, Any]:
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            structure = Structure.from_file(path, primitive=False)
        try:
            symmetry = SpacegroupAnalyzer(structure, symprec=0.1).get_space_group_symbol()
        except Exception:
            symmetry = None
        mixed_sites = sum(len(site.species) > 1 for site in structure)
        partial_sites = sum(abs(float(sum(site.species.values())) - 1.0) > 1e-6 for site in structure)
        return {
            "path": path.name,
            "formula": structure.composition.reduced_formula,
            "sites": len(structure),
            "volume": float(structure.volume),
            "volume_per_site": float(structure.volume / len(structure)),
            "density": float(structure.density),
            "inferred_space_group": symmetry,
            "mixed_occupancy_sites": mixed_sites,
            "nonunit_occupancy_sites": partial_sites,
        }
    except Exception as error:
        return {"path": path.name, "error": f"{type(error).__name__}: {error}"}


def structural_diagnostics(example: Example, verifier: dict[str, Any]) -> dict[str, Any]:
    matched = set((verifier.get("metrics") or {}).get("matched_candidates", []))
    candidates = []
    for candidate in example.candidates:
        summary = _structure_summary(candidate)
        summary["matcher_exact"] = candidate.name in matched
        candidates.append(summary)
    return {
        "reference": _structure_summary(example.reference),
        "candidates": candidates,
    }


def rwp_summary(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {"available": False}
    try:
        report = json.loads(path.read_text(encoding="utf-8"))
    except Exception as error:
        return {"available": False, "error": f"{type(error).__name__}: {error}"}
    results = []
    for item in report.get("results", []):
        results.append(
            {
                key: item.get(key)
                for key in ("candidate", "status", "rwp_percent", "structure_group", "error")
                if item.get(key) is not None
            }
        )
    return {
        "available": True,
        "protocol": (report.get("protocol") or {}).get("id"),
        "results": results,
    }
