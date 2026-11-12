# PXRD phase analysis

The best physically screened model contains three crystalline components. Fractions are normalized over these modeled crystalline phases; they do not quantify amorphous material.

| Phase model | Space group and refined cell (Å, °) | Weight fraction | Evidence level |
|---|---|---:|---|
| MnWO4 (huebnerite/wolframite) | P 2/c; a=4.91390, b=5.72899, c=5.00219, β=88.9727 | 0.68062 ± 0.00710 | High |
| WO3 | P 21/c; a=7.73385, b=7.63214, c=10.59171, β=135.7603 | 0.22038 ± 0.00520 | High |
| Mn2WO6, Pbcn analogue | Pbcn; a=4.62733, b=16.65066, c=4.94886 | 0.09900 ± 0.00658 | Tentative |

The quoted uncertainties are GSAS-II covariance estimates and are smaller than the likely systematic uncertainty from overlap, preferred orientation, source-coordinate choice, and the uncertain minor-phase structure.

## Identification and inventory checks

The Cu Kα1/Kα2 data (1.540598/1.544426 Å, ratio 0.5) were modeled over the complete measured 9.903–100.095° 2θ range. The MnWO4 model uses the huebnerite topology from COD 9008131 with its small Fe occupancy replaced by Mn. The WO3 model uses monoclinic COD 2311041. Their peak families persist from low through high angle, and alternate MgWO4-derived MnWO4 and triclinic/small-cell WO3 records fit worse under the same nuisance model.

The residual inventory was searched for exact Mn–O–W records and for charge-balanced non-1:1 products. `learned/stoichiometric_analogues.py` was run for Mn2WO5, Mn2W2O7, Mn4WO7, and Mn2WO6. The retained Mn2WO6 model was made by physically substituting Mn into the Pbcn Fe2WO6 parent COD 2310464. On the same full-range baseline it lowers Rwp from 22.713% to 22.462%, refines to about 9.9 wt%, and changes the parent cell lengths by no more than about 1.1%. The equal-complexity tetragonal Cr2WO6-derived topology refined to zero. This topology discrimination supports a weak Pbcn component, but no exact Mn2WO6 record was available and its phase Rf is 42.9%; therefore its exact structure and fraction cannot be determined reliably from this pattern alone.

Re-challenges rejected tetragonal Mn3O4, W17O47, triclinic WO3, and the tetragonal Mn2WO6 analogue at zero scale. Mn3WO6 refined to 0.2 ± 0.7 wt% and the Mn2W2O7 analogue to 0.8 ± 0.8 wt%, so neither was retained. W18O49 and a distorted orthorhombic Mn3O4 record also fit worse or required implausible cell changes. A duplicate MnWO4 component lowered Rwp but split roughly one-third of the material into an anisotropically distorted copy of the same composition; with no independent chemistry, that was treated as unresolved profile/structural mismatch rather than a separate phase.

The formal oxidation states are Mn2+/W6+ in MnWO4, W6+ in WO3, and Mn3+/W6+ in Mn2WO6, consistent with the mixed Mn2+/Mn3+ precursor Mn3O4. On a 100 g modeled-crystalline basis, the fractions correspond to 0.22479 mol MnWO4, 0.09506 mol WO3, and 0.02540 mol Mn2WO6 (Mn:W = 0.798). A formal precursor balance is

`0.09187 Mn3O4 + 0.34525 WO3 -> 0.22479 MnWO4 + 0.02540 Mn2WO6 + 0.09506 WO3 + 0.03323 O2`.

This is an element/charge balance, not a reconstruction of the batch: precursor amounts, gas exchange, and noncrystalline material are unknown.

## Profile and nuisance-model checks

The final common profile has nonnegative U/W/X = 0/30/0.5, with V/Y/Z fixed at zero. Direct isolated observed widths remain approximately constant (for example 0.129° at 18.064°, 0.125° at 51.250°, and 0.162° at 80.035°), which rejects the earlier high-U branch that broadened calculated high-angle peaks excessively. Repeated low-angle asymmetry supports SH/L=0.13168. Polarization refined to 0.24951. Surface roughness produced negative parameters and was rejected. Six-, eight-, and ten-term backgrounds changed Rwp by only about 0.02 percentage point; eight Chebyshev terms were retained.

Preferred-orientation tests compared no texture and distinct axial/diagonal directions. The replay-stable choices are March–Dollase [001] for MnWO4 (0.8589) and [010] for WO3 (0.7888). Isotropic size/strain terms changed final-baseline Rwp by at most 0.008 percentage point; the best uniaxial strain term changed it by 0.016 point, while generalized strain became nonphysical and worsened the fit. All such terms were pruned. Unconstrained coordinate branches moved oxygen atoms by roughly 0.4–0.6 Å or produced implausible bonds and were also pruned; submitted coordinates therefore remain source-based while the cells are refined.

The following audit uses background-subtracted profiles, a seven-point quadratic Savitzky–Golay filter, and local prominence half-height crossings. L/R are the left/right half-widths in degrees. The weak Mn2WO6 middle/high-angle measurements are noise-limited and are included to show, rather than conceal, the remaining uncertainty.

| Phase, region, hkl | Observed position | Calculated position | Observed FWHM (L/R) | Calculated FWHM (L/R) |
|---|---:|---:|---:|---:|
| MnWO4 low (1 1 -1) | 30.028 | 30.006 | 0.103 (0.048/0.055) | 0.147 (0.076/0.071) |
| MnWO4 middle (1 0 2) | 40.079 | 40.090 | 0.072 (0.038/0.034) | 0.091 (0.051/0.040) |
| MnWO4 high (4 0 2) | 87.783 | 87.816 | 0.071 (0.034/0.037) | 0.087 (0.050/0.037) |
| WO3 low (0 2 0) | 23.291 | 23.247 | 0.077 (0.043/0.035) | 0.132 (0.070/0.062) |
| WO3 middle (2 2 -4) | 41.481 | 41.459 | 0.079 (0.050/0.029) | 0.093 (0.052/0.041) |
| WO3 high (4 5 -2) | 84.697 | 84.664 | 0.053 (0.012/0.040) | 0.101 (0.051/0.050) |
| Mn2WO6 low (1 3 0) | 24.964 | 24.986 | 0.049 (0.019/0.031) | 0.165 (0.095/0.070) |
| Mn2WO6 middle (2 0 0) | 38.841 | 38.852 | 0.043 (0.022/0.021) | 0.116 (0.049/0.067) |
| Mn2WO6 high (0 12 1) | 70.397 | 70.375 | 0.087 (0.036/0.051) | 0.072 (0.036/0.036) |

## Fit quality and uncertainty

After save/reopen/full-range replay, Rwp=22.462%, Rp=15.352%, Rexp=2.490%, and goodness-of-fit=9.020. The fit is chemically and positionally informative but not counting-statistics limited; coherent intensity and width residuals remain, as also reflected by phase Rf values of 30.6% (MnWO4), 38.3% (WO3), and 42.9% (Mn2WO6). Preferred orientation, source-based coordinates, possible defect/disorder scattering, and any amorphous content are not uniquely separable here. The MnWO4 and WO3 identifications are reliable, but their normalized fractions likely carry several weight-percent systematic uncertainty. The Mn2WO6 assignment is the best screened weak-phase model, not a definitive structure solution; its reported 9.9 wt% should be regarded as an approximate model allocation (roughly 5–15 wt% is a more realistic qualitative range).
