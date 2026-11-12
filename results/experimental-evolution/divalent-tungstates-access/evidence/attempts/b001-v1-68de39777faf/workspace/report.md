# Powder XRD phase analysis

The submitted five-phase model gives **Rwp = 15.053%**, **Rp = 8.339%**, and GOF = 8.492 on all 8,301 points. Weight fractions are normalized over the modeled crystalline material only.

| Phase | Space group | Weight fraction |
|---|---:|---:|
| MnWO4, wolframite | P2/c | 66.89% |
| WO3, monoclinic | P21/c | 14.76% |
| Mn2WO6, Y2WO6-derived analogue | P212121 | 6.59% |
| MnO, hexagonal | P63mc | 10.45% |
| Mn3O4, hausmannite | I41/amd | 1.31% |

## Evidence and model selection

The dominant peak family is indexed by wolframite MnWO4 (COD 1520200). Its refined cell is 4.79821 x 5.71387 x 4.98005 A, beta = 91.1095 degrees. Only the symmetry-allowed Mn and W y coordinates were adjusted; broader oxygen-coordinate refinement was rolled back after producing shifts much larger than the expected reference mismatch.

Residual peaks from unreacted oxide are best described by room-temperature monoclinic WO3 (COD 2311041). All nine accessible same-formula WO3 entries were screened (1004057, 1010618, 1521532, 1521533, 1528915, 1563541, 2106293, 2107312, and 2311041); the selected neutron model gave the best physically stable common-setting refinement.

The coherent 20.36, 20.90, 29.15, and 35.55 degree family requires an orthorhombic P212121 component. No exact Mn2WO6 entry was available, so the submitted model was constructed from Y2WO6 COD 1541070 by Y-to-Mn substitution while preserving topology and multiplicities, followed by independent cell refinement. Its geometry is physical (shortest W-O 1.748 A, Mn-O 2.088 A, O-O 2.381 A). Alternative Y2WO6, Fe2WO6, Cr2WO6, Bi2WO6, La2WO6, and other Mn-W-O stoichiometry/prototype branches were screened and were inferior. A modest internal [110] March-Dollase ratio of 0.747 was retained. Unrestrained cation-coordinate refinement gave a 1.30 A W-O contact and was rejected; [001]/[010] texture alternatives hit the allowed bounds and were also rejected.

Hexagonal MnO (COD 4117966) was the unique strongest match in a screen of all 38 accessible Mn-O structures and remained a positive contribution after Mn2WO6 was included. Tetragonal Mn3O4 (COD 9001963), a plausible residual precursor, accounts for weak residual intensity near 32.3, 36.7, and 59.9 degrees. Its scale remained positive with a near-source cell; a branch that improved the fit by distorting its cell by about 2% was rolled back. Cubic Mn2O3 collapsed to zero scale. One orthorhombic MnO2 import and an earlier divergent orthorhombic Mn2O3 cell trial are classified unknown, not rejected.

## Remaining uncertainty

The largest residuals are intensity mismatches on indexed Mn2WO6 reflections, so its topology and cell are better established than its atomic coordinates. Its 6.59% fraction is model-dependent (roughly 6-8% across physical texture/profile rollbacks) and should not be treated as high-precision quantification. The hexagonal MnO profile reached the laboratory envelope of 0.04 micrometre size and 8,000 ppm isotropic microstrain; its fraction varied about 7-11% across simpler physical rollbacks. Mn3O4 is near the detection/quantification limit and its 1.31% fraction is tentative. The formal scale-derived uncertainties in `result.json` therefore understate the systematic uncertainty.

Angular zero and specimen height were 99.99% correlated when refined together. The final model uses the simpler physically allowed specimen shift of -717.3 micrometres with zero fixed at 0 degrees. Every submitted CIF passes the scorer's contact/occupancy screen. No amorphous content can be inferred from this dataset, so all reported fractions are crystalline-phase-normalized.
