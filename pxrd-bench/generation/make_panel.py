#!/usr/bin/env python3
"""Create a deterministic runnable panel from the locked pXRD corpora."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def records(benchmark_root: Path) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for directory in ("pXRD-100", "pXRD-ood"):
        corpus = benchmark_root / directory
        source = load_json(corpus / "manifest.json")
        patterns = load_json(corpus / "targets/fixedparams-v1/manifest.json")
        pattern_by_id = {str(item["case_id"]): item for item in patterns["cases"]}
        for item in source["cases"]:
            case_id = str(item["case_id"])
            pattern = pattern_by_id[case_id]
            result.append(
                {
                    "case_id": case_id,
                    "formula": item["formula"],
                    "dataset": source["dataset_id"],
                    "panel": item["panel"],
                    "stream": item.get("stream"),
                    "crystal_system": item.get("crystal_system"),
                    "primitive_site_count": item.get("primitive_site_count"),
                    "reference_path": f"{directory}/{item['path']}",
                    "reference_sha256": item["sha256"],
                    "pattern_path": (
                        f"{directory}/targets/fixedparams-v1/{pattern['pattern_path']}"
                    ),
                    "pattern_sha256": pattern["pattern_sha256"],
                    "wavelength": 1.5406,
                    "radiation": "Cu Kalpha1",
                }
            )
    return result


def sample(items: list[dict[str, Any]], size: int | None, seed: int) -> list[dict[str, Any]]:
    if size is None or size == len(items):
        return items
    if size < 1 or size > len(items):
        raise ValueError(f"size must be between 1 and {len(items)}")
    randomizer = random.Random(seed)
    chosen = randomizer.sample(items, size)
    return sorted(chosen, key=lambda item: str(item["case_id"]))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark-root", type=Path, default=Path(__file__).parents[1])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--size", type=int)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    benchmark_root = args.benchmark_root.resolve()
    output = args.output.resolve()
    selected = sample(records(benchmark_root), args.size, args.seed)
    relative_root = Path(__import__("os").path.relpath(benchmark_root, output.parent)).as_posix()
    payload = {
        "schema_version": "1",
        "panel_id": output.stem,
        "description": "Deterministic panel sampled from locked pXRD-100 and pXRD-ood.",
        "path_root": relative_root,
        "seed": args.seed,
        "case_count": len(selected),
        "cases": selected,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
