# Powder XRD phase analysis

## Result

| Phase | Space group | Weight fraction |
|---|---:|---:|
| ZnWO4, wolframite | P2/c (No. 13) | 82.645(181)% |
| ZnO, wurtzite | P6_3mc (No. 186) | 4.883(168)% |
| WO3, monoclinic gamma | P2_1/c (No. 14) | 12.472(110)% |

Fractions are normalized over the three modeled crystalline phases. Parentheses are formal one-standard-deviation values from the GSAS-II covariance matrix; they do not include model-choice or texture systematics. The final full-grid fit has Rwp = 9.198%, Rp = 5.115%, goodness of fit = 3.485, and converged with no frozen variables. Because pointwise experimental uncertainties were not supplied, the goodness of fit is not an absolute statistical test.

## Evidence and model selection

The precursor context is a 1:1 ZnO + WO3 mixture fired at 700 degrees C. The dominant peak family at 15.79, 19.19, 24.11/24.80, 30.76/30.98, 36.69, and 38.58 degrees 2theta indexes as monoclinic wolframite ZnWO4. A scheelite ZnWO4 transfer failed the same peak-family test and gave an early Rwp near 54%, versus about 23% for wolframite under comparable initial refinement.

After fitting ZnWO4, coherent residual families identify both precursors. Wurtzite ZnO accounts for 32.06, 34.90, 47.94, 56.83, and 68.26 degrees. Monoclinic WO3 accounts for the 23.41/23.96/24.66 triplet and peaks near 33.60 and 34.49 degrees, with its remaining reflections overlapping ZnWO4. Orthorhombic, tetragonal, and hexagonal WO3 controls gave checkpoint Rwp values of about 12.21%, 14.59%, and 16.65%. A triclinic WO3 branch reached 9.53% at one checkpoint but collapsed toward a monoclinic metric and produced W-O distances of 1.54-2.35 angstrom; it was rejected as an unphysical intensity overfit. The submitted monoclinic parent retains six-coordinate W sites with final W-O ranges of 1.68-2.22 and 1.79-2.12 angstrom.

The phase inventory also closes the chemistry: per 100 g of crystalline material it corresponds to 0.2639 mol ZnWO4, 0.0600 mol ZnO, and 0.0538 mol WO3. The total Zn:W molar ratio is 1.020, close to the measured precursor ratio without adding an ad hoc phase. No coherent unassigned peak family remains.

## Structural reliability and remaining uncertainty

The frozen reference index did not contain ZnWO4 itself, so its model was transferred from a wolframite Mn/Fe tungstate parent by Zn substitution, then its cell and atomic coordinates were refined. The resulting ZnO6 and WO6 octahedra remain chemically plausible, but oxygen coordinates are less certain than the phase identity and cell.

For ZnO, the cell was refined while the internal oxygen coordinate was retained from the physical reference; an attempted oxygen refinement ran to its bound. For the 12.5% WO3 phase, the cell and W positions were refined from a geometry-valid neutron structure, while oxygen positions were retained from that reference. A bounded WO3 oxygen trial drove 14 coordinate parameters to their limits and was rejected. Thus the ZnO and WO3 topology, unit cell, and phase fractions are supported, but their detailed oxygen coordinates cannot be determined reliably from this X-ray pattern alone.

Preferred-orientation corrections are substantial (especially ZnWO4 [111] and WO3 [110]), so realistic fraction uncertainty is larger than the formal values in the table. The submitted CIFs, fractions, and `fit.csv` were exported from the converged `final.gpx` project.
