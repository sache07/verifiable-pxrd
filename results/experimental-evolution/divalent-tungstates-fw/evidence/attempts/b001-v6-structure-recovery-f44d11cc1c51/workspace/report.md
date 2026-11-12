# PXRD phase analysis

## Result

The crystalline inventory is a three-phase Ca–W–O mixture. Weight fractions are normalized only over the modeled crystalline phases:

| Phase | Space group | Refined cell | Weight fraction |
|---|---|---|---:|
| CaWO4, scheelite | I 41/a | a = 5.24881 Å, c = 11.38043 Å | 72.35 wt% |
| WO3, monoclinic | P 21/c | a = 7.29521 Å, b = 7.54258 Å, c = 10.51419 Å, β = 133.0276° | 15.25 wt% |
| Ca3WO6, ordered-perovskite-related | P 21/c | a = 5.55066 Å, b = 5.80708 Å, c = 9.72425 Å, β = 124.6048° | 12.40 wt% |

No amorphous fraction can be obtained without an internal standard, so these values are not absolute bulk fractions. Formal fraction uncertainties are also not reliable from this scan alone; source/texture/model choices imply systematic uncertainty of more practical importance than the least-squares scale errors.

## Evidence and model selection

The metadata identify a CaO + WO3 synthesis at 800 °C measured in reflection geometry with the stated Cu Kα1/Kα2 doublet. The observed pattern contains three coherent line families:

- Scheelite CaWO4 accounts for the dominant family, including lines near 18.50, 28.57, 31.32, 34.03, 39.04, 46.97, and 57.72° 2θ.
- Monoclinic WO3 accounts for the 23.02/23.47/24.27°, 26.51°, 33.15/33.47°, and 41.35/41.80° groups.
- A distinct ordered-perovskite-related family near 19.36, 22.04, 30.66, 32.10, 36.53, and 37.45° requires Ca3WO6. These lines remain coherent when scales, cells, and simple widths are varied and are not explained by the other two phases.

The normalized structural parents were COD 7219229 (CaWO4) and COD 2311041 (WO3). Ca3WO6 was not available as an exact library entry, so chemically sensible cation mappings were compared. A P 21/c Ca2CoWO6 parent (COD 7222332), with both non-W cation sites mapped to Ca, gave the best physical low-flexibility fit. Its replayed matched-source Rwp was 13.118%, versus 13.205% and 13.206% for mapped P 21 NaErCoWO6 and NaYNiWO6 parents. Ca3W2O9 controls did not account for the residual family and either refined to a very small contribution or failed to converge.

Final deletion tests, with the remaining scales and background rebalanced, increased Rwp from 12.740% to 47.927% without CaWO4, 19.103% without WO3, and 16.064% without Ca3WO6. The remaining prominent residuals occur at modeled reflections rather than forming another coherent unassigned line family.

## Refinement and physical checks

The submitted GSAS-II model uses the measured Cu doublet, a positive six-term background, specimen displacement, common W/X profile terms, one isotropic size term per phase, and a moderate CaWO4 [111] March–Dollase term (1.197). Alternative zero-offset/specimen-displacement branches and low-index texture axes were compared. Asymmetry did not improve the replayed curve. A freely refined polarization term lowered Rwp but drifted from 0.815 to 0.917 on restart toward its physical bound; it was rejected as compensatory and fixed at the standard unpolarized value of 0.5.

Connected, restrained coordinate blocks were tested from parent and perturbed starts. Large apparent CaWO4 oxygen shifts disappeared when the independently supported texture term was included. WO3 and mapped-Ca3WO6 coordinate branches produced small monotonic gains but did not reach nuisance-independent stationary endpoints before displacement/contact limits. Their motion was therefore rejected, and the normalized parent coordinates were retained. Consequently, the Ca3WO6 phase assignment, cell, and approximate fraction are supported, but its exact cation/oxygen coordinates—and discrimination from a very similar ordered-perovskite polytype—cannot be determined reliably from this pattern.

All submitted CIFs pass composition and contact screening. Minimum key distances are CaWO4 W–O 1.764 Å and Ca–O 2.470 Å; WO3 W–O 1.715 Å and O–O 2.539 Å; Ca3WO6 W–O 1.971 Å, Ca–O 2.138 Å, and O–O 2.781 Å.

The final whole-pattern statistics are Rwp = 12.740%, Rp = 9.710%, Rexp = 2.613%, and goodness of fit = 4.876 (8,301 points; 26 refined parameters). The elevated goodness of fit and systematic modeled-reflection intensity residuals are the main remaining limitations.

An independent native GSAS-II replay regenerated reflection lists and the full profile from `final.gpx` without optimization. It reproduced the submitted profile to numerical precision, returned the same phase fractions, left the project unchanged, and reported no negative-background, negative-width, scale, or displacement-parameter review flags.
