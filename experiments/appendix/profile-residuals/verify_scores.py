"""Verify reconstructed scorers against frozen scores on one fixed case per condition."""
import argparse
import csv
import hashlib
import importlib.metadata
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASELINES = {
    "crystalyze": ("crystalyze", "element-set-k8"),
    "diffractgpt": ("diffractgpt", "reduced-composition-greedy-k1"),
    "decifer-known-z": ("decifer", "known-conventional-z-k8"),
    "pxrdgen-known-z": ("pxrdgen", "known-primitive-z-k8"),
    "ab-pxrd-solver": ("ab-pxrd-solver", "reduced-composition-k1"),
    "realpxrd-solver-known-z": ("realpxrd-solver", "known-primitive-z-k20")}
AGENTS = {"gpt-5-6-sol-high": "llm/full-200-api-sol-high-r1",
          "matsci-codex": "matsci-codex/full-200-r1", "pxrd-codex": "pxrd-codex/full-200-api-sol-high-r1",
          "adapted-codex": "adapted-codex/full-200-chatgpt-sol-high-r1"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gsas", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--case", default="pxrd100-rep-001")
    parser.add_argument("--native", action="store_true")
    parser.add_argument("--report", type=Path, help="Also write compact verification metadata here (no CIFs or profiles)")
    parser.add_argument("--diffractgpt-archive", type=Path, help="Private original run folder; CIFs remain outside the public bundle")
    args = parser.parse_args()
    data = ROOT / "results/appendix/profile-residuals/as-submitted"
    shared = list(csv.DictReader((data / "fixedparams-v1-rwp-candidates.csv").open()))
    native = list(csv.DictReader((data / "native-rwp-candidates.csv").open()))
    corpus = "pXRD-100" if args.case.startswith("pxrd100") else "pXRD-ood"
    references = json.loads((ROOT / "pxrd-bench" / corpus / "manifest.json").read_text())["cases"]
    reference = ROOT / "pxrd-bench" / corpus / next(r["path"] for r in references if r["case_id"] == args.case)
    results = []
    for slug in (*BASELINES, *AGENTS):
        row = next((r for r in shared if r["condition_slug"] == slug and r["case_id"] == args.case
                    and r["candidate_index"] == "0"), None)
        if not row or not row["rwp_percent"]:
            results.append({"condition": slug, "status": "no archived score for fixed check case"})
            continue
        if slug in BASELINES:
            method, variant = BASELINES[slug]
            bundle = ROOT / "results/baselines" / method / corpus.lower() / variant
            identities = list(csv.DictReader((bundle / "candidates.csv").open()))
            identity = next(r for r in identities if r["case_id"] == args.case and r["sample_index"] == "0")
            if not identity["candidate_path"]:
                if method == "diffractgpt" and args.diffractgpt_archive:
                    candidate = args.diffractgpt_archive / identity["candidate_member"]
                else:
                    results.append({"condition": slug, "status": "not checked: candidate CIF not published", "candidate_sha256": identity["candidate_sha256"]})
                    continue
            else:
                candidate = bundle / identity["candidate_path"]
            if hashlib.sha256(candidate.read_bytes()).hexdigest() != identity["candidate_sha256"]:
                raise ValueError(f"Candidate hash mismatch: {candidate}")
        else:
            candidate = ROOT / "results/agent-adaptation" / AGENTS[slug] / "attempts" / args.case / "submission/selected.cif"
        out = args.output / slug
        expected = float(row["rwp_percent"])
        command = [sys.executable, str(Path(__file__).with_name("score_pair.py")), str(reference), str(candidate)]
        if args.native and slug in BASELINES:
            if method == "realpxrd-solver":
                continue
            match = next(r for r in native if r["framework_slug"] == slug and r["case_id"] == args.case and r["sample_index"] == "0")
            expected = float(match["rwp_percent"])
            command = [sys.executable, str(Path(__file__).with_name("score_native.py")), method, corpus.lower(), args.case, str(candidate)]
        command += ["--gsas", str(args.gsas), "--output", str(out)]
        process = subprocess.run(command, capture_output=True, text=True, timeout=120)
        out.mkdir(parents=True, exist_ok=True)
        (out / "verification.log").write_text(process.stdout + process.stderr)
        observed = json.loads((out / "score.json").read_text())["rwp_percent"] if process.returncode == 0 else None
        locator = str(candidate.relative_to(ROOT)) if candidate.is_relative_to(ROOT) else "private-archive/" + identity["candidate_member"]
        result = {"condition": slug, "case_id": args.case, "candidate": locator,
                  "expected": expected, "observed": observed,
                  "absolute_error": abs(observed - expected) if observed is not None else None,
                  "status": "verified" if observed is not None and abs(observed - expected) < 1e-5 else "failed",
                  "candidate_sha256": hashlib.sha256(candidate.read_bytes()).hexdigest() if candidate.exists() else None}
        results.append(result)
        print(result, flush=True)
    args.output.mkdir(parents=True, exist_ok=True)
    metadata = {"metric": "native" if args.native else "shared-fixedparams-v1", "case_id": args.case,
                "reference_sha256": hashlib.sha256(reference.read_bytes()).hexdigest(), "checks": results,
                "packages": {name: importlib.metadata.version(name) for name in
                             ("numpy", "scipy", "pymatgen", "spglib", "torch", "jarvis-tools")},
                "source_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob("*.py")},
                "gsas_commit": subprocess.check_output(["git", "-C", str(args.gsas.parent), "rev-parse", "HEAD"], text=True).strip()}
    serialized = json.dumps(metadata, indent=2) + "\n"
    (args.output / "verification.json").write_text(serialized)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(serialized)
    return int(any(r["status"] == "failed" for r in results))


if __name__ == "__main__":
    raise SystemExit(main())
