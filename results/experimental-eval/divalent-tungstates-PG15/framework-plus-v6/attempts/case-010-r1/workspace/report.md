# Powder XRD phase analysis

## Result

The pattern is modeled by four crystalline phases. Fractions are normalized over these modeled crystalline phases; without an internal standard they do not measure any amorphous content.

| Phase | Structural model | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| WO₃ | triclinic *P* -1, COD 2106293 | 7.30559, 7.53749, 7.69372; 89.9386, 90.6756, 89.9235 | 0.71045 |
| α-Mn₂O₃ | orthorhombic *Pbca*, COD 1514103 | 9.41863, 9.41192, 9.41024 | 0.27198 |
| MnWO₄ | wolframite, monoclinic *P* 2/*c*, COD 1520200 | 4.79830, 5.70800, 4.97470; β = 91.1240 | 0.00491 |
| β-MnO₂ | rutile, tetragonal *P* 4₂/*mnm*, COD 1514110 | 4.40000, 4.40000, 2.87000 | 0.01266 |

The interpretation is therefore a predominantly unreacted WO₃/Mn₂O₃ precursor mixture after the reported 500 °C treatment, with trace MnWO₄ reaction product and a small rutile-MnO₂ component.

## Evidence

Triclinic WO₃ accounts for the low-angle triplet and split reflections near 33.9–34.5°. Under the same restrained nuisance model it was substantially better than the room-temperature monoclinic WO₃ records. Orthorhombic Mn₂O₃ was preferred over the cubic alternatives by the coherent families near 33.27, 35.82, 38.53, 49–55, 66.03, and 81.84°.

The two weak phases survived a clean-profile re-challenge together. MnWO₄ has partly isolated support near 18.80, 30.32, and 41.47°, while MnO₂ has coherent support near 28.99, 37.69, and 56.96°. Their initial scale estimates were about 6–9 standard deviations above zero. Alternate MnO₂ polymorphs collapsed to zero; an alternate rutile record fitted less well. Mn₃O₄ collapsed to zero, and Mn₃WO₆ remained below one scale standard deviation and destabilized the main-phase profile, so neither was retained.

The baseline uses the stated Cu Kα doublet, one specimen-displacement correction, a positive smooth power-law background, and common nonnegative U/W/X profile terms. The six-parameter physical background curve is stored in `final.gpx` as fixed Chebyshev coefficients solely to make replay self-contained. Texture, roughness, variable SH/L, and phase-size terms were rejected as unsupported, bound, or covariant. The retained breadth is uniaxial [010] microstrain for WO₃ and isotropic microstrain for Mn₂O₃. Saving, reopening, and regenerating fresh reflection lists reproduced the submitted profile exactly; no variables were frozen and all CIFs pass the geometry/occupancy screen.

The final full-grid fit has Rwp = 6.441%, reduced χ² = 5.868, and goodness of fit = 2.422 for 8,301 points and 21 refined parameters.

## Remaining uncertainty

The major-phase identities are reliable, but the pseudo-monoclinic metric leaves some WO₃ polymorph ambiguity. WO₃ W positions were adjusted only along a restrained direction (0.036 Å RMS relative to the parent); unrestricted W and especially O-coordinate refinements overfit. Oxygen coordinates and Mn₂O₃ internal coordinates therefore remain parent-model values and are not independently determined by this laboratory pattern.

The MnWO₄ and MnO₂ fractions are near the practical detection limit. Scale-only statistical errors are roughly 0.1 and 0.2 weight-percent, respectively, with larger model-dependent uncertainty. Their cells and atomic coordinates could not be refined reliably and were held at the cited parent models; a free MnWO₄ cell moved outside a defensible source-mismatch range. The major-phase fractions should likewise be regarded as semi-quantitative (model systematics of order a few weight-percent), not absolute assay values.
