# Powder X-ray diffraction phase analysis

## Result

Three crystalline phases are required by the pattern. The quantitative result is normalized over those modeled crystalline phases:

| Phase | Space group | Weight percent | Formal 1σ (wt.%-points) | Structural model |
|---|---:|---:|---:|---|
| γ-WO₃ | P 21/c | 58.34 | 0.22 | [WO3_gamma_monoclinic.cif](WO3_gamma_monoclinic.cif) |
| Calcite CaCO₃ | R -3 c | 29.07 | 0.26 | [CaCO3_calcite.cif](CaCO3_calcite.cif) |
| Scheelite CaWO₄ | I 41/a | 12.59 | 0.12 | [CaWO4_scheelite.cif](CaWO4_scheelite.cif) |

The monoclinic WO₃ CIF uses the valid nonstandard *P*2₁/*c* cell inherited from COD 2311041 (β ≈ 136.143°); it is an alternative setting of room-temperature γ-WO₃.

## Evidence and refinement

The phase assignments are supported by complete peak families, not single lines: the dominant γ-WO₃ multiplet near 23.4–24.7° 2θ and its dense higher-angle pattern; calcite peaks near 29.7, 36.3, 39.7, 43.5 and 64.9°; and scheelite CaWO₄ peaks near 18.9, 29.0 and 31.7°. These phases are chemically consistent with partial reaction of the supplied CaCO₃ and WO₃ precursors at 500 °C. Preliminary two-phase fits were much worse (best Rwp 16.75%, versus 7.467% here), and the final residual contains no coherent family requiring another crystalline phase.

The fit used the reported Cu Kα₁/Kα₂ wavelengths and 0.5 intensity ratio, Poisson estimates σ = √counts because pointwise uncertainties were absent, a 12-term Chebyshev background, and 8284 points over nominal 10–100° 2θ. Refined terms included phase scales and cells, common zero, phase-dependent size/strain, a March–Dollase calcite (104) texture term, and constrained W positions plus common W/O isotropic displacement terms in WO₃. Oxygen coordinates and the CaWO₄/CaCO₃ atomic coordinates were held at their reference values because this overlapped laboratory pattern did not determine them robustly. Final statistics are Rwp = 7.467%, Rp = 5.539%, Rexp = 2.394%, and goodness-of-fit = 3.127.

## Remaining uncertainty

The tabulated 1σ values are covariance-only precision estimates and are smaller than the true uncertainty. There was no calibrated instrumental profile or external/internal standard; physically plausible profile and texture choices move the fractions by several weight-percentage points. Thus the phase identities and three-phase requirement are reliable, while the reported fractions should be treated as approximate (roughly a few wt.%-points systematic uncertainty). The analysis cannot quantify amorphous material, and a trace crystalline phase below the residual/model-error level cannot be excluded. Fractions therefore sum to 100% only over the three modeled crystalline phases.

The submitted profile is [fit.csv](fit.csv), and the exact project used for all values and CIF exports is [final.gpx](final.gpx).
