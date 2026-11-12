# Powder XRD phase analysis

The crystalline pattern is best described by scheelite SrWO4, residual monoclinic WO3, and a third hexagonal phase. The normalized nominal fractions are 79.13, 11.65, and 9.22 wt%, respectively. These fractions exclude any amorphous or still-unmodeled material.

| Phase | Space group and refined cell | Weight fraction | Assessment |
|---|---|---:|---|
| SrWO4 (scheelite) | I 41/a; a = 5.41953 A, c = 11.96334 A | 0.79132 | Secure identification |
| WO3 (monoclinic) | P 21/c; a = 7.30606 A, b = 7.54009 A, c = 10.53697 A, beta = 133.0979 deg | 0.11652 | Secure phase/lattice identification; oxygen coordinates are weakly constrained by X-rays |
| Hexagonal average-model phase | P 63/m c m; a = 9.61676 A, c = 3.90999 A | 0.09216 | Tentative structure and composition |

## Evidence

The dominant peak positions and intensity pattern match scheelite SrWO4, which is also the expected product from SrCO3 and WO3 after firing at 900 C. A second coherent set of reflections matches monoclinic WO3 and accounts for unreacted precursor. After those two phases are fitted, residual peaks near 10.98, 21.69, 29.70, 32.59, 44.50, 53.63, 67.2-67.8, and 94.8 deg 2-theta index on a hexagonal cell near a = 9.62 A and c = 3.91 A. Adding this lattice lowers Rwp from about 16.15% for the two-phase model to 14.63%. Searches for a stable fourth crystalline phase, including residual carbonate and additional tungstate/oxide candidates, did not produce a reproducible positive contribution.

The third-phase CIF is a chemically complete, contact-free WO3 average framework with corner-sharing WO6 units. It reproduces the indexed reflection family but is not a unique structure solution: heavy-atom split-site, Sr-bearing, and related average models give similar profiles. Its preferred-orientation parameter also reached the allowed March-Dollase boundary (0.70 along 111), so scale and texture are correlated.

## Uncertainty

The formal least-squares fraction uncertainties (about 0.2-0.3 wt% absolute) substantially understate model uncertainty. Across reasonable third-phase average models its nominal abundance is approximately 9-15 wt%, with compensating changes in the SrWO4 fraction. Therefore the submitted 9.22 wt% value, and the atomic identity/topology of that phase, cannot be considered reliable without complementary composition data or higher-resolution diffraction. The identifications of SrWO4 and monoclinic WO3 are much more robust. No claim is made for amorphous content.

Fit statistics from an independent forward replay of `final.gpx` over all 8,282 observed points are Rwp = 14.630%, Rp = 9.751%, Rexp = 3.532%, and goodness of fit = 4.142. The elevated goodness of fit and correlated residuals are consistent with the unresolved third-phase structure and simplified microstructure model.
