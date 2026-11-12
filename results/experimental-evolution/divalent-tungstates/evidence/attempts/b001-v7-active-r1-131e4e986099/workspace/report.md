# PXRD phase analysis

## Result

The pattern is described by three crystalline phases. Fractions are normalized over those modeled crystalline phases; uncertainties in parentheses are the formal GSAS-II least-squares ESDs in percentage points.

| Phase | Structure | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| SrWO4 | scheelite, I 41/a | a = 5.38364, c = 11.87971 | 60.084(149)% |
| WO3 | monoclinic, P 21/n | a = 7.27617, b = 7.54199, c = 7.68025, beta = 90.8913 | 24.826(121)% |
| SrCO3 | orthorhombic, Pnma | a = 6.01261, b = 5.08923, c = 8.37832 | 15.090(148)% |

The final full-range replay gives Rwp = 3.6480%, Rp = 2.8205%, Rexp = 2.8612%, and goodness-of-fit = 1.2750 over 9.9034–100.0946° 2theta. The Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio from the metadata were retained.

## Phase and chemical evidence

The precursor and temperature context (WO3 + SrCO3, 650 °C) supports an incomplete solid-state reaction,

`SrCO3 + WO3 -> SrWO4 + CO2`,

with both starting phases remaining. On a one-gram modeled-crystalline basis, the refined amounts are 0.001791 mol SrWO4, 0.001071 mol WO3, and 0.001022 mol SrCO3. The two residual precursor amounts differ by only 4.8%, and the reconstructed initial Sr:W ratio is 0.983:1. This independent element balance supports the three-phase assignment and a near-1:1 precursor charge balance.

The structural starts were monoclinic WO3 (COD 1528915), SrCO3 (COD 9008198), and a scheelite SrMoO4 parent (COD 2300460) with Mo physically substituted by W. The SrWO4 oxygen coordinate was refined with four equivalent W–O restraints at 1.79(2) Å; the submitted structure has W–O = 1.794 Å and Sr–O = 2.483/2.638 Å. An unrestrained oxygen refinement lowered Rwp but shifted W–O to about 1.93 Å and was rejected as chemically unreliable. The final restraint gives the expected tetrahedral geometry. WO3 has six nearest W–O distances of approximately 1.85–2.14 Å, while the SrCO3 carbonate C–O distances are approximately 1.289–1.302 Å.

Alternative WO3 structures were challenged with the same background, profile, texture, cell, and strain freedoms. At that comparison stage, the retained P 21/n model gave Rwp = 3.905%; the best Pnma alternate gave 4.814% and the best P 4/n c c alternate 7.137%, with coherent misfit peaks. Scheelite CaWO4, BaWO4, EuWO4, and SrMoO4 analogues were also screened; the Sr-site-matched SrMoO4 parent gave the most physical substitutional start. Charge-balanced non-1:1 Sr–W–O possibilities were revisited. The exact Sr3W2O9 record (COD 2311977) refined to only 0.160(59) wt% and changed Rwp by 0.0016 percentage point without supplying a unique residual family, so it is a watch-list phase rather than a reliable detection. No other coherent unassigned peak family remained.

## Refinement and profile evidence

Because pointwise uncertainties were not supplied, sigma = sqrt(max(counts, 1)) was used without smoothing, resampling, or background subtraction. The accepted nuisance model uses an eight-term smooth Chebyshev background, one angular correction (zero = -0.63774°), a nonnegative common profile with U fixed at its zero boundary and W/X refined, and polarization = 0.6445. Six background terms fit slightly worse; twelve improved Rwp by only 0.030 percentage point. Surface roughness refined negative and was more than 99.9% correlated, while axial-divergence SH/L worsened the fit, so both were neutralized before texture was assessed.

