# Powder XRD phase analysis

The accepted model contains four crystalline phases. Fractions are normalized only over those modeled crystalline phases.

| Phase | Space group | Frozen COD reference | wt% |
|---|---:|---:|---:|
| CuWO4 | P-1 (2) | 4000806 | 65.17 |
| WO3 | P2_1/c (14) | 2311041 | 19.46 |
| Cu3WO6 | Pa-3 (205) | 1527404 | 12.98 |
| CuO | C2/c (15) | 1011194 | 2.40 |

## Evidence

The precursor chemistry (CuO + WO3, 700 °C) first supports copper tungstate and residual precursor models. Triclinic CuWO4 accounts for the strong 18.81°, 29.09°, 30.08°, and 31.4–31.5° families. Monoclinic WO3 accounts for the 22.67°, 23.07–23.13°, and 23.89° family. A separate coherent set at 15.20°, 19.80°, 32.50°, 33.79°, 49.70°, 57.60°, and 63.29° requires cubic Cu3WO6. The weak but reproducible CuO pair near 35.10° and 38.32°, together with additional higher-angle lines, gives a positive minor CuO scale. No coherent residual reflection family remained after these four phases were included.

Exact-composition frozen references were compared under matched nuisance refinements. COD 4000806 (P-1 CuWO4) decisively outperformed the monoclinic CuWO4 alternative. COD 2311041 gave the best physical monoclinic WO3 model; tetragonal, hexagonal, and orthorhombic WO3 references left whole-family residuals. COD 1527404 supplies the Cu3WO6 topology, and the higher-symmetry C2/c CuO model (COD 1011194) was retained because C2/c and Cc CuO were profile-indistinguishable at this abundance.

The final bounded coordinate polish selected its converged all-coordinate branch. Its geometry audit found no catastrophic contacts and retained all phase fractions. Shortest refined cation–oxygen distances are chemically plausible for these oxides (approximately 1.94 Å Cu–O in CuWO4, 1.70 Å W–O in WO3, 1.90 Å Cu–O in Cu3WO6, and 1.94 Å Cu–O in CuO).

## Fit and uncertainty

Native replay of `final.gpx` over all 8301 measured points gives Rwp = 3.475% and Rp = 2.497% with 1/max(Iobs,1) weighting. The background remains positive over the full scan. The required staged coordinate polish selected its physical all-coordinate branch without geometry or phase-fraction audit violations. A subsequent residual check showed that the Cu3WO6 peaks had been over-broadened; correcting that crystallite-size term and allowing supported CuWO4/Cu3WO6 microstrain terms before the final scale/background settle reduced reflection-centered residuals. This profile completion changed the Cu3WO6 estimate by about 1.6 wt% relative to the coordinate-polished checkpoint, which is a useful indication of systematic quantitative uncertainty.

The major-phase inventory is well supported, but the fit remains above the counting-noise floor and residual intensity errors are centered mainly on accepted reflections. Consequently, refined oxygen coordinates and specimen/profile terms should not be interpreted as high-precision crystallography. The approximately 2.4 wt% CuO fraction is the least reliable quantitative value because its peaks overlap the major phases; its presence is supported, but its exact fraction and the C2/c versus Cc distortion cannot be determined reliably from this pattern. The monoclinic WO3 topology is secure, while its exact oxygen positions and choice among closely related monoclinic settings carry residual model uncertainty. No amorphous fraction can be inferred from this crystalline-only normalization.
