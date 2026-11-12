#!/usr/bin/env python3
"""Rank visible COD records with the same reduced stoichiometric pattern."""

from __future__ import annotations

import argparse
import gzip
import json
import math
from pathlib import Path
import warnings

from pymatgen.core import Composition, Element, Structure

warnings.filterwarnings("ignore", category=UserWarning)


def reduced_amounts(formula: str) -> dict[str, float]:
    composition = Composition(formula).reduced_composition
    if any(not isinstance(element, Element) for element in composition):
        raise ValueError("formula contains a non-element placeholder")
    raw = {str(element): float(amount) for element, amount in composition.items()}
    scale = min(raw.values())
    return {element: round(amount / scale, 5) for element, amount in raw.items()}


def signature(amounts: dict[str, float]) -> tuple[float, ...]:
    values = sorted(amounts.values())
    scale = min(values)
    return tuple(round(value / scale, 5) for value in values)


def element_distance(left: str, right: str) -> float:
    if left == right:
        return 0.0
    a, b = Element(left), Element(right)
    group_a = a.group if a.group is not None else 9
    group_b = b.group if b.group is not None else 9
    row_a = a.row if a.row is not None else 4
    row_b = b.row if b.row is not None else 4
    return abs(group_a - group_b) + 0.75 * abs(row_a - row_b) + 1.0


def substitution_cost(target: dict[str, float], candidate: dict[str, float]) -> float:
    by_amount_target: dict[float, list[str]] = {}
    by_amount_candidate: dict[float, list[str]] = {}
    for element, amount in target.items():
        by_amount_target.setdefault(round(amount, 5), []).append(element)
    for element, amount in candidate.items():
        by_amount_candidate.setdefault(round(amount, 5), []).append(element)

    cost = 0.0
    for amount, original_target_elements in by_amount_target.items():
        target_elements = list(original_target_elements)
        remaining = list(by_amount_candidate[amount])
        for element in list(target_elements):
            if element in remaining:
                remaining.remove(element)
                target_elements.remove(element)
        for element in target_elements:
            partner = min(remaining, key=lambda x: element_distance(element, x))
            cost += amount * element_distance(element, partner)
            remaining.remove(partner)
    return cost / sum(target.values())


def cif_path(root: Path | None, cod_id: str) -> Path | None:
    if root is None:
        return None
    return root / cod_id[0] / cod_id[1:3] / cod_id[3:5] / f"{cod_id}.cif"


def cell_mismatch(path: Path | None, target_cell: list[float] | None) -> float | None:
    if path is None or target_cell is None or not path.is_file():
        return None
    try:
        structure = Structure.from_file(path)
    except Exception:
        return None
    observed = list(structure.lattice.abc) + list(structure.lattice.angles)
    length_error = sum(abs(math.log(observed[i] / target_cell[i])) for i in range(3)) / 3
    angle_error = sum(abs(observed[i] - target_cell[i]) / 90.0 for i in range(3, 6)) / 3
    return 100.0 * (length_error + 0.25 * angle_error)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("formula")
    parser.add_argument("index", type=Path)
    parser.add_argument("--cif-root", type=Path)
    parser.add_argument("--space-group", type=int)
    parser.add_argument("--cell", type=float, nargs=6)
    parser.add_argument("--exclude", nargs="*", default=[])
    parser.add_argument("--exclude-exact-composition", action="store_true")
    parser.add_argument("--limit", type=int, default=40)
    args = parser.parse_args()

    target = reduced_amounts(args.formula)
    target_signature = signature(target)
    with gzip.open(args.index, "rt") as handle:
        database = json.load(handle)

    rows = []
    for system, records in database.items():
        for formula, cod_id, space_group, quality in records:
            if str(cod_id) in args.exclude:
                continue
            try:
                amounts = reduced_amounts(formula)
            except Exception:
                continue
            if signature(amounts) != target_signature:
                continue
            if args.exclude_exact_composition and amounts == target:
                continue
            path = cif_path(args.cif_root, str(cod_id))
            mismatch = cell_mismatch(path, args.cell)
            rows.append(
                {
                    "formula": formula,
                    "cod_id": str(cod_id),
                    "space_group": space_group,
                    "system": system,
                    "substitution_cost": round(substitution_cost(dict(target), amounts), 6),
                    "space_group_mismatch": int(
                        args.space_group is not None and space_group != args.space_group
                    ),
                    "cell_mismatch_percent": None if mismatch is None else round(mismatch, 4),
                    "quality": quality,
                    "cif": None if path is None else str(path),
                }
            )

    rows.sort(
        key=lambda row: (
            row["space_group_mismatch"],
            row["substitution_cost"],
            float("inf") if row["cell_mismatch_percent"] is None else row["cell_mismatch_percent"],
            float("inf") if row["quality"] is None else row["quality"],
            row["cod_id"],
        )
    )
    print(json.dumps(rows[: args.limit], indent=2))


if __name__ == "__main__":
    main()
