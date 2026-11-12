# Powder X-ray diffraction phase analysis

The specimen was prepared from CaCO3 and WO3 at 650 °C and measured in reflection geometry with the reported Cu Kα1/Kα2 doublet. The unprocessed 9.90–100.09° 2θ profile is described by two crystalline phases:

| Phase | Structural model | Weight fraction* |
|---|---|---:|
| CaWO4 | scheelite, *I*4₁/*a*; a = 5.23404 Å, c = 11.3263 Å | 0.84684(54) |
| WO3 | monoclinic, *P*2₁/*c*; a = 7.30735 Å, b = 7.54925 Å, c = 10.5072 Å, β = 132.997° | 0.15316(54) |

\*Fractions are normalized over the modeled crystalline phases. Parentheses are formal least-squares standard uncertainties on the fraction, not an allowance for model or sample-systematic error.

## Evidence and refinement

The broad scheelite family accounts for the dominant reflections, including the features near 18.27, 28.43/28.77, 31.21, 33.85, 46.89, and 57.65° 2θ. The sharper residual family—most visibly the split peaks near 22.76, 23.18, and 23.99°, with repeated support near 26.19, 32.88/33.12, 40.98/41.51, and 49.48°—is indexed by monoclinic WO3. The latter is chemically consistent with residual precursor. Scheelite CaWO4 and *P*2₁/*c* WO3 references jointly account for every coherent residual family; CaCO3/CaO and alternative CaWO4 polymorph families have no independent reflection support in this pattern.

The full-pattern GSAS-II refinement used both reported wavelengths, a 12-term Chebyshev background, phase scales and cells, a common instrumental profile, and phase-specific isotropic size/strain and displacement terms. The final fit has Rwp = 3.8688%, Rp = 2.9413%, Rexp = 3.1382%, and goodness of fit = 1.2343 for 8301 observations. A refined zero offset of −0.37084° was required. The final bounded coordinate polish improved Rwp by 0.094 percentage point without destabilizing the fractions or producing short contacts (minimum W–O distances are 1.784 Å in CaWO4 and 1.685 Å in WO3; minimum WO3 O–O is 2.543 Å).

## Remaining uncertainty

The phase identities and approximately 84.7/15.3 wt% crystalline split are reliable for this two-phase model. The formal fraction uncertainties are smaller than likely systematic effects from absorption, calibration/profile correlations, reference chemistry, and any amorphous material, which cannot be quantified by this normalization. No additional crystalline phase is supported above the residual/noise level, but a trace phase below the pattern's detection limit cannot be excluded. Because WO3 is the minor, strongly overlapped phase, its fine oxygen coordinates are less reliably determined than its topology, unit cell, and scale; the submitted coordinates should therefore not be interpreted as a high-precision independent WO3 structure determination.

All CIFs, fractions, fit statistics, and the calculated profile were exported from `final.gpx`. A fresh no-refinement replay regenerated the complete profile from native GSAS-II structure factors and reflection lists, left the project unchanged, and raised no profile-review flags.
