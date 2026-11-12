# Powder X-ray diffraction phase analysis

## Result

The pattern is best described by four crystalline phases. Fractions are normalized over those phases; no amorphous fraction can be obtained without an internal standard.

| Phase | Space group | Refined unit cell | Weight fraction |
|---|---|---|---:|
| SrWO4, scheelite | I41/a | a = 5.41939 A, c = 11.96311 A | 65.42% |
| WO3, monoclinic | P21/c | a = 7.30723 A, b = 7.54119 A, c = 10.53866 A, beta = 133.0962 deg | 10.57% |
| Sr3W2O9, monoclinic | C2/c | a = 9.63168 A, b = 5.53386 A, c = 13.45121 A, beta = 103.5836 deg | 10.92% |
| Sr3WO6, cubic analogue | Pa-3 | a = 10.92994 A | 13.09% |

The final GSAS-II fit over 10.009-99.994 degrees 2theta (8,282 points) has Rwp = 11.342%, Rp = 7.999%, and GOF = 3.209. The weighted chi-square is 85,261.8. The calculated aggregate Sr:W molar ratio is 1.057:1, consistent with the SrCO3 + WO3 chemical context.

## Evidence

Scheelite SrWO4 accounts for the dominant peak system, including the groups near 18.3, 28.0-30.2, 33.4, 45.4-47.7, 52.0, and 56.1 degrees. Monoclinic WO3 resolves the characteristic 23.4-24.8 degree multiplet and many weaker lines through the 33-56 degree region. The C2/c Sr3W2O9 model explains independent intensity near 22.1, 29.7, 32.7, 44.6, and 53.5 degrees; suppressing this phase caused a large fit deterioration.

A remaining coherent cubic component was found by whole-profile residual screening. Its principal diagnostic reflections include the pair near 29.8 and 30.9 degrees. A Pa-3 Sr3WO6 model, generated from an isostructural divalent-metal tungstate analogue and then refined against this pattern, reduced Rwp from about 13.07% to 12.03% before the final joint optimization; the final four-phase refinement reached 11.34%.

Starting structure candidates were tested by full-pattern fit, not only by matching the strongest peaks. Scale factors, cells, peak-shape terms, background, and bounded preferred-orientation terms were jointly optimized. The final project was independently reopened and recalculated in GSAS-II; it reproduced the submitted fractions and Rwp, and its regenerated profile agrees with `fit.csv` to numerical precision.

## Uncertainty and limitations

The phase inventory is more secure than the last digits of the fractions. Strong overlap, anisotropic intensity effects, and the absence of supplied pointwise uncertainties or an internal standard make a practical uncertainty of a few absolute weight percent more realistic than the numerical precision in `result.json`. The fractions do not include possible amorphous material.

The cubic component and Pa-3 structure family are supported by its distinct reflections, but its exact assignment as stoichiometric Sr3WO6 is tentative: the model is analogue-derived, so an isostructural Sr-W-O defect composition cannot be excluded from this pattern alone. Its 13.09% fraction is therefore less reliable than the dominant SrWO4 fraction.

For WO3, the W framework and monoclinic phase assignment are reliable, but oxygen coordinates are weakly constrained by Cu X-ray data. Two oxygen positions inherited from the source model were chemically regularized to remove an unphysical short O-O contact; they should not be interpreted as a precision oxygen-sublattice refinement. All submitted models pass the final interatomic-contact screen.

The remaining positive residual features are mostly at reflections already represented by the four models and are consistent with imperfect profile/intensity modeling. A few weak low-angle residuals did not support a unique fifth phase, so no additional crystalline phase was reported.
