#!/usr/bin/env python3
"""Compare returned v6 ZnWO4 structures after equivalent-cell alignment."""

from __future__ import annotations

import json
from pathlib import Path

from pymatgen.analysis.structure_matcher import StructureMatcher
from pymatgen.core import Structure


EVIDENCE = Path(__file__).resolve().parents[2] / "evidence" / "attempts"
FILES = {
    "recovered_rep1": EVIDENCE
    / "b002-v6-efdf82b5144b/workspace/phase_1_ZnWO4.cif",
    "failed_rep2": EVIDENCE / "b002-v6-4231c2299c73/workspace/ZnWO4.cif",
    "failed_rep3": EVIDENCE / "b002-v6-57d5c04ba22f/workspace/phase_ZnWO4.cif",
}


def main() -> None:
    reference = Structure.from_file(FILES["recovered_rep1"], primitive=False)
    matcher = StructureMatcher(
        ltol=0.05,
        stol=1.0,
        angle_tol=2.0,
        primitive_cell=False,
        scale=False,
        attempt_supercell=False,
    )
    result = {"reference": str(FILES["recovered_rep1"]), "comparisons": {}}
    for label, path in FILES.items():
        candidate = Structure.from_file(path, primitive=False)
        aligned = matcher.get_s2_like_s1(reference, candidate)
        if aligned is None:
            result["comparisons"][label] = {"path": str(path), "aligned": False}
            continue
        rows = []
        for ref_index, (ref_site, other_site) in enumerate(zip(reference, aligned)):
            if ref_site.species != other_site.species:
                raise RuntimeError(
                    f"alignment species mismatch at {ref_index}: "
                    f"{ref_site.species} != {other_site.species}"
                )
            distance = float(
                aligned.lattice.get_distance_and_image(
                    other_site.frac_coords, ref_site.frac_coords
                )[0]
            )
            rows.append(
                {
                    "species": ref_site.species_string,
                    "reference_index": ref_index,
                    "distance_A": distance,
                }
            )
        result["comparisons"][label] = {
            "path": str(path),
            "aligned": True,
            "max_distance_A": max(row["distance_A"] for row in rows),
            "mean_O_distance_A": sum(
                row["distance_A"] for row in rows if row["species"] == "O"
            )
            / sum(row["species"] == "O" for row in rows),
            "sites": rows,
        }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
