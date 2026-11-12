# Powder XRD phase analysis

## Result

The crystalline pattern is adequately described by two residual precursor phases:

| Phase | Structural model | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| BaCO3 (witherite) | Orthorhombic *Pnma* (No. 62) | a = 6.43532, b = 5.31026, c = 8.91817 | 0.54290 (54.29 wt%) |
| WO3 | Monoclinic *P*21/*c* (No. 14) | a = 7.31033, b = 7.54034, c = 10.54424, beta = 133.1315° | 0.45710 (45.71 wt%) |

Fractions are normalized over these modeled crystalline phases. They do not measure amorphous material. A realistic systematic uncertainty is about ±0.02 in absolute fraction (roughly ±2 percentage points), larger than the least-squares precision, because phase scale, texture, roughness, and profile broadening are correlated.

## Evidence and refinement

The chemical context is BaCO3 + WO3 heated at 400 °C. The observed low-angle region contains the diagnostic monoclinic WO3 cluster near 23.43, 23.91, and 24.65° 2theta, while the remaining peak families, including those near 24.22, 28.03, 34–35, 42.29, and 45.17°, are indexed by orthorhombic BaCO3. Physically bounded candidate refinements favored COD 9010928 for BaCO3 and the *P*21/*c* COD 2311041 model for WO3. Alternative carbonate settings/models fitted substantially worse; alternative WO3 polymorphs required implausible lattice/profile excursions and fitted worse under the same bounds.

The final GSAS-II refinement used the supplied Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio, a 20-term Chebyshev background, zero shift, polarization, axial-divergence/profile terms, phase scales and cells, BaCO3 size/microstrain with mild [010] March-Dollase texture, and anisotropic WO3 microstrain. The W sublattice was adjusted only slightly (about 0.040 Å RMS from the reference model). Carbon and oxygen coordinates could not be refined independently without large, chemically implausible shifts, so their reference coordinates were retained; their exact positions are therefore not determined by this powder pattern.

A fresh atomic forward replay of `final.gpx` over all 8301 observations gives Rwp = 5.8329%, Rp = 4.3889%, Rexp = 3.4723%, and goodness of fit = 1.6798 (Poisson counting weights). The replay regenerated structure factors and reflections from the saved atoms rather than using cached calculated arrays. Both submitted CIFs match the project exports and pass the broad contact/occupancy screen.

## Remaining uncertainty

Adding plausible reaction products did not establish a third phase: BaWO4 and Ba3W2O9 each refined to about 0.27 wt%, BaO2 to about 0.14 wt%, and Ba3WO6 to about 0.02 wt%. Those sub-percent values are below reliable quantitative identification here. A second, strongly overlapping WO3 polymorph can absorb up to roughly 1.7 wt% of residual intensity, but its scale and structure are highly correlated with the main WO3 model and are not uniquely supported. Accordingly, no third phase is reported; a minor overlapping crystalline component at approximately the 1–2 wt% level cannot be excluded.
