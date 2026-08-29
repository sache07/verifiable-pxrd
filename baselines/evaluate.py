"""Evaluate deCIFer, PXRDGen, or DiffractGPT corpus generations.

Use the same pinned Pymatgen environment as the Crystalyze evaluation::

    .runs/envs/crystalyze-runtime/bin/python baselines/evaluate.py \
        decifer .runs/baselines/outputs/pxrd-100/decifer/<run-id>
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
import multiprocessing
import warnings
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np
from pymatgen.core import Composition, Structure

from verifiable_pxrd.baselines.candidates import materialize_case_candidates
from verifiable_pxrd.baselines.matching import (
    element_composition_match,
    formula_metric_metadata,
    primary_matcher,
    primary_metric_metadata,
    primary_structure_match,
)
from verifiable_pxrd.baselines.targets import (
    SUPPORT_POLICIES,
    framework_target_root,
    validate_source_manifest,
)

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "pxrd-bench" / "pXRD-100"
SOURCE_MANIFEST = CORPUS / "manifest.json"
DATASET_ID: str | None = None
CASE_PREFIX: str | None = None
SUPPORT_POLICY = "manifest"
EXPECTED_CASES = 100
MATCH_TIMEOUT_SECONDS = 30.0
MATCH_MEMORY_LIMIT_BYTES = 4 * 1024**3

PROFILES = {
    "decifer": {
        "display_name": "deCIFer",
        "result_name": "deCIFer",
        "samples": 8,
        "target_manifest": framework_target_root(ROOT, "decifer", CORPUS) / "manifest.json",
        "conditioning": "pXRD plus reduced composition",
        "caveat": None,
    },
    "decifer-oracle": {
        "display_name": "deCIFer full-cell oracle",
        "result_name": "deCIFer",
        "samples": 8,
        "target_manifest": framework_target_root(ROOT, "decifer", CORPUS) / "manifest.json",
        "conditioning": "pXRD plus exact full-unit-cell composition",
        "caveat": (
            "Oracle caveat: the full unit-cell formula was derived from each hidden target "
            "CIF. It supplies exact element counts and formula-unit multiplicity, which is "
            "more information than pXRD plus reduced composition."
        ),
    },
    "pxrdgen": {
        "display_name": "PXRDGen",
        "result_name": "PXRDGen",
        "samples": 8,
        "target_manifest": framework_target_root(ROOT, "pxrdgen", CORPUS) / "manifest.json",
        "conditioning": "pXRD plus exact primitive-cell composition and atom count",
        "caveat": (
            "Oracle caveat: the primitive-cell formula and exact atom count were derived from "
            "each hidden target CIF. This is more information than pXRD plus reduced composition."
        ),
    },
    "diffractgpt": {
        "display_name": "DiffractGPT",
        "result_name": "DiffractGPT",
        "samples": 1,
        "target_manifest": framework_target_root(ROOT, "diffractgpt", CORPUS) / "manifest.json",
        "conditioning": "pXRD plus reduced composition",
        "caveat": (
            "The released helper defines one greedy decode, so no best-of-8 score is reported. "
            "The paper adapter also does not declare a license, so these local artifacts should "
            "not be redistributed until its licensing is clarified."
        ),
    },
    "ab-pxrd-solver": {
        "display_name": "Ab-PXRD-Solver",
        "result_name": "Ab-PXRD-Solver",
        "samples": 1,
        "target_manifest": framework_target_root(ROOT, "ab-pxrd-solver", CORPUS) / "manifest.json",
        "conditioning": "released benchmark-style GSAS pXRD plus reduced composition",
        "caveat": (
            "The deterministic solver emits at most one selected structure. Space group is "
            "inferred from the input rather than supplied. Its released input-generation "
            "profile is distinct from its internal fast candidate-screening profile. Each "
            "case has a four-hour wall-time cap; a candidate emitted before the cap remains "
            "eligible and is explicitly labeled timeout-with-candidate."
        ),
    },
    "realpxrd-solver": {
        "display_name": "RealPXRD-Solver (primitive-composition oracle)",
        "result_name": "RealPXRD-Solver",
        "samples": 20,
        "target_manifest": framework_target_root(ROOT, "realpxrd-solver", CORPUS) / "manifest.json",
        "conditioning": "native pXRD peaks plus exact primitive-cell composition and atom count",
        "input_mode": "lattice-free-primitive-formula-oracle",
        "caveat": (
            "Oracle caveat: primitive-cell composition and atom count were derived from the "
            "hidden target CIF. The public GSAS-II ranking/refinement stage is unavailable, "
            "so candidate order is sampler order and best-of-20 is an oracle-recall metric."
        ),
    },
    "realpxrd-solver-k100": {
        "display_name": "RealPXRD-Solver (primitive-composition oracle, k=100)",
        "result_name": "RealPXRD-Solver",
        "samples": 100,
        "target_manifest": framework_target_root(ROOT, "realpxrd-solver", CORPUS) / "manifest.json",
        "conditioning": "native pXRD peaks plus exact primitive-cell composition and atom count",
        "input_mode": "lattice-free-primitive-formula-oracle",
        "caveat": (
            "Oracle caveat: primitive-cell composition and atom count were derived from the "
            "hidden target CIF. The public GSAS-II ranking/refinement stage is unavailable, "
            "so candidate order is sampler order and best-of-100 is an oracle-recall metric."
        ),
    },
    "realpxrd-solver-lattice": {
        "display_name": "RealPXRD-Solver (primitive-cell lattice oracle)",
        "result_name": "RealPXRD-Solver",
        "samples": 20,
        "target_manifest": framework_target_root(ROOT, "realpxrd-solver", CORPUS) / "manifest.json",
        "conditioning": (
            "native pXRD peaks plus exact primitive-cell composition, atom count, and lattice"
        ),
        "input_mode": "lattice-conditioned-primitive-cell-oracle",
        "caveat": (
            "Upper-bound oracle caveat: primitive-cell composition, atom count, and lattice "
            "were derived from the hidden target CIF. Candidate order is sampler order and "
            "best-of-20 is an oracle-recall metric."
        ),
    },
    "realpxrd-solver-reduced": {
        "display_name": "RealPXRD-Solver (reduced-formula control)",
        "result_name": "RealPXRD-Solver",
        "samples": 20,
        "target_manifest": framework_target_root(ROOT, "realpxrd-solver", CORPUS) / "manifest.json",
        "conditioning": "native pXRD peaks plus reduced composition",
        "input_mode": "lattice-free-reduced-formula",
        "caveat": (
            "The released model requires a literal atom inventory and cannot infer an unknown "
            "formula-unit multiplier. This prompt-equivalent control therefore undercounts "
            "atoms whenever the true primitive cell contains multiple reduced formula units."
        ),
    },
}


def configure_dataset(args: argparse.Namespace) -> None:
    global CORPUS, SOURCE_MANIFEST, DATASET_ID, CASE_PREFIX, SUPPORT_POLICY
    CORPUS = args.corpus_root.expanduser().resolve()
    SOURCE_MANIFEST = CORPUS / "manifest.json"
    DATASET_ID = args.dataset_id
    CASE_PREFIX = args.case_prefix
    SUPPORT_POLICY = args.support_policy
    directories = {
        "decifer": "decifer",
        "decifer-oracle": "decifer",
        "pxrdgen": "pxrdgen",
        "diffractgpt": "diffractgpt",
        "ab-pxrd-solver": "ab-pxrd-solver",
        "realpxrd-solver": "realpxrd-solver",
        "realpxrd-solver-k100": "realpxrd-solver",
        "realpxrd-solver-lattice": "realpxrd-solver",
        "realpxrd-solver-reduced": "realpxrd-solver",
    }
    for name, directory in directories.items():
        PROFILES[name]["target_manifest"] = (
            framework_target_root(ROOT, directory, CORPUS) / "manifest.json"
        )


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def optional_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if np.isfinite(number) else None


def numeric_distribution(values: list[float], expected_count: int) -> dict[str, Any]:
    array = np.asarray(values, dtype=np.float64)
    return {
        "expected_count": expected_count,
        "finite_count": len(array),
        "coverage": float(len(array) / expected_count),
        "mean": float(np.mean(array)) if len(array) else None,
        "population_std": float(np.std(array, ddof=0)) if len(array) else None,
        "median": float(np.median(array)) if len(array) else None,
        "min": float(np.min(array)) if len(array) else None,
        "max": float(np.max(array)) if len(array) else None,
    }


def ab_solver_outcome(
    shard_root: Path,
    record: dict[str, Any],
) -> tuple[str, str | None]:
    if record.get("status") == "generated":
        if bool(record.get("timed_out")):
            return "timeout_with_candidate", "upstream case capped after emitting candidate"
        return "selected_structure", None
    if bool(record.get("timed_out")):
        return "timeout", "upstream case timeout"
    returncode = record.get("returncode")
    if returncode not in (None, 0):
        exception: str | None = None
        stderr_path = record.get("stderr_path")
        if stderr_path:
            resolved = (shard_root / str(stderr_path)).resolve()
            if resolved == shard_root or shard_root not in resolved.parents:
                raise RuntimeError("unsafe Ab-PXRD-Solver stderr path")
            if resolved.is_file():
                lines = [line.strip() for line in resolved.read_text(encoding="utf-8").splitlines()]
                exception = next(
                    (
                        line
                        for line in reversed(lines)
                        if line and ("Error:" in line or line.startswith("Exception:"))
                    ),
                    None,
                )
        return "runtime_error", exception
    return "no_selected_structure", None


def validate_ab_import_audit(
    run_root: Path,
    source_digest: str,
    target_digest: str,
) -> dict[str, Any] | None:
    """Validate the optional base/expanded-formula repair merge ledger."""

    path = run_root / "IMPORT-AUDIT.json"
    if not path.is_file():
        return None
    audit = load_json(path)
    if audit.get("source_manifest_sha256") != source_digest:
        raise RuntimeError("Ab-PXRD-Solver import audit source-manifest mismatch")
    if audit.get("target_manifest_sha256") != target_digest:
        raise RuntimeError("Ab-PXRD-Solver import audit target-manifest mismatch")
    if int(audit.get("case_count", -1)) != EXPECTED_CASES:
        raise RuntimeError("Ab-PXRD-Solver import audit case-count mismatch")
    rows = list(audit.get("shards") or [])
    if len(rows) != EXPECTED_CASES:
        raise RuntimeError("Ab-PXRD-Solver import audit shard-count mismatch")
    seen: set[str] = set()
    repair_ids: list[str] = []
    aliases_added = 0
    for row in rows:
        case_id = str(row["case_id"])
        if case_id in seen:
            raise RuntimeError(f"duplicate Ab-PXRD-Solver import audit case: {case_id}")
        seen.add(case_id)
        result_path = run_root / f"shard-{int(row['shard_index']):03d}" / "results.json"
        if not result_path.is_file():
            raise RuntimeError(f"missing imported Ab-PXRD-Solver result: {result_path}")
        if sha256_file(result_path) != row.get("imported_results_sha256"):
            raise RuntimeError(f"imported Ab-PXRD-Solver result digest mismatch: {case_id}")
        if row.get("selected_source") == "expanded_formula_repair":
            repair_ids.append(case_id)
        aliases_added += len(row.get("metadata_aliases_added") or {})
    declared_repair_ids = [str(value) for value in audit.get("formula_repair_case_ids") or []]
    if sorted(repair_ids) != sorted(declared_repair_ids):
        raise RuntimeError("Ab-PXRD-Solver import audit formula-repair set mismatch")
    if len(repair_ids) != int(audit.get("formula_repair_case_count", -1)):
        raise RuntimeError("Ab-PXRD-Solver import audit formula-repair count mismatch")
    return {
        "path": "IMPORT-AUDIT.json",
        "sha256": sha256_file(path),
        "case_count": len(rows),
        "formula_repair_case_count": len(repair_ids),
        "formula_repair_case_ids": sorted(repair_ids),
        "metadata_alias_count_added": aliases_added,
        "raw_runs_preserved": True,
    }


def minimum_periodic_distance(structure: Structure) -> float:
    if len(structure) < 2:
        return float("inf")
    distances = np.asarray(structure.distance_matrix, dtype=np.float64)
    distances += np.diag(np.full(len(structure), 10.5))
    return float(np.min(distances))


def _structure_match_worker(
    connection: Any,
    predicted: Structure,
    ground_truth: Structure,
) -> None:
    """Run one potentially combinatorial StructureMatcher call in isolation."""

    try:
        import resource

        resource.setrlimit(
            resource.RLIMIT_AS,
            (MATCH_MEMORY_LIMIT_BYTES, MATCH_MEMORY_LIMIT_BYTES),
        )
        connection.send(
            (
                "ok",
                primary_structure_match(predicted, ground_truth, primary_matcher()),
            )
        )
    except BaseException as exc:  # child must report allocation failures as data
        connection.send(("error", f"{type(exc).__name__}: {exc}"))
    finally:
        connection.close()


def guarded_structure_match(
    predicted: Structure,
    ground_truth: Structure,
) -> tuple[bool, tuple[float, float] | None, str]:
    """Bound matcher memory/time so one pathological candidate cannot kill a run."""

    context = multiprocessing.get_context("fork")
    receive, send = context.Pipe(duplex=False)
    process = context.Process(
        target=_structure_match_worker,
        args=(send, predicted, ground_truth),
        daemon=True,
    )
    process.start()
    send.close()
    payload: tuple[str, Any] | None = None
    try:
        if receive.poll(MATCH_TIMEOUT_SECONDS):
            payload = receive.recv()
    except EOFError:
        payload = None
    finally:
        receive.close()
    if payload is None and process.is_alive():
        process.terminate()
    process.join(timeout=5)
    if process.is_alive():
        process.kill()
        process.join()
    if payload is None:
        if process.exitcode == 0:
            return False, None, "StructureMatcher worker returned no result"
        return False, None, f"StructureMatcher worker exited with code {process.exitcode}"
    if payload[0] == "error":
        return False, None, str(payload[1])
    matched, distances = payload[1]
    if distances is None:
        return bool(matched), None, ""
    return bool(matched), (float(distances[0]), float(distances[1])), ""


def load_candidates(
    run_root: Path,
    profile: dict[str, Any],
    source_digest: str,
    source_dataset_id: str,
) -> tuple[
    dict[str, tuple[Path, dict[str, Any]]],
    list[dict[str, Any]],
    dict[str, int],
]:
    indexed: dict[str, tuple[Path, dict[str, Any]]] = {}
    shard_results: list[dict[str, Any]] = []
    audit = {"candidate_hashes_checked": 0, "raw_hashes_checked": 0}
    for result_path in sorted(run_root.glob("shard-*/results.json")):
        result = load_json(result_path)
        shard_results.append(result)
        if result["framework"] != profile["result_name"]:
            raise RuntimeError(f"unexpected framework in {result_path}")
        if int(result["samples_per_case"]) != int(profile["samples"]):
            raise RuntimeError(f"unexpected sample count in {result_path}")
        if result["source_manifest_sha256"] != source_digest:
            raise RuntimeError(f"stale source-manifest digest in {result_path}")
        if result.get("source_dataset_id") != source_dataset_id:
            raise RuntimeError(f"dataset identity mismatch in {result_path}")
        if result.get("case_prefix") != CASE_PREFIX:
            raise RuntimeError(f"case-prefix mismatch in {result_path}")
        if result.get("support_policy") != SUPPORT_POLICY:
            raise RuntimeError(f"support-policy mismatch in {result_path}")
        shard_root = result_path.parent
        for candidate in result["candidates"]:
            key = f"{candidate['case_id']}:{int(candidate['sample_index'])}"
            if key in indexed:
                raise RuntimeError(f"duplicate candidate record: {key}")
            candidate_path = (shard_root / candidate["candidate_path"]).resolve()
            if run_root != candidate_path and run_root not in candidate_path.parents:
                raise RuntimeError(f"unsafe candidate path for {key}")
            if not candidate_path.is_file():
                raise RuntimeError(f"missing candidate artifact for {key}: {candidate_path}")
            if sha256_file(candidate_path) != candidate["candidate_sha256"]:
                raise RuntimeError(f"candidate digest mismatch for {key}")
            audit["candidate_hashes_checked"] += 1
            if candidate.get("raw_path"):
                raw_path = (shard_root / candidate["raw_path"]).resolve()
                if run_root != raw_path and run_root not in raw_path.parents:
                    raise RuntimeError(f"unsafe raw artifact path for {key}")
                if not raw_path.is_file():
                    raise RuntimeError(f"missing raw artifact for {key}: {raw_path}")
                if sha256_file(raw_path) != candidate["raw_sha256"]:
                    raise RuntimeError(f"raw artifact digest mismatch for {key}")
                audit["raw_hashes_checked"] += 1
            indexed[key] = (shard_root, candidate)
    return indexed, shard_results, audit


def evaluate(framework: str, run_root: Path) -> dict[str, Any]:
    profile = PROFILES[framework]
    source_digest = sha256_file(SOURCE_MANIFEST)
    source_dataset_id, source_case_list = validate_source_manifest(
        load_json(SOURCE_MANIFEST),
        expected_cases=EXPECTED_CASES,
        dataset_id=DATASET_ID,
        case_prefix=CASE_PREFIX,
    )
    source_cases = {case["case_id"]: case for case in source_case_list}
    target_manifest = load_json(profile["target_manifest"])
    target_manifest_digest = sha256_file(profile["target_manifest"])
    target_cases = {str(case["case_id"]): case for case in target_manifest["cases"]}
    target_ids = [str(case["case_id"]) for case in target_manifest["cases"]]
    if target_manifest["source_manifest_sha256"] != source_digest:
        raise RuntimeError("framework target manifest is stale")
    if len(source_cases) != EXPECTED_CASES or set(target_ids) != set(source_cases):
        raise RuntimeError("framework target coverage does not equal the selected corpus")
    if target_manifest.get("source_dataset_id", source_dataset_id) != source_dataset_id:
        raise RuntimeError("framework target dataset identity mismatch")
    if target_manifest.get("case_prefix") != CASE_PREFIX:
        raise RuntimeError("framework target case-prefix contract mismatch")
    if target_manifest.get("support_policy", "manifest") != SUPPORT_POLICY:
        raise RuntimeError("framework target support-policy contract mismatch")

    candidates, shards, artifact_audit = load_candidates(
        run_root, profile, source_digest, source_dataset_id
    )
    expected_samples = int(profile["samples"])
    expected_keys = {
        f"{case_id}:{sample_index}"
        for case_id in target_ids
        for sample_index in range(expected_samples)
    }
    if set(candidates) != expected_keys:
        missing = sorted(expected_keys - set(candidates))
        extra = sorted(set(candidates) - expected_keys)
        raise RuntimeError(f"incomplete run: missing={missing[:8]}, extra={extra[:8]}")

    conditioning_audit: dict[str, Any] | None = None
    if framework == "decifer-oracle":
        mismatches: list[str] = []
        for key, (_, candidate) in candidates.items():
            expected = target_cases[str(candidate["case_id"])]
            expected_formula = str(expected["paper_native_cell_composition"])
            if (
                candidate.get("input_mode") != "full_cell_formula_oracle_from_hidden_cif"
                or candidate.get("input_formula") != expected_formula
                or candidate.get("prompt") != f"data_{expected_formula}\n"
            ):
                mismatches.append(key)
        if mismatches:
            raise RuntimeError(f"deCIFer full-cell oracle-input audit failed: {mismatches[:8]}")
        conditioning_audit = {
            "candidate_inputs_checked": len(candidates),
            "mismatch_count": 0,
            "full_cell_formula_differs_from_reduced_prompt_string_case_count": sum(
                str(case["paper_native_cell_composition"]) != str(case["composition"])
                for case in target_cases.values()
            ),
            "full_cell_formula_units_gt_one_case_count": int(
                target_manifest["source_cell_formula_units_gt_one_count"]
            ),
            "full_cell_atom_count_range": [
                int(
                    min(
                        Composition(case["paper_native_cell_composition"]).num_atoms
                        for case in target_cases.values()
                    )
                ),
                int(
                    max(
                        Composition(case["paper_native_cell_composition"]).num_atoms
                        for case in target_cases.values()
                    )
                ),
            ],
            "statement": (
                "Every candidate received the hidden target's exact paper-native full-cell "
                "formula in its data_ prompt."
            ),
        }
    if framework == "pxrdgen":
        mismatches: list[str] = []
        for key, (_, candidate) in candidates.items():
            expected = target_cases[str(candidate["case_id"])]
            if (
                candidate.get("input_mode") != "primitive_cell_formula_oracle_from_hidden_cif"
                or candidate.get("input_formula") != expected["primitive_cell_formula"]
                or int(candidate.get("input_atom_count", -1))
                != int(expected["primitive_cell_atom_count"])
            ):
                mismatches.append(key)
        if mismatches:
            raise RuntimeError(f"PXRDGen oracle-input audit failed: {mismatches[:8]}")
        conditioning_audit = {
            "candidate_inputs_checked": len(candidates),
            "mismatch_count": 0,
            "primitive_formula_differs_from_reduced_case_count": int(
                target_manifest["primitive_formula_differs_from_reduced_count"]
            ),
            "statement": (
                "Every candidate received the hidden target's exact primitive-cell formula "
                "and atom count."
            ),
        }
    if framework.startswith("realpxrd-solver"):
        input_mode = str(profile["input_mode"])
        reduced = input_mode == "lattice-free-reduced-formula"
        lattice_conditioned = input_mode == "lattice-conditioned-primitive-cell-oracle"
        mismatches: list[str] = []
        for key, (_, candidate) in candidates.items():
            expected = target_cases[str(candidate["case_id"])]
            expected_formula = str(
                expected["reduced_formula_explicit"]
                if reduced
                else expected["primitive_cell_formula"]
            )
            expected_count = int(
                expected["reduced_formula_atom_count"]
                if reduced
                else expected["primitive_cell_atom_count"]
            )
            if (
                candidate.get("input_mode") != input_mode
                or candidate.get("input_formula") != expected_formula
                or int(candidate.get("input_atom_count", -1)) != expected_count
                or bool(candidate.get("oracle_input")) == reduced
                or bool(candidate.get("input_lattice_conditioned")) != lattice_conditioned
            ):
                mismatches.append(key)
        if mismatches:
            raise RuntimeError(f"RealPXRD-Solver conditioning-input audit failed: {mismatches[:8]}")
        multipliers = [
            int(case["primitive_cell_formula_unit_multiplier"]) for case in target_cases.values()
        ]
        conditioning_audit = {
            "candidate_inputs_checked": len(candidates),
            "mismatch_count": 0,
            "input_mode": input_mode,
            "oracle_input": not reduced,
            "lattice_conditioned": lattice_conditioned,
            "primitive_formula_units_gt_one_case_count": sum(
                multiplier > 1 for multiplier in multipliers
            ),
            "statement": (
                "Every candidate received the input condition declared by the selected "
                "RealPXRD-Solver benchmark profile."
            ),
        }
    if framework == "ab-pxrd-solver":
        mismatches: list[str] = []
        expanded_count = 0
        for key, (_, candidate) in candidates.items():
            expected_formula = str(target_cases[str(candidate["case_id"])]["formula"])
            command = list(candidate.get("command") or [])
            try:
                solver_formula = str(command[command.index("--formula") + 1])
            except (ValueError, IndexError):
                mismatches.append(key)
                continue
            expanded_count += int(solver_formula != expected_formula)
            try:
                same_composition = Composition(solver_formula) == Composition(expected_formula)
            except Exception:
                same_composition = False
            if (
                candidate.get("input_formula") != expected_formula
                or "(" in solver_formula
                or ")" in solver_formula
                or not same_composition
            ):
                mismatches.append(key)
        if mismatches:
            raise RuntimeError(f"Ab-PXRD-Solver composition-input audit failed: {mismatches[:8]}")
        conditioning_audit = {
            "candidate_inputs_checked": len(candidates),
            "mismatch_count": 0,
            "expanded_parenthesized_formula_case_count": expanded_count,
            "statement": (
                "Every candidate received the target manifest's reduced composition. "
                "Parenthesized pymatgen formula presentations were flattened to equivalent "
                "integer element counts for the released regex-only parser."
            ),
        }

    candidate_rows: list[dict[str, Any]] = []
    case_rows: list[dict[str, Any]] = []
    for case_id in target_ids:
        source_case = source_cases[case_id]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            ground_truth = Structure.from_file(CORPUS / source_case["path"])
        rows: list[dict[str, Any]] = []
        for sample_index in range(expected_samples):
            shard_root, record = candidates[f"{case_id}:{sample_index}"]
            candidate_path = (shard_root / record["candidate_path"]).resolve()
            solver_summary = record.get("solver_summary") or {}
            upstream_outcome, upstream_exception = (
                ab_solver_outcome(shard_root, record)
                if framework == "ab-pxrd-solver"
                else (None, None)
            )
            row: dict[str, Any] = {
                "case_id": case_id,
                "panel": source_case["panel"],
                "stream": source_case.get("stream"),
                "sample_index": sample_index,
                "status": record["status"],
                "candidate_path": str(candidate_path.relative_to(run_root)),
                "target_formula": source_case["formula"],
                "predicted_formula": record.get("predicted_formula"),
                "formula_match": False,
                "target_full_cell_formula": (
                    target_cases[case_id]["paper_native_cell_composition"]
                    if framework == "decifer-oracle"
                    else None
                ),
                "full_cell_composition_match": False,
                "structure_valid": False,
                "structure_match": False,
                "matcher_rms": None,
                "matcher_max_dist": None,
                "minimum_periodic_distance_angstrom": None,
                "evaluation_error": record.get("error"),
                "solver_status": solver_summary.get("Status"),
                "solver_rwp_percent": optional_float(solver_summary.get("Rwp")),
                "solver_r2": optional_float(solver_summary.get("R2")),
                "solver_chi2": optional_float(solver_summary.get("Chi2")),
                "solver_space_group": solver_summary.get("SPG") or None,
                "solver_runtime": solver_summary.get("Runtime") or None,
                "solver_structure_count": optional_float(solver_summary.get("N_struc")),
                "solver_attempt_count": optional_float(solver_summary.get("N_attempts")),
                "upstream_returncode": record.get("returncode"),
                "upstream_timed_out": record.get("timed_out"),
                "upstream_outcome": upstream_outcome,
                "upstream_exception": upstream_exception,
            }
            if record["status"] == "generated" and candidate_path.suffix.lower() == ".cif":
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        predicted = Structure.from_file(candidate_path)
                    row["formula_match"] = element_composition_match(
                        predicted,
                        ground_truth,
                    )
                    if framework == "decifer-oracle":
                        row["full_cell_composition_match"] = element_composition_match(
                            predicted.composition,
                            Composition(target_cases[case_id]["paper_native_cell_composition"]),
                            reduced=False,
                        )
                    minimum_distance = minimum_periodic_distance(predicted)
                    row["minimum_periodic_distance_angstrom"] = minimum_distance
                    row["structure_valid"] = bool(
                        predicted.volume >= 0.1
                        and (minimum_distance is None or minimum_distance >= 0.5)
                    )
                    if row["formula_match"] and row["structure_valid"]:
                        matched, distances, matcher_error = guarded_structure_match(
                            predicted,
                            ground_truth,
                        )
                        if matcher_error:
                            row["evaluation_error"] = matcher_error
                        row["structure_match"] = matched
                        if matched and distances is not None:
                            row["matcher_rms"] = float(distances[0])
                            row["matcher_max_dist"] = float(distances[1])
                except Exception as exc:
                    row["evaluation_error"] = f"{type(exc).__name__}: {exc}"
            rows.append(row)
            candidate_rows.append(row)

        matched = [row for row in rows if row["structure_match"]]
        case_row = {
            "case_id": case_id,
            "panel": source_case["panel"],
            "stream": source_case.get("stream"),
            "target_formula": source_case["formula"],
            "best_of_1_structure_match": bool(rows[0]["structure_match"]),
            "best_of_1_formula_match": bool(rows[0]["formula_match"]),
            "best_of_1_full_cell_composition_match": bool(rows[0]["full_cell_composition_match"]),
            "matched_sample_indices": [int(row["sample_index"]) for row in matched],
            "best_match_rms": (
                min(float(row["matcher_rms"]) for row in matched) if matched else None
            ),
        }
        if expected_samples > 1:
            case_row.update(
                {
                    "best_of_k_structure_match": bool(matched),
                    "best_of_k_formula_match": any(row["formula_match"] for row in rows),
                    "best_of_k_full_cell_composition_match": any(
                        row["full_cell_composition_match"] for row in rows
                    ),
                }
            )
        case_rows.append(case_row)

    summary = summarize(
        case_rows,
        candidate_rows,
        expected_samples,
        report_full_cell=framework == "decifer-oracle",
    )
    solver_native_metrics: dict[str, Any] | None = None
    import_audit: dict[str, Any] | None = None
    if framework == "ab-pxrd-solver":
        import_audit = validate_ab_import_audit(
            run_root,
            source_digest,
            target_manifest_digest,
        )
        solver_native_metrics = {
            "definition": (
                "Upstream GSAS-II refinement diagnostics for the selected structure. Rwp is "
                "reported in percent by Ab-PXRD-Solver and is distinct from this benchmark's "
                "independently normalized fixed-profile Rwp."
            ),
            "status_counts": dict(
                sorted(
                    Counter(
                        str(row["solver_status"] or "missing") for row in candidate_rows
                    ).items()
                )
            ),
            "outcome_counts": dict(
                sorted(Counter(str(row["upstream_outcome"]) for row in candidate_rows).items())
            ),
            "rwp_percent": numeric_distribution(
                [
                    float(row["solver_rwp_percent"])
                    for row in candidate_rows
                    if row["solver_rwp_percent"] is not None
                ],
                len(candidate_rows),
            ),
            "r2": numeric_distribution(
                [float(row["solver_r2"]) for row in candidate_rows if row["solver_r2"] is not None],
                len(candidate_rows),
            ),
            "chi2": numeric_distribution(
                [
                    float(row["solver_chi2"])
                    for row in candidate_rows
                    if row["solver_chi2"] is not None
                ],
                len(candidate_rows),
            ),
        }
    metric = {
        "structure_matcher": {
            **primary_metric_metadata(),
            "process_isolation": True,
            "timeout_seconds": MATCH_TIMEOUT_SECONDS,
            "memory_limit_bytes": MATCH_MEMORY_LIMIT_BYTES,
        },
        "formula_match": formula_metric_metadata(),
        "structure_validity": {"minimum_distance_angstrom": 0.5, "volume_min": 0.1},
        "best_of_1": "candidate sample_index 0",
        "evaluator_pymatgen": importlib.metadata.version("pymatgen"),
    }
    if expected_samples > 1:
        metric["best_of_k"] = f"oracle over sample_index 0 through {expected_samples - 1}"
    report = {
        "schema_version": "1.1.0",
        "source_dataset_id": source_dataset_id,
        "framework": profile["display_name"],
        "run_id": run_root.name,
        "source_manifest_sha256": source_digest,
        "conditioning": profile["conditioning"],
        "conditioning_audit": conditioning_audit,
        "artifact_audit": {
            **artifact_audit,
            "hash_mismatch_count": 0,
            "missing_or_extra_candidate_count": 0,
        },
        "caveat": profile["caveat"],
        "metric": metric,
        "generation": {
            "shard_count": len(shards),
            "aggregate_container_seconds": sum(
                float(shard["runtime"]["total_seconds"]) for shard in shards
            ),
            "first_shard_provenance": {
                key: shards[0][key]
                for key in (
                    "framework_commit",
                    "checkpoint_sha256",
                    "encoder_checkpoint_sha256",
                    "base_model_revision",
                    "base_model_sha256",
                    "adapter_revision",
                    "adapter_sha256",
                    "adapter_license",
                    "source_commit",
                    "mace_model_sha256",
                    "gsasii_commit",
                    "inference",
                )
                if key in shards[0]
            },
        },
        "summary": summary,
        "solver_native_metrics": solver_native_metrics,
        "import_audit": import_audit,
        "cases": case_rows,
    }
    write_csv(run_root / "evaluation-candidates.csv", candidate_rows)
    write_csv(run_root / "evaluation-cases.csv", case_rows)
    write_json(run_root / "evaluation.json", report)
    write_json(
        run_root / "run-summary.json",
        {key: value for key, value in report.items() if key != "cases"},
    )
    materialize_case_candidates(
        run_root,
        verifier_rows=candidate_rows,
        verifier_metadata=report["metric"],
    )
    write_readme(run_root / "RUN.md", profile, report)
    return report


def summarize(
    case_rows: list[dict[str, Any]],
    candidate_rows: list[dict[str, Any]],
    samples: int,
    *,
    report_full_cell: bool = False,
) -> dict[str, Any]:
    def aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
        count = len(rows)
        structure_1 = sum(bool(row["best_of_1_structure_match"]) for row in rows)
        formula_1 = sum(bool(row["best_of_1_formula_match"]) for row in rows)
        result = {
            "case_count": count,
            "best_of_1_structure_match_count": structure_1,
            "best_of_1_structure_match_rate": structure_1 / count if count else None,
            "best_of_1_formula_match_count": formula_1,
            "best_of_1_formula_match_rate": formula_1 / count if count else None,
        }
        if report_full_cell:
            full_cell_1 = sum(bool(row["best_of_1_full_cell_composition_match"]) for row in rows)
            result.update(
                {
                    "best_of_1_full_cell_composition_match_count": full_cell_1,
                    "best_of_1_full_cell_composition_match_rate": (
                        full_cell_1 / count if count else None
                    ),
                }
            )
        if samples > 1:
            structure_k = sum(bool(row["best_of_k_structure_match"]) for row in rows)
            formula_k = sum(bool(row["best_of_k_formula_match"]) for row in rows)
            result.update(
                {
                    "best_of_k_structure_match_count": structure_k,
                    "best_of_k_structure_match_rate": structure_k / count if count else None,
                    "best_of_k_formula_match_count": formula_k,
                    "best_of_k_formula_match_rate": formula_k / count if count else None,
                }
            )
            if report_full_cell:
                full_cell_k = sum(
                    bool(row["best_of_k_full_cell_composition_match"]) for row in rows
                )
                result.update(
                    {
                        "best_of_k_full_cell_composition_match_count": full_cell_k,
                        "best_of_k_full_cell_composition_match_rate": (
                            full_cell_k / count if count else None
                        ),
                    }
                )
        return result

    panels: dict[str, list[dict[str, Any]]] = defaultdict(list)
    streams: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in case_rows:
        panels[str(row["panel"])].append(row)
        if row.get("stream"):
            streams[str(row["stream"])].append(row)
    statuses = Counter(str(row["status"]) for row in candidate_rows)
    return {
        "samples_per_case": samples,
        "all": aggregate(case_rows),
        "panels": {name: aggregate(rows) for name, rows in sorted(panels.items())},
        "streams": {name: aggregate(rows) for name, rows in sorted(streams.items())},
        "candidate_count": len(candidate_rows),
        "candidate_status_counts": dict(sorted(statuses.items())),
        "valid_structure_candidate_count": sum(
            bool(row["structure_valid"]) for row in candidate_rows
        ),
    }


def write_json(path: Path, payload: Any) -> None:
    temporary = path.with_suffix(path.suffix + ".partial")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError("cannot write an empty evaluation table")
    temporary = path.with_suffix(path.suffix + ".partial")
    with temporary.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    key: json.dumps(value) if isinstance(value, list) else value
                    for key, value in row.items()
                }
            )
    temporary.replace(path)


def write_readme(path: Path, profile: dict[str, Any], report: dict[str, Any]) -> None:
    summary = report["summary"]
    total = summary["all"]
    samples = summary["samples_per_case"]
    lines = [
        f"# {profile['display_name']} {report['source_dataset_id']} run",
        "",
        f"Conditioning: {profile['conditioning']}.",
        (
            "Evaluation: primary exact-recovery Pymatgen `StructureMatcher` with "
            "`ltol=0.2`, `stol=0.3`, `angle_tol=5`, exact cell scale, symmetric "
            "element-aware fitting, and commensurate-supercell support."
        ),
        "",
    ]
    if samples > 1:
        lines.extend(
            [
                f"| Metric | Best-of-1 | Best-of-{samples} |",
                "|---|---:|---:|",
                (
                    "| Structure match | "
                    f"{total['best_of_1_structure_match_count']}/{total['case_count']} "
                    f"({total['best_of_1_structure_match_rate']:.1%}) | "
                    f"{total['best_of_k_structure_match_count']}/{total['case_count']} "
                    f"({total['best_of_k_structure_match_rate']:.1%}) |"
                ),
                (
                    "| Reduced-formula match | "
                    f"{total['best_of_1_formula_match_count']}/{total['case_count']} "
                    f"({total['best_of_1_formula_match_rate']:.1%}) | "
                    f"{total['best_of_k_formula_match_count']}/{total['case_count']} "
                    f"({total['best_of_k_formula_match_rate']:.1%}) |"
                ),
            ]
        )
        if "best_of_1_full_cell_composition_match_count" in total:
            lines.append(
                "| Exact full-cell composition | "
                f"{total['best_of_1_full_cell_composition_match_count']}/{total['case_count']} "
                f"({total['best_of_1_full_cell_composition_match_rate']:.1%}) | "
                f"{total['best_of_k_full_cell_composition_match_count']}/{total['case_count']} "
                f"({total['best_of_k_full_cell_composition_match_rate']:.1%}) |"
            )
    else:
        lines.extend(
            [
                "| Metric | Best-of-1 |",
                "|---|---:|",
                (
                    "| Structure match | "
                    f"{total['best_of_1_structure_match_count']}/{total['case_count']} "
                    f"({total['best_of_1_structure_match_rate']:.1%}) |"
                ),
                (
                    "| Reduced-formula match | "
                    f"{total['best_of_1_formula_match_count']}/{total['case_count']} "
                    f"({total['best_of_1_formula_match_rate']:.1%}) |"
                ),
            ]
        )
    lines.extend(["", "## Structure matches by panel", ""])
    if samples > 1:
        lines.extend(
            [
                f"| Panel | Cases | Best-of-1 | Best-of-{samples} |",
                "|---|---:|---:|---:|",
            ]
        )
        for panel, panel_summary in summary["panels"].items():
            lines.append(
                f"| {panel.title()} | {panel_summary['case_count']} | "
                f"{panel_summary['best_of_1_structure_match_count']} | "
                f"{panel_summary['best_of_k_structure_match_count']} |"
            )
    else:
        lines.extend(["| Panel | Cases | Best-of-1 |", "|---|---:|---:|"])
        for panel, panel_summary in summary["panels"].items():
            lines.append(
                f"| {panel.title()} | {panel_summary['case_count']} | "
                f"{panel_summary['best_of_1_structure_match_count']} |"
            )
    if summary.get("streams"):
        lines.extend(["", "## Structure matches by generation stream", ""])
        if samples > 1:
            lines.extend(
                [
                    f"| Stream | Cases | Best-of-1 | Best-of-{samples} |",
                    "|---|---:|---:|---:|",
                ]
            )
            for stream, stream_summary in summary["streams"].items():
                lines.append(
                    f"| {stream} | {stream_summary['case_count']} | "
                    f"{stream_summary['best_of_1_structure_match_count']} | "
                    f"{stream_summary['best_of_k_structure_match_count']} |"
                )
        else:
            lines.extend(["| Stream | Cases | Best-of-1 |", "|---|---:|---:|"])
            for stream, stream_summary in summary["streams"].items():
                lines.append(
                    f"| {stream} | {stream_summary['case_count']} | "
                    f"{stream_summary['best_of_1_structure_match_count']} |"
                )
    lines.extend(
        [
            "",
            (
                f"Candidate artifacts: {summary['candidate_count']} total; status counts "
                f"`{json.dumps(summary['candidate_status_counts'], sort_keys=True)}`."
            ),
            (
                "Artifact hashes checked: "
                f"{report['artifact_audit']['candidate_hashes_checked']} candidate files and "
                f"{report['artifact_audit']['raw_hashes_checked']} raw files; zero mismatches."
            ),
            (
                "Inference settings: `"
                + json.dumps(
                    report["generation"]["first_shard_provenance"]["inference"],
                    sort_keys=True,
                )
                + "`."
            ),
        ]
    )
    if profile["caveat"]:
        lines.extend(["", f"Caveat: {profile['caveat']}"])
    if report.get("import_audit"):
        audit = report["import_audit"]
        lines.extend(
            [
                "",
                (
                    "AWS import audit: "
                    f"{audit['formula_repair_case_count']} parenthesized-formula cases use "
                    "the separately preserved expanded-formula repair run; all 100 imported "
                    "result hashes were verified against `IMPORT-AUDIT.json`."
                ),
            ]
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("framework", choices=sorted(PROFILES))
    parser.add_argument("run_root", type=Path)
    parser.add_argument("--corpus-root", type=Path, default=CORPUS)
    parser.add_argument("--dataset-id")
    parser.add_argument("--case-prefix")
    parser.add_argument("--support-policy", choices=SUPPORT_POLICIES, default="manifest")
    args = parser.parse_args()
    configure_dataset(args)
    run_root = args.run_root.resolve()
    if not run_root.is_dir():
        parser.error(f"run directory does not exist: {run_root}")
    report = evaluate(args.framework, run_root)
    print(json.dumps(report["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
