# PXRD phase analysis

The refined crystalline assemblage is 81.64(52) wt% scheelite SrWO4, 9.84(28) wt% WO3, and 8.52(48) wt% of an F-centered cubic component modeled tentatively as ordered double-perovskite Sr3WO6. Fractions are normalized only over these modeled crystalline phases; this dataset cannot determine amorphous content or absolute crystallinity.

| Phase model | Space group | Refined cell (A, degrees) | Crystalline wt% |
|---|---:|---|---:|
| SrWO4 | I41/a (88) | a = 5.41105, c = 11.94320 | 81.64(52) |
| WO3 | P21/c (14) | a = 7.67332, b = 7.52516, c = 10.52635, beta = 136.1995 | 9.84(28) |
| Sr3WO6 | Fm-3m (225) | a = 8.58944 | 8.52(48) |

## Evidence and model selection

The chemical inventory is consistent with the reported SrCO3 + WO3 precursors heated at 900 C. The SrWO4 and WO3 atomistic models came from COD entries 1546036 and 2311041. The third component has a repeated F-cubic reflection sequence (including approximately 20.68, 29.77, 35.31/36.72, 42.19, 53.44, 61.28, 64.94, 70.78, 74.69, 78.60, 83.91, and 93.32 degrees 2theta); a charge-balanced Sr3WO6 model in Fm-3m, derived from the ordered double-perovskite topology of COD 1001128, explains that family without strong unmatched predictions.

Matched mature-model leave-one-out tests raised Rwp from 20.744% to 41.442% without SrWO4, 22.169% without WO3, and 21.408% without Sr3WO6. Retested SrCO3 and Sr3W2O9 additions refined to only 0.51(50) and 0.28(22) wt%, respectively, with negligible complete-pattern gains; monoclinic SrWO4 collapsed to zero scale. A triclinic WO3 replacement was worse at fixed cell (Rwp 21.293%); freeing six cell terms gave only a nominal 20.724% and failed to converge, so the stable P21/c model was retained.

The final refinement uses the supplied Cu K-alpha doublet, a 12-term Chebyshev background, one stable sample-displacement correction, global Gaussian width, SrWO4 isotropic size broadening, and Sr3WO6 isotropic microstrain. Texture and atomic-coordinate branches were rejected as negligible, unstable, or chemically implausible. All submitted CIFs pass the supplied occupancy, symmetry, duplicate-site, and contact audit. The regenerated profile exactly matches the profile saved in `final.gpx`; Rwp = 20.744%, Rp = 15.194%, and GOF = 5.877 with no dropped variables.

## Remaining uncertainty

The SrWO4 assignment is robust. WO3 itself is well supported, but its exact low-symmetry polymorph is not uniquely resolved by this uncalibrated powder dataset. The Sr3WO6 assignment is tentative: its lattice and multiple reflections are supported, but the atomistic identity was obtained by chemically constrained topology transfer rather than a direct database match. Its very large refined microstrain (about 1.47 x 10^4 microstrain) is correlated with scale, so 8.5 wt% is semi-quantitative and the formal 0.48 wt% standard uncertainty understates model uncertainty. Atomic coordinates were therefore kept at audited source/model values. The high GOF also reflects systematic profile/intensity mismatch and Poisson weights inferred from counts because pointwise uncertainties and a calibrated instrument profile were not supplied.
