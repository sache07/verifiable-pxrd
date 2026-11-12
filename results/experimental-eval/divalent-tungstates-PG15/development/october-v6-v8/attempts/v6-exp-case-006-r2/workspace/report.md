# PXRD phase analysis

The modeled crystalline product is **97.864(54) wt% triclinic CuWO4** (wolframite type, `P -1`) and **2.136(54) wt% monoclinic WO3** (`P 21/c`). Fractions are normalized over these modeled crystalline phases.

| Phase | Refined cell | Crystalline weight fraction |
|---|---|---:|
| CuWO4, `P -1` | a = 4.70706 Å, b = 5.84097 Å, c = 4.88008 Å; α = 91.6550°, β = 92.5337°, γ = 82.7496° | 0.978644(541) |
| WO3, `P 21/c` | a = 7.68497 Å, b = 7.53926 Å, c = 10.51685 Å; β = 136.0601° | 0.021356(541) |

## Evidence and refinement

The dominant peak set is explained throughout the scan by an atomistic triclinic CuWO4 model. Its cell and all independent atomic coordinates were refined; the exported structure has full occupancies, sensible Cu–O/W–O contacts, and no CIF-audit flags. The WO3 model improves several distinct residual features, including lines near 23.4°, 24.7°, 34.5°, and 50.2° 2θ. Removing WO3 raises Rwp from 6.640% to 7.221%, so its scale is not overlap-only.

The final nuisance model uses sample displacement, global U/V/X peak-width terms, refined polarization, and a weak CuWO4 [001] March–Dollase correction (ratio 0.9837). Surface roughness was rejected because its two parameters became 99.7% correlated and one became negative. Phase size and microstrain refinements returned neutral, negative, or negligible values and were omitted. The joint zero/displacement branch was rejected at 0.99993 correlation; displacement alone was retained. Final GSAS-II statistics are Rwp = 6.640%, Rp = 4.777%, Rexp = 2.434%, and GOF = 2.736. The regenerated full-grid profile in `fit.csv` has Rwp = 6.634%.

## Remaining uncertainty

The WO3 chemical assignment is secure, but its exact low-temperature polymorph/setting is less secure at only ~2 wt%: a triclinic WO3 alternative was close in whole-pattern fit but did not give a stable complete replay, while orthorhombic WO3 was clearly worse. WO3 coordinates and source displacement parameters were therefore not refined. The quoted fraction uncertainties are formal GSAS-II standard uncertainties and do not include this model uncertainty.

A source-cell CuO test corresponded to about 0.18 wt% but changed Rwp by only ~0.0015 percentage point. Allowing its cell to drift produced a larger, localized gain but an implausible cell shift and absent-prediction penalties, so CuO is not reliably established and no CuO fraction is reported. Residuals are concentrated mainly at the strongest CuWO4 reflections rather than as a coherent unmatched peak family.

No internal standard was supplied, so amorphous material and absolute crystalline content cannot be determined. Pointwise uncertainties were also absent; count-based weights were used. Both submitted CIFs pass composition, occupancy, symmetry, duplicate-site, and contact screening, and `final.gpx` passes convergence, regenerated-profile, and positive-width audits.
