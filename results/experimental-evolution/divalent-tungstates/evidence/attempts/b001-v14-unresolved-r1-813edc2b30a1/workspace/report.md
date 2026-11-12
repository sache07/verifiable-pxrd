# PXRD phase analysis

The pattern is closed with three crystalline phases. Weight fractions are normalized over those modeled crystalline phases only.

| Phase | Space group | Weight fraction | Refined cell (Å, °) |
|---|---:|---:|---|
| PbWO₄ | I4₁/a | 61.43(18)% | a = 5.472622, c = 12.073172 |
| WO₃ | P2₁/c | 21.06(14)% | a = 7.700674, b = 7.543745, c = 10.535588, β = 136.19166 |
| Pb₃O₄ | P4₂/mbc | 17.51(19)% | a = 8.810911, c = 6.571249 |

## Evidence

Scheelite PbWO₄ accounts for the dominant families near 27.8, 33.2, 45.1, 47.4, 51.6, 55.6, 56.9, and 72.4°. Monoclinic WO₃ is required by its resolved 23.53/24.01/24.83° group and additional independent families. After fitting those phases, positive residual families near 14.64, 26.79, 31.18, 32.54, 34.48, 47.94, 50.25, and 52.51° identify residual tetragonal Pb₃O₄. All three scales remain positive on independent replay.

Structurally distinct source records were challenged with matched nuisance models. The selected PbWO₄ and WO₃ records beat same-formula alternatives; lower-symmetry competitors were much poorer or numerically invalid. For Pb₃O₄, COD 9012124 gives Rwp = 5.3753%, compared with 5.3906% for a second tetragonal record that also has geometry warnings. Orthorhombic Pb₃O₄ loses at the neutral checkpoint (Rwp = 8.56% versus 6.32%) and its width-elaborated branch collapses to the size bound. The final exported CIFs all pass `learned/cif_health.py`.

No fourth crystalline phase is retained. The largest noncoincident excess is broad intensity around 30.82° (approximately 0.34° FWHM), with no second independent family; it is insufficient for a replay-stable crystalline scale or a defensible analogue construction.

## Refinement and uncertainty

The full 9.9034–100.0946° range was refined with the reported Cu Kα doublet, an 8-term Chebyshev background, phase scales and cells, one zero correction, and nonnegative common U/W/X profile terms. Supported microstructure terms were PbWO₄ size and Pb₃O₄ size plus strain. Weak compact texture corrections were retained for PbWO₄ [100] and WO₃ [010]. Roughness, free polarization, extra asymmetry, WO₃ widths, and atomic-coordinate/ADP refinement were rejected as unsupported, nonphysical, or unstable. Final statistics are Rwp = 5.3753%, Rp = 3.6185%, GOF = 2.1665, and χ² = 38830.47 for 8301 observations and 28 variables.

The quoted parentheses are GSAS-II counting-statistical standard uncertainties and understate model uncertainty. Effective polarization and a calibrated instrumental profile were not supplied, source ADPs had to remain fixed, and residuals are correlated (Durbin–Watson 0.444). Sensitivity challenges indicate that practical absolute fraction uncertainty is roughly 1–2 percentage points. Phase identities and lattice models are reliable, but the atomic coordinates are source-derived rather than independently determined from this multiphase laboratory pattern; the Pb₃O₄ size/strain decomposition is also not unique. No amorphous fraction can be quantified from this refinement.
