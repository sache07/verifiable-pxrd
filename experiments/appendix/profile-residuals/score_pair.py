"""Re-simulate a clean reference/candidate pair using the locked benchmark builder.

Run inside the pinned GSAS-II environment described by native-refinement.
This is an oracle diagnostic: it reads a reference CIF and performs no refinement.
"""
import argparse
import importlib.util
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
import numpy as np

from metric import clean_rwp

ROOT = Path(__file__).resolve().parents[3]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--sources", type=Path, default=ROOT / ".runs/native-refinement/sources")
    parser.add_argument("--gsas", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.gsas.resolve()))
    os.environ["GSASII_PATH"] = str(args.gsas.resolve())
    sys.path.insert(0, str(ROOT / "pxrd-bench/generation"))
    # The builder needs only this pinned module's GSAS loader. No model or solver is run.
    spec = importlib.util.spec_from_file_location("pxrd_app.tools.gsas", args.sources / "Ab/gsas.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.modules["pxrd_app.tools.gsas"] = module
    import build_ab_pxrd_solver_targets as builder
    profiles = []
    with tempfile.TemporaryDirectory(prefix="fixedparams-upstream-") as temporary:
        tools = Path(temporary) / "pxrd_app/tools"
        tools.mkdir(parents=True)
        shutil.copy2(args.sources / "Ab/INST_XRY.PRM", tools / "INST_XRY.PRM")
        for name, path in (("reference", args.reference), ("candidate", args.candidate)):
            result = builder._simulate_fixedparams_job((name, str(path.resolve()), temporary, 0))
            profiles.append(result["clean"])
    args.output.mkdir(parents=True, exist_ok=True)
    value = clean_rwp(*profiles)
    np.savez_compressed(args.output / "profiles.npz", reference=profiles[0], candidate=profiles[1])
    (args.output / "score.json").write_text(json.dumps({"rwp_percent": value,
        "profile": "fixedparams-v1-clean-reference", "fitted": [], "noise": False}, indent=2) + "\n")
    print(value)


if __name__ == "__main__":
    main()
