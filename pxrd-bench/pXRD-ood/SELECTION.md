# Selection and novelty protocol

All candidate formulas and structures are checked against the complete frozen
source boundary in `SOURCE.lock.json`. Composition-novel cases have zero reduced-
formula hits and retain a species-erased match to a known parent. Topology-novel
cases use formulas exposed in every learned-model corpus and at least one retrieval
catalog, but have no `StructureMatcher.fit_anonymous` match under the locked
tolerances. Baseline outputs never participate in selection.

The exposure union covers the exact Crystalyze and PXRDGen MP-20 releases, every
tuple in the released deCIFer NOMA archive, the official and released DiffractGPT
JARVIS datasets, DARA's bundled public-COD index, a complete official COD rsync
mirror snapshot dated 2026-07-06 plus every official live-only CIF through
2026-07-19, and a complete Materials Project 2026.04.13 snapshot. DARA's licensed
ICSD corpus and the unpublished AGAPI-XRD server revision remain explicitly
unchecked; the public JARVIS/COD stores reported for AGAPI-XRD are frozen here.

Strict structure absence uses `StructureMatcher` with `ltol=0.20`, `stol=0.30`,
`angle_tol=5`, primitive reduction and scale normalization. Topology novelty uses
`fit_anonymous` over every reference with the same anonymized reduced formula.
Every final audit recomputes formula, strict-structure, and topology certificates
from the frozen SQLite index rather than trusting the copied manifest result.
