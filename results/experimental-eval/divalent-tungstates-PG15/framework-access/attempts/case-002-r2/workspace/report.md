# Powder-XRD phase analysis

The pattern is modeled as two crystalline phases. Fractions are normalized over those modeled crystalline phases; this analysis does not quantify any amorphous material.

| Phase | Structural model | Refined cell | Weight fraction |
|---|---|---|---:|
| Oxygen-deficient barium peroxide, BaO2−x (submitted as Ba2O3.7664) | COD 1521428, I4/mmm | a = 3.81286 Å, c = 6.84606 Å | 0.3247 |
| Tungsten trioxide, WO3 | COD 2311041, P21/c | a = 7.31487 Å, b = 7.53211 Å, c = 10.54723 Å, beta = 133.1929° | 0.6753 |

The WO3 model accounts for the diagnostic low-angle triplet at approximately 23.42°, 23.92°, and 24.66° 2theta and its repeated monoclinic multiplets. In comparable two-phase refinements, COD 2311041 gave Rwp = 8.06% before the final model refinements, versus 8.62% for the closest P21/c alternative, 16.78% for a triclinic alternative, and 18.41% for an orthorhombic alternative. The peroxide-type phase accounts for the strong reflections near 26.33°, 27.07°, 33.54°, 43°, 46.6°, and 55.8°.

The refined tetragonal cell is consistent with the oxygen-deficient peroxide entry COD 1521428 and is not within the small reference-mismatch range of the older stoichiometric BaO2 entry COD 1010113. However, oxygen scattering is weak relative to Ba under Cu radiation. The peroxide framework and its abundance are supported, but the exact oxygen occupancy is not reliably determined by this pattern alone; Ba2O3.7664 should therefore be read as the best matching database model, not as a precise oxygen assay. The short O–O distance (about 1.41 Å) is the expected peroxide dumbbell.

BaO and BaWO4 test phases refined to essentially zero abundance. A second, nearly duplicate P21/c WO3 database entry could absorb roughly 2 wt% as an empirical peak-shape component, but it introduced no independent reflections and was not retained as a distinct phase.

The final full-pattern fit has Rwp = 7.215%, Rp = 5.344%, Rwp,min = 3.641%, and Rwp/Rwp,min = 1.982 over 8,301 points. Some systematic residual remains at strong overlapping peaks, so the normalized fractions are best regarded as approximately 0.325 ± 0.02 and 0.675 ± 0.02 (absolute fraction). Atomic shifts were bounded to the small-reference-mismatch scale; oxygen coordinates are less certain than the Ba and W sublattices. The native GSAS-II replay of `final.gpx` reproduces the submitted profile and fractions without additional optimization.
