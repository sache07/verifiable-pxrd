"""Bounded, resumable Modal pilot/sweep. No reference data is uploaded."""
from __future__ import annotations

import io
import fcntl
import os
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import modal

from common import HERE, PROTOCOL, REPO, code_hash, fingerprint, read_json, reservation_usd, verify_task, write_json

SOURCE_HASH_AT_IMPORT = code_hash()
SOURCES = Path(os.environ.get("NATIVE_REFINEMENT_SOURCES", REPO / ".runs/native-refinement/sources"))
app = modal.App("pxrd-native-refinement-v2")
volume = modal.Volume.from_name("pxrd-native-refinement-v2", create_if_missing=True)
base = (modal.Image.debian_slim(python_version="3.11")
    .apt_install("git", "libgfortran5", "libgomp1")
    .pip_install("numpy==1.26.4", "scipy==1.11.4", "pymatgen==2023.8.10", "spglib==2.7.0",
                 "matplotlib==3.8.4", "PyCifRW==4.4.6", "h5py==3.11.0", "pillow==10.4.0")
    .run_commands("git clone --quiet https://github.com/AdvancedPhotonSource/GSAS-II.git /opt/GSAS-II",
                  f"git -C /opt/GSAS-II checkout --quiet {PROTOCOL['gsas_commit']}")
    .add_local_dir(SOURCES, "/opt/refinement-sources", copy=True)
    .add_local_dir(HERE, "/opt/refinement", copy=True, ignore=["__pycache__", ".pytest_cache"])
    .env({"REFINEMENT_SOURCES": "/opt/refinement-sources", "GSASII_PATH": "/opt/GSAS-II/GSASII",
          "PYTHONPATH": "/opt/refinement:/opt/GSAS-II/GSASII", "MPLBACKEND": "Agg",
          "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"})
    .run_commands("python /opt/refinement/install_runtime.py", "python -c 'import GSASIIscriptable; import pyspg; import pypowder'"))
gpu_image = base.pip_install("torch==2.2.2")


def execute(task, campaign, source_hash):
    verify_task(task)
    started = time.monotonic()
    key = fingerprint({"task": task, "source": source_hash})
    destination = Path("/outputs") / campaign / key
    volume.reload()
    if (destination / "result.json").exists():
        return pack(destination, task, key)
    destination.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="native-refinement-") as temporary:
        root = Path(temporary)
        write_json(root / "task.json", task)
        with (destination / "worker.log").open("w") as log:
            proc = subprocess.Popen([sys.executable, "/opt/refinement/worker.py", str(root / "task.json"), str(destination), source_hash],
                                    stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
            try:
                returncode = proc.wait(timeout=task["timeout_seconds"] + 120)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.wait()
                returncode = -9
        if not (destination / "result.json").exists():
            write_json(destination / "result.json", {"id": task["id"], "status": "timeout" if returncode == -9 else "crashed",
                "returncode": returncode, "wall_seconds": time.monotonic()-started, "input_sha256": task["candidate_sha256"]})
    result = read_json(destination / "result.json")
    result.update(task_fingerprint=key, remote_wall_seconds=time.monotonic()-started, source_code_sha256=source_hash)
    write_json(destination / "result.json", result)
    for name in ("sources.lock.json", "patched-sources.json", "binary-lock.json"):
        (destination/name).write_bytes((Path("/opt/refinement-sources")/name).read_bytes())
    volume.commit()
    return pack(destination, task, key)


def pack(destination, task, key):
    # Small portable artifacts; leave bulky GSAS projects on the persistent Volume.
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as archive:
        for path in sorted(destination.rglob("*")):
            if path.is_file() and path.suffix in {".cif", ".json", ".log", ".npz"}:
                archive.add(path, arcname=str(path.relative_to(destination)))
    return {"id": task["id"], "key": key, "archive": buffer.getvalue(), "result": read_json(destination / "result.json")}


@app.function(image=base, cpu=(2, 2), memory=(8192, 8192), timeout=2100,
              max_containers=int(os.environ.get("NATIVE_CPU_CONCURRENCY", "4")),
              scaledown_window=2, retries=0, volumes={"/outputs": volume})
def cpu_worker(task, campaign, source_hash):
    return execute(task, campaign, source_hash)


@app.function(image=gpu_image, gpu=["T4", "L4"], cpu=(2, 2), memory=(8192, 8192), timeout=3900,
              max_containers=int(os.environ.get("NATIVE_GPU_CONCURRENCY", "2")),
              scaledown_window=2, retries=0, volumes={"/outputs": volume})
def gpu_worker(task, campaign, source_hash):
    return execute(task, campaign, source_hash)


def collect(payload, output):
    destination = output / "candidates" / payload["id"]
    destination.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(payload["archive"]), mode="r:gz") as archive:
        for member in archive.getmembers():
            if member.issym() or member.islnk() or not (destination / member.name).resolve().is_relative_to(destination.resolve()):
                raise ValueError("Unsafe result archive")
        archive.extractall(destination, filter="data")
    print(payload["id"], payload["result"]["status"], round(payload["result"].get("wall_seconds", 0), 1), flush=True)


