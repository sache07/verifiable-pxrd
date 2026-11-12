# Powder XRD phase analysis

The pattern is modeled by two crystalline phases: **97.63 wt% wolframite MnWO4** and **2.37 wt% monoclinic WO3**, normalized over the modeled crystalline material. The exact no-fit replay of `final.gpx` gives Rwp = 4.468%, Rp = 3.408%, and GOF = 1.621 on all 8301 measured points.

## Evidence

The P2/c wolframite model accounts for every major family, including the peaks at approximately 15.72, 18.70, 23.90, 24.37, 30.12, 30.60, 31.37, 36.25, and 37.53 degrees 2-theta. Its refined cell is a = 4.83211, b = 5.75823, c = 4.99743 A and beta = 91.2177 degrees. The available exact MnWO4 COD record was measured at 2.4 GPa, so it was used only as a wolframite seed; the refined ambient-sized cell and the same topology in Fe/Zn/Mg tungstate analogues support the assignment.

Adding monoclinic WO3 removes coherent residual families at about 23.47 (002), 24.70 (20-2), 33.94-34.49, and 47.59-50.23 degrees and improves Rwp from 5.077% for the one-phase model to 4.468%. A physically screened neutron P21/c record (COD 2311041) gave the best replay among the tested WO3 records. The refined WO3 cell is a = 7.30339, b = 7.54263, c = 10.5323 A and beta = 133.137 degrees. Triclinic and orthorhombic alternatives gave poorer fits, while tetragonal and hexagonal records refined to negligible scales.

Both MnO records and Mn3WO6 were rejected on the final common profile; Mn3WO6 reached zero scale. Final re-challenges gave less than 0.11 wt% MnO at under 2 sigma and about 0.13 wt% Mn3O4 at about 1 sigma, without convincing unique reflection families, so these were not retained.

## Refinement and uncertainty

The baseline used a smooth eight-term Chebyshev background, one specimen-displacement correction, a nonnegative common peak profile, low-angle asymmetry, and a one-parameter surface correction. Separate WO3 size/strain terms were unsupported and pruned. Instrument U and W sit at the adopted search limits and X was fixed because it is degenerate with Lorentzian size, so the individual width parameters are not uniquely determined even though isolated low-, middle-, and high-angle families are reproduced. The weak [001] texture correction is also nearly tied with [110]. The final project has no frozen parameters, negative widths, negative background, or replay review flags; its CIFs exactly match the saved project.

The formal scale covariance gives about 0.05 wt% (1 sigma) uncertainty for the WO3 fraction, but profile, ADP, and polymorph choices make a more realistic uncertainty roughly 0.2 wt%. MnWO4 coordinates are diffraction-refined. The weak WO3 signal supports its phase, symmetry, cell, and fraction, but not an independent refinement of all internal coordinates: unconstrained coordinate trials produced excessive shifts and short contacts. Its submitted internal coordinates therefore remain those of the screened neutron model, and should not be interpreted as newly determined from this pattern. No amorphous fraction can be obtained from these data.
