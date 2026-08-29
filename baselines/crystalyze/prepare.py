"""Download and verify the published Crystalyze inference artifacts.

The source checkout and model files live in ignored staging directories. The
checkpoint is about 415 MB.

Examples::

    uv run --with gdown python baselines/crystalyze/prepare.py download
    uv run python baselines/crystalyze/prepare.py status
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
    "repository": "https://github.com/ML-PXRD/Crystalyze.git",
    "commit": "d265e8b4687fda9586a73f3eb881bb881171b05b",
    "directory": ".upstream/Crystalyze",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_lock() -> dict[str, Any]:
    return json.loads(LOCK_PATH.read_text(encoding="utf-8"))


def checkout_pin() -> dict[str, Any]:
    return SOURCE_PIN


def checkout_state() -> tuple[bool, str]:
    pin = checkout_pin()
    checkout = ROOT / pin["directory"]
    if not (checkout / ".git").is_dir():
        return False, "missing (run `python baselines/crystalyze/prepare.py download`)"
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=checkout,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    dirty = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=checkout,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if revision != pin["commit"]:
        return False, f"revision {revision}, expected {pin['commit']}"
    if dirty:
        return False, "checkout has local changes"
    return True, revision


def prepare_checkout() -> None:
    pin = checkout_pin()
    checkout = ROOT / pin["directory"]
    checkout.parent.mkdir(parents=True, exist_ok=True)
    if not (checkout / ".git").is_dir():
        subprocess.run(
            ["git", "clone", "--filter=blob:none", "--no-checkout", pin["repository"], checkout],
            check=True,
        )
    dirty = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=checkout,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if dirty:
        raise RuntimeError(f"refusing to change dirty upstream checkout: {checkout}")
    subprocess.run(
        ["git", "fetch", "origin", pin["commit"], "--depth=1"], cwd=checkout, check=True
    )
    subprocess.run(
        ["git", "checkout", "--detach", pin["commit"]], cwd=checkout, check=True
    )


def artifact_path_state(artifact: dict[str, Any], path: Path) -> tuple[bool, str]:
    if not path.is_file():
        return False, "missing"
    size = path.stat().st_size
    if size != artifact["size_bytes"]:
        return False, f"size {size}, expected {artifact['size_bytes']}"
    digest = sha256_file(path)
    if digest != artifact["sha256"]:
        return False, f"sha256 {digest}, expected {artifact['sha256']}"
    return True, digest


def artifact_state(artifact: dict[str, Any], destination: Path) -> tuple[bool, str]:
    return artifact_path_state(artifact, destination / artifact["path"])


def status() -> bool:
    lock = load_lock()
    destination = ROOT / lock["destination"]
    checkout_ok, checkout_detail = checkout_state()
    print(f"{'OK' if checkout_ok else 'BAD':3} source checkout: {checkout_detail}")
    all_ok = checkout_ok
    for artifact in lock["artifacts"]:
        ok, detail = artifact_state(artifact, destination)
        all_ok &= ok
        print(f"{'OK' if ok else 'BAD':3} {artifact['path']}: {detail}")
    return all_ok


def download() -> None:
    prepare_checkout()
    try:
        import gdown
    except ImportError as exc:
        raise SystemExit(
            "gdown is required; run with `uv run --with gdown python "
            "baselines/crystalyze/prepare.py download`"
        ) from exc

    lock = load_lock()
    destination = ROOT / lock["destination"]
    for artifact in lock["artifacts"]:
        ok, _ = artifact_state(artifact, destination)
        if ok:
            print(f"cached {artifact['path']}")
            continue
        target = destination / artifact["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix(target.suffix + ".partial")
        downloaded = gdown.download(id=artifact["file_id"], output=str(temporary), quiet=False)
        if downloaded is None:
            raise RuntimeError(f"download failed for {artifact['path']}")
        ok, detail = artifact_path_state(artifact, temporary)
        if not ok:
            temporary.unlink(missing_ok=True)
            raise RuntimeError(f"download verification failed for {artifact['path']}: {detail}")
        temporary.replace(target)
        print(f"verified {artifact['path']}")


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
