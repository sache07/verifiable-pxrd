# PXRD phase analysis

The pattern is explained by three crystalline phases. Weight fractions are normalized over these modeled crystalline phases.

| Phase | Structural model | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| Triclinic WO3 | P -1, COD 2106293 | a=7.30362, b=7.53593, c=7.69096; α=89.9616, β=90.7146, γ=89.9970 | 59.40(20)% |
| Scheelite CaWO4 | I 41/a, COD 7219229 | a=5.24153, c=11.37707 | 12.48(11)% |
| Calcite CaCO3 | R -3 c, COD 1547347 | a=4.98733, c=17.06065 | 28.13(25)% |

## Evidence and model selection

The assignments are chemically consistent with the stated CaCO3/WO3 precursors and 500 °C treatment. Each phase explains several distinct reflections: the split WO3 group near 23.4–24.7°, CaWO4 peaks at about 18.91, 29.01, 31.71 and 34.46°, and calcite peaks near 29.69, 39.70, 43.45 and 48.78° 2θ. With the mature nuisance model fixed, leaving out WO3, CaWO4 or calcite raises Rwp from 7.47% to 47.99%, 14.56% or 14.42%, respectively.

Atomistic alternatives were compared over the complete pattern. A superficially competitive WO3 entry (COD 1528915) was rejected after its CIF audit exposed impossible 1.575 Å O–O contacts. The closest valid alternative WO3 model (COD 2107312) reached Rwp 17.09% and a broadening boundary in the mature model. A high-pressure CaCO3 alternative (COD 2106394) reached Rwp 8.50% with a singular refinement, and the alternative CaWO4 candidate collapsed to zero scale. The three submitted CIFs have full occupancy, sensible contacts and no CIF-audit flags.

The final GSAS-II fit used the supplied Cu Kα1/Kα2 wavelengths and 0.5 intensity ratio over 10–100° 2θ, a Chebyshev background, refined phase scales and cells, specimen displacement, minimal W/X profile terms and a one-parameter roughness correction. Supported phase terms were WO3 size plus strain, CaWO4 size, weak WO3 [010] texture and calcite [104] texture. Because no calibrated instrumental profile was supplied, the size/strain values are effective broadening parameters and should not be interpreted as accurate microstructural measurements.

The required angular comparison retained displacement-only correction. Zero-only was worse (Rwp 7.550%); the joint zero/displacement branch was rejected at 99.97% correlation. The final refinement converged without dropped variables (maximum shift/esd 0.039), with Rwp=7.467%, Rp=5.509% and goodness of fit=3.126. Regional Rwp values are 6.41%, 9.20%, 7.74% and 6.85% for 10–30°, 30–50°, 50–70° and 70–100°, respectively. The largest residuals coincide with modeled strong reflections (especially CaWO4 020, calcite 104 and WO3 lines), supporting intensity/profile mismatch rather than another coherent crystalline phase.

## Remaining uncertainty

The parent atomic coordinates and displacement parameters were retained: coordinate refinements either gave no material benefit or became unstable/chemically implausible. Thus the phase identities and cells are well supported, but the powder data do not independently determine precise atomic coordinates. Parenthesized fraction uncertainties are covariance-derived one-sigma values and do not include model/profile systematics; the 30–50° intensity residuals show that those formal errors are optimistic. No internal standard was supplied, so amorphous content cannot be quantified and the reported fractions are conditional on the three crystalline phases. The regenerated final project passes the GPX convergence, profile-replay and positive-width audits.

In `fit.csv`, `difference` is observed minus calculated intensity.
