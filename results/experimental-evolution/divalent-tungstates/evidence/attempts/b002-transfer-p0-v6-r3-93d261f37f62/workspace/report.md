# PXRD phase analysis and Rietveld refinement

## Result

The crystalline material is a three-phase mixture of wolframite-type MgWO4, monoclinic WO3, and residual rocksalt MgO. Fractions are normalized over the modeled crystalline phases; no amorphous fraction can be measured without an internal standard.

| Phase | Space group | Weight fraction | Refined cell (A, degrees) |
|---|---:|---:|---|
| MgWO4 | P 2/c | 51.11 wt% | a = 4.69654, b = 5.68396, c = 4.94755, beta = 90.8255 |
| WO3 | P 21/c | 41.45 wt% | a = 7.68751, b = 7.54144, c = 10.51950, beta = 136.0552 |
| MgO | F m -3 m | 7.43 wt% | a = 4.21054 |

The final fit has Rwp = 1.686%, Rp = 1.319%, Rexp = 1.527%, and goodness of fit = 1.104 over the nominal 10-100 degree 2-theta range. `fit.csv`, the three CIFs, and the reported fractions/statistics were all exported or calculated from a reopened `final.gpx` and cross-checked against it.

## Evidence and model selection

The chemistry is consistent with partial reaction of the stated WO3 and MgO precursors at 700 C. MgWO4 accounts for the strong 18.88 degree line and the 30.41/30.73 degree group; monoclinic WO3 accounts for the characteristic 23.12, 23.57, 24.38, 26.57, and 28.93 degree families. MgO was retained from the weak-phase watch list because its 200 line at 42.92 degrees gives a coherent, phase-specific residual reduction, with corroborating higher-angle 220/222/400 families. The refined amounts also give a bulk Mg:W molar ratio of about 1.02, independently consistent with the precursor context.

The starting records were full-occupancy, non-disordered structures: synthetic MgWO4 (COD 9013902), a room-temperature neutron WO3 structure (COD 2311041), and ambient MgO (COD 9000499). Under the same neutral profile, the selected two-phase MgWO4/WO3 inventory gave Rwp about 9.02%; alternative physical WO3 records COD 1528915 and 2107312 gave about 9.45% and 12.14%, respectively. Adding MgO lowered Rwp to about 8.87% before texture, broadening, or coordinate refinement. Thus the alternate WO3 records were rejected by their diffraction fit, not by chemistry alone.

The final baseline uses a smooth six-coefficient Chebyshev background, one zero correction (-0.00673 degrees), and nonnegative U/W/X terms; V/Y/Z, roughness, and unused phase size/strain terms are zero and inactive. The reported Cu Kalpha1/Kalpha2 wavelengths and fixed 0.5 intensity ratio were used. Effective polarization (0.535) and low-angle SH/L asymmetry (0.0173) were supported across multiple peaks. A MgWO4 [010] March-Dollase correction (1.293) was strongly supported by several isolated families; a small WO3 [111] correction (1.018) survived a removal test. WO3 required complementary isotropic size and strain terms (about 0.156 micrometres and 3986 microstrain), but these correlated nuisance descriptors should not be interpreted as precise microscopy measurements. MgWO4 and MgO size/strain remained neutral. Low-, middle-, and high-angle isolated-family widths were reproduced without a systematic hkl-dependent trend, so anisotropic broadening was not added.

## Structural and quantitative uncertainty

All sites remain fully occupied. The refined MgWO4 coordinates give Mg-O = 2.095-2.134 A and W-O = 1.762-2.134 A. For WO3, only the W positions were refined; its source oxygen coordinates were retained because unconstrained oxygen refinement was poorly determined and produced an implausibly short W-O contact. The submitted WO3 model gives distorted but credible W-O octahedra spanning 1.697-2.166 A. MgO was retained as the ideal rocksalt model with Mg-O = 2.105 A. Consequently, phase identities, cells, and the MgWO4 model are well supported, while the WO3 oxygen coordinates are not independently determined by this powder pattern.

Formal covariance errors on the phase amounts are only 0.06, 0.06, and 0.07 wt% for MgWO4, WO3, and MgO. They exclude preferred-orientation, profile, source-structure, and counting-model uncertainty. A more realistic precision is approximately +/-1 wt% absolute for each major phase and +/-0.5-1 wt% for MgO. The pointwise standard uncertainties were not supplied, so raw-count Poisson weighting was used; this and the absence of an internal standard limit interpretation of the very low residual indices. No additional coherent crystalline family remains evident, but trace phases below the residual/background sensitivity and any amorphous material cannot be quantified reliably.
