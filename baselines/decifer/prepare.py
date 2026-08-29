"""Download and verify the official deCIFer inference checkpoint.

The pinned source checkout is intentionally kept under the ignored
``.upstream`` tree. The 665 MB checkpoint similarly lives in ``.runs``.

Examples::

    uv run python baselines/decifer/prepare.py download
    uv run python baselines/decifer/prepare.py status
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
CHECKOUT = ROOT / ".upstream" / "deCIFer"
CHECKOUT_COMMIT = "91ace18de9aa118f1174942fbe1ec85f127c7864"
REPOSITORY = "https://github.com/FrederikLizakJohansen/deCIFer.git"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_lock() -> dict[str, Any]:
    return json.loads(LOCK_PATH.read_text(encoding="utf-8"))


def git(*arguments: str, cwd: Path) -> str:
    return subprocess.run(
        ["git", *arguments],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def checkout_state() -> tuple[bool, str]:
    if not (CHECKOUT / ".git").is_dir():
        return False, "missing (run `python baselines/decifer/prepare.py download`)"
    revision = git("rev-parse", "HEAD", cwd=CHECKOUT)
    dirty = git("status", "--porcelain", cwd=CHECKOUT)
    if revision != CHECKOUT_COMMIT:
        return False, f"revision {revision}, expected {CHECKOUT_COMMIT}"
    if dirty:
        return False, "checkout has local changes"
    return True, revision


def prepare_checkout() -> None:
    CHECKOUT.parent.mkdir(parents=True, exist_ok=True)
    if not (CHECKOUT / ".git").is_dir():
        subprocess.run(
            ["git", "clone", "--filter=blob:none", "--no-checkout", REPOSITORY, CHECKOUT],
            check=True,
        )
    if git("status", "--porcelain", cwd=CHECKOUT):
        raise RuntimeError(f"refusing to change dirty upstream checkout: {CHECKOUT}")
    git("fetch", "origin", CHECKOUT_COMMIT, "--depth=1", cwd=CHECKOUT)
    git("checkout", "--detach", CHECKOUT_COMMIT, cwd=CHECKOUT)


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


def download_file(artifact: dict[str, Any], target: Path) -> None:
    temporary = target.with_suffix(target.suffix + ".partial")
    temporary.unlink(missing_ok=True)
    request = urllib.request.Request(
        artifact["url"], headers={"User-Agent": "verifiable-pxrd/1.0"}
    )
    downloaded = 0
    report_at = 64 * 1024 * 1024
    with urllib.request.urlopen(request) as response, temporary.open("wb") as stream:
        while chunk := response.read(1024 * 1024):
            stream.write(chunk)
            downloaded += len(chunk)
            if downloaded >= report_at:
                print(f"downloaded {downloaded / (1024 * 1024):.0f} MiB")
                report_at += 64 * 1024 * 1024
    ok, detail = artifact_path_state(artifact, temporary)
    if not ok:
        temporary.unlink(missing_ok=True)
        raise RuntimeError(f"download verification failed for {artifact['path']}: {detail}")
    temporary.replace(target)


def download() -> None:
    prepare_checkout()
    lock = load_lock()
    destination = ROOT / lock["destination"]
    for artifact in lock["artifacts"]:
        ok, _ = artifact_state(artifact, destination)
        if ok:
            print(f"cached {artifact['path']}")
            continue
        target = destination / artifact["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        download_file(artifact, target)
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
