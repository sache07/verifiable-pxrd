# Batch b005 prospective review

## Scope and role

This one-case optional transfer batch was curated before any b005 solver rollout and before reading any v6 outcome. It is intended for a second active-panel opening, not as an outcome-selected replacement for b004. It introduces same-composition polymorph separation, a challenge not represented in b001-b003.

| Case | Inventory (wt%) | Difficulty or control role | Fit to the lab priorities |
|---|---:|---|---|
| b005-c01 | Stolzite PbWO4 60.00, raspite PbWO4 25.00, massicot PbO 7.36, WO3 7.64 | Full-reference four-phase PbO reaction with two structurally distinct PbWO4 polymorphs. Equimolar residual PbO and WO3 preserve global Pb:W = 1:1. | Tests whether one formula match is incorrectly treated as phase closure, whether overlapping same-composition frameworks are separated, and whether both polymorphs and weak precursors survive a heavy-atom refinement. |

Both PbWO4 frameworks and both residual precursors remain available. A one-hour firing without regrinding makes coexistence of product polymorphs and unreacted precursors a defensible kinetic diagnostic, but the published structures do not establish that this assemblage is an equilibrium state at 650 C.

## Source review

- COD 1527935 is an ordered I41/a scheelite/stolzite PbWO4 model. COD 9007617 is the structurally distinct ambient P21/a raspite model. Both register as ordered 24-site cells and pass broad geometry, with minimum separations 1.753 and 1.746 A respectively; those shortest distances are W-O bonds.
- COD 2310433 is the ordered orthorhombic Pbcm massicot PbO neutron model, with a 2.165 A minimum separation.
- COD 2311041 is the physically screened P21/c WO3 neutron model used in earlier batches.
- A newer synthetic 290 K stolzite source, COD 9009811, was the first prospective choice. It registered cleanly but the fixed reference-mismatch realization could not preserve its detected symmetry in twenty deterministic redraws, so generation stopped before a case existed. It was replaced on source robustness grounds by the independent ordered COD 1527935 model; the recipe, seed, composition, and challenge were not changed.

## Prospective generation audit

The recipe, seed, count level, and composition were fixed before generation. The source substitution above repaired a generation-validity failure rather than selecting a favorable solver or score outcome. The resulting case passed the frozen strict-recovery checks.

| Case | Oracle max fraction error | Oracle Rwp (%) | Omission RMS, stolzite / raspite / PbO / WO3 (noise units) | Strict eligible |
|---|---:|---:|---:|---|
| b005-c01 | 0.000467 | 2.266 | 16.820 / 7.761 / 3.604 / 2.356 | yes |

Every phase is individually detectable in the fixed realization. The omission audit uses known generating structures and background family; it does not prove unique polymorph assignment among all possible PbWO4 models.
