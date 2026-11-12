# PXRD phase analysis

The pattern is modeled with three crystalline phases. The two major phases are unreacted BaCO3 and WO3; a small, tentative amount of the expected reaction product BaWO4 is also supported. Weight fractions are normalized over these modeled crystalline phases.

| Phase | Structural model | Weight fraction |
|---|---|---:|
| BaCO3 | Pnma, COD 9010928 | 53.57 wt% (formal s.u. 0.13 wt%) |
| WO3 | P21/c, COD 2311041 | 45.85 wt% (formal s.u. 0.13 wt%) |
| BaWO4 | I41/a scheelite prototype | 0.582 wt% (formal s.u. 0.047 wt%) |

The final full-range refinement (9.9034–100.0949 degrees 2theta) has Rwp = 7.149%, Rp = 5.570%, Rexp = 3.481%, and goodness of fit = 2.057. The project converged after save/reopen replay with a maximum final shift/s.u. of 0.00043.

## Evidence and model selection

BaCO3 accounts for coherent families near 24.20/24.57, 34.04–34.86, 42.29, 47.06–47.27, and 68.38–71.23 degrees. Monoclinic WO3 accounts for the 23.40/23.89/24.64 triplet, the 33.55–34.45 group, and families near 47.50, 50.16, 55.62–56.24, and 76.46–78.73 degrees. Their refined cells and full-occupancy source coordinates give sensible geometry; representative distances are C–O >= 1.275 A in BaCO3 and W–O = 1.715–2.160 A in WO3.

Several WO3 records and polymorphs were challenged under a common restrained profile. The selected room-temperature P21/c neutron model and a near-monoclinic P-1 low-temperature model fit almost indistinguishably (two-phase Rwp 7.259% versus 7.253%, with two additional cell variables for P-1). An older monoclinic record was worse (Rwp 8.14%), and an orthorhombic high-temperature model was rejected (Rwp about 13.4% and an unphysical scale). P21/c was retained for ambient-phase plausibility and parsimony, but the powder data do not reliably distinguish P21/c from the metrically near-monoclinic P-1 alternative.

The available exact BaWO4 database record contained split, half-occupied oxygen sites with implausible alternate contacts. A cross-chemistry search instead identified full-occupancy scheelite BaMoO4 (COD 2300459); isovalent Mo6+ to W6+ substitution produced an ordered BaWO4 model with W–O = 1.723 A and Ba–O = 2.774–2.814 A. Its cell and coordinates were fixed because the trace signal cannot determine them. The scale is supported mainly by partly overlapped families at 26.76, 43.26, 53.87, and 54.77 degrees. Under the final common profile, adding this phase lowered Rwp from 7.2135% to 7.1491% and chi-squared by about 633 for one variable. Starting its scale near zero and deliberately high both returned 0.5815 wt%. Its nominally more isolated 28.35 and 32.17 degree lines are too weak for decisive confirmation, so the phase assignment and exact fraction remain tentative.

Other chemically plausible Ba-W-O phases were screened, but their dominant expected families were absent. In particular, the strongest lines expected for Ba3W2O9 and Ba3WO6 near 26–31 and 29/42 degrees, respectively, are not present as coherent unmatched sets.

## Refinement adequacy

The final baseline uses the specified Cu Kalpha1/Kalpha2 doublet, one refined zero correction (+0.3151 degrees), a positive smooth eight-term Chebyshev background, and nonnegative low-dimensional U/X common broadening with W fixed at zero. Background values remain positive (about 189–2286 counts). Low-, middle-, and high-angle peak families were inspected for position, width, and asymmetry; isolated major-phase centroids generally agree within one to a few data steps, with no systematic angular drift. Releasing SH/L or roughness produced worse, negative, or highly correlated terms and was rejected.

Neutral phase size/strain and texture models were challenged one phase at a time. The retained additions are weak BaCO3 [110] March-Dollase texture (0.9059) and replay-stable WO3 [0 1 1] uniaxial Gaussian microstrain (about 7082/4505 microstrain). Isotropic or uniaxial BaCO3 broadening, WO3 size, additional WO3 texture, and combined size/strain terms were unsupported, bound, negative, or strongly correlated and were pruned. Atomic coordinates and displacement parameters were not refined because this overlapped laboratory pattern does not constrain them reliably.

## Remaining uncertainty

The covariance s.u. values in the table are precision estimates, not total uncertainties. Source choice, WO3 symmetry, profile shape, and preferred orientation imply a more realistic uncertainty of roughly 0.5–1 wt% for each major phase. The WO3 space-group choice cannot be made uniquely from this dataset. For BaWO4, neither its structure parameters nor a precise fraction can be determined reliably; 0.582 wt% should be read as an indicative approximately 0.6 wt% trace level, with systematic uncertainty larger than its formal 0.047 wt% s.u.

`final.gpx`, the three submitted CIFs, `fit.csv`, and `result.json` were exported from the same reopened final project. The profile arrays, cells, fractions, and fit statistics were checked against that project exactly (CSV rounding below 5e-9 counts).
