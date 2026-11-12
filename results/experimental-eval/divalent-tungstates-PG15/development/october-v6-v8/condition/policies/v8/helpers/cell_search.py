#!/usr/bin/env python3
"""Rank CIFs in a masked COD resource against an indexed unit cell.

The query is intentionally composition agnostic.  Cell lengths may differ by
small integer axis transforms, as happens when indexing finds a subcell or a
database CIF uses a different conventional setting.  This is a retrieval aid,
not a structure validator: candidates still require extinction, chemistry,
geometry, and full-pattern tests.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import itertools
import json
import math
import re
import sys
from pathlib import Path


LATTICE_SYSTEM_SPACE_GROUPS = {
    "triclinic": range(1, 3),
    "monoclinic": range(3, 16),
    "orthorhombic": range(16, 75),
    "tetragonal": range(75, 143),
    "trigonal": range(143, 168),
    "hexagonal": range(168, 195),
    "cubic": range(195, 231),
}

CELL_TAGS = {
    "a": ("_cell_length_a",),
    "b": ("_cell_length_b",),
    "c": ("_cell_length_c",),
    "alpha": ("_cell_angle_alpha",),
    "beta": ("_cell_angle_beta",),
    "gamma": ("_cell_angle_gamma",),
}

NUMBER = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][+-]?\d+)?")


def parse_number(raw: str) -> float | None:
    raw = raw.strip().strip("'\"")
    match = NUMBER.match(raw)
    if not match:
        return None
    try:
        return float(match.group(0))
    except ValueError:
        return None


def read_cell(path: Path) -> tuple[float, float, float, float, float, float] | None:
    values: dict[str, float] = {}
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            pending: str | None = None
            for raw_line in handle:
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                if pending is not None:
                    value = parse_number(line.split()[0])
                    if value is not None:
                        values[pending] = value
                    pending = None
                    if len(values) == 6:
                        break
                    continue
                lowered = line.lower()
                for key, tags in CELL_TAGS.items():
                    if key in values:
                        continue
                    tag = tags[0]
                    if lowered == tag:
                        pending = key
                        break
                    if lowered.startswith(tag + " ") or lowered.startswith(tag + "\t"):
                        parts = line.split(None, 1)
                        if len(parts) == 2:
                            value = parse_number(parts[1])
                            if value is not None:
                                values[key] = value
                        break
                if len(values) == 6:
                    break
    except OSError:
        return None
    if len(values) != 6:
        return None
    return tuple(values[key] for key in ("a", "b", "c", "alpha", "beta", "gamma"))


def parse_space_groups(raw: str | None, lattice_system: str | None) -> set[int] | None:
    selected: set[int] = set()
    if lattice_system:
        selected.update(LATTICE_SYSTEM_SPACE_GROUPS[lattice_system])
    if raw:
        for token in raw.split(","):
            token = token.strip()
            if not token:
                continue
            if "-" in token:
                start, stop = (int(part) for part in token.split("-", 1))
                selected.update(range(min(start, stop), max(start, stop) + 1))
            else:
                selected.add(int(token))
    return selected or None


def cif_path(root: Path, cod_id: str) -> Path:
    return root / cod_id[0] / cod_id[1:3] / cod_id[3:5] / f"{cod_id}.cif"


def best_metric_match(
    target: tuple[float, float, float, float, float, float],
    candidate: tuple[float, float, float, float, float, float],
    multipliers: tuple[float, ...],
) -> tuple[float, tuple[int, int, int], tuple[float, float, float], float, float]:
    target_lengths = target[:3]
    candidate_lengths = candidate[:3]
    target_angles = sorted(target[3:])
    candidate_angles = sorted(candidate[3:])
    angle_rms = math.sqrt(
        sum((left - right) ** 2 for left, right in zip(target_angles, candidate_angles)) / 3
    )
    best: tuple[float, tuple[int, int, int], tuple[float, float, float], float, float] | None = None
    for permutation in itertools.permutations(range(3)):
        reordered = tuple(target_lengths[index] for index in permutation)
        for transform in itertools.product(multipliers, repeat=3):
            log_ratios = tuple(
                math.log(candidate_lengths[index] / (reordered[index] * transform[index]))
                for index in range(3)
            )
            length_rms = math.sqrt(sum(value * value for value in log_ratios) / 3)
            # Ten degrees of angle mismatch is comparable to about 10% metric mismatch.
            score = math.sqrt(length_rms * length_rms + (angle_rms / 100.0) ** 2)
            item = (score, permutation, transform, length_rms, angle_rms)
            if best is None or item[0] < best[0]:
                best = item
    assert best is not None
    return best


def load_records(index_path: Path, allowed_space_groups: set[int] | None):
    with gzip.open(index_path, "rt", encoding="utf-8") as handle:
        index = json.load(handle)
    seen: set[str] = set()
    for chemical_system, entries in index.items():
        for entry in entries:
            if len(entry) < 3:
                continue
            formula, cod_id, space_group = entry[:3]
            cod_id = str(cod_id)
            try:
                space_group = int(space_group)
            except (TypeError, ValueError):
                continue
            if cod_id in seen or (allowed_space_groups and space_group not in allowed_space_groups):
                continue
            seen.add(cod_id)
            yield chemical_system, str(formula), cod_id, space_group


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", required=True, type=Path, help="masked index.json.gz")
    parser.add_argument("--cif-root", required=True, type=Path, help="masked CIF directory")
    parser.add_argument(
        "--cell",
        required=True,
        type=float,
        nargs=6,
        metavar=("A", "B", "C", "ALPHA", "BETA", "GAMMA"),
    )
    parser.add_argument("--space-groups", help="comma-separated numbers or ranges")
    parser.add_argument("--lattice-system", choices=sorted(LATTICE_SYSTEM_SPACE_GROUPS))
    parser.add_argument(
        "--multipliers",
        default="0.5,1,2,3",
        help="candidate/target axis transforms to test (default: 0.5,1,2,3)",
    )
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--max-score", type=float, default=0.35)
    parser.add_argument("--output", type=Path, help="optional CSV output")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    multipliers = tuple(float(value) for value in args.multipliers.split(",") if value.strip())
    if not multipliers or any(value <= 0 for value in multipliers):
        raise SystemExit("--multipliers must contain positive numbers")
    allowed = parse_space_groups(args.space_groups, args.lattice_system)
    target = tuple(args.cell)
    rows = []
    missing = 0
    parsed = 0
    for chemical_system, formula, cod_id, space_group in load_records(args.index, allowed):
        path = cif_path(args.cif_root, cod_id)
        cell = read_cell(path)
        if cell is None:
            missing += 1
            continue
        parsed += 1
        score, permutation, transform, length_rms, angle_rms = best_metric_match(
            target, cell, multipliers
        )
        if score > args.max_score:
            continue
        rows.append(
            {
                "score": score,
                "length_rms_log": length_rms,
                "angle_rms_deg": angle_rms,
                "cod_id": cod_id,
                "formula": formula,
                "chemical_system": chemical_system,
                "space_group_number": space_group,
                "a": cell[0],
                "b": cell[1],
                "c": cell[2],
                "alpha": cell[3],
                "beta": cell[4],
                "gamma": cell[5],
                "target_axis_order": "".join("abc"[index] for index in permutation),
                "axis_multipliers": ",".join(f"{value:g}" for value in transform),
                "cif_path": str(path),
            }
        )
    rows.sort(key=lambda row: (row["score"], row["cod_id"]))
    rows = rows[: max(0, args.limit)]
    fieldnames = list(rows[0]) if rows else [
        "score",
        "length_rms_log",
        "angle_rms_deg",
        "cod_id",
        "formula",
        "chemical_system",
        "space_group_number",
        "a",
        "b",
        "c",
        "alpha",
        "beta",
        "gamma",
        "target_axis_order",
        "axis_multipliers",
        "cif_path",
    ]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8", newline="") as handle:
            file_writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
            file_writer.writeheader()
            file_writer.writerows(rows)
    print(f"# parsed={parsed} missing_or_unreadable={missing} returned={len(rows)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
