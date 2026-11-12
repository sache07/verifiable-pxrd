# PXRD phase analysis

The crystalline pattern is best described by four phases in the PbO-WO3 system. Fractions below are normalized over those modeled crystalline phases; this experiment does not determine an amorphous fraction.

| Phase | Space group | wt% | statistical s.u. (wt%) | CIF |
|---|---:|---:|---:|---|
| PbWO4 (scheelite/stolzite) | I 41/a | 73.90 | 0.27 | `phase_1_PbWO4_scheelite.cif` |
| PbO (massicot) | P b c m | 9.31 | 0.15 | `phase_2_PbO_massicot.cif` |
| WO3 (monoclinic) | P 21/n | 11.67 | 0.25 | `phase_3_WO3_monoclinic.cif` |
| PbO (litharge) | P 4/n m m | 5.12 | 0.13 | `phase_4_PbO_litharge.cif` |

The final Cu Kalpha1/Kalpha2 Rietveld fit over 10.02-99.98 degrees has Rwp = 13.60%, Rp = 9.11%, and GOF = 3.89. The refined common zero offset is 0.309 degrees 2-theta. Only unit cells, phase scales, background, zero, and an effective common peak profile were refined; atomic coordinates and displacement parameters were held to the reference structures because the laboratory powder data do not support reliable unconstrained coordinate refinement.

## Evidence

Scheelite PbWO4 is fixed by its strong series at approximately 27.70, 29.91, 33.05, 45.02, 47.28, 51.48, 55.54, and 56.82 degrees. Monoclinic WO3 accounts for the characteristic low-angle triplet near 23.38, 23.89, and 24.64 degrees and lines near 33.52, 34.44, and 41.92 degrees. Orthorhombic massicot PbO is supported by lines near 29.35, 30.62, 38.12, 49.49, 53.39, 60.54, and 63.28 degrees. Tetragonal litharge PbO is supported independently by lines/shoulders near 17.97, 28.9, 32.10, 36.00, 45.92, and 48.86 degrees. The litharge coordinates were transformed from the published P4/nmm origin-1 setting into GSAS-II's origin-2 setting before refinement.

## Remaining uncertainty

Several positive residual peaks—notably near 25.92, 30.16, and 31.04 degrees—track expected Cu Kbeta positions from the fitted phases. For example, the WO3 Kalpha reflections near 33.51 and 34.43 degrees map to Kbeta near 30.24 and 31.06 degrees. Kbeta was not included because the supplied measurement model specifies only Cu Kalpha1/Kalpha2; these residuals were therefore not converted into chemically implausible extra phases. Peak overlap, the uncalibrated instrumental profile, and correlation of zero/sample displacement with lattice constants make the quoted covariance s.u. values optimistic. A practical systematic uncertainty is about 2-4 wt% for the dominant phase and 1-2 wt% for each minor phase. Structures or fractions below roughly 1-2 wt% cannot be established reliably from this pattern.
