# Powder XRD phase analysis

The modeled crystalline product contains four phases (fractions normalized over the modeled crystalline material):

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| MnWO₄ (wolframite) | P2/c | a = 4.79429, b = 5.70966, c = 4.97654, β = 91.1209 | 70.35% |
| WO₃ (monoclinic) | P2₁/c | a = 7.69178, b = 7.54061, c = 10.52353, β = 136.0822 | 16.60% |
| Mn₂WO₆ (orthorhombic) | P2₁2₁2₁ | a = 5.04651, b = 8.64589, c = 9.39388 | 12.49% |
| MnO (rocksalt) | Fm-3m | a = 4.39365 | 0.56% |

MnWO₄ and WO₃ account for the dominant reflection sets and are chemically consistent with the Mn₃O₄ + WO₃ reaction fired at 800 °C. Their published structural references were refined with bounded cell, heavy-atom, profile, and scale parameters. The WO₃ oxygen coordinates were not independently determined: a bounded trial drove nearly every O coordinate to its limit for a negligible improvement, so the physically clean reference O substructure was retained.

A coherent residual family at approximately 20.32, 20.88, 29.14, 35.3–35.6, 46.20–47.01, and 57.00° 2θ required a third tungstate. It indexes consistently as orthorhombic Mn₂WO₆. No suitable same-chemistry atomic model was available, so P2₁2₁2₁ Y₂WO₆ and several related tungstate/tellurate frameworks were tested by element substitution. The Y₂WO₆ topology gave the best physically constrained result. Multiple coordinate starts converged to the submitted Mn₂WO₆ model, with W–O distances of 1.68–2.12 Å and no impossible contacts. The topology, cell, and phase presence are supported, but the Mn/O coordinates are analogue-derived and not unique; this CIF should therefore be regarded as a provisional structural model rather than a definitive Mn₂WO₆ structure.

Weak lines near 35.6, 59.9, and 74.9° support rocksalt MnO. Its scale remained positive over physically allowed crystallite-size trials and is about 6 standard uncertainties above zero in the final scale covariance. Mn₃O₄ and Mn₂O₃ trial scales collapsed, while hexagonal MnO required unphysical broadening. Because the retained MnO peaks are weak and overlapped, 0.56(9)% is only the formal least-squares result; its systematic fraction uncertainty is likely larger.

The fresh, read-only GSAS-II replay gives Rwp = 13.037% and Rp = 7.343% over all 8301 points (GSAS-II fit-range Rwp = 13.038%, goodness of fit = 7.36). Remaining residuals are chiefly intensity/width errors at overlapping reflections of accepted phases, especially around 35.6°, rather than a separate coherent unindexed family. The reported uncertainties are conditional on this four-phase crystalline model; amorphous content was not quantified.
