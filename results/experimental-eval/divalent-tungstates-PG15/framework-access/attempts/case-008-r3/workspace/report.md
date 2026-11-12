# Powder XRD phase analysis

## Result

The crystalline pattern is modeled as **MnWO4 wolframite (97.574 wt%)** plus **monoclinic gamma-WO3 (2.426 wt%)**. Fractions are normalized over these modeled crystalline phases; they do not quantify any amorphous content.

| Phase | Space group | Refined cell | Crystalline weight fraction |
|---|---|---|---:|
| MnWO4, wolframite | P 2/c | a = 4.83158 A, b = 5.75758 A, c = 4.99695 A, beta = 91.2186 deg | 0.975739 |
| gamma-WO3, monoclinic | P 21/c | a = 7.30378 A, b = 7.54025 A, c = 10.5277 A, beta = 133.118 deg | 0.024261 |

The final whole-pattern fit has Rwp = 3.8422%, Rp = 2.9188%, Rexp = 2.7517%, and GOF = 1.3963 (8301 points). The independently regenerated profile from `final.gpx` has no replay review flags.

## Evidence

The MnO + WO3 precursor context and 900 C treatment make MnWO4 the expected reaction product. More importantly, the observed peak sequence over the full 10-100 deg range matches the monoclinic wolframite model (COD-derived starting model 1520200), including the strong groups near 15.7, 18.7, 23.9-24.4, 30.1-31.4, and 36.3-37.5 deg 2theta. A one-phase refinement left coherent residual peaks and gave about 5.13% Rwp.

The remaining features near 23.45, 24.68, and the 33-35 deg cluster are jointly explained by monoclinic gamma-WO3. Adding this phase reduced Rwp to about 4.57% before the later specimen/profile corrections and to 3.8422% in the final model. Under the same profile model, the selected P21/c WO3 framework (COD-derived starting model 2311041) fit slightly better than the close alternative monoclinic setting (about 3.880% versus 3.888% Rwp in the comparison stage); tested triclinic and other WO3 models were worse (about 4.01% or above). No independent residual peak family justified a third crystalline phase.

The refinement used both Cu Kalpha wavelengths and their reported 0.5 intensity ratio, a 15-term Chebyshev-1 background, specimen displacement and Suortti roughness, phase scales/cells, bounded March-Dollase terms, and an anisotropic microstrain term for MnWO4. MnWO4 coordinates and one common isotropic displacement parameter were refined. The minor WO3 coordinates were retained from the literature framework because unconstrained coordinate refinement was unstable at this abundance; its cell and profile contribution were refined. No Pawley or Le Bail intensities are used.

## Uncertainty

The WO3 phase is supported by multiple peaks, but its exact coordinate variant is not determined reliably at only about 2.4 wt%. Closely related monoclinic gamma-WO3 descriptions are nearly indistinguishable here. A constrained profile scan favored the allowed upper limit of 0.020 A^2 for the WO3 isotropic displacement parameter; fixing other plausible values shifted its fraction from roughly 2.2 to 2.5 wt%. Thus the formal covariance error (about 0.045 wt% absolute) is too optimistic: a practical result is **2.4 +/- 0.3 wt% WO3** and **97.6 -/+ 0.3 wt% MnWO4**, with additional unquantified uncertainty if amorphous material is present. The reported exact fractions are the values stored in `final.gpx` and used for `fit.csv`.
