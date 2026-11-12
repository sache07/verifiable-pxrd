# Powder XRD phase analysis

The pattern is modeled with three crystalline phases. Weight fractions are normalized over those phases only.

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| CaWO₄, scheelite | I 41/a | a = 5.25050, c = 11.38526 | 69.52 wt% |
| γ-WO₃, monoclinic | P 21/c | a = 7.29808, b = 7.54251, c = 10.51602, β = 133.0229 | 15.96 wt% |
| Ca₃WO₆ | P 21 | a = 5.55304, b = 5.81027, c = 8.01111, β = 90.2204 | 14.52 wt% |

The final whole-pattern fit gives Rwp = 3.465%, Rp = 2.716%, Rexp = 2.617%, and goodness-of-fit = 1.324 over all 8301 measured points. The independently replayed `final.gpx` reproduces this profile without parameter optimization.

## Evidence

Scheelite CaWO₄ accounts for the dominant reflections, including the intense 28.57° peak and the groups near 31.32°, 34.03°, 46.97°, 54.15°, and 57.72° 2θ. Monoclinic WO₃ is required by its characteristic low-angle cluster at approximately 23.02°, 23.47°, and 24.27°. A two-phase CaWO₄ + WO₃ model left coherent peaks near 18.75°, 19.36°, 22.04°, 30.66°, 32.10°, 37.45°, 45.08°, 50.72°, and 56.9° and had Rwp about 11.4%. Adding the Ca₃WO₆ model reduced the initial three-phase Rwp to 8.87% before the specimen/profile refinement and removed those residual families.

The Ca₃WO₆ model was built from the isostructural Ca₃UO₆ P 21 framework (U replaced by W), contracted to the indexed cell, and then conservatively refined. Its approximately stoichiometric coexistence with residual WO₃ is also chemically consistent with partial reaction of CaO + WO₃ at 800 °C; the refined phase fractions imply an overall crystalline Ca:W molar ratio of about 1.01, matching the 1:1 precursor ratio. The final structures have plausible contacts; the shortest W–O distances are about 1.77 Å in CaWO₄, 1.74 Å in WO₃, and 1.92 Å in Ca₃WO₆.

## Remaining uncertainty

The CaWO₄ structure and abundance are reliable. The γ-WO₃ assignment is well supported as a WO₃ phase, but this broadened powder pattern does not decisively distinguish P 21/c from a very closely related triclinic distortion. For Ca₃WO₆, the composition, cell, and need for a third phase are robust, while the exact P 21 atomic coordinates are not uniquely determined because this is an adapted analogue model and its peaks overlap the major phases.

Strong correlations among scale, polarization, surface roughness, texture, and overlapping intensities limit formal fraction precision. A realistic systematic uncertainty is roughly ±1–2 wt% absolute for CaWO₄ and WO₃ and ±2–3 wt% for Ca₃WO₆. Absolute crystalline fractions relative to any amorphous content cannot be determined from this scan without an internal standard.
