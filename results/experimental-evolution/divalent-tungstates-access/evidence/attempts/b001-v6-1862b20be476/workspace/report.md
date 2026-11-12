# Powder X-ray diffraction phase analysis

The 700 °C CuO–WO3 specimen is a four-phase crystalline mixture. Quantitative results, normalized over the modeled crystalline phases, are:

| Phase | Structural model | Weight fraction |
|---|---|---:|
| CuWO4 | triclinic `P -1`, COD 4000806 | 64.208(30)% |
| WO3 | monoclinic `P 21/c`, COD 2311041 | 20.069(23)% |
| Cu3WO6 | cubic `P a -3`, COD 1527404 | 13.436(22)% |
| CuO | monoclinic `C 2/c`, COD 1011194 | 2.287(20)% |

The parenthetical values are one-standard-uncertainty estimates in the last shown digits from the final least-squares covariance matrix. They are conditional counting/model uncertainties, not complete systematic error estimates.

## Evidence

Reference screening began with the chemically ordinary CuWO4 product and residual WO3/CuO precursors. Their joint fit left coherent reflection families near 15.2, 19.8, 32.5, 33.8, 49.7, and 57.6° 2theta; these are jointly indexed by cubic Cu3WO6. The remaining weak family at approximately 35.1, 38.3, 48.4, 52.9, 58.1, 61.2, and 65.3° supports residual CuO. No coherent unassigned reflection family remains in the final difference curve.

Exact-composition alternatives were tested. Triclinic CuWO4 (COD 4000806) was decisively better than the tested `P 2/c` model (COD 4000807). The selected WO3 model (COD 2311041) outperformed the other tested WO3 polymorphs. Two monoclinic CuO descriptions fit almost identically; the ordinary higher-symmetry `C 2/c` model was retained. Texture trials were negligible, while uniaxial microstrain along [100] for CuWO4 had broad peak-family support and was retained.

The final four-phase Rietveld model fits all 8,301 observations from 9.9034 to 100.0946° 2theta with `Rwp = 2.7827%`, `Rp = 2.1479%`, and goodness of fit `1.7247`. A fresh GSAS-II atomic forward replay, ignoring saved calculated arrays, reproduced `Rwp = 2.7827%`, the phase fractions above, and reported no profile-audit flags. The one-time staged polish reduced Rwp from 4.1232% while changing every phase fraction by less than 0.18 percentage point. Its geometry audit found no catastrophic contacts; representative shortest bonds are W–O 1.72–1.75 Å and Cu–O 1.91–1.95 Å.

## Remaining uncertainty

The existence and approximate abundance of all four phases are well supported. The exact low-symmetry distortion of the 2.3 wt% CuO component cannot be distinguished reliably from the close `Cc` alternative by this powder pattern alone, so its `C 2/c` assignment should be regarded as the parsimonious model rather than a unique symmetry determination. The reported fractions exclude amorphous material and any crystalline component below the pattern's detection/discrimination limit; the very small covariance uncertainties therefore understate uncertainty from structural choice, peak overlap, absorption, and specimen effects.

`final.gpx`, all submitted CIFs, and `fit.csv` were exported from the same accepted polished project.
