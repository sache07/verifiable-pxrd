# Powder XRD phase analysis

The pattern is explained by two crystalline phases. Weight fractions are normalized over those modeled crystalline phases.

| Phase | Structure | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| CaWO4, scheelite | `I 41/a` | a = b = 5.23805, c = 11.33458 | 0.85392 (85.39 wt%) |
| WO3, monoclinic | `P 21/c` | a = 7.31514, b = 7.55742, c = 10.51865, β = 132.9971° | 0.14608 (14.61 wt%) |

## Evidence

The dominant broad reflection family, including the features near 18.27°, 28.43–28.76°, 31.21°, 33.84°, 38.92°, and 46.89° 2θ, indexes as scheelite CaWO4. The sharper family near 22.77°, 23.18°, 23.99°, 26.19°, 32.88–33.14°, 40.98–41.51°, and 49.48° indexes as monoclinic WO3. This inventory is also chemically economical for partially reacted CaCO3 + WO3 at 650 °C.

Multiple physical WO3 coordinate starts and both monoclinic and triclinic descriptions were compared with matched coordinate and profile relaxation. The `P 21/c` model gave the better parsimonious physical solution. Calcite, CaO, and alternative calcium tungstate/oxide phases were not retained because their diagnostic strong reflections are absent and no separate coherent residual family remains after fitting CaWO4 + WO3. Residual intensity and width structure occurs at reflections of the accepted phases and was handled with coordinates, phase-specific size/strain, and a weak CaWO4 preferred-orientation correction rather than by adding phases.

The final full-grid atomic replay gives Rwp = 3.4305%, χ² = 9919.08, and goodness of fit = 1.094. A fresh replay of `final.gpx` reproduced the submitted profile and fractions without optimization or physical-profile warnings.

## Uncertainty

The formal scale-covariance uncertainty is about 0.00069 in weight fraction (0.07 percentage point) for each phase, but this understates model uncertainty. A practical uncertainty of roughly one percentage point is more appropriate because phase fraction correlates with displacement factors, preferred orientation, and the minor-phase oxygen coordinates. The two-phase inventory and framework assignments are substantially more secure than the exact WO3 oxygen positions.

No amorphous fraction can be determined without an internal standard, so the reported fractions must not be interpreted as absolute whole-sample fractions. No additional crystalline structure can be determined reliably from the remaining residuals; they do not form an unindexed reflection family.
