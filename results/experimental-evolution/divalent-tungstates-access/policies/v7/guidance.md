# Close, compare, finish, polish


Work from the specimen inputs, pattern, and frozen index. Build ordinary phases
first. In the best complete common state, map coherent residual families and
test exact-composition references or chemically plausible products. Before
declaring closure, retain only positive contributions stable across a
reflection family; numerical failure is unknown, not rejection. Stop library
search once all coherent families index to physical accepted phases.

Only while one coherent family remains genuinely unassigned, form a short
reaction-balanced formula list and compare symmetry-diverse compatible parents
from substituted chemistries; do not restrict parents to the sample elements.
For each serious missing-reference topology preserve at least two physical
starts when available. Convert candidates to the target composition and give
them identical cell and coordinate adaptation before texture, roughness, or
other nuisance terms. Compare only equally developed checkpoints; early Rwp or
substitution count is not decisive. Keep the winning physical basin, discard
the others explicitly, and stop this search at physical closure.

Finish the accepted model before final polish: scales/background, cells and
calibration, supported coordinates, then supported phase/profile/specimen
terms. Require replay stability. Roll back any calibration or profile term
outside the supplied laboratory ranges, pinned at a tested bound, or
inseparable from a correlated alternative. Center/wing residuals on accepted
reflections mean profile work is unfinished, not evidence for a new phase.

Only then save `final.gpx` and run the supplied bounded polish exactly once:

```bash
$GSAS2_PYTHON learned/staged_polish.py final.gpx polished.gpx inputs
```

Review its audit and accept only a converged physical branch. After invocation,
perform read-only geometry/replay checks and export; do not add phases or refine
coordinates, cells, calibration, profile, background, scales, or nuisance
terms. If such work is needed, the input was not terminal. Submit the accepted
project and re-export every CIF, fraction, `fit.csv`, and report from that exact
project.
