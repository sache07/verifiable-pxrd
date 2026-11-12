# Powder XRD phase analysis

## Result

The pattern is described by two crystalline phases. Weight fractions are normalized over these modeled crystalline phases only.

| Phase | Structure | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| WO₃ | monoclinic, P 2₁/c (alternate setting) | a = 7.70076, b = 7.54352, c = 10.55532, β = 136.1547 | 0.7504(28) |
| Co₃O₄ | cubic spinel, Fd-3m | a = 8.09150 | 0.2496(28) |

The full-range GSAS-II refinement (10–100° 2θ, Cu Kα₁/Kα₂ = 1.540598/1.544426 Å with the reported 0.5 intensity ratio) gives Rwp = 3.168%, Rp = 2.271%, Rexp = 1.722%, and goodness of fit = 1.843 for 8,301 points and 31 refined parameters.

## Evidence and model choice

The dominant monoclinic WO₃ model accounts for the resolved 23.5–24.7° triplet and the many split high-angle families. The spinel Co₃O₄ model independently accounts for its characteristic reflections near 19.4, 31.6, 37.2, 38.9, 45.2, 59.7, and 65.6° 2θ. Starting structures were frozen-index COD entries 2311041 (WO₃) and 9005896 (Co₃O₄), followed by cell, scale, profile, and limited coordinate refinement. A close triclinic WO₃ alternative did not improve the fit. The selected WO₃ model retains physical octahedral W–O distances of 1.74–2.13 Å; Co₃O₄ has physical tetrahedral/octahedral Co–O distances near 1.92–1.93 Å.

A chemically plausible wolframite CoWO₄ P2/c trial had its stable positive scale driven to the numerical floor, and its diagnostic reflection family was absent. After fitting WO₃ and Co₃O₄, the largest residuals coincide with already modeled strong reflections and reflect imperfect relative intensities/line shape; no coherent residual family remains in regions where the calculated crystalline signal is weak. CoWO₄ therefore has no reliably determinable nonzero fraction and is not included in the phase inventory.

The refinement used count-statistical weights because pointwise uncertainties were not supplied. Instrument/profile terms, sample displacement, a uniaxial WO₃ microstrain term, heavy-atom coordinates, and the Co₃O₄ oxygen coordinate were refined conservatively. WO₃ oxygen coordinates were retained from the reference because free refinement was unstable; a common fixed Uiso = 0.006 Å² was selected from a bounded physical scan. Terms that reached justified profile limits were fixed before the final converged replay. The final maximum shift/e.s.d. is 0.12.

## Remaining uncertainty

The reported fraction e.s.d. is the formal GSAS-II value (about 0.28 weight-percentage point). Profile, displacement-parameter, and reference-structure correlations make a systematic uncertainty of roughly 1–2 percentage points more realistic. A trace phase below approximately 0.5–1 wt% cannot be excluded from these data. No internal standard was present, so the fractions do not quantify amorphous material or total crystalline content.

The submitted CIFs, profile, fractions, and statistics were all exported from `final.gpx`.
