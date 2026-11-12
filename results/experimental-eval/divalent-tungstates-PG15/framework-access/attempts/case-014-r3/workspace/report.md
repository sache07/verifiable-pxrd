# Powder XRD phase analysis

The pattern is best represented by three crystalline components. Fractions are normalized over those modeled crystalline phases:

| Phase | Structural assignment | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| 1 | Scheelite SrWO₄, *I*4₁/*a* | *a* = 5.41969, *c* = 11.96369 | 0.7257 (72.6 wt%) |
| 2 | Monoclinic WO₃, *P*2₁/*n* | *a* = 7.30395, *b* = 7.54571, *c* = 7.69565, β = 90.8389 | 0.1266 (12.7 wt%) |
| 3 | Contracted scheelite-type SrWO₄ analogue, *I*4₁/*a* | *a* = 5.12984, *c* = 11.10266 | 0.1477 (14.8 wt%) |

The dominant sharp reflection set indexes uniquely as scheelite SrWO₄ and is chemically consistent with reaction of the reported SrCO₃ and WO₃ precursors at 900 °C. A second set of lines is matched by monoclinic WO₃, consistent with residual precursor. After fitting both, the remaining broad, repeated reflection set is tetragonal and is matched substantially better by a compact scheelite ABO₄ framework than by tested Sr oxides/carbonates, WO₃ polymorphs, wolframite/fergusonite tungstates, or Sr-rich tungstates. Its submitted model was therefore constructed from the tetragonal CdWO₄ scheelite framework by Cd→Sr substitution and refined as SrWO₄.

The whole-pattern fit gives Rwp = 11.725%, Rp = 8.089%, χ² = 91103.4, and saved-refinement GOF = 3.323. The independently regenerated full-grid profile in `fit.csv` comes directly from `final.gpx`; the saved fit interval was 10.05–99.90° 2θ.

The third phase is tentative. Its strong broadening and intensity mismatch drive microstrain and March–Dollase texture to their allowed limits, so neither its exact composition/atomic structure nor its 14.8 wt% fraction is reliable at the formal scale-factor uncertainty (0.17 wt%). A realistic uncertainty is several weight percent and propagates into the other two fractions. Weak structured residuals remain, but no tested fourth phase gave a stable, chemically defensible refinement; any additional minor crystalline component is therefore unresolved rather than quantified. The 40-term smooth background and profile correlations also mean the reported formal standard uncertainties understate model uncertainty.
