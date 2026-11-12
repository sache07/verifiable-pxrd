# Powder XRD phase analysis

The pattern is modeled by four crystalline phases. Fractions below are normalized over those modeled crystalline phases; no amorphous fraction was measured.

| Phase | Structural model | Weight fraction |
|---|---|---:|
| CaWO4 | scheelite, `I 41/a`, COD 7219229 parent | 0.62869 ± 0.00101 |
| WO3 | monoclinic, `P 21/c`, COD 2311041 parent | 0.26888 ± 0.00065 |
| CaO | rocksalt, `F m -3 m`, COD 1563196 parent | 0.03502 ± 0.00044 |
| CaCO3 | calcite, `R -3 c`, COD 1547347 parent | 0.06741 ± 0.00103 |

## Evidence and model selection

The chemical context (CaCO3 + WO3 fired at 650 °C) is consistent with the dominant CaWO4 reaction product, residual WO3, residual calcite, and CaO from carbonate decomposition. The assignments are supported by coherent line families rather than isolated peaks: CaWO4 accounts for the strong 18.69, 28.80, 31.65, 34.19, and 39.19° features; monoclinic WO3 accounts for the 23.2–24.5°, 26.66°, and 33.34° multiplets; CaO accounts for 32.26, 37.42, 53.88, and 67.38°; and calcite accounts for the 29.51° line and its higher-angle companions.

WO3 source models were compared with identical cumulative refinement settings and fixed parent coordinates. After matched restarts, the selected monoclinic COD 2311041 model gave Rwp 4.612%, versus 4.934% for the best triclinic finalist; the other monoclinic and orthorhombic candidates were worse. The submitted WO3 CIF retains the source's valid but nonstandard monoclinic setting (beta about 136.09°).

The final profile model includes the measured Cu Kalpha doublet, a 13-term Chebyshev background, refined cells/scales, a reproducible correlated zero/specimen-displacement correction, common profile and axial-divergence terms, polarization and surface roughness, and phase-specific broadening/texture where supported. CaWO4 texture and calcite strain collapsed to their null values after ADP refinement and were removed. Removing CaO increased Rwp to 4.390%, removing calcite to 4.246%, and removing both to 5.244%, after the remaining model was re-equilibrated.

Atomic motion was tested last. Retained blocks are CaWO4 O coordinates, WO3 W coordinates, WO3 O4/O6 coordinates, CaWO4 isotropic ADPs, and WO3 W isotropic ADPs. Their improvements reproduced from independent nuisance starts. Resetting the CaWO4 O, WO3 W, or WO3 O4/O6 blocks raised Rwp to 3.042%, 3.073%, or 3.022%, respectively. Unconstrained refinement of all WO3 oxygen sites produced W–O contacts near 1.56 Å and was rejected. The submitted models pass physical screening: shortest bonds are 1.754 Å (CaWO4 W–O), 1.723 Å (WO3 W–O), 2.409 Å (CaO Ca–O), and 1.274 Å (calcite C–O), with full occupancies and positive displacement parameters.

## Fit and uncertainty

An independent zero-optimization replay of `final.gpx`, using freshly generated GSAS-II reflection lists, gives Rwp = 2.99676%, Rp = 2.21698%, Rexp = 2.76280%, and GOF = 1.08468 over the full supplied scan. The replay changed no project parameters and raised no physical/profile review flags. Remaining residual extrema track the shapes of the strongest overlapping peaks rather than forming another coherent multi-line phase family.

The quoted fraction uncertainties are formal one-standard-deviation values from the counting-statistics refinement. They do not include systematic uncertainty from preferred orientation, microstructure, absorption/surface roughness, or the correlated zero/displacement and scale/ADP subspaces. Repeated full-model starts agreed within about 0.005 wt%, but the formal uncertainties—especially for calcite and CaO—should still be regarded as optimistic. The WO3 polymorph/source distinction and calcite texture are the main structural-model uncertainties. No crystalline phase is left unidentified at a reliably quantifiable level, but this analysis cannot exclude amorphous material or phases below the pattern's detection limit.
