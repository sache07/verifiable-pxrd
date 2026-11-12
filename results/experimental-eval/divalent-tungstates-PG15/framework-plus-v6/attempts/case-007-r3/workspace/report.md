# Powder XRD phase analysis

## Result

The scan is modeled as three crystalline phases. Fractions are normalized over those phases only.

| Phase | Structural model | Refined cell (angstrom, degrees) | Crystalline wt.% |
|---|---|---|---:|
| MgWO4, wolframite | P 2/c; COD 9013902 | a=4.69016, b=5.67480, c=4.92910, beta=90.7737 | 76.7677 |
| WO3, triclinic | P -1; COD 2106293 | a=7.30361, b=7.53377, c=7.68982, alpha=89.8626, beta=90.8030, gamma=90.0887 | 16.2874 |
| MgO, periclase | F m -3 m; COD 9000499 | a=4.21309 | 6.9450 |

The corresponding atomic models are `phase_mgwo4.cif`, `phase_wo3.cif`, and `phase_mgo.cif`. `final.gpx` is the exact project independently replayed to create `fit.csv` and the fractions above.

## Evidence and model selection

The chemistry is consistent with reaction of the reported MgO and WO3 precursors at 900 degrees C. Wolframite MgWO4 accounts for the dominant peak families across the complete 9.90-100.09 degree 2-theta range. Residual WO3 is required by the coherent 23.43/23.93/24.67 degree cluster and additional families near 34.47 and 50.2 degrees. Periclase MgO is independently supported by its isolated 200 line at 43.209 degrees and its higher-angle family near 62.54 degrees; its scale remains positive after the common profile is rebuilt.

Several WO3 records/polymorphs were challenged under the same restrained nuisance model. Triclinic P -1 COD 2106293 gave the best replay-stable whole-pattern agreement; tested monoclinic alternatives COD 2311041 and COD 1528915 left larger structured residuals. The three retained phases all improve coherent families rather than single bins, and no auxiliary background peaks were used.

## Refinement and fit quality

The Cu K-alpha1/K-alpha2 wavelengths and 0.5 intensity ratio were fixed to the metadata. The full-range GSAS-II Rietveld model used a positive eight-node log-interpolated background, one specimen-displacement correction, common nonnegative U/W/X profile terms, refined polarization, isotropic MgWO4 size broadening, uniaxial WO3 microstrain, and weak replay-stable March-Dollase corrections. Unused size/strain terms were neutralized. The background is positive throughout (273.9-2360.3 counts), and independent replay raised no negative-width, negative-background, occupancy, or displacement-parameter flags.

On the complete measured grid, Rwp is 7.50695%, Rp is 5.27347%, chi-square is 57086.978, and GOF is 2.62797 (8301 points, 35 refined parameters, weights 1/max(counts,1)).

## Remaining uncertainty

The fractions are conditional crystalline-phase fractions: without an internal standard they do not measure amorphous material or absolute reaction yield. Formal scale-covariance uncertainties are about 0.31, 0.13, and 0.34 wt.% for MgWO4, WO3, and MgO respectively, but model/background systematics are likely larger.

The WO3 polymorph assignment is the least secure because its broadened reflections overlap MgWO4. Its cell and scale are supported, and its W coordinates were only slightly adjusted, but the minor-phase oxygen coordinates could not be determined reliably from this powder scan; the published COD 2106293 oxygen geometry was therefore retained. Free oxygen refinement produced large, non-robust shifts and was rejected. Low-level additional crystalline material below the sensitivity of this pattern cannot be excluded.
