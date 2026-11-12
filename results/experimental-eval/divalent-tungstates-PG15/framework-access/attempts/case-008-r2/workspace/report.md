# Powder XRD phase analysis

The crystalline product is a two-phase mixture dominated by monoclinic wolframite MnWO4, with a minor monoclinic WO3 residue. Weight fractions are normalized over the modeled crystalline phases; no amorphous fraction or external-standard correction is implied.

| Phase | Space group | Refined cell (A, degrees) | Crystalline weight fraction |
|---|---|---|---:|
| MnWO4 (wolframite) | P 1 2/c 1, No. 13 | a = 4.83151, b = 5.75746, c = 4.99686, beta = 91.2193 | 0.97385 (97.39 wt%) |
| WO3 (monoclinic) | P 1 21/c 1, No. 14 | a = 7.68530, b = 7.53930, c = 10.53008, beta = 136.0882 | 0.02615 (2.61 wt%) |

## Evidence and refinement

The Cu Kalpha1/Kalpha2 pattern was modeled over the complete measured range (9.903-100.095 degrees 2theta). The positions and relative intensities of all major peaks index as wolframite MnWO4. A one-phase MnWO4 refinement left coherent residual peaks near 23.45, 23.92, 24.68, and 34.47 degrees and gave Rwp about 4.63%. Adding monoclinic P21/c WO3 accounts for those residuals and lowers Rwp to 3.9186% (Rp 2.9866%, Rexp 2.7588%, goodness of fit 1.4236). Fresh structure factors and reflection lists regenerated independently from `final.gpx` reproduce the submitted profile and fractions.

The MnWO4 model was initialized from COD 1520200 and its cell and independent atomic coordinates were refined. Coordinate starts from several isostructural wolframites and randomized perturbations converged to the same model. The WO3 model was initialized from the neutron structure COD 2311041; its cell and profile contribution were refined, while its atomic coordinates were retained from the parent structure. Quantitative fractions were calculated from the GSAS-II phase scales and cell masses and then normalized to the two crystalline phases.

Alternative residual-phase tests included MnO, Mn2O3, Mn3O4, Mn3WO6, and several WO3 polymorphs. The monoclinic P21/c WO3 model gave the best physically plausible residual fit. Candidate third phases refined to at most about 0.2 wt% with negligible fit improvement, so neither their identity nor fraction can be determined reliably and they are not reported as phases.

## Remaining uncertainty

WO3 is only a 2.6 wt% component. Reasonable choices for its fixed displacement parameter and peak broadening shifted its fraction across roughly 2.3-2.7 wt%; a practical uncertainty is therefore about +/-0.3 wt% absolute (with the complementary uncertainty on MnWO4). The presence and monoclinic phase assignment are supported by multiple peaks, but the detailed WO3 oxygen coordinates and displacement parameters cannot be determined reliably from this pattern. The reported fractions apply only to modeled crystalline material.
