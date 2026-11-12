# Quantitative phase analysis

## Result

The pattern is modeled by three crystalline phases. Fractions are normalized over those modeled crystalline phases; they do not measure amorphous material.

| Phase | Space group | Weight fraction | Final CIF |
|---|---:|---:|---|
| MnWO4, wolframite | P 2/c | 72.04(50)% | `phase_mnwo4.cif` |
| WO3, monoclinic | P 21/c | 19.18(21)% | `phase_wo3.cif` |
| Mn3O4, hausmannite | I 41/a m d | 8.78(57)% | `phase_mn3o4.cif` |

Parenthesized uncertainties are GSAS-II covariance e.s.d.s in weight-percent units. The full-range fit gives Rwp = 7.447%, Rp = 4.947%, Rexp = 2.490%, goodness of fit = 3.000, and chi-squared = 74235.55 for 8301 observations and 51 variables. The final serialized project replayed with no frozen parameters and a maximum shift/e.s.d. of 0.00050.

## Evidence and model selection

The chemical context is WO3 + Mn3O4 heated at 700 °C. No precursor amounts or ratio were reported, so no mass-balance ratio was varied or imposed. The dominant phase is a wolframite MnWO4 model in P 2/c. It was constructed by the charge-preserving Mn2+ for Mg2+ substitution in a physical MgWO4 wolframite parent, then indexed and refined; Fe/Zn wolframite analogues and a structurally distinct scheelite model were also challenged. Wolframite gave the coherent low-, middle-, and high-angle family match. Its cell and eight independent atomic coordinates were refined.

Monoclinic WO3 uses physical record COD 2311041. Distinct P 21/c, P -1, Pnma, and tetragonal WO3 records were compared as competitors, not coexisting phases. The retained P 21/c record remained best after equal profile elaboration and nuisance cross-seeding. The final low-index texture screen selected [001]; opposite texture/size starts returned the same minimum. A symmetry-compatible crystallite-size split along monoclinic b and finite isotropic strain are supported. Atomic coordinates for this minor phase remain source-based while its cell, scale, texture, and widths were refined.

Tetragonal Mn3O4 uses COD 1011262. Its noncoincident families include 31.76° (103), 58.04° (321), 59.29° (224), and 64.17° (400). Removing the phase raises chi-squared by 3773 and Rwp to 7.634%. The orthorhombic Mn3O4 competitor collapses to zero scale. Isotropic strain and [110] March-Dollase texture are replay-stable; size-only and size-plus-strain trials hit the size boundary and were rejected. Its source coordinates were not refined.

The final profile uses the reported Cu K-alpha doublet and intensity ratio, Poisson weights `1/counts` because pointwise uncertainties were not supplied, a smooth order-18 Chebyshev background, one zero correction, nonnegative common W/X width terms with U fixed at its zero boundary, refined polarization, and one roughness-B term. Higher background orders lowered the numerical residual by following strong-reflection residual families and destabilized the weak-phase width/fraction, so they were rejected as background/scale surrogates. Unsupported SH/L, extra roughness-A, main-phase size/strain, and Mn3O4 size terms were pruned.

The final CIF health screen passed all three exports. Re-challenged watch-list phases Mn3WO6 and orthorhombic Mn3O4 collapsed to zero scale. Cubic Mn2O3 refined to only about 0.18 wt%. Orthorhombic Mn2O3 gave a small scale-only signal, but size trials hit 0.01 micrometres and widened strain trials ran to 100000 microstrain while inflating the apparent fraction; it therefore failed the replay-stable weak-phase/two-family gate and was excluded.

## Remaining uncertainty

The formal fraction e.s.d.s do not include source-model, texture, background, or instrument-calibration uncertainty. The goodness of fit above one and strong residuals at a few major peaks show remaining systematic mismatch. In particular, Mn3O4 is broad and its fraction is coupled to strain and texture, so 8.78% should not be interpreted more precisely than the quoted uncertainty. The close WO3 P 21/c versus P -1 competition limits polymorph certainty even though P 21/c consistently ranked better.

No calibrated instrument profile or internal standard was supplied. The refined zero correction is consequently correlated with cell dimensions, and the very small lattice-parameter covariance e.s.d.s understate systematic cell uncertainty. No amorphous fraction can be obtained from this refinement, and the reported fractions apply only to the three retained crystalline phases.
