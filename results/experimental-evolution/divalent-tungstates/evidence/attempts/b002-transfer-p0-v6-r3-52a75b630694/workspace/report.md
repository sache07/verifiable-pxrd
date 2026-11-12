# Phase analysis and refinement report

The pattern is described by three crystalline phases (fractions normalized over these phases):

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| MgWO4, wolframite type | P 2/c | a = 4.69585, b = 5.68281, c = 4.94671, beta = 90.8249 | 51.19 wt% |
| WO3, monoclinic | P 21/c | a = 7.68599, b = 7.54027, c = 10.5165, beta = 136.044 | 41.36 wt% |
| MgO, periclase | F m -3 m | a = 4.20987 | 7.44 wt% |

The WO3 cell is reported in the oblique P 21/c source setting; it is an alternative basis for the familiar room-temperature monoclinic WO3 structure.

## Evidence and refinement

Wolframite-type MgWO4 accounts for the dominant 18.88°, 23.82°, 30.41/30.73°, 36.29°, and 40.96° features. Monoclinic WO3 is required by the resolved 23.12/23.57/24.38° group and the associated 33–34° peaks. Residual MgO is identified independently by its 42.94°, 62.26°, and 78.88° reflections. No additional crystalline phase is required by an unmatched set of peaks.

Candidate structures were tested by full-pattern Rietveld refinement. The neutron-derived monoclinic WO3 model (COD 2311041) gave Rwp = 2.47%, better than the older rounded monoclinic model (3.52%) and a triclinic model (2.65%); the triclinic refinement was not fully converged and relaxed toward nearly monoclinic angles. The residual WO3 and MgO amounts are also chemically coherent: per 100 g of crystalline material they correspond to about 0.178 mol WO3 and 0.185 mol MgO, consistent with incomplete reaction of a near-1:1 precursor mixture.

GSAS-II used the reported Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio over the full 9.903–100.095° range. Because pointwise uncertainties were absent, Poisson counting weights (w = 1/I) were used. Refined terms included phase scales and cells, a 10-term Chebyshev background, zero offset, one shared Gaussian width term, and effective polarization. A March–Dollase [010] correction was needed for MgWO4, and a single isotropic broadening term was needed for the visibly broader WO3 peaks. Atomic coordinates were held at the reference-model values. The final statistics are Rp = 1.883%, Rwp = 2.470%, Rexp = 1.525%, and GOF = 1.620, with no SVD singularities or parameters frozen at limits.

## Remaining uncertainty

The covariance-only fraction uncertainties in `result.json` are about 0.07–0.10 wt%, but they understate practical uncertainty. Structure choice, preferred orientation, the uncalibrated instrumental profile, and the non-unique separation of WO3 size/strain broadening imply roughly 1–2 wt% absolute uncertainty for the major phases. MgO may have comparable relative systematic uncertainty because no particle-size-dependent microabsorption correction was possible. The data do not determine an amorphous fraction, so the reported fractions apply only to the modeled crystalline material.
