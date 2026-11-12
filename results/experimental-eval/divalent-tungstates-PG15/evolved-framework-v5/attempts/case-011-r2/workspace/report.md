# Powder XRD phase analysis

The specimen is modeled as two crystalline precursor phases; no crystalline tungstate product is required by the pattern.

| Phase | Structure | Refined cell (Å, °) | Crystalline weight fraction |
|---|---|---|---:|
| WO₃ | monoclinic, *P*2₁/*c* | a = 7.69190, b = 7.53563, c = 10.53830, β = 136.1120 | 0.7179 (71.79 wt%) |
| MnO₂ | pyrolusite, *P*4₂/*mnm* | a = 4.39937, c = 2.87356 | 0.2821 (28.21 wt%) |

The formal GSAS-II 1σ uncertainty is 0.0022 in weight fraction for each phase. Fractions are normalized only over the modeled crystalline phases.

## Evidence

The WO₃ model accounts for the characteristic monoclinic triplet at approximately 23.44, 23.93, and 24.69° 2θ and its repeated families near 33–35, 50.2, and 56.2°. Pyrolusite MnO₂ accounts for the independent families near 29.01, 37.67, and 56.96°. After both phases were fitted, the remaining residuals were centered on their indexed peaks and were predominantly intensity/line-shape errors; no coherent unindexed reflection family remained. In particular, diagnostic low-angle and 30°-region reflections expected from MnWO₄ or Mn₃WO₆ were absent.

The starting structures were exact-composition COD references 2311041 (WO₃) and 1514110 (MnO₂). Several bounded coordinate starts converged to the same basin. The final geometries remain chemically ordinary: each W is six-coordinate with W–O distances of 1.67–2.20 Å, and each Mn is six-coordinate with Mn–O distances of 1.87–1.92 Å. The accepted profile includes a modest MnO₂ (110) March–Dollase term and weak uniaxial WO₃ microstrain anisotropy; a surface-roughness model was rejected because its parameters were non-identifiable.

The full 8301-point fit gives Rwp = 6.374%, Rp = 4.617%, Rexp = 2.688%, and goodness-of-fit = 2.371. The saved `final.gpx` reproduces Rwp within 0.00001 percentage point on a fresh refinement.

## Remaining uncertainty

The phase identities, topologies, and lattice metrics are reliable. The detailed WO₃ oxygen coordinates and refined displacement parameters are less well determined because overlapping peaks and correlated intensity/profile effects permit nearby coordinate solutions. The formal fraction errors therefore understate model uncertainty; the reported 71.8/28.2 wt% split should not be interpreted more precisely than roughly 1–2 percentage points. The fit does not determine an amorphous fraction, and trace crystalline phases below the pattern's detection limit cannot be excluded.
