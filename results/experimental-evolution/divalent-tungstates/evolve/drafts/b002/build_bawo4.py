#!/usr/bin/env python3
"""Build an ordered BaWO4 scheelite model from documented COD parents."""

from pathlib import Path

from pymatgen.core import Lattice, Structure
from pymatgen.io.cif import CifWriter
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer


PARENT = Path(
    "<HOME>/.local/share/characterizagent/backends/dara/"
    "cod-filtered-2024/cif/1/54/60/1546036.cif"
)
OUTPUT = Path(__file__).with_name("bawo4-ordered-analogue.cif")


def main() -> None:
    parent = Structure.from_file(PARENT, primitive=False)
    model = parent.copy()
    model.replace_species({"Sr": "Ba"})
    model = Structure(
        Lattice.tetragonal(5.614, 12.719),
        model.species,
        model.frac_coords,
        coords_are_cartesian=False,
        site_properties=model.site_properties,
    )
    analyzer = SpacegroupAnalyzer(model, symprec=1e-3, angle_tolerance=1.0)
    assert model.composition.reduced_formula == "BaWO4"
    assert analyzer.get_space_group_number() == 88
    assert model.is_ordered
    distances = model.distance_matrix
    shortest = min(
        distances[i, j]
        for i in range(len(model))
        for j in range(i + 1, len(model))
        if distances[i, j] > 1e-8
    )
    assert shortest > 1.6
    CifWriter(model, symprec=1e-3, refine_struct=True).write_file(OUTPUT)
    print(
        {
            "output": str(OUTPUT),
            "formula": model.composition.reduced_formula,
            "space_group": analyzer.get_space_group_symbol(),
            "space_group_number": analyzer.get_space_group_number(),
            "shortest_distance_A": shortest,
            "density_g_cm3": model.density,
        }
    )


if __name__ == "__main__":
    main()
