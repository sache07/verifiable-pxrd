#!/usr/bin/env python3
"""Diagnostic: copy independent-atom coordinates between matching GPX phases."""

from __future__ import annotations

import json
import sys

from GSASII import GSASIIscriptable as G2sc


def select(project, token):
    matches = [phase for phase in project.phases() if token.lower() in phase.name.lower()]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one phase matching {token!r}, found {[p.name for p in matches]}")
    return matches[0]


def signature(phase):
    cx, ct, _cs, _cia = phase.data["General"]["AtomPtrs"]
    return [(row[ct], row[cx + 3], row[cx + 4]) for row in phase.data["Atoms"]]


def main(recipient_path, donor_path, output_path, phase_token):
    G2sc.SetPrintLevel("warn")
    recipient = G2sc.G2Project(gpxfile=recipient_path)
    donor = G2sc.G2Project(gpxfile=donor_path)
    target = select(recipient, phase_token)
    source = select(donor, phase_token)
    if target.data["General"]["SGData"]["SpGrp"] != source.data["General"]["SGData"]["SpGrp"]:
        raise RuntimeError("Space groups differ; coordinate copying would be ambiguous")
    if signature(target) != signature(source):
        raise RuntimeError(
            "Independent atom type/site signatures differ; put both models in the same setting first"
        )
    cx = target.data["General"]["AtomPtrs"][0]
    changes = []
    for target_atom, source_atom in zip(target.data["Atoms"], source.data["Atoms"]):
        before = [float(value) for value in target_atom[cx : cx + 3]]
        after = [float(value) for value in source_atom[cx : cx + 3]]
        target_atom[cx : cx + 3] = after
        changes.append(
            {
                "label": target_atom[0],
                "element": target_atom[1],
                "before": before,
                "after": after,
            }
        )
    recipient.save(output_path)
    print(json.dumps({"phase": target.name, "changes": changes}, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise SystemExit(
            "usage: transplant_phase_coordinates.py RECIPIENT.gpx DONOR.gpx OUTPUT.gpx PHASE_TOKEN"
        )
    main(*sys.argv[1:])
