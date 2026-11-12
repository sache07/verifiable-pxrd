# Powder XRD phase analysis

The 800 °C product from WO3 and BaCO3 contains three modeled crystalline phases. Fractions are normalized over those phases; no amorphous or unmodeled mass is included.

| Phase | Structural model | Crystalline weight fraction |
|---|---|---:|
| Ba3W2O9 | R-3c, COD 1533878 parent | 0.71888 |
| WO3 | P21/c, COD 2311041 parent | 0.22996 |
| BaCO3 | Pnma, COD 9010928 parent | 0.05116 |

## Evidence

Ba3W2O9 accounts for the dominant broadened reflection families near 16.4, 17.7, 26.2, 27.7, 30.8, 33.0, 37.6, 40.8 and 43.0° 2theta. Monoclinic WO3 accounts for the remaining sharp/intermediate oxide reflections, while orthorhombic BaCO3 accounts for the distinct sharp family including peaks near 19.7, 24.1, 34.8 and 42.2°. Every coherent residual family was assigned to one of these phases; adding BaWO4 or another phase was not supported.

For WO3, symmetry-diverse exact-composition references were compared after equivalent cell, coordinate, Uiso and texture development. COD 2311041 gave the physical winning basin (comparison Rwp 4.26%, versus 5.67% for COD 1528915); two other starts reached coordinate/Uiso bounds and were rejected. A P21/m start failed numerically and therefore remained unknown rather than being treated as a scientific rejection. Search stopped after the three accepted phases indexed all coherent families.

The final bounded polish selected its converged heavy-then-light coordinate branch with no frozen variables, short contacts, or fraction collapse. The final saved-project statistics are Rwp = 3.1187%, Rp = 2.2645%, and GOF = 1.3579. A fresh native GSAS-II replay optimized zero parameters, left `final.gpx` unchanged, and returned no profile-review flags; its complete-grid Rwp is 3.1192%.

## Uncertainty

Phase identities and the dominant/minor ordering are reliable. Reported covariance errors are conditional on this model and do not capture reference, background, texture, or microabsorption systematics; this is especially relevant to the approximately 5.1 wt% BaCO3 fraction. Oxygen and carbonate-group coordinates are less strongly determined by laboratory X-ray data than the cation framework, although the accepted bounded coordinates retain physical geometry. Fractions are crystalline-only, so an amorphous fraction, if present, cannot be determined from this refinement without an internal standard.
