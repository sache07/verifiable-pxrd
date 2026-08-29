"""Download and verify the official PXRDGen Code Ocean artifacts.

The authors released PXRDGen as an immutable Code Ocean v1 capsule rather than
as a Git repository. A benchmarkable, inference-focused mirror is staged under
the ignored ``.upstream/PXRDGen`` directory, while checkpoints and the GSAS-II
runtime remain in the ignored ``.runs`` tree.
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
GSASII_PREFIX = ROOT / ".runs" / "envs" / "pxrdgen-gsas2full"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_lock() -> dict[str, Any]:
    return json.loads(LOCK_PATH.read_text(encoding="utf-8"))


def file_state(path: Path, size: int, digest: str) -> tuple[bool, str]:
    if not path.is_file():
        return False, "missing"
    actual_size = path.stat().st_size
    if actual_size != size:
        return False, f"size {actual_size}, expected {size}"
    actual_digest = sha256_file(path)
    if actual_digest != digest:
        return False, f"sha256 {actual_digest}, expected {digest}"
    return True, actual_digest


def source_items(lock: dict[str, Any]) -> list[dict[str, Any]]:
    destination = ROOT / lock["source_destination"]
    base_url = lock["capsule"]["base_url"]
    return [
        {
            **artifact,
            "destination": destination / artifact["capsule_path"],
            "url": f"{base_url}/{artifact['capsule_path']}",
            "label": f"source {artifact['capsule_path']}",
        }
        for artifact in lock["source_artifacts"]
    ]


def model_items(lock: dict[str, Any]) -> list[dict[str, Any]]:
    base_url = lock["capsule"]["base_url"]
    return [
        {
            **artifact,
            "destination": ROOT / artifact["destination"],
            "url": f"{base_url}/{artifact['capsule_path']}",
            "label": f"model {artifact['capsule_path']}",
        }
        for artifact in lock["model_artifacts"]
    ]


def installer_item(lock: dict[str, Any]) -> dict[str, Any]:
    artifact = lock["gsasii_installer"]
    return {
        **artifact,
        "destination": ROOT / artifact["destination"],
        "label": "GSAS-II legacy installer",
    }


def download_item(item: dict[str, Any]) -> None:
    path: Path = item["destination"]
    ok, _ = file_state(path, item["size_bytes"], item["sha256"])
    if ok:
        print(f"cached {item['label']}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".partial")
    request = urllib.request.Request(
        item["url"], headers={"User-Agent": "verifiable-pxrd/1.0"}
    )
    print(f"downloading {item['label']}")
    try:
        with urllib.request.urlopen(request) as response, temporary.open("wb") as stream:
            while chunk := response.read(1024 * 1024):
                stream.write(chunk)
        ok, detail = file_state(temporary, item["size_bytes"], item["sha256"])
        if not ok:
            raise RuntimeError(f"download verification failed: {detail}")
        temporary.replace(path)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
    print(f"verified {item['label']}")


def gsasii_state() -> tuple[bool, str]:
    python = GSASII_PREFIX / "bin" / "python"
    source = GSASII_PREFIX / "GSAS-II" / "GSASII"
    if not python.is_file() or not (source / "GSASIIscriptable.py").is_file():
        return False, "missing (run `python baselines/pxrdgen/prepare.py install-gsasii`)"
    code = (
        "import sys; "
        f"sys.path.insert(0, {str(source)!r}); "
        "import GSASIIpath; print(GSASIIpath.GetVersionNumber())"
    )
    result = subprocess.run([str(python), "-c", code], check=False, capture_output=True, text=True)
    if result.returncode != 0:
        return False, result.stderr.strip() or "GSAS-II import failed"
    revision = result.stdout.strip().splitlines()[-1]
    if revision != "5806":
        return False, f"revision {revision}, expected 5806"
    return True, f"revision {revision}"


def status(*, include_installer: bool = True, include_runtime: bool = True) -> bool:
    lock = load_lock()
    all_ok = True
    items = source_items(lock) + model_items(lock)
    if include_installer:
        items.append(installer_item(lock))
    for item in items:
        ok, detail = file_state(item["destination"], item["size_bytes"], item["sha256"])
        all_ok &= ok
        print(f"{'OK' if ok else 'BAD':3} {item['label']}: {detail}")
    if include_runtime:
        gsas_ok, gsas_detail = gsasii_state()
        all_ok &= gsas_ok
        print(f"{'OK' if gsas_ok else 'BAD':3} GSAS-II runtime: {gsas_detail}")
    return all_ok


def download(include_installer: bool) -> None:
    lock = load_lock()
    items = source_items(lock) + model_items(lock)
    if include_installer:
        items.append(installer_item(lock))
    for item in items:
        download_item(item)


def install_gsasii() -> None:
    ok, detail = gsasii_state()
    if ok:
        print(f"cached GSAS-II runtime: {detail}")
        return
    lock = load_lock()
    installer = installer_item(lock)
    download_item(installer)
    if GSASII_PREFIX.exists():
        raise RuntimeError(
            f"incomplete GSAS-II prefix exists at {GSASII_PREFIX}; move it aside and retry"
        )
    subprocess.run(
        ["bash", str(installer["destination"]), "-b", "-p", str(GSASII_PREFIX)],
        cwd=ROOT,
        check=True,
    )
    ok, detail = gsasii_state()
    if not ok:
        raise RuntimeError(f"GSAS-II installation did not validate: {detail}")
    print(f"verified GSAS-II runtime: {detail}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=("download", "download-all", "install-gsasii", "status"),
        nargs="?",
        default="status",
    )
    args = parser.parse_args()
    if args.command == "download":
        download(include_installer=False)
    elif args.command == "download-all":
        download(include_installer=True)
    elif args.command == "install-gsasii":
        install_gsasii()
    if args.command == "download" and not status(include_installer=False, include_runtime=False):
        sys.exit(1)
    if args.command == "download-all" and not status(include_runtime=False):
        sys.exit(1)
    if args.command == "status" and not status():
        sys.exit(1)


if __name__ == "__main__":
    main()
