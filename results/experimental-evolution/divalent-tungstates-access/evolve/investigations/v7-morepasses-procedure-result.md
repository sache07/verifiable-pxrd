# Five-pass procedure-test result

Test: `ptest-v7-morepasses-04`

Procedure SHA-256:
`954ecebf0bbb6445cdac938860abb83f8c0c55ba4789fcdd9c87af0a8349d6fe`

The procedure test completed all 18 prospectively selected returned projects
with 18 scored outputs, no failures, and no physical flags. Ten projects
improved and eight returned unchanged; none worsened. Median hidden D fell
from 2.572690 to 2.021926.

## Prospective criteria

| Criterion | Result |
|---|---|
| All 18 projects score | Pass: 18/18 |
| Every output remains physical | Pass: 0 physical flags |
| No source project worsens by more than 0.10 D | Pass: no project worsened |
| All eight prior procedure-test outcomes retained within 0.05 D | Pass: all 8/8 retained or improved |
| Fresh c03 rep3 reaches D <= 1 | Pass: D 3.558335 -> 0.330035 |

The eight-project core contains six further improvements and two unchanged
outputs relative to their source projects. The ten fresh controls contain four
improvements and six unchanged outputs. Notable fresh changes are c03 rep1
3.629654 -> 1.534953, c03 rep3 3.558335 -> 0.330035, c06 rep2
0.949909 -> 0.772978, and harder-Zn rep2 17.433009 -> 17.322028. The
remaining fresh harder-Zn failures are unchanged, confirming that extra local
coordinate passes do not replace independent parent starts or nuisance-term
control.

## Decision

Pass. License only the fixed coordinate-stabilization cap increase from three
to five for the next prospective package. Preserve every other convergence,
rollback, fraction, geometry, and minimum-gain gate. This diagnostic does not
validate the proposed source-residue check, equal-depth parent comparison,
terminal-helper ordering, or nuisance-bound rollback; those remain behavioral
interventions that require rollout comparison.

