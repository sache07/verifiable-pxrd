"""Materialize framework outputs as case-first candidate directories."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
from collections import defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

CASE_ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")
SHARD_PATTERN = re.compile(r"shard-\d+")
BOOLEAN_FIELDS = {
    "formula_match",
    "full_cell_composition_match",
    "structure_valid",
    "structure_match",
}
FLOAT_FIELDS = {
    "matcher_rms",
    "matcher_max_dist",
    "minimum_periodic_distance_angstrom",
}
VERIFIER_FIELDS = (
    "status",
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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json_atomic(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.partial")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(payload, stream, indent=2, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def safe_case_id(value: Any) -> str:
    case_id = str(value)
    if CASE_ID_PATTERN.fullmatch(case_id) is None:
        raise RuntimeError(f"unsafe candidate case ID: {case_id!r}")
    return case_id


def safe_source_path(shard: Path, value: Any) -> Path:
    relative = Path(str(value))
    if relative.is_absolute() or ".." in relative.parts:
        raise RuntimeError(f"unsafe candidate artifact path: {value!r}")
    source = (shard / relative).resolve()
    shard_root = shard.resolve()
    if source == shard_root or not source.is_relative_to(shard_root):
        raise RuntimeError(f"candidate artifact escapes its shard: {value!r}")
    if not source.is_file() or source.is_symlink():
        raise RuntimeError(f"missing or unsafe candidate artifact: {source}")
    return source


def canonical_candidate_name(sample_index: int) -> str:
    return f"candidate-{sample_index + 1:02d}.cif"


def candidate_records(run_root: Path) -> list[dict[str, Any]]:
    """Read and validate every candidate record in a native sharded run."""

    records: list[dict[str, Any]] = []
    seen: set[tuple[str, int]] = set()
    shards = sorted(
        path
        for path in run_root.iterdir()
        if path.is_dir() and SHARD_PATTERN.fullmatch(path.name)
    )
    if not shards:
        raise RuntimeError(f"no completed shard directories in {run_root}")
    for shard in shards:
        results_path = shard / "results.json"
        if not results_path.is_file():
            raise RuntimeError(f"shard has no results.json: {shard}")
        payload = json.loads(results_path.read_text(encoding="utf-8"))
        for source_record in payload.get("candidates", []):
            case_id = safe_case_id(source_record.get("case_id"))
            sample_index = int(source_record.get("sample_index"))
            if sample_index < 0:
                raise RuntimeError(f"negative candidate sample index: {case_id}: {sample_index}")
            key = (case_id, sample_index)
            if key in seen:
                raise RuntimeError(f"duplicate candidate record: {key}")
            seen.add(key)
            source = safe_source_path(shard, source_record.get("candidate_path"))
            expected_sha256 = str(source_record.get("candidate_sha256") or "")
            if not re.fullmatch(r"[0-9a-f]{64}", expected_sha256):
                raise RuntimeError(f"invalid candidate SHA-256: {key}")
            if sha256_file(source) != expected_sha256:
                raise RuntimeError(f"candidate SHA-256 mismatch: {source}")
            canonical_name = canonical_candidate_name(sample_index)
            publishable_cif = (
                str(source_record.get("status")) == "generated"
                and source.name == canonical_name
            )
            records.append(
                {
                    "case_id": case_id,
                    "sample_index": sample_index,
                    "status": str(source_record.get("status")),
                    "source": source,
                    "source_member": f"{shard.name}/{source.relative_to(shard).as_posix()}",
                    "sha256": expected_sha256,
                    "canonical_name": canonical_name,
                    "publishable_cif": publishable_cif,
                }
            )
    return sorted(records, key=lambda row: (row["case_id"], row["sample_index"]))


def optional_json_value(field: str, value: Any) -> Any:
    if value is None or value == "":
        return None
    if field in BOOLEAN_FIELDS:
        if isinstance(value, bool):
            return value
        return str(value).strip().lower() in {"1", "true", "yes"}
    if field in FLOAT_FIELDS:
        return float(value)
    return value


def index_verifier_rows(
    rows: Sequence[Mapping[str, Any]] | None,
) -> dict[tuple[str, int], Mapping[str, Any]] | None:
    if rows is None:
        return None
    indexed: dict[tuple[str, int], Mapping[str, Any]] = {}
    for row in rows:
        key = (safe_case_id(row.get("case_id")), int(row.get("sample_index")))
        if key in indexed:
            raise RuntimeError(f"duplicate verifier result: {key}")
        indexed[key] = row
    return indexed


def detect_verifier_inputs(
    run_root: Path,
) -> tuple[list[dict[str, str]] | None, dict[str, Any] | None]:
    evaluation_csv = run_root / "evaluation-candidates.csv"
    if not evaluation_csv.is_file():
        return None, None
    with evaluation_csv.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    metadata: dict[str, Any] | None = None
    for name in ("evaluation.json", "run-summary.json"):
        path = run_root / name
        if not path.is_file():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        metric = payload.get("metric")
        if isinstance(metric, dict):
            metadata = metric
            break
    return rows, metadata


def copy_candidate(source: Path, destination: Path, expected_sha256: str) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if destination.is_symlink() or not destination.is_file():
            raise RuntimeError(f"unsafe existing candidate destination: {destination}")
        if sha256_file(destination) != expected_sha256:
            raise RuntimeError(f"candidate destination has conflicting contents: {destination}")
        return
    temporary = destination.with_name(f".{destination.name}.partial")
    shutil.copyfile(source, temporary)
    if sha256_file(temporary) != expected_sha256:
        raise RuntimeError(f"candidate copy failed verification: {destination}")
    os.replace(temporary, destination)


def materialize_case_candidates(
    run_root: Path,
    output_root: Path | None = None,
    *,
    verifier_rows: Sequence[Mapping[str, Any]] | None = None,
    verifier_metadata: Mapping[str, Any] | None = None,
    publish_cifs: bool = True,
) -> dict[str, Any]:
    """Create ``candidates/<case-id>/`` from a native sharded run.

    Generation can call this without verifier rows. Evaluation calls it again with
    verifier rows, adding one ``verifier-results.json`` file per benchmark case.
    Existing byte-identical CIFs are retained, making repeated collection safe.
    """

    source_root = run_root.expanduser().resolve()
    if not source_root.is_dir():
        raise RuntimeError(f"candidate input run does not exist: {source_root}")
    destination_root = (
        output_root.expanduser().resolve()
        if output_root is not None
        else source_root / "candidates"
    )
    if destination_root == source_root:
        raise RuntimeError("candidate output must not replace the input run directory")
    destination_root.mkdir(parents=True, exist_ok=True)

    if verifier_rows is None:
        detected_rows, detected_metadata = detect_verifier_inputs(source_root)
        verifier_rows = detected_rows
        if verifier_metadata is None:
            verifier_metadata = detected_metadata

    records = candidate_records(source_root)
    verifier_index = index_verifier_rows(verifier_rows)
    record_keys = {(row["case_id"], row["sample_index"]) for row in records}
    if verifier_index is not None and set(verifier_index) != record_keys:
        missing = sorted(record_keys - set(verifier_index))[:5]
        extra = sorted(set(verifier_index) - record_keys)[:5]
        raise RuntimeError(f"verifier/candidate key mismatch: missing={missing}, extra={extra}")

    by_case: dict[str, list[dict[str, Any]]] = defaultdict(list)
    candidate_entries: list[dict[str, Any]] = []
    expected_files: set[str] = {"manifest.json"}
    for record in records:
        case_id = str(record["case_id"])
        candidate_relative: str | None = None
        if publish_cifs and bool(record["publishable_cif"]):
            relative = Path(case_id) / str(record["canonical_name"])
            copy_candidate(
                Path(record["source"]),
                destination_root / relative,
                str(record["sha256"]),
            )
            candidate_relative = relative.as_posix()
            expected_files.add(candidate_relative)
        entry = {
            "case_id": case_id,
            "sample_index": int(record["sample_index"]),
            "status": str(record["status"]),
            "candidate_path": candidate_relative,
            "candidate_sha256": str(record["sha256"]),
            "source_member": str(record["source_member"]),
        }
        candidate_entries.append(entry)
        by_case[case_id].append(entry)

    verifier_file_count = 0
    if verifier_index is not None:
        for case_id, case_entries in sorted(by_case.items()):
            outcomes = []
            for entry in sorted(case_entries, key=lambda row: int(row["sample_index"])):
                key = (case_id, int(entry["sample_index"]))
                verifier_row = verifier_index[key]
                outcome = {
                    "sample_index": entry["sample_index"],
                    "candidate_file": (
                        Path(str(entry["candidate_path"])).name
                        if entry["candidate_path"]
                        else None
                    ),
                    "candidate_sha256": entry["candidate_sha256"],
                }
                for field in VERIFIER_FIELDS:
                    outcome[field] = optional_json_value(field, verifier_row.get(field))
                outcomes.append(outcome)
            verifier_relative = Path(case_id) / "verifier-results.json"
            write_json_atomic(
                destination_root / verifier_relative,
                {
                    "schema_version": "1.0.0",
                    "case_id": case_id,
                    "verifier": dict(verifier_metadata or {}),
                    "candidates": outcomes,
                },
            )
            expected_files.add(verifier_relative.as_posix())
            verifier_file_count += 1

    file_entries = []
    for relative in sorted(expected_files - {"manifest.json"}):
        path = destination_root / relative
        file_entries.append(
            {
                "path": relative,
                "sha256": sha256_file(path),
                "size_bytes": path.stat().st_size,
            }
        )
    manifest = {
        "schema_version": "1.0.0",
        "source_run_id": source_root.name,
        "case_count": len(by_case),
        "candidate_record_count": len(records),
        "candidate_cif_count": sum(bool(row["candidate_path"]) for row in candidate_entries),
        "verifier_result_file_count": verifier_file_count,
        "cifs_published": publish_cifs,
        "candidates": candidate_entries,
        "files": file_entries,
    }
    write_json_atomic(destination_root / "manifest.json", manifest)

    observed_files = {
        path.relative_to(destination_root).as_posix()
        for path in destination_root.rglob("*")
        if path.is_file()
    }
    if observed_files != expected_files:
        raise RuntimeError(
            "unexpected files in case-first candidate directory: "
            f"{sorted(observed_files - expected_files)[:5]}"
        )
    return {
        "path": str(destination_root),
        "case_count": len(by_case),
        "candidate_record_count": len(records),
        "candidate_cif_count": manifest["candidate_cif_count"],
        "verifier_result_file_count": verifier_file_count,
        "manifest_sha256": sha256_file(destination_root / "manifest.json"),
        "candidates": candidate_entries,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Materialize a sharded baseline run as candidates/<case-id>/.",
    )
    parser.add_argument("--input", type=Path, required=True, help="Native run directory")
    parser.add_argument(
        "--output",
        type=Path,
        help="Destination candidates directory (default: <input>/candidates)",
    )
    args = parser.parse_args(argv)
    summary = materialize_case_candidates(args.input, args.output)
    print(json.dumps({key: value for key, value in summary.items() if key != "candidates"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
