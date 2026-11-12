# Powder XRD phase analysis

## Result

The crystalline specimen is predominantly wolframite-type MnWO4 with a small amount of unreacted monoclinic WO3.

| Phase | Structural model | Crystalline weight fraction |
|---|---|---:|
| MnWO4 | wolframite, `P 2/c` | 0.97873 (97.873 wt%) |
| WO3 | monoclinic gamma-WO3, `P 21/c` | 0.02127 (2.127 wt%) |

These fractions are normalized over the modeled crystalline material only. No external standard was present, so an amorphous fraction or absolute crystalline fraction cannot be determined.

## Evidence and model selection

The dominant reflection family, including the peaks near 15.71, 18.68, 23.89/24.36, 30.10/30.59, 31.37, 36.27, 37.52, and 40.58/41.18 degrees 2theta, is indexed by wolframite MnWO4. The starting topology was COD 1520200; although that source entry was measured at 2.4 GPa, only its wolframite topology was transferred and its cell and allowed coordinates were refined to this pattern. The resulting Mn-O distances are 2.100-2.291 A and W-O distances are 1.793-2.140 A, consistent with distorted MnO6 and WO6 octahedra.

A MnWO4-only model left a coherent residual family. Its lines near 23.47/24.66 degrees and throughout the 33-35, 41-42, 47-51, and 53-63 degree regions match WO3; adding it reduced a comparable physical full-profile fit from Rwp about 5.26% to 4.03%. Several exact-composition WO3 references were tested. The room-temperature neutron `P 21/c` model (COD 2311041) gave the best physical full-profile fit; its refined cell retains W-O distances of 1.715-2.160 A. A physical triclinic WO3 alternative fit less well, while another monoclinic reference had implausibly short geometry. Mn3WO6 and MnO were not accepted because their diagnostic reflection families were absent. After adding WO3, no coherent third residual family remained; the largest residuals are chiefly shoulders of reflections from the accepted phases.

## Refinement and fit quality

The GSAS-II refinement used the original 8,301-point count grid with Poisson counting weights and the reported Cu Kalpha1/Kalpha2 wavelengths and intensity ratio. Background, phase scales and cells, specimen displacement/roughness, instrumental profile terms, mild MnWO4 preferred orientation, and supported MnWO4 coordinates were refined. The low-abundance WO3 cell was refined, but its atomic coordinates were held at the neutron-reference values because this pattern does not constrain them reliably.

Final statistics are Rwp = 4.0264%, Rp = 3.0576%, Rexp = 2.7588%, and goodness of fit = 1.4638. An independent native GSAS-II forward replay regenerated the entire profile from the saved atoms and profile parameters, reproduced Rwp = 4.0264% and both fractions, and reported no background, displacement-parameter, or peak-width review flags.

## Remaining uncertainty

The covariance-derived scale-only standard uncertainty is 0.041 wt% for each normalized phase fraction. This understates model uncertainty: the minor-phase structure choice and the strong scale/surface-roughness correlation make about +/-0.3 wt% a more realistic practical uncertainty for the WO3 amount. Thus the defensible abundance is approximately 2.1 +/- 0.3 wt% WO3 on a crystalline-only basis. The WO3 phase identity and cell are supported, but its individual atomic coordinates cannot be claimed as independently measured here. Weak isolated residual features are insufficient to identify or quantify another phase.
