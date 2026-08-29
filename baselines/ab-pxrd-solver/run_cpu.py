#!/usr/bin/env python3
"""Resumable, one-case-per-shard CPU harness for Ab-PXRD-Solver.

This runner intentionally uses only the Python standard library.  It is copied
into the hash-bound EC2 bundle and can therefore start before the benchmark
package itself is installed.  Each upstream process gets its own process group;
the wall-time limit terminates that entire group so timed-out MACE/GSAS children
cannot survive as orphans.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import re
import shutil
import signal
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SOURCE_COMMIT = "0d67964dfcbd2e2fa09e79bbbac2f5d020a121e9"
GSASII_COMMIT = "1a0aeec6c61b54f68e6812704730a471187ac393"
MACE_MODEL_SHA256 = "2ddb079cee0e131eaaf6912ba581b394551ead283e95c99cfe78c605d10b5736"
DEFAULT_SEED_BASE = 20260721
DEFAULT_TIMEOUT_SECONDS = 14_400
_WRITE_LOCK = threading.Lock()
_FORMULA_TOKEN = re.compile(r"[A-Z][a-z]?|\(|\)|(?:\d+(?:\.\d*)?|\.\d+)")
_NUMBER_TOKEN = re.compile(r"\d+(?:\.\d*)?|\.\d+")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json_atomic(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def read_summary(path: Path) -> dict[str, str] | None:
    if not path.is_file() or path.stat().st_size == 0:
        return None
    with path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    return rows[-1] if rows else None


def expanded_integer_formula(formula: str) -> str:
    """Serialize a reduced formula for the upstream regex-only parser.

    Ab-PXRD-Solver's released ``parse_formula`` recognizes element/count pairs
    but not parentheses.  Pymatgen's reduced-formula presentation can contain
    grouped subexpressions, so expand those groups without changing the supplied
    composition before passing the value to ``--formula``.
    """

    compact = formula.replace(" ", "")
    tokens = _FORMULA_TOKEN.findall(compact)
    if "".join(tokens) != compact:
        raise ValueError(f"unsupported formula syntax: {formula}")
    stack: list[dict[str, float]] = [{}]
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token == "(":
            stack.append({})
            index += 1
            continue
        if token == ")":
            if len(stack) == 1:
                raise ValueError(f"unbalanced formula: {formula}")
            group = stack.pop()
            multiplier = 1.0
            if index + 1 < len(tokens) and _NUMBER_TOKEN.fullmatch(tokens[index + 1]):
                multiplier = float(tokens[index + 1])
                index += 1
            for element, amount in group.items():
                stack[-1][element] = stack[-1].get(element, 0.0) + amount * multiplier
            index += 1
            continue
        if _NUMBER_TOKEN.fullmatch(token):
            raise ValueError(f"orphan number in formula: {formula}")
        amount = 1.0
        if index + 1 < len(tokens) and _NUMBER_TOKEN.fullmatch(tokens[index + 1]):
            amount = float(tokens[index + 1])
            index += 1
        stack[-1][token] = stack[-1].get(token, 0.0) + amount
        index += 1
    if len(stack) != 1:
        raise ValueError(f"unbalanced formula: {formula}")

    serialized: list[str] = []
    for element, amount in stack[0].items():
        integer = round(amount)
        if abs(amount - integer) > 1.0e-9 or integer < 1:
            raise ValueError(
                f"Ab-PXRD-Solver requires positive integer element counts: {formula}"
            )
        serialized.append(element)
        if integer != 1:
            serialized.append(str(integer))
    if not serialized:
        raise ValueError("empty formula")
    return "".join(serialized)


def copy_upstream_evidence(case_output: Path, evidence: Path) -> list[Path]:
    retained: list[Path] = []
    for source in sorted((case_output / "cifs").glob("*.cif")):
        destination = evidence / "cifs" / source.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        retained.append(destination)
    for source in sorted((case_output / "logs").glob("*")):
        if source.is_file():
            destination = evidence / "logs" / source.name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
    summary = case_output / "summary.csv"
    if summary.is_file():
        evidence.mkdir(parents=True, exist_ok=True)
        shutil.copy2(summary, evidence / "summary.csv")
    return retained


def select_candidate(cifs: list[Path], summary: dict[str, str] | None) -> Path | None:
    if not cifs:
        return None
    if summary:
        spg = str(summary.get("SPG") or "").strip()
        matching = [path for path in cifs if spg and path.stem.endswith(f"_{spg}")]
        if matching:
            return matching[-1]
    return cifs[-1]


def terminate_process_group(process: subprocess.Popen[bytes]) -> None:
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        process.wait(timeout=15)
        return
    except subprocess.TimeoutExpired:
        pass
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        return
    process.wait(timeout=15)


def upload_path(local_path: Path, s3_uri: str, *, recursive: bool = False) -> None:
    command = ["aws", "s3", "cp", str(local_path), s3_uri, "--only-show-errors"]
    if recursive:
        command.append("--recursive")
    subprocess.run(command, check=True)


def run_case(
    *,
    case: dict[str, Any],
    case_index: int,
    manifest: dict[str, Any],
    args: argparse.Namespace,
    run_root: Path,
) -> dict[str, Any]:
    case_id = str(case["case_id"])
    source_dataset_id = args.dataset_id
    case_prefix = str(
        manifest.get("case_prefix")
        or str(manifest["cases"][0]["case_id"]).split("-", 1)[0]
    )
    support_policy = str(manifest.get("support_policy") or "require-all")
    shard_name = f"shard-{case_index:03d}"
    destination = run_root / shard_name
    if destination.is_dir() and (destination / "results.json").is_file():
        existing = json.loads((destination / "results.json").read_text(encoding="utf-8"))
        if existing.get("case_ids") != [case_id]:
            raise RuntimeError(f"resume identity mismatch in {destination}")
        return {"case_id": case_id, "shard": shard_name, "status": "resumed"}

    partial = run_root / f".{shard_name}.partial-{os.getpid()}-{threading.get_ident()}"
    if partial.exists():
        shutil.rmtree(partial)
    partial.mkdir(parents=True)
    work_output = partial / "work" / case_id / "Results"
    work_output.mkdir(parents=True)
    stdout_path = partial / "logs" / f"{case_id}.stdout.txt"
    stderr_path = partial / "logs" / f"{case_id}.stderr.txt"
    stdout_path.parent.mkdir(parents=True)

    pattern = args.targets / str(case["pattern_path"])
    if sha256_file(pattern) != str(case["pattern_sha256"]):
        raise RuntimeError(f"target pattern digest mismatch for {case_id}")
    case_seed = args.seed_base + case_index
    input_formula = str(case["formula"])
    solver_formula = expanded_integer_formula(input_formula)
    command = [
        str(args.python),
        str(args.source / "PXRD_solve.py"),
        "--input", str(pattern),
        "--formula", solver_formula,
        "--infer-spg",
        "--output", str(work_output),
        "--workers", "1",
        "--max-vol", "1500",
        "--max-wp", "18",
        "--max-dof", "25",
        "--max-z", "24",
        "--qrs", "halton",
    ]
    environment = dict(os.environ)
    environment.update(
        {
            "PYTHONUNBUFFERED": "1",
            "PYTHONPATH": str(args.source),
            "GSASII_PATH": str(args.gsasii),
            "XDG_CACHE_HOME": str(args.cache),
            "PXRD_SEED_BASE": str(case_seed),
            "PXRD_SILENCE_MACE": "1",
            "OMP_NUM_THREADS": "1",
            "OPENBLAS_NUM_THREADS": "1",
            "MKL_NUM_THREADS": "1",
            "NUMEXPR_NUM_THREADS": "1",
            "TORCH_NUM_THREADS": "1",
        }
    )
    started_utc = datetime.now(UTC).isoformat()
    started = time.perf_counter()
    timed_out = False
    with stdout_path.open("wb", buffering=0) as stdout, stderr_path.open("wb", buffering=0) as stderr:
        process = subprocess.Popen(
            command,
            cwd=args.source,
            env=environment,
            stdout=stdout,
            stderr=stderr,
            start_new_session=True,
        )
        try:
            returncode = process.wait(timeout=args.timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            terminate_process_group(process)
            returncode = 124
            stderr.write(f"\nTimed out after {args.timeout} seconds; process group terminated.\n".encode())
    runtime_seconds = time.perf_counter() - started

    evidence = partial / "upstream" / case_id
    retained_cifs = copy_upstream_evidence(work_output, evidence)
    summary = read_summary(work_output / "summary.csv")
    selected = select_candidate(retained_cifs, summary)
    record: dict[str, Any] = {
        "case_id": case_id,
        "sample_index": 0,
        "seed": case_seed,
        "input_formula": input_formula,
        "solver_formula": solver_formula,
        "composition_serialization": "expanded_integer_formula_no_parentheses",
        "input_mode": "reduced_formula_and_pxrd_infer_spacegroup",
        "command": command,
        "returncode": returncode,
        "timed_out": timed_out,
        "runtime_seconds": runtime_seconds,
        "started_at_utc": started_utc,
        "completed_at_utc": datetime.now(UTC).isoformat(),
        "solver_summary": summary,
        "raw_candidate_count": len(retained_cifs),
        "stdout_path": str(stdout_path.relative_to(partial)),
        "stdout_sha256": sha256_file(stdout_path),
        "stderr_path": str(stderr_path.relative_to(partial)),
        "stderr_sha256": sha256_file(stderr_path),
    }
    if selected is not None:
        normalized = partial / "candidates" / case_id / "candidate-01.cif"
        normalized.parent.mkdir(parents=True)
        shutil.copy2(selected, normalized)
        record.update(
            {
                "status": "generated",
                "candidate_path": str(normalized.relative_to(partial)),
                "candidate_sha256": sha256_file(normalized),
                "selected_upstream_path": str(selected.relative_to(partial)),
                "selected_upstream_sha256": sha256_file(selected),
            }
        )
    else:
        invalid = partial / "candidates" / case_id / "candidate-01.invalid.json"
        invalid.parent.mkdir(parents=True)
        error = {
            "returncode": returncode,
            "timed_out": timed_out,
            "solver_status": summary.get("Status") if summary else None,
            "message": "Ab-PXRD-Solver produced no selected CIF",
        }
        write_json_atomic(invalid, error)
        record.update(
            {
                "status": "invalid",
                "candidate_path": str(invalid.relative_to(partial)),
                "candidate_sha256": sha256_file(invalid),
                "error": error["message"],
            }
        )

    request = {
        "run_id": args.run_id,
        "shard_index": case_index,
        "case_ids": [case_id],
        "seed_base": args.seed_base,
        "samples": 1,
        "case_timeout_seconds": args.timeout,
        "dataset_id": args.dataset_id,
        "source_dataset_id": source_dataset_id,
        "case_prefix": case_prefix,
        "support_policy": support_policy,
        "source_manifest_sha256": manifest.get("source_manifest_sha256"),
    }
    result = {
        "schema_version": "1.0.0",
        "framework": "Ab-PXRD-Solver",
        "source_commit": SOURCE_COMMIT,
        "mace_model_sha256": MACE_MODEL_SHA256,
        "gsasii_commit": GSASII_COMMIT,
        "dataset_id": args.dataset_id,
        "source_dataset_id": source_dataset_id,
        "case_prefix": case_prefix,
        "support_policy": support_policy,
        "source_manifest_sha256": manifest.get("source_manifest_sha256"),
        "target_manifest_sha256": sha256_file(args.targets / "manifest.json"),
        "run_id": args.run_id,
        "shard_index": case_index,
        "case_ids": [case_id],
        "case_count": 1,
        "samples_per_case": 1,
        "candidate_count": 1,
        "generated_candidate_count": int(record["status"] == "generated"),
        "invalid_candidate_count": int(record["status"] == "invalid"),
        "inference": {
            "input_mode": "reduced_formula_and_pxrd_infer_spacegroup",
            "composition_serialization": "expanded_integer_formula_no_parentheses",
            "space_group_supplied": False,
            "qrs": "halton",
            "seed_base": args.seed_base,
            "case_timeout_seconds": args.timeout,
            "compute": "AWS EC2 CPU",
        },
        "runtime": {"python": platform.python_version(), "total_seconds": runtime_seconds},
        "candidates": [record],
    }
    shutil.rmtree(partial / "work", ignore_errors=True)
    write_json_atomic(partial / "request.json", request)
    write_json_atomic(partial / "results.json", result)
    with _WRITE_LOCK:
        if destination.exists():
            raise RuntimeError(f"refusing to overwrite completed shard {destination}")
        partial.replace(destination)
    if args.s3_uri:
        upload_path(destination, f"{args.s3_uri.rstrip('/')}/{shard_name}/", recursive=True)
    return {
        "case_id": case_id,
        "shard": shard_name,
        "status": record["status"],
        "timed_out": timed_out,
        "returncode": returncode,
        "runtime_seconds": runtime_seconds,
    }


def progress_payload(run_root: Path, total: int, started_at: str) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for result_path in sorted(run_root.glob("shard-*/results.json")):
        payload = json.loads(result_path.read_text(encoding="utf-8"))
        rows.extend(payload.get("candidates", []))
    return {
        "schema_version": "1.0.0",
        "run_id": run_root.name,
        "started_at_utc": started_at,
        "updated_at_utc": datetime.now(UTC).isoformat(),
        "expected_case_count": total,
        "completed_case_count": len(rows),
        "generated_count": sum(row.get("status") == "generated" for row in rows),
        "timed_out_count": sum(bool(row.get("timed_out")) for row in rows),
        "runtime_error_count": sum(
            not row.get("timed_out") and int(row.get("returncode", 0)) != 0 for row in rows
        ),
        "running_case_count": max(0, min(total - len(rows), 0)),
        "remaining_case_count": total - len(rows),
        "cases": [
            {
                "case_id": row.get("case_id"),
                "status": row.get("status"),
                "timed_out": row.get("timed_out"),
                "runtime_seconds": row.get("runtime_seconds"),
            }
            for row in rows
        ],
    }


def materialize_case_candidates(run_root: Path) -> dict[str, Any]:
    """Create the case-first CIF view without requiring the benchmark package."""

    output = run_root / "candidates"
    existing_manifest = output / "manifest.json"
    if (run_root / "evaluation-candidates.csv").is_file() and existing_manifest.is_file():
        existing = json.loads(existing_manifest.read_text(encoding="utf-8"))
        if int(existing.get("verifier_result_file_count", 0)) > 0:
            return {
                "path": str(output),
                "case_count": int(existing["case_count"]),
                "candidate_record_count": int(existing["candidate_record_count"]),
                "candidate_cif_count": int(existing["candidate_cif_count"]),
                "verifier_result_file_count": int(existing["verifier_result_file_count"]),
                "manifest_sha256": sha256_file(existing_manifest),
            }
    output.mkdir(parents=True, exist_ok=True)
    entries: list[dict[str, Any]] = []
    files: list[dict[str, Any]] = []
    cases: set[str] = set()
    for result_path in sorted(run_root.glob("shard-*/results.json")):
        shard = result_path.parent
        payload = json.loads(result_path.read_text(encoding="utf-8"))
        for record in payload.get("candidates", []):
            case_id = str(record["case_id"])
            if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", case_id) is None:
                raise RuntimeError(f"unsafe candidate case ID: {case_id!r}")
            cases.add(case_id)
            sample_index = int(record["sample_index"])
            relative_source = Path(str(record["candidate_path"]))
            if relative_source.is_absolute() or ".." in relative_source.parts:
                raise RuntimeError(f"unsafe candidate path: {relative_source}")
            source = (shard / relative_source).resolve()
            if not source.is_file() or not source.is_relative_to(shard.resolve()):
                raise RuntimeError(f"missing or unsafe candidate artifact: {source}")
            digest = str(record["candidate_sha256"])
            if sha256_file(source) != digest:
                raise RuntimeError(f"candidate SHA-256 mismatch: {source}")
            expected_name = f"candidate-{sample_index + 1:02d}.cif"
            candidate_path: str | None = None
            if record.get("status") == "generated" and source.name == expected_name:
                relative_output = Path(case_id) / expected_name
                destination = output / relative_output
                destination.parent.mkdir(parents=True, exist_ok=True)
                if destination.exists() and sha256_file(destination) != digest:
                    raise RuntimeError(f"conflicting case-first candidate: {destination}")
                if not destination.exists():
                    temporary = destination.with_name(f".{destination.name}.partial")
                    shutil.copyfile(source, temporary)
                    if sha256_file(temporary) != digest:
                        raise RuntimeError(f"candidate copy failed verification: {destination}")
                    temporary.replace(destination)
                candidate_path = relative_output.as_posix()
                files.append(
                    {
                        "path": candidate_path,
                        "sha256": digest,
                        "size_bytes": destination.stat().st_size,
                    }
                )
            entries.append(
                {
                    "case_id": case_id,
                    "sample_index": sample_index,
                    "status": str(record["status"]),
                    "candidate_path": candidate_path,
                    "candidate_sha256": digest,
                    "source_member": (
                        f"{shard.name}/{source.relative_to(shard).as_posix()}"
                    ),
                }
            )
    entries.sort(key=lambda row: (str(row["case_id"]), int(row["sample_index"])))
    files.sort(key=lambda row: str(row["path"]))
    manifest = {
        "schema_version": "1.0.0",
        "source_run_id": run_root.name,
        "case_count": len(cases),
        "candidate_record_count": len(entries),
        "candidate_cif_count": len(files),
        "verifier_result_file_count": 0,
        "cifs_published": True,
        "candidates": entries,
        "files": files,
    }
    write_json_atomic(output / "manifest.json", manifest)
    return {
        "path": str(output),
        "case_count": len(cases),
        "candidate_record_count": len(entries),
        "candidate_cif_count": len(files),
        "verifier_result_file_count": 0,
        "manifest_sha256": sha256_file(output / "manifest.json"),
    }


def validate_runtime(args: argparse.Namespace) -> dict[str, Any]:
    required = [
        args.source / "PXRD_solve.py",
        args.source / "pxrd_app" / "core.py",
        args.source / "pxrd_app" / "tools" / "models" / "peaks" / "best_model.pth",
        args.source / "pxrd_app" / "tools" / "models" / "density" / "checkpoint-r0.pth.tar",
        args.gsasii / "GSASIIscriptable.py",
        args.targets / "manifest.json",
        args.cache / "mace" / "20231210mace128L0_energy_epoch249model",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError("missing runtime artifacts: " + ", ".join(missing))
    model = required[-1]
    if sha256_file(model) != MACE_MODEL_SHA256:
        raise RuntimeError("MACE model digest mismatch")
    # This is the compatibility correction needed when no seed cell is found.
    core_text = (args.source / "pxrd_app" / "core.py").read_text(encoding="utf-8")
    if "total_count = 0" not in core_text:
        raise RuntimeError("missing audited total_count initialization compatibility fix")
    command = [
        str(args.python),
        "-c",
        (
            "import torch,numpy; from mace.calculators import mace_mp; "
            "from ase import Atoms; c=mace_mp(model='small',device='cpu',default_dtype='float32'); "
            "a=Atoms('Si2',positions=[[0,0,0],[1.3575,1.3575,1.3575]],"
            "cell=[5.43,5.43,5.43],pbc=True); a.calc=c; e=float(a.get_potential_energy()); "
            "assert numpy.isfinite(e); print(torch.__version__, e)"
        ),
    ]
    environment = dict(os.environ)
    environment.update(
        {
            "XDG_CACHE_HOME": str(args.cache),
            "OMP_NUM_THREADS": "1",
            "OPENBLAS_NUM_THREADS": "1",
            "MKL_NUM_THREADS": "1",
            "PXRD_SILENCE_MACE": "1",
        }
    )
    smoke = subprocess.run(command, env=environment, check=True, capture_output=True, text=True, timeout=300)
    return {"status": "OK", "mace_smoke": smoke.stdout.strip(), "artifact_count": len(required)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--targets", type=Path, required=True)
    parser.add_argument("--gsasii", type=Path, required=True)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--python", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--dataset-id", required=True)
    parser.add_argument("--workers", type=int, default=24)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--seed-base", type=int, default=DEFAULT_SEED_BASE)
    parser.add_argument("--s3-uri")
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument("--limit", type=int)
    parser.add_argument("--doctor-only", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.workers <= 64:
        parser.error("--workers must be between 1 and 64")
    if not 60 <= args.timeout <= DEFAULT_TIMEOUT_SECONDS:
        parser.error(f"--timeout must be between 60 and {DEFAULT_TIMEOUT_SECONDS}")
    if not args.run_id or any(ch not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for ch in args.run_id):
        parser.error("--run-id contains unsafe characters")
    return args


def main() -> int:
    args = parse_args()
    args.source = args.source.resolve()
    args.targets = args.targets.resolve()
    args.gsasii = args.gsasii.resolve()
    args.cache = args.cache.resolve()
    # Do not resolve the venv's Python symlink: resolving it to the base uv
    # interpreter bypasses pyvenv.cfg and therefore the pinned environment.
    args.python = args.python.absolute()
    args.output_root = args.output_root.resolve()
    doctor = validate_runtime(args)
    print(json.dumps({"doctor": doctor}, sort_keys=True), flush=True)
    if args.doctor_only:
        return 0

    manifest = json.loads((args.targets / "manifest.json").read_text(encoding="utf-8"))
    cases = list(manifest["cases"])
    if len(cases) != 100 or int(manifest.get("supported_case_count", -1)) != 100:
        raise RuntimeError("benchmark target manifest is not complete (expected 100 supported cases)")
    if len({str(case["case_id"]) for case in cases}) != len(cases):
        raise RuntimeError("duplicate case IDs in target manifest")
    selected = set(args.case_id)
    indexed_cases = [(index, case) for index, case in enumerate(cases) if not selected or str(case["case_id"]) in selected]
    if selected - {str(case["case_id"]) for case in cases}:
        raise RuntimeError("unknown requested case IDs: " + ", ".join(sorted(selected - {str(c['case_id']) for c in cases})))
    if args.limit is not None:
        indexed_cases = indexed_cases[: args.limit]

    run_root = args.output_root / args.run_id
    run_root.mkdir(parents=True, exist_ok=True)
    started_at = datetime.now(UTC).isoformat()
    run_metadata = {
        "schema_version": "1.0.0",
        "run_id": args.run_id,
        "dataset_id": args.dataset_id,
        "source_dataset_id": args.dataset_id,
        "case_prefix": str(
            manifest.get("case_prefix")
            or str(manifest["cases"][0]["case_id"]).split("-", 1)[0]
        ),
        "support_policy": str(manifest.get("support_policy") or "require-all"),
        "framework": "Ab-PXRD-Solver",
        "source_commit": SOURCE_COMMIT,
        "gsasii_commit": GSASII_COMMIT,
        "mace_model_sha256": MACE_MODEL_SHA256,
        "target_manifest_sha256": sha256_file(args.targets / "manifest.json"),
        "source_manifest_sha256": manifest.get("source_manifest_sha256"),
        "selected_case_ids": [str(case["case_id"]) for _, case in indexed_cases],
        "expected_case_count": len(indexed_cases),
        "workers": args.workers,
        "case_timeout_seconds": args.timeout,
        "seed_base": args.seed_base,
        "started_at_utc": started_at,
        "host": platform.node(),
        "compute": "AWS EC2 CPU",
        "composition_serialization": "expanded_integer_formula_no_parentheses",
    }
    metadata_path = run_root / "RUN.json"
    if metadata_path.exists():
        previous = json.loads(metadata_path.read_text(encoding="utf-8"))
        for key in (
            "run_id",
            "dataset_id",
            "source_commit",
            "target_manifest_sha256",
            "case_timeout_seconds",
            "seed_base",
            "selected_case_ids",
        ):
            if previous.get(key) != run_metadata.get(key):
                raise RuntimeError(f"resume metadata mismatch for {key}")
        started_at = str(previous.get("started_at_utc", started_at))
    else:
        write_json_atomic(metadata_path, run_metadata)
        if args.s3_uri:
            upload_path(metadata_path, f"{args.s3_uri.rstrip('/')}/RUN.json")

    pending = [
        (index, case)
        for index, case in indexed_cases
        if not (run_root / f"shard-{index:03d}" / "results.json").is_file()
    ]
    print(f"Starting {len(pending)} pending cases with {args.workers} workers; {len(indexed_cases) - len(pending)} resumed.", flush=True)
    failures: list[str] = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(
                run_case,
                case=case,
                case_index=index,
                manifest=manifest,
                args=args,
                run_root=run_root,
            ): str(case["case_id"])
            for index, case in pending
        }
        for future in as_completed(futures):
            case_id = futures[future]
            try:
                outcome = future.result()
                print(json.dumps({"completed": outcome}, sort_keys=True), flush=True)
            except Exception as exc:
                failures.append(case_id)
                print(json.dumps({"harness_error": {"case_id": case_id, "error": repr(exc)}}), file=sys.stderr, flush=True)
            with _WRITE_LOCK:
                progress = progress_payload(run_root, len(indexed_cases), started_at)
                progress["harness_error_case_ids"] = failures
                write_json_atomic(run_root / "progress.json", progress)
            if args.s3_uri:
                upload_path(run_root / "progress.json", f"{args.s3_uri.rstrip('/')}/progress.json")

    progress = progress_payload(run_root, len(indexed_cases), started_at)
    progress["harness_error_case_ids"] = failures
    progress["completed_at_utc"] = datetime.now(UTC).isoformat()
    progress["case_first_candidates"] = materialize_case_candidates(run_root)
    write_json_atomic(run_root / "progress.json", progress)
    if args.s3_uri:
        upload_path(run_root / "progress.json", f"{args.s3_uri.rstrip('/')}/progress.json")
    print(json.dumps({"final": progress}, sort_keys=True), flush=True)
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
