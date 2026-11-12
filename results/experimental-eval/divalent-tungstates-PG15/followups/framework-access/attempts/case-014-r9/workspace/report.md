# Powder XRD phase analysis

The pattern is best represented by three crystalline phases. The refinement used the unprocessed 10-100 degree scan with the reported Cu Kalpha1/Kalpha2 wavelengths (1.540598/1.544426 A) and 0.5 intensity ratio. Weight fractions are normalized over these modeled crystalline phases; they do not include any amorphous material.

| Phase | Space group and refined cell | Crystalline weight fraction |
|---|---|---:|
| SrWO4 (scheelite) | I 41/a; a = 5.42114 A, c = 11.96578 A | 68.56% |
| WO3 | P 21/c; a = 7.30583 A, b = 7.54397 A, c = 10.54108 A, beta = 133.0790 deg | 11.37% |
| Sr3WO6-type | P a -3; a = 10.94067 A | 20.07% |

## Evidence

The dominant reflections are indexed by scheelite SrWO4, including the strong 112 line near 28.00 degrees and the coherent 45.47, 51.98, 56.09, and 57.37 degree series. Monoclinic WO3 accounts for the split 23.48/23.96/24.74 degree group and additional lines near 33.61, 34.53, 41.79, and 42.20 degrees. After those phases are included, a reproducible residual series remains at approximately 18.51, 29.80, 30.94, 38.95, 44.93, 51.81, 53.95, 56.72, 76.63, and 94.90 degrees. It is indexed consistently by a cubic Pa-3 cell and is modeled as Sr3WO6 using the isostructural Cu3WO6 framework with Cu replaced by Sr, followed by cell and small cation-coordinate refinement. Alternative Sr oxide/carbonate, WO3-polymorph, and lower-symmetry Sr-W-O trial phases did not give a stable additional contribution or a comparably coherent indexing of this series.

The exact saved atomic model gives Rwp = 12.884%, Rp = 8.572%, Rexp = 3.532%, and goodness of fit = 3.648 over all 8,282 points. The GSAS-II project replay regenerates the submitted calculated profile from the atomic models without optimization.

## Remaining uncertainty

SrWO4 is the most secure identification. WO3 is a minor, highly overlapped component: its phase identity and cell are supported, but its oxygen coordinates are inherited from the historic P21/c reference and cannot be determined reliably from this pattern. In particular, that reference contains four symmetry-related O-O contacts near 1.58 A; a modern neutron-derived WO3 model removes them but gives a slightly poorer fit (Rwp 12.946% instead of 12.884%). The submitted WO3 coordinates should therefore be treated as a diffraction-matching diagnostic model of the W sublattice, not as a reliable oxygen geometry. The Sr3WO6 inventory and cubic cell are supported by many residual peaks, but this is an analogue-derived structural assignment rather than an independently solved structure. Its oxygen coordinates, anisotropic broadening/texture parameters, and exact fraction are correlated and are not reliable to the displayed numerical precision; a few weight-percent absolute systematic uncertainty is more realistic. The elevated Rwp relative to Rexp shows remaining profile/model mismatch, so trace crystalline material below the overlapping residual level cannot be excluded, but no fourth phase is justified quantitatively.
