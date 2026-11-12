#!/usr/bin/env python3
"""Advisory physical-integrity audit for candidate CIF files.

This intentionally reports suspicious geometry for scientific review rather
than declaring every unusual contact invalid. Short O--O bonds, for example,
can be real in peroxide-bearing compounds.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from pymatgen.core import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer


def site_species(site) -> list[dict[str, float]]:
    return [
        {"element": str(specie), "occupancy": float(occupancy)}
        for specie, occupancy in site.species.items()
    ]


def element_symbols(site) -> set[str]:
    return {getattr(specie, "element", specie).symbol for specie in site.species}


def audit(path: Path) -> dict:
    structure = Structure.from_file(path)
    occupancy_flags = []
    for index, site in enumerate(structure):
        total = float(sum(site.species.values()))
        if total <= 0.0 or total > 1.0001:
            occupancy_flags.append(
                {
                    "site": index,
                    "total_occupancy": total,
                    "species": site_species(site),
                }
            )

    centers, neighbors, images, distances = structure.get_neighbor_list(3.0)
    unique = {}
    for center, neighbor, image, distance in zip(
        centers, neighbors, images, distances
    ):
        image_tuple = tuple(int(value) for value in image)
        reverse = tuple(-value for value in image_tuple)
        key = min(
            (int(center), int(neighbor), image_tuple),
            (int(neighbor), int(center), reverse),
        )
        unique[key] = min(float(distance), unique.get(key, math.inf))

    contacts = []
    review_flags = []
    for (first, second, image), distance in sorted(
        unique.items(), key=lambda item: item[1]
    ):
        if first == second and image == (0, 0, 0):
            continue
        symbols_first = element_symbols(structure[first])
        symbols_second = element_symbols(structure[second])
        entry = {
            "sites": [first, second],
            "image": list(image),
            "distance_A": distance,
            "species": [site_species(structure[first]), site_species(structure[second])],
        }
        if len(contacts) < 24:
            contacts.append(entry)

        reason = None
        if distance < 0.5:
            reason = "near_duplicate_periodic_sites"
        elif symbols_first == {"O"} and symbols_second == {"O"} and distance < 1.8:
            reason = "unusually_short_O_O_review_peroxide_or_model_error"
        if reason:
            review_flags.append({**entry, "reason": reason})

    try:
        symmetry = SpacegroupAnalyzer(
            structure, symprec=0.01, angle_tolerance=5.0
        )
        symmetry_summary = {
            "symbol": symmetry.get_space_group_symbol(),
            "number": int(symmetry.get_space_group_number()),
        }
    except Exception as error:
        symmetry_summary = {"error": str(error)}
        review_flags.append({"reason": "symmetry_analysis_failed", "error": str(error)})

    return {
        "path": str(path),
        "formula": structure.composition.formula,
        "reduced_formula": structure.composition.reduced_formula,
        "sites": len(structure),
        "volume_A3": float(structure.volume),
        "density_g_cm3": float(structure.density),
        "symmetry": symmetry_summary,
        "occupancy_flags": occupancy_flags,
        "review_flags": review_flags,
        "closest_contacts": contacts,
        "status": "needs_review" if occupancy_flags or review_flags else "no_screen_flags",
        "scope": (
            "Necessary parsing/occupancy/geometry screen only; scientific identity, "
            "bonding, stability, and fit support still require review."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cif", nargs="+", type=Path)
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()
    results = []
    for path in args.cif:
        try:
            results.append(audit(path.resolve()))
        except Exception as error:
            results.append(
                {
                    "path": str(path.resolve()),
                    "status": "parse_error",
                    "error": str(error),
                }
            )
    indent = None if args.compact else 2
    print(json.dumps(results, indent=indent))


if __name__ == "__main__":
    main()
