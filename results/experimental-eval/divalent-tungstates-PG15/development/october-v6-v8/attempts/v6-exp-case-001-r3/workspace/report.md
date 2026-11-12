# PXRD phase analysis

## Result

The crystalline pattern is described by unreacted **witherite BaCO3** and **distorted WO3**. The quantitative result, normalized over these modeled crystalline phases, is:

| Phase | Structural model | Refined cell (A, deg) | Weight fraction |
|---|---|---|---:|
| BaCO3 | Pnma (No. 62), COD 9010928 | a = 5.30692(15), b = 8.91308(26), c = 6.43190(20) | 52.16(15)% |
| WO3 | P-1 (No. 2), COD 2106293 | a = 7.30625(24), b = 7.53572(22), c = 7.69149(25); alpha = 89.925(22), beta = 90.7548(33), gamma = 90.082(12) | 47.84(15)% |

Parenthesized fraction uncertainties are the formal scale-derived values only (0.15 percentage point). A more realistic model-dependent uncertainty is approximately **1 absolute wt%**, chiefly because closely related low-symmetry WO3 models have similar powder profiles. The fractions do not quantify amorphous material.

## Evidence and refinement

The measured Cu K-alpha pattern contains two coherent, full-range reflection families. Orthorhombic BaCO3 accounts for distinctive peaks near 24.21, 28.04, 34.89, and 45.17 deg 2-theta, while distorted WO3 accounts for the 23.43/23.91/24.65 deg cluster and many independent higher-angle reflections. Both submitted atomistic models pass composition, occupancy, duplicate-site, symmetry-expansion, and close-contact audits without flags.

The final Rietveld refinement used the reported Cu K-alpha1/K-alpha2 wavelengths and 0.5 intensity ratio, refined cells and phase scales, a sample-displacement correction, a 12-term Chebyshev background, positive global U/W/Z profile terms, simple surface roughness, BaCO3 isotropic size broadening, WO3 isotropic microstrain, and weak one-axis March-Dollase terms. Atomic coordinates were retained from the audited source models: refining WO3 coordinates shortened one W-O contact to an implausible 1.606 A and was rolled back. Matched leave-one-out tests supported every retained optional profile term. The final project converged with no dropped variables and maximum shift/esd = 0.017.

For 10-100 deg 2-theta, **Rwp = 6.340%, Rp = 4.801%, Rexp = 3.484%, and GOF = 1.823**. The exported profile covers the complete measured grid (9.9034-100.0949 deg); regeneration from `final.gpx` reproduced it exactly and gives full-grid Rwp = 6.330%.

## Remaining uncertainty

A mature, otherwise matched monoclinic P21/c WO3 alternative gave Rwp = 6.360%, compared with 6.340% for the selected P-1 model. The P-1 improvement is distributed across the upper-angle pattern rather than one overlap, so it is preferred, but the exact WO3 distortion is not uniquely resolved by these data.

BaWO4 was explicitly tested because it is chemically plausible for BaCO3 + WO3 at 400 C. Its fitted amount was only about 0.37 wt%, and its apparent gain came entirely from the overlapping 26.2-27.2 deg region; it did not improve the independent expected reflection near 31.9 deg and worsened another region. It therefore fails the multi-peak support criterion and is not reported as a phase. A trace amount below reliable powder-diffraction quantification cannot be excluded. Since pointwise uncertainties were not supplied, formal fit and fraction uncertainties rely on counting-statistical GSAS-II weights and should not be interpreted as complete systematic errors.
