# Powder XRD phase analysis

The pattern is modeled by three crystalline phases, with fractions normalized only over those modeled crystalline phases:

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| Monoclinic WO₃ | P2₁/c | a = 7.69770, b = 7.54228, c = 10.54976, β = 136.14245 | 0.5658 |
| Scheelite CaWO₄ | I4₁/a | a = 5.24603, c = 11.38625 | 0.1214 |
| Calcite CaCO₃ | R-3c | a = 4.99162, c = 17.07669 | 0.3128 |

## Evidence

The chemistry is consistent with partial reaction of the stated CaCO₃ and WO₃ precursors at 500 °C to form CaWO₄. Monoclinic WO₃ accounts for the diagnostic split group near 23.42, 23.90, and 24.67° 2θ and the numerous lower-symmetry reflections throughout the scan. Scheelite CaWO₄ accounts for its characteristic reflections near 18.89, 29.02, and 47.52°, while calcite is required by the strong 29.71° reflection and supporting peaks near 39.72 and 43.47°. Every major Bragg feature is assigned by these three phases; adding another crystalline phase was not supported.

Starting models were COD 2311041 (WO₃), COD 7219229 (CaWO₄), and COD 1547347 (calcite). Cells and symmetry-allowed coordinates were refined, with phase-specific size/microstrain and mild preferred orientation where supported. Coordinate shifts were constrained to the known reference-mismatch range so that weakly determined oxygen coordinates did not absorb profile error. A fresh, no-refinement replay of `final.gpx` reproduces `fit.csv` to numerical precision and gives Rwp = 7.3005% and Rp = 5.3433% over all 8293 points.

## Remaining uncertainty

The three-phase inventory is robust, but the fractions are not independent of background, preferred orientation, microstrain, and displacement parameters. A practical systematic uncertainty is about 2–3 wt% for WO₃ and calcite and about 1–2 wt% for CaWO₄; these are not formal standard uncertainties. The detailed oxygen coordinates and the size/strain decomposition are less reliable than the phase identities, cells, and W-containing frameworks. Calcite's isotropic displacement parameter reached the allowed upper bound, another indication of intensity-parameter correlation. No amorphous content was quantified, so the reported fractions must not be interpreted as absolute bulk fractions if an amorphous component is present.
