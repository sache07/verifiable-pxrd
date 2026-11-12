# Powder XRD phase analysis

The best retained model contains three crystalline phases. Fractions are normalized only over these modeled crystalline phases; the scan does not determine amorphous content or absolute crystallinity.

| Phase | Space group | Refined cell (Å, °) | Crystalline weight fraction |
|---|---|---|---:|
| Wolframite MnWO4 | P 2/c | 4.80026, 5.71554, 4.98096; β = 91.1225 | 0.7122 |
| Triclinic WO3 | P -1 | 7.31016, 7.54799, 7.70431; α = 90.3007, β = 90.7663, γ = 89.9259 | 0.1770 |
| Mn2WO5-like phase | P n n m | 8.63729, 8.91267, 6.04043 | 0.1108 |

## Evidence

The 8,301-point reflection scan was modeled with the reported Cu Kα1/Kα2 wavelengths (1.540598/1.544426 Å) and 0.5 intensity ratio. The 800 °C WO3 + Mn3O4 context is consistent with a dominant Mn tungstate plus residual tungsten oxide. An ordinary wolframite MnWO4 reference (COD 1520200) accounts for the dominant peaks. Adding triclinic WO3 (model based on COD 2106293) in the same project reduced the ordinary-reference fit from Rwp 24.535% to 19.859%; Mn3O4 and Mn2O3 scales then collapsed to the lower bound in equivalent common-state tests.

Coherent residual peaks prompted same-stoichiometry prototype transfer. Pnnm Mn2AsO5/Zn2AsO5 frameworks survived common-state replacement tests after As→W substitution; the selected direct Mn2AsO5-parent model (COD 9000178) refined to the cell above. A distinct R-3 Mn3WO6 transfer gave a similarly competitive early residual fit, but its scale, along with Ia-3 Mn3WO6 and Pmn2_1 MnWO4 additions, collapsed when added to the retained three-phase state. Mn2WO6 and Mn3W2O8 variants that reached stable common states did not survive; failed or aborted trials were treated as unknown. One P2_1/c Mn3W2O8 import failure likewise remains unknown rather than being counted as negative evidence.

The submitted CIFs exactly match the phases exported by a fresh read-only replay of `final.gpx`. Broad physical screening passed all three: occupancies are valid, densities are 5.34–7.36 g cm^-3, shortest metal–O distances are 1.58–1.78 Å, and shortest O–O distances are at least 2.36 Å.

## Fit and uncertainty

The saved GSAS-II refinement gives Rwp = 11.143%, Rp = 6.473%, Rexp = 1.774%, and GOF = 6.296. A fresh full-grid replay that ignored cached calculated arrays and optimized no parameters gives Rwp = 11.939% and Rp = 6.912% with weights 1/max(Iobs,1); `fit.csv` contains this replayed profile. The higher replay residual, GOF well above one, and coherent remaining difference intensity show that the model is not at the counting-noise limit.

MnWO4 is a robust identification, and WO3 is well supported although its detailed triclinic coordinates overlap strongly with the other phases. The Mn2WO5/Pnnm assignment is provisional rather than unique: it required bounded coordinate transfer, strong [010] March–Dollase texture (0.7094), and boundary-limited microstructure parameters. Its nominal 0.1108 fraction therefore cannot be claimed to the formal covariance e.s.d. (0.00146); prototype/profile trials move the minor-phase amount by several weight percent. The exact minor-phase symmetry/composition and fractions more precise than roughly the reported 71/18/11 wt% split are not reliably determined from this pattern alone.