Distinct axial and diagonal March–Dollase axes were compared. The retained terms are SrWO4 [110], r = 0.7524; WO3 [001], r = 1.3549; and SrCO3 [001], r = 0.8070. Isotropic size terms were unsupported. WO3 alone required angle/hkl-dependent width treatment: isotropic strain gave Rwp = 4.045%, whereas uniaxial strain along [010] gave 3.905% before the restrained SrWO4 coordinate refinement; size plus strain was worse at 4.235%. A monoclinic generalized-strain challenge gave only a 0.008-point Rwp change for three principal terms, with S004 = 86(149), and six-/nine-term trials generated non-positive width combinations and no stable replay improvement. The two-parameter, positive uniaxial model was therefore retained.

After unsupported and bound terms were pruned, the project was saved, reopened, replayed over the full measured range, saved again, and reopened for export. A final machine check found exact agreement between that reopened project and every fraction, fit statistic, and profile column in the submitted JSON/CSV; the rounded CIF cells also agree with the project.

The table records maxima and half-height widths from phase-isolated measured profiles (`observed - total calculated + calculated phase`) and the corresponding calculated phase profiles. Each entry is `observed / calculated`, in degrees 2theta. The measured curves were lightly smoothed only for this numerical audit, not for refinement.

| Phase | Region, representative hkl | Position | Left half-width | Right half-width | FWHM |
|---|---|---:|---:|---:|---:|
| SrWO4 | low, 011 | 17.466 / 17.456 | 0.094 / 0.092 | 0.081 / 0.086 | 0.175 / 0.178 |
| SrWO4 | middle, 024 | 44.817 / 44.817 | 0.099 / 0.095 | 0.134 / 0.135 | 0.233 / 0.230 |
| SrWO4 | high, 424 | 86.707 / 86.696 | 0.105 / 0.092 | 0.114 / 0.093 | 0.219 / 0.185 |
| WO3 | low, 200 | 23.834 / 23.834 | 0.098 / 0.104 | 0.099 / 0.100 | 0.197 / 0.204 |
| WO3 | middle, 222 | 41.307 / 41.329 | 0.070 / 0.115 | 0.130 / 0.141 | 0.200 / 0.256 |
| WO3 | high, 340 family | 61.704 / 61.725 | 0.117 / 0.117 | 0.105 / 0.127 | 0.222 / 0.244 |
| SrCO3 | low, 111 | 24.649 / 24.627 | 0.110 / 0.087 | 0.077 / 0.099 | 0.187 / 0.186 |
| SrCO3 | middle, 122 | 43.644 / 43.633 | 0.116 / 0.096 | 0.125 / 0.131 | 0.241 / 0.227 |
| SrCO3 | high, 124 | 58.509 / 58.476 | 0.091 / 0.088 | 0.060 / 0.180 | 0.151 / 0.268 |

The strong low- and middle-angle peaks and the SrWO4 high-angle peak provide reliable position and width evidence. The high-angle SrCO3 line is only about 70 calculated counts above background and is noise-limited; its observed half-widths are reported as required but cannot be determined reliably. It was not used to justify a separate SrCO3 broadening term. The WO3 222 family also retains a moderate width mismatch, but broader inventory, size/strain, anisotropy, and polymorph challenges did not produce a more physical replay-stable model.

## Remaining uncertainty

All three phase identities are reliable, and the major-phase fractions are stable across the physically acceptable challenges. The quoted ESDs are counting-statistical only; background, preferred orientation, absorption, and structural-model choices make the practical fraction uncertainty larger, so sub-0.5 wt% differences should not be interpreted as precise. A trace Sr3W2O9 fraction cannot be established reliably and is excluded from the normalized result.

The powder data constrain cells, phase scales, texture, and the restrained SrWO4 oxygen coordinate. They do not independently determine the detailed WO3 or SrCO3 atomic coordinates or displacement parameters; those values remain inherited from the cited structural records. The SrWO4 oxygen position is chemically plausible but restraint-sensitive. The remaining goodness-of-fit above one and localized residuals at the strongest peaks are consistent with these profile/texture limitations rather than a resolvable additional crystalline phase.
