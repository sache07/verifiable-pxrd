"""Instrument the first StructSnap schedule or its lattice-only first stage.

Neither mode executes the release's complete multi-schedule refinement search.
"""
from __future__ import annotations

import io
import os
import sys
import time
from pathlib import Path

import numpy as np

from common import digest, write_json


def run(task, root):
    import torch
    from pymatgen.core import Structure
    from pymatgen.io.cif import CifWriter

    if not torch.cuda.is_available():
        raise RuntimeError("StructSnap requires a CUDA GPU; no CPU fallback")
    torch.set_num_threads(2)
    torch.manual_seed(20260915)
    np.random.seed(20260915)
    source = Path(os.environ["REFINEMENT_SOURCES"]) / "Crystalyze"
    sys.path.insert(0, str(source))
    from cdvae.common.full_structure_snap import FullStructureSnapper

    data = np.loadtxt(io.StringIO(task["pattern_text"]), delimiter=",", skiprows=1)
    angles, intensity = data.T
    step = float(np.median(np.diff(angles)))
    if len(angles) != 8500 or not np.allclose(np.diff(angles), step):
        raise ValueError("Unexpected StructSnap observation grid")
    wavelength = task["wavelength"]
    # The native binning uses an exclusive upper bound: 5...89.99 => [5,90).
    qmin, qmax = 4 * np.pi * np.sin(np.radians([angles[0], angles[-1] + step]) / 2) / wavelength
    records = []
    stages = []
    mode = task.get("structsnap_mode", "two-stage")
    if mode not in {"two-stage", "lattice-stage1"}:
        raise ValueError(f"Unknown StructSnap mode: {mode}")
    last_stage = 1 if mode == "lattice-stage1" else 2
    for number in range(1, last_stage + 1):
        stages.append(dict(batch_size=1, bin_batch_size=1, learning_rate=0.0004,
            iterations=task.get("diagnostic_iterations", 30001), UVW=torch.tensor([0., 0., 1.5], device="cuda:0"),
            snap_lengths=True, snap_angles=False, snap_coords=number == 2,
            snap_UVW=[False, False, True], symmeterize=True, force_angles=False,
            slow_peak_shape=False, convergence_tolerance=-0.001, UVW_exponent=1.5,
            UVW_rate_slow=1, UVW_rate=5, finished=number == last_stage))

    class InstrumentedSnapper(FullStructureSnapper):
        def fine_snap_structure(self, patterns, structures, parameter_dictionary=None, plot_dictionary=None):
            number = len(records) + 1
            trace = []
            base = self.calculate_fine_loss

            def measured(*args, **kwargs):
                value = base(*args, **kwargs)
                trace.append(float(value[0][0]))
                return value

            self.calculate_fine_loss = measured
            started = time.monotonic()
            try:
                batch, uvw, losses = super().fine_snap_structure(
                    patterns, structures, parameter_dictionary, plot_dictionary)
            finally:
                self.calculate_fine_loss = base
            structure = self.batch_to_structure(batch)
            out = root / f"stage-{number}.cif"
            CifWriter(structure, significant_figures=12).write_file(out)
            with torch.no_grad():
                fresh, profile = base(patterns, batch, UVW=uvw, mini_batch_size=1, bin_batch_size=1)
                reloaded, _ = base(patterns, self.structure_to_batch(Structure.from_file(out)),
                                   UVW=uvw, mini_batch_size=1, bin_batch_size=1)
            if not torch.isfinite(profile).all() or not torch.isfinite(uvw).all() or float(uvw[0, 2]) <= 0:
                raise ValueError("Invalid returned StructSnap profile/UVW")
            if abs(fresh[0] - reloaded[0]) > 1e-4:
                raise ValueError("Exported CIF does not reproduce StructSnap profile fit")
            np.savez_compressed(root / f"stage-{number}-profile.npz", two_theta=angles,
                                observed=patterns.detach().cpu().numpy()[0],
                                calculated=profile.detach().cpu().numpy()[0])
            record = {"stage": number, "iterations": len(trace), "wall_seconds": time.monotonic() - started,
                      "logged_negative_cosine": float(losses[0]), "fresh_negative_cosine": float(fresh[0]),
                      "roundtrip_negative_cosine": float(reloaded[0]), "uvw": uvw.detach().cpu().tolist(),
                      "cif_sha256": digest(out.read_bytes()), "loss_trace": trace}
            records.append(record)
            write_json(root / "stages.json", records)
            return batch, uvw, losses

    engine = InstrumentedSnapper(q_min=qmin, q_max=qmax, wavelength=wavelength, in_dim=8500,
                                 output_dim=256, scn=False, parameter_dictionaries=stages)
    batch = engine.structure_to_batch(Structure.from_file(root / "input.cif"))
    patterns = torch.tensor(intensity.copy(), device="cuda:0", dtype=torch.float32).unsqueeze(0)
    if task.get("self_target"):
        with torch.no_grad():
            _, patterns = engine.calculate_fine_loss(patterns, batch, mini_batch_size=1, bin_batch_size=1,
                                                     UVW=stages[0]["UVW"].unsqueeze(0))
    with torch.no_grad():
        raw_loss, _ = engine.calculate_fine_loss(patterns.clone(), batch,
            mini_batch_size=1, bin_batch_size=1, UVW=stages[0]["UVW"].unsqueeze(0))
        before_loss, _ = engine.calculate_fine_loss(engine.background_subtraction(patterns.clone()), batch,
            mini_batch_size=1, bin_batch_size=1, UVW=stages[0]["UVW"].unsqueeze(0))
    snapped, loss = engine.full_structure_snap(patterns, batch)
    CifWriter(engine.batch_to_structure(snapped), significant_figures=12).write_file(root / "refined.cif")
    return {"gpu": torch.cuda.get_device_name(), "cuda": torch.version.cuda,
            "structsnap_mode": mode,
            "raw_before_negative_cosine": float(raw_loss[0]),
            "native_before_negative_cosine": float(before_loss[0]),
            "native_after_negative_cosine": records[-1]["fresh_negative_cosine"],
            "reported_final_loss": float(loss[0]), "stages": [{k:v for k,v in r.items() if k != "loss_trace"} for r in records],
            "adaptations": ["pymatgen import repair", "save best UVW alongside best structure",
                            "batch_size=bin_batch_size=1", "observation wavelength and exclusive grid endpoint"],
            "symmetry_tolerance": "native effective symprec=0.01 (wrapper drops keyword arguments)"}
