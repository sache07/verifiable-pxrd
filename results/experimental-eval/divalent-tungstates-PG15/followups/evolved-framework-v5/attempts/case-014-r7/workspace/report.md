# Powder XRD phase analysis

## Result

The best physical full-pattern model contains four crystalline phases. Fractions are normalized over those modeled crystalline phases only.

| Phase | Space group | COD starting model | Weight fraction | Assessment |
|---|---:|---:|---:|---|
| SrWO4, scheelite | I 41/a | 1546036 | 70.82(25)% | Reliable identification |
| WO3, monoclinic | P 21/c | 2311041 | 10.22(17)% | Reliable identification |
| Sr3W2O9 | C 2/c | 2311977 | 10.24(30)% | Tentative exact topology/fraction |
| SrWO4, fergusonite | I 2/a | 1546037 | 8.71(22)% | Tentative exact topology/fraction |

The parenthesized uncertainties are GSAS-II formal standard uncertainties, not realistic total uncertainties. The two SrWO4 polymorphs total 79.54 wt% on this crystalline-only basis.

## Evidence and model selection

The model was refined against all 8,282 original points from 10.0094 to 99.9944 degrees 2theta, using the reported Cu Kalpha1/Kalpha2 wavelengths (1.540598/1.544426 A) and 0.5 intensity ratio. Since the input supplies counts but no pointwise uncertainties, Poisson working uncertainties, sigma = sqrt(counts), were used.

Scheelite SrWO4 accounts for the dominant reflection family. Monoclinic WO3 is independently required by its characteristic group near 23.45, 23.97, and 24.73 degrees and supporting reflections across the scan. After those two phases were fitted, Sr3W2O9 indexed a coherent residual family, notably near 32.6 and 44.67 degrees and through the 56--61 degree region. The fergusonite model accounts for the split feature near 29.75 degrees and a supporting family at higher angles. Adding Sr3W2O9 lowered a preliminary two-phase Rwp from about 17.6% to 14.9%; adding fergusonite lowered it by a further approximately 0.9 percentage point. A four-phase Le Bail diagnostic reached about 8.9% Rwp, supporting the accepted peak-position inventory while showing that much of the remaining Rietveld residual is intensity/profile related.

Tests of the reported precursors did not support additional crystalline phases: SrCO3 refined to zero scale, while SrO contributed only about 0.4 wt%, improved Rwp by only 0.03 percentage point, required a contracted cell, and did not explain a broad reflection family. Those phases were therefore excluded. An alternative WO3 reference gave a marginal numerical change but produced an unphysical 1.58 A O--O contact; the physical P 21/c model was retained.

The submitted model is a Rietveld model, not a Pawley or Le Bail endpoint. Cell, scale, background, bounded heavy/light-coordinate, and supported profile/texture refinements were staged with rollback of nonphysical branches. Independent CIF parsing reproduced all formulas and cells; the shortest periodic contacts are 1.93 A in scheelite, 1.73 A in WO3, 1.75 A in Sr3W2O9, and 1.79 A in fergusonite, with chemically plausible W--O coordination.

## Fit and uncertainty

The final fit has Rwp = 13.061%, Rp = 9.469%, Rexp = 3.529%, and goodness of fit = 3.701 for 8,282 observations and 30 variables. The stored GSAS-II Durbin--Watson statistic is 0.173, so the remaining residuals are strongly correlated rather than counting-noise limited.

Scheelite and WO3 are reliably identified, but their quoted formal fraction errors still understate profile/calibration systematics. The exact Sr3W2O9 and fergusonite assignments and their individual fractions cannot be claimed at formal-error precision. Both starting topologies come from high-pressure-related references, their refined cell volumes are about 5% below those references, and their scales correlate with overlap and preferred orientation. They are the best coherent family-wide matches found, but the defensible interpretation is approximately 10 wt% Sr3W2O9 and 9 wt% fergusonite, not sub-percent accuracy.

The calibration/profile model also reached practical bounds (sample displacement -800 micrometres, zero offset -0.105 degrees, and bounded U/W terms), which adds systematic uncertainty to absolute cells and fractions. One isolated positive residual centered near 30.895 degrees remains unindexed. It is insufficient to identify or quantify a fifth phase reliably, so no fifth phase is reported. Amorphous material was not quantified; all fractions are normalized over the modeled crystalline phases.
