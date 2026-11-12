# Quantitative phase analysis

## Result

The modeled crystalline material is **NiWO4 (wolframite, P2/c)** plus **monoclinic WO3 (P21/n)**. Fractions normalized over these modeled crystalline phases are **76.39 wt% NiWO4** and **23.61 wt% WO3**. The covariance-derived formal standard uncertainty is about 0.10 wt% for each fraction, but a more realistic model/systematic uncertainty is approximately 1 wt% because source/profile and structural-model choices dominate the counting-statistical value. No amorphous fraction can be obtained from this analysis, so these values are not absolute bulk fractions.

The full-range final replay gives Rwp = 4.612%, Rp = 3.594%, Rexp = 3.479%, and GOF = 1.328 for 8282 observations from 10.00943 to 99.99442 degrees 2theta.

## Evidence and model selection

The 900 C NiO + WO3 reaction context supports NiWO4 formation. NiWO4 is required by coherent families near 19.19, 23.91/24.85, 30.87, 36.52, 41.63, and 54.58 degrees. Residual monoclinic WO3 is independently required by its split low-angle cluster at 23.06, 23.53, and 24.28 degrees and families near 26.53, 28.82, 33.20/34.09, and 55.88 degrees.

Inventory challenges used the same restrained nuisance model. A neutron-derived monoclinic WO3 record, transformed exactly to the conventional near-orthogonal P21/n setting, gave Rwp 5.558% before later nuisance/coordinate tests; an older rounded monoclinic record gave 5.979%, while triclinic WO3 gave 5.584% despite three additional cell freedoms. A single-wavelength source model gave 6.991%, supporting the reported Cu Kalpha1/Kalpha2 pair and fixed 0.5 intensity ratio. For NiWO4, the exact P2/c record decisively outperformed fully occupied Ni-substituted ZnWO4, MgWO4, and MnWO4 prototypes (Rwp 5.55% versus 7.46%, 6.98%, and 7.45%, respectively). All screened structures had sensible occupancy and octahedral coordination before fitting.

NiO was reintroduced under the final common profile with its cell fixed. It refined to only 0.21 +/- 0.09 wt% and improved Rwp by 0.0014 percentage point; its diagnostic 43.3 degree family is absent. This is below reliable detection and NiO is therefore excluded rather than reported as a phase. The trial implies an approximate 3-sigma upper level near 0.5 wt% under this model.

## Refinement and physical checks

The common baseline uses a 10-coefficient smooth Chebyshev background, one zero correction (-0.09370 degrees), nonnegative U/W/X profile terms (12.682, 36.418, 7.870), and refined polarization (0.6748). V/Y/Z are zero, SH/L is fixed at 0.002, sample shift/transparency/roughness are neutral, and phase size terms are fixed at the effectively neutral 10 micrometre limit. Low-, middle-, and high-angle isolated families show no systematic position or common-width drift. WO3 alone supports replay-stable isotropic microstrain (1060 microstrain); WO3 size runs to the neutral bound. NiWO4 isotropic strain runs to zero, while its apparent size term is bound when tested alone and becomes more than 0.90 correlated with common X and WO3 strain when combined; all are therefore rejected.

Symmetry-distinct [100], [010], [001], and [101] March-Dollase trials were compared. WO3 ratios remained statistically indistinguishable from random orientation. NiWO4 supports a small [001] correction (MD = 0.99004); improvements occur across several isolated families rather than one line. Surface roughness was rejected: its two-parameter test drove A to its lower bound and correlated B by more than 0.90 with both phase scales. Refining SH/L was likewise rejected because it was 0.98 correlated with zero.

The refined Ni coordinate is y = 0.661157; the other NiWO4 atom coordinates remain at the selected exact-record values. Unrestrained oxygen-coordinate refinement lowered Rwp but produced an under-bonded W coordination and was rejected. WO3 coordinates remain those of the neutron parent. Thus the cells, phase fractions, Ni position, and heavy-atom framework are supported by this laboratory pattern, but detailed oxygen positions are not independently determined reliably.

`final.gpx`, the two exported CIFs, `fit.csv`, and `result.json` all come from the same final save/reopen/replay state.
