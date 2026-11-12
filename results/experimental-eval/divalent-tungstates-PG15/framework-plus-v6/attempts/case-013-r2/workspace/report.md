# Powder XRD phase analysis

The sample was treated as the crystalline product of PbO + WO3 fired at 500 °C. The full 10.009–99.994° 2θ Cu Kα1/Kα2 scan (8,282 points) was refined in GSAS-II. Fractions below are normalized over the modeled crystalline phases; they do not quantify amorphous material.

## Result

| Phase | Space group | Crystalline weight fraction |
|---|---:|---:|
| PbWO4, scheelite | I41/a | 57.86% |
| Pb2WO5, Pb2MoO5-type provisional model | C2/m | 16.12% |
| WO3, monoclinic | P21/n | 10.64% |
| PbO, massicot | Pbcm | 7.56% |
| PbO, litharge | P4/nmm | 3.22% |
| PbO, long-period alpha-PbO approximant | Pbma | 2.72% |
| Pb3O4, minium | P42/mbc | 1.87% |

The independently regenerated full-pattern statistics are Rwp = 10.4627%, Rp = 7.1698%, Rexp = 3.5015%, and goodness of fit = 2.988. The calculated and background profiles remain positive over the complete scan.

## Evidence and refinement choices

Scheelite PbWO4 accounts for the dominant families near 27.70, 29.92, 33.06, 45.03, 47.29, 51.49, and 55.55° 2θ. Monoclinic WO3 is required by its resolved low-angle 23.39/23.89/24.66° family and higher-angle splitting. No exact Pb2WO5 entry was available, so a chemically isovalent Mo6+→W6+ substitution was made in the C2/m Pb2MoO5 structure (COD 7220560). Its coherent families near 25.92, 29–31, 41.91, and 51.96° support a Pb2WO5-type intermediate; scale was established before cell/coordinate adjustment.

The minor Pb oxides are not retained merely because their scales are positive. After fully reconverging the remaining model, deleting massicot, litharge, minium, or long-period PbO raised Rwp from 10.463% to approximately 12.484%, 11.72%, 10.620%, and 11.02%, respectively. Conversely, final-profile challenges with raspite PbWO4 and defect scheelite both collapsed to effectively zero scale. The corrected litharge origin setting exports the intended PbO stoichiometry.

The accepted nuisance model uses one specimen-displacement correction (−547 μm), no zero shift, polarization 0.787, a smooth eight-term Chebyshev background, and a common U/W/X plus SH/L profile. U was unsupported and fixed at zero. Supported March–Dollase terms were Pb2WO5 [100], massicot [100], and litharge [110]. One interior WO3 size term (0.50 μm) and isotropic Pb2WO5 strain (about 2,106 ppm) were replay-stable. Other size/strain terms hit bounds or replayed poorly; uniaxial Pb2WO5 strain oscillated and was rejected. The fitted common X term (11.82) is above the nominal generator prior: forcing that prior drove phase-width terms to bounds and worsened the fit, so the common width must be regarded as an empirical profile parameter, not an independently calibrated instrument value.

The submitted `final.gpx` was reopened and replayed repeatedly before export. An independent atomic forward replay regenerated reflections and structure factors without optimizing any parameter, matched the submitted fractions/CIFs, and returned no profile-review flags. `fit.csv` contains that independently regenerated observed/calculated/background/difference profile.

## Remaining uncertainty

The Pb2WO5 atomic model is provisional because it is an isovalent cross-chemistry analogue rather than an exact database structure. Its phase presence is well supported, but detailed coordinates and its 16.12% fraction are more model-dependent than those of scheelite. The long-period PbO model is an approximant with a physically bounded parent-derived cell; its detailed superstructure and 2.72% fraction are also lower confidence. The 1.87% minium fraction is supported by deletion testing but is sensitive to overlap with the other Pb oxides.

The historical monoclinic WO3 model retains four symmetry-equivalent O···O contacts of 1.577 Å. Coordinate refinement was unstable and was rejected, so the WO3 phase assignment and scale are supported but its oxygen geometry should not be interpreted as a reliable local-structure determination. More generally, the goodness of fit and profile-width ambiguity show residual systematic error; the reported fractions are model-conditioned crystalline fractions, not absolute bulk assay values.
