"""Fetch only pinned refinement source and instrument files; no model checkpoints."""
from __future__ import annotations

import argparse
import urllib.request
from pathlib import Path

from common import HERE, PROTOCOL, REPO, digest, read_json, write_json

CAPSULE = "https://files.codeocean.com/files/verified/75fac1ae-f64b-41ef-9680-ef896215fa3c_v1.0"


def sources():
    files = {}
    for name in ("full_structure_snap.py", "diffraction.py", "instantiate_sga.py", "segfault_protect.py"):
        files[f"Crystalyze/cdvae/common/{name}"] = (
            f"https://raw.githubusercontent.com/ML-PXRD/Crystalyze/{PROTOCOL['crystalyze_commit']}/cdvae/common/{name}", None)
    for name in ("gsas.py", "INST_XRY.PRM"):
        files[f"Ab/{name}"] = (
            f"https://raw.githubusercontent.com/MaterSim/Ab-PXRD-Solver/{PROTOCOL['ab_commit']}/pxrd_app/tools/{name}", None)
    lock = read_json(REPO / "baselines/pxrdgen/artifacts.lock.json")
    for entry in lock["source_artifacts"]:
        if "/Rietveld/" in entry["capsule_path"]:
            files["PXRDGen/" + Path(entry["capsule_path"]).name] = (
                CAPSULE + "/" + entry["capsule_path"], entry["sha256"])
    return files


def fetch(destination, capsule_source=None):
    manifest = {}
    frozen = read_json(HERE / "sources.lock.json") if (HERE / "sources.lock.json").exists() else {}
    for name, (url, expected) in sources().items():
        expected = expected or frozen.get(name, {}).get("sha256")
        path = destination / name
        if path.exists():
            payload = path.read_bytes()
        elif name.startswith("PXRDGen/") and capsule_source:
            payload = (capsule_source / "code/Rietveld" / Path(name).name).read_bytes()
        else:
            with urllib.request.urlopen(url, timeout=90) as response:
                payload = response.read()
        if expected and digest(payload) != expected:
            raise ValueError(f"Source hash mismatch: {name}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
        manifest[name] = {"url": url, "sha256": digest(payload)}
        print(name, digest(payload), flush=True)
    write_json(destination / "sources.lock.json", manifest)
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, default=REPO / ".runs/native-refinement/sources")
    parser.add_argument("--capsule-source", type=Path, help="Unpacked official capsule (if its file server denies downloads)")
    args = parser.parse_args()
    fetch(args.destination, args.capsule_source)
