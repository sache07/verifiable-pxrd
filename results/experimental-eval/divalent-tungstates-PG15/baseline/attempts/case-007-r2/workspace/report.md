# Phase analysis and refinement report

The pattern is described by three crystalline phases: wolframite-type MgWO4, monoclinic WO3, and residual rocksalt MgO. The refined crystalline weight fractions are:

| Phase | Space group | Weight fraction | Refined cell (angstrom, degrees) |
|---|---:|---:|---|
| MgWO4 | P 2/c | 0.7772 (formal s.u. 0.0016) | a=4.69029, b=5.67452, c=4.92896, beta=90.7755 |
| WO3 | P 21/n | 0.1524 (formal s.u. 0.0009) | a=7.30241, b=7.53623, c=7.69064, beta=90.8246 |
| MgO | F m -3 m | 0.0704 (formal s.u. 0.0016) | a=4.21234 |

These fractions sum to one over the modeled crystalline material. No amorphous fraction can be obtained from this scan without an internal standard.

## Evidence and model selection

MgWO4 accounts for the dominant reflections, including the lines near 15.93, 19.24, 24.21, 30.81/31.11, 36.79, and 41.86 degrees 2theta. The WO3 assignment is supported by its characteristic resolved group near 23.43, 23.93, and 24.67 degrees and by additional groups between 33-35 and 49-56 degrees. A room-temperature monoclinic P21/n model fit these splittings substantially better than a triclinic model under the same preliminary refinement (Rwp about 10.86% versus 12.4%); the triclinic model also drove a size term to its lower bound. The smaller MgO contribution is independently identified by its Fm-3m lines near 43.21, 62.54, 74.9, 78.9, and 94.3 degrees. The remaining residual maxima coincide with indexed reflections rather than forming a coherent fourth-phase peak set.

Starting structures were COD 9013902 (MgWO4), 1528915 (monoclinic WO3), and 9000499 (MgO). Full-pattern GSAS-II refinement used the stated Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio, the full 9.90-100.09 degree range, an eight-term Chebyshev background, Bragg-Brentano specimen displacement, axial-divergence/profile terms, effective polarization, phase scales, and unit cells. MgWO4 coordinates and the W coordinates in WO3 were refined. The WO3 oxygen coordinates were retained from the literature model because this 15 wt% phase is not sufficiently constrained by Cu X-ray data to refine them reliably; MgO coordinates are fixed by symmetry.

The final fit has Rwp=8.888%, Rp=6.353%, Rexp=2.863%, and goodness-of-fit=3.113 for 8,301 points and 42 refined variables. `fit.csv` defines the difference as observed minus calculated.

## Remaining uncertainty

The tabulated fraction uncertainties are covariance-based statistical values only. Because pointwise uncertainties and a calibrated instrument profile were not supplied, and because specimen displacement and axial-divergence terms are correlated, realistic systematic uncertainty is larger (approximately one absolute weight percent for the principal fractions). Microabsorption or preferred orientation could also bias the scale-derived fractions. Phase identities and the presence of all three phases are secure, but the detailed WO3 oxygen substructure and any amorphous content cannot be determined reliably from this dataset alone.
