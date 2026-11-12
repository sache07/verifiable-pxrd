# Powder XRD phase analysis

The 300 °C product is dominated by the two precursor structures, with a trace wolframite reaction product. Fractions are normalized over the modeled crystalline phases only.

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| Monoclinic WO3 | P 21/c | a = 7.69385, b = 7.53731, c = 10.53955, β = 136.11045 | 73.740(180)% |
| β-MnO2 (pyrolusite) | P 42/m n m | a = 4.39927, c = 2.87402 | 25.697(175)% |
| MnWO4 (wolframite) | P 2/c | a = 4.80867, b = 5.76844, c = 4.95204, β = 90.8598 | 0.563(54)% |

Parenthetical uncertainties are covariance-based one-sigma errors and do not include model-selection systematics.

## Evidence

The distorted monoclinic WO3 model accounts for the dominant peak families over the full 10–100° range and was preferred to screened triclinic, P21/n, Pnma, and small-cell WO3 records under the same restrained profile model. The unusual β ≈ 136° cell is a valid nonconventional setting of monoclinic WO3. Pyrolusite MnO2 gives the remaining strong rutile-type families; its oxygen coordinate refined to x = 0.30222. These assignments are also chemically consistent with the stated WO3 and MnO2 precursors and the low 300 °C treatment.

After those phases were converged, coherent residual families remained near 30.38/30.71°, 41.05°, and 61.54° 2θ. A P2/c MnWO4 wolframite model accounts for these partly isolated features and lowers Rwp from about 5.858% to 5.818%. The exact-composition starting record was measured at 2.4 GPa, so ambient FeWO4, ZnWO4, and MgWO4 wolframite parents with Mn substitution were also screened. The exact MnWO4 topology gave the most stable physically plausible cell/intensity model after refinement. All submitted structures pass the geometry/occupancy screen; their shortest interatomic distances are 1.742, 1.880, and 1.792 Å for WO3, MnO2, and MnWO4, respectively.

Mn2O3 was retained on the watch list but not accepted. It can refine to about 0.9 wt% and lower Rwp to 5.788%, but almost all of that gain occurs in crowded WO3 regions around 33.2° and 55.6°, without a coherent set of unique Mn2O3 families. Mn3WO6 remains near 0.1 wt% for a negligible improvement, and Mn3O4 collapses to zero scale.

## Refinement and uncertainty

The final model uses the measured Cu Kα1/Kα2 wavelengths and 0.5 intensity ratio, a six-coefficient smooth Chebyshev background, one specimen-displacement correction, a nonnegative common W/X profile, and only replay-stable phase broadening/texture terms. Unsupported SH/L, extra profile, roughness, displacement-parameter, and weak-phase broadening refinements were fixed or pruned. The saved project converged with maximum shift/esd = 0.010 and no frozen parameters. Independent full-grid atomic replay gives Rwp = 5.81836%, Rp = 4.43637%, and GOF = 2.16481.

The MnWO4 presence is supported, but its atomic coordinates and exact fraction cannot be determined reliably from this trace signal. Its reported 0.563(54) wt% is conditional on neutral weak-phase broadening; rejected size/strain trials show that model-systematic uncertainty is larger than the formal error. No pointwise uncertainties were supplied, so counting-statistics weights were used. Amorphous material, if present, is not quantified.

`fit.csv` was regenerated from `final.gpx` by native GSAS-II atomic forward calculation on the complete measured grid, not copied from cached profile arrays.
