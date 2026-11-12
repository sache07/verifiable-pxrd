# PXRD phase analysis

The pattern is modeled by four crystalline phases. Weight fractions are normalized over those modeled crystalline phases; they do not quantify amorphous material.

| Phase | Space group | Weight fraction |
|---|---:|---:|
| BaWO4 (scheelite) | I 41/a | 0.6464 ± 0.0016 |
| Ba3W2O9 | R -3 c | 0.1499 ± 0.0010 |
| WO3 | P 21/c | 0.1264 ± 0.0014 |
| BaCO3 (witherite) | Pmcn (Pnma-equivalent setting) | 0.0773 ± 0.0018 |

The full-range replay gives Rwp = 3.1796%, Rp = 2.4566%, Rexp = 3.0104%, and GOF = 1.0562 for 8,301 points and 36 refined parameters.

## Evidence and model selection

The chemistry is consistent with incomplete reaction of the reported WO3 and BaCO3 precursors at 750 °C: BaWO4 is dominant, Ba3W2O9 is a substantial non-1:1 barium tungstate product, and WO3 and BaCO3 remain. No precursor amounts or ratio were supplied in `metadata.json`, so no composition closure constraint was imposed or varied.

BaWO4 is supported by independent families near 17.49, 26.69, 28.39, 32.04, 43.19, 48.98, 53.68, and 54.65° 2θ. The retained ordered scheelite model adapts the isostructural SrWO4 topology (COD 1546036) by Sr→Ba and refines the BaWO4 cell. It outperformed both the split-site exact BaWO4 record and a BaMoO4-topology analogue in neutral and elaborated source trials.

Ba3W2O9 is required by families near 16.48, 17.76, 26.28, 27.80, 30.82, 37.66, 40.80, 51.84, 63.07/63.82, and 71.51°. Its COD 1533878 model retains positive scale and stable fraction through the profile and texture loops.

Monoclinic WO3 is identified by the resolved 23.40/23.88/24.65° triplet and additional 33.56/34.45° structure. Monoclinic COD 2311041 beat triclinic and orthorhombic competitors before elaboration; on the final profile its combined-width model gives Rwp 3.1796%, whereas the triclinic replacement gives 4.4680% and does not reconverge physically under further width elaboration. A provisional coexisting triclinic WO3 scale corresponded to only about 0.62 wt%, but varied from about 0.39 to 0.82 wt% under legitimate texture/broadening reallocations and produced a singular width trial. It therefore fails the same-formula coexistence gate and is not reported as a phase. Trace polymorphic WO3 below this reliability threshold cannot be excluded.

Orthorhombic BaCO3 is supported by multiple non-coincident families, including reflections near 20.18, 24.55, 34.01, 34.84, 44.47, 47.03, and 73.18°. Its scale converged from independent starts; the hexagonal polymorph and an alternate incompatible-setting record collapsed to zero in the rebuilt watch list. The retained COD 9010928 cell refined to approximately 5.3058 × 8.9079 × 6.4313 Å.

The accepted profile uses a smooth 10-term Chebyshev background, one specimen-displacement correction, nonnegative common U/W/X terms, and B-only surface roughness. BaWO4 broadening is neutral (size 10 µm, strain zero); Ba3W2O9 retains [001] strain anisotropy; WO3 uses isotropic size plus strain; and BaCO3 retains [010] strain anisotropy. All March-Dollase ratios are fixed at one. A joint polarization/roughness trial was rejected despite lower Rwp because it remained nonconverged after two 30-cycle passes and was more than 96% mutually correlated and more than 98% correlated with the dominant scale.

## Remaining uncertainty

The quoted uncertainties are GSAS-II covariance estimates and do not include source, background, or line-shape systematics. The BaCO3 identification is secure, but its absolute fraction is the least robust: neutral and broadened physical models span roughly 5–8 wt%, so a systematic uncertainty of order 2 wt% is more realistic than its formal e.s.d. Atomic coordinates and displacement parameters were held at the screened source-model values; only cells, scales, and supported profile terms were refined because this multiphase laboratory pattern does not determine free atomic coordinates reliably.

All four submitted CIFs pass `learned/cif_health.py` after export. The CIFs, normalized fractions, fit profile, and statistics were generated from the replayed `final.gpx` project.
