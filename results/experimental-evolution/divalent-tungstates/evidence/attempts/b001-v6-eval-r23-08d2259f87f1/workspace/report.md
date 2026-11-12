# PXRD phase analysis

The pattern is modeled by three crystalline phases: scheelite SrWO4, monoclinic WO3, and orthorhombic SrCO3. This is chemically consistent with partial reaction of the reported WO3/SrCO3 precursor mixture at 650 °C.

| Phase | Space group | Crystalline weight fraction |
|---|---:|---:|
| SrWO4 | I 41/a | 61.71(14)% |
| WO3 | P 21/c | 22.97(11)% |
| SrCO3 | P n m a | 15.32(15)% |

The fractions sum to 100% over the modeled crystalline phases. The parenthetical uncertainties are covariance-derived formal ESDs; texture and reference-structure choices give a more realistic systematic uncertainty of roughly 1–2 weight-percentage points. No amorphous fraction can be obtained from these data without an internal standard.

## Phase evidence and model selection

SrWO4 accounts for the dominant scheelite reflection families. No exact SrWO4 entry was present in the supplied index, so the analogue search was used. Several I 41/a parents were inspected. A direct SrMoO4 analogue (COD 2300460), an EuWO4 analogue, and isovalent CaWO4 (COD 7219229) were replayed under the same background, scale, cell, texture, and profile model. The CaWO4 oxygen geometry with Ca replaced by Sr gave the best physically acceptable fixed-coordinate model (Rwp 3.918% before the final anisotropic-width challenge, versus 4.095% for EuWO4 and 4.238% for the initial SrMoO4 model). In the refined SrWO4 cell it gives four W–O distances of 1.822 Å and eight Sr–O distances of 2.549–2.565 Å. An unconstrained oxygen-coordinate trial lowered Rwp in the initial model but expanded W–O to 1.97 Å, so it was rejected as an intensity-model surrogate. The submitted SrWO4 coordinates and displacement factors are therefore fixed prototype values; only its cell, scale, and texture were refined.

WO3 is represented by ambient monoclinic P 21/c COD 2311041 in its valid nonstandard setting. Other supplied records were tested: P21/n COD 1528915 fit less well, several P21/m/Pnma/P21/c records failed to converge physically, and triclinic P-1 COD 2106293 was nearly competitive. Under a matched nuisance model the monoclinic and triclinic fits were Rwp 4.238% and 4.245%, respectively. The monoclinic assignment is preferred because it is slightly better and is consistent with ordinary ambient WO3; nevertheless, the exact low-symmetry WO3 polymorph is less certain than the WO3 chemical-phase identification.

SrCO3 is the ambient Pnma form (COD 9008198). Its scale initially collapsed when the database cell was used unchanged, but a reversible 0.45% expanded-cell seed brought coherent 111/102/211/013/122 families near 24.65, 25.29, 35.67, 36.07, 43.67, and 49.46° 2theta into registration. The phase then converged reproducibly to 15.3 wt%. Removing its texture term worsened Rwp from 3.637% to 3.716%, and removing the phase leaves coherent residual families, so it is retained.

The exact-composition candidate Sr3W2O9 (COD 2311977) was re-challenged under the accepted common profile. It refined to only 0.10(6) wt%, changed Rwp by less than 0.001 percentage point, and had no convincing unique residual family. That trace cannot be determined reliably and is not included in the reported crystalline fractions.

## Refinement and profile adequacy

The final refinement covers the complete measured range, 9.9034–100.0946° 2theta, with the reported Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio fixed. It uses a smooth six-term Chebyshev background, one specimen-displacement correction, and a common nonnegative profile with U = V = Y = 0, W = 39.230, X = 4.165, and fixed SH/L = 0.002. Releasing U made it negative and was rejected. Releasing SH/L after the width model was established gave no material improvement and was 95% correlated with displacement, so it was pruned. A zero-only correction converged at Rwp 3.666%, compared with 3.637% for specimen displacement, and left a less satisfactory angle-dependent position match. The refined displacement is large, +1056.5 micrometres, so absolute cell dimensions remain conditional on the instrument/sample-height calibration.

Isotropic WO3 domain size improved the common-profile fit, and symmetry-distinct uniaxial trials then favored the [010] axis. The accepted equatorial and axial sizes are 0.408(29) and 0.0742(16) micrometres; their mutual correlation is only 0.14. Alternative [100], [001], and [10-1] axes gave Rwp 3.812%, 3.715%, and 3.898%. Size terms for SrWO4 and SrCO3 were unsupported, while strain trials became negative or strongly redundant and were rejected. March–Dollase terms were retained for SrWO4 [110], WO3 [10-1], and SrCO3 [001]; removing them one at a time gives Rwp 5.065%, 5.294%, and 3.716%, respectively. These texture corrections are a principal source of systematic uncertainty in the fractions.

The final fit has Rwp = 3.6375%, Rp = 2.7683%, and goodness of fit = 1.2733 for 8301 observations and 26 refined variables. Low-, middle-, and high-angle isolated families show consistent positions and broadly adequate FWHM; the smooth difference curve has residual intensity around known overlapping/strong reflections but no remaining coherent unindexed family. Pointwise uncertainties were not supplied, so the goodness of fit and formal ESDs use GSAS-II counting-statistics weights derived from the observed counts.

The saved project was reopened and replayed over the full range to a maximum shift/ESD of 0.00015. The three CIFs and `fit.csv` were exported directly from that final `final.gpx`; in `fit.csv`, difference is observed minus calculated.
