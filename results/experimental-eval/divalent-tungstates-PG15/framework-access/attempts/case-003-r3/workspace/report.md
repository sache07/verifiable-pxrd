# Powder XRD phase analysis

## Result

The pattern is described by three crystalline phases. Weight fractions are normalized only over these modeled crystalline phases.

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| Monoclinic WO₃ | P 2₁/c | a = 7.31182, b = 7.54427, c = 10.5518, β = 133.144 | 0.5575 (55.75 wt%) |
| CaWO₄, scheelite | I 4₁/a | a = 5.24785, c = 11.3882 | 0.1149 (11.49 wt%) |
| CaCO₃, calcite | R -3 c | a = 4.99295, c = 17.0813 | 0.3276 (32.76 wt%) |

The independently regenerated GSAS-II profile gives Rwp = 7.081%, Rp = 5.109%, and goodness of fit = 2.959 for all 8,293 observations.

## Evidence and refinement

The chemical context is consistent with partial reaction of CaCO₃ and WO₃ at 500 °C to form CaWO₄. The monoclinic WO₃ model accounts for the diagnostic group of reflections between approximately 23 and 25° 2θ and its higher-angle families. Scheelite CaWO₄ is required by the reflections near 18.6, 28.7, 31.5, and 34.2°, while calcite is independently fixed by its intense 29.4° reflection and the associated 39.4 and 43.2° peaks. Removing any one model leaves its complete reflection family in the difference curve; no additional coherent peak family remains after the three-phase fit.

Starting atomic models were COD 2311041 (WO₃), COD 7219229 (CaWO₄), and COD 1547347 (calcite). Cells, symmetry-allowed coordinates, phase scales, physically bounded profile broadening, weak preferred orientation where supported, and a smooth positive background were refined in GSAS-II using the stated Cu Kα₁/Kα₂ wavelengths and ratio. The final project was then forward-replayed from its saved atomic models; `fit.csv` contains that regenerated profile rather than a cached refinement curve.

## Remaining uncertainty

The phase identities and major/minor inventory are reliable, but the displayed fraction digits are not a realistic uncertainty statement. Peak overlap, empirical-background correlation, preferred orientation, and the absence of supplied pointwise uncertainties limit the fractions to roughly a few absolute weight percent (about ±2–3 wt% for WO₃ and calcite and ±1–2 wt% for CaWO₄). Formal least-squares errors are smaller and do not include these systematic effects.

The fractions exclude amorphous material: without an internal standard, an absolute amorphous fraction cannot be determined. Trace crystalline phases below the residual/detection level also cannot be excluded. Space groups, cells, and heavy-atom frameworks are well constrained; oxygen coordinates are less precise. The CaWO₄ size term and calcite displacement parameter reached imposed physical bounds, and angular zero/displacement are strongly correlated, so those nuisance parameters—and fine structural interpretation based on them—are not reliable.
