# Crystalline phase analysis

The pattern is modeled as three crystalline phases: scheelite BaWO4, R-3c Ba3W2O9, and monoclinic gamma-WO3. The refined crystalline-only fractions are approximately **66.9 wt% BaWO4, 16.9 wt% Ba3W2O9, and 16.2 wt% WO3**.

| Phase | Space group | Refined cell | Crystalline wt% |
|---|---|---|---:|
| BaWO4 | I 41/a | a = 5.63044 A, c = 12.69400 A | 66.94 |
| Ba3W2O9 | R -3 c | a = 10.13489 A, c = 13.95624 A | 16.86 |
| WO3 | P 21/n | a = 7.29889 A, b = 7.53687 A, c = 7.68728 A, beta = 90.8812 deg | 16.20 |

## Evidence

BaWO4 accounts for the dominant line at 26.69 degrees and the complete sequence at 28.39, 32.04, 43.19, 45.81, 48.98, 53.68 degrees and higher angles. Ba3W2O9 is independently required by its characteristic reflections at 17.76, 26.28, 30.82, and 40.80 degrees. The 23.40/23.88/24.65 degree triplet and its higher-angle partners identify WO3.

Phase-omission tests are decisive: Rwp rises from 4.95% to 7.03% without WO3, to 8.27% without Ba3W2O9, and to 9.45% for BaWO4 alone. Orthorhombic and tetragonal WO3 models fit worse. A triclinic WO3 model gives only a marginal Rwp improvement (about 0.06 percentage point) despite three extra cell parameters, and its alpha and gamma angles refine to within 0.01 degree of 90 degrees; the room-temperature P 21/n model is therefore preferred. A BaCO3 trial lacked its diagnostic 19.4-19.9 degree lines and collapsed to an unphysical approximately 1 nm broadening term, so crystalline BaCO3 was not retained.

## Refinement and uncertainty

GSAS-II refinement used the full 9.90-100.09 degree range, the reported Cu K-alpha1/K-alpha2 wavelengths and 0.5 intensity ratio, Poisson counting weights because point uncertainties were absent, a smooth Chebyshev background, refined phase scales and cells, and phase-specific isotropic broadening. The fit is Rp = 3.66%, Rwp = 4.95%, Rexp = 3.02%, and goodness-of-fit = 1.64.

The ordered BaWO4 oxygen position was held at a chemically reasonable tetrahedral geometry (W-O = 1.81 A); unconstrained light-atom refinement was not reliable. Only the Ba3W2O9 W z coordinate was refined; the remaining minor-phase atomic coordinates were held to reference structures. The reported covariance errors in `result.json` are formal only. Because no calibrated instrument profile or standard was supplied, profile/size separation and the refined 0.280 degree zero correction introduce larger systematic uncertainty; realistic fraction uncertainties are about 2-3 absolute wt% (roughly 3 wt% for BaWO4 and WO3). Cell precision is likewise overstated by the formal errors. Fractions are normalized over modeled crystalline phases and cannot measure any amorphous content.
