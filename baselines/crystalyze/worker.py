# ruff: noqa: UP006, UP031, UP035
"""Python 3.8 worker for Crystalyze inference inside a Modal container."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import random
import re
import sys
import tarfile
import tempfile
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, List, Mapping, Sequence, Tuple

REMOTE_ROOT = Path("/opt/crystalyze")
MODEL_ROOT = REMOTE_ROOT / "model_folder"
TARGET_ROOT = REMOTE_ROOT / "targets"
CHECKPOINT_FILENAME = "epoch=804-step=57154.ckpt"
CHECKPOINT_SHA256 = "ee95964d8ca104cdc9fbb55ce54f9e52d891154d35ee1a47031fe01b0d523ee0"
CHECKPOINT_SIZE = 414_720_000
HPARAMS_SHA256 = "d1053e8bbaa5a0d1dbfe528c28d2750dc29b193f75046028ae06a3ec3051af3f"
CRYSTALYZE_COMMIT = "d265e8b4687fda9586a73f3eb881bb881171b05b"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            chunk = stream.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def configure_runtime() -> None:
    os.environ.setdefault("PROJECT_ROOT", str(REMOTE_ROOT))
    os.environ.setdefault("HYDRA_JOBS", "/tmp/crystalyze-hydra")
    os.environ.setdefault("WABDB_DIR", "/tmp/crystalyze-wandb")
    if str(REMOTE_ROOT) not in sys.path:
        sys.path.insert(0, str(REMOTE_ROOT))
    Path(os.environ["HYDRA_JOBS"]).mkdir(parents=True, exist_ok=True)
    Path(os.environ["WABDB_DIR"]).mkdir(parents=True, exist_ok=True)


def portable_load_model() -> Tuple[Any, Any]:
    configure_runtime()
    import hydra
    import torch
    from hydra import initialize_config_dir
    from hydra.experimental import compose

    checkpoint = MODEL_ROOT / CHECKPOINT_FILENAME
    if checkpoint.stat().st_size != CHECKPOINT_SIZE or sha256(checkpoint) != CHECKPOINT_SHA256:
        raise RuntimeError("Crystalyze checkpoint failed its locked size or SHA-256")
    if sha256(MODEL_ROOT / "hparams.yaml") != HPARAMS_SHA256:
        raise RuntimeError("Crystalyze hparams failed its locked SHA-256")
    with initialize_config_dir(str(MODEL_ROOT)):
        cfg = compose(config_name="hparams")
        model = hydra.utils.instantiate(
            cfg.model,
            optim=cfg.optim,
            data=cfg.data,
            logging=cfg.logging,
            _recursive_=False,
        )
    payload = torch.load(str(checkpoint), map_location="cpu")
    state_result = model.load_state_dict(payload["state_dict"], strict=False)
    if state_result.missing_keys or state_result.unexpected_keys:
        raise RuntimeError(
            "checkpoint state mismatch: missing=%s unexpected=%s"
            % (state_result.missing_keys, state_result.unexpected_keys)
        )
    model.lattice_scaler = torch.load(str(MODEL_ROOT / "lattice_scaler.pt"), map_location="cpu")
    model.scaler = torch.load(str(MODEL_ROOT / "prop_scaler.pt"), map_location="cpu")
    model.eval()
    model.cuda(0)
    return model, cfg


def validate_request(payload: Mapping[str, Any]) -> Dict[str, Any]:
    case_ids = [str(value) for value in payload.get("case_ids", [])]
    if not case_ids or len(case_ids) != len(set(case_ids)):
        raise ValueError("case_ids must be a non-empty, deduplicated list")
    samples = int(payload.get("samples", 8))
    n_step_each = int(payload.get("n_step_each", 100))
    run_id = str(payload.get("run_id", "crystalyze-run"))
    shard_index = int(payload.get("shard_index", 0))
    if not 1 <= samples <= 32:
        raise ValueError("samples must be in [1, 32]")
    if not 1 <= n_step_each <= 100:
        raise ValueError("n_step_each must be in [1, 100]")
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", run_id) is None:
        raise ValueError("run_id must be a filesystem-safe identifier")
    if shard_index < 0:
        raise ValueError("shard_index must be non-negative")
    request = {
        "case_ids": case_ids,
        "samples": samples,
        "n_step_each": n_step_each,
        "step_lr": float(payload.get("step_lr", 1e-4)),
        "min_sigma": float(payload.get("min_sigma", 0.0)),
        "seed": int(payload.get("seed", 42)),
        "run_id": run_id,
        "shard_index": shard_index,
    }
    for key in (
        "source_dataset_id",
        "case_prefix",
        "support_policy",
        "source_manifest_sha256",
    ):
        request[key] = str(payload.get(key, ""))
    return request


def target_manifest() -> Tuple[Dict[str, Any], Dict[str, Dict[str, Any]]]:
    payload = json.loads((TARGET_ROOT / "manifest.json").read_text(encoding="utf-8"))
    return payload, {str(case["case_id"]): case for case in payload["cases"]}


def validate_identity(request: Mapping[str, Any], payload: Mapping[str, Any]) -> None:
    source_digest = str(payload.get("source_manifest_sha256", ""))
    if request.get("source_manifest_sha256") != source_digest:
        raise RuntimeError("Crystalyze request source-manifest digest mismatch")
    for key in ("source_dataset_id", "case_prefix", "support_policy"):
        expected = str(payload.get(key, request.get(key, "")))
        if request.get(key) != expected:
            raise RuntimeError("Crystalyze request %s mismatch" % key)


def prepare_inputs(
    case_ids: Sequence[str], samples: int, manifest: Mapping[str, Mapping[str, Any]]
) -> Tuple[Any, Any, List[Dict[str, Any]]]:
    """Reproduce upstream interpolation, normalization, and 15-degree masking."""

    import numpy as np
    import torch
    from pymatgen.core import Element
    from scipy.interpolate import interp1d

    profiles = []
    element_rows = []
    metadata: List[Dict[str, Any]] = []
    for case_id in case_ids:
        if case_id not in manifest:
            raise ValueError("unknown Crystalyze target case: %s" % case_id)
        case = dict(manifest[case_id])
        if not bool(case["model_supported"]):
            raise ValueError("case exceeds the checkpoint's 20-site domain: %s" % case_id)
        values = np.loadtxt(
            str(TARGET_ROOT / str(case["pattern_path"])), delimiter=",", skiprows=1
        )
        interpolator = interp1d(
            values[:, 0], values[:, 1], kind="cubic", bounds_error=False, fill_value=0
        )
        intensity = np.asarray(interpolator(np.linspace(5, 90, 8500)), dtype=np.float32)
        maximum = float(np.max(intensity))
        if not np.isfinite(maximum) or maximum <= 0:
            raise RuntimeError("target has a non-positive interpolation maximum: %s" % case_id)
        intensity /= maximum
        intensity[:1000] = 0.0
        profiles.append(intensity)

        atomic_numbers = [int(Element(symbol).Z) for symbol in case["elements"]]
        if any(number > 100 for number in atomic_numbers):
            raise ValueError("Crystalyze supports elements only through fermium: %s" % case_id)
        padded = np.zeros(256, dtype=np.int64)
        padded[: len(atomic_numbers)] = atomic_numbers
        element_rows.append(padded)
        metadata.append(case)

    profile_tensor = torch.tensor(np.stack(profiles), dtype=torch.float32)
    profile_tensor = profile_tensor.repeat_interleave(samples, dim=0).unsqueeze(1).cuda(0)
    element_tensor = torch.tensor(np.stack(element_rows), dtype=torch.long)
    element_tensor = element_tensor.repeat_interleave(samples, dim=0).cuda(0)
    return profile_tensor, element_tensor, metadata


def seed_everything(seed: int) -> None:
    import numpy as np
    import torch

    random.seed(seed)
    np.random.seed(seed % (2**32 - 1))
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def candidate_records(
    output: Mapping[str, Any],
    case_metadata: Sequence[Mapping[str, Any]],
    samples: int,
    destination: Path,
) -> List[Dict[str, Any]]:
    import numpy as np
    from pymatgen.core import Lattice, Structure
    from pymatgen.io.cif import CifWriter

    num_atoms = output["num_atoms"].detach().cpu().numpy().astype(int)
    lengths = output["lengths"].detach().cpu().numpy()
    angles = output["angles"].detach().cpu().numpy()
    frac_coords = output["frac_coords"].detach().cpu().numpy()
    atom_types = output["atom_types"].detach().cpu().numpy().astype(int)
    expected = len(case_metadata) * samples
    if len(num_atoms) != expected:
        raise RuntimeError("model returned %d crystals, expected %d" % (len(num_atoms), expected))

    records: List[Dict[str, Any]] = []
    atom_offset = 0
    for flat_index, site_count in enumerate(num_atoms.tolist()):
        case_index = flat_index // samples
        sample_index = flat_index % samples
        case_id = str(case_metadata[case_index]["case_id"])
        case_root = destination / "candidates" / case_id
        case_root.mkdir(parents=True, exist_ok=True)
        candidate_name = "candidate-%02d" % (sample_index + 1)
        coords = frac_coords[atom_offset : atom_offset + site_count]
        species = atom_types[atom_offset : atom_offset + site_count]
        atom_offset += site_count
        record: Dict[str, Any] = {
            "case_id": case_id,
            "sample_index": sample_index,
            "best_of_1_member": sample_index == 0,
            "predicted_site_count": site_count,
            "predicted_atomic_numbers": species.tolist(),
            "predicted_lengths_angstrom": lengths[flat_index].tolist(),
            "predicted_angles_deg": angles[flat_index].tolist(),
        }
        try:
            finite = bool(
                site_count > 0
                and np.isfinite(coords).all()
                and np.isfinite(lengths[flat_index]).all()
                and np.isfinite(angles[flat_index]).all()
                and np.all(lengths[flat_index] > 0)
                and np.all(angles[flat_index] > 0)
                and np.all(angles[flat_index] < 180)
            )
            if not finite:
                raise ValueError("non-physical or non-finite predicted lattice")
            lattice = Lattice.from_parameters(
                *lengths[flat_index].tolist(), *angles[flat_index].tolist()
            )
            structure = Structure(lattice, species.tolist(), coords, coords_are_cartesian=False)
            cif_path = case_root / (candidate_name + ".cif")
            cif_path.write_text(str(CifWriter(structure, symprec=None)), encoding="utf-8")
            record.update(
                {
                    "status": "generated",
                    "candidate_path": str(cif_path.relative_to(destination)),
                    "candidate_sha256": sha256(cif_path),
                    "predicted_formula": structure.composition.reduced_formula,
                    "volume_angstrom3": float(structure.volume),
                }
            )
        except Exception as exc:
            error_path = case_root / (candidate_name + ".invalid.json")
            error_path.write_text(
                json.dumps({"error": str(exc), **record}, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            record.update(
                {
                    "status": "invalid",
                    "error": str(exc),
                    "candidate_path": str(error_path.relative_to(destination)),
                    "candidate_sha256": sha256(error_path),
                }
            )
        records.append(record)
    if atom_offset != len(atom_types):
        raise RuntimeError("model atom tensor did not split cleanly")
    return records


def run_request(request_payload: Mapping[str, Any]) -> Tuple[Path, Dict[str, Any]]:
    import torch

    request = validate_request(request_payload)
    target_payload, manifest = target_manifest()
    validate_identity(request, target_payload)
    seed_everything(int(request["seed"]))
    torch.cuda.reset_peak_memory_stats()
    started = time.perf_counter()
    model, cfg = portable_load_model()
    torch.cuda.synchronize()
    loaded = time.perf_counter()
    profiles, elements, metadata = prepare_inputs(
        request["case_ids"], int(request["samples"]), manifest
    )
    ld_kwargs = SimpleNamespace(
        n_step_each=int(request["n_step_each"]),
        step_lr=float(request["step_lr"]),
        min_sigma=float(request["min_sigma"]),
        save_traj=False,
        disable_bar=True,
    )
    with torch.no_grad():
        _, _, latent = model.encode(
            None,
            None,
            None,
            elements,
            None,
            testing=False,
            pv_xrd=profiles,
            multi_hot_encode=None,
        )
        generated = model.langevin_dynamics(
            latent,
            ld_kwargs,
            gt_num_atoms=None,
            gt_atom_types=None,
            gt_elements_input=elements,
        )
    torch.cuda.synchronize()
    generated_at = time.perf_counter()

    run_id = str(request["run_id"])
    shard_name = "shard-%03d" % int(request["shard_index"])
    temporary_root = Path(tempfile.mkdtemp(prefix="crystalyze-output-"))
    destination = temporary_root / run_id / shard_name
    destination.mkdir(parents=True, exist_ok=False)
    records = candidate_records(generated, metadata, int(request["samples"]), destination)
    completed_at = time.perf_counter()
    result = {
        "schema_version": "1.0.0",
        "framework": "Crystalyze",
        "framework_commit": CRYSTALYZE_COMMIT,
        "checkpoint_sha256": CHECKPOINT_SHA256,
        "source_dataset_id": request["source_dataset_id"],
        "case_prefix": request["case_prefix"],
        "support_policy": request["support_policy"],
        "source_manifest_sha256": request["source_manifest_sha256"],
        "run_id": run_id,
        "shard_index": int(request["shard_index"]),
        "case_ids": request["case_ids"],
        "case_count": len(request["case_ids"]),
        "samples_per_case": int(request["samples"]),
        "candidate_count": len(records),
        "generated_candidate_count": sum(r["status"] == "generated" for r in records),
        "invalid_candidate_count": sum(r["status"] == "invalid" for r in records),
        "inference": {
            "force_num_atoms": False,
            "force_atom_types": False,
            "composition_constraint": "allowed_elements_only",
            "n_step_each": int(request["n_step_each"]),
            "noise_levels": int(cfg.model.num_noise_level),
            "step_lr": float(request["step_lr"]),
            "min_sigma": float(request["min_sigma"]),
            "seed": int(request["seed"]),
        },
        "preprocessing": {
            "upstream_interpolation": "cubic to np.linspace(5, 90, 8500)",
            "normalization": "divide by interpolated maximum",
            "masked_leading_bins": 1000,
        },
        "runtime": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "cuda_runtime": str(torch.version.cuda),
            "device_name": torch.cuda.get_device_name(0),
            "device_capability": list(torch.cuda.get_device_capability(0)),
            "model_load_seconds": loaded - started,
            "generation_seconds": generated_at - loaded,
            "serialization_seconds": completed_at - generated_at,
            "total_seconds": completed_at - started,
            "peak_cuda_memory_bytes": int(torch.cuda.max_memory_allocated()),
        },
        "candidates": records,
    }
    (destination / "request.json").write_text(
        json.dumps(request, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (destination / "results.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return destination, result


def archive_directory(destination: Path, archive_path: Path) -> None:
    with tarfile.open(str(archive_path), mode="w:gz") as archive:
        archive.add(destination, arcname="/".join(destination.parts[-2:]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request-json", required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    request = json.loads(args.request_json)
    destination, result = run_request(request)
    archive_directory(destination, args.archive)
    args.summary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
