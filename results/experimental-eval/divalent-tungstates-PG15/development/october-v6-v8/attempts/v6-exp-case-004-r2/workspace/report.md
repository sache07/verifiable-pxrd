# PXRD phase analysis

## Result

The crystalline pattern is described by two phases:

| Phase | Structural model | Weight fraction |
|---|---|---:|
| WO3 | triclinic, P -1 (COD 2106293) | 70.784 +/- 0.159 wt% |
| CoWO4 | wolframite, P 2/c | 29.216 +/- 0.159 wt% |

The fractions are normalized over the modeled crystalline phases only. They do not measure amorphous material or absolute phase abundance because no internal standard was supplied.

## Evidence and model selection

The triclinic WO3 model accounts for the characteristic split group near 23.2-24.4 deg 2theta and its many higher-angle reflections. Wolframite CoWO4 is required by multiple lines across the complete pattern, including the distinct feature near 30.7 deg. Both submitted atomistic models passed the supplied CIF composition, occupancy, symmetry-expansion, duplicate-site and contact audit.

The CoWO4 model uses the audited wolframite MgWO4 topology from COD 9013902 with the charge-balanced Mg2+ -> Co2+ substitution; source coordinates were retained. A P21/c WO3 alternative converged at Rwp = 6.249%, worse than the accepted P -1 model. A sanitized direct CoWO4 candidate was slightly worse in the matched fixed-cell comparison (Rwp = 6.124%) and became oscillatory when its cell was released (maximum shift/esd repeatedly 0.11-5.5), so its transient lower Rwp was rejected as non-reproducible. Co3O4 collapsed to effectively zero scale.

A forced CoO branch refined to 0.783 wt% and changed Rwp only from 6.103% to 6.090%. This assignment is not reliable: only three of six CoO lines improved their local residuals, while the strongest predicted line at 42.51 deg 2theta made the residual substantially worse and two further lines also worsened it. CoO is therefore not included; a crystalline trace near the roughly 1 wt% level cannot be excluded or quantified reliably from this pattern.

## Refinement and uncertainty

The final GSAS-II refinement used 8284 points from 10.0 to 100.0 deg 2theta and 20 variables. It converged without dropped variables (maximum shift/esd 0.019) at Rwp = 6.103%, Rp = 4.615%, Rexp = 3.283% and goodness-of-fit = 1.861. The supplied Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio were used. Refined terms were a 12-coefficient Chebyshev-1 background, phase scales and cells, sample displacement, one surface-roughness term, global U/W/Y profile terms, and isotropic WO3 crystallite size. Strain, preferred orientation, extra profile/envelope terms, and coordinate refinement were tested but rejected when unstable, highly correlated, negligible, or unsupported across the full range. Metal/O isotropic U values were fixed at 0.005/0.010 A^2 after zero source values were found unsuitable.

Pointwise uncertainties were not supplied, so Poisson counting weights (1/I) were used. The quoted fraction uncertainties are covariance-derived formal values and do not include structural-model, absorption/microabsorption, preferred-orientation, or trace-phase uncertainty; the true compositional uncertainty is therefore larger. `fit.csv` contains the full measured range, while the reported refinement statistics use the stated 10-100 deg range.
