# Powder XRD phase analysis

## Result

| Phase | Structure | Crystalline weight fraction |
|---|---|---:|
| MnWO4 (wolframite) | P 2/c; COD 1520200 | 62.466% |
| Mn3WO6 | R -3; COD 2002703 | 18.828% |
| WO3 | P -1 triclinic; COD 2106293 | 18.705% |

The final read-only atomic replay gives Rwp = 3.1651% and Rp = 2.3180% over all 8301 measured points. The mandatory staged polish selected `heavy_light` at Rwp = 3.1651%; its output is the submitted `final.gpx`. Replay generated fresh structure factors and reflection lists, changed no parameters, and returned no profile-review flags.

## Evidence

MnWO4 accounts for the dominant wolframite reflection set. The 19.68/20.18 degree pair and its higher-angle family require rhombohedral Mn3WO6, while the 22.89/24.16 degree peaks and the 33-34 degree family require WO3. Controlled phase deletion raised Rwp from the complete rough model (10.80%) to 12.92% without Mn3WO6, 16.36% without WO3, and 17.76% for MnWO4 alone.

Several exact-composition WO3 parents were developed comparably. The accepted triclinic P -1 basin reached 3.20% before the final polish and retained physical contacts (minimum O-O about 2.56 A); the best monoclinic alternative stopped at 3.30% and inherited an implausibly short O-O contact near 1.58 A, so it was discarded. Orthorhombic and alternate monoclinic starts fit substantially worse. In the accepted model, every coherent reflection family is indexed by one of the three retained phases; the largest remaining residuals are paired peak-center/wing shape errors on accepted reflections rather than a separate indexed family.

## Uncertainty

The fractions are normalized only over modeled crystalline material; this measurement does not quantify amorphous content. Strong but bounded preferred orientation is needed for all three phases, and the Mn3WO6 texture axis has close alternatives, so systematic fraction uncertainty is larger than a covariance-only standard error. Nevertheless, the phase contributions remain positive and the fractions are stable across the accepted branches. No fourth crystalline phase can be identified reliably, and trace phases below the pattern's detection limit are not excluded.

The bounded `heavy_light` coordinate-polish branch was selected and passed the convergence, fraction-stability, and geometry audits. Fine oxygen positions remain less precisely constrained than phase identity and lattice.

Calibration/profile alternatives that reached bounds or were inseparable from correlated parameters were rolled back. The retained zero offset (-0.247578 degrees), axial-divergence term, crystallite sizes, Mn3WO6 isotropic microstrain, and March-Dollase terms are all inside the supplied laboratory ranges.
