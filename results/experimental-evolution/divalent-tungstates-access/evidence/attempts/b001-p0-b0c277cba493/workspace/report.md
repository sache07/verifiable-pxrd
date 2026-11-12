# Powder XRD phase analysis

## Result

The crystalline portion is **CaWO4 scheelite (I41/a), 85.16 wt%**, plus **monoclinic WO3 (P21/c), 14.84 wt%**. Fractions are normalized only over the modeled crystalline phases; this experiment does not determine any amorphous fraction.

The submitted atomic-model fit has Rwp = 4.441%, Rp = 3.143% and goodness-of-fit = 1.416 (counting-statistical Rwp expectation 3.135%). The refined cells are CaWO4 a = 5.23627, c = 11.33167 A, and WO3 a = 7.31176, b = 7.55401, c = 10.51398 A, beta = 132.99745 degrees.

## Evidence

The dominant 18.28, 28.43, 33.85, 46.89 and 57.64 degree peaks and the remaining scheelite series are reproduced by CaWO4. The resolved 22.77/23.18/23.99 degree triplet and its higher-angle companions require low-symmetry WO3. This agrees with the WO3 + CaCO3 precursor context at 650 degrees C: CaWO4 formed as the main product while some WO3 remained. Models for CaCO3, CaO and alternate calcium tungstates did not account for an additional peak family, and the final residual contains no coherent set requiring a third crystalline phase.

Matched candidate screening favored the P21/c WO3 parent; triclinic P-1 was the closest alternative, so the WO3 identity is secure but the exact low-symmetry polymorph is less certain than the CaWO4 assignment. The final profile was regenerated directly from the saved atomic GSAS-II model over all 8301 observations; cached calculated intensities were not used, and no negative-width, negative-background or displacement-parameter flags were found.

## Uncertainty

A practical model spread is about 1--2 wt% absolute for either phase; the reported values are the exact scale-derived fractions in `final.gpx`. Absolute cell metrics correlate with zero/specimen displacement, so calibration-bounded values were used. Scheelite's oxygen coordinate is supported only at modest precision. WO3 oxygen coordinates cannot be determined reliably from this mixture pattern: unconstrained refinement produced implausibly short W--O contacts, so the submitted P21/c coordinates are regularized to remain within 0.05 A RMS (O) and 0.04 A RMS (W) of the published parent. The CIF therefore identifies the phase and provides a physically credible diffraction model, but should not be interpreted as a precise determination of WO3 local octahedral distortions.
