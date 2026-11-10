"""Isolated candidate process; receives no reference CIF or matcher labels."""
from __future__ import annotations

import importlib.metadata
import json
import os
import platform
import sys
import time
import traceback
from pathlib import Path

from common import PROTOCOL, code_hash, digest, read_json, time_limit, verify_task, write_json


def main():
    task = read_json(sys.argv[1])
    root = Path(sys.argv[2]).resolve()
    root.mkdir(parents=True, exist_ok=True)
    os.chdir(root)
    started = time.monotonic()
    result = {"id": task["id"], "protocol": PROTOCOL["id"], "code_sha256": code_hash(),
              "input_sha256": task["candidate_sha256"], "pattern_sha256": task["pattern_sha256"],
              "self_target": task.get("self_target", False), "status": "failed"}
    try:
        if len(sys.argv) > 3 and sys.argv[3] != result["code_sha256"]:
            raise ValueError("Runner changed while the image was building; relaunch from a stable source tree")
        verify_task(task)
        (root / "input.cif").write_text(task["candidate_cif"])
        if task["method"] == "crystalyze":
            from structsnap import run
        else:
            from gsas import run
        if task["method"] == "crystalyze":
            with time_limit(task["timeout_seconds"]):
                result.update(run(task, root))
            try:
                from gsas import diagnostic, observation
                if not task.get("self_target"):
                    result["paired_profile"] = diagnostic(task, root, *observation(task))
            except Exception as error:
                result["paired_profile_error"] = f"{type(error).__name__}: {error}"
        else:
            result.update(run(task, root))
        from pymatgen.core import Structure
        import numpy as np
        before = Structure.from_file(root / "input.cif")
        after = Structure.from_file(root / "refined.cif")
        if not after.is_ordered or not len(after) or after.volume <= 0:
            raise ValueError("Invalid exported cell/occupancy")
        if not np.isfinite(after.frac_coords).all() or not np.isfinite(after.lattice.matrix).all():
            raise ValueError("Nonfinite exported geometry")
        if not before.composition.element_composition.fractional_composition.almost_equals(
            after.composition.element_composition.fractional_composition, rtol=1e-5, atol=1e-8
        ):
            raise ValueError("Export changed elemental proportions")
        result["output_sha256"] = digest((root / "refined.cif").read_bytes())
        result["status"] = "completed"
    except Exception as error:
        if isinstance(error, TimeoutError):
            result["status"] = "timeout"
        result["error"] = f"{type(error).__name__}: {error}"
        stage_path = root / "refinement-stage.json"
        if stage_path.exists():
            result["failure_stage"] = read_json(stage_path)["stage"]
        traceback.print_exc()
    result["wall_seconds"] = time.monotonic() - started
    result["runtime"] = {"python": platform.python_version()}
    for name in ("numpy", "scipy", "pymatgen", "spglib", "torch"):
        try:
            result["runtime"][name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            pass
    write_json(root / "result.json", result)
    write_json(root / "packages.json", {d.metadata["Name"]: d.version for d in importlib.metadata.distributions()})
    return 0 if result["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
