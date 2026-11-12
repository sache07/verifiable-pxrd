# Powder XRD phase analysis

The pattern is explained by two crystalline phases. Weight fractions are normalized over these modeled crystalline phases; they do not quantify any amorphous material.

| Phase | Space group and refined cell | Weight fraction |
|---|---|---:|
| Monoclinic γ-WO₃ | *P*2₁/*c*; *a* = 7.69307 Å, *b* = 7.53615 Å, *c* = 10.5452 Å, β = 136.156° (non-conventional basis) | 0.76273 (76.27 wt%) |
| Spinel Co₃O₄ | *Fd*3̅*m*; *a* = 8.08355 Å | 0.23727 (23.73 wt%) |

## Evidence

The Co₃O₄ assignment is fixed by the spinel reflection series, including peaks at approximately 19.38°, 31.64°, 37.20°, 45.14°, 59.68°, and 65.55° 2θ. Monoclinic WO₃ accounts for the dense split multiplets around 23.3–24.9° and the remaining families throughout the scan. These assignments are chemically consistent with the stated Co₃O₄ and WO₃ precursors after heating at 500 °C.

Exact-composition starting structures were COD 2311041 for WO₃ and COD 9005896 for Co₃O₄. Alternative WO₃ checkpoints gave poorer whole-pattern agreement. Candidate CoWO₄ models required strong reflection families, notably in the 30–31° region and elsewhere, that are absent. After the two accepted phases were fitted, the largest residuals were bipolar features on the flanks of their existing peaks rather than a new coherent family, so no third crystalline phase was accepted.

The final GSAS-II model used the reported Cu Kα₁/Kα₂ doublet, refined phase scales and cells, background, angular calibration/specimen displacement, bounded profile terms, polarization and surface roughness. A uniaxial WO₃ strain term was supported; preferred orientation was not. Heavy-atom coordinates and the Co₃O₄ oxygen coordinate were refined, while WO₃ oxygen shifts were bounded to retain ordinary octahedral geometry. The exported structures pass the geometry screen: W–O distances are 1.724–2.159 Å and Co–O distances are 1.912–1.932 Å.

Fresh, zero-optimization replay of `final.gpx` over all 8,301 measured points gives *R*wp = 3.05296%, *R*p = 2.19262%, *R*exp = 1.71945%, and goodness of fit = 1.77554. The replay reported no physical/profile review flags, and `fit.csv` contains the replayed observed, calculated, difference, and background arrays on the complete original grid.

## Remaining uncertainty

The phase identities and major-phase inventory are reliable. The scale covariance alone corresponds to about 0.14 wt% conditional precision, but correlations with displacement parameters, surface roughness, fixed displacement factors, and peak-shape choices dominate the realistic uncertainty. An estimated uncertainty of about ±2 absolute wt% is therefore assigned to each normalized fraction.

The WO₃ oxygen coordinates are less securely determined than the topology and tungsten sublattice because laboratory X-ray intensity is W-dominated; they should not be interpreted as a high-precision bond-geometry determination. Absolute lattice and microstructure parameters also inherit uncertainty from the correlated zero/specimen-displacement correction, whose specimen-shift term reached the imposed physical bound. Trace crystalline phases below the pattern's detection sensitivity and amorphous content cannot be excluded or quantified, but no unresolved coherent reflection family remains.
