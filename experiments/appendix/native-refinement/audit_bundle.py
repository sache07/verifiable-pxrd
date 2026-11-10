"""Check bundled CIF/source hashes and independently recompute saved fit metrics."""
import argparse
import tarfile
from pathlib import Path
import numpy as np
from common import digest, fingerprint, read_json, write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path, help="Bundle, or output directory when --raw-runs is used")
    parser.add_argument("--raw-runs", type=Path, nargs="+", help="Audit raw arrays/CIF hashes before compact export")
    parser.add_argument("--seal", action="store_true", help="Record newly generated report files after checking existing artifact hashes")
    args = parser.parse_args()
    root = args.bundle
    manifest = read_json(root / "manifest.json") if not args.raw_runs else {"files": {}}
    for name, expected in manifest["files"].items():
        if digest((root / name).read_bytes()) != expected:
            raise ValueError(f"Bundle artifact changed: {name}")
    for archive in (root / "runners").glob("*.tar.gz"):
        with tarfile.open(archive) as stream:
            actual = fingerprint({member.name: digest(stream.extractfile(member).read())
                                  for member in stream.getmembers() if member.name.endswith(".py")})
        if archive.name != actual + ".tar.gz":
            raise ValueError(f"Runner identity mismatch: {archive}")
    candidates, paired, native, rechecked = 0, 0, 0, 0
    seen = set()
    paths = (p for run in args.raw_runs or [root] for p in (run / "candidates").rglob("result.json"))
    for path in paths:
        result, directory = read_json(path), path.parent
        if result["id"] in seen:
            raise ValueError("Duplicate candidate across runs: " + result["id"])
        seen.add(result["id"])
        candidates += 1
        if digest((directory / "input.cif").read_bytes()) != result["input_sha256"]:
            raise ValueError(f"Input CIF identity mismatch: {directory}")
        if result["status"] == "completed" and digest((directory / "refined.cif").read_bytes()) != result["output_sha256"]:
            raise ValueError(f"Output CIF identity mismatch: {directory}")
        if (directory / "paired-profiles.npz").exists():
            with np.load(directory / "paired-profiles.npz") as profiles:
                y = profiles["observed"]
                for side in ("before", "after"):
                    value = 100 * np.sqrt(np.sum((y - profiles[side])**2) / np.sum(y**2))
                    if abs(value - result["paired_profile"][side]["rwp_percent"]) > 1e-8:
                        raise ValueError(f"Paired residual mismatch: {directory}/{side}")
            paired += 1
        if (directory / "rechecked-profiles.npz").exists():
            record = read_json(directory / "profile-recheck.json")
            if record["input_sha256"] != result["input_sha256"] or record["output_sha256"] != result["output_sha256"]:
                raise ValueError(f"Recheck candidate hashes differ: {directory}")
            with np.load(directory / "rechecked-profiles.npz") as profiles:
                y = profiles["observed"]
                for side in ("before", "after"):
                    value = 100 * np.sqrt(np.sum((y - profiles[side])**2) / np.sum(y**2))
                    if not np.isfinite(value) or abs(value - record["paired_profile"][side]["rwp_percent"]) > 1e-8:
                        raise ValueError(f"Rechecked residual mismatch: {directory}/{side}")
            rechecked += 1
        for stage in result.get("stages", []):
            profile = directory / f"stage-{stage['stage']}-profile.npz"
            if not profile.exists():
                continue
            with np.load(profile) as arrays:
                y, calc = arrays["observed"].astype(float), arrays["calculated"].astype(float)
                value = -np.dot(y, calc) / (np.linalg.norm(y) * np.linalg.norm(calc))
                if abs(value - stage["fresh_negative_cosine"]) > 2e-6:
                    raise ValueError(f"Native cosine mismatch: {profile}")
            native += 1
    audit = {"candidates": candidates, "paired_profiles_verified": paired, "native_stage_profiles_verified": native,
             "rechecked_profiles_verified": rechecked,
             "all_preexisting_artifact_hashes_verified": not bool(args.raw_runs), "cif_hashes_verified": True}
    write_json(root / ("raw-audit.json" if args.raw_runs else "audit.json"), audit)
    if args.raw_runs and args.seal:
        raise ValueError("Raw runs cannot seal a bundle manifest")
    if args.seal:
        manifest["files"] = {str(p.relative_to(root)): digest(p.read_bytes()) for p in sorted(root.rglob("*"))
                             if p.is_file() and p != root / "manifest.json"}
        write_json(root / "manifest.json", manifest)
    print(audit)


if __name__ == "__main__":
    main()