@app.local_entrypoint()
def main(tasks: str, output: str, campaign: str = "pilot-20261109", methods: str = "", limit: int = 0,
         self_target: bool = False, diagnostic_iterations: int = 0, budget: float = 50.,
         budget_ledger: str = str(REPO / ".runs/native-refinement/budget-ledger.json"), allow_full: bool = False):
    if not campaign.replace("-", "").replace("_", "").isalnum():
        raise ValueError("Unsafe campaign name")
    selected = read_json(tasks)
    manifest = read_json(Path(tasks).parent / "manifest.json")
    if not manifest["pilot"] and not allow_full:
        raise ValueError("Full sweep requires explicit --allow-full and prior spending approval")
    if methods:
        selected = [t for t in selected if t["method"] in methods.split(",")]
    if limit:
        selected = selected[:limit]
    if self_target or diagnostic_iterations:
        for t in selected:
            t["self_target"] = self_target
            t["id"] += "-self" if self_target else "-smoke"
            if diagnostic_iterations and t["method"] == "crystalyze":
                t["diagnostic_iterations"] = diagnostic_iterations
                t["timeout_seconds"] = min(t["timeout_seconds"], 300)
    root = Path(output)
    root.mkdir(parents=True, exist_ok=True)
    ledger_path = Path(budget_ledger)
    source_hash = SOURCE_HASH_AT_IMPORT
    queued = []
    for task in selected:
        target = root / "candidates" / task["id"] / "result.json"
        if target.exists():
            old = read_json(target)
            if old.get("task_fingerprint") == fingerprint({"task": task, "source": source_hash}):
                continue
            raise ValueError(f"Existing result belongs to different inputs/code: {target}; use a separate output directory")
        verify_task(task)
        queued.append(task)
    reservation = sum(reservation_usd(t) for t in queued)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot = root / "runner"
    snapshot.mkdir(exist_ok=True)
    for path in HERE.iterdir():
        if path.is_file() and path.suffix in {".py", ".json"}:
            shutil.copy2(path, snapshot / path.name)
    calls = []
    with ledger_path.with_suffix(".lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        ledger = read_json(ledger_path) if ledger_path.exists() else {"reserved_usd": 5., "calls": [], "build_overhead_allowance_usd": 5.}
        if ledger["reserved_usd"] + reservation > budget:
            raise ValueError(f"Reservation ${ledger['reserved_usd']+reservation:.2f} exceeds cap ${budget:.2f}")
        ledger["reserved_usd"] += reservation
        write_json(ledger_path, ledger)
        print(f"Reserved ${reservation:.2f} for {len(queued)} calls (conservative resource estimate).", flush=True)
        for task in queued:
            function = gpu_worker if task["method"] == "crystalyze" else cpu_worker
            call = function.spawn(task, campaign, source_hash)
            calls.append(call)
            ledger["calls"].append({"id": task["id"], "call_id": call.object_id, "reservation_usd": reservation_usd(task),
                                    "output": str(root.resolve()), "campaign": campaign, "source_hash": source_hash})
            write_json(ledger_path, ledger)
    with ThreadPoolExecutor(max_workers=16) as pool:
        futures = {pool.submit(call.get): call for call in calls}
        for future in as_completed(futures):
            try:
                collect(future.result(), root)
            except Exception as error:
                print(f"Collection failed for {futures[future].object_id}: {error}; recover using collect.py", flush=True)
