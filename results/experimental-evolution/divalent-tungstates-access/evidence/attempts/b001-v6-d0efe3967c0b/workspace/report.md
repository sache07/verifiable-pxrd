# Powder XRD phase analysis

## Result

Three crystalline phases are required. Weight fractions are normalized to the modeled crystalline material; the measurement does not provide an amorphous-content standard.

| Phase | Structural model | Weight fraction |
|---|---|---:|
| MnWO4 | Wolframite, P2/c, refined from COD 1520200 | 0.7050 (70.50 wt%) |
| WO3 | Monoclinic, P21/c, refined from COD 2311041 | 0.1504 (15.04 wt%) |
| Mn3WO6 | R-3 analogue-derived model | 0.1446 (14.46 wt%) |

The independently regenerated full-grid fit has Rwp = 3.0044%, Rp = 2.2189%, and GSAS-II goodness of fit = 1.696 for 8,301 observations. The submitted `final.gpx`, CIFs, fractions, and `fit.csv` all derive from the same project. Replay regenerated the profile without fitting and raised no physical/profile review flags.

## Evidence

The dominant reflection set, including the characteristic splitting around 24.1/24.6 and 30.4/30.8 degrees 2theta, is the wolframite MnWO4 pattern. Monoclinic WO3 accounts for the second ordinary family. Among exact-composition WO3 references tested with the same other phases, the selected P21/c model was clearly preferred: independently replayed Rwp values were about 4.36% for P21/c, 4.80% for P-1, and 5.22% for P21/n before final coordinate polishing.

MnWO4 + WO3 alone left a coherent family near 20.3/20.9, 29.1, 32.3, 35.6, 46–47, 54.9, 57, 67.0, 70.7, and 74.9 degrees. Ordinary Mn oxides and a Pbcn Mn2WO6 analogue either refined to negligible scale or required unstable/nonphysical profile or cell parameters and did not explain that family. An R-3 Mn3WO6 model, formed by the chemically isovalent Te(VI) -> W(VI) substitution in Mn3TeO6 (COD 2211528), explains the family across the full angular range and reduced replayed Rwp from roughly 19% for the two-phase model to 4.36% before final refinement.

The phase fractions also satisfy the precursor chemistry unusually well. For an overall Mn:W ratio of 1, the assemblage requires two moles of residual WO3 per mole of Mn3WO6; their expected masses are nearly equal. The refined WO3/Mn3WO6 mass ratio is 1.041, essentially the stoichiometric value for `Mn3WO6 + 2 WO3`.

Bounded coordinate polishing converged from all tested coordinate orders to the same solution. The final models have ordinary octahedral distances: MnWO4 has Mn-O = 2.107–2.225 A and W-O = 1.777–2.169 A; WO3 has W-O = 1.696–2.174 A; Mn3WO6 has Mn-O = 2.114–2.349 A and W-O = 1.830–1.920 A. No catastrophic contacts occur. Remaining residual extrema are centered on reflections of these accepted phases rather than forming another indexable family.

## Uncertainty

The MnWO4 and WO3 phase identities are reliable. The R-3 Mn3WO6 assignment is strongly supported by its complete reflection family, positive stable scale, charge balance, and physical geometry, but its detailed topology and oxygen coordinates remain less certain because the starting structure is analogue-derived and powder data alone do not prove uniqueness.

The crystalline fractions were stable to approximately 0.2 wt% through the final coordinate branches, but systematic model uncertainty is larger than the formal least-squares precision; about 1–2 wt% absolute uncertainty is a reasonable interpretation for the minor-phase split. No amorphous fraction can be inferred. The angular zero (0.25 degrees) is at its allowed limit and is correlated with the refined specimen displacement (-282.6 micrometres), while some profile terms also lie at bounds. Consequently, individual calibration/profile parameters and small cell shifts should not be overinterpreted.
