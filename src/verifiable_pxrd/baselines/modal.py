"""Shared durable I/O for the pXRD-100 Modal inference runners."""

from __future__ import annotations

import hashlib
import io
import json
import os
import re
import tarfile
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_run_id(value: str) -> str:
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", value) is None:
        raise ValueError("run_id must be a filesystem-safe identifier")
    return value


def write_atomic(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".partial")
    with temporary.open("w", encoding="utf-8") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def archive_directory(destination: Path) -> bytes:
    payload = io.BytesIO()
    with tarfile.open(fileobj=payload, mode="w:gz") as archive:
        archive.add(destination, arcname="/".join(destination.parts[-2:]))
    return payload.getvalue()


def materialize_archive(payload: bytes, output_root: Path) -> Path:
    """Safely extract exactly one ``run-id/shard-id`` result archive."""

    output_root.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as archive:
        members = archive.getmembers()
        roots = {tuple(Path(member.name).parts[:2]) for member in members if member.name}
        if len(roots) != 1:
            raise RuntimeError("result archive has an invalid root")
        run_name, shard_name = next(iter(roots))
        if not run_name or not shard_name:
            raise RuntimeError("result archive has an empty root")
        output_resolved = output_root.resolve()
        for member in members:
            if member.issym() or member.islnk():
                raise RuntimeError("result archive contains a link")
            target = (output_root / member.name).resolve()
            if target != output_resolved and output_resolved not in target.parents:
                raise RuntimeError("result archive contains an unsafe path")
        archive.extractall(output_root, members=members)
    return output_root / run_name / shard_name


def collect_handle(handle_path: Path, output_root: Path, *, timeout: float = 0) -> dict[str, Any]:
    """Collect every finished Modal function call and durably update its handle."""

    import modal

    handle = json.loads(handle_path.read_text(encoding="utf-8"))
    completed = {int(value) for value in handle.get("completed_shards", [])}
    failures: list[dict[str, Any]] = []
    for call in handle["calls"]:
        shard_index = int(call["shard_index"])
        if shard_index in completed:
            continue
        try:
            payload = modal.FunctionCall.from_id(str(call["call_id"])).get(timeout=timeout)
            materialize_archive(payload, output_root)
            completed.add(shard_index)
        except TimeoutError:
            continue
        except Exception as exc:
            failures.append({"shard_index": shard_index, "error": repr(exc)})
    handle["completed_shards"] = sorted(completed)
    handle["failures"] = failures
    write_atomic(handle_path, json.dumps(handle, indent=2, sort_keys=True) + "\n")
    return handle


def summarize_shards(run_root: Path) -> dict[str, Any]:
    results = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(run_root.glob("shard-*/results.json"))
    ]
    return {
        "run_id": run_root.name,
        "shard_count": len(results),
        "case_count": sum(int(result["case_count"]) for result in results),
        "candidate_count": sum(int(result["candidate_count"]) for result in results),
        "generated_candidate_count": sum(
            int(result["generated_candidate_count"]) for result in results
        ),
        "invalid_candidate_count": sum(
            int(result["invalid_candidate_count"]) for result in results
        ),
        "aggregate_container_seconds": sum(
            float(result["runtime"]["total_seconds"]) for result in results
        ),
    }
