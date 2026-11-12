# Quantitative phase analysis

The pattern is best described by five crystalline phases. Weight fractions are normalized over those modeled crystalline phases; no internal standard was present, so an amorphous fraction cannot be measured.

| Phase | Structural model | Weight fraction (wt%) | Formal fit s.u. (wt%) |
|---|---|---:|---:|
| PbWO4 (stolzite/scheelite) | I41/a, COD 9009811 | 61.57 | 0.23 |
| Pb2WO5 | C2/m, W-substituted Pb2MoO5 prototype (COD 7220560) | 15.75 | 0.24 |
| WO3 | monoclinic P21/n, COD 1528915 | 10.34 | 0.18 |
| PbO (massicot) | orthorhombic Pbcm, COD 2310433 | 7.13 | 0.11 |
| PbO (litharge) | tetragonal P4/nmm, COD 9012700 | 5.21 | 0.09 |

## Evidence

PbWO4 accounts for the dominant scheelite peak families across the full angular range. The Pb2WO5 model accounts for coherent additional families near 25.9, 29.35, 30.62, and 31.05 degrees 2theta that cannot be represented by PbWO4, WO3, or either PbO polymorph. No exact Pb2WO5 entry was available in the local structure inventory, so cross-chemistry analogue screening was used. Isovalent Mo-to-W substitution in monoclinic Pb2MoO5 gives chemically sensible W-O distances (approximately 1.77-1.80 A) after cell refinement and a stable positive scale.

Monoclinic WO3 explains the characteristic cluster around 23-25 degrees and its higher-angle families. Orthorhombic massicot and tetragonal litharge are independently required: each gives repeated, coherently positioned peaks, and litharge in particular removes residuals near 28.85, 32.11, 36.01, 48.86, and 54.91 degrees. Coexistence of PbO polymorphs is chemically plausible after heating at 500 degrees C, close to the PbO polymorphic transition, followed by cooling.

The final full-range refinement used both Cu Kalpha wavelengths with the Kalpha2/Kalpha1 ratio fixed at 0.5, Poisson counting weights, an eight-term smooth Chebyshev background, one zero correction, and a common nonnegative U/W/X profile with axial asymmetry. Unused size, strain, roughness, and texture terms were neutralized. Only a modest isotropic microstrain contribution for Pb2WO5 was retained; it was positive and replay-stable. Trials of phase-specific size, additional common-width terms, uniaxial broadening, and March-Dollase texture either hit bounds, became nonphysical, or were unsupported by isolated peak families. The fitted profile tracks isolated low-, middle-, and high-angle peak widths without a systematic position or width trend.

Final statistics are Rwp = 11.688%, Rp = 7.893%, Rexp = 3.502%, and goodness of fit = 3.345 for 8,282 observations and 34 refined variables. The observed, calculated, difference, and background curves in `fit.csv` were regenerated directly from the saved `final.gpx`.

## Remaining uncertainty

The tabulated standard uncertainties are covariance-based counting-statistical values and are smaller than the likely model uncertainty. A more realistic interpretation is roughly 1-2 wt% absolute uncertainty for the major PbWO4/Pb2WO5 partition and about 0.5 wt% for each minor phase.

The Pb2WO5 assignment is supported by its diffraction families and chemistry, but its atomic model is an analogue rather than an independently solved Pb2WO5 structure; its structure and fraction are therefore less secure than those of the database-matched phases. Ambient monoclinic and nearly pseudomonoclinic triclinic WO3 models fit almost equally well (the triclinic trial lowered Rwp by about 0.1 percentage point using extra cell degrees of freedom). Because measurement temperature was not reported, the WO3 symmetry cannot be distinguished reliably from this powder pattern alone; the expected room-temperature monoclinic form was retained, and the WO3 fraction is comparatively insensitive to that choice.

Pb3O4 was also re-challenged after establishing the common profile. A formal approximately 2 wt% scale could be obtained mainly through overlapped reflections, but its strongest unique peaks were not coherently present. It is therefore not established reliably and was excluded rather than reported as a crystalline phase. Weak unmodeled material below the pattern's practical detection limit may remain, as indicated by the non-unity goodness of fit.
