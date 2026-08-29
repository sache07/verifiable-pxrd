#!/usr/bin/env python3
"""Build and validate release-facing bundles from the frozen baseline runs."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import tarfile
import tempfile
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from verifiable_pxrd.baselines.candidates import materialize_case_candidates

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = REPOSITORY_ROOT / "results" / "baselines"
ARCHIVE_NAME = "candidates.tar.zst"
TEXT_FILES = {".cif", ".csv", ".json", ".log", ".md", ".txt"}
FORBIDDEN_PUBLIC_TEXT = (
    "/home/",
    "/users/",
    "AWS_SECRET_ACCESS_KEY",
    "authorization: bearer",
    "sk-proj-",
)


@dataclass(frozen=True)
class RunSpec:
    framework_slug: str
    framework: str
    corpus_slug: str
    corpus: str
    condition_slug: str
    condition: str
    source_relative_path: str
    input_contract: str
    oracle_input: bool
    generated_k: int
    reported_k: int
    publish_archive: bool = True
    archive_exclusion_reason: str | None = None

    @property
    def bundle_relative_path(self) -> Path:
        return Path(self.framework_slug) / self.corpus_slug / self.condition_slug


RUN_SPECS = (
    RunSpec(
        "crystalyze",
        "Crystalyze",
        "pxrd-100",
        "pXRD-100",
        "element-set-k8",
        "element-set conditioning",
        "pXRD-100/results/crystalyze/crystalyze-20260720-v2-fourway-bof8-t4",
        "pXRD and supplied element set",
        False,
        8,
        8,
    ),
    RunSpec(
        "crystalyze",
        "Crystalyze",
        "pxrd-ood",
        "pXRD-ood",
        "element-set-k8",
        "element-set conditioning",
        "pXRD-ood/results/crystalyze/crystalyze-20260720-ood-paper-bof8-t4",
        "pXRD and supplied element set",
        False,
        8,
        8,
    ),
    RunSpec(
        "decifer",
        "deCIFer",
        "pxrd-100",
        "pXRD-100",
        "reduced-composition-k8",
        "reduced-composition conditioning",
        "pXRD-100/results/decifer/decifer-20260720-v2-fourway-reduced-bof8-l4",
        "pXRD and reduced composition",
        False,
        8,
        8,
    ),
    RunSpec(
        "decifer",
        "deCIFer",
        "pxrd-ood",
        "pXRD-ood",
        "reduced-composition-k8",
        "reduced-composition conditioning",
        "pXRD-ood/results/decifer/decifer-20260720-ood-paper-bof8-l4",
        "pXRD and reduced composition",
        False,
        8,
        8,
    ),
    RunSpec(
        "decifer",
        "deCIFer",
        "pxrd-100",
        "pXRD-100",
        "known-conventional-z-k8",
        "known conventional-cell Z",
        "pXRD-100/results/decifer/decifer-20260720-v2-fourway-full-cell-oracle-bof8-l4",
        "pXRD, composition, and known conventional-cell Z",
        True,
        8,
        8,
    ),
    RunSpec(
        "decifer",
        "deCIFer",
        "pxrd-ood",
        "pXRD-ood",
        "known-conventional-z-k8",
        "known conventional-cell Z",
        "pXRD-ood/results/decifer/decifer-20260720-ood-full-cell-oracle-bof8-l4",
        "pXRD, composition, and known conventional-cell Z",
        True,
        8,
        8,
    ),
    RunSpec(
        "pxrdgen",
        "PXRDGen",
        "pxrd-100",
        "pXRD-100",
        "known-primitive-z-k8",
        "known primitive-cell Z",
        "pXRD-100/results/pxrdgen/pxrdgen-20260720-v2-fourway-primitive-oracle-bof8-raw-l4",
        "pXRD, composition, and known primitive-cell Z",
        True,
        8,
        8,
    ),
    RunSpec(
        "pxrdgen",
        "PXRDGen",
        "pxrd-ood",
        "pXRD-ood",
        "known-primitive-z-k8",
        "known primitive-cell Z",
        "pXRD-ood/results/pxrdgen/pxrdgen-20260720-ood-primitive-oracle-bof8-raw-l4",
        "pXRD, composition, and known primitive-cell Z",
        True,
        8,
        8,
    ),
    RunSpec(
        "diffractgpt",
        "DiffractGPT",
        "pxrd-100",
        "pXRD-100",
        "reduced-composition-greedy-k1",
        "single greedy decode",
        "pXRD-100/results/diffractgpt/diffractgpt-20260720-v2-fourway-paper-greedy-l4",
        "pXRD and reduced composition",
        False,
        1,
        1,
        False,
        "Generated artifacts are withheld pending clarification of the adapter's redistribution license.",
    ),
    RunSpec(
        "diffractgpt",
        "DiffractGPT",
        "pxrd-ood",
        "pXRD-ood",
        "reduced-composition-greedy-k1",
        "single greedy decode",
        "pXRD-ood/results/diffractgpt/diffractgpt-20260720-ood-paper-greedy-l4",
        "pXRD and reduced composition",
        False,
        1,
        1,
        False,
        "Generated artifacts are withheld pending clarification of the adapter's redistribution license.",
    ),
    RunSpec(
        "ab-pxrd-solver",
        "Ab-PXRD-Solver",
        "pxrd-100",
        "pXRD-100",
        "reduced-composition-k1",
        "reduced-composition solver",
        "pXRD-100/results/ab-pxrd-solver/ab-pxrd-solver-20260722-v2-fourway-reduced-cpu4h",
        "pXRD and reduced composition",
        False,
        1,
        1,
    ),
    RunSpec(
        "ab-pxrd-solver",
        "Ab-PXRD-Solver",
        "pxrd-ood",
        "pXRD-ood",
        "reduced-composition-k1",
        "reduced-composition solver",
        "pXRD-ood/results/ab-pxrd-solver/ab-pxrd-solver-20260722-ood-reduced-cpu4h",
        "pXRD and reduced composition",
        False,
        1,
        1,
    ),
    RunSpec(
        "realpxrd-solver",
        "RealPXRD-Solver",
        "pxrd-100",
        "pXRD-100",
        "known-primitive-z-k20",
        "known primitive-cell Z",
        "pXRD-100/results/realpxrd-solver/realpxrd-pxrd100-lattice-free-oracle-20260824",
        "pXRD, composition, and known primitive-cell Z",
        True,
        20,
        8,
    ),
    RunSpec(
        "realpxrd-solver",
        "RealPXRD-Solver",
        "pxrd-ood",
        "pXRD-ood",
        "known-primitive-z-k20",
        "known primitive-cell Z",
        "pXRD-ood/results/realpxrd-solver/realpxrd-ood-lattice-free-oracle-20260809",
        "pXRD, composition, and known primitive-cell Z",
        True,
        20,
        8,
    ),
)

CANDIDATE_COLUMNS = (
    "case_id",
    "panel",
    "stream",
    "sample_index",
    "status",
    "candidate_path",
    "verifier_result_path",
    "candidate_member",
    "candidate_sha256",
    "raw_member",
    "raw_sha256",
    "shard_results_member",
    "artifacts_published",
    "input_mode",
    "seed",
    "runtime_seconds",
    "target_formula",
    "predicted_formula",
    "formula_match",
    "target_full_cell_formula",
    "full_cell_composition_match",
    "structure_valid",
    "structure_match",
    "matcher_rms",
    "matcher_max_dist",
    "minimum_periodic_distance_angstrom",
    "evaluation_error",
    "solver_status",
    "upstream_outcome",
)

CASE_COLUMNS = (
    "case_id",
    "panel",
    "stream",
    "target_formula",
    "generated_k",
    "reported_k",
    "candidate_record_count",
    "generated_candidate_count",
    "valid_structure_candidate_count",
    "best_of_1_formula_match",
    "best_of_reported_k_formula_match",
    "best_of_generated_k_formula_match",
    "best_of_1_full_cell_composition_match",
    "best_of_reported_k_full_cell_composition_match",
    "best_of_generated_k_full_cell_composition_match",
    "best_of_1_structure_match",
    "best_of_reported_k_structure_match",
    "best_of_generated_k_structure_match",
    "reported_matched_sample_indices",
    "all_matched_sample_indices",
    "best_reported_match_rms",
    "best_generated_match_rms",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError(f"expected a JSON object: {path}")
    return payload


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, columns: tuple[str, ...], rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def clean_cell(value: Any) -> str:
    """Keep generated CSV records single-line while preserving visible error text."""

    if value is None:
        return ""
    return (
        str(value)
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .replace("\n", "\\n")
        .strip()
    )


def relative_member(shard: str, value: Any) -> str:
    if not value:
        return ""
    member = Path(shard) / str(value)
    if member.is_absolute() or ".." in member.parts:
        raise RuntimeError(f"unsafe artifact member: {member}")
    return member.as_posix()


def validate_source_artifact(root: Path, member: str, expected_sha256: str) -> None:
    path = root / member
    if not path.is_file():
        raise RuntimeError(f"missing source artifact: {path}")
    actual = sha256_file(path)
    if actual != expected_sha256:
        raise RuntimeError(f"source artifact hash mismatch: {path}")


def read_candidate_rows(spec: RunSpec, source: Path) -> list[dict[str, Any]]:
    artifact_records: dict[tuple[str, int], tuple[str, dict[str, Any]]] = {}
    shard_paths = sorted(path for path in source.iterdir() if re.fullmatch(r"shard-\d+", path.name))
    if not shard_paths:
        raise RuntimeError(f"no source shards: {source}")
    for shard in shard_paths:
        result_path = shard / "results.json"
        request_path = shard / "request.json"
        if not result_path.is_file() or not request_path.is_file():
            raise RuntimeError(f"incomplete source shard: {shard}")
        payload = load_json(result_path)
        for record in payload.get("candidates", []):
            key = (str(record["case_id"]), int(record["sample_index"]))
            if key in artifact_records:
                raise RuntimeError(f"duplicate source candidate: {key}")
            artifact_records[key] = (shard.name, record)

    evaluation_path = source / "evaluation-candidates.csv"
    with evaluation_path.open(encoding="utf-8", newline="") as stream:
        evaluation_rows = list(csv.DictReader(stream))
    if len(evaluation_rows) != len(artifact_records):
        raise RuntimeError(
            f"candidate index mismatch for {source}: "
            f"evaluation={len(evaluation_rows)}, artifacts={len(artifact_records)}"
        )

    normalized: list[dict[str, Any]] = []
    for evaluation in evaluation_rows:
        key = (str(evaluation["case_id"]), int(evaluation["sample_index"]))
        if key not in artifact_records:
            raise RuntimeError(f"evaluation candidate is missing from source shards: {key}")
        shard, record = artifact_records[key]
        if str(record["status"]) != str(evaluation["status"]):
            raise RuntimeError(f"candidate status mismatch: {key}")
        candidate_member = relative_member(shard, record["candidate_path"])
        if candidate_member != str(evaluation["candidate_path"]):
            raise RuntimeError(f"candidate path mismatch: {key}")
        candidate_sha256 = str(record["candidate_sha256"])
        validate_source_artifact(source, candidate_member, candidate_sha256)

        raw_member = relative_member(shard, record.get("raw_path"))
        raw_sha256 = str(record.get("raw_sha256") or "")
        if bool(raw_member) != bool(raw_sha256):
            raise RuntimeError(f"incomplete raw artifact identity: {key}")
        if raw_member:
            validate_source_artifact(source, raw_member, raw_sha256)

        runtime = (
            record.get("runtime_seconds_case_batch")
            or record.get("runtime_seconds_batch_share")
            or record.get("runtime_seconds")
            or ""
        )
        normalized.append(
            {
                "case_id": key[0],
                "panel": clean_cell(evaluation.get("panel")),
                "stream": clean_cell(evaluation.get("stream")),
                "sample_index": key[1],
                "status": clean_cell(record["status"]),
                "candidate_path": "",
                "verifier_result_path": "",
                "candidate_member": candidate_member,
                "candidate_sha256": candidate_sha256,
                "raw_member": raw_member,
                "raw_sha256": raw_sha256,
                "shard_results_member": f"{shard}/results.json",
                "artifacts_published": bool_text(spec.publish_archive),
                "input_mode": clean_cell(record.get("input_mode")),
                "seed": record.get("seed", ""),
                "runtime_seconds": runtime,
                "target_formula": clean_cell(evaluation.get("target_formula")),
                "predicted_formula": clean_cell(evaluation.get("predicted_formula")),
                "formula_match": bool_text(parse_bool(evaluation.get("formula_match"))),
                "target_full_cell_formula": clean_cell(
                    evaluation.get("target_full_cell_formula")
                ),
                "full_cell_composition_match": bool_text(
                    parse_bool(evaluation.get("full_cell_composition_match"))
                ),
                "structure_valid": bool_text(parse_bool(evaluation.get("structure_valid"))),
                "structure_match": bool_text(parse_bool(evaluation.get("structure_match"))),
                "matcher_rms": evaluation.get("matcher_rms", ""),
                "matcher_max_dist": evaluation.get("matcher_max_dist", ""),
                "minimum_periodic_distance_angstrom": evaluation.get(
                    "minimum_periodic_distance_angstrom", ""
                ),
                "evaluation_error": clean_cell(evaluation.get("evaluation_error")),
                "solver_status": clean_cell(evaluation.get("solver_status")),
                "upstream_outcome": clean_cell(evaluation.get("upstream_outcome")),
            }
        )
    return sorted(normalized, key=lambda row: (str(row["case_id"]), int(row["sample_index"])))


def minimum_rms(rows: list[dict[str, Any]]) -> str:
    values = [
        float(row["matcher_rms"])
        for row in rows
        if parse_bool(row["structure_match"]) and str(row["matcher_rms"]).strip()
    ]
    return "" if not values else repr(min(values))


def build_case_rows(spec: RunSpec, candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in candidates:
        grouped[str(row["case_id"])].append(row)
    if len(grouped) != 100:
        raise RuntimeError(f"expected 100 cases for {spec.bundle_relative_path}, found {len(grouped)}")

    rows: list[dict[str, Any]] = []
    for case_id, case_candidates in sorted(grouped.items()):
        case_candidates.sort(key=lambda row: int(row["sample_index"]))
        observed_indices = [int(row["sample_index"]) for row in case_candidates]
        if observed_indices != list(range(spec.generated_k)):
            raise RuntimeError(f"non-contiguous candidate indices for {case_id}: {observed_indices}")
        first = case_candidates[:1]
        reported = case_candidates[: spec.reported_k]
        generated = case_candidates[: spec.generated_k]

        def any_match(subset: list[dict[str, Any]], key: str) -> bool:
            return any(parse_bool(row[key]) for row in subset)

        reported_matches = [
            int(row["sample_index"]) for row in reported if parse_bool(row["structure_match"])
        ]
        all_matches = [
            int(row["sample_index"]) for row in generated if parse_bool(row["structure_match"])
        ]
        rows.append(
            {
                "case_id": case_id,
                "panel": case_candidates[0]["panel"],
                "stream": case_candidates[0]["stream"],
                "target_formula": case_candidates[0]["target_formula"],
                "generated_k": spec.generated_k,
                "reported_k": spec.reported_k,
                "candidate_record_count": len(case_candidates),
                "generated_candidate_count": sum(
                    str(row["status"]) == "generated" for row in generated
                ),
                "valid_structure_candidate_count": sum(
                    parse_bool(row["structure_valid"]) for row in generated
                ),
                "best_of_1_formula_match": bool_text(any_match(first, "formula_match")),
                "best_of_reported_k_formula_match": bool_text(
                    any_match(reported, "formula_match")
                ),
                "best_of_generated_k_formula_match": bool_text(
                    any_match(generated, "formula_match")
                ),
                "best_of_1_full_cell_composition_match": bool_text(
                    any_match(first, "full_cell_composition_match")
                ),
                "best_of_reported_k_full_cell_composition_match": bool_text(
                    any_match(reported, "full_cell_composition_match")
                ),
                "best_of_generated_k_full_cell_composition_match": bool_text(
                    any_match(generated, "full_cell_composition_match")
                ),
                "best_of_1_structure_match": bool_text(any_match(first, "structure_match")),
                "best_of_reported_k_structure_match": bool_text(
                    any_match(reported, "structure_match")
                ),
                "best_of_generated_k_structure_match": bool_text(
                    any_match(generated, "structure_match")
                ),
                "reported_matched_sample_indices": json.dumps(reported_matches, separators=(",", ":")),
                "all_matched_sample_indices": json.dumps(all_matches, separators=(",", ":")),
                "best_reported_match_rms": minimum_rms(reported),
                "best_generated_match_rms": minimum_rms(generated),
            }
        )
    return rows


def aggregate_results(spec: RunSpec, cases: list[dict[str, Any]]) -> dict[str, Any]:
    def count(key: str) -> int:
        return sum(parse_bool(row[key]) for row in cases)

    return {
        "case_count": len(cases),
        "candidate_record_count": sum(int(row["candidate_record_count"]) for row in cases),
        "generated_candidate_count": sum(int(row["generated_candidate_count"]) for row in cases),
        "invalid_candidate_count": sum(
            int(row["candidate_record_count"]) - int(row["generated_candidate_count"])
            for row in cases
        ),
        "valid_structure_candidate_count": sum(
            int(row["valid_structure_candidate_count"]) for row in cases
        ),
        "formula_matches_at_1": count("best_of_1_formula_match"),
        "formula_matches_at_reported_k": count("best_of_reported_k_formula_match"),
        "formula_matches_at_generated_k": count("best_of_generated_k_formula_match"),
        "exact_structure_matches_at_1": count("best_of_1_structure_match"),
        "exact_structure_matches_at_reported_k": count("best_of_reported_k_structure_match"),
        "exact_structure_matches_at_generated_k": count("best_of_generated_k_structure_match"),
        "generated_k": spec.generated_k,
        "reported_k": spec.reported_k,
    }


def source_overall_summary(source_summary: dict[str, Any]) -> dict[str, Any]:
    summary = source_summary["summary"]
    overall = summary.get("all") or summary.get("supported") or {}
    return {**summary, **overall}


def validate_against_source_summary(
    spec: RunSpec, source_summary: dict[str, Any], results: dict[str, Any]
) -> None:
    source = source_overall_summary(source_summary)
    comparisons = {
        "candidate_count": "candidate_record_count",
        "valid_structure_candidate_count": "valid_structure_candidate_count",
        "best_of_1_formula_match_count": "formula_matches_at_1",
        "best_of_1_structure_match_count": "exact_structure_matches_at_1",
    }
    for source_key, result_key in comparisons.items():
        if source_key in source and int(source[source_key]) != int(results[result_key]):
            raise RuntimeError(
                f"source summary mismatch for {spec.bundle_relative_path}: "
                f"{source_key}={source[source_key]} vs {result_key}={results[result_key]}"
            )
    generated_structure_key = f"best_of_{spec.generated_k}_structure_match_count"
    generated_formula_key = f"best_of_{spec.generated_k}_formula_match_count"
    if "best_of_k_structure_match_count" in source:
        generated_structure_key = "best_of_k_structure_match_count"
    if "best_of_k_formula_match_count" in source:
        generated_formula_key = "best_of_k_formula_match_count"
    if generated_structure_key in source and int(source[generated_structure_key]) != int(
        results["exact_structure_matches_at_generated_k"]
    ):
        raise RuntimeError(f"generated-k structure summary mismatch: {spec.bundle_relative_path}")
    if generated_formula_key in source and int(source[generated_formula_key]) != int(
        results["formula_matches_at_generated_k"]
    ):
        raise RuntimeError(f"generated-k formula summary mismatch: {spec.bundle_relative_path}")


def build_archive(source: Path, output: Path) -> dict[str, Any]:
    shards = sorted(path.name for path in source.iterdir() if re.fullmatch(r"shard-\d+", path.name))
    regular_files = sorted(
        path.relative_to(source).as_posix()
        for shard in shards
        for path in (source / shard).rglob("*")
        if path.is_file()
    )
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=".candidates.", suffix=".tar.zst.tmp", dir=output.parent
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    tar_command = [
        "tar",
        "--sort=name",
        "--mtime=@0",
        "--owner=0",
        "--group=0",
        "--numeric-owner",
        "--format=posix",
        "--pax-option=delete=atime,delete=ctime",
        "--mode=u+rwX,go+rX",
        "-cf",
        "-",
        "--",
        *shards,
    ]
    tar_process = subprocess.Popen(
        tar_command,
        cwd=source,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert tar_process.stdout is not None
    compression = subprocess.run(
        ["zstd", "-q", "-10", "--threads=1", "-f", "-o", str(temporary)],
        stdin=tar_process.stdout,
        capture_output=True,
        check=False,
    )
    tar_process.stdout.close()
    tar_stderr = tar_process.stderr.read() if tar_process.stderr is not None else b""
    tar_returncode = tar_process.wait()
    if tar_returncode != 0 or compression.returncode != 0:
        temporary.unlink(missing_ok=True)
        raise RuntimeError(
            "archive construction failed: "
            f"tar={tar_returncode} {tar_stderr.decode(errors='replace')}; "
            f"zstd={compression.returncode} {compression.stderr.decode(errors='replace')}"
        )
    os.replace(temporary, output)
    return {
        "filename": output.name,
        "sha256": sha256_file(output),
        "size_bytes": output.stat().st_size,
        "regular_file_count": len(regular_files),
        "scope": "complete frozen shard directories: requests, results, candidates, raw outputs, and logs",
    }


def bundle_readme(
    spec: RunSpec,
    run_id: str,
    results: dict[str, Any],
    candidate_directory: dict[str, Any],
    archive: dict[str, Any],
) -> str:
    lines = [
        f"# {spec.framework}: {spec.corpus}, {spec.condition}",
        "",
        f"This is the normalized presentation bundle for `{run_id}`. Artifact identities,",
        "redistributable CIF bytes, and evaluation outcomes are copied from the frozen",
        "source run without scientific postprocessing.",
        "",
        f"- Input: {spec.input_contract}.",
        f"- Oracle input: `{str(spec.oracle_input).lower()}`.",
        f"- Generated candidates per case: {spec.generated_k}.",
        f"- Paper reporting cutoff: {spec.reported_k}.",
        f"- Exact@1: {results['exact_structure_matches_at_1']}/100.",
    ]
    if spec.reported_k != 1:
        lines.append(
            f"- Exact@{spec.reported_k}: "
            f"{results['exact_structure_matches_at_reported_k']}/100."
        )
    if spec.generated_k != spec.reported_k:
        lines.append(
            f"- Exact@{spec.generated_k} over the full retained run: "
            f"{results['exact_structure_matches_at_generated_k']}/100."
        )
    lines.extend(
        [
            "",
            "Files:",
            "",
            "- `run.json`: condition, provenance, verifier, aggregate counts, and source summary.",
            "- `cases.csv`: one normalized row per benchmark case.",
            "- `candidates.csv`: one normalized row per sampled or solver candidate; sample indices are zero-based.",
            "- `candidates/<case-id>/`: generated CIFs and a `verifier-results.json` record for every case.",
            "- `artifacts.sha256`: checksums for every file in this bundle.",
        ]
    )
    if archive["published"]:
        lines.append(
            "- `candidates.tar.zst`: complete frozen execution shards retained for raw provenance."
        )
    else:
        lines.extend(
            [
                "",
                f"Generated CIFs are not redistributed: {archive['exclusion_reason']}",
                "Per-case verifier results, source paths, and SHA-256 identities remain available.",
            ]
        )
    lines.extend(
        [
            "",
            (
                "The case-first directory contains "
                f"{candidate_directory['candidate_cif_count']} CIFs and "
                f"{candidate_directory['verifier_result_file_count']} verifier-result files."
            ),
        ]
    )
    return "\n".join(lines) + "\n"


def write_artifact_manifest(bundle: Path, include_archive: bool) -> None:
    names = [
        "README.md",
        "candidates/manifest.json",
        "cases.csv",
        "candidates.csv",
        "run.json",
    ]
    if include_archive:
        names.append(ARCHIVE_NAME)
    lines = [f"{sha256_file(bundle / name)}  {name}" for name in sorted(names)]
    (bundle / "artifacts.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_bundle(spec: RunSpec, source_root: Path, output_root: Path) -> dict[str, Any]:
    source = source_root / spec.source_relative_path
    if not source.is_dir():
        raise RuntimeError(f"missing frozen source run: {source}")
    source_summary_path = source / "run-summary.json"
    evaluation_path = source / "evaluation.json"
    source_summary = load_json(source_summary_path)
    if source_summary.get("artifact_audit", {}).get("hash_mismatch_count") != 0:
        raise RuntimeError(f"source run failed its artifact audit: {source}")

    candidates = read_candidate_rows(spec, source)
    cases = build_case_rows(spec, candidates)
    results = aggregate_results(spec, cases)
    validate_against_source_summary(spec, source_summary, results)

    bundle = output_root / spec.bundle_relative_path
    bundle.mkdir(parents=True, exist_ok=True)
    materialized = materialize_case_candidates(
        source,
        bundle / "candidates",
        verifier_rows=candidates,
        verifier_metadata=source_summary.get("metric", {}),
        publish_cifs=spec.publish_archive,
    )
    materialized_by_key = {
        (str(row["case_id"]), int(row["sample_index"])): row
        for row in materialized["candidates"]
    }
    for candidate in candidates:
        key = (str(candidate["case_id"]), int(candidate["sample_index"]))
        presentation = materialized_by_key[key]
        candidate["candidate_path"] = (
            f"candidates/{presentation['candidate_path']}"
            if presentation["candidate_path"]
            else ""
        )
        candidate["verifier_result_path"] = (
            f"candidates/{candidate['case_id']}/verifier-results.json"
        )
    write_csv(bundle / "candidates.csv", CANDIDATE_COLUMNS, candidates)
    write_csv(bundle / "cases.csv", CASE_COLUMNS, cases)

    if spec.publish_archive:
        archive = {"published": True, **build_archive(source, bundle / ARCHIVE_NAME)}
    else:
        if (bundle / ARCHIVE_NAME).exists():
            raise RuntimeError(f"withheld archive unexpectedly exists: {bundle / ARCHIVE_NAME}")
        archive = {
            "published": False,
            "filename": None,
            "sha256": None,
            "size_bytes": 0,
            "regular_file_count": 0,
            "scope": None,
            "exclusion_reason": spec.archive_exclusion_reason,
        }

    run_payload = {
        "schema_version": "1.1.0",
        "framework": spec.framework,
        "framework_slug": spec.framework_slug,
        "corpus": spec.corpus,
        "corpus_slug": spec.corpus_slug,
        "condition": spec.condition,
        "condition_slug": spec.condition_slug,
        "input_contract": spec.input_contract,
        "oracle_input": spec.oracle_input,
        "sampling": {
            "generated_k": spec.generated_k,
            "reported_k": [1] if spec.reported_k == 1 else [1, spec.reported_k],
        },
        "results": results,
        "candidate_directory": {
            "path": "candidates",
            "case_count": materialized["case_count"],
            "candidate_record_count": materialized["candidate_record_count"],
            "candidate_cif_count": materialized["candidate_cif_count"],
            "verifier_result_file_count": materialized["verifier_result_file_count"],
            "cifs_published": spec.publish_archive,
            "manifest_sha256": materialized["manifest_sha256"],
        },
        "raw_run_archive": archive,
        "source": {
            "run_id": source_summary["run_id"],
            "relative_path": spec.source_relative_path,
            "source_dataset_id": source_summary["source_dataset_id"],
            "source_manifest_sha256": source_summary["source_manifest_sha256"],
            "run_summary_sha256": sha256_file(source_summary_path),
            "evaluation_sha256": sha256_file(evaluation_path),
        },
        "verifier": source_summary.get("metric"),
        "source_run_summary": source_summary,
    }
    serialized = json.dumps(run_payload, sort_keys=True)
    for forbidden in FORBIDDEN_PUBLIC_TEXT:
        if forbidden.lower() in serialized.lower():
            raise RuntimeError(f"non-public text in normalized run metadata: {forbidden}")
    write_json(bundle / "run.json", run_payload)
    (bundle / "README.md").write_text(
        bundle_readme(
            spec,
            str(source_summary["run_id"]),
            results,
            run_payload["candidate_directory"],
            archive,
        ),
        encoding="utf-8",
    )
    write_artifact_manifest(bundle, spec.publish_archive)

    expected_files = {
        "README.md",
        "artifacts.sha256",
        "cases.csv",
        "candidates.csv",
        "run.json",
    }
    if spec.publish_archive:
        expected_files.add(ARCHIVE_NAME)
    observed_files = {path.name for path in bundle.iterdir() if path.is_file()}
    if observed_files != expected_files:
        raise RuntimeError(f"unexpected bundle files in {bundle}: {observed_files - expected_files}")
    return {
        "framework": spec.framework,
        "framework_slug": spec.framework_slug,
        "corpus": spec.corpus,
        "corpus_slug": spec.corpus_slug,
        "condition": spec.condition,
        "condition_slug": spec.condition_slug,
        "bundle_path": spec.bundle_relative_path.as_posix(),
        "run_id": source_summary["run_id"],
        "oracle_input": spec.oracle_input,
        "generated_k": spec.generated_k,
        "reported_k": spec.reported_k,
        "exact_structure_matches_at_1": results["exact_structure_matches_at_1"],
        "exact_structure_matches_at_reported_k": results[
            "exact_structure_matches_at_reported_k"
        ],
        "exact_structure_matches_at_generated_k": results[
            "exact_structure_matches_at_generated_k"
        ],
        "candidate_record_count": results["candidate_record_count"],
        "candidate_cif_count": materialized["candidate_cif_count"],
        "candidate_archive_published": spec.publish_archive,
        "artifacts_sha256": sha256_file(bundle / "artifacts.sha256"),
    }


def framework_readme(framework: str, records: list[dict[str, Any]]) -> str:
    lines = [
        f"# {framework} results",
        "",
        "| Corpus | Condition | Exact@1 | Exact@reported-k | Bundle |",
        "| --- | --- | ---: | ---: | --- |",
    ]
    for record in records:
        link = f"{record['corpus_slug']}/{record['condition_slug']}/"
        lines.append(
            f"| {record['corpus']} | {record['condition']} | "
            f"{record['exact_structure_matches_at_1']}/100 | "
            f"{record['exact_structure_matches_at_reported_k']}/100 | "
            f"[`{record['run_id']}`]({link}) |"
        )
    return "\n".join(lines) + "\n"


def root_readme(records: list[dict[str, Any]]) -> str:
    lines = [
        "# Baseline results",
        "",
        "These are normalized, auditable bundles for the non-agent comparison methods in",
        "the paper. Every reported run provides a common `run.json`, case index, candidate",
        "index, and checksum manifest. Each condition exposes generated CIFs and verifier",
        "outcomes under `candidates/<case-id>/`; compressed archives retain the untouched",
        "execution shards as secondary provenance.",
        "",
        "| Framework | Corpus | Condition | Exact@1 | Exact@reported-k | CIFs | Raw archive |",
        "| --- | --- | --- | ---: | ---: | ---: | --- |",
    ]
    for record in records:
        path = record["bundle_path"]
        archive = "included" if record["candidate_archive_published"] else "withheld"
        lines.append(
            f"| [{record['framework']}]({path}/) | {record['corpus']} | "
            f"{record['condition']} | {record['exact_structure_matches_at_1']}/100 | "
            f"{record['exact_structure_matches_at_reported_k']}/100 | "
            f"{record['candidate_cif_count']} | {archive} |"
        )
    lines.extend(
        [
            "RealPXRD-Solver retains 20 generated candidates per case, while the paper reports",
            "the common first/best-eight cutoff. Both values are explicit in its `cases.csv` and",
            "`run.json`. DiffractGPT candidate files are withheld pending redistribution-license",
            "clarification; their identities and evaluation outcomes remain indexed.",
            "",
            "This directory is the canonical framework-by-framework evidence surface.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_all(source_root: Path, output_root: Path) -> None:
    output_root.mkdir(parents=True, exist_ok=True)
    records = [build_bundle(spec, source_root, output_root) for spec in RUN_SPECS]
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    names: dict[str, str] = {}
    for record in records:
        slug = str(record["framework_slug"])
        grouped[slug].append(record)
        names[slug] = str(record["framework"])
    for slug, framework_records in grouped.items():
        framework_root = output_root / slug
        (framework_root / "README.md").write_text(
            framework_readme(names[slug], framework_records), encoding="utf-8"
        )
    manifest = {
        "schema_version": "1.1.0",
        "bundle_count": len(records),
        "bundles": records,
    }
    write_json(output_root / "manifest.json", manifest)
    (output_root / "README.md").write_text(root_readme(records), encoding="utf-8")


def read_checksum_manifest(path: Path) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        digest, separator, name = line.partition("  ")
        if not separator or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise RuntimeError(f"malformed checksum line: {path}: {line}")
        rows[name] = digest
    return rows


def validate_archive(bundle: Path, run: dict[str, Any], candidates: list[dict[str, str]]) -> None:
    archive = bundle / ARCHIVE_NAME
    metadata = run["raw_run_archive"]
    if sha256_file(archive) != metadata["sha256"]:
        raise RuntimeError(f"archive hash mismatch: {archive}")
    expected_hashes: dict[str, str] = {}
    for row in candidates:
        expected_hashes[row["candidate_member"]] = row["candidate_sha256"]
        if row["raw_member"]:
            expected_hashes[row["raw_member"]] = row["raw_sha256"]

    process = subprocess.Popen(
        ["zstd", "-q", "-dc", str(archive)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdout is not None
    observed: set[str] = set()
    regular_file_count = 0
    with tarfile.open(fileobj=process.stdout, mode="r|") as tar:
        for member in tar:
            name = member.name.removeprefix("./")
            path = Path(name)
            if path.is_absolute() or ".." in path.parts or not re.fullmatch(r"shard-\d+", path.parts[0]):
                raise RuntimeError(f"unsafe archive member: {archive}: {name}")
            if not member.isfile():
                continue
            regular_file_count += 1
            extracted = tar.extractfile(member)
            if extracted is None:
                raise RuntimeError(f"failed to read archive member: {archive}: {name}")
            digest = hashlib.sha256()
            text_payload = bytearray() if path.suffix.lower() in TEXT_FILES else None
            while chunk := extracted.read(1024 * 1024):
                digest.update(chunk)
                if text_payload is not None:
                    text_payload.extend(chunk)
            if name in expected_hashes:
                if digest.hexdigest() != expected_hashes[name]:
                    raise RuntimeError(f"candidate hash mismatch inside archive: {archive}: {name}")
                observed.add(name)
            if text_payload is not None:
                decoded = text_payload.decode("utf-8", errors="replace").lower()
                for forbidden in FORBIDDEN_PUBLIC_TEXT:
                    if forbidden.lower() in decoded:
                        raise RuntimeError(f"non-public text inside archive: {archive}: {name}")
    process.stdout.close()
    stderr = process.stderr.read() if process.stderr is not None else b""
    returncode = process.wait()
    if returncode != 0:
        raise RuntimeError(f"zstd validation failed: {archive}: {stderr.decode(errors='replace')}")
    if observed != set(expected_hashes):
        missing = sorted(set(expected_hashes) - observed)
        raise RuntimeError(f"indexed artifacts missing from archive {archive}: {missing[:5]}")
    if regular_file_count != int(metadata["regular_file_count"]):
        raise RuntimeError(f"archive file-count mismatch: {archive}")


def safe_bundle_member(bundle: Path, value: str) -> Path:
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        raise RuntimeError(f"unsafe bundle member: {bundle}: {value}")
    path = (bundle / relative).resolve()
    if path == bundle.resolve() or not path.is_relative_to(bundle.resolve()):
        raise RuntimeError(f"bundle member escapes its bundle: {bundle}: {value}")
    return path


def validate_candidate_directory(
    bundle: Path,
    run: dict[str, Any],
    candidates: list[dict[str, str]],
) -> None:
    metadata = run["candidate_directory"]
    candidate_root = bundle / str(metadata["path"])
    manifest_path = candidate_root / "manifest.json"
    if not candidate_root.is_dir() or not manifest_path.is_file():
        raise RuntimeError(f"missing case-first candidate directory: {candidate_root}")
    if sha256_file(manifest_path) != metadata["manifest_sha256"]:
        raise RuntimeError(f"candidate-directory manifest mismatch: {candidate_root}")
    manifest = load_json(manifest_path)
    if int(manifest["case_count"]) != 100 or int(metadata["case_count"]) != 100:
        raise RuntimeError(f"candidate-directory case count mismatch: {candidate_root}")
    if int(manifest["candidate_record_count"]) != len(candidates):
        raise RuntimeError(f"candidate-directory record count mismatch: {candidate_root}")

    declared_files = {"manifest.json"}
    for entry in manifest.get("files", []):
        relative = str(entry["path"])
        path = safe_bundle_member(candidate_root, relative)
        if not path.is_file() or path.is_symlink():
            raise RuntimeError(f"missing case-first candidate artifact: {path}")
        if sha256_file(path) != str(entry["sha256"]):
            raise RuntimeError(f"case-first candidate artifact hash mismatch: {path}")
        if path.stat().st_size != int(entry["size_bytes"]):
            raise RuntimeError(f"case-first candidate artifact size mismatch: {path}")
        declared_files.add(relative)
    observed_files = {
        path.relative_to(candidate_root).as_posix()
        for path in candidate_root.rglob("*")
        if path.is_file()
    }
    if observed_files != declared_files:
        raise RuntimeError(f"candidate-directory file set mismatch: {candidate_root}")

    candidate_cifs = 0
    verifier_paths: set[str] = set()
    by_case: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in candidates:
        case_id = str(row["case_id"])
        by_case[case_id].append(row)
        verifier_path = str(row["verifier_result_path"])
        expected_verifier = f"candidates/{case_id}/verifier-results.json"
        if verifier_path != expected_verifier:
            raise RuntimeError(f"candidate verifier path mismatch: {case_id}")
        verifier_paths.add(verifier_path)
        candidate_path = str(row["candidate_path"])
        if candidate_path:
            expected_name = f"candidate-{int(row['sample_index']) + 1:02d}.cif"
            expected_path = f"candidates/{case_id}/{expected_name}"
            if candidate_path != expected_path:
                raise RuntimeError(f"case-first candidate path mismatch: {candidate_path}")
            path = safe_bundle_member(bundle, candidate_path)
            if not path.is_file() or sha256_file(path) != row["candidate_sha256"]:
                raise RuntimeError(f"case-first candidate hash mismatch: {path}")
            candidate_cifs += 1

    if len(by_case) != 100 or len(verifier_paths) != 100:
        raise RuntimeError(f"case-first verifier coverage mismatch: {candidate_root}")
    if candidate_cifs != int(metadata["candidate_cif_count"]):
        raise RuntimeError(f"case-first CIF count mismatch: {candidate_root}")
    if len(verifier_paths) != int(metadata["verifier_result_file_count"]):
        raise RuntimeError(f"verifier-result file count mismatch: {candidate_root}")
    if bool(metadata["cifs_published"]) != bool(run["raw_run_archive"]["published"]):
        raise RuntimeError(f"candidate publication policy mismatch: {candidate_root}")

    for case_id, rows in by_case.items():
        verifier_path = safe_bundle_member(
            bundle, f"candidates/{case_id}/verifier-results.json"
        )
        verifier = load_json(verifier_path)
        outcomes = verifier.get("candidates", [])
        if verifier.get("case_id") != case_id or len(outcomes) != len(rows):
            raise RuntimeError(f"malformed per-case verifier results: {verifier_path}")
        indexed = {int(row["sample_index"]): row for row in rows}
        for outcome in outcomes:
            sample_index = int(outcome["sample_index"])
            if sample_index not in indexed:
                raise RuntimeError(f"unexpected verifier sample index: {verifier_path}")
            source = indexed[sample_index]
            for field in ("formula_match", "structure_valid", "structure_match"):
                if bool(outcome[field]) != parse_bool(source[field]):
                    raise RuntimeError(f"verifier outcome mismatch: {verifier_path}: {field}")


def validate_bundle(root: Path, record: dict[str, Any]) -> None:
    bundle = root / str(record["bundle_path"])
    checksums = read_checksum_manifest(bundle / "artifacts.sha256")
    for name, expected in checksums.items():
        path = bundle / name
        if not path.is_file() or sha256_file(path) != expected:
            raise RuntimeError(f"bundle checksum mismatch: {path}")
    if sha256_file(bundle / "artifacts.sha256") != record["artifacts_sha256"]:
        raise RuntimeError(f"bundle manifest identity mismatch: {bundle}")

    run = load_json(bundle / "run.json")
    with (bundle / "candidates.csv").open(encoding="utf-8", newline="") as stream:
        candidates = list(csv.DictReader(stream))
    with (bundle / "cases.csv").open(encoding="utf-8", newline="") as stream:
        cases = list(csv.DictReader(stream))
    if len(candidates) != int(run["results"]["candidate_record_count"]):
        raise RuntimeError(f"candidate count mismatch: {bundle}")
    if len(cases) != 100:
        raise RuntimeError(f"case count mismatch: {bundle}")
    if sum(parse_bool(row["best_of_1_structure_match"]) for row in cases) != int(
        run["results"]["exact_structure_matches_at_1"]
    ):
        raise RuntimeError(f"exact@1 mismatch: {bundle}")
    if sum(parse_bool(row["best_of_reported_k_structure_match"]) for row in cases) != int(
        run["results"]["exact_structure_matches_at_reported_k"]
    ):
        raise RuntimeError(f"exact@reported-k mismatch: {bundle}")
    validate_candidate_directory(bundle, run, candidates)
    expected_checksums = {
        "README.md",
        "candidates/manifest.json",
        "cases.csv",
        "candidates.csv",
        "run.json",
    }
    if run["raw_run_archive"]["published"]:
        expected_checksums.add(ARCHIVE_NAME)
        if set(checksums) != expected_checksums:
            raise RuntimeError(f"published bundle file set mismatch: {bundle}")
        if any(not parse_bool(row["artifacts_published"]) for row in candidates):
            raise RuntimeError(f"published candidate index is inconsistent: {bundle}")
        validate_archive(bundle, run, candidates)
    else:
        if set(checksums) != expected_checksums:
            raise RuntimeError(f"withheld bundle file set mismatch: {bundle}")
        if (bundle / ARCHIVE_NAME).exists() or ARCHIVE_NAME in checksums:
            raise RuntimeError(f"withheld archive is present: {bundle}")
        if any(parse_bool(row["artifacts_published"]) for row in candidates):
            raise RuntimeError(f"withheld candidate index is inconsistent: {bundle}")

    for path in bundle.iterdir():
        if path.suffix.lower() not in {".csv", ".json", ".md", ".sha256"}:
            continue
        text = path.read_text(encoding="utf-8").lower()
        for forbidden in FORBIDDEN_PUBLIC_TEXT:
            if forbidden.lower() in text:
                raise RuntimeError(f"non-public text in bundle: {path}")


def validate_all(output_root: Path) -> None:
    manifest = load_json(output_root / "manifest.json")
    records = manifest.get("bundles", [])
    if len(records) != len(RUN_SPECS) or int(manifest.get("bundle_count", 0)) != len(RUN_SPECS):
        raise RuntimeError("baseline result manifest does not contain the expected 14 bundles")
    observed_paths = {str(record["bundle_path"]) for record in records}
    expected_paths = {spec.bundle_relative_path.as_posix() for spec in RUN_SPECS}
    if observed_paths != expected_paths:
        raise RuntimeError("baseline result manifest paths do not match the declared run set")
    for record in records:
        validate_bundle(output_root, record)
    print(
        json.dumps(
            {
                "status": "OK",
                "bundle_count": len(records),
                "candidate_record_count": sum(int(row["candidate_record_count"]) for row in records),
                "published_archive_count": sum(
                    bool(row["candidate_archive_published"]) for row in records
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build", "validate"))
    parser.add_argument(
        "--source-root",
        type=Path,
        help="root containing the frozen framework-native runs (required for build)",
    )
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    args = parser.parse_args()
    output_root = args.output_root.expanduser().resolve()
    if args.command == "build":
        if args.source_root is None:
            parser.error("build requires --source-root")
        source_root = args.source_root.expanduser().resolve()
        build_all(source_root, output_root)
    validate_all(output_root)


if __name__ == "__main__":
    main()
