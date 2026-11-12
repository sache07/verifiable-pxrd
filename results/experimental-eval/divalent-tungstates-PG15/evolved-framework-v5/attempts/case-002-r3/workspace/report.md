# Powder X-ray diffraction phase analysis

## Result

The specimen is modeled by two crystalline precursor phases. Fractions are normalized over those modeled crystalline phases; they do not measure amorphous material.

| Phase | Structural model | Refined cell | Weight fraction |
|---|---|---|---:|
| Monoclinic WO3 | COD 2311041, P 21/c | a = 7.68724 Å, b = 7.52902 Å, c = 10.54389 Å, beta = 136.0968° | 0.64764 (64.76 wt%) |
| Tetragonal BaO2 | COD 1010113, I 4/mmm | a = 3.81196 Å, c = 6.84381 Å | 0.35236 (35.24 wt%) |

The whole-pattern fit over 9.9034–100.0949° 2theta gives Rwp = 7.5813%, Rp = 5.6285%, Rexp = 3.6367%, goodness of fit = 2.0847, and chi-square = 35992.60 for 8301 observations. With the supplied raw counts and no pointwise standard uncertainties, refinement used counting-statistical weights, 1/max(counts, 1).

## Evidence and model selection

The metadata identifies BaO2 and WO3 precursors heated at only 200 °C and a Cu K-alpha reflection measurement. The pattern is dominated by the characteristic split monoclinic-WO3 groups near 23.39, 23.89, and 24.60°, and 33.55–34.42° 2theta. Tetragonal BaO2 accounts for the independent family at approximately 26.29/27.02, 42.91, 46.59, 55.34/55.73, and 68.88°.

Exact-composition reference models were compared before coordinate refinement. COD 2311041 gave the best physical WO3 topology among the tested monoclinic, triclinic, and orthorhombic references; bounded coordinate refinement retained six-coordinate W environments with W–O distances of 1.777–2.180 Å. The BaO2 model retains a 1.410 Å peroxide O–O bond. The alternative WO3 models fit less well or introduced shorter, less credible contacts, so none justified replacing this topology.

Scheelite BaWO4 was considered as the chemically plausible reaction product. Its diagnostic calculated reflections near 17.27, 31.88, and 53.60° are absent as a coherent family. The largest remaining positive residuals instead lie on the already modeled WO3/BaO2 peak groups, reflecting imperfect peak shape/intensity rather than a third lattice. No additional crystalline phase has a reliably determinable structure or fraction from this pattern.

The final GSAS-II model uses the reported Cu K-alpha1/K-alpha2 wavelengths and 0.5 intensity ratio, a smooth 16-term Chebyshev background, refined cells and scales, bounded specimen/instrument calibration, anisotropic phase broadening, and a small WO3 [010] March–Dollase correction (ratio 1.028). Atomic coordinates were refined only where they remained chemically physical. A fresh zero-variable replay regenerated reflection lists and structure factors from `final.gpx`; it reproduced Rwp and the fractions exactly and reproduced the submitted calculated profile to below 5e-9 counts.

## Remaining uncertainty

The scale-factor covariance gives a formal one-standard-deviation fraction uncertainty of 0.00123 (0.12 percentage point), but this is too optimistic because uncertainties were not supplied and calibration/profile terms are correlated. In particular, the specimen displacement refined to the imposed -800 micrometre bound, with zero offset -0.1788°, and several broadening terms also reached their bounds. A more realistic uncertainty is about 2–3 wt percentage points for either normalized crystalline fraction.

Phase identities and average topologies are well supported, but the oxygen coordinates and microstructural parameters should not be treated as a precision structure determination. Trace crystalline phases below the residual/detection level and any amorphous fraction cannot be quantified reliably from this dataset.
