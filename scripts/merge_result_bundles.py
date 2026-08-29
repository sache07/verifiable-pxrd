#!/usr/bin/env python3
"""Merge disjoint normalized result bundles without rewriting their evidence."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

from verifiable_pxrd.util import sha256_file, write_json


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", action="append", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--id", required=True)
    parser.add_argument("--panel", required=True)
    args = parser.parse_args()

    sources = [path.resolve() for path in args.source]
    destination = args.destination.resolve()
    if destination.exists():
        raise RuntimeError(f"refusing to overwrite {destination}")
    destination.mkdir(parents=True)

    cases: list[dict[str, Any]] = []
    seen: set[str] = set()
    source_records: list[dict[str, Any]] = []
    for source in sources:
        bundle_path = source / "bundle.json"
        bundle = load(bundle_path)
        source_id = str(bundle["result_id"])
        source_records.append(
            {
                "result_id": source_id,
                "bundle_sha256": sha256_file(bundle_path),
                "case_count": int(bundle["case_count"]),
            }
        )
        metadata = source / "source-metadata"
        if metadata.is_dir():
            shutil.copytree(metadata, destination / "sources" / source_id)
        shutil.copy2(bundle_path, destination / "sources" / source_id / "bundle.json")
        for record in bundle["cases"]:
            case_id = str(record["case_id"])
            if case_id in seen:
                raise RuntimeError(f"duplicate case across source bundles: {case_id}")
            seen.add(case_id)
            shutil.copytree(source / "attempts" / case_id, destination / "attempts" / case_id)
            cases.append(record)

    cases.sort(key=lambda item: str(item["case_id"]))
    completed = [item for item in cases if item.get("status") == "archived"]
    selected = [item for item in completed if bool(item.get("selected_exact"))]
    candidates = [item for item in completed if bool(item.get("candidates_exact"))]
    write_json(
        destination / "bundle.json",
        {
            "schema_version": "1",
            "result_id": args.id,
            "panel": args.panel,
            "source_bundles": source_records,
            "traces_included": all(
                bool(load(path / "bundle.json")["traces_included"]) for path in sources
            ),
            "case_count": len(cases),
            "completed_count": len(completed),
            "selected_exact_count": len(selected),
            "selected_exact_rate_completed": len(selected) / len(completed) if completed else None,
            "selected_exact_case_ids": [str(item["case_id"]) for item in selected],
            "candidates_exact_count": len(candidates),
            "candidates_exact_case_ids": [str(item["case_id"]) for item in candidates],
            "cases": cases,
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
