# Powder XRD phase analysis

The modeled crystalline material contains two phases:

| Phase | Refined model | Weight fraction |
|---|---|---:|
| monoclinic γ-WO₃ | P2₁/n (No. 14), a = 7.3174 Å, b = 7.5350 Å, c = 7.6918 Å, β = 90.7239° | 0.68777 (68.78 wt%) |
| tetragonal BaO₂ | I4/mmm (No. 139), a = 3.8150 Å, c = 6.8485 Å | 0.31223 (31.22 wt%) |

Fractions are normalized over these modeled crystalline phases; no amorphous fraction was measured. Their covariance-only 1σ uncertainty is 0.13 percentage point, but profile/background/texture choices dominate, so about ±1 wt% is a more realistic precision.

## Evidence

The γ-WO₃ model reproduces the diagnostic split low-angle family at 23.419°, 23.905°, and 24.619° 2θ and its many independent middle- and high-angle families. The BaO₂ model accounts for the 002, 101, and 110 peaks at 26.308°, 27.034°, and 33.486°, as well as the distinct 46.601°/47.924° pair. Alternate monoclinic WO₃ records were tested; COD 1528915 gave the coherent triplet and whole-pattern cell solution. COD 1010113 supplied the BaO₂ peroxide structure.

A clean common profile used both Cu Kα wavelengths, one specimen-displacement correction (−552 µm), positive interior U/W/X values of 35/4/5.5, and a smooth positive 12-term background. Broad peaks required phase size/strain terms; the approximate coherent sizes are 0.110 µm for WO₃ and 0.077 µm for BaO₂. Phase-by-phase trials supported high strain amplitudes (WO₃ [001] uniaxial 8,000/10,027 ppm and BaO₂ isotropic 8,000 ppm), which were then fixed. Reproducible March–Dollase terms were retained for WO₃ [111] (0.917) and the tetragonally equivalent BaO₂ [100]/[010] family (1.105). Size and strain are strongly correlated and sit at the high end of the physical range, so they should not be interpreted as precise microstructural measurements.

The source structures were allowed only small, symmetry-preserving coordinate changes within the stated source-mismatch envelope. Free coordinates were rejected because they drove oxygen sites by as much as ~1 Å. The submitted model uses element-wise RMS shifts of 0.050 Å for WO₃ oxygen, 0.030 Å for W, and 0.050 Å for the sole BaO₂ oxygen coordinate. The necessary geometry screen has no impossible hard contacts. It flags short O–O distances inherited from the source topology: 1.617 Å in WO₃ and the intentional 1.415 Å peroxide bond in BaO₂. These small refined coordinates are prior-limited and are less reliable than the phase identities and cells.

Scheelite BaWO₄ was re-challenged after rebuilding the common profile. Its scale repeatedly converged to only about 0.5 wt%, mostly from overlapped lines, while adding its strongest unique 200 line at 31.85° where no corresponding peak is present and worsening that local residual. It was therefore excluded. Sub-percent BaWO₄ cannot be ruled out, but neither its presence nor a fraction can be reported reliably.

## Fit and verification

The read-only GSAS-II atomic replay covers all 8,301 original points from 9.9034° to 100.0949°: Rwp = 8.263%, Rp = 6.071%, Rexp = 3.641%, and goodness of fit = 2.273. Calculated intensity and background are nonnegative. The replay reported no profile-review flags, did not modify the project, and the submitted CIFs match its GSAS-II exports exactly.
