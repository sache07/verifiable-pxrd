# Powder-XRD phase analysis

## Result

Two crystalline phases are supported by the full pattern. Fractions are normalized over these modeled crystalline phases.

| Phase | Structural model | Refined cell | Weight fraction |
|---|---|---|---:|
| WO3 | monoclinic, P 21/c | a = 7.30689 A, b = 7.53789 A, c = 10.54754 A, beta = 133.1555 deg | 0.7630 (76.30 wt%) |
| Co3O4 | cubic spinel, Fd-3m | a = 8.08544 A | 0.2370 (23.70 wt%) |

The verified GSAS-II forward replay gives Rwp = 3.1222%, Rp = 2.2386%, chi-square = 27283.91, and GOF = 1.8165 for 8,301 points and 32 refined variables. The calculated profile in `fit.csv` is this fresh replay of `final.gpx`, rather than a cached curve.

## Evidence and refinement

The chemistry is consistent with incompletely reacted starting oxides after heating at 500 degC. An unreacted 1:1 Co:W charge would contain 74.28 wt% WO3 and 25.72 wt% Co3O4, close to the diffraction-derived result. The intense monoclinic-WO3 triplet at approximately 23.465, 23.954, and 24.714 deg 2theta and its many higher-angle lines are reproduced by the P 21/c model. The independent Co3O4 spinel line series, including peaks near 31.64, 37.20, 45.14, 59.68, and 65.56 deg, is simultaneously reproduced. Candidate structures were screened against the entire 10-100 deg pattern; the retained starting models correspond to COD 2311041 (WO3, transformed setting) and COD 9005896 (Co3O4).

The refinement used the stated Cu K-alpha1/K-alpha2 wavelengths and 0.5 intensity ratio, a Bragg-Brentano specimen displacement, a smooth Chebyshev background, phase scales, cells, crystallite-size/microstrain broadening, and constrained atomic coordinates. A fresh atomic-model replay has positive intensities and background and raises no profile-physics flags. Adding CoWO4 or CoO drove their scales effectively to zero. An alternate trace WO3 component refined to only about 1 wt% with unstable lattice/profile parameters and negligible fit gain, so it was not accepted as a distinct phase. A Le Bail diagnostic improved Rwp only from 3.122% to 2.963%, indicating that most observed intensity is explained by the submitted atomic models rather than by free reflection intensities.

## Uncertainty

The phase identities and two-phase inventory are reliable. The fractions are semi-quantitative: a conservative model uncertainty is about 2-3 absolute wt percentage points because scale, broadening, specimen displacement, absorption, and any weak preferred orientation are correlated. They do not quantify amorphous material or material below the diffraction detection limit.

The exact oxygen coordinates in monoclinic WO3 are not determined with high precision by this heavy-atom-dominated powder pattern; the submitted CIF is a physically constrained structural model, not a claim of single-crystal coordinate accuracy. A possible third phase at roughly the 1 wt% level cannot be identified or quantified reliably and is therefore not reported. No crystalline CoWO4 is required by the data.
