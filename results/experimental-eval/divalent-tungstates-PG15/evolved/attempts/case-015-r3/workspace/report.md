# Quantitative phase analysis

The pattern is modeled by three crystalline phases. Fractions are normalized over those modeled crystalline phases only.

| Phase | Space group and refined cell (Å, °) | Weight fraction |
|---|---|---:|
| ZnWO4, wolframite | P 2/c; 4.69335, 5.72173, 4.92892, β = 90.6346 | 74.54 wt% |
| WO3, room-temperature monoclinic | P 21/n; 7.30511, 7.54006, 7.69593, β = 90.8211 | 18.38 wt% |
| ZnO, wurtzite | P 63mc; a = 3.25199, c = 5.21199 | 7.08 wt% |

Formal one-sigma fraction uncertainties from the covariance matrix are 0.10, 0.09, and 0.08 absolute wt%, respectively. These values do not include model selection, background/profile, specimen, or reference-structure uncertainty; about 1–2 absolute wt% is a more conservative practical uncertainty. No amorphous fraction can be obtained from these data without an internal standard.

## Phase evidence and structural choices

The chemistry is consistent with ZnO + WO3 reacting at 900 °C to form dominant ZnWO4 while leaving both precursors. ZnWO4 accounts for the dominant pattern. Monoclinic WO3 is required by coherent families near 23.3, 26.7, 28.9, 33.3–34.3, 50.1, and 56.1° 2θ. Wurtzite ZnO is independently supported by its characteristic family near 31.9, 34.4, 36.4, 47.6, 56.8, 63.0, 68.0, and 69.3° 2θ, including several peaks that are unique or only partly overlapped. No additional coherent residual family justifies a fourth phase.

Full-occupancy, chemically ordered records were used. The ZnWO4 model is based on COD 1520641 and ZnO on COD 9004178. For WO3, several exact-composition polymorphs were challenged under a common nuisance model. Orthorhombic, tetragonal, and high-pressure monoclinic records fit materially worse. A triclinic P-1 model gave only a tiny improvement in the early screen while its angles collapsed to nearly monoclinic values, so the extra cell degrees of freedom were rejected.

The initially screened room-temperature WO3 record (COD 1528915) had coarse coordinates and an inherited 1.58 Å O–O contact. It was replaced by the room-temperature neutron structure COD 2311041, transformed by a unimodular basis change into the near-orthogonal P 21/n setting. Under the same 37-parameter model this both removed the short contact and lowered Rwp from 5.357% to 5.012%. The submitted WO3 structure has sixfold W–O distances of about 1.71–2.16 Å. Submitted ZnWO4 distances are W–O 1.79–2.18 Å and Zn–O 1.97–2.20 Å; the ZnO tetrahedra are also normal.

## Refinement and residual checks

The GSAS-II refinement used the reported Cu Kα1/Kα2 wavelengths and fixed 0.5 intensity ratio, Poisson count weights, an eight-coefficient Chebyshev-1 background, one specimen-displacement correction, and a common nonnegative W/X profile with U fixed at zero. SH/L asymmetry and a two-parameter Bragg–Brentano surface-roughness correction were retained after replay. Polarization refinement ran to a bound and was rejected. All phase scales and cells were refined.

Phase size and strain were tested from neutral values one phase at a time. Only isotropic WO3 microstrain was supported, refining reproducibly to 3183(111) microstrain. The no-broadening model gave Rwp = 5.291%; size alone gave 5.128%, while adding size to strain drove size to the 10 µm neutral ceiling and became singular, so size was pruned. A weak ZnWO4 [110] March–Dollase term, 1.0164(25), is supported by multiple separated families; removing it gives Rwp = 5.026%. Other tested texture axes were inferior or returned near random orientation. ZnWO4 coordinates were retained because resetting them to the source structure raised Rwp to 5.070% after reconvergence, while the refined octahedra remained physical. WO3 coordinates and ZnO's internal coordinate were held to their reference values because unconstrained powder-only refinement was unstable or unresolved.

The final replay converged with maximum shift/e.s.d. = 0.003. Fit statistics are Rwp = 5.012%, Rp = 3.918%, Rexp = 3.796%, and goodness-of-fit = 1.323 for 8,284 points and 37 refined parameters. The difference profile is mostly counting-scale noise; the largest remaining features are derivative-like shape/intensity residuals around the strongest low-angle peaks rather than a coherent missing-phase series. Fractions and structures in `result.json`, the three CIFs, and `fit.csv` were exported directly from `final.gpx` after that replay.
