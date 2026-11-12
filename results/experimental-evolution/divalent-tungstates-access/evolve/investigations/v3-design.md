# v3 design

Status: v1 and v2 are complete and unpromotable. This records the frozen-test
hypothesis for the third and final candidate in development cycle 1.

## Evidence

- v2 preserves the useful common-state rule: c02 is 3/3 recovered with mean
  87.12, and one c06 run formally recovered the intended Mn3TeO6-derived R-3
  Mn3WO6 route at 15.30 wt% and Rwp 2.005%.
- c05 completed at 34.82/32.07/66.84 with mean 44.58, independently violating
  the regression gate. All runs found the formulas. The recovered run used the
  one-element FeWO4 parent and recovered a coherent ordinary profile state; the
  two failures used a two-element CoMoO4-II parent, had weaker major-framework
  accuracy, and tested many alternatives while nuisance families remained
  wrong or bounded.
- c03 completed at 47.15/42.09/65.26, mean 51.50 versus P0 84.12. All runs
  reached formula-level closure including CuO. The two failures under-refined
  accepted structures or minimally repaired a poor WO3 parent while exploring
  broad alternatives. The lone recovery recognized oscillatory residuals at
  modeled peaks, stopped prototype work, and polished the ordinary state.
- Oracle comparison of c05 projects shows the profile gap is not phase
  discovery. The successful P0 project recovered a coherent ordinary
  specimen/instrument and phase-profile solution. The v2 projects left sample
  effects absent or compensating, instrument terms inaccurate or at bounds,
  and minor-phase size/strain/texture families wrong while spending effort on
  alternate-framework trials.
- The first harder-Mn v2 run selected the intended tier-2 Cd3TeO6-derived R-3
  Mn3WO6, rejected topology/stoichiometry decoys, and recovered all fractions,
  but remained at D 2.116 because the transferred Mn3WO6 and WO3 coordinates
  were only moderately accurate. The residual problem has moved from search to
  adaptation depth.
- All three c06 v2 runs constructed Mn3TeO6-derived R-3 Mn3WO6; two selected
  it with the exact inventory and fractions. One recovered at D 0.266; the
  other remained at D 1.569 with only 55.7% Mn3WO6 site accuracy. Discovery is
  reproducible, while selection depth and coordinate/profile adaptation
  control formal recovery.
- The final c06 v2 run constructed R-3 Mn3WO6 but selected Pnnm Mn2WO5 after
  cell-only convergence gave the decoy a tiny Rwp advantage (18.63% versus
  18.81%). It then deeply adapted only the decoy and scored 21.31 (D 53.870).
  In another replicate, a provisional Pnnm advantage reversed after deeper
  relaxation. Plausible exact-stoichiometry routes need comparable adaptation
  depth before rejection.
- The second harder-Mn v2 run repeated the same mechanism with the tier-2
  parent: R-3 Mn3WO6 reached Rwp 15.13, P21/c Mn2WO5 reached 14.70, and only
  the slight early winner received deep coordinate/profile adaptation. The
  final Mn2WO5 model scored 31.67 (D 10.823) and omitted the hidden R-3 phase.
- The final harder-Mn v2 run inferred Mn2WO6 for the unassigned family,
  selected a Y2WO6-derived P212121 model, and never constructed the surviving
  tier-2 R-3 route. It reached a physical three-phase Rwp of 14.67%, launched
  15 texture screens, and timed out at 14,400 seconds without a submission.
  The invalid score is a scientific failure. A narrow reaction-balanced
  stoichiometry shortlist is needed before topology transfer, without
  restoring v1's indiscriminate breadth.
- Harder-Zn v2 completed at 91.11/28.88/31.73, mean 50.58 versus P0 72.28;
  all three recovered the exact inventory but only one formally recovered.
  Every run used CoMoO4-derived wolframite. The recovery escaped a wrong
  transferred-coordinate basin with a broader physical coordinate-start
  search, selected clean P21/c WO3 and completed texture/profile refinement.
  The failures retained weak major/WO3 coordinates while pursuing additional
  residual models or profile grids. Parent chemistry alone does not explain
  the split; post-closure coordinate-basin completion does.
- v1 is complete. Its final c06 and harder-Mn tails omitted R-3 and selected
  lower-stoichiometry decoys; broad mandatory enumeration constructed the
  desired route in only 1/3 c06 and 2/3 harder-Mn runs. Trigger specificity,
  chemical economy and completion of an accepted model matter more than raw
  search breadth.

## Leading intervention

Make prototype transfer conditional on an **unassigned reflection family**,
not merely a coherent residual. Residuals centered on reflections of accepted
phases indicate coordinate, calibration, texture or broadening mismatch and
should trigger ordinary refinement rather than a new library search. Require
same-formula candidates to be physically clean and compared in the current
multiphase state before committing. For a truly unassigned family, retain a
small reaction-balanced set of plausible stoichiometries before framework
transfer. Once every coherent residual family indexes to accepted phases,
stop structure search and make joint refinement the main task.

Final guidance summary:

> Use cross-chemistry prototype transfer only for a coherent reflection family
> that no ordinary composition or precursor/product can assign; do not use it
> to explain position, width, or intensity errors at reflections of accepted
> phases. Keep a small reaction-balanced set of plausible stoichiometries for
> that family. Among compatible topology parents, prefer the chemically nearest
> framework unless an equally adapted common-state comparison clearly favors
> another; do not rank a plausible exact-stoichiometry transfer by an early
> scale/cell fit against a deeply refined decoy. Compare physically clean
> same-formula references in the current multiphase state. Test every addition
> or replacement in the best current multiphase project; reject a plausible
> weak component only after its scale stably collapses, and keep failed trials
> unknown.
> Once every coherent residual family indexes to accepted phases, stop library
> search and devote the remaining work to ordinary joint refinement, including
> staged symmetry-allowed coordinates (well-resolved/heavy sites before weak
> light-atom substructures). If an accepted transferred framework still
> misfits intensities at its own reflections, test distinct physical coordinate
> starts before seeking another phase. Then refine
> calibration/specimen effects, and phase-specific profile terms. Keep only
> physical improvements confirmed by fresh full-grid replay.

## Freeze decision

- Keep v3 guidance-only. P0 and successful v2 runs already demonstrate the
  needed refinement operations, while a generic nuisance optimizer would risk
  overfitting and a generic prototype enumerator would recreate v1's search
  sprawl.
- Freeze the package only after these predictions and this review are final,
  then run three fresh solves on all six active cases.
