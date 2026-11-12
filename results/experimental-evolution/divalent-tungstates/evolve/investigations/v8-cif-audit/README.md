# CIF health-report prototype

## Hypothesis

The v7 source regressions are execution failures, not an absence of prose: the
guidance asks for disorder/geometry screening, but three completed solves still
retain a known short-contact WO3 record and the Ba solve additionally retains a
split, partially occupied BaWO4 record.  A small report may make this gate less
attention-dependent without encoding a case lookup or repairing a structure.

`cif_health.py` parses one or more arbitrary CIFs and reports formula, detected
space group, partial/invalid occupancies, contacts below 0.8 A, and O--O
contacts below a broad 1.8 A oxide-review distance.  It never changes a CIF and
labels the check as necessary rather than sufficient; real disorder or peroxide
chemistry can be reviewed rather than automatically rejected.

## Retrospective check

- v7 b002-c02 BaWO4: `review`, 32 partial sites and 16 O--O contacts at
  1.170 A; its WO3: `review`, four O--O contacts at 1.577 A.
- v7 b001-c03 and c05 WO3: each `review`, four O--O contacts at about
  1.577 A.  Their other submitted phases pass.
- v7 b002-c01 physical MgWO4 and WO3 both pass.
- All 12 final CIFs from the three successful v6 b002-c02 transfer solves pass.
- All six final CIFs from the v6 b001-c03 and c05 development solves pass.

Thus the prototype separates every presently observed v7 source regression
from 18 retained physical v6 structures in the directly relevant cases.  This
is retrospective mechanism evidence only; a frozen prospective screen is
needed to assess whether solvers invoke it and choose better sources.
