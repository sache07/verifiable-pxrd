"""Local, post-hoc scoring of returned CIFs; never exposes labels to workers."""
import argparse
import csv
import importlib.metadata
import sys
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from common import REPO, digest, fingerprint, read_json, write_json

sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))
from baselines.evaluate import guarded_structure_match, minimum_periodic_distance
from verifiable_pxrd.baselines.matching import element_composition_match, primary_metric_metadata
from pymatgen.core import Structure


def evaluate(cif, reference):
    predicted, truth = Structure.from_file(cif), Structure.from_file(reference)
    valid = predicted.volume >= .1 and minimum_periodic_distance(predicted) >= .5
    if not valid or not element_composition_match(predicted, truth):
        return False, ""
    exact, _, error = guarded_structure_match(predicted, truth)
    return exact, error


def score_entry(arguments):
    entry, results, runs = arguments
    method, corpus, case, slot = entry["id"].split("/")
    source = REPO / entry["candidate_path"]
    reference = REPO / entry["reference_path"]
    if digest(reference.read_bytes()) != entry["reference_sha256"]:
        raise ValueError(f"Reference changed: {reference}")
    found = [run / "candidates" / entry["id"] for run in runs
             if (run / "candidates" / entry["id"] / "result.json").exists()]
    if len(found) > 1:
        raise ValueError(f"Duplicate candidate in run folders: {entry['id']}")
    directory = found[0] if found else results / "candidates" / entry["id"]
    result = read_json(directory / "result.json") if (directory / "result.json").exists() else {"status": "pending"}
    recheck = read_json(directory / "profile-recheck.json") if (directory / "profile-recheck.json").exists() else None
    if recheck and (recheck["input_sha256"] != result.get("input_sha256") or recheck["output_sha256"] != result.get("output_sha256")):
        raise ValueError("Profile recheck candidate hashes differ")
    original_sha = digest(source.read_bytes())
    if result.get("input_sha256", original_sha) != original_sha:
        raise ValueError("Original CIF hash mismatch")
    if result["status"] == "completed" and digest((directory / "refined.cif").read_bytes()) != result["output_sha256"]:
        raise ValueError(f"Refined CIF changed: {directory}")
    key = fingerprint(dict(entry=entry, result=result, recheck=recheck, original_sha=original_sha,
        scorer=digest(Path(__file__).read_bytes()), metric=primary_metric_metadata(),
        versions={n: importlib.metadata.version(n) for n in ("pymatgen", "numpy", "spglib")}))
    cache = results / ".score-cache" / entry["id"] / "score.json"
    if cache.exists():
        saved = read_json(cache)
        if saved["key"] == key:
            return saved["row"]
    try:
        before, before_error = evaluate(source, reference)
    except Exception as exc:
        before, before_error = False, f"{type(exc).__name__}: {exc}"
    after, error = None, ""
    if result["status"] == "completed":
        try:
            after, error = evaluate(directory / "refined.cif", reference)
        except Exception as exc:
            after, error = False, str(exc)
    paired = result.get("paired_profile", {})
    profile_source = "inline" if paired else "unavailable"
    if not paired and recheck and recheck["status"] == "completed":
        paired = recheck["paired_profile"]
        profile_source = "fresh-process-recheck"
    row = {"id": entry["id"], "method": method, "corpus": corpus, "case": case, "slot": int(slot),
           "status": result["status"], "before_exact": before, "after_exact": after,
           "after_with_failure_fallback": after if after is not None else (before if result["status"] != "pending" else None),
           "original_label": entry["before_structure_match"], "wall_seconds": result.get("wall_seconds"),
           "before_rwp": paired.get("before", {}).get("rwp_percent"),
           "after_rwp": paired.get("after", {}).get("rwp_percent"),
           "profile_source": profile_source,
           "error": error or before_error or result.get("error", "")}
    write_json(cache, {"key": key, "row": row})
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--runs", type=Path, nargs="+", help="Read disjoint shards; write reports/cache to --results")
    args = parser.parse_args()
    rows, groups = [], defaultdict(list)
    args.results.mkdir(parents=True, exist_ok=True)
    entries = [(entry, args.results, args.runs or [args.results]) for entry in read_json(args.inputs / "local-index.json")]
    if args.workers > 1:
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            rows = list(pool.map(score_entry, entries, chunksize=8))
    else:
        rows = list(map(score_entry, entries))
    for row in rows:
        groups[(row["method"], row["corpus"])].append(row)
    for entry in read_json(args.inputs / "missing.json"):
        row = dict(id=entry["id"], method=entry["method"], corpus=entry["corpus"], case=entry["case_id"],
                   slot=entry["slot"], status="missing-original", before_exact=False, after_exact=False,
                   after_with_failure_fallback=False, original_label=False, wall_seconds=None,
                   before_rwp=None, after_rwp=None, error="No submitted CIF")
        row["profile_source"] = "unavailable"
        rows.append(row)
        groups[(entry["method"], entry["corpus"])].append(row)
    summary = []
    for (method, corpus), members in groups.items():
        completed = [r for r in members if r["status"] == "completed"]
        paired = [r for r in completed if r["before_rwp"] is not None and r["after_rwp"] is not None]
        cases = defaultdict(list)
        for row in members:
            cases[row["case"]].append(row)
        recovery = {}
        for k in (1, 8, 20):
            before_count, after_count, strict_count, pending = 0, 0, 0, 0
            for candidates in cases.values():
                relevant = [r for r in candidates if r["slot"] <= k]
                before_count += any(r["before_exact"] for r in relevant)
                pending += any(r["status"] == "pending" for r in relevant)
                after_count += any(r["after_with_failure_fallback"] for r in relevant)
                strict_count += any(r["after_exact"] for r in relevant)
            recovery[f"first_{k}"] = {"before": before_count, "after": after_count if not pending else None,
                                      "after_successful_exports_only": strict_count if not pending else None,
                                      "fallback_only_matches": after_count - strict_count if not pending else None,
                                      "case_count": len(cases), "pending_cases": pending}
        summary.append({"method": method, "corpus": corpus, "candidates": len(members), "recovery": recovery,
            "status": dict(Counter(r["status"] for r in members)),
            "before_exact": sum(r["before_exact"] for r in members),
            "after_with_failure_fallback": sum(bool(r["after_with_failure_fallback"]) for r in members),
            "gained": sum(not r["before_exact"] and r["after_exact"] for r in completed),
            "lost": sum(r["before_exact"] and not r["after_exact"] for r in completed),
            "paired_profile_n": len(paired),
            "original_label_disagreements": sum(r["before_exact"] != r["original_label"] for r in members)})
    with (args.results / "scores.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    pilot = read_json(args.inputs / "manifest.json")["pilot"]
    write_json(args.results / "summary.json", {"pilot": pilot,
        "scoring_versions": {name: importlib.metadata.version(name) for name in ("pymatgen", "numpy", "spglib")},
        "metric": primary_metric_metadata(), "groups": summary,
        "warning": (("Pilot rows are implementation checks, not benchmark recovery-rate estimates. " if pilot else "")
                    + "Pending results are never counted as completed failures.")})
    for row in summary:
        print(row)


if __name__ == "__main__":
    main()
