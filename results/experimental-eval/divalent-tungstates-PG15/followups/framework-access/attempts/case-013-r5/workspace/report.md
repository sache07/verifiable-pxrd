# Powder XRD phase analysis

The pattern from the reported 500 °C PbO + WO3 synthesis is best described by six crystalline Pb-W-O phases. The quantitative result is normalized over those modeled crystalline phases; an amorphous fraction was not measurable without an external standard.

| Phase | Space group; refined cell (Å, °) | Weight fraction (wt%) |
|---|---|---:|
| Pb7W8O28.8 | P4/nnc; a = 7.72323, c = 12.05422 | 54.83 ± 0.19 |
| massicot PbO | Pbcm; a = 5.89167, b = 5.49079, c = 4.75702 | 10.21 ± 0.11 |
| monoclinic WO3 | P21/c; a = 7.29780, b = 7.54375, c = 10.55956, beta = 133.2682 | 11.17 ± 0.15 |
| litharge PbO | P4/nmm; a = 3.97643, c = 5.03270 | 6.86 ± 0.10 |
| low-symmetry PbWO4 polymorph | P2/c; a = 9.35857, b = 5.20819, c = 7.28093, beta = 94.9679 | 13.65 ± 0.16 |
| Pb3WO6, double-perovskite type | P21/c; a = 5.80136, b = 5.85512, c = 10.03599, beta = 125.3206 | 3.28 ± 0.07 |

The uncertainties in the table are propagated scale-factor standard errors from the final cycle. They do not include model-selection error and therefore understate the realistic uncertainty, particularly for the last two phases.

## Evidence and refinement

The raw-count scan was modeled in GSAS-II with the metadata Cu Kα1/Kα2 wavelengths (1.540598/1.544426 Å) and 0.5 Kα2/Kα1 ratio. Phase scale factors, cells, a smooth Chebyshev background, physically bounded isotropic size/microstrain terms, and limited preferred orientation were refined. A joint cell/position refinement gave an angular zero of -0.064° and a specimen displacement of about -594 µm; both lie inside the documented measurement ranges. Weight fractions are the normalized products of the saved GSAS-II cell masses and phase scales. The submitted profile is a fresh atomic forward replay of `final.gpx`, not its cached calculated array.

The dominant peak positions and intensity sequence identify tetragonal Pb7W8O28.8 (starting model COD 9016035). Residual sets require both PbO polymorphs—orthorhombic massicot (COD 2310433) and tetragonal litharge (COD 9012700)—as well as unreacted monoclinic WO3 (COD 2311041). A P2/c PbWO4 framework accounts for otherwise unmatched features near 25.91° and 30.15° 2θ; introducing it reduced the intermediate Rwp from about 14.02% to 12.88%. The weak 31.05° feature and overlapping higher-angle lines support a final minor Pb3WO6 component, which reduced that intermediate Rwp to about 12.43%. Plausible alternatives including scheelite/raspite PbWO4, WO2 and reduced tungsten oxides did not retain significant stable scales or gave poorer profile agreement.

The final independent full-grid replay gives Rwp = 10.036%, Rp = 7.367%, and goodness of fit = 2.870 for 8,282 observations. The replay reports no negative-background, peak-width, polarization, or displacement-parameter review flags. `fit.csv` contains observed, calculated, and observed-minus-calculated intensities.

## Remaining uncertainty

The P2/c PbWO4 model is analogue-derived from the CsLu(WO4)2 framework (COD 1530890), replacing the Cs/Lu cation pair by Pb; the Pb3WO6 model is analogue-derived from Sr2CaWO6 (COD 2104688), replacing Sr/Ca by Pb. Their cells and bounded coordinates were refined, but their exact atom arrangements are not uniquely determined by this overlapped laboratory pattern. These structural assignments—and consequently their individual fractions—are less reliable than those of the four reference-backed phases. The PbWO4 preferred-orientation and broadening terms also correlate with its scale.

Laboratory Cu XRD has limited sensitivity to oxygen occupancy, so the precise O/vacancy distribution represented by Pb7W8O28.8 is not independently established here. No additional crystalline phase is required at a stable scale, but a very weak or amorphous component cannot be excluded.
