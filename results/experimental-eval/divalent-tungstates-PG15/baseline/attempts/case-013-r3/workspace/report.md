# Quantitative phase analysis

A six-phase GSAS-II Rietveld model accounts for the crystalline diffraction pattern. Weight fractions are normalized over these modeled crystalline phases; they do not quantify amorphous material.

| Phase | Space group | Weight percent | Submitted structure |
|---|---:|---:|---|
| PbWO4, scheelite | I 41/a | 59.43 (20) | [phase_01_PbWO4_scheelite.cif](phase_01_PbWO4_scheelite.cif) |
| Pb2WO5, lead oxytungstate | C 2/m | 14.38 (16) | [phase_02_Pb2WO5.cif](phase_02_Pb2WO5.cif) |
| WO3, monoclinic | P 21/n | 9.88 (15) | [phase_03_WO3_monoclinic.cif](phase_03_WO3_monoclinic.cif) |
| PbO, massicot | P b c m | 7.08 (10) | [phase_04_PbO_massicot.cif](phase_04_PbO_massicot.cif) |
| PbO, litharge | P 4/n m m | 4.55 (8) | [phase_05_PbO_litharge.cif](phase_05_PbO_litharge.cif) |
| Pb2O3, lead sesquioxide | P 21/c | 4.68 (11) | [phase_06_Pb2O3.cif](phase_06_Pb2O3.cif) |

Parentheses are covariance-only one-standard-deviation uncertainties on the last shown digits. They are smaller than the likely practical uncertainty.

## Evidence and refinement

The PbO + WO3 reaction context and the dominant scheelite sequence at approximately 27.70, 29.91, 33.06, 45.03, 47.28, 51.49, and 55.54 degrees 2theta identify PbWO4 as the principal product. The resolved WO3 triplet near 23.4, 23.9, and 24.6 degrees supports residual monoclinic WO3. Pb2WO5 is required by the group near 25.91, 26.79, 30.62, and 31.05 degrees and supporting higher-angle reflections. Massicot and litharge give distinct PbO contributions, most clearly around 29.35 degrees for massicot and 28.9/32.1 degrees for litharge. The close pair at about 30.15 and 30.24 degrees, with supporting lines near 43.6 and 50.0 degrees, supports Pb2O3.

The refinement used the stated Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio over 10.009-99.994 degrees 2theta. Phase scales, unit cells, zero, an empirical peak profile, and a 15-term Chebyshev background were refined. Pb/W coordinates in the Pb2WO5 model and the Pb height in litharge were optimized before coordinates were fixed for the final pass. The converged fit has Rwp = 10.2345%, Rp = 7.3447%, goodness of fit = 2.931, and maximum shift/esd = 0.089 for 8,282 points and 46 refined variables. The complete numerical results are in [result.json](result.json), the profile is in [fit.csv](fit.csv), and the generating project is [final.gpx](final.gpx).

## Remaining uncertainty

No pointwise standard uncertainties or calibrated instrument broadening function were supplied. The fitted peak shape is therefore empirical, and residuals remain strongly serially correlated (Durbin-Watson = 0.266). Peak overlap among the Pb/W oxides, possible preferred orientation, and strong microabsorption can bias scale-derived fractions. A practical uncertainty of roughly 1-2 absolute wt% is more realistic than the formal errors, especially for Pb2WO5 and the minor oxides.

The Pb2WO5 CIF is based on the isostructural Pb2MoO5 model (COD 7220560) with Mo replaced by W; its cell and heavy-atom coordinates are supported by the pattern, but the oxygen coordinates and detailed structure are not determined reliably from these data. Pb2O3 is also less secure than PbWO4 and WO3 because many of its reflections overlap other phases. Trace Pb3O4 or PbO2-like material cannot be excluded uniquely, but adding such phases was not justified by phase-specific residual peaks. All percentages are crystalline-phase-normalized; an amorphous fraction cannot be determined without an internal standard.
