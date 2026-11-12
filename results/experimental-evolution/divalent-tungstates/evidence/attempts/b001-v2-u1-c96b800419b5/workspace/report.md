# PXRD phase analysis and refinement

## Result

Three crystalline phases are required. Weight fractions are normalized over these modeled crystalline phases.

| Phase | Structural model | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| SrWO₄ | scheelite, *I*4₁/*a* (No. 88) | *a* = 5.39312, *c* = 11.89974 | 60.07(24) wt% |
| SrCO₃ | orthorhombic *Pnma* (No. 62) | *a* = 6.02662, *b* = 5.09640, *c* = 8.39400 | 15.42(25) wt% |
| WO₃ | triclinic *P*−1 (No. 2) | *a* = 7.28910, *b* = 7.55309, *c* = 7.69136; α = 89.8167°, β = 90.8701°, γ = 89.9420° | 24.51(19) wt% |

The final full-range native Rietveld replay gives Rwp = 6.569%, Rp = 4.324%, Rexp = 2.861%, and GOF = 2.299 (8301 observations, 25 variables). Parenthesized fraction uncertainties are GSAS-II formal one-standard-deviation values, not estimates of total systematic uncertainty.

## Evidence and model selection

The strongest families at approximately 17.46, 27.20, 29.44, 44.82, 47.13, 55.53, 56.82, 72.65, and 86.71° 2θ identify scheelite SrWO₄. The 22.95/23.83/24.65° triplet and associated 28.34 and 33.60° lines require WO₃, while lines near 25.29, 25.97, 36.07, 37.50, 43.67, and 49.46° require SrCO₃. Starting with SrWO₄ alone gave Rwp about 12.41%; adding SrCO₃ reduced it to about 11.97%, and adding WO₃ reduced it to about 7.26% before the accepted profile refinements. Remaining large residuals are concentrated around already assigned strong reflections rather than forming a convincing fourth-phase family.

No exact SrWO₄ entry was present in the supplied candidate inventory, so cross-chemistry scheelite analogues were screened. The submitted ordered model retains the fractional coordinates of CaWO₄ COD 7219229 with the chemically justified Ca→Sr substitution; its starting lattice was set to the Sr-sized isostructural SrMoO₄ COD 2300460 lattice before cell refinement. This gave physically reasonable W–O = 1.822 Å and Sr–O = 2.549–2.565 Å in the final structure. Under the same modest nuisance model it fitted materially better than the SrMoO₄-coordinate alternative (Rwp 7.26% versus 7.54% before final profile work).

The selected SrCO₃ parent is the ordered *Pnma* COD 9008198 model. Its carbonate C–O distances remain 1.291–1.304 Å and Sr–O distances 2.568–2.732 Å. A disordered *R*−3*m* alternative fitted worse (Rwp 8.31% under the comparison model) and refined to only a small compensating scale.

For WO₃, the ordered triclinic COD 2106293 model was preferred over room-temperature monoclinic and orthorhombic records under identical profile assumptions. Against the closest monoclinic alternative, *P*−1 gave Rwp 7.537% and χ² 57501 versus 7.622% and χ² 58812, despite only two additional cell variables. Other records with invalid atom typing, partial/disordered sites, or impossible contacts were rejected before interpretation. A reported Sr₃W₂O₉ record was also rejected before fitting because its stated high-pressure synthesis is incompatible with the reported 650 °C ambient-pressure preparation. The final phase fractions give a crystalline Sr:W molar ratio of 0.996, independently consistent with the SrCO₃ + WO₃ precursor inventory.

## Profile and replay checks

The reported Cu Kα₁/Kα₂ wavelengths and 0.5 intensity ratio were fixed. Because pointwise uncertainties were absent, counting-statistics weights were used. Peak offsets decrease with angle, so specimen displacement was refined (1059 µm) while zero was fixed; the two correlated corrections were not co-refined. The common sharp-phase baseline used U = V = 0 and fixed W = 42, with only nonnegative common X refined (3.750). Separate size/strain challenges were started from neutral values. Only isotropic WO₃ microstrain was reproducible and stable (about 4195 µstrain); size terms and SrWO₄/SrCO₃ broadening either hit bounds, became nonphysical, or were unsupported and were pruned. No texture, anisotropic broadening, or refined asymmetry term was retained. The largest final parameter correlation is 0.630, while common X and WO₃ strain correlate only −0.262.

A trial refinement of the three scheelite oxygen coordinates lowered Rwp to 6.33% but produced W–O = 2.016 Å and Sr–O = 2.43–2.47 Å. It was therefore rejected as profile/intensity compensation, and all submitted atomic coordinates are fixed, physically screened parent coordinates. After the profile choices were accepted, the project was extended to the complete 9.9034–100.0946° range, saved, reopened, and freshly refined in native atomic Rietveld mode. A second reopen reproduced Rwp = 6.5692%; the exported CIFs, fractions, and `fit.csv` all come from that replay-checked `final.gpx`.

## Remaining uncertainty

The three phase identities and their relative crystalline fractions are well supported, but the formal fraction errors understate model uncertainty because no calibrated instrument profile or pointwise standard uncertainties were supplied. Scale and WO₃ strain retain a moderate correlation (0.545). The reported fractions do not quantify amorphous material or any phase below the pattern's detection/identification limit, so absolute bulk fractions cannot be claimed reliably.

The SrWO₄ phase and lattice are reliable, but its exact oxygen coordinates cannot be determined reliably from this pattern and are inherited from the screened scheelite analogue. The triclinic WO₃ model is statistically preferred, but a closely related monoclinic/domain description cannot be excluded completely because WO₃ peaks are broadened and extensively overlapped. Weak structured residuals remain, but they do not support a reliable identity or fraction for an additional crystalline phase.
