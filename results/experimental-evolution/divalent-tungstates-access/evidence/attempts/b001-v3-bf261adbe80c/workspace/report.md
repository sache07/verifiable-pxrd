# Powder XRD phase analysis

The pattern is described by three crystalline phases. Weight fractions are normalized over these modeled crystalline phases; an amorphous fraction cannot be determined from this refinement.

| Phase | Space group | Weight fraction |
|---|---:|---:|
| MnWO4 (wolframite) | P 2/c | 0.6800 (68.00 wt%) |
| Mn3WO6, analogue-derived | R -3 | 0.1503 (15.03 wt%) |
| gamma-WO3 | P 21/n | 0.1697 (16.97 wt%) |

The frozen full-grid GSAS-II replay gives Rwp = 2.848%, Rp = 1.969%, and GOF = 1.608 (8301 points). Its calculated curve and fractions reproduce `fit.csv` and `result.json` directly.

## Evidence

The dominant reflection set indexes as wolframite MnWO4 (COD 1520200), refined to a = 4.79948, b = 5.71503, c = 4.98256 A and beta = 91.1254 degrees. After fitting that phase, one coherent residual family was matched by the R -3 Mn3TeO6 topology (COD 2211528) after chemically plausible Te-to-W transfer, giving Mn3WO6. C2/c Mn3TeO6-family starts and a Pa-3 Cu3WO6-family start gave materially worse fits under comparable staged relaxation. The remaining family, including the 23.5-24.7, 33.7-34.5, 41.8, 50.3, and 56.3 degree groups, is accounted for by monoclinic gamma-WO3; P 21/n outperformed the tested P 21/c and Pnma references.

The phase assemblage is chemically economical. Replacing three MnWO4 formula units by Mn3WO6 + 2 WO3 preserves Mn, W, and O exactly; the refined WO3:Mn3WO6 molar ratio is about 2.17 and the overall Mn:W ratio is about 0.98. No coherent residual reflection family remains unindexed.

## Uncertainty and model limits

The MnWO4 assignment and its dominant fraction are robust. The R -3 Mn3WO6 topology is supported by a distinct reflection family and reaction balance, but it is a cross-chemistry prototype transfer; its exact light-atom coordinates are less certain than its phase identity and lattice. For WO3, unconstrained oxygen refinement produced impossible contacts and was rejected. The submitted WO3 coordinates are therefore constrained to a 0.05 A RMS displacement from the published gamma-WO3 parent. A 1.57 A O-O contact is inherited from that historical parent model and remains a review-level limitation, not a refinement-created contact. The WO3 topology and fraction are supported, but the powder data do not determine a unique high-precision oxygen substructure.

The Mn3WO6 and WO3 fractions are correlated through overlapping peaks and structural intensity uncertainty; their quoted digits are refinement output, not absolute accuracy. A practical systematic uncertainty is on the order of 1-2 wt% for each minor phase. The angular zero and specimen displacement are also strongly correlated, although bounded branch tests leave the phase inventory unchanged.
