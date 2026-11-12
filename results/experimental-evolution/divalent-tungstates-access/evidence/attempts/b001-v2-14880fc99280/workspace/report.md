# Powder XRD phase analysis

The crystalline assemblage is scheelite CaWO4 with residual monoclinic WO3 and calcite CaCO3. The refined fractions below are normalized over these modeled crystalline phases; the experiment does not provide an amorphous-content standard.

| Phase | Structural model | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| CaWO4 | Scheelite, `I 41/a`, COD 7219229 | a = 5.23957, c = 11.33835 | 0.7911 (79.11 wt%) |
| WO3 | Monoclinic gamma-WO3, `P 21/c`, COD 2311041 | a = 7.69576, b = 7.55870, c = 10.52001, beta = 135.9446 | 0.1369 (13.69 wt%) |
| CaCO3 | Calcite, `R -3 c`, COD 1547347 | a = 4.99125, c = 17.06350 | 0.0721 (7.21 wt%) |

## Evidence

The dominant scheelite sequence accounts for the strong groups near 18.3, 28.4–28.8, 31.3, and 33.9° 2θ. The split WO3 group near 22.76, 23.18, and 23.98° and its many weaker reflections require the monoclinic model. In common-state replacement tests, alternative WO3 references COD 1528915 (`P 21/n`) and COD 2106293 (`P -1`) gave replayed Rwp values of 3.760% and 4.015%, respectively, versus 3.386% for COD 2311041 at that stage. A fergusonite CaWO4 replacement gave Rwp 35.10%, decisively favoring scheelite.

After fitting CaWO4 and WO3, coherent residuals at about 29.1, 39.2, 42.8, 48.2, and 57° matched calcite. Removing calcite from the final fixed common state raises Rwp from 3.366% to 3.684%. Independent calcite-scale trials started at 0.01, half the fitted value, and twice the fitted value all converged to scale 3.0223 and 7.209 wt%; analogous WO3 trials likewise converged to 13.685 wt%. Thus neither plausible precursor scale collapses. The final composition is also chemically coherent for incomplete reaction of the stated WO3 and CaCO3 precursors: on a molar basis the modeled total Ca:W ratio is about 1.04:1.

After calcite was included, the remaining largest smoothed residual features coincided with reflections of the three modeled phases rather than forming an independent unindexed peak set. Residual-directed analogue/prototype additions were therefore not warranted. Failed alternative-import/refinement trials were treated as unknown, not as phase exclusions.

## Fit and checks

The final fresh GSAS-II forward replay uses the full 9.90343-100.09455 degree grid (8,301 points) and gives Rwp = 3.3665%, Rp = 2.6129%, and chi-square per point = 1.1507 for Poisson weights. The counting-statistics Rwp floor is 3.1382%. A native replay regenerated structure factors and reflection lists from `final.gpx`; it reproduced `fit.csv` to below 1e-12 count and reported no negative-width, negative-background, displacement-parameter, or polarization review flags.

All exported CIFs pass the supplied occupancy/contact screen: no contact is below 0.8 Å and no O–O contact is below the 1.8 Å review threshold. Preferred orientation and uniaxial-strain trials were unsupported; isotropic broadening was retained.

## Remaining uncertainty

Phase identities are high confidence. The tabulated fractions should not be interpreted to four-digit accuracy: no pointwise uncertainties or external quantitative standard were supplied, and scale factors correlate with displacement parameters, background, crystallite broadening, and possible microabsorption. Model-sensitivity trials indicate that approximately 1–2 wt% absolute is a more realistic practical precision, with the 7 wt% calcite fraction least certain.

Oxygen coordinates, especially in WO3 and calcite, are not independently precise from this laboratory powder pattern. They were allowed only physically screened, bounded departures from the reference structures. Thus the CIFs are suitable phase/profile models, but detailed bond distortions and the last digits of oxygen positions should not be treated as reliably determined.
