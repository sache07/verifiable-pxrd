# Powder XRD phase analysis

## Result

| Crystalline phase | Refined symmetry and cell | Weight fraction |
|---|---|---:|
| Ordered inverse-wolframite ZnWO4 | P2/c; a = 4.70188, b = 5.73394, c = 4.93290 Å, beta = 90.6377° | 83.11% |
| Monoclinic WO3 | P21/c; a = 7.70475, b = 7.52198, c = 10.53647 Å, beta = 136.0735° | 12.05% |
| Wurtzite ZnO | P63mc; a = 3.25543, c = 5.18339 Å | 4.83% |

The fractions are normalized over the three modeled crystalline phases. The final refinement has Rwp = 2.9287%, goodness of fit = 1.1084, and maximum shift/esd = 0.0119. A fresh atomic-model replay over the complete measured grid gives Rwp = 2.9282% and no profile-review flags.

## Evidence and model selection

ZnWO4 is the dominant reaction product expected from the WO3 + ZnO firing context, but a conventional wolframite cation assignment did not reproduce the decisive intensity pair near 41.6° 2theta. Exchanging Zn and W between the two ordered octahedral sites in the same P2/c topology reduced Rwp from about 10.15% to 5.71% before coordinate adaptation. Five independently adapted inverse-topology starts based on CoMoO4, FeNbO4, MnReO4, InNbO4, and InTaO4 analogues converged to the same ordering; the equally developed FeNbO4-derived basin was retained. The bounded final polish lowered Rwp from 3.1163% to 2.9287%. The final model has minimum W-O and Zn-O distances of 1.810 and 1.993 Å, respectively, with no short-contact flags.

The secondary phases match exact-composition references: monoclinic WO3 (COD 2311041) and wurtzite ZnO (COD 9004178). Both retain positive, stable contributions across complete reflection families and across the competing coordinate branches: WO3 remains near 12 wt% and ZnO near 4.8 wt%. Their presence is also chemically consistent with residual precursor after a single 700 °C firing.

No fourth crystalline phase is justified by the final residual. Trial W3O8 models contributed at most about 0.1 wt% and became bound-limited or worsened the fit. A P21/m WO3 trial reached only about 0.3 wt% in a scale-only check and then failed numerically; W10O29 also failed numerically. Those numerical failures are unknown outcomes rather than structural rejections, but no stable positive reflection family remains to support adding any of them.

## Remaining uncertainty

The P2/c ZnWO4 topology and Zn/W site ordering are strongly intensity-constrained, while its exact oxygen coordinates are less secure because they were obtained by analogue adaptation and bounded powder refinement. Preferred orientation is material in all three phases; the ZnO texture axis is only weakly distinguished from an alternative axis. The displayed hundredths of a percent preserve numerical normalization and should not be taken as analytical precision; texture/model systematics are larger than that despite the small least-squares residual.

These are relative crystalline fractions. With no internal standard, amorphous material cannot be quantified, and a trace crystalline component below reliable family-level detection cannot be excluded. The submitted `final.gpx`, CIFs, fractions, and `fit.csv` all correspond to the selected bounded-polish branch; `fit.csv` uses observed minus calculated for the difference column.
