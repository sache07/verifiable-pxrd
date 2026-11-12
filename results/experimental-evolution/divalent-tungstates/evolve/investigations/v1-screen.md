# v1 prospective development screen

Frozen package: v1, 401 guidance words, helper hash `0d58e24b4c66dfc7d43567767635c32522c40d000b584912343304844794e5b8`. Group `b001-v1` is one fresh solve per case. This rubric was fixed before any v1 completion.

| Case | Prospective behavioral check | Scientific success check |
|---|---|---|
| c01 | Inspect/reset HAP defaults; use a physical, adequate global-to-phase width sequence without unnecessary inventory work. | Correct sole phase, physical replay, profile near the noise floor; no regression from the 85.86 P0 mean. |
| c02 | Retain ZnWO4+WO3+ZnO; select a physically passing WO3 record; keep global widths nonnegative and release phase terms selectively. | All three phases and stable fractions; physical replay; headline above the 57.48 baseline and aiming above 80. |
| c03 | Adapt scheelite cleanly; compare WO3 polymorphs before flexible texture/strain and reject compensation-driven alternatives. | Correct SrWO4+monoclinic WO3+SrCO3, physical replay, improved structural/profile agreement over 46.31. |
| c04 | Preserve the already successful MnWO4/Mn3O4 inventory search; use physical WO3 and an adequate positive profile before phase broadening. | Correct three phases and reasonable weak-phase fraction; physical replay; improve over the 40.95 high-variance baseline. |
| c05 | Treat coherent residuals as missing-structure evidence, invoke the generic stoichiometric-analogue helper, adapt and screen a same-framework parent, then reconverge. | Recover Ca3WO6 with CaWO4+WO3, remove spurious CaO, physical replay, large gain over the 26.41 baseline. |
| c06 | Screen alternate records, retain massicot PbO, reconverge after every inventory change, and initialize HAP broadening explicitly. | Recover all four physical phases and improve over the 43.25 baseline without source/profile review flags. |

The screen passes only if the intended mechanisms are actually used, not merely if a score rises. The package should be revised if any case remains below 80, while preserving successful behavior and avoiding case-specific additions.

## Results as completed

| Case | Score / profile | Behavioral result | Decision |
|---|---|---|---|
| c01 | 98.02; D 0.0250; Rwp 2.303%; physical pass | Reset microstrain to zero and size to 10 micrometres; selected positive U/W/Z, rejected correlated V/axial terms, and used no texture or phase broadening. | Pass. Preserve this guidance unchanged. |
| c02 | 72.56; D 0.419; Rwp 3.274%; physical pass | Correct inventory and physical WO3; common polymorph comparison, positive U/W/X, zero strain defaults, selective ZnWO4 size. Fractions bias ZnO high and WO3 low. Solver forced specimen displacement versus zero, while truth contains identifiable contributions from both, and omitted strong WO3-specific strain. | Behavioral mechanism passes but score target fails. Test staged second angular correction and residual-driven phase strain after the screen; avoid weakening the c01 guard. |
| c03 | 63.83; D 0.735; Rwp 3.796%; physical pass | Correct three-phase inventory, physical monoclinic WO3, clean cross-chemistry scheelite adaptation, neutral HAP defaults, and supported WO3 strain/texture. Fractions are within about 3 wt% of truth. Common widths absorbed true relative phase-size differences; displacement was forced against zero although both effects exist. | Core mechanism passes but score target fails. Same staged angular/common-profile hypothesis as c02; analogue-coordinate uncertainty is secondary. |
| c05 | 47.53; D 3.214; Rwp 4.617%; physical pass | The solver invoked the generic analogue helper, ranked and adapted a same-framework A3BO6 parent, recovered Ca3WO6 with CaWO4+physical monoclinic WO3, and rejected spurious CaO. Fractions are 79.27/10.75/9.99 wt% versus 76.92/12.39/10.69 truth. A single zero term approximated the combined true zero+displacement, while common W, a wrong-axis texture term, and excessive Ca3WO6 strain absorbed phase-profile differences. | Inventory/helper mechanism passes strongly but profile target fails. Preserve analogue discovery; test staged dual angular correction and resolved-peak-anchored profile allocation before changing the helper. |
| c04 | 35.29; D 8.892; Rwp 7.731%; physical pass | Correct MnWO4+WO3+Mn3O4 inventory, screened WO3, clean wolframite adaptation, and fractions 75.20/19.42/5.38 wt% versus 74.67/19.06/6.27 truth. The single zero ran to -0.497 degrees to absorb true zero+displacement. A large fixed U/V/W profile and WO3 strain then absorbed broadening that truth assigns mainly to finite Mn3O4/WO3 sizes and Mn3O4 strain. | Inventory, source, and adaptation mechanisms pass; profile target and baseline-regression check fail. This is the strongest test case for staged angular correction followed by phase-attributed widths. |
| c06 | 70.17; D 0.590; Rwp 3.146%; physical pass | Recovered all four physical phases, including 4.60 wt% massicot versus 5.43 wt% truth; screened records, reconverged inventory changes, and used supported positive global widths plus selective sizes. A displacement of -730 micrometres approximated the true -326 micrometres plus +0.246-degree zero; omitted anisotropic phase strain remains the principal profile limitation. | Core source/inventory/HAP mechanisms pass strongly and improve about 27 points over the P0 mean; target still fails. Preserve this workflow and test the replicated dual-angular rule before adding broader profile complexity. |

All six v1 projects have the correct phase inventory, physically valid replay,
and no source/profile review flag. Mean score is 64.56 versus 50.04 for P0;
five cases improve and c04 regresses. The package therefore succeeds on phase
discovery and physical model selection but does not yet meet the predeclared
per-case profile target. Revision should preserve all inventory mechanisms and
address only the replicated angular/profile-allocation failure.
