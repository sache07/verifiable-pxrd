# Powder XRD phase analysis

The submitted model contains six crystalline components. Fractions are normalized over those modeled crystalline phases; no amorphous fraction or absolute yield can be obtained from this scan alone.

| Phase model | Space group | Refined cell (Å, °) | Weight fraction |
|---|---:|---|---:|
| MnWO4 wolframite | P 2/c | 4.80108, 5.71661, 4.98259; beta 91.1133 | 73.60% |
| WO3 monoclinic | P 21/c | 7.70314, 7.55075, 10.55139; beta 136.1532 | 10.45% |
| Mn2WO6 analogue | P 21 21 21 | 5.07102, 8.65377, 9.36926 | 3.21% |
| cation-disordered Mn2WO6-type analogue | Pbcn | 4.45932, 5.44511, 4.83144 | 2.76% |
| MnO, wurtzite polymorph | P 63mc | 3.37285, 3.37285, 5.38098 | 5.70% |
| Mn2WO6 analogue, provisional | P -3 1 m | 5.00781, 5.00781, 4.44414 | 4.29% |

## Evidence

MnWO4 and WO3 account for the dominant peak families and survived comparison with the available same-formula records and symmetry-diverse tungstate/WO3 alternatives. The direct Mn-oxide screen strongly selected wurtzite MnO over rocksalt MnO, Mn2O3, MnO2, and both Mn3O4 polymorph families.

Three weaker families require Mn2WO6-type models. The P 21 21 21 model is obtained by Y-to-Mn substitution in the Y2WO6 topology (COD 1541070) and fit better than three independent P 21 21 21 tellurate parents. The Pbcn model is the mixed Mn/W-site Fe2WO6 topology (COD 1565524), normalized to Mn2WO6 stoichiometry. The P -3 1 m model is derived from MnSb2O6 (COD 4342220) by Sb-to-Mn and Mn-to-W substitution. It remains positive and stable, while Pb/Sb, Ca/Sb, and Hg/As versions of the same topology refine to much smaller or zero contributions. All six exported CIFs pass the geometry/occupancy screen without short-contact flags.

The final native GSAS-II replay reproduces `fit.csv` to numerical precision and reports no profile-review flags. Fit statistics are Rwp = 16.3133%, Rp = 10.0826%, Rexp = 1.7740%, and goodness of fit = 9.2048.

## Remaining uncertainty

The three Mn2WO6 structures are analogue-derived rather than independently solved. In particular, the trigonal model has uniform W-O distances of about 2.145 Å and should be regarded as a provisional average topology. Its individual structure and 4.29% fraction cannot be determined reliably from this powder pattern alone. The split among the three Mn2WO6-type components (10.25% combined) is also strongly correlated.

Coherent residual intensity remains at 20.32, 20.88, 35.61, 47.02, and about 54.9 degrees 2theta. These positions coincide mainly with reflections of the retained P 21 21 21 family, indicating an imperfect analogue intensity model rather than a cleanly separable extra phase. Unrestrained or tightly bounded coordinate refinements moved to limits or produced implausible contacts and were rejected.

WO3 and P 21 21 21 Mn2WO6 profile refinements requested strain above the allowed range; size-only replacements hit the 0.04 micrometre lower bound. The final project therefore restores the simpler pre-profile values (0.3 micrometre, 1000 ppm) for those two phases. A rejected boundary-limited fit gave Rwp 13.96% but shifted the MnWO4/WO3/P 21 21 21 fractions to 67.2/15.9/6.1%, compared with 73.6/10.5/3.2% here. This sensitivity is larger than counting-statistical uncertainty, so especially the WO3 and minor-phase fractions should be treated as model-dependent estimates rather than precise quantitative phase analysis.
