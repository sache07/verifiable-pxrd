"""Freeze reference-blind tasks from released baseline bundles, plus local scoring index."""
from __future__ import annotations

import argparse
import csv
import io
from pathlib import Path

from common import PROTOCOL, REPO, digest, fingerprint, read_json, verify_task, write_json


def prepare(output, pilot=False, methods=None):
    from pymatgen.core import Structure

    tasks, index, missing, exclusions = [], [], [], []
    for method, config in PROTOCOL["methods"].items():
        if methods and method not in methods:
            continue
        for corpus, corpus_dir in (("pxrd-100", "pXRD-100"), ("pxrd-ood", "pXRD-ood")):
            bundle = REPO / "results/baselines" / method / corpus / config["variant"]
            target_root = REPO / "baselines" / method / "targets" / corpus
            targets = {c["case_id"]: c for c in read_json(target_root / "manifest.json")["cases"]}
            references = {c["case_id"]: c for c in read_json(REPO / "pxrd-bench" / corpus_dir / "manifest.json")["cases"]}
            rows = list(csv.DictReader(io.StringIO((bundle / "candidates.csv").read_text())))
            if pilot:
                by_case = {}
                for row in rows:
                    if row["candidate_path"] and row["case_id"] not in by_case:
                        by_case[row["case_id"]] = row
                sizes = {}
                for case, row in by_case.items():
                    try:
                        sizes[case] = len(Structure.from_file(bundle / row["candidate_path"]))
                    except Exception:
                        print(f"Pilot excludes unparsable first candidate: {method}/{case}")
                        exclusions.append({"method": method, "case_id": case, "reason": "unparsable first available CIF"})
                ordered = sorted((r for c, r in by_case.items() if c in sizes),
                                 key=lambda r: (sizes[r["case_id"]], r["case_id"]))
                count = PROTOCOL["pilot"]["per_method_per_corpus"]
                rows = [ordered[round(i * (len(ordered) - 1) / (count - 1))] for i in range(count)]
            for row in rows:
                case = row["case_id"]
                slot = int(row["sample_index"]) + 1
                task_id = f"{method}/{corpus}/{case}/{slot:02d}"
                if not row["candidate_path"]:
                    missing.append({"id": task_id, "method": method, "corpus": corpus, "case_id": case, "slot": slot})
                    continue
                candidate = bundle / row["candidate_path"]
                cif = candidate.read_text()
                if digest(cif.encode()) != row["candidate_sha256"]:
                    raise ValueError(f"Candidate drift: {candidate}")
                target = targets[case]
                pattern = target_root / target["pattern_path"]
                text = pattern.read_text()
                if digest(text.encode()) != target["pattern_sha256"]:
                    raise ValueError(f"Observation drift: {pattern}")
                task = {
                    "id": task_id, "method": method, "corpus": corpus, "case_id": case, "slot": slot,
                    "candidate_cif": cif, "candidate_sha256": digest(cif.encode()),
                    "pattern_text": text, "pattern_sha256": digest(text.encode()),
                    "intensity_multiplier": target.get("intensity_max_before_normalization", 1.0) if method == "pxrdgen" else 1.0,
                    "timeout_seconds": config["timeout_seconds"], "wavelength": 1.54184,
                    "protocol_sha256": fingerprint(PROTOCOL), "self_target": False,
                }
                verify_task(task)
                tasks.append(task)
                ref = REPO / "pxrd-bench" / corpus_dir / references[case]["path"]
                index.append({"id": task_id, "candidate_path": str(candidate.relative_to(REPO)),
                              "reference_path": str(ref.relative_to(REPO)),
                              "reference_sha256": digest(ref.read_bytes()),
                              "before_structure_match": row["structure_match"].lower() == "true"})
    # Worker requests contain no reference paths, formulas derived from truth, or labels.
    write_json(output / "tasks.json", tasks)
    write_json(output / "local-index.json", index)
    write_json(output / "missing.json", missing)
    write_json(output / "manifest.json", {"protocol": PROTOCOL, "pilot": pilot,
               "tasks_sha256": fingerprint(tasks), "count": len(tasks), "missing": len(missing), "pilot_exclusions": exclusions})
    print(f"Prepared {len(tasks)} candidates; {len(missing)} missing originals; pilot={pilot}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--pilot", action="store_true")
    parser.add_argument("--methods", nargs="+", choices=list(PROTOCOL["methods"]))
    args = parser.parse_args()
    prepare(args.output, args.pilot, args.methods)
