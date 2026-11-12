# Powder X-ray diffraction phase analysis

## Result

| Phase | Space group | Refined cell (Å, °) | Crystalline weight fraction |
|---|---|---|---:|
| MgWO4 | P 2/c | a=4.68959, b=5.67377, c=4.92821, beta=90.775 | 77.97% |
| WO3 | P 21/c | a=7.68889, b=7.53627, c=10.52848, beta=136.087 (alternate monoclinic setting) | 14.15% |
| MgO | F m -3 m | a=4.21200 | 7.88% |

The fractions are normalized only over the three modeled crystalline phases. Without an internal standard, this scan does not determine an amorphous fraction or absolute crystalline yield.

## Evidence and refinement

The precursor chemistry (MgO + WO3, heated at 900 °C) and the peak inventory support formation of MgWO4 with residual WO3 and MgO. The dominant MgWO4 model accounts for its diagnostic low-angle and split groups near 15.9, 19.2, 24.2–24.9, and 30.8–31.1° 2theta. Monoclinic WO3 accounts for the residual clusters around 23–25° and 33–35°. Rock-salt MgO is required by its comparatively isolated (200) peak near 43.2° in this displaced-pattern geometry, with supporting features near 62.5° and 75°. No additional strong, reproducible peak set remains that requires a fourth crystalline phase.

Local COD models 9013902 (MgWO4), 2311041 (WO3), and 9000499 (MgO) supplied the starting structures. A GSAS-II Rietveld refinement used the reported Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio. Refined quantities included phase scales and cells, zero, instrumental/profile terms, phase size/strain terms, MgWO4 preferred orientation, and a 16-term Chebyshev background. Atomic-coordinate refinement was restrained by the parent structures and chemically plausible distances. The resulting nearest contacts are physically reasonable: MgWO4 has W–O 1.864–2.184 Å and Mg–O 1.968–2.113 Å; WO3 has W–O 1.702–2.145 Å; MgO has Mg–O 2.106 Å.

The exact saved project was independently replayed with native GSAS-II structure factors and fresh reflection lists, with no parameter optimization and no profile-review flags. Over all 8301 measured points (9.90343322–100.09488522°), Rwp is 5.8179%, Rp is 4.3014%, and the Poisson-weighted goodness of fit is 2.037. The Rwp stored by GSAS-II for its 10–100° refinement interval is 5.8215%. `fit.csv` contains the whole original grid and uses observed minus calculated for the difference column.

## Remaining uncertainty

The three phase identities are reliable, and their fractions are a defensible crystalline-phase normalization. The quoted decimals are reproducibility values, not realistic accuracy: scale/profile overlap, preferred orientation, microabsorption, and the lack of an internal standard make systematic fraction uncertainty of a few weight-percent plausible, especially for WO3 and MgO.

The detailed oxygen displacements are less secure than the phase types, cells, and heavy-atom sublattices because Cu X-ray scattering is dominated by W and the minor WO3 reflections overlap MgWO4. WO3 oxygen coordinates were therefore kept close to the published model with only a modest data-driven adjustment. Alternative monoclinic and triclinic WO3 parents were tested; an unconstrained P-1 model could reduce the residual slightly only by adding weakly determined metric freedom that moved toward the selected monoclinic metric. P 21/c is the more parsimonious assignment, but subtle WO3 distortion/polymorph details cannot be determined uniquely from this pattern alone. The residual above the ideal counting-noise level is concentrated mainly in overlapped intensity/profile details rather than unindexed strong peaks.
