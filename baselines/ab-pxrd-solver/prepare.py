"""Stage and verify the pinned Ab-PXRD-Solver source and MACE artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = Path(__file__).with_name("artifacts.lock.json")
UPSTREAM = ROOT / ".upstream" / "Ab-PXRD-Solver"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_lock() -> dict[str, Any]:
    return json.loads(LOCK_PATH.read_text(encoding="utf-8"))


def source_path(relative: str) -> Path:
    parts = Path(relative).parts
    return UPSTREAM / Path(*parts[1:])


def sync_source(lock: dict[str, Any]) -> None:
    source = lock["source"]
    UPSTREAM.parent.mkdir(parents=True, exist_ok=True)
    if not (UPSTREAM / ".git").is_dir():
        subprocess.run(
            [
                "git",
                "clone",
                "--filter=blob:none",
                "--no-checkout",
                source["repository"],
                UPSTREAM,
            ],
            check=True,
        )
    dirty = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=UPSTREAM,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if dirty:
        raise RuntimeError(f"refusing to change dirty upstream checkout: {UPSTREAM}")
    subprocess.run(
        ["git", "fetch", "origin", source["commit"], "--depth=1"],
        cwd=UPSTREAM,
        check=True,
    )
    subprocess.run(
        ["git", "checkout", "--detach", source["commit"]], cwd=UPSTREAM, check=True
    )


def mace_path(lock: dict[str, Any]) -> Path:
    return ROOT / str(lock["mace_small"]["cache_path"])


def download_mace(lock: dict[str, Any]) -> None:
    artifact = lock["mace_small"]
    target = mace_path(lock)
    if target.is_file() and sha256_file(target) == artifact["sha256"]:
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(".partial")
    request = urllib.request.Request(
        artifact["download_url"], headers={"User-Agent": "verifiable-pxrd/1.0"}
    )
    with urllib.request.urlopen(request) as response, temporary.open("wb") as stream:
        while chunk := response.read(1024 * 1024):
            stream.write(chunk)
    if temporary.stat().st_size != artifact["size_bytes"]:
        temporary.unlink(missing_ok=True)
        raise RuntimeError("downloaded MACE model has the wrong size")
    if sha256_file(temporary) != artifact["sha256"]:
        temporary.unlink(missing_ok=True)
        raise RuntimeError("downloaded MACE model has the wrong digest")
    temporary.replace(target)


def status(lock: dict[str, Any]) -> bool:
    expected_commit = str(lock["source"]["commit"])
    if (UPSTREAM / ".git").is_dir():
        actual_commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=UPSTREAM,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    else:
        actual_commit = "missing"
    source_ok = actual_commit == expected_commit
    print(f"{'OK' if source_ok else 'BAD':3} source: {actual_commit}")
    all_ok = source_ok
    for artifact in lock["source"]["artifacts"]:
        path = source_path(str(artifact["path"]))
        ok = path.is_file() and sha256_file(path) == artifact["sha256"]
        all_ok &= ok
        print(f"{'OK' if ok else 'BAD':3} {artifact['path']}")
    model = mace_path(lock)
    model_ok = model.is_file() and sha256_file(model) == lock["mace_small"]["sha256"]
    all_ok &= model_ok
    print(f"{'OK' if model_ok else 'BAD':3} MACE-MP small")
    return all_ok


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("download", "status"), nargs="?", default="status")
    args = parser.parse_args()
    lock = load_lock()
    if args.command == "download":
        sync_source(lock)
        download_mace(lock)
    if not status(lock):
        sys.exit(1)


if __name__ == "__main__":
    main()
