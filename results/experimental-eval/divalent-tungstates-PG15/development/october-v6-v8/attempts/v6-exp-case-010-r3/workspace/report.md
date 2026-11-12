# PXRD phase analysis

The crystalline model contains three phases (fractions normalized over the modeled crystalline material):

| Phase | Space group | Weight fraction |
|---|---:|---:|
| WO3 | P 21/c | 0.7102(43) |
| alpha-Mn2O3 | Pbca | 0.2786(43) |
| MnWO4 | P 2/c | 0.01116(81) |

The final Rietveld fit has Rwp = 6.7153%, Rp = 4.9074%, and goodness-of-fit = 2.532. The Cu K-alpha doublet and reflection geometry from the metadata were used. Because pointwise uncertainties were not supplied, counting-statistical uncertainties of sqrt(counts) were assumed.

## Evidence

Monoclinic WO3 explains the dominant 23.4–24.7 degree peak group and the repeated WO3 reflection families over the full range. Orthorhombic alpha-Mn2O3 explains the remaining bixbyite-family peaks. A mature, matched Ia-3 alternative reconverged at Rwp = 6.766%, versus 6.737% for coordinate-refined Pbca before the final MnWO4 texture update; Pbca also remained preferred after a parameter-count penalty (Delta BIC about 240). Removing Mn2O3 from the final model raises Rwp to 10.46%.

MnWO4 is minor but supported by a positive scale, multiple reflections (including the residual pair near 30.1–30.4 degrees), and full-pattern behavior: removing it raises Rwp from 6.715% to 6.796%. A [001] March-Dollase term is supported for MnWO4 and improves all four tested angular regions. Mn3O4 and Mn3WO6 additions refined to zero or insignificant amounts. Alternative WO3 cells/settings and malformed candidates were rejected by full-pattern or CIF-geometry tests.

All submitted CIFs pass the supplied occupancy, symmetry, duplicate-site, and contact audit. The final project is converged with no dropped variables; regenerated and saved profiles agree exactly in the project audit.

## Remaining uncertainty

The parenthesized errors are covariance-derived one-sigma values and do not include model systematics. WO3 displacement parameters were fixed at 0.005 A^2 because free ADPs correlated with the intensity envelope; plausible ADP choices shift the major-phase fractions by roughly 1 absolute wt%. The 1.1 wt% MnWO4 amount is less robust than its phase identification because texture and weak-peak overlap matter; accepted/rejected nuisance branches span approximately 0.9–1.4 wt%. Pbca is favored over Ia-3, but some refined Mn2O3 coordinate pairs remain moderately correlated, so individual atomic coordinates should not be interpreted at single-crystal precision.

The fractions describe crystalline phases only. Without an internal standard, an amorphous or non-diffracting fraction cannot be determined reliably. No additional crystalline phase had reproducible multi-peak support.
