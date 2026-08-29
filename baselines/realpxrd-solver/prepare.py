"""Download and verify the released RealPXRD-Solver inference artifacts.

The source is a pinned, ignored Git checkout.  The selected checkpoints are
the full-corpus lattice-free and lattice-conditioned models used for cells in
the benchmark's <=20-site envelope.  The separately released >25-atom
fine-tuning variants are intentionally not staged.

Examples::

    uv run --with gdown python baselines/realpxrd-solver/prepare.py download
    uv run python baselines/realpxrd-solver/prepare.py status
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = Path(__file__).with_name("artifacts.lock.json")
SOURCE_PIN = {
    "source_id": "realpxrd-solver-code",
    "repository": "https://github.com/liqi-529/RealPXRD-Solver.git",
    "commit": "5e7e60176e1875071a12fb4583a1f0112bc3bcad",
    "directory": ".upstream/RealPXRD-Solver",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_lock() -> dict[str, Any]:
    return json.loads(LOCK_PATH.read_text(encoding="utf-8"))


def source_pin(lock: dict[str, Any]) -> dict[str, Any]:
    if lock["source_checkout_id"] != SOURCE_PIN["source_id"]:
        raise RuntimeError("unexpected RealPXRD-Solver source identifier")
    return SOURCE_PIN


def checkout_state(lock: dict[str, Any]) -> tuple[bool, str]:
    pin = source_pin(lock)
    checkout = ROOT / pin["directory"]
    if not (checkout / ".git").is_dir():
        return False, f"missing; clone {pin['repository']} to {pin['directory']}"
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=checkout,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    dirty_lines = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=checkout,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    dirty = "\n".join(line for line in dirty_lines if "__pycache__/" not in line)
    if revision != pin["commit"]:
        return False, f"revision {revision}, expected {pin['commit']}"
    if dirty:
        return False, "checkout has local changes"
    return True, revision


def prepare_checkout(lock: dict[str, Any]) -> None:
    pin = source_pin(lock)
    checkout = ROOT / pin["directory"]
    if (checkout / ".git").is_dir():
        ok, detail = checkout_state(lock)
        if not ok:
            raise RuntimeError(f"refusing to alter existing source checkout: {detail}")
        print(f"cached source checkout: {detail}")
        return
    if checkout.exists():
        raise RuntimeError(f"source destination exists but is not a Git checkout: {checkout}")
    checkout.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["git", "clone", "--no-checkout", pin["repository"], str(checkout)],
        cwd=ROOT,
        check=True,
    )
    subprocess.run(
        ["git", "checkout", "--detach", pin["commit"]],
        cwd=checkout,
        check=True,
    )
    ok, detail = checkout_state(lock)
    if not ok:
        raise RuntimeError(f"prepared source checkout failed verification: {detail}")
    print(f"verified source checkout: {detail}")


def artifact_path(lock: dict[str, Any], artifact: dict[str, Any]) -> Path:
    return ROOT / lock["destination"] / artifact["path"]


def artifact_state(path: Path, artifact: dict[str, Any]) -> tuple[bool, str]:
    if not path.is_file():
        return False, "missing"
    size = path.stat().st_size
    if size != artifact["size_bytes"]:
        return False, f"size {size}, expected {artifact['size_bytes']}"
    digest = sha256_file(path)
    if digest != artifact["sha256"]:
        return False, f"sha256 {digest}, expected {artifact['sha256']}"
    return True, digest


def status() -> bool:
    lock = load_lock()
    source_ok, source_detail = checkout_state(lock)
    print(f"{'OK' if source_ok else 'BAD':3} source checkout: {source_detail}")
    all_ok = source_ok
    for artifact in lock["artifacts"]:
        path = artifact_path(lock, artifact)
        ok, detail = artifact_state(path, artifact)
        all_ok &= ok
        print(f"{'OK' if ok else 'BAD':3} {artifact['path']}: {detail}")
    return all_ok


def download() -> None:
    try:
        import gdown
    except ImportError as exc:
        raise SystemExit(
            "gdown is required; run with `uv run --with gdown python "
            "baselines/realpxrd-solver/prepare.py download`"
        ) from exc

    lock = load_lock()
    prepare_checkout(lock)
    for artifact in lock["artifacts"]:
        target = artifact_path(lock, artifact)
        ok, _ = artifact_state(target, artifact)
        if ok:
            print(f"cached {artifact['path']}")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix(target.suffix + ".partial")
        downloaded = gdown.download(id=artifact["file_id"], output=str(temporary), quiet=False)
        if downloaded is None:
            temporary.unlink(missing_ok=True)
            raise RuntimeError(f"download failed for {artifact['path']}")
        ok, detail = artifact_state(temporary, artifact)
        if not ok:
            temporary.unlink(missing_ok=True)
            raise RuntimeError(f"download verification failed for {artifact['path']}: {detail}")
        temporary.replace(target)
        print(f"verified {artifact['path']}: {detail}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("download", "status"), nargs="?", default="status")
    args = parser.parse_args()
    if args.command == "download":
        download()
    if not status():
        sys.exit(1)


if __name__ == "__main__":
    main()
