# Phase analysis and Rietveld refinement

## Result

The crystalline pattern is modeled by four phases. Weight fractions are normalized over these modeled crystalline phases only; no amorphous fraction can be obtained without an internal standard.

| Phase | Space group | Reference model | Refined weight fraction | Refined cell (Å, °) |
|---|---:|---:|---:|---|
| BaWO4 (scheelite) | I 41/a | COD 1527204 | 0.61819 (formal s.u. 0.00212) | a = 5.630413(71), c = 12.693978(106) |
| Ba3W2O9 | R -3 c | COD 1533878 | 0.16540 (0.00136) | a = 10.134994(477), c = 13.956527(598) |
| WO3, monoclinic | P 21/n | COD 1528915 | 0.13336 (0.00192) | a = 7.295384(503), b = 7.540841(593), c = 7.688955(625), beta = 90.8944(105) |
| BaCO3 (witherite) | P m c n | COD 9010928 | 0.08305 (0.00258) | a = 5.30726(147), b = 8.91867(283), c = 6.43765(205) |

The full-range, reopened-project fit has Rwp = 4.1678%, Rp = 3.0103%, goodness-of-fit = 1.3846, and chi-squared = 15841.64 for 8301 observations and 38 refined parameters. The last maximum shift/s.u. was 0.0016.

## Phase and chemistry evidence

The metadata identifies a reflection-geometry Cu K-alpha measurement of WO3 + BaCO3 heated at 750 °C. Both K-alpha wavelengths and the reported 0.5 K-alpha2/K-alpha1 ratio were used. Distinct peak families establish each retained phase: BaWO4 accounts for the dominant 26.7, 32.1, 43.2, 49.0 and 53.7° families; Ba3W2O9 accounts for independent lines near 17.8, 30.8, 37.7 and 40.8°; monoclinic WO3 accounts for the 23.40/23.86/24.66°, 28.90/29.21° and 33.54/33.86° splittings; and BaCO3 contributes independent intensity near 24.18, 45.15 and 87.04°.

Inventory tests used the same neutral profile and nuisance model. BaWO4 alone gave Rwp 10.032%; BaWO4 + Ba3W2O9 gave 7.803%; BaWO4 + WO3 gave 8.981%; and the three together gave 6.174%. Under that same model, monoclinic P 21/n WO3 was better than triclinic WO3 (6.495%) and orthorhombic WO3 (6.642%). Adding BaCO3 lowered Rwp to 5.778% and removed its independent residual family. Thus the alternate WO3 records were rejected by the pattern, not by chemistry.

All retained formulas are charge balanced with Ba2+, W6+, O2- and CO3(2-). The refined fractions correspond to Ba/W = 1.0097, close to the 1:1 precursor inventory despite allowing the non-1:1 Ba3W2O9 product. Charge-balanced alternatives considered after the initial residual audit included Ba2WO5, BaW2O7 and Ba2W3O11. Exact-record and stoichiometric-analogue searches did not yield a physically matching residual family for these; their nearest substituted parents also failed the pattern screen. They remain chemically possible trace-phase watch-list items, but no fifth crystalline fraction can be assigned reliably. Re-challenging the watch list after nuisance, texture and broadening changes found no coherent unmodeled peak family.

## Refinement choices and controls

Raw counts were weighted with Poisson estimates because pointwise uncertainties were not supplied. The initial common profile was deliberately low-dimensional and nonnegative: U = V = Y = Z = 0, with W and X refined. The final values are W = 18.8319 and X = 2.90742; SH/L remained fixed because repeated low-angle asymmetry was not supported. Unused phase broadening was neutralized before testing (10 µm size and zero strain). Only one angular correction was used, a refined zero offset of 0.279816°; a sample-displacement alternative was worse (Rwp 5.787% versus 5.778%) and was disabled.

A smooth 13-term Chebyshev background and one Suortti roughness parameter, B = 0.12270 with A = 0, were retained. Refining polarization together with roughness returned polarization to approximately its fixed 0.5 value and did not materially improve the fit, so it was pruned. BaWO4 texture challenges from the same no-texture project gave Rwp 4.563%, 4.622% and 4.366% for [001], [100] and [112], respectively; the replay-stable [112] March-Dollase term (1.36428) was retained.

