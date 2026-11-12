# PXRD phase analysis

The pattern is described by two crystalline phases, normalized to **69.24 wt% triclinic WO3** and **30.76 wt% CoWO4**. The final full-range refinement (9.9034–100.0949 degrees 2-theta, 8,301 points) gives `Rwp = 6.10%`, `Rp = 4.67%`, `Rexp = 3.28%`, and goodness-of-fit `1.86`.

| Phase | Refined structure | Crystalline weight fraction |
|---|---|---:|
| WO3 | triclinic `P -1`; a = 7.30627, b = 7.53548, c = 7.69180 Å; alpha = 89.7604, beta = 90.7896, gamma = 90.1839 degrees | 69.24 wt% |
| CoWO4 | monoclinic `P 2/c`; a = 4.66833, b = 5.68342, c = 4.94941 Å; beta = 89.9998 degrees | 30.76 wt% |

## Evidence

The WO3 assignment accounts for the characteristic 23.17/23.67/24.41-degree triplet and peaks near 33.35, 34.21, 41.48, 50.00, and 55.98 degrees. CoWO4 is required by its strong 30.70-degree line and the supporting peaks near 19.04, 36.46, 54.16, 61.81, and 65.13 degrees. A detailed triclinic WO3 reference model (COD 2106293) consistently outperformed a monoclinic WO3 alternative in matched refinements (`Rwp` about 6.21% versus 6.58% before the final CoWO4 cation-coordinate adjustment); the refined alpha and gamma angles also remain significantly different from 90 degrees.

CoO and Co3O4 were explicitly tested as possible precursor/oxidation residues. Co3O4 refined to zero. Fixed-cell CoO did not improve the converged fit; allowing its cell to float only absorbed overlapping profile residuals and required an implausibly expanded cell. Neither is therefore reported as a determined phase. Trace phases below roughly 1–2 wt% cannot be excluded.

## Refinement and uncertainty

GSAS-II used the supplied Cu K-alpha1/K-alpha2 wavelengths and fixed 0.5 intensity ratio, Poisson counting weights, a 15-term Chebyshev background, refined phase scales and cells, one common Gaussian width term, and phase-specific isotropic size broadening. The symmetry-allowed Co and W y coordinates in CoWO4 were refined; oxygen coordinates and the detailed WO3 coordinates were held to literature values because this laboratory powder pattern does not determine them reliably.

The formal least-squares fraction uncertainty is 0.18 wt% for each phase, but it excludes model and instrument-profile uncertainty. Comparison across defensible WO3/profile models suggests a more realistic uncertainty of about **±2 wt%**. Fractions are normalized only over the modeled crystalline material; without an internal standard, amorphous content cannot be quantified. Crystallite-size values are not interpreted because no calibrated instrumental profile was supplied.
