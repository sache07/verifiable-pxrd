# Powder XRD phase analysis

## Result

The specimen is a three-phase crystalline mixture dominated by unreacted precursor phases, with only trace scheelite product. Fractions are normalized over the modeled crystalline phases:

| Phase | Space group | Weight fraction | Formal 1σ |
|---|---|---:|---:|
| BaCO3 (witherite) | Pmcn, No. 62 | 52.84 wt% | 0.17 wt% |
| WO3 (monoclinic) | P21/c, No. 14 | 46.65 wt% | 0.16 wt% |
| BaWO4 (scheelite) | I41/a, No. 88 | 0.51 wt% | 0.05 wt% |

The full-grid GSAS-II fit uses all 8301 measured points from 9.903433 to 100.094885° 2θ. Fit statistics are Rwp = 6.6507%, Rp = 5.0148%, Rexp = 3.4807%, and goodness-of-fit S = 1.915.

## Evidence and model choice

The BaCO3 and WO3 assignments are chemically expected from the stated BaCO3 + WO3 precursor mixture heated at only 400 °C, and each is supported across the pattern rather than by a single line. The final reflection lists contain 181 BaCO3 and 440 WO3 reflections. Representative strong calculated positions are 24.219, 34.877, 42.307, 45.166, and 47.075° for BaCO3, and 23.427, 23.909, 24.662, 34.464, 50.172, and 56.169° for WO3. Exact-composition WO3 references were screened in the same multiphase fit; COD 2311041 gave the broad, coherent family match and a physical octahedral W–O geometry.

BaWO4 is supported by a stable positive scale and a family of scheelite reflections, including 26.793, 43.312, 49.072, 53.864, 54.798, 68.116, and 69.309° 2θ. Its scale remains near 0.5 wt% when the oxygen model is changed. Remaining large residual extrema sit on accepted-phase peaks and alternate in sign, indicating imperfect intensity/profile descriptions rather than a separate coherent reflection family. No fourth crystalline phase was justified.

The BaCO3 topology and Ba sublattice began from COD 9010928. Its published carbonate coordinates contain a 1.407 Å C–O bond, so the same-topology regular carbonate group from COD 1011149 was mapped into that Pmcn setting and held fixed; the submitted model has C–O = 1.239–1.241 Å and Ba–O = 2.710–2.920 Å. This physical model was selected even though the distorted source coordinates lower Rwp by 0.029 percentage point. The WO3 model is COD 2311041 with refined W positions and fixed parent O positions; its two W sites have six W–O distances spanning 1.720–2.199 Å. The trace BaWO4 CIF is a full-occupancy scheelite model derived from BaMoO4 COD 2300459 by Mo→W substitution and a fitted BaWO4 cell; it gives four W–O bonds of 1.721 Å. The sole exact-composition BaWO4 reference available in the frozen index (COD 1527204) was rejected because split half-occupancy O sites produced 1.46 Å W–O and 1.16 Å O–O contacts.

## Uncertainty

The quoted standard uncertainties are covariance-derived counting-statistics values and do not include model selection, background/profile correlation, preferred orientation, microabsorption, or amorphous material. With no internal standard, amorphous content and absolute specimen composition cannot be determined; only crystalline-normalized fractions are reported. The two major fractions are well supported, but the BaWO4 amount should be read as about 0.5 wt%, with systematic uncertainty plausibly larger than its formal ±0.05 wt% (roughly ±0.1 wt% is more realistic from model branches).

Light-atom coordinates and displacement parameters are not independently determined by this heavy-atom-dominated laboratory X-ray pattern. Unconstrained O refinements generated implausible bonds and were rolled back. The BaWO4 oxygen coordinates are analogue-derived, so the scheelite topology and reflection family are supported but its detailed oxygen structure is not reliably refined here. WO3 isotropic displacement entries retained from the source include zero placeholders; they must not be interpreted as measured thermal motion. Because no calibrated instrumental profile was supplied, instrument broadening, crystallite size, and microstrain are also not uniquely separable; bounded physical profile/strain terms were used only to describe peak shapes.
