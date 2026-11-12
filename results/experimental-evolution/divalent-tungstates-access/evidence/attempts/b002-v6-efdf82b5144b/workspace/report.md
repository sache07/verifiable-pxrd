# Powder XRD phase analysis

## Result

The 700 °C product from the 1:1 WO3/ZnO precursor mixture is a partially reacted, three-phase crystalline mixture:

| Phase | Structural model | Crystalline weight fraction |
|---|---|---:|
| ZnWO4, wolframite | monoclinic P2/c | 0.82651 (82.65 wt%) |
| WO3 | monoclinic P21/c | 0.12265 (12.26 wt%) |
| ZnO, wurtzite | hexagonal P63mc | 0.05084 (5.08 wt%) |

The fractions are normalized only over the modeled crystalline phases. No amorphous fraction was measured. The independent, no-refinement replay of `final.gpx` over all 8,301 original points gives Rwp = 3.55997%, Rp = 2.67994%, and goodness of fit = 1.34723 with weights 1/max(counts,1).

## Evidence and model selection

The dominant reflection sequence is indexed throughout the scan by wolframite ZnWO4, including the low-angle 010 and 100 reflections near 15.79° and 19.19° 2theta and the characteristic split group near 30.8–31.0°. Because the exact ZnWO4 entry was withheld from the frozen reference index, its model was adapted from an isostructural divalent-metal wolframite and refined in P2/c.

Monoclinic WO3 accounts for coherent residual families at approximately 23–25°, 29°, 33–35°, 42°, and 47–56°. A neutron-derived P21/c WO3 model (COD 2311041) was selected over a numerically close alternative that produced an implausibly short O–O contact. Wurtzite ZnO accounts for the weaker but repeated families near 32.0°, 34.9°, 36.7°, 48°, and 56.8°; its starting model was COD 9004178. These phases are also the chemically ordinary target plus residual precursors expected from the synthesis. No coherent residual reflection family remains that justifies another crystalline phase.

The accepted profile includes mild March–Dollase orientation terms for ZnWO4 [111], WO3 [110], and ZnO [001], phase-specific coherent sizes of about 0.067, 0.093, and 0.060 micrometres, respectively, and a specimen displacement of -669 micrometres. Isotropic microstrain refined effectively to zero and was omitted. Surface roughness was rejected because its parameters were highly correlated and repeatedly hit bounds. The required one-shot staged coordinate polish reduced Rwp from 3.71161% to 3.55997% without fraction collapse or bad geometry. Final bond ranges are chemically ordinary: ZnWO4 W–O 1.797–2.170 Å and Zn–O 2.000–2.231 Å; WO3 W–O 1.682–2.209 Å with O–O at least 2.538 Å; and ZnO Zn–O 1.973–1.995 Å.

## Remaining uncertainty

The phase inventory and three structure types are reliable at the measured resolution. The reported covariance-only fraction standard uncertainties are small, but they do not include model choice, texture, ADP, overlap, or background systematics. A more realistic reading is approximately ±1 wt% absolute for ZnWO4 and WO3 and ±0.5 wt% for ZnO. The ZnWO4 orientation parameter reached the lower end of the tested physical range, so it is a notable source of fraction uncertainty.

The exact oxygen coordinates and isotropic displacement parameter of the 12 wt% WO3 phase, and the internal coordinate of the 5 wt% ZnO phase, are not independently precise from this pattern. The final WO3 oxygen sublattice therefore remains reference-dominated; its refined W positions and all interatomic distances are physical. Minor-phase common Uiso values were fixed at 0.010 Å² because profile scans did not yield stable interior minima. Trace phases below the pattern's practical detection limit cannot be excluded.
