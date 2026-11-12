# Powder X-ray diffraction phase analysis

## Result

The crystalline material is an essentially unreacted two-precursor mixture. No crystalline manganese tungstate product is required by the diffraction pattern.

| Phase | Structural model | Refined cell (Å, °) | Crystalline weight fraction |
|---|---|---|---:|
| Monoclinic γ-WO₃ | *P* 2₁/*c* (No. 14), COD 2311041 | *a* = 7.69505, *b* = 7.53853, *c* = 10.54126, β = 136.10879 | 0.74083 (74.08 wt%) |
| Pyrolusite MnO₂ | *P* 4₂/*mnm* (No. 136), COD 1514110 | *a* = 4.40075, *c* = 2.87411 | 0.25917 (25.92 wt%) |

Fractions are normalized to the two modeled crystalline phases. The GSAS-II covariance calculation gives a formal standard uncertainty of 0.00173 in each fraction (0.17 percentage point), but this is smaller than the realistic systematic uncertainty discussed below.

## Evidence and refinement

The sharp WO₃ triplet near 23.44, 23.93, and 24.69° 2θ and its multiplet near 33.6–34.5° are reproduced by the monoclinic WO₃ model. The broader peaks near 29.0, 37.7, 43.1, 57.0, 59.7, and 67.5° are reproduced by rutile-type pyrolusite. A common angular shift is explained by a refined specimen displacement of −0.637 mm. Together, these two structures account for all significant Bragg peaks. In particular, the characteristic low-angle and approximately 30° peak set expected for wolframite MnWO₄ is absent.

Alternative WO₃ reference settings were screened. A triclinic model used extra degrees of freedom while converging toward a metrically monoclinic cell and predicting unsupported splitting; the physically stable *P* 2₁/*c* model was therefore selected. The refined ratio is also chemically consistent with an unreacted 1:1 metal-molar precursor charge, whose nominal WO₃:MnO₂ mass ratio is about 72.7:27.3.

The final GSAS-II Rietveld refinement used the supplied Cu Kα₁/Kα₂ wavelengths and 0.5 intensity ratio over the complete 9.9034–100.0949° scan. Since pointwise uncertainties were not supplied, count-statistical weights were used. Refined terms included phase scales and cells, a smooth Chebyshev background, specimen displacement and roughness, common profile terms, and phase-dependent size/strain; modest [110] March–Dollase texture was included for MnO₂. WO₃ W positions and the MnO₂ oxygen coordinate were refined. The weakly constrained WO₃ oxygen shifts were regularized to a physically plausible 0.05 Å RMS displacement from the reference model.

The converged fit has Rwp = 5.280%, Rp = 3.881%, Rexp = 2.693%, and goodness of fit = 1.967 (8,301 observations, 58 refined parameters). The calculated profile includes the background, and `fit.csv` defines the difference as observed minus calculated.

## Remaining uncertainty

Phase identification is high confidence, and the relative abundance of the two major crystalline phases is reasonably constrained. A practical uncertainty of about ±2 weight-percentage points is more defensible than the formal covariance error because there is no calibrated instrumental profile or supplied counting uncertainty, and scale, texture, roughness, background, and absorption-related effects are partly correlated.

Absolute phase fractions in the whole specimen cannot be determined reliably without an internal standard, so amorphous material is not quantified. A trace crystalline impurity below roughly 1–2 wt% could also be hidden by overlap and background. The unit cells and structure types are robust, but the detailed WO₃ oxygen displacement pattern and correlated heavy-atom coordinates are not a unique structure determination from this powder pattern; the submitted CIF is a restrained, chemically plausible Rietveld model.
