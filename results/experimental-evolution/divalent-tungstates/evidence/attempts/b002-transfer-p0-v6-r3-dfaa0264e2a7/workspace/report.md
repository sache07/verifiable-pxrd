# PXRD phase analysis

## Result

The pattern is described by three crystalline phases. Fractions are normalized to the modeled crystalline material; they do not measure amorphous content.

| Phase | Structural model | Weight fraction | Refined cell |
|---|---|---:|---|
| MgWO4, wolframite type | P 2/c, based on COD 9013902 | 51.15 wt% (formal 1σ 0.06 wt%) | a = 4.69595, b = 5.68290, c = 4.94670 Å, β = 90.82496° |
| WO3, monoclinic | P 21/c, based on COD 2311041 | 41.30 wt% (formal 1σ 0.05 wt%) | a = 7.68615, b = 7.54017, c = 10.51776 Å, β = 136.05668° |
| MgO, periclase | F m -3 m, based on COD 9000499 | 7.55 wt% (formal 1σ 0.07 wt%) | a = 4.20986 Å |

The unusual β angle for WO3 is the valid source-cell setting retained from the neutron structure, not a different composition. The phase-weighted Mg:W mole ratio is about 1.025, independently consistent with the MgO + WO3 reaction inventory.

## Evidence and refinement

Coherent peak families support all three phases across the measured range. Diagnostic MgWO4 intensity occurs near 15.56°, 18.88°, 23.82°, and the 30.41/30.75° pair; WO3 accounts for the 23.13/23.57°, 26.58°, 28.93°, and 33.28° families; and MgO is required by its separated 42.93°, 62.26°, 74.57°, 78.88°, and 94.69° reflections (Cu Kα 2θ). These assignments are chemically consistent with partial reaction of the reported WO3 and MgO precursors at 700 °C.

Exact-composition records were available, so no cross-chemistry site substitution was used. The models have full occupancy and reasonable refined geometry: Mg–O = 2.082–2.133 Å and W–O = 1.773–2.145 Å in MgWO4; W–O = 1.693–2.172 Å in WO3; and nearest Mg–O = 2.105 Å in MgO. A triclinic WO3 record and a second monoclinic record were compared under the same nuisance model. The selected P 21/c neutron model was marginally better than the triclinic alternative after WO3 broadening was modeled (Rwp 7.092% versus 7.113% at that inventory stage), used fewer cell variables, and is the physically appropriate room-temperature description.

The final full-range refinement used the reported Cu Kα1/Kα2 doublet, a six-term smooth Chebyshev background, one zero correction, and a common nonnegative U/W/X profile. Unused size, strain, roughness, extinction, and texture terms were neutralized. Only WO3 required replay-stable uniaxial size and strain broadening. MgWO4 required [010] March–Dollase preferred orientation (r = 1.298), supported by multiple low-, middle-, and high-angle families; alternative symmetry-distinct axes fitted substantially worse. MgWO4 symmetry-allowed coordinates and the two WO3 W sites were refined. The WO3 oxygen framework was retained from the neutron source because laboratory XRD does not determine those oxygen coordinates robustly; MgO coordinates are symmetry-fixed.

After save, reopen, and full-range replay, the refinement converged with Rwp = 1.6620%, Rp = 1.3065%, Rexp = 1.5271%, goodness of fit = 1.0911, Durbin–Watson = 1.6933, and maximum shift/σ = 0.0095 for 8,301 observations and 41 variables. `fit.csv`, `result.json`, the CIFs, and these statistics were exported from the reopened `final.gpx` and checked for exact numerical agreement.

## Remaining uncertainty

The tabulated fraction uncertainties are conditional covariance estimates and are much smaller than likely model-systematic error. Preferred orientation, overlap, and the absence of a calibrated instrumental profile or internal standard make approximately 1–2 absolute wt% a more defensible practical precision. The fractions apply only to the three modeled crystalline phases; amorphous material cannot be quantified from this data set.

MgO2, MgWO, MgWO6, WO2, and W3O8 watch-list trials refined to zero or statistically insignificant abundance and lacked coherent supporting residual families. One W18O49 database record generated no usable GSAS-II reflection list, so that specific model could not be tested reliably. No additional phase can be quantified reliably, although an unmodeled trace phase hidden by overlap cannot be categorically excluded. The WO3 phase identity is secure, but the fine distinction among closely related distorted WO3 descriptions and its oxygen coordinates is less certain than the phase assignment or cell.
