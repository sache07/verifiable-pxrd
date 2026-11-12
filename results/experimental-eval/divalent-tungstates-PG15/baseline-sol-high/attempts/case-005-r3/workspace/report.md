# PXRD phase analysis

The crystalline pattern is described by two phases. Weight fractions are normalized over those modeled crystalline phases only.

| Phase | Space group | Refined cell | Weight fraction |
|---|---|---|---:|
| Monoclinic WO3 | P 21/c (nonstandard setting) | a = 7.69454 Å, b = 7.53721 Å, c = 10.54659 Å, beta = 136.1558° | 71.49 wt% |
| Spinel Co3O4 | F d -3 m | a = 8.08475 Å | 28.51 wt% |

GSAS-II gives a formal one-standard-deviation uncertainty of 0.17 percentage points on each normalized fraction. This is a counting-statistical/model covariance estimate; systematic uncertainty from the uncalibrated instrumental profile, microabsorption (especially for W-rich WO3), and possible preferred orientation is likely larger.

## Evidence

The intense WO3 triplet at approximately 23.46, 23.95, and 24.71° 2theta, together with the peak groups near 33.6–34.5, 42.2, 50.3, 53.8–55.1, and 56.2°, is matched by monoclinic WO3. The second phase is required by the complete spinel Co3O4 sequence near 19.37, 31.64, 37.20, 38.91, 45.14, 59.68, and 65.56°. In contrast, the diagnostic strong CoWO4 reflection expected near 30.6° is absent. Thus the 500 °C material is predominantly the two crystalline precursors rather than a detectable cobalt-tungstate product.

Starting structural models were COD 2311041 (WO3) and COD 9005896 (Co3O4). Cell parameters, phase scales, sample-height correction, background, and profile terms were refined. Atomic coordinates, occupancies, and displacement parameters were retained from the reference models because this laboratory powder pattern does not independently constrain a full coordinate refinement. The WO3 CIF uses the source's valid but unusual P 21/c cell setting; its formula is equivalent to WO3.

## Fit and uncertainty

The final fit over 10–100° 2theta has Rwp = 3.414%, Rp = 2.427%, Rexp = 1.722%, and goodness of fit = 1.982. The supplied data had no pointwise uncertainties, so sigma = sqrt(counts) was used. The Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio from the metadata were fixed.

No additional crystalline phase is supported by systematic unmatched peaks. A trace phase below the pattern's detection sensitivity cannot be excluded, and no amorphous fraction can be obtained without an internal standard. Therefore the reported fractions are reliable as normalized fractions of the two modeled crystalline phases, but not as absolute whole-sample mass fractions. Crystallite size and microstrain also cannot be determined reliably without a calibrated instrumental profile and were not refined in the final model.

The submitted CIFs, fractions, and calculated profile were all exported from `final.gpx`.
