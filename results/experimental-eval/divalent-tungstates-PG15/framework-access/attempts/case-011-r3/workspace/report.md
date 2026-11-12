# Powder XRD phase analysis

The pattern is modeled as two crystalline precursor phases, with no additional crystalline product required by the data.

| Phase | Structure | Refined cell | Crystalline weight fraction |
|---|---|---|---:|
| WO3 | monoclinic, P 21/c | a = 7.70236 Å, b = 7.54569 Å, c = 10.55124 Å, beta = 136.1092° | 0.7324 (about 73.2 wt%) |
| MnO2 | pyrolusite, P 42/m n m | a = 4.40490 Å, c = 2.87689 Å | 0.2676 (about 26.8 wt%) |

## Evidence and refinement

The resolved WO3 fingerprint includes the low-angle group at 23.44, 23.93, and 24.69° 2theta and its associated 33–34° and 49–50° families. The remaining strong lines at approximately 29.01, 37.68, 56.96, and 72.53° match rutile-type pyrolusite MnO2. Together these phases account for all prominent peaks; in particular, a separate MnWO4 phase is not needed. This is chemically consistent with incomplete reaction of the stated MnO2 and WO3 precursors after heating at only 300 °C.

Published COD models 2311041 (WO3) and 1514110 (MnO2) were used as parents. A GSAS-II Rietveld refinement used the reported Cu Kalpha1/Kalpha2 wavelengths and intensity ratio, then refined phase scales, cells, profile terms, crystallite-size/microstrain terms, background, specimen/angular corrections, and a March–Dollase term for MnO2. Atomic coordinates were kept near the published parents and isotropic displacement factors were fixed to avoid unstable coordinate/thermal correlations. Weight fractions were calculated from refined phase scale times unit-cell mass.

An independent forward replay of `final.gpx`, using fresh GSAS-II reflection lists and no additional fitting, gives Rwp = 5.4166%, Rp = 3.9738%, chi-square = 33576.49, and GOF = 2.016 for 8,301 points and 40 refined variables. The calculated profile is nonnegative over the complete measured range. `fit.csv` is this replayed profile, with difference defined as observed minus calculated.

## Remaining uncertainty

The phase chemistry and two-phase inventory are well supported, but the exact low-symmetry distortion of WO3 is not unique from this powder pattern. A triclinic P-1 WO3 alternative gave an essentially indistinguishable Rwp (about 5.411% versus 5.417%) while requiring more structural freedom; the monoclinic P 21/c model was retained as the parsimonious room-temperature assignment. Thus the detailed WO3 oxygen coordinates should not be treated as uniquely determined.

No pointwise uncertainties were supplied, so Poisson counting weights were used and the reported fraction uncertainty is a sensitivity estimate rather than a formal standard uncertainty. Reasonable WO3 symmetry and displacement-factor alternatives changed the phase fractions by roughly 1.5 percentage points; about ±2 wt% absolute is a prudent uncertainty for each normalized crystalline fraction. Trace crystalline phases below the pattern's detection limit and amorphous content cannot be excluded, and the fractions do not quantify such material.
