# Powder XRD phase analysis

## Result

The pattern is modeled by two crystalline phases:

| Phase | Structural model | Refined cell (Å, °) | Crystalline weight fraction |
|---|---|---|---:|
| WO3 | triclinic *P* -1, COD 2106293 | a = 7.31922, b = 7.53647, c = 7.69530; α = 89.5169, β = 90.7169, γ = 90.2694 | 65.46% |
| BaO2 | tetragonal *I*4/mmm, COD 1010113 | a = 3.81489, c = 6.85201 | 34.54% |

Fractions are normalized over these modeled crystalline phases. The data do not provide an absolute amorphous fraction.

## Evidence and refinement

The split low-angle group at approximately 23.4, 23.9 and 24.7° 2θ, followed by the dense higher-angle pattern, selects the low-symmetry WO3 model. A monoclinic WO3 alternative gave a visibly poorer whole-pattern fit. Independent peaks near 26.3, 27.0, 33.5, 42.9, 46.6 and 55.4° are accounted for by tetragonal BaO2. BaWO4 was rejected because its required strong reflections around 31.9–32.5° are absent. No coherent residual peak set requires a third crystalline phase. In the 200 °C synthesis context, the crystalline material is therefore consistent with largely unreacted precursors rather than detectable crystalline BaWO4 product.

The final GSAS-II atomic-model replay gives Rwp = 7.190%, Rp = 5.399%, and goodness of fit = 1.977 (Poisson-limit Rwp = 3.641%). The supplied `fit.csv` was regenerated from `final.gpx`; no stored calculated profile was reused. Cu Kα1/Kα2 wavelengths and their 0.5 intensity ratio were fixed to the metadata. A +0.25° zero term and -78.6 µm specimen displacement were used.

## Remaining uncertainty

Phase identity is substantially more reliable than individual oxygen coordinates. Atomic shifts were restricted to a small neighborhood of the database models (oxygen RMS shift about 0.05 Å for WO3), and isotropic displacement parameters were fixed; the CIFs should therefore be treated as profile-compatible structural models, not independent high-precision coordinate determinations. The BaO2 model contains a 1.368 Å O-O peroxide pair. Its exact length is especially weakly constrained by X-ray data and is short relative to many ambient-pressure peroxides, so that oxygen coordinate should not be interpreted as a precise bond-length measurement.

Zero, specimen displacement and lattice scale are strongly correlated. Consequently, the reported unit-cell parameters have additional systematic uncertainty not represented by least-squares standard errors. Phase fractions were stable across the tested structural/profile variants; a conservative model uncertainty is about ±2 percentage points for each fraction. The residual Rwp above the counting-statistics limit indicates remaining line-shape/background mismatch, but no additional crystalline phase can be assigned reliably from it.
