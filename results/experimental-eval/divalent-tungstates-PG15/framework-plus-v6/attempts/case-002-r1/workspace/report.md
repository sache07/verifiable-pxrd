# Powder XRD phase analysis

The pattern is modeled as two crystalline phases:

| Phase | Space group | Refined cell (Å, °) | Crystalline weight fraction |
|---|---|---|---:|
| BaO₂ | *I4/mmm* | 3.81251, 3.81251, 6.84736; 90, 90, 90 | 0.3326 |
| WO₃ | *P*−1 | 7.31445, 7.53280, 7.69066; 89.531, 90.715, 90.282 | 0.6674 |

These fractions are normalized over the modeled crystalline material. There was no internal standard, so amorphous content and absolute crystalline yield cannot be determined.

## Evidence

The triclinic WO₃ model (COD 2106293) accounts for the characteristic split low-angle family near 23.4, 23.9, and 24.7° 2θ and the corresponding split families throughout the middle- and high-angle ranges. Monoclinic, orthorhombic, and tetragonal WO₃ records were compared under the same background/profile treatment and gave systematically poorer peak-position and intensity agreement.

Tetragonal BaO₂ (COD 1010113) accounts coherently for the families near 26.3, 27.1, 33.5, 43.0, 46.6, and 55–56° 2θ. This is chemically consistent with the BaO₂ + WO₃ precursors and the low reported treatment temperature of 200 °C. A modest BaO₂ March–Dollase correction was supported by several separated families, although the exact texture axis is weakly determined.

BaWO₄, BaO, BaCO₃, Ba(OH)₂, Ba₃W₂O₉, and reduced tungsten oxides were challenged as possible minor phases. BaWO₄ and BaO refined to about 0.16 wt% each without a meaningful unique-family improvement; Ba₃W₂O₉ worsened the fit. BaCO₃ could borrow overlapped intensity, but its diagnostic families were absent and a free-cell trial required implausible cell distortion. These phases were therefore excluded rather than reported as false precision.

## Refinement and fit

The peroxide internal coordinate and the X-ray-visible W coordinates were refined within the parent structures; WO₃ oxygen coordinates were retained from the physically screened parent because this laboratory X-ray pattern does not determine all 36 light-atom positional parameters reliably. One isotropic displacement parameter was used per phase. The final background is a smooth, positive 12-coefficient Chebyshev function. One specimen-displacement correction, fixed nonnegative common profile terms, isotropic size terms, WO₃ [100] uniaxial broadening, and weak BaO₂ texture were used. Roughness and additional texture/broadening terms were rejected when they behaved as scale/background surrogates or were not replay-stable.

An independent atomic forward replay of `final.gpx` over all 8301 measured points gives Rwp = 7.038%, Rp = 5.267%, χ² = 31020.13, and GOF = 1.935 using weights 1/max(*I*obs, 1). The replay background remains positive (184–2441 counts), and no negative analytic peak widths or other replay profile flags occur. `fit.csv` is the replayed observed/calculated/difference profile, not a stale project curve.

## Remaining uncertainty

The fractions are robust to the accepted profile alternatives at roughly ±0.02 absolute (about ±2 percentage points, anti-correlated between the two phases). The exact instrument-versus-size-versus-strain decomposition is not identifiable without a calibration standard and should not be interpreted as a microstructure measurement. Trace crystalline phases below approximately 1–2 wt% cannot be excluded reliably.

The refined BaO₂ model contains an O–O distance of 1.468 Å. A generic oxide contact screen flags this for review, but it is the intended peroxide O₂²⁻ bond rather than an atomic clash. The WO₃ geometry passes the contact screen. The WO₃ framework assignment and cell are reliable; its individual oxygen coordinates are parent-model values and are not independently established by this pattern.
