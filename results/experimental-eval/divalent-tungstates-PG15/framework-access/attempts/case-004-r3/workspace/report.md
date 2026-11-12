# Powder XRD phase analysis

## Result

The crystalline product is modeled as two phases:

| Phase | Structural model | Refined cell | Weight fraction |
|---|---|---|---:|
| CoWO4 | Wolframite, P 2/c | a = 4.66955 Å, b = 5.68428 Å, c = 4.95072 Å, beta = 89.9619° | 0.2892 |
| WO3 | Monoclinic, P 21/c (alternative setting) | a = 7.69352 Å, b = 7.53735 Å, c = 10.5376 Å, beta = 136.102° | 0.7108 |

The fractions are normalized over the modeled crystalline phases. The fit has Rwp = 4.8129%, Rp = 3.7038%, and weighted chi-square = 17870.31 for 8301 observations, using `1/max(Iobs,1)` weights because the raw-count data have no supplied uncertainties.

## Evidence and refinement

The strong 23.17/23.67/24.41° triplet and the peaks near 26.66° and 29.00° identify monoclinic WO3. Peaks near 15.62°, 19.09°, and 30.71° require wolframite CoWO4. The characteristic series expected for residual CoO or Co3O4 is absent; isolated overlaps do not form a coherent third-phase pattern. A triclinic WO3 model was tested and gave a worse whole-pattern fit than the monoclinic model.

The starting atomic models were COD 5910316 for P 2/c CoWO4 and COD 2311041 for P 21/c WO3. The CoWO4 source listing contained symmetry-expanded duplicate sites, so it was reduced to its valid unique asymmetric sites before refinement. Cell metrics, atomic coordinates, one isotropic displacement parameter per phase, phase scales, specimen displacement, surface roughness, weak March-Dollase terms, and peak-shape/size/strain terms were tested in GSAS-II. WO3 required [001] uniaxial microstrain; the fitted orientation corrections remained close to random (MD approximately 0.979 for CoWO4 [001] and 1.050 for WO3 [110]).

Unconstrained oxygen-coordinate refinement lowered Rwp to about 4.775% but displaced WO3 oxygen sites by about 0.22 Å RMS, outside the stated reference-mismatch envelope. That overfit was rejected. The submitted coordinates use symmetry-preserving corrections constrained to at most 0.04 Å RMS for metals and 0.05 Å RMS for oxygen; both CIFs pass the contact/occupancy screen. A fresh, zero-parameter GSAS-II replay from `final.gpx`, ignoring cached calculated arrays, reproduced Rwp = 4.8129%, the two submitted CIFs exactly, and fractions 0.2891946/0.7108054.

## Remaining uncertainty

Phase identities and unit cells are well supported. The exact oxygen coordinates are not reliably determined from this powder pattern: their constrained corrections reached the allowed envelope, so they should be treated as chemically screened model coordinates rather than precise independent measurements. The phase fractions are estimated to carry about ±0.02 absolute systematic uncertainty (roughly ±2 wt%-points), mainly from correlations among displacement parameters, roughness, preferred orientation, background, and phase scale. No amorphous fraction can be determined from this analysis, and trace crystalline phases below the pattern's detection sensitivity cannot be excluded.
