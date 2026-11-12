#!/usr/bin/env python3
"""Enumerate composition-preserving oxide prototype substitutions.

This research prototype searches a frozen COD-style index for structures whose
cation sites can be relabelled to a requested target formula without changing
the normalized site stoichiometry. It ranks chemistry routes only; diffraction
fit, topology, oxidation-state plausibility and geometry still require review.
"""

from __future__ import annotations

import argparse
import gzip
import itertools
import json
import re
import warnings
from pathlib import Path

from pymatgen.core import Composition, Structure
from pymatgen.io.cif import CifWriter


def normalized_oxide(formula: str) -> dict[str, float] | None:
    try:
        amounts = Composition(formula).get_el_amt_dict()
    except Exception:
        return None
    oxygen = float(amounts.get("O", 0.0))
    if oxygen <= 0 or len(amounts) < 2:
        return None
    return {element: float(amount) / oxygen for element, amount in amounts.items()}


def route_mappings(
    source: dict[str, float], target: dict[str, float], tolerance: float, max_source_cations: int
) -> list[dict[str, str]]:
    source_cations = sorted(set(source) - {"O"})
    target_cations = sorted(set(target) - {"O"})
    if not source_cations or len(source_cations) > max_source_cations:
        return []
    mappings: list[dict[str, str]] = []
    for assigned in itertools.product(target_cations, repeat=len(source_cations)):
        if set(assigned) != set(target_cations):
            continue
        mapped = {element: 0.0 for element in target_cations}
        for source_element, target_element in zip(source_cations, assigned):
            mapped[target_element] += source[source_element]
        if all(abs(mapped[element] - target[element]) <= tolerance for element in target_cations):
            mappings.append(dict(zip(source_cations, assigned)))
    return mappings


def cod_path(root: Path, record_id: str) -> Path:
    return root / record_id[0] / record_id[1:3] / record_id[3:5] / f"{record_id}.cif"


def safe_formula(formula: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", formula).strip("_")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target_formula", help="target composition, for example A3BO6")
    parser.add_argument("--index", type=Path, required=True, help="frozen index.json.gz")
    parser.add_argument("--cif-root", type=Path, help="COD-style CIF root; needed with --write-cifs")
    parser.add_argument("--out", type=Path, help="write the JSON result here as well as stdout")
    parser.add_argument("--write-cifs", type=Path, help="construct mapped CIFs for returned routes")
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="RECORD_ID",
        help="exclude a record ID; may be repeated",
    )
    parser.add_argument("--limit", type=int, default=100, help="maximum routes returned (default: 100)")
    parser.add_argument(
        "--stoichiometry-tolerance",
        type=float,
        default=0.015,
        help="absolute cation/O ratio tolerance (default: 0.015)",
    )
    parser.add_argument(
        "--max-source-cations",
        type=int,
        default=3,
        help="maximum distinct parent cations, allowing solid solutions (default: 3)",
    )
    parser.add_argument("--max-sites", type=int, default=160, help="skip larger CIFs when writing")
    args = parser.parse_args()

    target = normalized_oxide(args.target_formula)
    if target is None or len(target) < 3:
        parser.error("target must be an oxide containing at least two cations")
    with gzip.open(args.index, "rt") as handle:
        index = json.load(handle)

    routes: list[dict[str, object]] = []
    seen: set[tuple[str, tuple[tuple[str, str], ...]]] = set()
    for system, records in index.items():
        for record in records:
            formula, raw_id, space_group = record[:3]
            quality = record[3] if len(record) > 3 else None
            if str(raw_id) in set(args.exclude):
                continue
            source = normalized_oxide(formula)
            if source is None:
                continue
            mappings = route_mappings(
                source, target, args.stoichiometry_tolerance, args.max_source_cations
            )
            for mapping in mappings:
                record_id = str(raw_id)
                key = (record_id, tuple(sorted(mapping.items())))
                if key in seen:
                    continue
                seen.add(key)
                changed = sorted(f"{old}->{new}" for old, new in mapping.items() if old != new)
                retained = sorted(element for element in mapping if mapping[element] == element)
                routes.append(
                    {
                        "record_id": record_id,
                        "parent_formula": formula,
                        "chemical_system": system,
                        "space_group": int(space_group),
                        "quality": quality,
                        "mapping": mapping,
                        "substitution_count": len(changed),
                        "substitutions": changed,
                        "retained_target_cations": retained,
                    }
                )

    routes.sort(
        key=lambda row: (
            row["substitution_count"],
            -len(row["retained_target_cations"]),
            len(row["mapping"]),
            row["quality"] is None,
            row["quality"] if isinstance(row["quality"], (int, float)) else 999.0,
            row["record_id"],
        )
    )
    routes = routes[: max(0, args.limit)]

    if args.write_cifs:
        if args.cif_root is None:
            parser.error("--cif-root is required with --write-cifs")
        args.write_cifs.mkdir(parents=True, exist_ok=True)
        for route in routes:
            record_id = str(route["record_id"])
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    structure = Structure.from_file(cod_path(args.cif_root, record_id), primitive=False)
                if len(structure) > args.max_sites:
                    route["construction_status"] = "skipped_max_sites"
                    continue
                structure.remove_oxidation_states()
                structure.replace_species(route["mapping"])
                normalized = normalized_oxide(structure.composition.formula)
                if normalized is None or any(
                    abs(normalized.get(element, 0.0) - amount) > args.stoichiometry_tolerance
                    for element, amount in target.items()
                ):
                    route["construction_status"] = "mapped_structure_stoichiometry_mismatch"
                    continue
                mapping_slug = "_".join(
                    f"{old}-{new}" for old, new in sorted(route["mapping"].items())
                )
                destination = args.write_cifs / (
                    f"{record_id}_{safe_formula(args.target_formula)}_{mapping_slug}.cif"
                )
                CifWriter(structure, symprec=1e-3, significant_figures=10).write_file(destination)
                route["construction_status"] = "written"
                route["cif_path"] = str(destination)
                route["sites"] = len(structure)
            except Exception as exc:
                route["construction_status"] = f"error:{type(exc).__name__}"

    result = {
        "target_formula": args.target_formula,
        "target_normalized_to_oxygen": target,
        "stoichiometry_tolerance": args.stoichiometry_tolerance,
        "route_count": len(routes),
        "warning": (
            "Composition-preserving relabelling is only a candidate generator; "
            "review topology, oxidation states, geometry and powder fit independently."
        ),
        "routes": routes,
    }
    rendered = json.dumps(result, indent=2) + "\n"
    if args.out:
        args.out.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
