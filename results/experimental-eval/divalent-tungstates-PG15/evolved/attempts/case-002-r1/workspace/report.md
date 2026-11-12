# Crystalline phase analysis

The modeled crystalline fraction is:

| Phase | Space group | Weight fraction | Assessment |
|---|---:|---:|---|
| WO₃, triclinic | P-1 | 63.874% | High confidence; formal s.u. 0.174 percentage point, estimated model uncertainty about ±2 points |
| BaO₂, tetragonal | I4/mmm | 34.718% | High confidence; formal s.u. 0.180 point, estimated model uncertainty about ±2 points |
| BaO, rocksalt | Fm-3m | 0.978% | Moderate confidence; formal s.u. 0.073 point, estimated model uncertainty about ±0.5 point |
| Ba₃W₂O₉, rhombohedral | R-3c | 0.430% | Tentative trace phase; formal s.u. 0.104 point, estimated model uncertainty about ±0.3 point |

Fractions are normalized to 100% over these modeled crystalline phases. No amorphous fraction can be obtained reliably from this dataset.

## Evidence

Triclinic WO₃ accounts for the diagnostic 23.39/23.89/24.59° group and its repeated split families through the full range. A physically sound P-1 record (COD 2106293) gave a substantially better common-profile fit than physical monoclinic and orthorhombic alternatives (two-phase replay Rwp 13.10%, 14.75%, and 17.82%, respectively). BaO₂ is independently supported by families near 26.28, 27.04, 33.51, 42.94, 46.59, 47.96, and 53.73°. Rocksalt BaO improves partly isolated 200 and 220 families near 32.84° and 46.98°, together with several higher-angle families.

Ba₃W₂O₉ is retained only provisionally. Its fixed literature model gives coherent partly isolated 110, 104, and 300 families near 17.77°, 27.75°, and 30.81°; the 30.81° residual window improves strongly. Removing it and reconverging raises Rwp from 8.7410% to 8.7490%, so its fraction is much less secure than the major phases.

BaWO₄ was specifically re-challenged with two ordered, physical scheelite prototypes after the common profile and phase-specific widths were established. Both scales collapsed to zero. The exact COD record with split half-occupied oxygen also had unphysical short contacts. BaWO₄ is therefore not reliably detected; a model-dependent practical upper bound is roughly 0.5 wt%. Ba₃WO₆ and Ba₀.₁₅WO₃ gave only sub-percent, profile-sensitive scales without sufficient independent family support and were not included.

## Refinement and limitations

The final GSAS-II model uses the reported Cu Kα₁/Kα₂ wavelengths and 0.5 intensity ratio, a smooth six-term Chebyshev-1 background, one specimen-displacement correction, and nonnegative fixed common instrument terms. Isotropic size and strain were tested one phase at a time. BaO₂ strain hit its bound and was rejected; replay-stable apparent sizes of about 23.5 nm for WO₃ and 19.7 nm for BaO₂ were retained. Because no calibrated instrument profile was supplied, these are peak-shape nuisance values rather than reliable crystallite-size measurements. A modest WO₃ [101] March–Dollase term (r = 0.9664) was supported across several low-, middle-, and high-angle families; tested BaO₂ texture axes refined to unity.

WO₃ and BaO₂ cells were refined; the trace-phase BaO and Ba₃W₂O₉ cells and all atomic coordinates were held to physically screened literature values. Exported geometries remain sensible: WO₃ W–O 1.72–2.22 Å, BaO₂ peroxide O–O 1.315 Å, BaO nearest Ba–O 2.748 Å, and Ba₃W₂O₉ W–O 1.90–2.23 Å.

The final replay converged with Rwp = 8.7410%, Rp = 6.8473%, GOF = 2.402, and maximum shift/s.u. = 0.018. The weighted residual Durbin–Watson value is 0.384, showing substantial serial correlation; consequently the covariance s.u.'s are optimistic and the larger model-based uncertainties above should be used. `fit.csv`, all CIFs, and `result.json` were exported from a reopened copy of `final.gpx` and numerically cross-checked against it.
