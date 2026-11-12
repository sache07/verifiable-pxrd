# v4 design

v3 proved that ordered common-profile fitting, global-intensity checks, and
texture-axis comparison can reach the noise floor (c02) and strongly improve
c03/c05. It failed reliably as a package because it did not distinguish the
provisional profile needed for inventory decisions from the final profile pass:
c04 finalized widths before adding Mn3O4, while c06 treated one unsuitable PbO
record as decisive. v4 makes those two transitions explicit and removes detail
that competes with them. The analogue helper remains byte-identical.

Prospective predictions for one fresh screen are below. The first request runs
the still-unresolved c03--c06; successful v3 c02 and v1 c01 are held as
regression cases until these improve.

| Case | Required v4 behavior | Success check |
|---|---|---|
| c02 | Preserve v3's physical three-phase result and restart the final profile only after inventory stability. | Correct physical inventory and score >80. |
| c03 | Preserve monoclinic WO3 under a common nuisance comparison; challenge phase widths for all three retained phases before texture. | Correct structures/inventory and score >80. |
| c04 | Complete MnWO4/WO3/Mn3O4 inventory before the clean profile pass; test Mn3O4 and WO3 size/strain and early repeated asymmetry. | Correct physical inventory and major recovery toward score >80. |
| c05 | Invoke the unchanged analogue helper; retain Ca3WO6; preserve global-intensity-before-axis comparison while restarting widths after inventory completion. | Correct physical inventory and score >80. |
| c06 | Treat zero scale from one PbO record as record-specific; screen a second physical alternate and retain all four phases before final profiling. | PbO retained, physical replay, score >80. |

Any inventory or physical regression rejects v4. A stored-fit-only gain,
bound-seeking branch, or failure to restart after an inventory change does not
count as the intended mechanism.

## Results as completed

| Case | Score / profile | Behavioral result | Decision |
|---|---|---|---|
| c06 | 54.18; D 1.852; Rwp 4.150% versus 2.485% floor; physical pass | The explicit record rule restored the complete PbWO4/WO3/Pb3O4/massicot-PbO inventory. Massicot remained independently supported at 4.65 wt% versus 5.43% truth, fractions were close, and structural score was 82.86. The solver then performed the mandated clean restart and phase-by-phase tests, but rejected U/W, fixed common X=5.69, and retained isotropic PbWO4/Pb3O4/PbO sizes plus WO3 strain. The generating profile has nonzero U/W, X=2.68, and strong anisotropic strain on Pb3O4/PbO. | Source-alternate and post-inventory restart mechanisms pass; score improves 17 points over v3 but remains below v1 and the >80 target. The residual failure is common-X versus anisotropic phase-strain allocation, not inventory attention. |
| c04 | 30.72; D 9.786; Rwp 7.923% versus 2.490% floor; physical pass | The solver selected good MnWO4/WO3 sources but rejected true Mn3O4 after only 0.07--0.11 Rwp-point gains under the provisional profile and did not retry it after the clean restart. The two-phase model inflated MnWO4 to 78.52 wt%. Its restarted profile again discarded U/SH-L (W=10.49, X=7.12), retained WO3 size, polarization, and weak texture, and remained near the diagnostic common-restart Rwp without completing the true all-phase allocation. | Severe inventory and profile failure. v4's one-way “inventory then profile” sequence is too rigid for overlapped weak phases: plausible candidates rejected under the provisional profile must be re-challenged after a physical common restart before exclusion. Interior common-profile starts also need to be explicit. |
| c05 | 60.35; D 1.114; Rwp 3.222% versus 2.241% floor; physical pass | The unchanged helper again recovered Ca3WO6; fractions were close, CaWO4 size was 0.087 micrometre, and [110] texture was correctly selected with ratio 1.245. However, the solver never tested sample roughness. It instead retained polarization, an 18-term Chebyshev background, common W/X with U pruned, and Ca3WO6 size. Structural score was 79.93. | Inventory/helper/texture mechanisms pass, but the score regresses from v3's 72.51 because v4 compressed the explicit background/polarization/roughness challenge into “global intensity effects.” Restore those named branches before texture and require a smooth background so it cannot absorb a shared low-angle trend. |
| c03 | 58.59; D 1.082; Rwp 4.139% versus 2.851% floor; physical pass | The solver retained the correct SrWO4/WO3/SrCO3 inventory and selected monoclinic WO3, but regressed from v3's 71.33. It stayed in a zero-only basin (zero = -0.637 degrees versus the generating zero plus specimen displacement), fixed polarization at 0.5, and rejected U/SH-L after releasing them only from their lower bounds. It retained WO3 size and [110]/[001]/[001] texture for SrWO4/WO3/SrCO3, but never tested the diagonal SrWO4 [111] family and did not combine the positive WO3 size and strain branches. Fractions were 62.19/22.87/14.94 wt% versus 59.06/25.02/15.93 truth; the wrong angular model also degraded cell accuracy and structural score to 74.42. | Inventory and polymorph mechanisms pass, but the clean restart is not robust when terms are released only from a bound. Require multiple interior common-profile starts, compare zero-only with displacement-only under the same converged model, test smooth background/polarization/roughness before texture, include axial and diagonal texture directions, and combine complementary positive size/strain branches before pruning. |
