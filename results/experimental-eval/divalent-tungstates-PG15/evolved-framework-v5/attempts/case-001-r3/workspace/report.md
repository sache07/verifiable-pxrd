# Powder XRD phase analysis

## Result

The crystalline specimen is modeled as two unreacted precursor phases:

| Phase | Structural model | Refined cell (Å, °) | Weight fraction* |
|---|---|---|---:|
| BaCO3, witherite | Pmcn (No. 62; Pnma-equivalent), COD 9010928 | a = 5.30821, b = 8.91559, c = 6.43308 | 0.5324 (53.24 wt%) |
| WO3, monoclinic | P21/c (No. 14), COD 2311041 | a = 7.69285, b = 7.53728, c = 10.54109, beta = 136.11381 | 0.4676 (46.76 wt%) |

\*Normalized over the modeled crystalline phases only.

The full-grid refinement gives Rwp = 5.9389%, Rp = 4.5121%, Rexp = 3.4807%, and goodness of fit = 1.7096 for 8,301 observations. The least-squares fraction standard uncertainty is 0.0014 for each phase, but it excludes model and specimen-effect uncertainty; about 1 wt% absolute is a more appropriate reporting precision.

## Evidence and model selection

The metadata identifies BaCO3 and WO3 precursors heated to only 400 °C. The witherite model accounts for the families near 24.2–24.7°, 34–35°, 42–47°, and 55–56° 2theta. Monoclinic WO3 accounts for the interleaved reflections near 23.4 and 23.9° and their higher-angle families. In the final two-phase state, every coherent reflection family maps to one of these phases.

Exact-composition references and plausible reaction product BaWO4 were tested. The selected P21/c WO3 reference retained six-coordinate, physically reasonable WO6 geometry and was preferred to a marginally lower-symmetry triclinic checkpoint whose Rwp gain was negligible. An older monoclinic WO3 entry was rejected because it produced an under-coordinated W environment. The refined structures remain chemically physical: C–O distances are 1.308–1.310 Å, and W–O distances are 1.773–2.138 Å.

BaWO4 was not accepted as a phase. Its strongest distinctive family around 32.1° is absent, its trial scale was only trace-sized, and further refinement made its size/cell/profile unstable rather than supporting a broad independent family. Therefore neither a BaWO4 structure nor fraction can be determined reliably from this pattern. A sub-percent to roughly 1 wt% crystalline amount cannot be excluded, and amorphous material is not quantified by the normalized fractions.

## Refinement and verification

The Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio were fixed to the metadata. With pointwise uncertainties unavailable, Poisson count weights were used. Refinement proceeded through background and phase scales, specimen displacement, cells and calibration/profile terms, bounded heavy- then light-atom coordinates, physical displacement parameters, surface roughness, mild BaCO3 [001] preferred orientation, and supported uniaxial peak broadening. The final coordinates were fixed after bounded refinement, and the final project contains positive phase scales and physical peak widths.

The submitted `final.gpx` was independently reloaded and replayed from freshly generated GSAS-II reflection lists over the entire original grid. It reproduced Rwp = 5.9389% with no profile review flags. The replay-exported structures agree with `BaCO3.cif` and `WO3.cif`, and the replayed fractions exactly match `result.json` at the reported precision.
