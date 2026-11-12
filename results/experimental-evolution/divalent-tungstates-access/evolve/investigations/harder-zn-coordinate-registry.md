# Harder-Zn accepted-framework basin diagnosis

## Evidence compared

- v4 rep3 `b002-v4-v5-99637c5841ce`: exact physical three-phase
  inventory, score 29.69, D 14.675, Rwp 9.198, ZnWO4 site accuracy 63.7%.
- v3 reps2/3 `b002-v3-3241ab995358` and
  `b002-v3-e9f76a0c7f51`: exact inventories, scores 77.87/80.79,
  D 0.404/0.348, Rwp 3.090/3.035, ZnWO4 site accuracy 93.1/95.6%.
- Procedure tests of narrow polish and cell-first polish on the v4 endpoint.

## Mechanism

The failed and successful ZnWO4 cells are already nearly the same: their
lengths differ by only a few thousandths of an angstrom and beta by about
0.02 degrees.  Heavy-site coordinates are likewise close after accounting for
the equivalent wolframite setting.  The decisive difference is the oxygen
sublattice registry: the failed model's two independent oxygen z coordinates
are about 1.75-1.93 A from the successful basin under the submitted setting,
far outside a safe local 0.10 A polish window.

This agrees with execution history.  The failed run began from MnWO4-like
coordinates, rejected one unconstrained oxygen branch, and later accepted a
different physically plausible local oxygen basin.  The successful v3 runs
explicitly preserved a modern wolframite start or compared CoWO4/NiWO4-derived
physical starts before committing.  Once in the good basin, ordinary
coordinate/profile refinement reached Rwp about 3%.

The isolated interventions separate the alternatives cleanly.  Narrow polish
returns baseline on the failed project.  Expanding/reordering cell refinement
also returns baseline, falsifying cell-coordinate ordering as the cause.
Therefore this endpoint is not a failure of local convergence around the
accepted coordinates; it is a discrete parent/light-sublattice registry choice
made before final polish.

## Reusable route forward

For an accepted transferred topology whose peak positions fit but relative
intensities remain grossly wrong, preserve at least two physically valid
same-topology coordinate starts from distinct compatible parents.  Compare
them only after identical cell, calibration, broadening and texture adaptation,
then run local bounded polish on the winning physical basin.  A generic helper
that sees only the final project cannot safely invent a 1.8 A oxygen-registry
jump; automating blind large coordinate shifts would add substantial
generalization risk.

This is current-cycle diagnostic evidence, not part of frozen v6.  It provides
a specific next-cycle route if v6 fresh runs reproduce the gross basin.

## Direct mechanism check

`direct-v7-zn-registry-01` tests the causal step with explicit oracle
limitations.  Starting from the physical exact-inventory v4 rep3 project, it
replaced only the ZnWO4 independent coordinates with those from a physical
recovered solve of the same frozen measurement; phases, cells and the failed
project's nuisance model were retained.  The unchanged v6 staged-polish helper
then brought all three coordinate orders to Rwp 3.273-3.278% versus 9.198% for
the original basin.  The selected branch converged with maximum shift/esd
0.032, no frozen variables, stable fractions and no geometry violations.

Independent scoring gives 71.46, D 0.582 and Rwp 3.273, compared with the
original endpoint's 29.69, D 14.675 and Rwp 9.198.  The diagnostic is formally
recovered and physically passes.  Because its donor coordinates came from a
successful answer, this establishes the mechanism rather than a valid recovery
algorithm.  A learned procedure must source its starts prospectively from
multiple available physical parents and compare them at equal depth; it must
not copy coordinates from evaluation evidence.

## Fresh v6 qualification

Fresh v6 harder-Zn finishes at one recovery from three exact physical
inventories, but its two failures do not simply reproduce the older 1.8 A
oxygen-registry separation. Symmetry-aligned comparison of their returned
ZnWO4 CIFs with recovered v6 rep1 gives maximum site differences of about
0.02 A for failed rep2 and 0.10 A for failed rep3. The comparison is recorded
by `compare_fresh_znwo4_registries.py`.

Both failures still selected CoMoO4-II after shallow parent comparisons, so
preserving equal-depth starts remains prudent. Their endpoints expose stronger
additional defects, however. Rep2 uses effective zero +0.407 degrees, outside
the supplied +/-0.25-degree range, with zero specimen shift and systematically
misplaced cells. Rep3 pins instrument U to 0, X to 6 and WO3 size to 1.5 um,
and retains extra minor-phase texture. These boundary/correlated nuisance
choices can explain gross profile error even when the principal coordinates
are close.

Thus the direct transplant experiment validates registry as one possible
mechanism, while fresh v6 shows it is not a sufficient diagnosis of every bad
wolframite fit. The reusable route needs both equal-depth parent comparison
before nuisance fitting and strict rollback of calibration/profile terms
outside laboratory ranges or pinned at tested bounds.
