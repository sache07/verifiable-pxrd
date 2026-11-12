# Powder XRD phase analysis

The accepted three-phase model is 70.2 wt% scheelite SrWO4, 11.4 wt% monoclinic WO3, and 18.5 wt% Sr3WO6 on the modeled-crystalline basis. The final full-grid fit has Rp = 10.86%, Rwp = 15.21%, Rexp = 3.54%, and GOF = 4.31.

| Phase | Evidence | Refined cell | Weight fraction |
|---|---|---|---:|
| SrWO4, I 41/a | Dominant families at about 18.33, 28.00, 30.21, 33.39, 45.47, 51.98, 56.08, and 57.35 degrees | a = 5.42061 A, c = 11.96332 A | 0.7016 |
| WO3, P 21/c | Characteristic 23.47/23.93/24.74 degree group and higher-angle companions | a = 7.69707 A, b = 7.54002 A, c = 10.54031 A, beta = 136.1233 degrees | 0.1139 |
| Sr3WO6, Pa-3, provisional | Positive scale across the 29.75/30.90 degree pair and companions near 45, 52, and 57 degrees; together with WO3 it approximately closes the starting 1:1 Sr:W balance | a = 10.93670 A | 0.1845 |

The monoclinic WO3 model was selected over a marginally better numerical checkpoint whose reference geometry contained a 1.58 A O-O contact. The submitted WO3 model has W-O distances of 1.72-2.16 A and a 2.54 A shortest O-O distance. A high-pressure monoclinic SrWO4 decoy also fit numerically, but required roughly 2-3% lattice compression relative to its already high-pressure reference and produced an implausible bulk Sr:W balance, so it was rejected.

Sr3WO6 is the principal uncertainty. No exact Sr3WO6 reference was present in the frozen index, so its model was transferred from the Pa-3 Cu3WO6 topology by Cu-to-Sr substitution and metric expansion. The resulting reflection coverage and bulk chemistry are persuasive, but its Sr coordination and split residual intensity near 22.10 and 32.62 degrees show that the exact ambient-pressure topology is not determined reliably. Oxygen-coordinate trials became nonphysical and were rolled back. Consequently, 18.5 wt% should be treated as semiquantitative (model-choice variation was several weight percent), and a trace additional or symmetry-lowered phase cannot be excluded. The quoted formal scale uncertainties in result.json do not include this systematic uncertainty.

The final profile uses the supplied Cu K-alpha doublet, a physical zero/displacement pair, and isotropic coherent-domain sizes of approximately 0.163, 0.076, and 0.042 micrometers for SrWO4, WO3, and Sr3WO6, respectively. Preferred orientation, microstrain, surface roughness, and extra-phase branches were retained only when physical; unsupported or nonphysical branches were discarded.
