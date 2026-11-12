"""Replay normalized public submissions without access to private run folders.

Example: python replay_bundle.py --conditions baseline evolved --cases case-014
No fitting or model calls. Requires the GSAS-II backend documented in README.md.
Sources are read-only; staged inputs and fresh evaluations go under --output.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tarfile
import tempfile
import warnings
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
BENCH = HERE.parent
ROOT = BENCH.parents[1]
RESULTS = ROOT / "results/experimental-eval/divalent-tungstates-PG15"


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def materialize(bundle, stage, case):
    """Create an evaluator-compatible copy; no source file is rewritten."""
    work = stage / "attempts/solve/workspace"
    work.mkdir(parents=True)
    for f in (bundle / "workspace").iterdir():
        if f.is_file() and f.name != "workspace-files.tar.gz":
            shutil.copyfile(f, work / f.name)
    archive = bundle / "workspace/workspace-files.tar.gz"
    if archive.exists():
        # Nested CIF exports are needed by some result.json representations.
        with tarfile.open(archive, "r:gz") as tar:
            for member in tar:
                if not member.isfile() or not member.name.lower().endswith(".cif"):
                    continue
                dest = (work / member.name).resolve()
                if not dest.is_relative_to(work.resolve()) or member.size > 10_000_000:
                    raise ValueError("Unsafe archived CIF")
                dest.parent.mkdir(parents=True, exist_ok=True)
                with tar.extractfile(member) as src, dest.open("wb") as target:
                    shutil.copyfileobj(src, target)
    inputs = BENCH / "cases" / case
    shutil.copytree(inputs, work / "inputs")
    shutil.copytree(inputs, stage / "cases" / case / "inputs")
    result = work / "result.json"
    if result.exists():
        text = result.read_text().replace("<ATTEMPT_WORKSPACE>/", "")
        result.write_text(text)
    run = stage / "attempts/solve/run"
    run.mkdir()
    launch = bundle / "run/launch.json"
    data = json.loads(launch.read_text()) if launch.exists() else {"status": "no_launch_record"}
    data.setdefault("status", "unknown")
    (run / "launch.json").write_text(json.dumps(data))
    job = {"id": "solve", "case_id": case, "policy": "public-replay", "replicate": 0}
    (stage / "attempts/solve/job.json").write_text(json.dumps(job))
    return job


def replay_one(task):
    condition, row, bundle, output, tolerance = task
    from evaluate_attempt import evaluate

    sources = [p for p in (bundle / "workspace").rglob("*") if p.is_file()]
    before = {str(p.relative_to(bundle)): sha(p) for p in sources}
    output.mkdir(parents=True, exist_ok=False)
    with tempfile.TemporaryDirectory(prefix="stage-", dir=output) as temp:
        stage = Path(temp)
        job = materialize(bundle, stage, row["case"])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = evaluate(stage, job, output / "evaluation", grid_tolerance=tolerance)
    old = row.get("replay_interior_rwp", row.get("replay_interior_rwp_percent"))
    new = result.get("replay_interior_rwp")
    matches = (old is None and new is None) or (
        old is not None and new is not None and abs(old - new) < 1e-6
    )
    unchanged = all(sha(bundle / rel) == digest for rel, digest in before.items())
    record = dict(
        condition=condition,
        case=row["case"],
        replicate=row["replicate"],
        bundle=str(bundle.relative_to(ROOT)),
        published_rwp=old,
        replayed_rwp=new,
        numerical_match=matches,
        sources_unchanged=unchanged,
        grid_tolerance_degrees=tolerance,
        status=result.get("replay", {}).get("status"),
        source_sha256=before,
    )
    (output / "verification.json").write_text(json.dumps(record, indent=2) + "\n")
    return record


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--conditions",
        nargs="+",
        default=[
            "baseline",
            "evolved",
            "framework-access",
            "framework-plus-v6",
            "evolved-framework-v5",
        ],
    )
    p.add_argument("--cases", nargs="+")
    p.add_argument("--replicates", nargs="+", type=int)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--workers", type=int, default=2)
    a = p.parse_args()
    a.output = a.output.resolve()
    if a.output.is_relative_to(RESULTS) or a.output.is_relative_to(BENCH):
        p.error("Output must be outside frozen benchmark and result directories")
    if a.output.exists():
        p.error("Use a new output directory; earlier validations are immutable")
    a.output.mkdir(parents=True)
    tasks = []
    skipped = []
    for condition in a.conditions:
        root = RESULTS / condition
        for row in json.loads((root / "per_attempt.json").read_text()):
            if (a.cases and row["case"] not in a.cases) or (
                a.replicates and row["replicate"] not in a.replicates
            ):
                continue
            key = f"{row['case']}-r{row['replicate']}"
            if row.get("evidence_status") == "assessment_only_source_attempt_unavailable":
                skipped.append(
                    dict(
                        condition=condition,
                        case=row["case"],
                        replicate=row["replicate"],
                        reason=row["evidence_status"],
                        published_rwp=row.get("replay_interior_rwp"),
                    )
                )
                continue
            tasks.append(
                (
                    condition,
                    row,
                    root / "attempts" / key,
                    a.output / condition / key,
                    1e-6 if condition == "baseline-opus" else 1e-7,
                )
            )
    results = []
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        for future in as_completed(pool.submit(replay_one, task) for task in tasks):
            result = future.result()
            results.append(result)
            print(json.dumps(result, default=str), flush=True)
    summary = dict(
        attempts=len(results),
        passed=sum(r["numerical_match"] and r["sources_unchanged"] for r in results),
        skipped=skipped,
        results=sorted(results, key=lambda r: (r["condition"], r["case"], r["replicate"])),
    )
    (a.output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if summary["passed"] != summary["attempts"]:
        raise SystemExit("At least one replay differs; inspect verification.json")


if __name__ == "__main__":
    main()
