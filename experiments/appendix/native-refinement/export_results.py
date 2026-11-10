"""Create a small public result bundle from explicitly selected local run folders."""
import argparse
import gzip
import shutil
import io
import tarfile
from pathlib import Path
from common import digest, fingerprint, read_json, write_json

KEEP = {"input.cif", "refined.cif", "result.json", "paired-profile.json", "paired-profiles.npz", "refinement-stage.json", "profile-recheck.json", "rechecked-profiles.npz"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--runs", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--runners", type=Path, help="Directory containing hash-named source snapshots")
    parser.add_argument("--omit-profile-arrays", action="store_true", help="Keep CIFs and metric JSON; regenerate dense arrays from pinned inputs/code")
    parser.add_argument("--method", help="Export only this method, retaining all of its candidates")
    parser.add_argument("--source-snapshot", type=Path, action="append", default=[],
                        help="Frozen local worker source; repeat for runs with different source versions")
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("Choose a new bundle path; existing output will not be overwritten")
    args.output.mkdir(parents=True)
    metadata = args.output / "inputs"
    metadata.mkdir()
    for filename in ("manifest.json", "local-index.json", "missing.json"):
        shutil.copy2(args.inputs / filename, metadata / filename)
    if args.method:
        for filename in ("local-index.json", "missing.json"):
            original = read_json(metadata / filename)
            filtered = [item for item in original if item["id"].startswith(args.method + "/")]
            write_json(metadata / filename, filtered)
        original = read_json(metadata / "manifest.json")
        write_json(metadata / "manifest.json", {"pilot": original["pilot"],
            "method": args.method, "count": len(read_json(metadata / "local-index.json")),
            "source_manifest_sha256": digest((args.inputs / "manifest.json").read_bytes())})
    sources = {}
    runner_hashes = set()
    for run in args.runs:
        for result in sorted((run / "candidates").rglob("result.json")):
            identifier = read_json(result)["id"]
            if args.method and not identifier.startswith(args.method + "/"):
                continue
            runner_hashes.add(read_json(result).get("code_sha256"))
            target = args.output / "candidates" / identifier
            if target.exists():
                raise ValueError(f"Duplicate result ID: {identifier}")
            target.mkdir(parents=True)
            for path in result.parent.iterdir():
                if args.omit_profile_arrays and path.suffix == ".npz":
                    continue
                if path.name in KEEP or (path.name.startswith("stage-") and path.suffix in {".cif", ".npz"}):
                    shutil.copy2(path, target / path.name)
                elif path.name == "stages.json":
                    (target / "stages.json.gz").write_bytes(gzip.compress(path.read_bytes(), mtime=0))
                elif path.suffix == ".log":
                    (target / (path.name + ".gz")).write_bytes(gzip.compress(path.read_bytes(), mtime=0))
                elif path.name in {"packages.json", "sources.lock.json", "patched-sources.json", "binary-lock.json"}:
                    sha = digest(path.read_bytes())
                    store = args.output / "provenance" / (sha + ".json")
                    store.parent.mkdir(exist_ok=True)
                    if not store.exists():
                        shutil.copy2(path, store)
                    sources.setdefault(identifier, {})[path.name] = str(store.relative_to(args.output))
    if args.runners:
        for sha in runner_hashes - {None}:
            source = args.runners / f"{sha}.tar.gz"
            if not source.exists():
                raise FileNotFoundError(f"Missing actual worker source snapshot: {source}")
            target = args.output / "runners" / source.name
            target.parent.mkdir(exist_ok=True)
            shutil.copy2(source, target)
    snapshot_hashes = set()
    for snapshot in args.source_snapshot:
        paths = sorted(p for p in snapshot.iterdir() if p.is_file() and p.suffix in {".py", ".json"})
        sha = fingerprint({p.name: digest(p.read_bytes()) for p in paths if p.suffix == ".py"})
        if sha not in runner_hashes:
            raise ValueError(f"Frozen source does not match actual worker results: {sha} vs {runner_hashes}")
        snapshot_hashes.add(sha)
        buffer = io.BytesIO()
        with tarfile.open(fileobj=buffer, mode="w") as archive:
            for path in paths:
                data = path.read_bytes()
                info = tarfile.TarInfo(path.name)
                info.size = len(data)
                archive.addfile(info, io.BytesIO(data))
        target = args.output / "runners" / f"{sha}.tar.gz"
        target.parent.mkdir(exist_ok=True)
        target.write_bytes(gzip.compress(buffer.getvalue(), mtime=0))
    if args.source_snapshot and snapshot_hashes != runner_hashes:
        raise ValueError(f"Missing worker source snapshots: {runner_hashes - snapshot_hashes}")
    files = {str(p.relative_to(args.output)): digest(p.read_bytes()) for p in sorted(args.output.rglob("*")) if p.is_file()}
    write_json(args.output / "manifest.json", {"files": files, "provenance": sources,
        "selection": "Explicit run folders; no filtering by success or fit score", "profile_arrays_omitted": args.omit_profile_arrays,
        "pilot": read_json(args.inputs / "manifest.json")["pilot"]})


if __name__ == "__main__":
    main()
