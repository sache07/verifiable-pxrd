#!/usr/bin/env python3
"""Rewrite one CIF as a symmetry-explicit P1 CIF for backend portability."""

from __future__ import annotations

import argparse
from pathlib import Path

from pymatgen.core import Structure
from pymatgen.io.cif import CifWriter


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    structure = Structure.from_file(args.source)
    args.destination.parent.mkdir(parents=True, exist_ok=True)
    CifWriter(structure, symprec=None).write_file(args.destination)


if __name__ == "__main__":
    main()
