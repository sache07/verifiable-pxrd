# Quantitative phase analysis

## Result

The pattern is described by four crystalline phases. Weight fractions are normalized to the modeled crystalline material; parenthetical uncertainties are the formal one-standard-deviation GSAS-II values.

| Phase | Space group | Weight fraction | Refined cell (Å, °) |
|---|---:|---:|---|
| PbWO4, scheelite | I 41/a | 56.72(12) wt% | a = 5.46603, c = 12.05825 |
| WO3, monoclinic | P 21/c | 21.19(9) wt% | a = 7.69121, b = 7.53458, c = 10.52328, beta = 136.19323 |
| Pb3O4, minium | P 42/m b c | 17.05(12) wt% | a = 8.80101, c = 6.55969 |
| PbO, massicot | P b c m | 5.04(8) wt% | a = 5.87838, b = 5.48491, c = 4.75145 |

The final full-pattern fit has Rwp = 3.1927%, Rp = 2.4327%, and goodness of fit = 1.2876 for 8,301 observations and 38 refined variables. The maximum final shift/esd is 0.0106. The monoclinic WO3 cell is an equivalent, nonstandard P 21/c setting, which accounts for its large beta angle.

## Evidence and model selection

The inventory is chemically consistent with partial reaction of WO3 and Pb3O4 at 500 °C: scheelite PbWO4 is the main product, with residual WO3 and Pb3O4 plus minor PbO. PbWO4 accounts for the strong families at approximately 27.79, 30.01, 33.14, 45.11, 47.36, and 51.57° 2theta. Monoclinic WO3 is required by the resolved 23.52/24.01/24.83° triplet and the 33.67--34.62° group. Pb3O4 supplies coherent peaks including 14.64, 26.79, 31.19, 32.54, 46.47, 52.50, and 66.43°. Massicot is supported by partly isolated or consistently overlapped families near 29.52, 38.23, 45.57, 49.66, 53.58, 60.72, 63.41, and 81.17°.

Exact-composition COD records were screened for occupancy, symmetry, contacts, and fit behavior: PbWO4 COD 9009811, WO3 COD 2311041, Pb3O4 COD 9012124, and PbO COD 2310433 were retained. Alternate scheelite, WO3, and minium records or polymorphs gave inferior common-checkpoint fits. In particular, an initially plausible WO3 record was rejected because it generated a 1.58 Å O--O contact. The retained WO3 model has six-coordinate W, a minimum O--O separation of 2.536 Å, and no GSAS-II short-contact warnings.

The weak-phase challenge strongly supports massicot: removing PbO and reconverging the remaining model raises Rwp to 4.5635%. Substitution by tetragonal litharge drives its scale to the numerical floor (10^-12). Texture tests along symmetry-distinct low-index axes were not replay-stable and were rejected.

## Refinement model

The original, unrounded 9.9034--100.0946° grid was used without resampling. Cu K-alpha1/K-alpha2 wavelengths and the 0.5 intensity ratio were fixed to the metadata. The physically bounded baseline uses an eight-coefficient smooth, positive Chebyshev background, one specimen-height correction (-730 micrometres), a nonnegative common X profile term, fixed polarization at its physical endpoint of 1.0, and minimum fixed axial asymmetry. Roughness, extra zero correction, texture, extinction, HStrain, and unused size/strain terms were neutralized.

Replay-stable isotropic size broadening was retained for PbWO4 (0.0728 micrometres) and Pb3O4 (0.0365 micrometres). Isotropic microstrain was retained for PbO (about 9,324 microstrain); WO3 needed no phase-specific broadening. Isolated low-, middle-, and high-angle families show no remaining systematic position trend, and the calculated background remains positive and smooth.

After the inventory, cells, and profile were stable, the required staged heavy-atom test was run from a saved/reopened project. It accepted W1 and W2 in WO3, Pb2+ in Pb3O4, and Pb in PbO; each move was below 0.094 Å, survived replay, introduced no frozen variables, and passed contact checks. Unsupported symmetry-fixed Pb/W sites in PbWO4 and Pb4+ in Pb3O4 were rejected. The final project was reopened and replayed twice before all CIFs, fractions, statistics, and profile values were exported.

## Remaining uncertainty

The quoted fraction uncertainties are conditional least-squares errors. They do not include phase-model, profile, preferred-orientation, absorption, or counting-statistics model uncertainty; pointwise experimental standard uncertainties were not supplied, so GSAS-II Poisson 1/I weights were used. The absolute amount of amorphous material cannot be determined without an internal standard, and trace crystalline phases below the laboratory-pattern detection limit cannot be excluded.

Oxygen coordinates and displacement parameters are not reliably determined by this Pb/W-dominated laboratory X-ray pattern and were therefore retained from the physically screened literature structures; the submitted CIFs should not be treated as precise oxygen-geometry determinations. The broadening mechanism of the 5 wt% PbO phase is also not uniquely determined: microstrain is the best restrained profile description, but crystallite-size broadening is a close phenomenological alternative.
