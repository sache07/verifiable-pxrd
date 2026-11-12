#!/usr/bin/env python3
"""Test whether physically positive grouped isotropic ADPs are determined."""

from collections import defaultdict
from pathlib import Path

from GSASII import GSASIIscriptable as G2sc


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "interaction_CuO_texture_010.gpx"
OUTPUT = ROOT / "term_grouped_uiso.gpx"
INITIAL = {"Cu": 0.006, "W": 0.004, "O": 0.008}


def main() -> None:
    project = G2sc.G2Project(str(BASE), newgpx=str(OUTPUT))
    grouped = defaultdict(list)
    for phase in project.phases():
        for atom in phase.atoms():
            atom.uiso = INITIAL[atom.element]
            atom.refinement_flags = "U"
            grouped[atom.element].append(
                project.make_var_obj(
                    phase=phase, varname="AUiso", atomId=atom, reloadIdx=False
                )
            )
    project.save()
    for variables in grouped.values():
        project.add_EquivConstr(variables, reloadIdx=True)
    project.set_Controls("cycles", 16)
    project.refine(makeBack=False)
    project.save()
    replay = G2sc.G2Project(str(OUTPUT))
    replay.set_Controls("cycles", 16)
    replay.refine(makeBack=False)
    replay.save()
    hist = replay.histogram(0)
    print("wR", hist.get_wR(), "mass", hist.ComputeMassFracs())
    for phase in replay.phases():
        print(
            phase.name,
            [(atom.label, atom.element, atom.uiso, atom.refinement_flags) for atom in phase.atoms()],
        )


if __name__ == "__main__":
    main()
