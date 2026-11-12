# Powder XRD phase analysis

## Result

The pattern is described by two crystalline phases:

| Phase | Space group | Refined cell (Å, °) | Crystalline weight fraction |
|---|---|---|---:|
| CaWO4, scheelite | I 41/a (No. 88) | a = 5.23512, c = 11.32852 | 85.33 wt% |
| WO3, monoclinic | P 21/c (No. 14, alternate setting) | a = 7.68769, b = 7.55073, c = 10.50873, beta = 135.94321 | 14.67 wt% |

Fractions are normalized over the modeled crystalline phases. No external standard was supplied, so an amorphous fraction cannot be measured from this dataset.

The final full-grid fit has Rwp = 3.8738%, Rp = 2.9214%, Rexp = 3.1382%, and goodness-of-fit = 1.2361 over 8301 points. Because pointwise uncertainties were not supplied, raw counts were treated with Poisson weights (w = 1/Iobs). In `fit.csv`, difference is observed minus calculated intensity.

## Evidence and model choice

The dominant family at 18.271, 28.420, 31.223, 33.853, 46.882, and 57.650° 2theta indexes as tetragonal scheelite CaWO4. The diagnostic secondary triplet at 22.758, 23.182, and 23.975° and its higher-angle companions index as room-temperature monoclinic WO3. This is chemically consistent with partial reaction of the reported WO3 and CaCO3 precursors at 650 °C. The characteristic strongest calcite line near 29.4° and the CaO family are absent. Remaining residual extrema coincide with profiles of the two accepted phases or smooth background curvature; they do not form a coherent third reflection family.

Starting structures were the exact-composition frozen COD references 7219229 (CaWO4) and 2311041 (WO3). A physical triclinic WO3 alternative gave a worse complete two-phase fit, while another monoclinic reference was rejected because it contained severely under-coordinated W. The accepted structures retain physical coordination: scheelite W–O is about 1.80 Å and Ca–O is 2.42–2.44 Å; monoclinic WO3 contains distorted WO6 units with W–O about 1.68–2.20 Å.

Cells, calibration, scales, smooth background, peak profile, phase size/microstrain, CaWO4 oxygen position, and WO3 tungsten positions were refined in staged bounded passes. Common isotropic displacement parameters were selected by a bounded physical scan (0.0104 Å² for CaWO4 and 0.0030 Å² for WO3). Free refinement of the weakly constrained WO3 oxygen positions produced nonphysical short bonds and was rolled back to the published oxygen framework. Texture, anisotropic strain, and surface-roughness terms were tested but did not have adequate support.

## Remaining uncertainty

The covariance-only fraction uncertainty is about 0.053 wt%, but that excludes model and calibration uncertainty. A practical uncertainty of roughly ±1 wt% per phase is more defensible; the phase identities and major/minor assignment are robust. The WO3 oxygen coordinates and its Uiso (which reached the lower physical scan bound) are not independently determined reliably by this W-dominated laboratory pattern. The angular zero reached its allowed boundary and is correlated with specimen displacement and cell dimensions, so the reported cells should not be treated as high-accuracy metrology. Trace crystalline phases below the pattern's detection capability, and any amorphous material, cannot be excluded.
