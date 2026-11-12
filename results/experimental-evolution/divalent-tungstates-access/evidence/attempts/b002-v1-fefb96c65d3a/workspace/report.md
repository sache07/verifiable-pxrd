# Powder XRD phase analysis

The final model contains nine crystalline profile components. Weight fractions are normalized over those modeled crystalline phases; no amorphous fraction was measured.

| Phase model | Space group | Weight % | Assessment |
|---|---:|---:|---|
| Wolframite MnWO4 | P2/c | 56.163 | High-confidence phase identity |
| Monoclinic WO3 | P21/c | 17.255 | High-confidence residual precursor |
| Monoclinic Mn2WO5 analogue | P21/c | 5.006 | Stable analogue-derived topology |
| Orthorhombic Mn2WO5 analogue | Pnnm | 6.891 | Stable analogue-derived topology |
| Rutile-like disordered MnWO4 | P42/mnm | 2.730 | Stable diffraction component; local cation order uncertain |
| Trigonal Mn2O3 analogue | P-3m1 | 6.508 | Stable analogue-derived oxide component |
| Orthorhombic MnO2 analogue | Pna21 | 4.236 | Stable analogue-derived oxide component |
| Minor rutile-family MnWO4 analogue | P42/mnm | 0.277 | Provisional; structure/composition and fraction not reliable |
| Cubic Mn2O3 analogue | Fd-3m | 0.933 | Minor but stable analogue-derived component |

The fit over 10–100 degrees 2theta has Rwp = 7.510%, Rp = 5.578%, and GSAS-II GOF = 3.773. A native no-refinement replay of `final.gpx` over all 8301 measured bins gives Rwp = 7.515%; this replay generated `fit.csv`. The replay completed without negative-background, peak-width, polarization, or displacement-parameter flags.

## Evidence

The metadata describes WO3 + Mn3O4 fired at 800 C and measured in Cu Kalpha Bragg-Brentano geometry. The dominant wolframite MnWO4 and residual monoclinic WO3 models account for the principal sharp families. All exact same-formula structures in the supplied index were enumerated. No exact Mn2WO5 structure was available, so oxide parents were substituted while preserving site multiplicity and topology. P21/c and Pnnm Mn2WO5 models both retained positive scales under common nuisance settings and passed contact/occupancy checks.

Successive residual searches over 3018 oxide-parent groups nominated the P42/mnm, P-3m1, Pna21, and Fd-3m components. Each was required to survive scale/background, then cell, then neutral-profile tests. Exact Mn3O4 and common exact Mn2O3 candidates collapsed; a hexagonal MnO branch became non-identifiable after P-3m1 Mn2O3 was included and was removed. After the final inventory, the largest residual extrema coincide with strong reflections of already modeled WO3, wolframite, Mn2WO5, and MnO2 and have neighboring opposite-sign lobes; no additional coherent unassigned family survived the control additions.

Refinement complexity was staged. The final model uses a specimen shift of 107 micrometres, limited March-Dollase terms for WO3 [100] (0.9071) and monoclinic Mn2WO5 [110] (1.3907), a 0.040 micrometre Pnnm size term, and isotropic strain of 7463 ppm for the larger-cell rutile component and 5663 ppm for P-3m1 Mn2O3. Roughness, polarization refinement, unstable size terms, extreme uniaxial strain, and coordinate branches with short contacts were rejected. Every submitted CIF has valid occupancies, density 3.61–7.40 g/cm3, no O-O contact below 1.8 A, and exactly matches the corresponding structure replay-exported from `final.gpx`.

## Remaining uncertainty

The least-squares fraction errors in `result.json` do not include model-selection uncertainty. The two Mn2WO5 models and the P-3m1/Pna21/Fd-3m manganese oxides are analogue-derived average structures; their diffraction contributions are supported, but exact local atomic arrangements are not uniquely determined from this powder pattern. The two P42/mnm MnWO4 models contain average disordered Mn/W cation sites, so their CIFs should not be interpreted as resolved local W coordination.

The 0.277 wt% second rutile-family component is below a defensible quantitative/identification threshold. It improves the profile reproducibly, but MnWO4, WO2, and MnO2-like variants share much of this weak peak family; its submitted MnWO4 average structure is provisional. Fractions for the other minor analogue phases can also carry systematic errors of several tenths to a few weight percent despite their smaller formal errors.

The complete tested/rejected branch record is in `candidate_ledger.md`.
