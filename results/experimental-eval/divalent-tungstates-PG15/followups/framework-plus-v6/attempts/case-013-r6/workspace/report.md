# Powder XRD phase analysis

The pattern is best represented by five crystalline models. Weight fractions are normalized over these modeled crystalline phases only.

| Phase | Structural model | Weight fraction |
|---|---|---:|
| Stolzite PbWO4 | I 41/a, COD 9009811 | 60.89 wt% |
| Monoclinic WO3 | P 21/c, COD 2311041 | 12.04 wt% |
| Massicot PbO | Pbcm, COD 2310433 | 15.84 wt% |
| Long-period alpha-PbO approximant | Pbcm, COD 1533609 | 7.83 wt% |
| Minium Pb3O4 | P 42/mbc, COD 9012124 | 3.40 wt% |

The full-range read-only GSAS-II replay gives Rwp = 13.607%, Rp = 9.398%, and goodness of fit = 3.890 for 8,282 points. The refined angular zero is +0.28888 degrees. The Cu K-alpha doublet and its stated 0.5 intensity ratio were retained. A smooth six-term Chebyshev background, nonnegative common U/W/X profile, SH/L asymmetry, polarization, phase scales and cells were reconverged. The final replay reports no negative-background, negative-width, occupancy, or displacement-tensor flags, and all five exported CIFs pass the supplied geometry/occupancy screen.

## Evidence

Stolzite accounts for the dominant families at approximately 27.70, 45.02, 51.48, 55.54, 56.81, and 72.3 degrees 2theta. Monoclinic WO3 is required by the characteristic 23.38/23.89/24.65 degree group and additional families near 33.5–34.4 degrees. Massicot accounts for independent groups near 29.3, 30.6, 38.1, 53.4, 60.5, and 63.3 degrees. These three assignments are chemically consistent with the PbO + WO3 precursors heated at 500 degrees C.

The long-period PbO record improves several coherent weak and partly overlapped families and was materially better than litharge or an extra PbWO4 polymorph under a common nuisance model. It is retained as a commensurate approximant to the reported incommensurate alpha-PbO structure; GSAS-II does not model the modulation here. The weak Pb3O4 model is supported by multiple partly overlapped families: removing it and reconverging raised Rwp by about 0.25 percentage point. Raspite PbWO4, litharge PbO, Pb-W-O superstructures, reduced tungsten oxides, and alternative WO3 records were challenged and either refined to negligible scale, lacked coherent multi-family support, or were physically inferior. In particular, the selected WO3 record avoids the short O--O contact of the best-fitting older alternative.

Published symmetry-constrained coordinates and occupancies were retained while cells were refined. Coordinate trials, especially oxygen coordinates in PbWO4 and WO3, were too correlated with profile/background terms or moved beyond physically justified bounds. A Uiso grid favored the registered 0.005 A2 value. Principal-phase size terms were stable; broad PbO features required size/strain modeling, with [100] March-Dollase texture for massicot. Roughness, unsupported texture axes, and bound anisotropic-strain combinations were rejected.

## Remaining uncertainty

The stolzite and WO3 identifications are reliable. The massicot fraction is less certain because its broad peaks couple scale, strain, size, and texture. The 7.83 wt% long-period PbO fraction and its detailed structure are only moderately to weakly determined: it is an approximant, it overlaps massicot strongly, and its profile terms are broad. The 3.40 wt% Pb3O4 assignment and fraction are low confidence because the phase is weak and mostly overlapped; the data do not determine its atomic coordinates independently. These two minor fractions should therefore be treated as approximate rather than precise quantitative values.

There remains a positive residual near 25.9 degrees and structured mismatch across roughly 29–31 degrees. No screened candidate produced a reliable set of additional unique peak families, so a further trace phase cannot be identified or quantified defensibly. Rwp and goodness of fit show that the model has not reached the counting-noise floor. No amorphous content was measured, and the reported fractions must not be interpreted as absolute whole-sample fractions.

`fit.csv`, all five CIFs, and the reported fractions were exported from the same saved `final.gpx` parameters. A fresh full-range replay optimized zero parameters and reproduced the submitted profile exactly.
