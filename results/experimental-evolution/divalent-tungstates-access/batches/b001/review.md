# Batch b001 prospective review

## Scope and selection

This six-case learning batch was fixed before any solver rollout. It spans a clean control, two full-reference multiphase reactions, and three missing-reference adaptations. All mixtures preserve the robotically dosed 1:1 divalent-metal:W ratio. Cation-rich intermediates are paired with the stoichiometric amount of residual WO3, which is plausible for a one-hour firing without regrinding even though a published structure is not itself proof that the phase is stable at the stated firing condition.

| Case | Inventory (wt%) | Difficulty or control role | Fit to the lab priorities |
|---|---|---|---|
| b001-c01 | ZnO 25.99, WO3 74.01 | Clean unreacted equimolar precursor control; full references, high counts, zero-offset and specimen-effect controls. | Establishes whether phase retrieval and mass quantitation work when complex refinement is unnecessary. |
| b001-c02 | CaWO4 80.19, CaCO3 5.97, WO3 13.84 | Moderate full-reference partial reaction. The weak calcite is deliberately near the identification limit while the two stronger phases constrain the chemistry. | Tests persistence with a minor residual precursor under ordinary profile, displacement, texture and reference-mismatch effects. |
| b001-c03 | CuWO4 65.48, Cu3WO6 12.59, CuO 2.43, WO3 19.50 | Hard four-phase full-reference reaction. The Cu3WO6 cation-rich intermediate and very weak CuO coexist with triclinic CuWO4 and WO3. | Isolates complex search/refinement and overlapping-phase behavior from missing-reference adaptation. |
| b001-c04 | SrWO4 80.49, SrCO3 7.59, WO3 11.92 | Easier missing-reference case. Every SrWO4 record is withheld. The nearest survivor is tier 1 CaWO4 (COD 7219229; Ca->Sr; framework RMS 0.0226; cell mismatch 4.3%). | Tests whether a solver recognizes a major missing scheelite and adapts a chemically adjacent framework while retaining minor phases. |
| b001-c05 | ZnWO4 75.00, ZnO 6.50, WO3 18.50 | Harder paired adaptation case. Both same-composition records and all eight one-substitution framework matches are withheld. The nearest survivor is tier 2 NbInO4 (COD 1524100; In->Zn and Nb->W; framework RMS 0.0106; cell mismatch 4.2%). | Tests deliberate two-site reference adaptation in a multiphase pattern, beside the easier tier-1 case required to make failure interpretable. |
| b001-c06 | MnWO4 68.42, Mn3WO6 15.46, WO3 16.12 | Missing secondary intermediate rather than missing principal product. COD 2002703 is withheld; tier 1 Mn3TeO6 (COD 2211528; Te->W; framework RMS 0.0183; cell mismatch 1.86%) survives. | Targets persistence after an initially convincing MnWO4/WO3 fit and chemical-intuition-guided recovery of an off-stoichiometric secondary phase. |

## Source review

- Twelve ordered models were registered from the frozen COD. Registration reports no remaining parsing warnings. Every registered model and every case-specific mismatched reference passes the scorer's frozen physical screen.
- The selected WO3 is the published monoclinic P21/c neutron-diffraction model COD 2311041. Its shortest W–O and O–O distances are 1.715 and 2.539 A. The initially considered COD 1528915 was rejected after the freeze gate exposed four fully occupied O–O contacts at 1.575 A. The CuWO4, SrWO4 and MnWO4 records are the ordinary low-pressure P-1, scheelite I41/a and wolframite P2/c forms, respectively; high-pressure CuWO4 P2/c, SrWO4 C2/c and Sr3W2O9 were explicitly not selected.
- Cu3WO6 and Mn3WO6 are published, fully occupied structures with sensible broad geometry screens. Their use models locally cation-rich intermediates, balanced globally by residual WO3; it does not assert equilibrium stability.
- COD 1547347 has valid 294 K calcite atom sites but a defective header (`C Ca O`, formula weight 68.1). The registered repaired source changes only `_chemical_formula_sum` to `C Ca O3` and `_chemical_formula_weight` to 100.086, matching the unchanged occupied composition and published calcite identity. The original COD ID remains the parent.

## Prospective generation audit

Seeds and recipes were chosen before generation and were not changed in response to private specimen realizations. All six cases passed the frozen strict-recovery checks.

| Case | Oracle max fraction error | Oracle Rwp (%) | Minimum omission RMS (noise units) | Strict eligible |
|---|---:|---:|---:|---|
| b001-c01 | 0.000399 | 2.824 | 7.479 | yes |
| b001-c02 | 0.000765 | 3.125 | 0.408 | yes |
| b001-c03 | 0.000200 | 1.620 | 2.191 | yes |
| b001-c04 | 0.001000 | 4.000 | 0.693 | yes |
| b001-c05 | 0.000095 | 2.264 | 2.214 | yes |
| b001-c06 | 0.000128 | 1.808 | 10.115 | yes |

The omission audit is an identifiability screen with known generating structures and background family, not evidence of uniqueness. The panel is prospective: no case was selected or discarded using solver outcomes.
