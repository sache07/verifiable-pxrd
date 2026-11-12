#!/usr/bin/env python3
"""Report broad, necessary CIF geometry and occupancy checks.

This is a source-selection aid, not a certificate of phase stability.  It
deliberately reports partial disorder and close oxygen sites for scientific
review instead of silently accepting or repairing them.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import warnings

from pymatgen.core import Structure
from pymatgen.io.cif import CifFile, str2float
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer


def _species(site) -> str:
    return site.species_string


def _only_oxygen(site) -> bool:
    return {element.symbol for element in site.species.elements} == {"O"}


def audit(path: Path, hard_contact: float, oxygen_review: float) -> dict:
    caught: list[str] = []
    raw_invalid_occupancies = []
    try:
        for block_name, block in CifFile.from_file(path).data.items():
            values = block.data.get("_atom_site_occupancy", [])
            if isinstance(values, str):
                values = [values]
            for index, token in enumerate(values):
                try:
                    value = float(str2float(token))
                except Exception:
                    value = math.nan
                if not math.isfinite(value) or value < 0 or value > 1.0001:
                    raw_invalid_occupancies.append(
                        {
                            "block": block_name,
                            "row": index,
                            "token": str(token),
                        }
                    )
        with warnings.catch_warnings(record=True) as emitted:
            warnings.simplefilter("always")
            structure = Structure.from_file(path)
        caught = [str(item.message) for item in emitted]
    except Exception as exc:  # Keep a multi-file audit useful after one bad CIF.
        return {"path": str(path), "status": "error", "error": str(exc)}

    partial_sites = []
    mixed_sites = []
    invalid_sites = []
    for index, site in enumerate(structure):
        occupancy = float(site.species.num_atoms)
        if occupancy < 0.9999:
            partial_sites.append(
                {"site": index, "species": _species(site), "occupancy": occupancy}
            )
        if occupancy > 1.0001 or occupancy <= 0:
            invalid_sites.append(
                {"site": index, "species": _species(site), "occupancy": occupancy}
            )
        if len(site.species) > 1:
            mixed_sites.append(
                {"site": index, "species": _species(site), "occupancy": occupancy}
            )

    centers, neighbors, images, distances = structure.get_neighbor_list(
        max(hard_contact, oxygen_review)
    )
    hard_contacts = []
    oxygen_contacts = []
    minimum_contact = None
    minimum_oxygen_contact = None
    for i, j, image, distance in zip(centers, neighbors, images, distances):
        i, j, distance = int(i), int(j), float(distance)
        image_key = tuple(int(value) for value in image)
        if i > j or (i == j and image_key <= (0, 0, 0)):
            continue
        minimum_contact = distance if minimum_contact is None else min(minimum_contact, distance)
        first, second = structure[i], structure[j]
        row = {
            "sites": [i, j],
            "image": list(image_key),
            "distance_A": distance,
            "species": [_species(first), _species(second)],
            "occupancies": [
                float(first.species.num_atoms),
                float(second.species.num_atoms),
            ],
        }
        if distance < hard_contact:
            hard_contacts.append(row)
        if _only_oxygen(first) and _only_oxygen(second):
            minimum_oxygen_contact = (
                distance
                if minimum_oxygen_contact is None
                else min(minimum_oxygen_contact, distance)
            )
            if distance < oxygen_review:
                oxygen_contacts.append(row)

    status = "pass"
    if raw_invalid_occupancies or invalid_sites or any(
        min(row["occupancies"]) >= 0.9999 for row in hard_contacts
    ):
        status = "fail"
    elif partial_sites or mixed_sites or hard_contacts or oxygen_contacts:
        status = "review"

    try:
        space_group = SpacegroupAnalyzer(structure, symprec=0.05).get_space_group_symbol()
    except Exception as exc:
        space_group = f"unresolved: {exc}"

    return {
        "path": str(path),
        "status": status,
        "formula": structure.composition.formula,
        "space_group": space_group,
        "sites": len(structure),
        "ordered": structure.is_ordered,
        "raw_invalid_occupancies": raw_invalid_occupancies,
        "partial_sites": partial_sites,
        "mixed_sites": mixed_sites,
        "invalid_sites": invalid_sites,
        "minimum_contact_A": minimum_contact,
        "minimum_oxygen_contact_A": minimum_oxygen_contact,
        "hard_contacts": hard_contacts[:50],
        "oxygen_contacts_for_review": oxygen_contacts[:50],
        "parser_warnings": caught,
        "scope": (
            "Broad necessary geometry/occupancy check only; review flagged disorder "
            "and contacts in chemical context and compare alternate records."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cifs", nargs="+", type=Path)
    parser.add_argument("--hard-contact-A", type=float, default=0.8)
    parser.add_argument("--oxygen-review-A", type=float, default=1.8)
    args = parser.parse_args()
    if args.hard_contact_A <= 0 or args.oxygen_review_A <= 0:
        parser.error("contact distances must be positive")
    rows = [
        audit(path.resolve(), args.hard_contact_A, args.oxygen_review_A)
        for path in args.cifs
    ]
    print(json.dumps(rows, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
