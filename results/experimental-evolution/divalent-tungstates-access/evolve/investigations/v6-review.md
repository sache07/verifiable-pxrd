# v6 review: bounded accepted-model polish

## Change and rationale

v4 and v5 both repaired physical same-formula selection on the full-reference
R-3 control, but neither recovered it in any replicate.  Their harder-Zn
failures also repeatedly closed a physical formula inventory and then diverged
in accepted-framework completion.  v4's extra formula/topology coverage was
actively unsuccessful: it selected R-3 only once on tier-1 c06 and never on
tier-2 harder Mn, while consuming attention within wrong formulas.  v6 removes
that intervention.

v6 retains a concise 233-word closure/physical-checkpoint procedure and adds
one optional final-stage executable, `helpers/staged_polish.py`.  It is invoked
only after coherent-family closure and ordinary refinement of a complete
physical model.  It never changes phase identity or count, reads no reference
files or case metadata, and needs no network.  From the submitted checkpoint
it compares all-coordinate, heavy-then-light, and phasewise coordinate orders;
uses fresh scale, reciprocal-cell, and 0.10 A-per-axis coordinate bounds;
restores every atom that reaches a bound; retries only interior sites; and
settles cells/scales/background.  A branch is eligible only after coordinate
and settle convergence below shift/esd 1, with no frozen variables, no
catastrophic contact, no pair-minimum contraction above 0.18 A, and no phase
fraction collapse below one quarter of its checkpoint value.  The original
project is returned unless an eligible branch lowers observed Rwp by at least
0.02 percentage point.  The defaults and audit are written to the adjacent
JSON summary.

## Isolated evidence

Local post-hoc development on two b003 projects showed three-order convergence
and safe Rwp gains of 0.121 and 0.039 point.  Controller test
`ptest-v6-staged-covfix-02` then ran the exact packaged script hash
`c022d6066528ad581e4d7b3f3b2f949f5f789c3c42282e06015bbdde2658bd9c`
on eight saved projects: four exact physical b003 failures, two exact-inventory
harder-Zn failures, and recovered c03/c06 controls.  All eight replayed and
scored, six improved hidden D, none worsened, two returned baseline, and no
physical flags appeared.  Median D fell 2.573 to 2.349.  Improvements occurred
on all four b003 projects (0.061-0.320 D), one harder-Zn project (0.149), and
the recovered c06 control (0.067); the weakest harder-Zn project and recovered
c03 control safely returned baseline.

A prospectively specified cell-first/wider-cell variant did not rescue that
weak transfer basin: 5/5 scored, but the target remained unchanged and c06
lost the narrow helper's gain.  It is excluded.  This negative comparison is
important: v6 ships the smaller mechanism supported across the broader panel,
not the most permissive optimizer tried.

## Limits and rollout interpretation

The diagnostic scores use synthetic truth and do not validate a fresh-solver
policy.  The helper cannot repair a missing phase, wrong topology, bad
same-formula framework, or gross transferred-coordinate basin; the rollout
must therefore be judged on adherence, re-export consistency, variance, and
the fixed aggregate/per-case promotion rule.  Solvers are explicitly told to
run it once near the end and to re-export all CIFs, fractions, `fit.csv`, and
the report from an accepted polished project.  No case IDs, coordinates,
reference structures, hidden fractions, or lookup rules are packaged.
