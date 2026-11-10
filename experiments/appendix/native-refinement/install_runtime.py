"""Build-time checks and narrowly specified compatibility/export repairs."""
from __future__ import annotations

import io
import argparse
import os
import tarfile
import time
import urllib.request
from pathlib import Path

from common import digest, read_json, write_json


def replace_once(path, old, new, count=1):
    content = path.read_text()
    if content.count(old) != count:
        raise ValueError(f"Patch target changed: {path}")
    path.write_text(content.replace(old, new))


def patch_sources():
    source = Path(os.environ["REFINEMENT_SOURCES"])
    manifest = read_json(source / "sources.lock.json")
    for name, entry in manifest.items():
        if digest((source / name).read_bytes()) != entry["sha256"]:
            raise ValueError(f"Source changed: {name}")
    replace_once(source / "Crystalyze/cdvae/common/instantiate_sga.py",
                 "from pymatgen.analysis.structure_analyzer import SpacegroupAnalyzer",
                 "from pymatgen.symmetry.analyzer import SpacegroupAnalyzer")
    replace_once(source / "Crystalyze/cdvae/common/full_structure_snap.py",
                 "                    best_loss[j] = losses[-1][j]",
                 "                    best_loss[j] = losses[-1][j]\n                    best_UVW[j] = parameter_dictionary['UVW'][j].detach().clone()")
    # Same optimizer, but return the fitted structure rather than the input path.
    replace_once(source / "Ab/gsas.py", "refined_cif = cif_file",
                 "from gsas import released_export\n" + "PLACEHOLDER", count=2)
    # The two assignments have different indentation; preserve it mechanically.
    path = source / "Ab/gsas.py"
    lines = path.read_text().splitlines()
    for i, line in enumerate(lines):
        if line == "PLACEHOLDER":
            indent = lines[i-1][:len(lines[i-1])-len(lines[i-1].lstrip())]
            lines[i] = indent + "refined_cif = str(released_export(phase, __import__('pathlib').Path(gpx_name).with_suffix('.fitted.cif')))"
    path.write_text("\n".join(lines) + "\n")
    write_json(source / "patched-sources.json", {name: digest((source/name).read_bytes()) for name in manifest})


def install_binaries(gsas_root):
    url = "https://github.com/AdvancedPhotonSource/GSAS-II-buildtools/releases/download/v1.0.1/linux_64_p3.11_n1.26.tgz"
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=45) as response:
                content = response.read()
            break
        except OSError:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)
    binary = gsas_root / "GSASII-bin/linux_64_p3.11_n1.26"
    binary.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(content), mode="r:gz") as archive:
        for member in archive.getmembers():
            if member.isfile():
                (binary / Path(member.name).name).write_bytes(archive.extractfile(member).read())
    expected = {"pyspg.cpython-311-x86_64-linux-gnu.so": "546be345775bcce0250e9fb714bad15a4995ca2f9764ed9519e3edf5816facfa",
                "pypowder.cpython-311-x86_64-linux-gnu.so": "c1cc9be96060a397baadea8a9536b69c8d4ada8035a7d3fda8e6d09b4a41efa4"}
    for name, sha in expected.items():
        if digest((binary/name).read_bytes()) != sha:
            raise ValueError(f"GSAS binary hash mismatch: {name}")
    record = {p.name: digest(p.read_bytes()) for p in binary.iterdir() if p.is_file()}
    write_json(gsas_root / "binary-lock.json", record)
    if os.environ.get("REFINEMENT_SOURCES"):
        write_json(Path(os.environ["REFINEMENT_SOURCES"]) / "binary-lock.json", record)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gsas-root", type=Path, default=Path("/opt/GSAS-II"))
    parser.add_argument("--binaries-only", action="store_true")
    args = parser.parse_args()
    if not args.binaries_only:
        patch_sources()
    install_binaries(args.gsas_root)
