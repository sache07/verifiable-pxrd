"""Verify the pinned Ab-PXRD-Solver checkout, runtime, models, and targets."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from verifiable_pxrd.baselines.targets import framework_target_root

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = ROOT.parent
UPSTREAM = ROOT / ".upstream" / "Ab-PXRD-Solver"
GSASII_DIR = ROOT / ".runs" / "envs" / "pxrdgen-gsas2full" / "GSAS-II" / "GSASII"
LOCK_PATH = Path(__file__).with_name("artifacts.lock.json")
EXPECTED_COMMIT = "0d67964dfcbd2e2fa09e79bbbac2f5d020a121e9"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_commit(path: Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=path,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def check_source() -> dict[str, Any]:
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    commit = git_commit(UPSTREAM)
    if commit != EXPECTED_COMMIT or commit != lock["source"]["commit"]:
        raise RuntimeError(f"source commit mismatch: {commit}")
    for record in lock["source"]["artifacts"]:
        relative = Path(record["path"])
        path = UPSTREAM / Path(*relative.parts[1:])
        if not path.is_file():
            raise RuntimeError(f"missing locked source artifact: {path}")
        digest = sha256_file(path)
        if digest != record["sha256"]:
            raise RuntimeError(f"source artifact digest mismatch: {path}")
    return {"commit": commit, "artifact_count": len(lock["source"]["artifacts"])}


def check_imports() -> dict[str, str]:
    import importlib.metadata as metadata

    expected = {
        "numpy": "1.26.4",
        "pandas": "2.2.3",
        "scipy": "1.13.1",
        "matplotlib": "3.9.2",
        "scikit-learn": "1.5.2",
        "pymatgen": "2025.5.28",
        "pyxtal": "1.1.4",
        "ase": "3.25.0",
        "spglib": "2.6.0",
        "torch": "2.6.0+cpu",
        "mace-torch": "0.3.14",
    }
    found = {name: metadata.version(name) for name in expected}
    if found != expected:
        raise RuntimeError(f"runtime package mismatch: expected={expected}, found={found}")
    return found


def check_gsasii_runtime() -> dict[str, Any]:
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))["gsasii_compatibility_runtime"]
    checkout = GSASII_DIR.parent
    if git_commit(checkout) != lock["commit"]:
        raise RuntimeError("GSAS-II compatibility checkout commit mismatch")
    bundle = ROOT / lock["binary_bundle"]["path"]
    artifacts = {
        "pyspg_sha256": bundle / "pyspg.cpython-311-x86_64-linux-gnu.so",
        "pypowder_sha256": bundle / "pypowder.cpython-311-x86_64-linux-gnu.so",
    }
    for key, path in artifacts.items():
        if not path.is_file() or sha256_file(path) != lock["binary_bundle"][key]:
            raise RuntimeError(f"GSAS-II binary digest mismatch: {path}")
    return {
        "commit": lock["commit"],
        "revision": lock["revision"],
        "binary_bundle": lock["binary_bundle"]["path"],
    }


def check_targets() -> dict[str, Any]:
    rows: dict[str, Any] = {}
    for corpus_name, dataset_id in (
        ("pXRD-100", "pXRD-100"),
        ("pXRD-ood", "pXRD-ood-v1"),
    ):
        corpus = REPOSITORY_ROOT / "pxrd-bench" / corpus_name
        source = corpus / "manifest.json"
        target_root = framework_target_root(REPOSITORY_ROOT, "ab-pxrd-solver", corpus)
        target = json.loads((target_root / "manifest.json").read_text(encoding="utf-8"))
        if target["source_dataset_id"] != dataset_id:
            raise RuntimeError(f"{corpus_name}: target dataset mismatch")
        if target["source_manifest_sha256"] != sha256_file(source):
            raise RuntimeError(f"{corpus_name}: stale target manifest")
        if target["case_count"] != 100 or target["supported_case_count"] != 100:
            raise RuntimeError(f"{corpus_name}: incomplete target support")
        for case in target["cases"]:
            for path_key, hash_key in (
                ("pattern_path", "pattern_sha256"),
                ("clean_pattern_path", "clean_pattern_sha256"),
            ):
                path = target_root / case[path_key]
                if sha256_file(path) != case[hash_key]:
                    raise RuntimeError(f"{corpus_name}: target digest mismatch: {path}")
        rows[corpus_name] = {
            "dataset_id": dataset_id,
            "case_count": target["case_count"],
            "supported_case_count": target["supported_case_count"],
        }
    return rows


def check_upstream_numerics() -> dict[str, Any]:
    import numpy as np
    import pandas as pd
    import torch

    sys.path.insert(0, str(UPSTREAM))
    from pxrd_app.tools.density import predict_density_ensemble
    from pxrd_app.tools.gsas import check_gsas_available, simulate_pxrd
    from pxrd_app.tools.manager import RawDataManager
    from pxrd_app.tools.peak_prediction import _get_peak_model
    from pxrd_app.tools.solver import SmartCellSolver

    ok, message = check_gsas_available()
    if not ok:
        raise RuntimeError(message)
    corpus_root = REPOSITORY_ROOT / "pxrd-bench" / "pXRD-100"
    target_root = framework_target_root(REPOSITORY_ROOT, "ab-pxrd-solver", corpus_root)
    target_manifest = json.loads((target_root / "manifest.json").read_text(encoding="utf-8"))
    target_case = next(
        case for case in target_manifest["cases"] if case["case_id"] == "pxrd100-poly-03-a"
    )
    frame = pd.read_csv(target_root / target_case["pattern_path"])
    manager = RawDataManager(
        frame.iloc[:, 0].to_numpy(), frame.iloc[:, 1].to_numpy(), bg_subtract=False
    )
    manager.get_peaks_from_scipy(height=1.5)
    peak_model, window_size, device = _get_peak_model()
    if window_size != 51 or str(device) != "cpu":
        raise RuntimeError(f"unexpected peak model configuration: {window_size}/{device}")
    with torch.inference_mode():
        sample = torch.tensor(manager.y[:window_size], dtype=torch.float32).view(1, -1)
        peak_logits = peak_model(sample)
    if peak_logits.shape != (1, 2) or not torch.isfinite(peak_logits).all():
        raise RuntimeError("peak checkpoint did not produce finite two-class logits")
    density = predict_density_ensemble(str(target_case["formula"]), sigma=2.5)
    if not all(math.isfinite(float(density[key])) for key in ("min", "max")):
        raise RuntimeError("density ensemble returned non-finite bounds")

    source_manifest = json.loads((corpus_root / "manifest.json").read_text(encoding="utf-8"))
    source_case = next(
        case for case in source_manifest["cases"] if case["case_id"] == target_case["case_id"]
    )
    source_cif = corpus_root / source_case["path"]
    with tempfile.TemporaryDirectory(prefix="ab-pxrd-doctor-") as temporary:
        os.environ["PXRD_TMP_ROOT"] = temporary
        _x, clean = simulate_pxrd(
            str(source_cif),
            U=0.2,
            V=-0.2,
            W=2.0,
            X=0.5,
            Y=0.5,
            grainsize=20,
            bg_ratio=0,
            add_noise=False,
            Tmin=10,
            Tmax=80,
            Tstep=0.02,
            wavelength=1.54184,
            max_counts=5000,
            iparams=str(UPSTREAM / "pxrd_app" / "tools" / "INST_XRY.PRM"),
        )
    observed_clean = pd.read_csv(target_root / target_case["clean_pattern_path"])[
        "intensity"
    ].to_numpy()
    maximum_error = float(np.max(np.abs(np.asarray(clean) - observed_clean)))
    if maximum_error > 5.0e-10:
        raise RuntimeError(f"frozen native target mismatch: {maximum_error}")
    return {
        "gsas": message,
        "peak_candidates_before_cnn": len(manager.peaks),
        "peak_checkpoint_logits": [float(value) for value in peak_logits[0]],
        "smart_cell_solver_import": SmartCellSolver.__name__,
        "density_bounds_g_cm3": [float(density["min"]), float(density["max"])],
        "target_resimulation_max_absolute_error": maximum_error,
    }


def main() -> None:
    global UPSTREAM, GSASII_DIR
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", type=Path, default=UPSTREAM)
    parser.add_argument("--gsasii-dir", type=Path, default=GSASII_DIR)
    args = parser.parse_args()
    UPSTREAM = args.upstream.expanduser().resolve()
    GSASII_DIR = args.gsasii_dir.expanduser().resolve()
    for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ[name] = "1"
    os.environ["GSASII_PATH"] = str(GSASII_DIR)
    report = {
        "status": "OK",
        "source": check_source(),
        "runtime": check_imports(),
        "gsasii_runtime": check_gsasii_runtime(),
        "targets": check_targets(),
        "numerics": check_upstream_numerics(),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
