"""Evaluate Crystalyze best-of-1 and best-of-8 corpus generations.

Run this with the pinned benchmark environment so every framework is evaluated
with the same current Pymatgen semantics::

    .runs/envs/crystalyze-runtime/bin/python \
        baselines/crystalyze/evaluate.py <run-directory>
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import warnings
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np
from make_targets import axis, simulate
from pymatgen.core import Structure
from scipy.interpolate import interp1d

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

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "pxrd-bench" / "pXRD-100"
SOURCE_MANIFEST = CORPUS / "manifest.json"
TARGET_MANIFEST = framework_target_root(ROOT, "crystalyze", CORPUS) / "manifest.json"
EXPECTED_SAMPLES = 8
DATASET_ID: str | None = None
CASE_PREFIX: str | None = None
SUPPORT_POLICY = "manifest"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def model_profile(structure: Structure) -> np.ndarray:
    """Simulate and apply the same interpolation/mask consumed by the encoder."""

    physical, _ = simulate(structure, axis())
    physical_axis = axis()
    interpolator = interp1d(
        physical_axis,
        physical,
        kind="cubic",
        bounds_error=False,
        fill_value=0,
    )
    values = np.asarray(interpolator(np.linspace(5, 90, 8500)), dtype=np.float64)
    maximum = float(np.max(values))
    if not math.isfinite(maximum) or maximum <= 0:
        raise ValueError("simulated model profile is empty or non-finite")
    values /= maximum
    values[:1000] = 0
    return values


def load_target_profile(case: dict[str, Any]) -> np.ndarray:
    values = np.loadtxt(
        TARGET_MANIFEST.parent / case["pattern_path"],
        delimiter=",",
        skiprows=1,
    )
    interpolator = interp1d(
        values[:, 0],
        values[:, 1],
        kind="cubic",
        bounds_error=False,
        fill_value=0,
    )
    profile = np.asarray(interpolator(np.linspace(5, 90, 8500)), dtype=np.float64)
    profile /= float(np.max(profile))
    profile[:1000] = 0
    return profile


def cosine_similarity(left: np.ndarray, right: np.ndarray) -> float:
    denominator = float(np.linalg.norm(left) * np.linalg.norm(right))
    if denominator == 0:
        return float("nan")
    return float(np.dot(left, right) / denominator)


def minimum_periodic_distance(structure: Structure) -> float:
    if len(structure) < 2:
        return float("inf")
    distances = np.asarray(structure.distance_matrix, dtype=np.float64)
    distances += np.diag(np.full(len(structure), 10.5))
    return float(np.min(distances))


def source_cases() -> dict[str, dict[str, Any]]:
    _, cases = validate_source_manifest(
        load_json(SOURCE_MANIFEST),
        expected_cases=100,
        dataset_id=DATASET_ID,
        case_prefix=CASE_PREFIX,
    )
    return {case["case_id"]: case for case in cases}


def target_cases() -> dict[str, dict[str, Any]]:
    manifest = load_json(TARGET_MANIFEST)
    source_dataset_id = load_json(SOURCE_MANIFEST)["dataset_id"]
    if manifest.get("source_dataset_id", source_dataset_id) != source_dataset_id:
        raise RuntimeError("Crystalyze target dataset identity mismatch")
    if manifest.get("case_prefix") != CASE_PREFIX:
        raise RuntimeError("Crystalyze target case-prefix contract mismatch")
    if manifest.get("support_policy", "manifest") != SUPPORT_POLICY:
        raise RuntimeError("Crystalyze target support-policy contract mismatch")
    if manifest["source_manifest_sha256"] != sha256_file(SOURCE_MANIFEST):
        raise RuntimeError("Crystalyze target manifest is stale")
    return {case["case_id"]: case for case in manifest["cases"]}


def configure_dataset(args: argparse.Namespace) -> None:
    global CORPUS, SOURCE_MANIFEST, TARGET_MANIFEST
    global DATASET_ID, CASE_PREFIX, SUPPORT_POLICY
    CORPUS = args.corpus_root.expanduser().resolve()
    SOURCE_MANIFEST = CORPUS / "manifest.json"
    TARGET_MANIFEST = framework_target_root(ROOT, "crystalyze", CORPUS) / "manifest.json"
    DATASET_ID = args.dataset_id
    CASE_PREFIX = args.case_prefix
    SUPPORT_POLICY = args.support_policy


def candidate_manifests(
    run_root: Path, source_digest: str, source_dataset_id: str
) -> tuple[dict[str, tuple[Path, dict[str, Any]]], list[dict[str, Any]], dict[str, int]]:
    indexed: dict[str, tuple[Path, dict[str, Any]]] = {}
    shards: list[dict[str, Any]] = []
    audit = {"candidate_hashes_checked": 0, "raw_hashes_checked": 0}
    for result_path in sorted(run_root.glob("shard-*/results.json")):
        result = load_json(result_path)
        shards.append(result)
        if result.get("framework") != "Crystalyze":
            raise RuntimeError(f"unexpected framework in {result_path}")
        if int(result["samples_per_case"]) != EXPECTED_SAMPLES:
            raise RuntimeError(f"unexpected sample count in {result_path}")
        if result.get("source_manifest_sha256") != source_digest:
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
            indexed[key] = (shard_root, candidate)
    return indexed, shards, audit


def evaluate(run_root: Path, *, profile_diagnostics: bool) -> dict[str, Any]:
    sources = source_cases()
    targets = target_cases()
    source_digest = sha256_file(SOURCE_MANIFEST)
    source_dataset_id = str(load_json(SOURCE_MANIFEST)["dataset_id"])
    candidates, shards, artifact_audit = candidate_manifests(
        run_root, source_digest, source_dataset_id
    )
    matcher = primary_matcher()
    case_rows: list[dict[str, Any]] = []
    candidate_rows: list[dict[str, Any]] = []

    supported_ids = [case_id for case_id, case in targets.items() if case["model_supported"]]
    target_manifest = load_json(TARGET_MANIFEST)
    if len(supported_ids) != int(target_manifest["supported_case_count"]):
        raise RuntimeError("supported target count disagrees with target manifest")
    expected_keys = {
        f"{case_id}:{sample}" for case_id in supported_ids for sample in range(EXPECTED_SAMPLES)
    }
    if set(candidates) != expected_keys:
        missing = sorted(expected_keys - set(candidates))
        extra = sorted(set(candidates) - expected_keys)
        raise RuntimeError(f"incomplete run: missing={missing[:8]}, extra={extra[:8]}")

    for case_id in supported_ids:
        target_case = targets[case_id]
        source_case = sources[case_id]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            ground_truth = Structure.from_file(CORPUS / source_case["path"])
        target_profile = load_target_profile(target_case) if profile_diagnostics else None
        rows = []
        for sample_index in range(EXPECTED_SAMPLES):
            shard_root, manifest = candidates[f"{case_id}:{sample_index}"]
            candidate_path = shard_root / manifest["candidate_path"]
            row: dict[str, Any] = {
                "case_id": case_id,
                "panel": source_case["panel"],
                "stream": source_case.get("stream"),
                "sample_index": sample_index,
                "status": manifest["status"],
                "candidate_path": str(candidate_path.relative_to(run_root)),
                "target_formula": source_case["formula"],
                "predicted_formula": manifest.get("predicted_formula"),
                "formula_match": False,
                "structure_valid": False,
                "structure_match": False,
                "matcher_rms": None,
                "matcher_max_dist": None,
                "minimum_periodic_distance_angstrom": None,
                "evaluation_error": None,
                "input_profile_cosine": None,
                "input_profile_rmse": None,
                "profile_error": None,
            }
            if manifest["status"] == "generated" and candidate_path.suffix == ".cif":
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    predicted = Structure.from_file(candidate_path)
                row["formula_match"] = element_composition_match(predicted, ground_truth)
                minimum_distance = minimum_periodic_distance(predicted)
                row["minimum_periodic_distance_angstrom"] = minimum_distance
                row["structure_valid"] = bool(
                    predicted.volume >= 0.1
                    and (minimum_distance is None or minimum_distance >= 0.5)
                )
                if row["formula_match"] and row["structure_valid"]:
                    try:
                        matched, distances = primary_structure_match(
                            predicted,
                            ground_truth,
                            matcher,
                        )
                    except Exception as exc:
                        matched, distances = False, None
                        row["evaluation_error"] = f"StructureMatcher {type(exc).__name__}: {exc}"
                    row["structure_match"] = matched
                    if matched and distances is not None:
                        row["matcher_rms"] = float(distances[0])
                        row["matcher_max_dist"] = float(distances[1])
                if profile_diagnostics and target_profile is not None:
                    try:
                        predicted_profile = model_profile(predicted)
                        row["input_profile_cosine"] = cosine_similarity(
                            predicted_profile, target_profile
                        )
                        row["input_profile_rmse"] = float(
                            np.sqrt(np.mean(np.square(predicted_profile - target_profile)))
                        )
                    except Exception as exc:
                        row["profile_error"] = str(exc)
            rows.append(row)
            candidate_rows.append(row)

        matched = [row for row in rows if row["structure_match"]]
        valid_profile_rows = [
            row
            for row in rows
            if isinstance(row["input_profile_cosine"], float)
            and math.isfinite(row["input_profile_cosine"])
        ]
        best_profile = (
            max(valid_profile_rows, key=lambda row: row["input_profile_cosine"])
            if valid_profile_rows
            else None
        )
        case_rows.append(
            {
                "case_id": case_id,
                "panel": source_case["panel"],
                "stream": source_case.get("stream"),
                "target_formula": source_case["formula"],
                "best_of_1_structure_match": bool(rows[0]["structure_match"]),
                "best_of_8_structure_match": bool(matched),
                "best_of_1_formula_match": bool(rows[0]["formula_match"]),
                "best_of_8_formula_match": any(row["formula_match"] for row in rows),
                "best_of_1_input_profile_cosine": rows[0]["input_profile_cosine"],
                "best_of_8_input_profile_cosine": (
                    best_profile["input_profile_cosine"] if best_profile else None
                ),
                "best_of_8_profile_sample_index": (
                    int(best_profile["sample_index"]) if best_profile else None
                ),
                "matched_sample_indices": [int(row["sample_index"]) for row in matched],
                "best_match_rms": (
                    min(float(row["matcher_rms"]) for row in matched) if matched else None
                ),
            }
        )

    summary = summarize(case_rows, candidate_rows, targets)
    write_csv(run_root / "evaluation-cases.csv", case_rows)
    write_csv(run_root / "evaluation-candidates.csv", candidate_rows)
    report = {
        "schema_version": "1.1.0",
        "source_dataset_id": source_dataset_id,
        "run_id": run_root.name,
        "source_manifest_sha256": source_digest,
        "conditioning": "pXRD plus supplied element set; stoichiometric counts not enforced",
        "artifact_audit": {
            **artifact_audit,
            "hash_mismatch_count": 0,
            "missing_or_extra_candidate_count": 0,
        },
        "metric": {
            "structure_matcher": primary_metric_metadata(),
            "formula_match": formula_metric_metadata(),
            "structure_validity": {"minimum_distance_angstrom": 0.5, "volume_min": 0.1},
            "best_of_1": "candidate sample_index 0",
            "best_of_8": "oracle over sample_index 0 through 7",
            "profile_diagnostic": (
                "Crystalyze encoder-input cosine after paper simulation and upstream mask"
                if profile_diagnostics
                else "not computed"
            ),
        },
        "generation": {
            "shard_count": len(shards),
            "aggregate_container_seconds": sum(
                float(shard["runtime"]["total_seconds"]) for shard in shards
            ),
            "first_shard_provenance": {
                key: shards[0][key]
                for key in ("framework_commit", "checkpoint_sha256", "inference")
                if key in shards[0]
            },
        },
        "summary": summary,
        "cases": case_rows,
    }
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
    write_readme(run_root / "EVALUATION.md", summary, profile_diagnostics)
    write_readme(run_root / "RUN.md", summary, profile_diagnostics)
    return report


def summarize(
    case_rows: list[dict[str, Any]],
    candidate_rows: list[dict[str, Any]],
    targets: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    def aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
        count = len(rows)
        bof1 = sum(bool(row["best_of_1_structure_match"]) for row in rows)
        bof8 = sum(bool(row["best_of_8_structure_match"]) for row in rows)
        formula1 = sum(bool(row["best_of_1_formula_match"]) for row in rows)
        formula8 = sum(bool(row["best_of_8_formula_match"]) for row in rows)
        return {
            "case_count": count,
            "best_of_1_structure_match_count": bof1,
            "best_of_1_structure_match_rate": bof1 / count if count else None,
            "best_of_8_structure_match_count": bof8,
            "best_of_8_structure_match_rate": bof8 / count if count else None,
            "best_of_1_formula_match_count": formula1,
            "best_of_1_formula_match_rate": formula1 / count if count else None,
            "best_of_8_formula_match_count": formula8,
            "best_of_8_formula_match_rate": formula8 / count if count else None,
        }

    by_panel: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_stream: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in case_rows:
        by_panel[str(row["panel"])].append(row)
        if row.get("stream"):
            by_stream[str(row["stream"])].append(row)
    unsupported = [case for case in targets.values() if not case["model_supported"]]
    statuses = Counter(str(row["status"]) for row in candidate_rows)
    return {
        "supported": aggregate(case_rows),
        "panels": {panel: aggregate(rows) for panel, rows in sorted(by_panel.items())},
        "streams": {stream: aggregate(rows) for stream, rows in sorted(by_stream.items())},
        "unsupported_case_count": len(unsupported),
        "unsupported_case_ids": [case["case_id"] for case in unsupported],
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


def write_readme(path: Path, summary: dict[str, Any], profiles: bool) -> None:
    supported = summary["supported"]
    lines = [
        "# Crystalyze evaluation",
        "",
        "Primary exact-recovery success uses Pymatgen `StructureMatcher` with ",
        "`ltol=0.2`, `stol=0.3`, `angle_tol=5`, exact cell scale, symmetric ",
        "element-aware fitting, and commensurate-supercell support. Candidate 1 is best-of-1; ",
        "best-of-8 is an oracle over all eight independently sampled candidates.",
        "",
        "| Metric | Best-of-1 | Best-of-8 |",
        "|---|---:|---:|",
        (
            "| Structure match | "
            f"{supported['best_of_1_structure_match_count']}/{supported['case_count']} "
            f"({supported['best_of_1_structure_match_rate']:.1%}) | "
            f"{supported['best_of_8_structure_match_count']}/{supported['case_count']} "
            f"({supported['best_of_8_structure_match_rate']:.1%}) |"
        ),
        (
            "| Reduced-formula match | "
            f"{supported['best_of_1_formula_match_count']}/{supported['case_count']} "
            f"({supported['best_of_1_formula_match_rate']:.1%}) | "
            f"{supported['best_of_8_formula_match_count']}/{supported['case_count']} "
            f"({supported['best_of_8_formula_match_rate']:.1%}) |"
        ),
        "",
        f"Unsupported cases: {summary['unsupported_case_count']}. ",
        f"Encoder-input pXRD diagnostics were {'computed' if profiles else 'not computed'}.",
        "",
    ]
    lines.extend(
        [
            "## Structure matches by panel",
            "",
            "| Panel | Cases | Best-of-1 | Best-of-8 |",
            "|---|---:|---:|---:|",
        ]
    )
    for panel, values in summary["panels"].items():
        lines.append(
            f"| {panel} | {values['case_count']} | "
            f"{values['best_of_1_structure_match_count']} | "
            f"{values['best_of_8_structure_match_count']} |"
        )
    if summary.get("streams"):
        lines.extend(
            [
                "",
                "## Structure matches by generation stream",
                "",
                "| Stream | Cases | Best-of-1 | Best-of-8 |",
                "|---|---:|---:|---:|",
            ]
        )
        for stream, values in summary["streams"].items():
            lines.append(
                f"| {stream} | {values['case_count']} | "
                f"{values['best_of_1_structure_match_count']} | "
                f"{values['best_of_8_structure_match_count']} |"
            )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_root", type=Path)
    parser.add_argument("--corpus-root", type=Path, default=CORPUS)
    parser.add_argument("--dataset-id")
    parser.add_argument("--case-prefix")
    parser.add_argument("--support-policy", choices=SUPPORT_POLICIES, default="manifest")
    parser.add_argument(
        "--skip-profile-diagnostics",
        action="store_true",
        help="Only compute formula and StructureMatcher outcomes.",
    )
    args = parser.parse_args()
    configure_dataset(args)
    run_root = args.run_root.resolve()
    report = evaluate(run_root, profile_diagnostics=not args.skip_profile_diagnostics)
    print(json.dumps(report["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
