# Powder XRD phase analysis

The 900 °C SrCO3 + WO3 specimen is best described by three crystalline components. Fractions are normalized over these modeled crystalline phases; they do not quantify any amorphous material.

| Phase | Structural model | Weight fraction |
|---|---|---:|
| SrWO4 | scheelite, I4_1/a | 0.7552 |
| WO3 | monoclinic, P2_1/c | 0.1056 |
| Sr2WO5 | provisional analogue-derived model, P2_1/c | 0.1393 |

The dominant scheelite assignment is secure from its complete strong-peak sequence, including the observed families near 18.33, 27.99, 33.39, 45.47, 51.98, and 56.08° 2theta. Monoclinic WO3 is independently supported by the diagnostic low-angle group near 23.46, 23.97, and 24.73°. Removing WO3 from the fixed common-profile model raises Rwp from 15.84% to 17.77%.

The remaining coherent intensity near 29.75, 30.90, 32.61, 44.65, 48.6, and 53.43° requires an Sr-rich component; removing it raises Rwp to 17.04%. Sr2WO5 is also chemically consistent with partial reaction through `Sr2WO5 + WO3 -> 2 SrWO4`. No exact visible reference was available. The submitted model was therefore made from the charge-balanced Ho2SiO5 topology by Ho→Sr and Si→W substitution, followed by a physical repair of the isolated WO4 groups to 1.78 Å W–O bonds. Ba2ReO5-, Er2SiO5-, and charge-scaled K2FeF5-derived alternatives were screened under the same nuisance model and fit less well or gave inferior residual-family agreement.

This third structure is not uniquely determined. In particular, a monoclinic SrWO4 record reproduces part of the same residual even better, but its source CIF is the approximately 11 GPa high-pressure phase; accepting it would be incompatible with the ambient-pressure firing history and worsens the Sr:W balance. A physically plausible Sr3WO6 analogue was also re-challenged under the final profile: it stabilized at only 1.33 wt% and reduced Rwp by 0.03 percentage point, with its strongest evidence overlapping the provisional Sr2WO5 peaks. It was retained as a watch-list possibility rather than asserted as a fourth phase.

The final full-grid GSAS-II replay gives Rwp = 15.8386% and GOF = 4.4823 using weights `1/max(counts,1)`. The retained baseline uses one specimen-displacement correction, a smooth three-term Q^-2 background, U/W/X = 0/40/6, SH/L = 0.03, and a supported low-angle roughness term (A = 0.1485, B = 0.10). Phase-common Uiso values were fixed at 0.003, 0.003, and 0.020 Å² for SrWO4, WO3, and Sr2WO5 respectively; unconstrained thermal trials left the laboratory's physical range and were rejected. Size, strain, texture, and extra asymmetry trials were pruned after save/reopen replay. The width terms reach the allowed common-profile limits, and structured residual remains; consequently the Sr2WO5 topology and weak-phase fraction are model-dependent, and the reported fraction digits should not be interpreted as formal precision. All submitted CIFs pass the broad contact/occupancy screen, the calculated background remains positive, and fresh replay exactly reproduces `fit.csv` without profile review flags.
