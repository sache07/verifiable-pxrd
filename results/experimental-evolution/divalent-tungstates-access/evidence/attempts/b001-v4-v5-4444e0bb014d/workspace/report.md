# Powder XRD phase analysis

## Result

The pattern is described by three crystalline phases. Weight fractions are normalized over those modeled crystalline phases; no amorphous fraction was measured.

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| CaWO₄, scheelite | *I* 4₁/*a* | *a* = 5.23717, *c* = 11.33302 | 79.23(25)% |
| WO₃, monoclinic | *P* 2₁/*c* | *a* = 7.69381, *b* = 7.55682, *c* = 10.51763, β = 135.9473 | 13.567(60)% |
| CaCO₃, calcite | *R* -3 *c* | *a* = 4.98915, *c* = 17.05362 | 7.20(28)% |

The full-grid refinement used all 8,301 points from 9.9034–100.0946° 2θ with the supplied Cu Kα₁/Kα₂ doublet. Final statistics are Rwp = 3.2149%, Rp = 2.4934%, Rexp = 3.1382%, and GOF = 1.0265. The standardized difference has RMS 1.024, close to counting noise.

## Evidence

- Scheelite CaWO₄ accounts for the dominant families, including the reflections near 18.27, 28.42, 31.21, 33.85, 38.91, and 46.89° 2θ. Its refined oxygen position gives W–O = 1.787 Å and Ca–O = 2.433–2.453 Å.
- Monoclinic WO₃ accounts for the characteristic 22.76/23.18/23.99° triplet and its higher-angle families. Exact-composition WO₃ references were compared; the physical *P* 2₁/*c* model derived from COD 2311041 gave the best broad-family match without short contacts. Refined W–O distances are 1.722–2.157 Å.
- Residual families near 29.0, 35.6, 39.1, 42.8, 48.2, and 64.3° are explained by calcite. The resulting inventory is chemically consistent with partial reaction of the stated CaCO₃ and WO₃ precursors at 650 °C. No coherent residual reflection family requires a fourth crystalline phase.

## Remaining uncertainty

The quoted uncertainties are formal GSAS-II standard uncertainties and do not include all model systematics. Calcite is broad and weak; its microstrain reached the allowed 8,000 ppm ceiling and was then held fixed, so its 7.2 wt% fraction is more profile/background-dependent than the formal uncertainty suggests. Treat that uncertainty as a lower bound.

The WO₃ topology and fraction are reliable, but its internal coordinates are less strongly constrained because it is a minority phase with overlapping peaks. A bounded tungsten-coordinate adjustment was retained because it improved the full-family intensities and kept physical geometry; WO₃ oxygen-coordinate refinement was rejected as under-supported. Calcite coordinates were likewise kept at the physical reference values after a free oxygen trial produced an implausibly short carbonate bond. A surface-roughness branch was rejected because both parameters hit their limits and were 99.99% correlated.

The final project is `final.gpx`; phase structures are `CaWO4.cif`, `WO3.cif`, and `CaCO3_calcite.cif`. The observed/calculated/difference profile is `fit.csv`, and machine-readable fractions and fit statistics are in `result.json`.
