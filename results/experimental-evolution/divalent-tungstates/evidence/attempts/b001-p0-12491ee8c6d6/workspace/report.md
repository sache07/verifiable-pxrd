# PXRD phase analysis and Rietveld refinement

## Result

The pattern is described by three crystalline phases. Weight fractions are normalized over the modeled crystalline material only.

| Phase | Structural model | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| Stolzite, PbWO₄ | tetragonal *I*4₁/*a* (No. 88) | *a* = 5.46593, *c* = 12.05882 | 61.1 wt% |
| Tungsten trioxide, WO₃ | monoclinic *P*2₁/*n* (No. 14) | *a* = 7.28474, *b* = 7.53483, *c* = 7.69051, β = 90.7642° | 22.1 wt% |
| Minium, Pb₃O₄ | tetragonal *P*4₂/*mbc* (No. 135) | *a* = 8.80123, *c* = 6.56033 | 16.8 wt% |

An estimated uncertainty of about ±2 wt% (absolute) is appropriate for each fraction; these uncertainties are correlated because the fractions sum to 100%. The much smaller covariance-only errors in `result.json` do not include model, profile, or phase-overlap uncertainty.

## Evidence for the assignments

The dominant PbWO₄ model accounts for the strongest peak at 27.811° 2θ and characteristic groups at 30.017°, 33.158°, 45.132°, and 55.629°. Monoclinic WO₃ is required by its distinctive low-angle triplet at 23.530°, 24.019°, and 24.845°, together with the multiplet near 33.66–34.60°. Pb₃O₄ is supported by the isolated 14.609° marker and contributions at 26.812°, 31.223°, 32.549°, and 52.521°. All three sets show the same displacement before correction, consistent with the refined specimen-height shift rather than separate unidentified phases.

The assemblage is also chemically consistent with partial reaction of the supplied Pb₃O₄ and WO₃ at 500 °C to form PbWO₄. In comparative refinements, omitting Pb₃O₄ left systematic residual peaks and raised Rwp to about 9.3%; a PbO model refined to negligible abundance. The selected monoclinic WO₃ model fit substantially better than tested triclinic and *P*2₁/*m* alternatives. No additional crystalline phase was justified by reproducible unmatched peaks.

## Refinement and fit quality

The final GSAS-II refinement used the supplied Cu Kα₁/Kα₂ wavelengths and 0.5 Kα₂/Kα₁ intensity ratio. It refined phase scales and cells, a common effective specimen displacement (−728.5 µm under the GSAS-II default 200 mm radius), phase-specific isotropic size broadening, one instrumental width term, effective polarization, and a 12-term Chebyshev background. Literature atomic coordinates were retained from COD 9009811 (PbWO₄), 1528915 (WO₃), and 1537983 (Pb₃O₄); atomic displacement parameters were fixed at plausible room-temperature values because unconstrained refinement was highly correlated with scale and polarization.

The final statistics are Rp = 3.224%, Rwp = 4.915%, Rexp = 2.485%, and goodness of fit = 1.981 for 8,301 observations and 29 refined variables. The last cycle converged with maximum shift/esd = 0.0012 and no frozen variables. Because the input contained no intensity uncertainties, GSAS-II weights were `w = 1/I`, equivalent to using counting-statistical σ ≈ √I; the statistics are conditional on that proxy.

## Remaining uncertainty

The three phase identities are reliable, but the data do not independently determine detailed atomic coordinates or displacement parameters; the submitted CIFs therefore combine literature coordinates with cells refined from this pattern. The uncalibrated instrumental profile, broad and overlapping peaks, large specimen displacement, and absent uncertainty estimates limit fraction accuracy. Sensible background/profile variants shifted individual fractions by roughly 1–2 wt%, which motivates the ±2 wt% estimate above. A minor additional crystalline component below a few weight percent could be hidden by overlap, and amorphous content cannot be quantified without an internal standard. Thus the reported values must not be interpreted as absolute whole-sample fractions if noncrystalline material is present.
