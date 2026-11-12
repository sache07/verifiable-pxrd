# Prospective v6 predictions

Recorded after `freeze-v6` was accepted and before any v6 solve was queued.
The package is frozen at prompt SHA-256 `799a091d...` and helper SHA-256
`c022d606...`.

## Mechanism predictions

- Solvers that reach a complete physical inventory should run the helper once
  near the end, inspect its summary, and keep either its safe selected branch
  or the original baseline.  At least half of exact-inventory runs should
  visibly execute it; accepted polished projects must have consistent
  re-exported CIFs, fractions and `fit.csv`.
- No helper-using submission should acquire a physical flag, lose a phase by
  scale collapse, or retain frozen coordinate/cell variables.  Already strong
  c03/c06 endpoints should return baseline or improve, not regress through
  automatic branch selection.
- The helper will not repair wrong phase formulas/topologies.  Tier-2
  harder-Mn retrieval and omission of weak calcite remain distinct risks; do
  not reinterpret failure there as a polishing failure.

## Case predictions

| Case | Frozen prospective prediction |
|---|---|
| b001-c02 | At least one recovery; mean >=70. Weak-calcite adherence may remain inconsistent, but polishing must not remove a retained calcite phase. |
| b001-c03 | At least 2/3 recovery and mean >=79.12 (within 5 of P0). The recovered four-phase control should be preserved. |
| b001-c06 | R-3 Mn3WO6 selected and recovered at least 2/3; mean >=55. The narrow helper's no-harm/improvement result should preserve v5's tier-1 success. |
| b002-c01 | Exact physical inventory at least 2/3, at least one recovery, and mean >=50. A helper gain on one diagnostic endpoint supports modest improvement, but the gross wrong-coordinate basin remains a known failure mode. |
| b002-c02 | Surviving tier-2 R-3 selected at least 1/3 and mean >=35; recovery is uncertain because v6 intentionally adds no retrieval breadth. A correct closed endpoint should polish rather than be replaced by a decoy. |
| b003-c01 | Exact physical R-3 + clean-WO3 inventory 3/3, helper execution at least 2/3, at least one recovery, and mean >=52. This is the clearest prospective test of accepted-model polish. |

## Package decision

The fixed promotion rule remains controlling: six complete three-replicate case
means, aggregate delta at least `max(4, 2*noise)`, and no case more than 15
below P0.  Procedure tests make a no-harm/modest-gain prediction, not a claim
that v6 will meet that rule.  In particular, promotion is unlikely unless the
fresh harder-Zn runs avoid v4/v5's gross transferred-coordinate basins.
