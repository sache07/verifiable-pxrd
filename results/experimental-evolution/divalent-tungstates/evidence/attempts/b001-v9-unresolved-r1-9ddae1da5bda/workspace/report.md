# Quantitative phase analysis

## Result

The modeled crystalline material contains four phases. Fractions are normalized over these crystalline phases only; parenthesized uncertainties are GSAS-II covariance estimates and do not include model/systematic uncertainty.

| Phase | Structural model | Refined cell (Å, degrees) | Weight fraction |
|---|---|---|---:|
| PbWO4, scheelite | `I 41/a`, COD 9009811 | a = 5.47280, c = 12.07238 | 0.58284(12) |
| WO3, monoclinic | `P 21/c`, COD 2311041 | a = 7.70103, b = 7.54398, c = 10.53657, beta = 136.1968 | 0.19820(9) |
| Pb3O4, minium | `P 42/mbc`, COD 9012124 | a = 8.81217, c = 6.56800 | 0.17034(12) |
| PbO, massicot | `Pbcm`, COD 2310433 | a = 5.88646, b = 5.49147, c = 4.75613 | 0.04862(7) |

The WO3 model uses the source record's unconventional but valid monoclinic setting. Atomic coordinates and occupancies were kept at the source values because this multiphase laboratory pattern does not determine them reliably; the cells, phase scales, and supported profile terms were refined.

## Evidence and model selection

Scheelite PbWO4 accounts for its strong families at approximately 27.81, 45.13, 55.63, and 72.36 degrees 2theta. Monoclinic WO3 is required by the low-angle 23.53/24.02/24.84-degree family and many additional lines. Minium Pb3O4 accounts for independent families near 26.81, 31.22, 32.55, 34.47, 50.29, and 58.48 degrees. Massicot PbO has a positive replay-stable scale and multiple families near 29.56, 30.89, 38.25, 45.7, 53.6, and 60.9 degrees. Thus each retained minor phase is supported by more than a single overlapped line.

All retained source records and all final CIFs passed `learned/cif_health.py`: they are ordered, have full valid occupancies, and show no flagged hard contacts. Important competitors were fitted under the same nuisance model. Raspite PbWO4 and partially occupied Pb7W8O28.8 collapsed to zero scale when added as watch phases; replacing scheelite with the latter gave Rwp 4.17% rather than 3.32%. A triclinic WO3 record reached Rwp 3.41% and was inferior to the retained monoclinic model. Orthorhombic Pb3O4 gave 7.11%. A reviewed tetragonal Pb3O4 record containing a 1.79 Å O-O contact gave 3.48%; the healthy ordered record fits better and has no such contact. Alternate PbO records were poorer or unstable. These records were treated as structural competitors, not extra phases.

After reconvergence, scale-only watch tests gave 0.050(25) wt% litharge and 0.028(27) wt% PbO2, with Rwp improvements of only 0.0007 and 0.0001 percentage point. Their nominal non-overlapped strong lines have absent/negative residuals, while small positive residuals coincide with retained-phase reflections. Neither has two independent non-coincident residual families, so neither is reported as a phase.

## Refinement and profile checks

The final GSAS-II replay used the full 9.9034–100.0946 degree range, the reported Cu Kalpha1/Kalpha2 wavelengths and fixed 0.5 intensity ratio, raw-count Poisson weights, a six-term Chebyshev background, nonnegative U/W/X, one refined zero correction, and one surface-roughness term. Inactive size, strain, texture, roughness, extinction, and anisotropic terms were explicitly neutral. Supported phase broadening was isotropic size for PbWO4 (0.0609 micrometre) and Pb3O4 (0.0330 micrometre), and isotropic microstrain for PbO (10425 ppm); these effective profile values should not be read as independent microscopy measurements.

The reopened-project fit has Rwp = 3.3193%, Rp = 2.5548%, Rexp = 2.4853%, goodness-of-fit = 1.3379, and Durbin-Watson = 1.1591. Two disk replays converged with final maximum shift/esd 0.004. Representative background-subtracted peak checks are:

| Family | Position observed / calculated (degrees) | FWHM observed / calculated (degrees) | Left/right half-width observed | Left/right half-width calculated |
|---|---:|---:|---:|---:|
| WO3 low | 23.5299 / 23.5299 | 0.1336 / 0.1298 | 0.0550 / 0.0787 | 0.0526 / 0.0772 |
| PbWO4 low | 27.8113 / 27.8113 | 0.2487 / 0.2500 | 0.1187 / 0.1300 | 0.1187 / 0.1313 |
| PbWO4 middle | 45.1323 / 45.1214 | 0.3218 / 0.3183 | 0.1453 / 0.1765 | 0.1346 / 0.1837 |
| PbWO4 high | 72.3635 / 72.3744 | 0.4357 / 0.4764 | 0.1696 / 0.2661 | 0.2077 / 0.2686 |
| PbWO4 highest | 94.0420 / 94.0528 | 0.5747 / 0.6345 | 0.1879 / 0.3868 | 0.2240 / 0.4106 |

Because the goodness-of-fit remains above the ideal counting-only expectation and high-angle calculated peaks are modestly broader, targeted alternatives were replayed. Surface roughness B improved Rwp from 4.18% to 3.32% and was retained at an interior value. Four- and five-term backgrounds were materially worse; eight terms produced correlated oscillatory coefficients. Polarization refined beyond its physical range. Sample displacement required an unstable approximately -730 micrometre value. SH/L asymmetry, combined roughness terms, Pb3O4 strain in place of size, PbO size in place of strain, and axial/diagonal March-Dollase texture gave no stable complementary improvement; texture ratios returned to 1.003 and 0.994. No bound nuisance term was used as phase evidence.

## Chemical balance and uncertainty

The metadata reports WO3 and Pb3O4 precursors but no amounts or ratio, so there is no fixed numerical precursor constraint to impose and feed closure cannot be claimed. As a consistency check only, the normalized crystalline result contains Pb:W = 1.0507 and corresponds to an equivalent Pb3O4:WO3 molar feed ratio of 0.3502, close to 1/3 for `Pb3O4 + 3 WO3 -> 3 PbWO4 + 1/2 O2`. Residual WO3 and Pb3O4 indicate incomplete conversion, while `2 Pb3O4 -> 6 PbO + O2` provides a charge-balanced route to PbO. All retained formulas are charge balanced. The balance-motivated non-1:1 Pb7W8O28.8 model was explicitly tested and rejected by zero scale and its reviewed partial occupancies; there is no coherent residual/imbalance combination requiring an invented analogue.

The quoted fraction errors are statistical and likely optimistic. Systematic uncertainty arises from the absent calibrated instrument profile, unknown polarization and specimen packing/roughness, strong Pb/W absorption, the large common angular zero correction, and possible amorphous material (no internal standard was supplied). Phase identities and the four-phase inventory are well supported, but absolute bulk fractions including amorphous content cannot be determined from these data.
