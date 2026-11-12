# Powder XRD phase analysis

The Cu Kα pattern from the 800 °C WO3/Mn3O4 reaction is best represented by six crystalline contributions. Fractions below are normalized over those modeled crystalline phases; they do not measure any amorphous content. Parenthesized uncertainties are formal GSAS-II one-standard-deviation scale uncertainties and do not include model-selection error.

| Phase | Refined cell (Å, °) | Weight fraction |
|---|---|---:|
| Wolframite MnWO4, P 2/c | 4.7984, 5.7051, 4.9738; β=91.106 | 53.410(307)% |
| Triclinic WO3, P -1 | 7.2999, 7.5402, 7.6891; 90.109, 90.911, 90.150 | 20.957(201)% |
| Wurtzite-type MnO, P 63mc | 3.3731, 5.3324 | 10.828(232)% |
| Rutile-type MnO2, P 42/mnm | 4.4025, 2.8976 | 7.444(185)% |
| Orthorhombic Pnnm W-O framework | 4.8421, 10.0305, 11.2225 | 5.679(174)% provisional |
| Hausmannite Mn3O4, I 41/amd | 5.7623, 9.4044 | 1.682(291)% |

The sharp majority reflections and their consistent monoclinic splitting establish wolframite MnWO4. Broad residual groups are independently accounted for by triclinic WO3, wurtzite-type MnO, and rutile-type MnO2; the latter includes diagnostic lines near 28.7°, 56.7°, and 59.4° 2θ. The small hausmannite scale remains positive, its refined cell is within 0.35% of the reference, and adding it accounts for residual intensity near its 32.4°, 36.1°, and 59.9° lines. Rock-salt MnO and alternative manganese-oxide candidates were tested but did not retain an independent, physically stable contribution.

An additional orthorhombic component is strongly indicated by correlated residual peaks near 20.0/20.4°, 35.2°, 45.6/46.9°, 64.6°, and 67.8–69.7°. A Pnnm W-O framework adapted from COD 1523082 indexes these lines and gives a chemically reasonable W-O network. Its parent is a high-pressure Li2WO4 framework whose light-cation sites are absent from the published CIF. Li is impossible in the stated synthesis, and the present powder data do not locate a defensible Mn/cation site: inserting candidate Mn sites worsened the fit or produced implausible contacts. The submitted CIF therefore represents only the diffraction-supported W-O sublattice. Its complete composition, cation occupancy, and consequently its 5.68% weight fraction cannot be determined reliably; that fraction is explicitly provisional and depends on the W/O-only cell mass.

The triclinic WO3 model was the best of the tested WO3 polymorphs, but its broad, highly strained peaks do not uniquely exclude closely related low-symmetry WO3 structures. The broad MnO/MnO2 peaks, strong texture corrections, and limiting microstrain values also make the minor-phase fractions more model-sensitive than their formal uncertainties suggest. The trace Mn3O4 assignment is correspondingly lower confidence.

An independent, read-only GSAS-II regeneration from `final.gpx` over all 8301 points gives Rwp = 11.872%, Rp = 6.906%, and goodness of fit = 5.971. The saved project has no frozen out-of-range refinement variables and contains the atomic models used for every submitted CIF and for `fit.csv`. Structured residual intensity remains, most prominently around 20.4°, consistent with the unresolved chemistry/profile of the orthorhombic component.
