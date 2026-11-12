# Powder X-ray diffraction phase analysis

The pattern is modeled by two crystalline phases, normalized over crystalline material:

| Phase | Space group | Weight fraction |
|---|---:|---:|
| CuWO4 | P -1 | 0.97230 (97.230 wt%) |
| WO3 | P 21/c | 0.02770 (2.770 wt%) |

The dominant peak positions and intensities identify ambient triclinic CuWO4. A P -1 framework derived from the isostructural Cu/Zn tungstate entry COD 2101690 was converted to CuWO4, then its cell and fractional coordinates were refined. The refined cell is a = 4.709740, b = 5.844525, c = 4.883083 A, alpha = 88.3466, beta = 92.5326, gamma = 97.2475 degrees. The resulting coordination is chemically sensible (shortest Cu-O 1.918 A and W-O 1.782 A).

Residual reflections near 23.43, 23.96, 24.68, 26.92, 33.56, 34.47, and 50.17 degrees 2-theta require monoclinic WO3. The submitted P 21/c model starts from COD 2311041; its cell and scale were refined in an equivalent nonstandard setting (a = 7.304591, b = 7.539549, c = 10.526603 A, beta = 133.0592 degrees). Explicit CuO, Cu2WO4, Cu3WO6, and alternative CuWO4-polymorph trials did not retain a significant positive scale. Thus there is no reliable evidence for another resolved crystalline phase, although trace material below the diffraction detection limit cannot be excluded.

GSAS-II Rietveld refinement used the supplied Cu K-alpha doublet, the complete 8301-point scan, Poisson count weights, a smooth background, and anisotropic microstrain broadening for CuWO4. The independently regenerated atomic-model profile gives Rwp = 3.5097%, Rp = 2.7587%, goodness of fit = 1.4495, and chi-square = 17269.59. The replay found no negative background, negative analytic width, or displacement-parameter flags. In `fit.csv`, difference means observed minus calculated intensity.

The quoted fractions are crystalline-phase-normalized and do not measure any amorphous content. Their formal GSAS-II standard uncertainty is about 0.05 wt percentage point, but profile/background correlation makes a conservative uncertainty of roughly 0.5 wt percentage point more realistic for the minor WO3 amount. At only 2.77 wt%, the WO3 polymorph/cell assignment is supported by its diagnostic peaks, but its individual atomic coordinates cannot be refined reliably from this pattern; the submitted coordinates are therefore literature-constrained, and closely related monoclinic WO3 coordinate variants are not distinguishable here.
