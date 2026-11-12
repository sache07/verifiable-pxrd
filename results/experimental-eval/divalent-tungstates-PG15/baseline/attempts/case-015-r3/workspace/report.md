# Crystalline phase analysis

The pattern is best described by three crystalline phases: wolframite ZnWO4, monoclinic gamma-WO3, and wurtzite ZnO. The refined fractions below are normalized to the modeled crystalline material only.

| Phase | Space group | Refined cell (A, degrees) | Crystalline weight fraction |
|---|---|---|---:|
| ZnWO4 (wolframite) | P 2/c | a=4.69132, b=5.72024, c=4.92796, beta=90.6245 | 77.39 +/- 0.55 wt% |
| gamma-WO3 | P 21/n | a=7.30912, b=7.54224, c=7.69204, beta=90.8095 | 15.66 +/- 0.33 wt% |
| ZnO (wurtzite) | P 63 m c | a=3.24983, c=5.20847 | 6.95 +/- 0.57 wt% |

The uncertainties in the table are formal GSAS-II covariance estimates. The values sum to 100.00 wt%.

## Evidence

The dominant peak positions and intensities match monoclinic ZnWO4, the expected reaction product of the stated ZnO and WO3 precursors after heating at 900 degrees C. A ZnWO4-only fit left strong residuals and gave Rwp=19.54%. Adding monoclinic WO3 reduced Rwp to 14.67% and accounts for its characteristic cluster near 23.1-24.3 degrees 2-theta and lines near 26.6, 28.6, and 33-34 degrees. The remaining positive component matches the full wurtzite ZnO sequence, including approximately 31.8, 34.4, 36.3, 47.5, 56.6, 62.8, 67.9, 69.1, and 95.3 degrees. Its nested addition reduced Rwp to 14.42% before final joint refinement; its refined scale remained positive and its cell is chemically sensible. The final model has Rp=10.16%, Rwp=13.59%, Rexp=3.79%, and goodness-of-fit=3.59.

The starting structural models were COD 1520641 (ZnWO4), a reduced P21/n setting derived from COD 2311041 (WO3), and COD 9004178 (ZnO). The refined structures retain plausible Zn-O and W-O coordination. No additional crystalline phase is justified by a reproducible set of unmatched reflections, although a trace phase below the sensitivity of this broad, overlapping pattern cannot be excluded.

## Refinement and limitations

The GSAS-II refinement used the full 9.9034-100.0949 degree range, the metadata Cu Kalpha1/Kalpha2 wavelengths (1.540598/1.544426 A), and the reported 0.5 Kalpha2/Kalpha1 ratio. Since measured pointwise uncertainties and a calibrated instrumental profile were absent, Poisson counting uncertainties were assigned and a fixed empirical instrumental profile was combined with phase-specific isotropic broadening. Refined terms included phase scales and cells, a 12-term Chebyshev background, zero offset, selected X-ray-sensitive heavy-atom coordinates, broadening terms, and a small ZnWO4 [100] March-Dollase correction.

Oxygen coordinates and displacement parameters cannot be determined reliably from these data. Unrestricted oxygen-coordinate trials generated implausibly short bonds, and an ADP trial lowered Rwp only by driving all refined ZnWO4 displacement parameters negative. Those overfit models were rejected. Systematic intensity residuals, especially at higher angle, remain; attempts to absorb them into the unspecified polarization/profile drove parameters outside physical ranges. Consequently, the quoted formal fraction errors are optimistic. A realistic interpretation is about +/-1-2 absolute wt% for the crystalline fractions, with the WO3/ZnO partition the least robust. Without an internal standard, the amorphous fraction cannot be determined.

The submitted CIFs and `fit.csv` were exported directly from the converged `final.gpx` project (41 refined parameters; maximum shift/esd 0.011).
