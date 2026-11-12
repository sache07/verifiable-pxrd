# Powder XRD phase analysis

The crystalline specimen is modeled by three phases: wolframite MnWO4, Mn3WO6, and monoclinic WO3. This inventory is chemically ordinary for an 800 °C reaction of WO3 with Mn3O4, and every coherent reflection family in the measured range is indexed by these phases.

| Phase | Space group | Refined cell (Å, °) | Crystalline weight fraction |
|---|---|---|---:|
| MnWO4 | P 2/c | a = 4.79767, b = 5.70863, c = 4.97588, β = 91.1628 | 0.63337 (63.34 wt%) |
| Mn3WO6 | R -3 | a = b = 8.89173, c = 10.48624 | 0.17993 (17.99 wt%) |
| WO3 | P 21/n | a = 7.28886, b = 7.52964, c = 7.68825, β = 90.7461 | 0.18670 (18.67 wt%) |

## Evidence and refinement

MnWO4 accounts for the dominant families near 15.26, 18.26, 23.49, 29.78/30.23, and 37.21° 2θ. Mn3WO6 is required by a separate coherent set including the 19.6–20.2, 28.5, 31.7, 35.0, 46.4, and 55–56° regions. Monoclinic WO3 accounts for the characteristic 22.9/24.1° pair and the 33–34° multiplet, plus their higher-angle partners. A Mn3O4 precursor model was not retained: its unique strong lines are absent and no stable positive contribution was supported. Residual extrema remain centered on reflections of the three accepted phases rather than forming an unindexed family.

Starting structures were exact-composition COD references 1520200 (MnWO4), 2002703 (Mn3WO6), and 2311041 (WO3). The WO3 reference was expressed in an equivalent Niggli-reduced P 21/n setting; stoichiometry, connectivity, and atomic topology were unchanged. A competing WO3 reference with a slightly attractive profile fit was rejected because it contained an unphysical approximately 1.58 Å O–O contact. Coordinate corrections were bounded to approximately 0.05 Å RMS from the physical references (largest individual shift 0.068 Å).

The full 9.9034–100.0946° grid was refined with the reported Cu Kα1/Kα2 wavelengths and intensity ratio, counting-statistical weights because point uncertainties were not supplied, a 12-term smooth Chebyshev background, Bragg–Brentano specimen displacement, bounded isotropic size/strain broadening, and March–Dollase texture. The supported texture terms are MnWO4 [111] r = 1.158, Mn3WO6 [110] r = 1.101, and WO3 [010] r = 1.303. Sizes are 0.050, 0.040, and 0.050 μm for MnWO4, Mn3WO6, and WO3; corresponding microstrains are 1800, 8000, and 1000 ppm. The Mn3WO6 strain reaches the tested physical ceiling and should be regarded as a broadening descriptor rather than a precise microstrain measurement.

The final fit gives Rwp = 3.1523%, Rp = 2.2861%, Rexp = 1.4263%, and goodness-of-fit = 2.2125 for 8301 observations. Independent atomic forward replay regenerated the complete profile without cached calculated intensities and matched `fit.csv` to below 5 × 10^-9 counts. It found positive phase scales, background, and analytic peak widths, with no profile-review flags. Final minimum contacts are physically plausible: O–O = 2.431/2.622/2.549 Å for MnWO4/Mn3WO6/WO3, respectively; the shortest W–O distances are 1.812, 1.923, and 1.666 Å.

## Remaining uncertainty

The phase identities and three-phase inventory are reliable. The fractions are normalized only over modeled crystalline material; amorphous content cannot be measured from this analysis. Formal scale-derived fraction e.s.d.'s are only 0.05–0.07 wt%, but they omit systematic uncertainty from texture, absorption, overlap, and structural-model choice. A more realistic interpretation is about ±2 wt% absolute for each fraction.

The refined angular zero (0.2003°) and specimen displacement (789 μm) are physically allowed but 99.91% correlated, so neither calibration value is independently reliable. The heavy-atom frameworks are well constrained; individual oxygen coordinates, especially in distorted WO3, are less certain from this overlapping laboratory X-ray pattern. No additional crystalline phase can be justified from the residual.
