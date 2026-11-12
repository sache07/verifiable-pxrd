# PXRD phase analysis

The pattern is modeled as two crystalline phases: **71.29 wt% monoclinic gamma-WO3** and **28.71 wt% tetragonal pyrolusite MnO2**, normalized over the modeled crystalline material. No crystalline MnWO4 is required by the data.

## Evidence

The gamma-WO3 assignment accounts for the diagnostic low-angle triplet at 23.443, 23.932, and 24.693 degrees 2theta and the split group at 33.592, 33.907, and 34.483 degrees. Pyrolusite MnO2 accounts for distinct reflections at 37.667, 43.122, 56.955, and 59.661 degrees. A refined specimen zero offset of +0.3287 degrees brings both sets into registration with their reference structures. In contrast, the strongest relatively unoverlapped MnWO4 reflections expected near 18.81 and 30.33/30.78 degrees after applying that offset are absent. This is chemically plausible for a 300 degrees C treatment of MnO2 and WO3: the measured crystalline material is predominantly unreacted precursor rather than manganese tungstate product.

Starting structures were COD 1528915 for gamma-WO3 (P 21/n, space-group No. 14) and COD 1514110 for pyrolusite MnO2 (P 42/m n m). Refined cells are:

- gamma-WO3: a = 7.31107 A, b = 7.54093 A, c = 7.69728 A, beta = 90.7659 degrees, V = 424.331 A^3.
- pyrolusite MnO2: a = 4.40171 A, c = 2.87518 A, V = 55.707 A^3.

The GSAS-II Rietveld refinement used the reported Cu K-alpha1/K-alpha2 wavelengths and 0.5 intensity ratio, counting-statistical weights derived from the raw counts, a 12-term Chebyshev background, refined phase scales and cells, and a constrained profile model. Atomic coordinates and displacement parameters were retained from the reference structures because this laboratory mixture pattern does not support their independent refinement. The final refinement converged with Rwp = 7.80%, Rp = 5.58%, Rexp = 2.69%, goodness of fit = 2.90, and maximum shift/s.u. = 0.044.

## Uncertainty

The GSAS-II covariance matrix gives a formal standard uncertainty of 0.19 wt% for each normalized phase fraction. This understates the practical uncertainty: point uncertainties and a calibrated instrumental profile were not supplied, the refined zero offset is sizable, and profile/background choices are correlated with scale. A few wt% systematic uncertainty is therefore more realistic. Fractions exclude amorphous material and any crystalline component below the pattern's detection limit. Residuals are concentrated around the strongest modeled WO3 peaks and are consistent with imperfect peak-shape/intensity modeling; they do not form a coherent additional phase fingerprint.
