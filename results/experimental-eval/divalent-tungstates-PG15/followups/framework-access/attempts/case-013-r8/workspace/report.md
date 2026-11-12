# Powder XRD phase analysis

The pattern is best described by seven crystalline phases. Weight fractions below are normalized only over those modeled crystalline phases; no amorphous fraction can be obtained from this scan without an internal standard.

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| Scheelite PbWO4 | I41/a | a = 5.46469, c = 12.06052 | 0.5335 |
| Massicot PbO | Pbcm | a = 5.90012, b = 5.49054, c = 4.75841 | 0.0745 |
| Monoclinic WO3 | P21/c | a = 7.30131, b = 7.54545, c = 10.57114, beta = 133.2705 | 0.1017 |
| Pb2WO5 | C2/m | a = 14.22825, b = 5.80989, c = 7.35574, beta = 113.8946 | 0.1219 |
| Litharge PbO | P4/nmm | a = 3.96965, c = 5.07052 | 0.0294 |
| Pb3WO6-like | P21/m | a = 7.15982, b = 5.74718, c = 8.05093, beta = 102.1221 | 0.0986 |
| Long-period alpha-PbO approximant | Pbcm | a = 5.02555, b = 5.63533, c = 45.03384 | 0.0404 |

The frozen GSAS-II replay gives Rwp = 8.655%, Rp = 6.182%, and weighted chi-square = 50,599.9 over 8,282 points using Poisson count weights. The fitted zero is 0.13284° 2theta and the specimen displacement is -284 micrometres.

## Evidence

Scheelite PbWO4 accounts for the dominant reflection series. The remaining indexed peaks require both PbO precursor polymorphs, monoclinic WO3, and the two lead-tungstate intermediates. A long-c PbO model accounts for a separate family of weak satellite/superstructure reflections that PbO2, Pb2O, and Pb3O4 alternatives did not retain once this component was present.

With every structure and peak shape frozen and only the other scales/background re-solved, deleting each phase raises Rwp as follows: PbWO4 36.19%, massicot 11.00%, WO3 11.12%, Pb2WO5 11.75%, litharge 8.764%, Pb3WO6-like 10.15%, and long-period PbO 8.890%, versus 8.655% for the complete model. Thus even the two weakest PbO components have independent, though modest, support.

Reference structures were used directly for PbWO4, massicot, WO3, and litharge. Pb2WO5 was modeled by replacing Mo with W in the isostructural Pb2MoO5 C2/m framework. The long-period phase is a commensurate approximant to modulated alpha-PbO.

## Remaining uncertainty

The abundance uncertainty is dominated by overlapping Pb-rich reflections and phase-specific broadening/texture, not counting statistics. Reasonable absolute systematic uncertainties are about 0.01 for PbWO4, WO3, and litharge; 0.015 for massicot, Pb2WO5, and long-period PbO; and 0.02 for the Pb3WO6-like phase. In particular, the long-period PbO contribution is defensibly about 3–6 wt%, so its exact fraction and modulation are not uniquely determined.

The Pb3WO6-like lattice and its contribution are strongly supported, but its submitted atomic model is provisional: it was adapted from a Pb3SO6 topology, and the resulting W–O distances near 1.47 Å are chemically compressed. Powder intensities constrain the Pb/W framework much better than the oxygen sublattice, so a unique local structure for this phase cannot be determined reliably from these data. The Pb2WO5 oxygen coordinates are likewise less certain than its lattice and heavy-atom framework.

All exported CIFs pass the broad occupancy/contact screen, and the corrected litharge model is stoichiometric PbO. The reported fractions do not include any unmodeled amorphous material.
