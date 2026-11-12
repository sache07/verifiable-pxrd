# Powder-XRD phase analysis

The PbO + WO₃ sample fired at 500 °C is modeled as a partially reacted mixture dominated by scheelite PbWO₄. Weight fractions below are normalized over the modeled crystalline phases; an amorphous fraction was not determined.

| Phase model | Space group | Weight fraction | Assessment |
|---|---:|---:|---|
| PbWO₄, scheelite | I4₁/a (88) | 0.6449 | robust |
| PbO, massicot | Pbcm (57) | 0.1637 | robust phase assignment; fraction profile-dependent |
| WO₃, monoclinic | P2₁/c setting (14) | 0.1113 | robust composition/lattice; atomic model uncertain |
| PbO long-period superstructure | Pbcm/Pbma setting (57) | 0.0801 | provisional minor-phase model |

The frozen full-grid calculation has Rwp = 12.93%, Rp = 8.70%, and goodness of fit = 3.70 using Poisson counting weights. The counting-statistical lower-limit Rwp is 3.50%, so the remaining structured residual is significant.

## Evidence

- Scheelite PbWO₄ accounts for the dominant series at approximately 27.70, 29.91, 33.05, 45.02, 47.28, 51.48, 55.54, and 56.82° 2θ. Its refined cell is a = 5.46197 Å and c = 12.05372 Å.
- Massicot PbO is supported by reflections near 29.34, 30.62, 38.12, 49.50, 51.00, 53.38, 56.30, 60.54, and 63.28°. Its very broad peaks require about 0.050 μm coherent size, [001] uniaxial microstrain (8000/2475 ppm), and [100] March–Dollase texture (0.793).
- Monoclinic WO₃ is required by the resolved low-angle group near 23.38, 23.88, and 24.64° and its higher-angle lines. The refined cell is a = 7.29761, b = 7.54230, c = 7.69386 Å, β = 90.44995°.
- Adding the long-period Pbcm PbO model explains residual intensity near 28.9, 32.0, 48.7, and 54.9° and reduces Rwp from about 14.66% for the three-phase model to 12.93%. Competing WO₂ models refined to zero scale; Pb₂O₃ required an implausible >9% cell change; and a fifth Pb₃O₄ phase gave only a marginal, boundary-driven improvement.

## Remaining uncertainty

The fourth phase is not determined reliably at the atomic-structure level. Its coherent size reached the allowed 0.04 μm lower bound and its preferred-orientation ratio reached 1.4, so its reported 8.0 wt% should be treated as approximate and could partly represent another highly broadened Pb–O superstructure. A broad residual centered near 25.9° remains unexplained; WO₂ was rejected because its required 37.3 and 53.6° reflections are absent.

The WO₃ lattice and abundance are supported, but closely related P2₁/c and P-1 references are difficult to distinguish. The submitted P2₁/c parent gives the best refined profile but contains a short 1.58 Å O–O contact and therefore needs structural adjudication; physical-pass alternatives worsened Rwp to at least 12.95% (P-1) or 13.74% (P2₁/c). Its detailed oxygen coordinates should not be regarded as reliably determined from this pattern.

Formal least-squares fraction errors in `result.json` are much smaller than these model-selection uncertainties. Conservative systematic uncertainties are roughly ±0.04 for PbWO₄ and massicot, ±0.03 for WO₃, and at least ±0.04 for the provisional PbO superstructure.
