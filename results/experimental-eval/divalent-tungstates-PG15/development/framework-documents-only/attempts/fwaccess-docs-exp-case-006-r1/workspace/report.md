# Powder XRD phase analysis

The modeled crystalline sample is **97.10 wt% wolframite-type CuWO4** and **2.90 wt% residual monoclinic WO3**, normalized over the two modeled crystalline phases.

| Phase | Structural model | Refined cell | Crystalline weight fraction |
|---|---|---|---:|
| CuWO4 | triclinic P -1 | a = 4.70897 A, b = 5.84337 A, c = 4.88216 A; alpha = 91.6548 deg, beta = 92.5338 deg, gamma = 82.7501 deg | 0.97099 (97.10 wt%) |
| WO3 | monoclinic P 21/c, COD 2311041 setting | a = 7.69147 A, b = 7.53927 A, c = 10.52541 A; beta = 136.0677 deg | 0.02901 (2.90 wt%) |

## Evidence

The CuWO4 P -1 framework accounts for every major reflection, including the intense groups near 19.3, 26.3, 29.0-32.4, 35.9-38.9 and 53-67 deg 2theta. A CuWO4 framework from COD 4000806 was adapted and refined because its compressed reference cell did not match the ambient-pressure peak positions. Refining the cell and atomic coordinates produced chemically plausible distorted octahedra: Cu-O = 1.94-2.44 A and W-O = 1.79-2.23 A.

A CuWO4-only model left a reproducible low-intensity triplet near 23-25 deg and reflections near 33-35 deg. These are the diagnostic clusters of WO3 after applying the common angular/specimen correction. Adding monoclinic WO3 reduced Rwp from about 5.05% to 3.90%. The COD 2311041 P 21/c model gave better whole-pattern and phase-specific agreement than the tested triclinic, orthorhombic and alternative monoclinic WO3 references. The strongest diagnostic peaks of CuO and Cu3WO6 are absent, and no third crystalline phase is required by the remaining residual.

The final GSAS-II statistics are Rwp = 3.903%, Rp = 3.043%, Rexp = 2.434%, and goodness of fit = 1.604 over 8284 profile points. `fit.csv` contains observed, calculated, observed-minus-calculated and background profiles from this same project.

## Uncertainty and limits

The formal GSAS-II fraction esd is about 0.055 wt%, but it understates model uncertainty. Alternative physically reasonable WO3 line-broadening and closely related low-symmetry WO3 models move the trace fraction through roughly 2.6-3.0 wt%; a practical uncertainty of about +/-0.4 wt% for WO3 is more defensible. Fractions exclude amorphous material and any crystalline component below the detection capability of this scan.

The monoclinic WO3 phase family and its trace abundance are reliable, but its detailed atomic coordinates are not independently determined at approximately 3 wt%. Its reference coordinates were therefore retained while its cell, scale and peak size contribution were refined. Closely related monoclinic/triclinic WO3 distortions cannot be distinguished unambiguously from this trace pattern alone. CuWO4 atomic geometry is much better constrained, though oxygen coordinates remain correlated with low-angle profile corrections.

The zero offset and specimen displacement are almost perfectly correlated in this single Bragg-Brentano scan. Their combined peak-position correction is supported, but the individual values should not be interpreted independently. Crystallite-size and instrumental Lorentzian broadening are also partly confounded; those nuisance terms are retained only to reproduce the submitted profile.
