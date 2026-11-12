# PXRD phase analysis

The pattern is a three-phase crystalline mixture. Weight fractions are normalized over the modeled crystalline phases; the uncertainties below are realistic absolute estimates from model sensitivity, not the much smaller least-squares standard errors.

| Phase | Structural model | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| MgWO4 | Wolframite type, P 2/c | a = 4.69600, b = 5.68287, c = 4.94671, β = 90.8254 | 50.9 ± 1.5 wt% |
| WO3 | γ-monoclinic, P 21/c | a = 7.68635, b = 7.54011, c = 10.51805, β = 136.0570 (valid transformed setting) | 42.1 ± 1.5 wt% |
| MgO | Periclase, F m -3 m | a = 4.20987 | 7.0 ± 0.5 wt% |

Evidence is direct and phase-specific. MgWO4 accounts for the strong 18.879°, 23.823°, and 30.408/30.745° peaks. Monoclinic WO3 accounts for the diagnostic 23.128/23.573/24.377° triplet and its correlated lines near 26.58°, 28.93°, 33.28°, and 34.16°. MgO is required by the 42.93°, 62.26°, 78.9°, and 94.15° rocksalt reflections. Removing MgO from an otherwise re-refined model raises Rwp from 1.65% to 2.51%; removing WO3 raises it to 17.1%. No coherent residual peak family supports an additional crystalline phase.

The final GSAS-II Rietveld fit used Cu Kα1/Kα2 wavelengths of 1.540598/1.544426 Å with the reported 0.5 intensity ratio, counting-statistical weights, a refined zero and effective polarization, phase scales and cells, phase-dependent broadening, and March–Dollase terms for pronounced MgWO4 texture and weak WO3 texture. MgWO4 coordinates and the WO3 W coordinates were refined. The final statistics over 10–100° are Rp = 1.293%, Rwp = 1.646%, Rexp = 1.527%, and GOF = 1.081.

The phase identities and approximate fractions are reliable, but the formal fraction errors in `result.json` understate systematic uncertainty. There was no calibrated instrumental profile and no supplied pointwise uncertainties; profile/size/strain separation is therefore not reliable and should not be interpreted as a crystallite-size measurement. WO3 oxygen coordinates are retained from the reference structure with fixed isotropic displacement parameters because this multiphase laboratory X-ray pattern does not determine that oxygen substructure reliably. Amorphous material, if present, is not quantified, and unidentified crystalline phases below roughly 1–2 wt% may escape detection.
