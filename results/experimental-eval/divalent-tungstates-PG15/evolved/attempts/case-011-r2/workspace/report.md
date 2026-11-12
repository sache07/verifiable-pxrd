# Powder-diffraction phase analysis

## Result

The pattern is described by two crystalline phases. Fractions are normalized over these modeled crystalline phases; they do not quantify any amorphous material.

| Phase | Structural model | Weight fraction |
|---|---|---:|
| Tungsten trioxide | triclinic WO3, *P* -1, COD 2106293 | 72.88 +/- 0.13% |
| Pyrolusite | beta-MnO2, *P* 42/*m n m*, COD 1514110 | 27.12 +/- 0.13% |

The values in parentheses are covariance-derived formal standard uncertainties. A more realistic systematic uncertainty is approximately 1 wt% because the WO3 symmetry choice and the MnO2 preferred-orientation model affect the partitioning more than the formal scale uncertainty.

## Evidence and model selection

The characteristic split WO3 low-angle group at about 23.44, 23.93, and 24.69 degrees 2theta, together with its middle- and high-angle families, supports the tungsten-oxide model. Independent lines at about 29.01, 37.67, 56.96, 59.66, and 72.53 degrees support beta-MnO2. This inventory is also chemically consistent with the stated MnO2/WO3 precursors and 300 degrees C treatment: the measured solid is predominantly retained precursor oxides rather than a demonstrable manganese tungstate product.

Several physical WO3 records were compared using the same background, scale, angular-correction, and profile treatment. COD 2106293 gave the best overall peak-position and intensity agreement. Its refined cell is *a* = 7.31586, *b* = 7.54573, *c* = 7.70250 A, alpha = 89.9381, beta = 90.7735, gamma = 90.0081 degrees. The beta-MnO2 cell is *a* = 4.40498 and *c* = 2.87697 A. Exported structures retain full occupancies and chemically reasonable nearest-neighbor distances: W-O 1.72-2.22 A and Mn-O 1.888-1.891 A.

The final GSAS-II model uses the Cu K-alpha doublet specified in the metadata, a smooth 10-coefficient Chebyshev background, one zero correction, and a common nonnegative low-dimensional peak profile. WO3 required symmetry-compatible uniaxial microstrain; MnO2 required a March-Dollase [110] preferred-orientation correction (ratio 0.824). Neutral or unsupported size, extra strain, roughness, and WO3 texture terms were removed. The final full-range save/reopen/replay converged with Rwp = 5.7245%, Rp = 4.2042%, and GOF = 2.1265. The calculated and difference curves in `fit.csv` are exact exports from `final.gpx`.

Potential minor phases were re-challenged after establishing the common profile. Exact MnWO4, an isovalently substituted ferberite prototype, Mn3WO6, and Mn3O4 refined to null scale. Mn2O3 trials produced an apparent approximately 1.1 wt% contribution, but the gain came mainly from overlapped peaks near 33.3 and 55.5 degrees while expected unique families were absent or worsened; it was therefore rejected as an intensity/profile surrogate rather than accepted as a phase. No third phase is supported coherently, although an unidentified or poorly crystalline component below roughly 1 wt% cannot be excluded.

## Remaining uncertainty

The selected WO3 cell is metrically close to monoclinic, so the *P* -1 assignment should be regarded as triclinic/pseudomonoclinic WO3 rather than an unambiguous symmetry determination from this laboratory powder pattern alone. A physical *P* 21/*c* alternative fit slightly worse and shifted the phase fractions by about 1 wt%; this brackets the main structural systematic uncertainty. The absence of supplied pointwise uncertainties also means the reported GOF and formal fraction uncertainties use a 1/I Poisson proxy and should not be interpreted as absolute uncertainty estimates.

Submitted artifacts are [phase_WO3_P-1.cif](phase_WO3_P-1.cif), [phase_beta-MnO2.cif](phase_beta-MnO2.cif), [fit.csv](fit.csv), [result.json](result.json), and the replayed [final.gpx](final.gpx).
