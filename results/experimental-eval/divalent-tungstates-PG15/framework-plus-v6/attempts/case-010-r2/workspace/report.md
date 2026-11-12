# Powder XRD phase analysis

The modeled crystalline inventory is **gamma-WO3, 74.74 wt%**, and **alpha-Mn2O3, 25.26 wt%**. Fractions are normalized over these two crystalline phases; they do not quantify any amorphous material.

| Phase | Evidence/model | Refined cell | Weight fraction |
|---|---|---|---:|
| gamma-WO3 | COD 2311041, monoclinic P 21/c (No. 14) | a = 7.30704, b = 7.53943, c = 10.54911 Å; beta = 133.1583° | 0.74736(26) |
| alpha-Mn2O3 | COD 1514103, orthorhombic Pbca (No. 61) | a = 9.42948, b = 9.40685, c = 9.41358 Å | 0.25264(26) |

The intense 23–25° triplet and the families throughout 34–90° identify monoclinic WO3. The weaker but coherent Mn2O3 families near 33.3°, 38.5°, 55.5°, and 66.0° require the second phase. Their fraction also agrees closely with the mass balance of an unreacted 1:1 Mn:W mixture of WO3 and one-half mole Mn2O3, which is chemically plausible after the reported 500 °C treatment. No coherent residual family requires MnWO4, Mn3O4, Mn3WO6, or a third crystalline phase.

All filtered exact-composition WO3 records were challenged under the same baseline. COD 2311041 gave the best physically valid model. The initially attractive COD 1010618 record was rejected because its geometry contains a 0.46 Å O–O contact; the physical triclinic alternate COD 2106293 fit worse and drove its metric toward the accepted monoclinic cell. Both submitted structures have full occupancies and pass the final geometry screen: minimum contacts are 1.756 Å (W–O) and 1.875 Å (Mn–O), with plausible densities of 7.265 and 5.023 g cm-3.

The final GSAS-II refinement used the measured Cu Kalpha doublet, a smooth six-term Chebyshev background, one specimen-displacement correction, polarization and axial asymmetry, phase-specific isotropic size, and [001] uniaxial microstrain for WO3. March-Dollase trials along five low-index axes converged to random powder and were removed. Mn2O3 strain, surface roughness, free displacement factors, and extra oxygen-coordinate refinements were rejected because they were correlated, bound-seeking, or caused nonphysical coordinate motion. Only modest W-coordinate shifts were supported; the WO3 oxygen positions and all Mn2O3 coordinates remain those of the physical parent records and are not independently determined by this pattern.

The final full-range fit has Rwp = 6.879%, Rp = 5.235%, Rexp = 2.662%, and GOF = 2.588. Independent atomic replay of `final.gpx` reproduced the phase fractions exactly and Rwp = 6.87891% with no profile-review flags. Formal fraction uncertainty is 0.26 percentage points, but profile/scale systematics dominate; a more realistic uncertainty is about ±1.5 wt% per phase. A minor additional crystalline phase below roughly 1–2 wt% cannot be excluded, and the largest residuals remain on the strongest overlapping WO3 peaks rather than forming a distinct unmodeled peak family.
