# Quantitative phase analysis

The pattern is best described by three crystalline phases. Weight fractions are normalized over these modeled crystalline phases only.

| Phase | Structural model | Weight fraction |
|---|---|---:|
| BaCO3 (witherite) | Pmcn, COD 9010928 | 53.75 wt% (formal s.u. 0.13 wt%) |
| WO3 | triclinic P-1, COD 2106293 | 45.42 wt% (formal s.u. 0.13 wt%) |
| BaWO4 (scheelite) | I41/a ordered model derived from COD 1527204 | 0.825 wt% (formal s.u. 0.053 wt%) |

This composition is chemically consistent with heating BaCO3 and WO3 at only 400 °C: most material remains as the two precursors and a small amount of BaWO4 product has formed.

## Evidence and model selection

The BaCO3 assignment is supported by distinct families near 24.21°, 34.86°, 45.15°, and 47.06° 2theta. The WO3 model reproduces the characteristic split groups around 23.43/23.91/24.65° and 33.57/33.99/34.45°. Under the same baseline, the triclinic WO3 record gave Rwp about 8.76%, compared with about 9.01% for the best physically acceptable monoclinic alternative. The final triclinic cell is a = 7.31154, b = 7.54183, c = 7.69810 Å, alpha = 89.8689°, beta = 90.7723°, gamma = 90.0911°.

BaWO4 is weak but reproducible. It contributes a partly isolated 024 line near 43.35° and coherent intensity at the overlapping 112, 020, 116, and 224 families. Removing it from the final nuisance model raises Rwp from 7.65% to 7.76%. Replacing its record with the exact split-O COD entry or a BaMoO4-derived scheelite analogue still gives 0.77–0.84 wt%, so the positive scale is not tied to one record. The submitted ordered model retains the physical oxygen site from COD 1527204 at full occupancy; it gives four W–O distances of 1.798 Å, whereas the raw split-site record contains an implausibly short W–O contact.

Unrestrained coordinate expansions were rejected: they produced a 1.20 Å C–O bond in BaCO3 or a 1.57 Å W–O contact in WO3. The submitted CIFs therefore retain physically screened reference coordinates while refining unit cells. The final geometries contain C–O distances of 1.275–1.407 Å and WO3 W–O distances of 1.716–2.220 Å.

## Refinement and fit

The final GSAS-II model uses the supplied Cu Kalpha doublet, a smooth six-term Chebyshev background, one zero correction (+0.31342°), and a nonnegative common U/X profile (U = 143.68, W fixed at 0, X = 13.986). Effective polarization refined to 0.7290(56). Roughness, asymmetry, and phase size/strain trials were rejected because they hit bounds, correlated strongly, failed replay, or shifted phase fractions as scale/profile surrogates. A modest BaCO3 March–Dollase correction along [110], 0.9065(41), was retained after comparison with axial and diagonal alternatives and support from multiple isolated families. WO3 texture trials refined close to unity.

For 8,284 fitted points and 25 variables, Rwp = 7.645%, Rp = 6.042%, Rexp = 3.484%, and goodness of fit = 2.20. The observed, calculated, difference, and background profiles in `fit.csv` are exported from the reopened `final.gpx` used for the CIFs and fractions.

## Remaining uncertainty

No pointwise uncertainties or calibrated instrument profile were supplied, so Poisson proxy weights were used. The reported standard uncertainties are conditional least-squares values and understate model/systematic uncertainty. In particular, the BaWO4 fraction should be interpreted as approximately 0.8 wt%, not as an absolute determination to ±0.053 wt%; its atomic coordinates cannot be refined reliably at this abundance. The exact WO3 polymorph is also less certain than the WO3 phase identity because its metric is close to monoclinic and the measurement temperature was not reported, although the observed splitting favors the triclinic model. Residual intensity mismatches remain in several strongly overlapped regions. Amorphous content and trace crystalline phases below the pattern's practical detection limit cannot be quantified, so the fractions apply only to the modeled crystalline material.
