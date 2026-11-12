# Powder X-ray diffraction phase analysis

The 700 °C ZnO + WO₃ sample is a partially reacted mixture of wolframite ZnWO₄ with residual monoclinic WO₃ and wurtzite ZnO. Fractions below are normalized over these modeled crystalline phases; they do not quantify any amorphous material.

| Phase | Space group | Refined cell (Å, °) | Weight fraction | CIF |
|---|---|---|---:|---|
| ZnWO₄, wolframite | P2/c (13) | a = 4.70124, b = 5.72745, c = 4.93887, β = 90.5993 | 0.75038 (75.04 wt%) | `phase_ZnWO4.cif` |
| WO₃, monoclinic | P2₁/c (14), alternative setting | a = 7.69327, b = 7.53752, c = 10.5217, β = 136.068 | 0.18324 (18.32 wt%) | `phase_WO3.cif` |
| ZnO, wurtzite | P6₃mc (186) | a = 3.25501, c = 5.22043 | 0.06639 (6.64 wt%) | `phase_ZnO.cif` |

## Evidence

The dominant family—including the low-angle lines near 15.6°, 19.0°, 23.9–24.6° and the resolved doublet near 30.5–30.8°—indexes as monoclinic wolframite, not scheelite. Because a clean ZnWO₄ entry was absent from the accessible reference set, the starting atomic model was transferred from Zn-rich Cu/Zn- and Cd/Zn-wolframite analogues, converted to pure ZnWO₄, and then refined. Independent refinements of its two oxygen orbits converged from different starts to small, physical displacements.

After fitting ZnWO₄, one coherent residual family indexed to room-temperature monoclinic WO₃ (notably near 23.2–29.0° and 33–34°). P2₁/c, P2₁/n and triclinic WO₃ starts were compared with comparable cell/profile relaxation; the accepted P2₁/c model gave the cleanest fit. A second family at approximately 31.8°, 34.5°, 47.6°, 56.6°, 62.8° and 67.9–69.1° is wurtzite ZnO. The residual WO₃ and ZnO amounts are also chemically coherent: their inferred mole amounts differ by only about 3%, as expected for incomplete reaction of the nominally equimolar precursors. No coherent residual reflection family remains after these three phases are included.

The complete atomic-model refinement over all 8,301 original points gives Rwp = 2.7578%, Rp = 2.1014%, χ² = 12,284.2 and goodness of fit = 1.2193. A fresh GSAS-II forward replay regenerated the full profile without optimizing parameters and returned the same Rwp, positive background/peak widths, in-range polarization, and no physical review flags. The final project uses modest March–Dollase corrections for ZnWO₄ [100] (ratio about 0.748) and WO₃ [010] (about 0.962), plus phase-specific size and strain. ZnO texture was rejected because its ratio returned effectively to unity; surface-roughness trials were rejected because their parameters became nonphysical.

## Remaining uncertainty

The scale-covariance-only standard uncertainties are about 0.05, 0.03 and 0.05 wt% for ZnWO₄, WO₃ and ZnO, respectively, but these do not include structural/profile systematics; the extra reported digits are for project reproducibility. The ZnWO₄ topology and the identities of all three phases are reliable. Detailed WO₃ oxygen coordinates are less certain: two oxygen sites gave reproducible physical improvements, while four weakly determined sites demanded 0.14–0.20 Å shifts and were rolled back to the reference coordinates. WO₃ Uiso also sits at the lower physically allowed trial value, so its fraction has additional model correlation. Instrument zero and specimen displacement are strongly correlated; the final project retains their stable combined correction and fixes the displacement during the last cycles. Crystallite size and strain should therefore be treated as profile descriptors rather than uniquely determined microstructural measurements.
