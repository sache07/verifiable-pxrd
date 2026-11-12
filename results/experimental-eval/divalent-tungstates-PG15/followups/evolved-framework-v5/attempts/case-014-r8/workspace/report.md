# Powder XRD phase analysis

The Cu Kα Bragg–Brentano pattern is modeled by three crystalline phases. Weight fractions are normalized only over those modeled crystalline phases; no amorphous fraction was measured.

| Phase | Structural model | Crystalline weight fraction |
|---|---|---:|
| SrWO₄ | scheelite, I4₁/a | 72.79(33)% |
| WO₃ | monoclinic, P2₁/c | 11.78(31)% |
| Sr₃W₂O₉ | monoclinic, C2/c | 15.43(22)% |

The final full-grid fit has Rwp = 13.167%, Rp = 9.141%, Rexp = 3.531%, and goodness of fit = 3.729 for 8,282 observations. Parenthesized fraction uncertainties are GSAS-II least-squares standard uncertainties, not estimates of model-selection uncertainty.

## Evidence

Scheelite SrWO₄ accounts for the dominant, coherent family including the reflections near 18.33, 27.99, 33.39, 45.47, and 56.08° 2θ. Ambient monoclinic WO₃ accounts for the characteristic cluster near 23.47–24.73° and its higher-angle family. These two identifications are robust and chemically ordinary for fired SrCO₃/WO₃ material.

After those phases were fitted, a coherent residual family remained, notably near 29.75, 32.60, and 44.65° plus supporting higher-angle lines. A residual-indexed C2/c Sr₃W₂O₉ model gave a stable positive scale and reduced the screening Rwp from about 17.79% for SrWO₄ + WO₃ to 15.38% before the final specimen/profile refinements. The closest tested Sr₃WO₆ analogue remained at about 16.43%; SrCO₃ refined to effectively zero, while SrO was only about 1% and lacked broad-family support. Search was stopped once the three accepted phases indexed all coherent reflection families.

The submitted coordinates retain physical reference topologies. Bounded coordinate trials for Sr₃W₂O₉ drove all tested coordinates to their limits and were rolled back. The exported structures have shortest W–O distances of 1.884 Å (SrWO₄), 1.716 Å (WO₃), and 1.772 Å (Sr₃W₂O₉), with no anomalously short O–O contacts. A common WO₃ Uiso refined stably to 0.0102(31) Å². Phase scales, background, cells/calibration, surface roughness, and supported isotropic size terms were refined in staged checkpoints; unsupported polarization and coordinate complexity were not retained.

## Remaining uncertainty

The SrWO₄ and WO₃ phase identities are reliable. The C2/c Sr₃W₂O₉ assignment is less secure: its reference topology (COD 2311977) was reported from high-pressure material, and its cell had to be adapted to the residual-indexed family. Its preferred-orientation screening also reached a bound. This single powder pattern therefore does not determine that minor phase topology uniquely. The reported 15.43% fraction is conditional on the C2/c assignment, and its realistic uncertainty is larger than the formal 0.22% least-squares value.

Some intensity/profile mismatch remains, reflected by the goodness of fit above and a 97% correlation between the two surface-roughness parameters. This does not reveal another coherent reflection family, but it further limits interpretation of the formal fraction uncertainties. `final.gpx` replays the complete 8,282-point fit; the submitted CIFs and `fit.csv` were exported directly from that project.
