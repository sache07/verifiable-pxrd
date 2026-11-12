# Powder XRD phase analysis

The 500 °C CaCO3/WO3 product is modeled by three chemical phases and four resolved crystalline profile populations. All fractions below are normalized over the modeled crystalline material; an amorphous fraction was not measured.

| Refined component | Space group | Refined cell (Å, °) | Crystalline wt.% |
|---|---:|---|---:|
| CaWO4, scheelite | I 41/a | a = 5.24319, c = 11.37421 | 11.98 |
| WO3, broad-domain population | P 21/c | a = 7.31054, b = 7.53961, c = 10.57812, beta = 133.3228 | 31.49 |
| CaCO3, calcite | R -3 c | a = 4.99057, c = 17.07422 | 31.85 |
| WO3, sharp-domain population | P 21/c | a = 7.30504, b = 7.53991, c = 10.52560, beta = 133.0377 | 24.69 |

The combined WO3 fraction is 56.17 wt.%. The nonconventional monoclinic cells above are the exact settings exported in the CIFs.

## Evidence and refinement

Scheelite CaWO4 accounts for coherent families near 18.95, 29.05, 47.5 and 56.2° 2theta. Calcite is required by its 29.72, 39.7 and 43.47° families. Monoclinic WO3 accounts for the characteristic 23.45/23.93/24.70° group and repeated middle- and high-angle families. A single WO3 population left coherent narrow shoulders throughout the pattern: the one-WO3 model gave about 7.20% Rwp, and a more flexible single-population generalized-strain model gave 6.16%, versus 5.3011% for two independently refined WO3 cell/profile populations.

The two WO3 populations use the same physically screened room-temperature P21/c atomic framework. An older alternate WO3 record that initially matched some intensity residuals was rejected because its source coordinates themselves produced a 1.575 Å O-O contact. Replacing it with the sound modern framework both removed the contact and improved the fit. All four submitted CIFs pass the geometry/occupancy screen; the WO3 octahedral distances and all O-O contacts are plausible.

The final full-range model uses the supplied Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio, an eight-term smooth Chebyshev background, one specimen-displacement correction, nonnegative common W/X profile terms, and accepted SH/L asymmetry. Unsupported size and strain anisotropy terms were neutralized or removed. Calcite [001] and sharp-WO3 [111] March-Dollase terms were retained because removing them raises replay Rwp to 5.382% and 5.345%, respectively. The [110] WO3 texture axis is nearly competitive, so the exact texture axis is not unique.

CaO, Ca3WO6, Ca4.26W10O30, W18O49, W10O29, W3O8, and alternate WO3 polymorphs were challenged under the common baseline. Their scales were zero or negligible and they did not explain coherent unique residual families, so they were not retained.

The final atomic GSAS-II replay over all 8,293 observations gives Rwp = 5.3011%, Rp = 4.1419%, chi-square = 40,653.18 and goodness of fit = 2.2189 for 36 refined parameters. The replay reports no negative-profile, width, background, or displacement-tensor review flags, and `fit.csv` is numerically identical to that replay.

## Remaining uncertainty

The distinction between two thermodynamic WO3 phases is not reliable from this pattern. The data robustly require broad and sharp monoclinic WO3 populations with slightly different cells, but these may instead be two strain/domain-size populations of one phase. Consequently, the combined WO3 fraction is more reliable than the separate 31.49/24.69 wt.% split, and the sharp component's atomic structure is not independently determined. The formal scale-fraction standard uncertainties in `result.json` do not include this model ambiguity.

CaWO4 broadening lies close to the allowed small-size/high-strain limits, so its crystallite-size and strain values should not be interpreted quantitatively. Residual mismatch at several intense overlapping peaks and the goodness of fit above one indicate remaining counting/model error. No claim is made about amorphous content or crystalline impurities below the sensitivity of this scan.
