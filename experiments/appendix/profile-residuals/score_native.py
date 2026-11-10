"""Recalculate one specialist-native residual using the repository target builders."""
import argparse
import importlib.util
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


def normalize(profile):
    values = np.asarray(profile, dtype=np.float64)
    if values.ndim != 1 or not len(values) or not np.isfinite(values).all() or values.max() <= 0:
        raise ValueError("Invalid native profile")
    return values / values.max()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("method", choices=["crystalyze", "diffractgpt", "decifer", "pxrdgen", "ab-pxrd-solver"])
    parser.add_argument("corpus", choices=["pxrd-100", "pxrd-ood"])
    parser.add_argument("case")
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--sources", type=Path, default=ROOT / ".runs/native-refinement/sources")
    parser.add_argument("--gsas", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(ROOT / "src"))
    directory = ROOT / "baselines" / args.method
    sys.path.insert(0, str(directory))
    builder = module("make_targets", directory / "make_targets.py")
    targets = directory / "targets" / args.corpus
    entry = next(r for r in json.loads((targets / "manifest.json").read_text())["cases"] if r["case_id"] == args.case)
    path = targets / entry["pattern_path"]
    if args.gsas:
        sys.path.insert(0, str(args.gsas.resolve()))
        os.environ["GSASII_PATH"] = str(args.gsas.resolve())
    if args.method == "crystalyze":
        from pymatgen.core import Structure
        from scipy.interpolate import interp1d
        evaluator = module("native_crystalyze_evaluator", directory / "evaluate.py")
        xy = np.loadtxt(path, delimiter=",", skiprows=1)
        observed = normalize(interp1d(xy[:, 0], xy[:, 1], kind="cubic", bounds_error=False, fill_value=0)(np.linspace(5, 90, 8500)))
        observed[:1000] = 0
        candidate = evaluator.model_profile(Structure.from_file(args.candidate))
    elif args.method == "diffractgpt":
        observed = np.loadtxt(path, delimiter=",", skiprows=1)[:, 1]
        candidate, _ = builder.simulate(builder.parse_p1_cif(args.candidate), builder.axis())
        candidate = builder.rounded_profile(candidate)
    elif args.method == "decifer":
        import torch
        from pymatgen.core import Structure
        torch.set_num_threads(1)
        observed = np.loadtxt(path, delimiter=",", skiprows=1)[:, 1]
        candidate, _ = builder.simulate(Structure.from_file(args.candidate), builder.axis())
    elif args.method == "pxrdgen":
        import GSASIIscriptable as g2
        g2.SetPrintLevel("warn")
        observed = np.loadtxt(path)
        candidate, _ = builder.simulate(g2, np, args.candidate.resolve(), args.sources.resolve() / "PXRDGen/INST_XRY_Cu.PRM", args.case)
    else:
        module("pxrd_app.tools.gsas", args.sources / "Ab/gsas.py")
        observed = np.loadtxt(path, delimiter=",", skiprows=1)[:, 1]
        with tempfile.TemporaryDirectory(prefix="native-ab-source-") as temporary:
            tools = Path(temporary) / "pxrd_app/tools"
            tools.mkdir(parents=True)
            shutil.copy2(args.sources / "Ab/INST_XRY.PRM", tools / "INST_XRY.PRM")
            candidate = builder._simulate_job((args.case, str(args.candidate.resolve()), temporary, entry["noise_seed"]))["noisy"]
    observed, candidate = normalize(observed), normalize(candidate)
    if observed.shape != candidate.shape:
        raise ValueError("Native profile shapes differ")
    value = float(100 * np.sqrt(np.sum((observed - candidate) ** 2) / np.sum(observed ** 2)))
    args.output.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(args.output / "profiles.npz", observed=observed, candidate=candidate)
    (args.output / "score.json").write_text(json.dumps({"method": args.method, "case_id": args.case,
        "rwp_percent": value, "metric_basis": "framework-native", "fitted": []}, indent=2) + "\n")
    print(value)


if __name__ == "__main__":
    main()
