# Prospective cycle-3 panel decision

Recorded after the complete fixed v6 comparison and before freezing or solving
b004. P0 remains the incumbent.

## Six active cases

| Case | Role in cycle 3 |
|---|---|
| b001-c03 | Ordinary complex four-phase no-harm control. P0 recovers 3/3, v5 also recovers 3/3, but v6 regresses to 0/3. It tests terminal sequencing and whether the five-pass local fix preserves an already soluble case. |
| b001-c06 | Tier-1 missing 15.5 wt% R-3 secondary. Several packages find the Mn3TeO6-derived route but recovery remains inconsistent; this tests focused formula/topology adjudication and equal-depth adaptation. |
| b002-c01 | Tier-2 missing major ZnWO4. Full inventory is usually found, but physical parent basins and calibration/profile boundaries produce large variance; this tests equal-depth parent starts and nuisance rollback. |
| b002-c02 | Tier-2 missing 20 wt% R-3 secondary. v6 selects R-3 0/3; this is the hard focused cross-chemistry retrieval case. |
| b003-c01 | Full-reference R-3 control. Exact physical inventory is reproducible but no package has recovered it consistently, isolating accepted-model completion from missing-reference search. |
| b004-c01 | New full-reference Ba3W2O9 + 5 wt% BaCO3 + WO3 transfer case. It tests unfamiliar cation-rich stoichiometry, weak retained-source persistence and heavy-atom refinement in new chemistry. |

## Set-aside cases

b001-c02 becomes an occasional regression control. Across v4, v5 and v6 it
stays near means 76.4/77.3/77.0 with exactly one recovery per version, so the
cycle-2 interventions do not move reliability closer to the floor. b004
transfers the concrete retained-carbonate mechanism to a new product and
cation rather than spending another active slot on the learned realization.

b001-c05 remains an occasional regression control after v3 recovered its
physical full inventory 3/3. b001-c01 is already at the floor and b001-c04 is
consistently recovered. Optional b005 is retained prospectively for a later
cycle; adding it now would exceed six cases and dilute the focused unresolved
mechanisms.

## Sequence

After the predeclared five-pass diagnostic finishes, freeze b004 with
`--kind transfer --incumbent P0` and run three P0 transfer solves. This
baseline-only prospective comparison opens cycle 3. Only then freeze v7 and
record its numeric six-case predictions before dispatching three solves on
each case.
