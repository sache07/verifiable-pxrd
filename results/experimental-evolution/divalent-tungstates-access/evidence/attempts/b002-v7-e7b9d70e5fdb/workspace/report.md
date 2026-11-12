# Powder X-ray diffraction phase analysis

## Result

The specimen contains three modeled crystalline phases. Fractions are normalized over those crystalline phases only.

| Phase | Space group | Refined cell (Å, °) | Weight fraction | CIF |
|---|---|---|---:|---|
| Wolframite-type ZnWO4 | P 2/c | a = 4.68785, b = 5.72424, c = 4.92289, beta = 90.5746 | 0.872319 (87.23 wt%) | [ZnWO4_wolframite.cif](ZnWO4_wolframite.cif) |
| Monoclinic WO3 | P 21/n (No. 14 setting equivalent to P 21/c) | a = 7.27674, b = 7.50281, c = 7.67812, beta = 90.6875 | 0.100680 (10.07 wt%) | [WO3_monoclinic.cif](WO3_monoclinic.cif) |
| Wurtzite ZnO | P 63 m c | a = b = 3.24856, c = 5.20920, gamma = 120 | 0.027001 (2.70 wt%) | [ZnO_wurtzite.cif](ZnO_wurtzite.cif) |

This inventory is chemically consistent with incomplete reaction of the reported ZnO and WO3 precursors at 700 °C to form ZnWO4.

## Evidence and model selection

The dominant family is indexed by monoclinic wolframite ZnWO4, including calculated reflections near 15.70, 19.15, 24.06/24.76, 30.71/30.95, 36.71, 38.61, and the corresponding high-angle multiplets. The remaining coherent low- and high-angle families are accounted for by monoclinic WO3 (notably 23.39/23.93/24.68, 33.60-34.54, 47.56, 50.34, and 55.84-56.40 degrees) and wurtzite ZnO (32.02, 34.64, 36.50, 47.77, 56.86, 63.08, 68.20, and 69.35 degrees). No coherent positive-reflection family remains unassigned.

The frozen index did not supply an exact-composition ZnWO4 reference, so symmetry-diverse analogue starts were converted to ZnWO4 and compared at equal development. The retained wolframite basin came from ScNbO4 (COD 5910338; Sc -> Zn and Nb -> W). It reached Rwp = 19.88%, versus about 21.57% for the independently developed CoMoO4-II start (COD 7205001; Co -> Zn and Mo -> W), whose preferred-orientation parameter also pinned at its tested limit. FeNbO4-derived, triclinic ZnMoO4-derived, and scheelite-derived alternatives did not provide physical profile closure and were discarded. The WO3 and ZnO starts were COD 1528915 and COD 9004178, respectively.

The accepted model used the supplied Cu Kalpha1/Kalpha2 wavelengths and intensity ratio. Scales, a nine-term background, cells, an interior zero offset, and supported size/strain and March-Dollase terms were developed before terminal scale/background convergence. A joint zero/displacement trial was 99.9% correlated and reached limits, so sample displacement was returned to zero; polarization, axial-divergence, and additional profile trials that reached laboratory bounds were likewise rejected. The required bounded polish was run once. Its converged physical selection was the unchanged baseline; lower-Rwp branches were rejected for frozen coordinate/cell variables or nonconvergent settling.

Fresh read-only GSAS-II replay regenerated structure factors and reflection lists without using the saved calculated profile. It reproduced Rwp = 19.8826%, Rp = 15.1178%, goodness of fit = 7.5184, and chi-square = 468549.85 over all 8301 points, while leaving `final.gpx` unchanged (SHA-256 `b56c271f1a2c3cea883287da00b42b9cf52f1139abdc4079e9cc9b1d6867b556`).

## Remaining uncertainty

The formal scale-covariance standard uncertainties are approximately 0.26, 0.19, and 0.20 wt% for ZnWO4, WO3, and ZnO, respectively, but these do not include model systematics. Pointwise standard uncertainties were not supplied, so the goodness of fit and formal covariance are conditional on the counting-statistics weights used here. The dominant ZnWO4 March-Dollase ratio is 0.704 on [111], close to the lower tested laboratory limit, so its scale and the minor-phase fractions remain coupled to texture. The 2.70 wt% ZnO fraction is therefore best regarded as semi-quantitative; its phase identity is supported by a full reflection family, but its attempted size/strain terms ran to bounds and were not retained.

Zn/W coordinates in the dominant phase were supported, but its oxygen coordinates remain analogue-derived. WO3 and ZnO coordinates likewise remain reference-derived because coordinate refinements were unstable. Read-only geometry checks give minimum Zn-O = 2.047 Å and W-O = 1.778 Å in ZnWO4 and Zn-O = 1.974 Å in ZnO. The WO3 model has W-O = 1.837 Å but also a short 1.570 Å O-O approach inherited from the reference oxygen array. It did not cross the polish audit's catastrophic-contact threshold, but the detailed WO3 oxygen geometry cannot be considered reliably determined from this pattern.

The relatively high Rwp and structured center/wing residuals show that profile, texture, and local-coordinate imperfections remain. The largest positive residuals coincide with accepted reflections (for example ZnWO4 near 31.03 degrees and WO3 near 53.82 and 64.89 degrees), rather than forming a separate indexable family. No amorphous fraction can be determined from this analysis, and all reported fractions exclude any amorphous or otherwise unmodeled material.
