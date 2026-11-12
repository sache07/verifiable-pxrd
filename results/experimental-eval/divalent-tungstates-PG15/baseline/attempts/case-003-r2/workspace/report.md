# PXRD phase analysis

The crystalline portion is modeled as **54.62 wt% monoclinic WO3**, **33.78 wt% calcite (CaCO3)**, and **11.60 wt% scheelite (CaWO4)**. Fractions are normalized over the modeled crystalline phases; the measurement has no internal standard, so an amorphous fraction cannot be determined.

| Phase | Space group | Refined cell | Crystalline wt% |
|---|---|---|---:|
| WO3 | P 21/c | a = 7.6913 Å, b = 7.5357 Å, c = 10.5406 Å, beta = 136.1456° | 54.62 |
| Calcite, CaCO3 | R -3 c | a = 4.9873 Å, c = 17.0641 Å | 33.78 |
| Scheelite, CaWO4 | I 41/a | a = 5.2420 Å, c = 11.3802 Å | 11.60 |

## Evidence and refinement

The precursor context and 500 °C treatment are consistent with partial reaction of CaCO3 and WO3 to CaWO4. The observed pattern contains the diagnostic monoclinic WO3 group near 23.42, 23.90, and 24.67° 2theta, the dominant calcite reflection near 29.71°, and distinct scheelite CaWO4 reflections near 18.91 and 29.02°. Whole-pattern screening favored COD 2311041 for WO3, COD 1547347 for calcite, and COD 7219229 for scheelite. Adding plausible fourth phases produced only non-unique contributions of about 0.2 wt% and no independent residual-peak set, so no fourth phase is reported.

The GSAS-II model uses the stated Cu Kalpha1/Kalpha2 wavelengths and intensity ratio, Poisson counting weights, a 12-term Chebyshev background, specimen displacement, refined phase scales and lattice parameters, and global U/V/W/X/Y peak-profile terms. Calcite required March-Dollase (104) preferred orientation (r = 0.780). The broader CaWO4 peaks required an isotropic coherent-domain size of about 0.050 micrometres. Atomic coordinates were retained from the source structures because coordinate/ADP refinement was unstable and strongly correlated at laboratory resolution. The final profile gives Rwp = 8.381%, Rp = 6.135%, and goodness of fit = 3.504.

## Uncertainty

The three phase identities are well supported, but the exact WO3 distortion is less secure than the chemical assignment: a triclinic WO3 model was a close, though poorer, alternative in screening. The reported fractions are not reliable to their displayed decimal precision because calcite texture and CaWO4 broadening correlate with scale. A model without phase-specific CaWO4 broadening gave approximately 55.7/36.0/8.3 wt% (WO3/calcite/CaWO4), compared with 54.6/33.8/11.6 wt% here. Reasonable model-dependent uncertainties are therefore about ±2 wt% for WO3, ±3 wt% for calcite, and ±3.5 wt% for CaWO4; these are sensitivity estimates, not one-sigma statistical errors. A trace fourth phase below roughly 0.3–0.5 wt% cannot be identified or quantified reliably from this pattern.

`final.gpx` is the project used to generate the submitted CIFs, fractions, and `fit.csv` profile.