Size and strain were compared one phase at a time from the same saved baseline. BaWO4 size and strain ran to their neutral limits and were rejected. For Ba3W2O9, WO3 and BaCO3, isotropic strain was better than size (Rwp 4.691 versus 4.703; 4.661 versus 4.668; and 4.684 versus an unstable 4.796, respectively). Their combination was replay-stable and complementary. Compatible uniaxial tests were then made along distinct axes. BaCO3 anisotropy changed Rwp by less than 0.0002 percentage point and was rejected. Natural [001] splits for Ba3W2O9 and WO3 were replay-stable and jointly lowered chi-squared by about 61 for two added parameters; final equatorial/axial microstrains are 1550/709 and 2307/3394, respectively. BaCO3 retains 6394 isotropic microstrain.

## Measured profile audit

The table records observed and calculated peak position, FWHM, and left/right half-width in degrees. Metrics use the background-subtracted profile with only a 1.2-point Gaussian filter (about 0.013°) to suppress counting noise; the refinement and `fit.csv` are unsmoothed. Peaks were selected to be phase-specific where possible.

| Phase, reflection | Range | Observed: position; FWHM; L/R | Calculated: position; FWHM; L/R |
|---|---|---|---|
| BaWO4 004 | low | 28.38718; 0.15390; 0.06634/0.08757 | 28.38718; 0.15367; 0.06655/0.08712 |
| BaWO4 116 | middle | 48.97901; 0.20687; 0.05893/0.14794 | 48.97901; 0.20700; 0.05995/0.14705 |
| BaWO4 424 | high | 82.61052; 0.13563; 0.06804/0.06759 | 82.61052; 0.12918; 0.06511/0.06408 |
| Ba3W2O9 300 | low | 30.82125; 0.17323; 0.07180/0.10143 | 30.82125; 0.17242; 0.07259/0.09983 |
| Ba3W2O9 223 | middle | 40.79661; 0.20406; 0.07754/0.12652 | 40.79661; 0.19768; 0.07452/0.12316 |
| Ba3W2O9 229 | high | 71.51592; 0.11463; 0.05928/0.05535 | 71.51592; 0.12367; 0.05985/0.06382 |
| WO3 002 | low | 23.39950; 0.17668; 0.06754/0.10914 | 23.41037; 0.16761; 0.07517/0.09244 |
| WO3 140/400/223 group | middle | 50.23951; 0.28695; 0.09249/0.19446 | 50.25038; 0.27354; 0.10279/0.17074 |
| WO3 440 family | high | 72.21137; 0.22294; 0.05655/0.16639 | 72.26570; 0.25280; 0.13643/0.11636 |
| BaCO3 111 | low | 24.18188; 0.17720; 0.07940/0.09780 | 24.19275; 0.16384; 0.08002/0.08382 |
| BaCO3 132 | middle | 45.19750; 0.19197; 0.13963/0.05234 | 45.15403; 0.29053; 0.14808/0.14245 |
| BaCO3 225 | high | 87.03314; 0.16577; 0.06966/0.09612 | 87.04401; 0.13536; 0.06857/0.06679 |

The isolated high-angle WO3 family is only about 61 counts above its local baseline, so its observed position and half-widths are not reliable at the precision shown. The middle BaCO3 line is also weak and partly affected by neighboring intensity. These limitations motivated restrained broadening rather than more general anisotropy.

## Remaining uncertainty

Phase presence and structure type are well supported, but the atomic coordinates and occupancies were not independently refined: the mixture does not contain enough isolated intensity for stable coordinate refinement. The CIF coordinates therefore come from the cited reference structures while their cells, scales and supported profile terms come from the final refinement.

The covariance s.u. values above describe only the selected model. Texture, roughness and minority-phase broadening correlate with integrated intensity; comparison with plausible but less complete models moves the major/minor fractions by roughly 1–4 absolute wt%. A realistic uncertainty is therefore several wt% for BaWO4 and about 1–2 wt% for WO3 and BaCO3, larger than the formal s.u. values. The goodness-of-fit remains above the counting-statistical expectation, with the largest residuals concentrated at modeled peak intensity/shape features (not a consistent new phase family), especially near 28.39, 32.07, 45.81, 53.71 and 54.63°.

`final.gpx` was saved, reopened and replayed over the full 9.903433–100.094553° range. No refined term is frozen at a bound. The four CIFs, normalized fractions, and all 8301 rows of `fit.csv` were exported from that reopened project; `result.json` was parsed and its paths and unit-sum fractions were verified.
