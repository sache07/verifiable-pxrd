# Powder XRD phase analysis

The pattern is modeled as three crystalline phases. Fractions are normalized over those phases only:

| Phase | Structural model | Weight fraction |
|---|---|---:|
| MgWO4, wolframite | P 2/c, COD 9013902 | 0.7773 |
| WO3 | P 21/c, COD 2311041 | 0.1525 |
| MgO, periclase | F m -3 m, COD 9000499 | 0.0702 |

The refinement uses the reported Cu Kalpha1/Kalpha2 doublet over the full 9.9034–100.0949 degree scan. A fresh atomic-model replay of `final.gpx`, which ignores cached calculated intensities, gives Rwp = 5.7249%, Rp = 4.1400%, Rexp = 2.8567%, and goodness of fit = 2.004. `fit.csv` contains that replayed profile; its difference column is observed minus calculated.

## Evidence

MgWO4 accounts for the dominant, dense wolframite reflection set. WO3 accounts for the remaining reflection cluster concentrated around 23–34 degrees; among screened WO3 references, COD 2311041 gave the best physically admissible monoclinic model. A triclinic alternative reached a similar preliminary residual only after implausibly large angular cell changes, while another monoclinic reference was distinctly worse. MgO is supported by its sparse rocksalt sequence, including features near 42.9, 62.3, 74.7, 78.6, and 93.9 degrees. Omitting MgWO4, WO3, or MgO raises Rwp to approximately 57.91%, 19.73%, or 7.21%, respectively. No coherent residual peak sequence supported a fourth crystalline phase.

Refined cells are MgWO4: a = 4.690795, b = 5.675295, c = 4.929473 A, beta = 90.77550 degrees; WO3: a = 7.690957, b = 7.538353, c = 10.531356 A, beta = 136.08478 degrees in the submitted P 21/c setting; and MgO: a = 4.213425 A. A constrained quadratic floor plus power-law tail described the background much better than either a simple polynomial or an exponential-tail model. The fixed 36-term Chebyshev representation in the project numerically reproduces that smooth physical background.

Residual-profile tests support weak March-Dollase corrections for MgWO4 along [111] (ratio 1.0171) and WO3 along [010] (ratio 1.0278), plus [001] uniaxial microstrain in MgWO4 (equatorial/axial terms about 3349/2424 ppm). Adding these three independently screened terms lowered replay Rwp from 5.8986% to 5.7249%. Equivalent anisotropy tests for WO3 and MgO collapsed to their isotropic values and were not retained.

## Remaining uncertainty

The reported least-squares precision understates model uncertainty. Background shape, common isotropic displacement parameters, polarization, low-angle surface correction, and phase scales are correlated. Sensitivity tests suggest approximate absolute fraction uncertainties of 0.010 for MgWO4, 0.005 for WO3, and 0.012 for MgO. These are model-sensitivity estimates, not formal standard deviations. MgO is least secure because it has only a few reflections and its scale correlates strongly with its displacement parameter. No amorphous fraction can be obtained from this analysis.

The MgWO4 coordinate shifts were small and remained inside physical bounds. The two refined WO3 W sites are highly correlated, so their shifts are only weakly determined. WO3 oxygen coordinates could not be refined reliably: a bounded trial drove nearly every oxygen coordinate to a limit, so the submitted CIF retains the parent oxygen positions. MgO coordinates are fixed by symmetry. Instrumental Lorentzian broadening versus crystallite size, absolute Gaussian broadening versus microstrain, and specimen displacement versus angular zero/cell scale are non-unique; their individual nuisance-parameter values should not be interpreted physically. The phase inventory and normalized crystalline fractions are nevertheless stable across the admissible model tests and are reproducible from `final.gpx`.
