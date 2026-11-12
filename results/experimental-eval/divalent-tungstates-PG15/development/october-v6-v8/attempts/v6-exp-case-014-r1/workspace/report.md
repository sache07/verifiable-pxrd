# PXRD phase analysis

The Cu Kα reflection pattern (10.05–99.95° 2θ refinement range) from the SrCO3 + WO3 material heated at 900 °C is best described by three crystalline phases. The quantitative values below are normalized over those modeled crystalline phases; there is no internal standard or amorphous-phase correction.

| Phase | Structural model | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| SrWO4, scheelite | COD 1546036; *I*41/*a* | a = 5.41859, c = 11.95978 | 0.7391 (73.91 wt%) |
| WO3, monoclinic | COD 2311041; *P*21/*c* | a = 7.68891, b = 7.53844, c = 10.53233, β = 136.0852 | 0.0928 (9.28 wt%) |
| Sr3W2O9 | COD 2311977; *C*2/*c* | a = 9.62829, b = 5.52393, c = 13.44125, β = 103.6321 | 0.1682 (16.82 wt%) |

The regenerated fitted-range statistics are Rwp = 12.918%, Rp = 9.135%, Rexp = 3.534%, and goodness-of-fit = 3.656. Pointwise standard uncertainties were not supplied, so Rexp and goodness-of-fit depend on inferred counting weights and should not be interpreted as an absolute noise-model test.

## Evidence for the phase model

Scheelite SrWO4 accounts for the dominant peak family. Monoclinic WO3 accounts for a weaker but reproducible set consistent with residual precursor/intermediate material. Adding Sr3W2O9 explains several coherent residual peaks, including the family near 29.75°, 32.63°, and 44.67° 2θ, without strong absent predictions. A composition-blind cell search also ranked this as the only close Sr-W-O atomistic match to that metric.

Matched leave-one-out refinements raised Rwp from about 12.93% to 40.57% without SrWO4, 15.03% without WO3, and 16.34% without Sr3W2O9. Thus all three scales have complete-pattern support rather than credit from a single overlap. The accepted nuisance model includes refined global Gaussian/Lorentzian profile terms and polarization, specimen displacement, and—only for Sr3W2O9—positive isotropic microstrain (~4730) and mild March-Dollase [110] texture (ratio 1.610). Total Gaussian and Lorentzian widths are positive for every regenerated reflection. No phase-size term or additional phase strain term met the stability/material-improvement criteria.

Refining the scheelite oxygen position and the Sr/W positions in Sr3W2O9 produced multi-region improvements and geometrically parseable structures. Restoring their source coordinates in matched branches worsened Rwp to 13.02% and 13.28%, respectively. The exported CIF audits found no occupancy, duplicate-site, symmetry-expansion, or short-contact screen flags. The shortest refined Sr3W2O9 W–O contact is about 1.626 Å; the phase identity is well supported, but its detailed heavy-atom coordinates are less certain than its cell and scale.

## Alternatives and remaining uncertainty

The WO3 identity and approximate fraction are robust, but its exact low-symmetry polymorph is not unique from this powder pattern. A final triclinic WO3 replacement reached Rwp = 12.925% versus 12.918% for the selected monoclinic model, despite two additional independent cell parameters and slower/incomplete cell convergence. Monoclinic *P*21/*c* is therefore the parsimonious choice, but the symmetry assignment should be regarded as weakly preferred rather than definitive. Tetragonal WO3 remained much worse (Rwp = 14.445%), and monoclinic SrWO4 was grossly incompatible (initial regenerated Rwp ≈ 98%).

A fourth SrO branch refined to about 0.48 wt% and lowered Rwp by only ~0.020 percentage point, but its strongest predicted reflections did not behave as a phase: local weighted residuals worsened at 111, 220, and 331, while most credit came from high-angle overlap. SrO2 branches were unstable or required implausible cell drift; one apparent orthorhombic “SrO2” library entry was actually incomplete Sr(OH)2. These trace candidates were rejected. Weak residual intensity remains, but no fourth atomistic structure or fraction can be determined reliably; the three reported fractions are therefore conditional on the accepted crystalline model.

The fractions should be treated as semi-quantitative rather than precise to the displayed digits. Model choice, preferred orientation, the Sr3W2O9 coordinates, absorption, and any unmodeled/amorphous material dominate over formal last-stage scale errors. `result.json` retains full numerical values for cross-file consistency.

## Integrity checks

`final.gpx` is the frozen GSAS-II project used for the submitted CIFs, fractions, and `fit.csv`. Fresh profile/reflection regeneration exactly reproduced the saved profile. The final project audit reported convergence, zero dropped variables, max shift/esd = 0.027, positive total widths for all reflections, and no flags. All three submitted CIFs passed `learned/cif_audit.py`.
