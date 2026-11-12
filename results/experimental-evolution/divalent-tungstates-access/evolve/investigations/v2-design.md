# v2 design draft (pre-freeze)

Status: mechanism selected after the first v1 c06 completion; ready to freeze as
guidance-only v2 while the remaining v1 attempts continue as replication.

## Evidence motivating replacement

- v1 makes clean-candidate selection and full inventory recovery more common,
  but c03 regressed 33.61 score points and is 0/3 recovered versus P0 3/3.
- Several solvers treated the four gates as the main task and under-refined an
  otherwise correct inventory. The detailed nuisance staging displaced P0's
  stronger ordinary refinement behavior.
- The clearest false rejection was procedural, not crystallographic: a c03
  solver screened CuO as a standalone phase instead of adding it to the stable
  three-phase project. Other failures similarly promoted failed or boundary
  branches into evidence.
- Broad enumeration without completed common-state comparisons creates a large
  ledger of unknowns and consumes attention without improving the final model.

## Candidate intervention

Replace all four v1 gates with one conditional residual rule and one final-state
rule. The first completed c06 attempt satisfies the mechanism criterion: it
constructed and selected Mn3TeO6-derived R-3 Mn3WO6 in the proper common state,
recovering 15.47 wt% versus 15.46 wt% truth.

Provisional guidance (89 words):

> Use residual-directed prototype transfer only when ordinary references leave
> coherent peaks. Search same-stoichiometry frameworks across chemistries,
> including one- or two-element substitutions, construct the target composition,
> and retain distinct plausible symmetries. Test every replacement or addition
> in the current best multiphase project with the other phases and nuisance
> settings unchanged; an isolated phase-only fit is not evidence. Failed or
> aborted trials remain unknown, and a plausible precursor is rejected only by
> stable near-zero scale in that common state. Physically screen submitted CIFs.
> After closure, resume normal refinement from the best saved project and submit
> the lowest-Rwp replayed physical model.

## Decision

Test the short guidance alone as v2. Do not ship a helper: a fresh solver reached
the intended route from prose, while the exploratory ranker still places a false
Ba3WO6 route first on c06 and misses Cd3TeO6 in the top 40 on the raw harder-Mn
mixture. Remaining c06 and harder-Mn results are replication and transfer
evidence, not prerequisites for this mechanism choice.
