# Crystalline phase analysis

## Result

The pattern is described by three crystalline phases. Weight fractions are normalized over these modeled crystalline phases; they do not include any amorphous material.

| Phase | Structural model | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| MgWO4 | wolframite, `P 2/c`, COD 9013902 | a = 4.69592, b = 5.68287, c = 4.94674, β = 90.8250 | 0.51388 ± 0.00070 |
| WO3 | monoclinic, `P 21/c`, COD 2311041 | a = 7.68631, b = 7.54008, c = 10.5172, β = 136.049 (source setting) | 0.41286 ± 0.00066 |
| MgO | rocksalt, `F m -3 m`, COD 9000499 | a = 4.20985 | 0.07326 ± 0.00089 |

The final full-range GSAS-II fit uses 8,301 points from 9.9034° to 100.0946° 2θ and gives Rwp = 2.2189%, Rp = 1.6994%, GOF = 1.4556, and χ² = 17,526.05 with 29 varied parameters. The tabulated uncertainties are covariance-derived one-sigma estimates and are smaller than likely model-dependent systematic errors.

## Chemical and diffraction evidence

The metadata reports WO3 and MgO precursors heated at 700 °C, but no precursor amounts or ratio. MgWO4 is therefore the chemically expected 1:1 reaction product, while WO3 and MgO are physically plausible residual precursors. The refined residual WO3 and MgO quantities are nearly equimolar (within about 2%), but no balance constraint was imposed because the feed ratio was not reported.

- MgWO4 accounts for the sharp wolframite families at approximately 18.88°, 23.82°, and the resolved 30.41°/30.73° pair, as well as many independent middle- and high-angle families.
- Monoclinic WO3 accounts for the broader 23.13°/23.57°/24.37° group and the 33.27°/34.16° group. Tetragonal, orthorhombic, hexagonal, alternate monoclinic, and triclinic WO3 records were challenged rather than treated as coexisting phases.
- MgO has positive scale in every valid replay. Its non-coincident (111) and (200) families occur at 36.94° and 42.92°; the (220), (311), (222), and (400) families provide additional, partly overlapped support. Activating the fixed-source-cell MgO scale lowered Rwp from 3.074% to 2.527% and gave 6.92 wt%; cell refinement gave 7.10 wt%, and the complete replay gave 7.33 wt%. This is not a one-peak or scale/background artifact.

The selected WO3 record was re-compared from a common neutral checkpoint with physically distinct records. After each model received its own width and texture loop, COD 2311041 reached Rwp = 2.220%, compared with 3.062% for alternate monoclinic COD 1528915 and 2.346% for triclinic COD 2106293. The triclinic model briefly ranked better at the neutral-width stage, but lost after cross-seeded elaboration and refined toward a pseudo-monoclinic metric (α and γ near 90°, β near 90.9°). Since observed splitting does not require the extra triclinic degrees of freedom, `P 21/c` was retained. No coherent residual families remained to justify a fourth phase or a non-1:1 analogue.

All retained source CIFs were screened before fitting. All three exported final CIFs also pass `learned/cif_health.py`, with ordered full-occupancy sites, no hard contacts, and minimum contacts of 1.781 Å for MgWO4 and 1.715 Å for WO3. One malformed WO3 record with a 0.464 Å hard contact was not admitted. Geometry health was used only as a necessary screen; polymorph selection came from the diffraction challenges above.

## Refinement and replay checks

Cu Kα1/Kα2 wavelengths and the reported 0.5 intensity ratio were fixed from the metadata. With no supplied pointwise uncertainties, count-statistical weights (1/count) were used. The accepted model contains an eight-term smooth Chebyshev-1 background, one zero correction (−0.0189°), nonnegative U/W/X profile terms, and refined polarization. Roughness remained zero and SH/L remained fixed; no repeated asymmetry required releasing it.

MgWO4 and MgO retain neutral isotropic broadening (10 µm size, zero microstrain). WO3 requires combined isotropic size and strain broadening (about 0.172 µm and 4.44 × 10³ microstrain). Size-only and strain-only WO3 trials gave Rwp = 2.440% and 2.331%, versus 2.220% combined. The two broadening values are strongly correlated (r = 0.939), so they should be regarded as profile descriptors rather than precise microstructural measurements. All MgWO4 and MgO phase-width trials collapsed or met a bound and were discarded by reloading the neutral checkpoint.

A March-Dollase term along MgWO4 [010] (ratio 1.302) is strongly supported. A mild WO3 [100] term (ratio 1.027) replays from Rwp = 2.272% to 2.220% without shifting fractions materially. MgO texture was rejected: its apparent [110] gain changed the fraction from about 7.3% to 6.0% and had 96% scale correlation, indicating a scale surrogate. The final project has no frozen or bound parameters, and a second full convergence loop preserved the source ranking, terms, and fractions.

## Low/middle/high-angle profile audit

The table reports observed/calculated maximum position and left/right half-widths with FWHM, all in degrees 2θ. A seven-point Savitzky-Golay filter was applied only to the observed curve for this diagnostic; the refinement and submitted profile use the original counts.

| Range and family | Maximum obs/calc | L/R obs (FWHM) | L/R calc (FWHM) |
|---|---:|---:|---:|
| Low, MgWO4 (100) | 18.8791 / 18.8791 | 0.0657 / 0.0672 (0.1329) | 0.0651 / 0.0682 (0.1334) |
| Low, WO3 (20-2) | 23.1278 / 23.1278 | 0.1087 / 0.1172 (0.2258) | 0.1064 / 0.1136 (0.2200) |
| Middle, MgO (111) | 36.9499 / 36.9390 | 0.0802 / 0.1017 (0.1820) | 0.0705 / 0.1110 (0.1815) |
| Middle, MgO (200) | 42.9264 / 42.9156 | 0.0758 / 0.1208 (0.1965) | 0.0654 / 0.1368 (0.2022) |
| High, family near 88.33° | 88.3262 / 88.3262 | 0.1035 / 0.1373 (0.2408) | 0.0991 / 0.1424 (0.2416) |
| High, family near 98.90° | 98.8884 / 98.8992 | 0.1131 / 0.1087 (0.2218) | 0.1086 / 0.1020 (0.2106) |

Across the nine audited families, maxima agree within one data step (0.0109°) and absolute FWHM differences range from 0.0004° to 0.0112°. Segment Rwp values are 2.368% (9.9–40°), 2.297% (40–70°), and 1.905% (70–100.1°), with no monotonic angular residual trend.

## Remaining uncertainty

The phase identities and presence of all three phases are well supported. The exact local WO3 symmetry is less certain than the inventory because the triclinic competitor is pseudo-symmetric and profile nuisance terms couple to its ranking; the simpler monoclinic model is nevertheless preferred by the complete replay. Atomic coordinates were inherited from the screened source structures and were not independently refined, so the CIFs are phase models with refined cells, not new determinations of atomic positions.

Without an internal standard, absolute amorphous content and fractions relative to the whole specimen cannot be determined. The submitted fractions are therefore only for the modeled crystalline material. Trace phases below the detection supported by this dataset also cannot be excluded.
