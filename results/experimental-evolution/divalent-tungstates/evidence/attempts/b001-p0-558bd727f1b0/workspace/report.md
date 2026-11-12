# PXRD phase analysis

## Result

The pattern is a three-phase crystalline mixture. Weight fractions are normalized over the modeled crystalline phases.

| Phase | Space group | Refined cell (Å) | Weight fraction |
|---|---:|---|---:|
| SrWO4, scheelite | I 41/a (No. 88) | a = 5.39405, c = 11.90269 | 64.56 wt% |
| WO3, orthorhombic | Pnma (No. 62) | a = 7.55372, b = 7.28593, c = 7.69113 | 20.13 wt% |
| SrCO3, strontianite | Pnma (No. 62) | a = 6.02546, b = 5.09775, c = 8.39501 | 15.30 wt% |

The converged GSAS-II fit has Rwp = 4.632%, Rp = 3.288%, Rexp = 2.861%, and GOF = 1.621 for 8,284 observations. The refined fractions sum to 1.000000.

## Evidence and model

Scheelite SrWO4 accounts for the dominant reflections, including those near 17.47, 27.20, 29.45, 32.64, 44.82, 47.13, 51.40, 55.53, and 56.82° 2theta. Orthorhombic Pnma WO3 is selected by the diagnostic 22.55/22.97/23.85° triplet and its high-angle sequence. In a common screening refinement, SrWO4 alone gave Rwp = 12.20%; adding tetragonal, monoclinic, or triclinic WO3 gave 12.89%, 12.00%, and 10.04%, respectively, while Pnma WO3 gave 8.79%.

Pnma SrCO3 explains the remaining coherent reflections around 24.64, 25.29, 29.07, and 30.97° and is chemically consistent with the SrCO3 precursor. Adding its fixed reference structure to the polished two-phase fit reduced Rwp from 5.77% to 5.01%; refining its cell and the full three-phase profile reduced Rwp to 4.63%. No residual peak set supports a fourth crystalline phase.

The refinement used the reported Cu K-alpha1/K-alpha2 wavelengths and 0.5 intensity ratio, Bragg-Brentano reflection geometry, Poisson count weights, an eight-term Chebyshev background, specimen displacement, empirical profile terms, and one March-Dollase correction per phase. Lattice parameters, phase scales, background, effective polarization, selected profile terms, and effective SrWO4/WO3 microstrain were refined. The final project is `final.gpx`, and `fit.csv` contains observed, calculated, and observed-minus-calculated counts over the fitted range.

## Uncertainty and limitations

The covariance-only standard uncertainties are 0.16–0.21 absolute wt%, but they understate model uncertainty. Reasonable background/profile/texture variants move the fractions by about 1–3 absolute wt%; a practical reading is therefore approximately 64.6 ± 3 wt% SrWO4, 20.1 ± 3 wt% WO3, and 15.3 ± 3 wt% SrCO3. Differential microabsorption was not correctable without particle-size information and could make the true systematic error larger. Amorphous content cannot be determined without an internal standard, so these values apply only to the modeled crystalline fraction.

Atomic coordinates were retained from reference scheelite, Pnma WO3 (COD 2107312), and Pnma SrCO3 (COD 9008198) models. Free oxygen-coordinate or displacement-parameter refinements were unstable or produced implausible geometry, so detailed atomic positions are not independently determined by this dataset. The refined cells are also correlated with an approximately 1.003 mm specimen-displacement correction; the extra digits in the CIFs should not be interpreted as absolute cell accuracy.
