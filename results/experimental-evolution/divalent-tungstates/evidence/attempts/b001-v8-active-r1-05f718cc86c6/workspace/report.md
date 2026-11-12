# Phase analysis and Rietveld refinement

The pattern is explained by three crystalline phases. Fractions are normalized over these modeled crystalline phases; without an internal standard they do not measure amorphous content.

The metadata describe a 700 degrees C reaction of WO3 and Mn3O4 measured in reflection geometry with a PIXcel1D detector. The refinement used the stated Cu Kalpha doublet (1.540598 and 1.544426 A, Kalpha2/Kalpha1 = 0.5) over 9.9034-100.0946 degrees 2theta.

| Phase | Structure | Weight fraction | CIF |
|---|---|---:|---|
| MnWO4 | wolframite, P2/c | 0.767912 (formal e.s.d. 0.000912) | `MnWO4.cif` |
| WO3 | triclinic, P-1 | 0.190855 (0.000601) | `WO3.cif` |
| Mn3O4 | hausmannite, I4_1/amd | 0.041233 (0.000849) | `Mn3O4.cif` |

## Evidence and model selection

The chemical inventory is coherent with the precursor balance

`Mn3O4 + 3 WO3 -> 3 MnWO4 + 1/2 O2`.

Thus the major MnWO4 product plus residual WO3 and Mn3O4 accounts for Mn, W, O and charge without invoking an additional product. The final cells are a = 4.800965, b = 5.709277, c = 4.977730 A, beta = 91.12937 degrees for MnWO4; a = 7.300551, b = 7.546810, c = 7.693574 A, alpha = 90.03833, beta = 90.92000, gamma = 89.97387 degrees for WO3; and a = 5.766437, c = 9.509581 A for Mn3O4.

No exact MnWO4 record was present in the visible structure inventory. Passing FeWO4, ZnWO4, MgWO4 and CdWO4 wolframite parents were therefore compared after identical Mn substitution, cell initialization and nuisance treatment. The MgWO4-derived model (COD 9013902) gave the best replayed fit; its eight symmetry-independent MnWO4 positional coordinates were then refined. This reduced Rwp from 3.31% to 2.68% and produced physically plausible octahedra. The final MnWO4 CIF passes `cif_health.py`; its shortest contacts are W-O 1.773 A and Mn-O 2.115 A.

WO3 uses the passing exact P-1 record COD 2106293. It substantially outperformed the passing P2_1/c record COD 1563541 under the same model. COD 1528915 was not retained because it was flagged for a 1.575 A fully occupied O-O contact and also presented a GSAS-II-incompatible setting. WO3 required finite isotropic size broadening, 0.0988 micrometres; the competing strain model was worse (Rwp 4.946% versus 4.820% at that comparison stage).

Mn3O4 is supported by a positive scale and complementary residual reductions at approximately 32.01, 58.18 and 64.31 degrees 2theta. Two passing exact hausmannite records were compared under the same nuisance model; COD 9001963 outperformed COD 1011262 (Rwp 4.749% versus 4.783% before cell release) and was retained. Its final nearest Mn-O distance is 1.931 A. A passing exact Mn3WO6 watch-list model (COD 2002703) fell to the scale lower bound, 1e-12, in the final re-challenge and was rejected.

All inactive phase-profile terms were explicitly neutralized: size = 10 micrometres, strain = 0, March ratio = 1 and roughness = 0. The common profile used nonnegative U/W/X, with U = 32.465, W = 4.370 and fixed X = 1.155. Releasing SH/L for the repeated low-angle asymmetry gave a stable 0.09904 and improved Rwp to 2.624%. Polarization was strongly supported at 0.82184. Surface roughness was rejected because trials were unphysical or 96-100% correlated; no texture correction was used. Eight background coefficients were retained because each was supported, while higher orders contained multiple terms below 2 sigma for only a small Rwp change.

Representative observed/calculated FWHM values are 0.136/0.120 degrees at 15.1 degrees, 0.128/0.137 degrees at 40.1 degrees, 0.120/0.127 degrees at 71.0 degrees and 0.169/0.163 degrees at 88.0 degrees. Their calculated peak maxima agree with observation at the middle and high angles; the low-angle maximum differs by about 0.011 degrees because of the asymmetric tail. This remaining mismatch was explicitly challenged through common U/W/X, SH/L, WO3 size versus strain, phase-specific MnWO4/Mn3O4 size versus strain, polarization, background and roughness tests.

## Fit and uncertainty

The reopened full-range project converged with Rp = 2.0525%, Rwp = 2.6240%, Rexp = 2.4860%, goodness of fit = 1.0555 and Durbin-Watson = 1.7945 for 8301 observations and 29 refined parameters. Both final replays had maximum shift/e.s.d. below 0.024. The submitted CIFs all pass the final health screen, and `fit.csv`, `result.json`, the CIF fractions and `final.gpx` were cross-checked against the reopened project.

The quoted fraction e.s.d.s are least-squares values and are smaller than model uncertainty. In particular, mutually competitive Mn3O4 size and strain trials shifted its fraction from about 3.7% to 4.7-5.0% while giving almost indistinguishable improvements. Neither broadening mechanism was retained, so the submitted 4.12 wt% should not be interpreted more precisely than roughly one weight-percentage point. The corresponding MnWO4 and WO3 fractions also carry correlated systematic uncertainty at about the percentage-point level. Phase identities and the three-phase inventory are substantially more secure than those last fraction digits. Any amorphous material or crystalline phase below the pattern's detection sensitivity remains unquantified.
