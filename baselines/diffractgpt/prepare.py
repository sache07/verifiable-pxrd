"""Download and verify immutable DiffractGPT inference artifacts.

The paper checkpoint is small enough to stage locally.  Its 4.13 GB base
model is locked too, but is optional locally because the benchmark will run on
Modal and can download that exact revision while constructing the image.

Examples::

    python3 baselines/diffractgpt/prepare.py download
    python3 baselines/diffractgpt/prepare.py status
    python3 baselines/diffractgpt/prepare.py download --include-base
"""

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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_lock() -> dict[str, Any]:
    return json.loads(LOCK_PATH.read_text(encoding="utf-8"))


def checkout_state(lock: dict[str, Any]) -> tuple[bool, str]:
    pin = lock["source_checkout"]
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


def prepare_checkout(lock: dict[str, Any]) -> None:
    pin = lock["source_checkout"]
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


def artifact_state(artifact: dict[str, Any], destination: Path) -> tuple[bool, str]:
    path = destination / artifact["path"]
    if not path.is_file():
        return False, "missing"
    size = path.stat().st_size
    if size != artifact["size_bytes"]:
        return False, f"size {size}, expected {artifact['size_bytes']}"
    digest = sha256_file(path)
    if digest != artifact["sha256"]:
        return False, f"sha256 {digest}, expected {artifact['sha256']}"
    return True, digest


def artifact_url(group: dict[str, Any], artifact: dict[str, Any]) -> str:
    return (
        "https://huggingface.co/"
        + group["repository"]
        + "/resolve/"
        + group["revision"]
        + "/"
        + artifact["path"]
        + "?download=true"
    )


def selected_groups(lock: dict[str, Any], include_base: bool) -> list[dict[str, Any]]:
    groups = [lock["checkpoint"]]
    if include_base:
        groups.append(lock["base_model"])
    return groups


def status(include_base: bool = False) -> bool:
    lock = load_lock()
    source_ok, source_detail = checkout_state(lock)
    print(f"{'OK' if source_ok else 'BAD':3} source checkout: {source_detail}")
    all_ok = source_ok
    for group in selected_groups(lock, include_base):
        destination = ROOT / group["destination"]
        print(f"PIN {group['repository']}@{group['revision']}")
        for artifact in group["artifacts"]:
            ok, detail = artifact_state(artifact, destination)
            all_ok &= ok
            print(f"{'OK' if ok else 'BAD':3} {artifact['path']}: {detail}")
    if not include_base:
        base = lock["base_model"]
        print(f"PIN base model (remote/Modal): {base['repository']}@{base['revision']}")
    return all_ok


def download(include_base: bool = False) -> None:
    lock = load_lock()
    prepare_checkout(lock)
    for group in selected_groups(lock, include_base):
        destination = ROOT / group["destination"]
        destination.mkdir(parents=True, exist_ok=True)
        for artifact in group["artifacts"]:
            ok, _ = artifact_state(artifact, destination)
            if ok:
                print(f"cached {group['repository']}:{artifact['path']}")
                continue
            target = destination / artifact["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            temporary = target.with_suffix(target.suffix + ".partial")
            request = urllib.request.Request(
                artifact_url(group, artifact),
                headers={"User-Agent": "verifiable-pxrd/1.0"},
            )
            print(f"downloading {group['repository']}:{artifact['path']}")
            try:
                with urllib.request.urlopen(request) as response, temporary.open("wb") as stream:
                    while chunk := response.read(1024 * 1024):
                        stream.write(chunk)
            except Exception:
                temporary.unlink(missing_ok=True)
                raise
            # Verify the partial directly before the atomic rename.
            if temporary.stat().st_size != artifact["size_bytes"]:
                ok = False
                detail = f"size {temporary.stat().st_size}, expected {artifact['size_bytes']}"
            elif sha256_file(temporary) != artifact["sha256"]:
                ok = False
                detail = "sha256 mismatch"
            else:
                ok = True
                detail = artifact["sha256"]
            if not ok:
                temporary.unlink(missing_ok=True)
                raise RuntimeError(f"download verification failed for {artifact['path']}: {detail}")
            temporary.replace(target)
            print(f"verified {artifact['path']}: {detail}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("download", "status"), nargs="?", default="status")
    parser.add_argument(
        "--include-base",
        action="store_true",
        help="also stage and verify the optional 4.13 GB base model",
    )
    args = parser.parse_args()
    if args.command == "download":
        download(include_base=args.include_base)
    if not status(include_base=args.include_base):
        sys.exit(1)


if __name__ == "__main__":
    main()
