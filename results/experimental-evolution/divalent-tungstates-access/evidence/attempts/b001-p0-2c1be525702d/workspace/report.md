# Powder XRD phase analysis

The pattern is modeled by three crystalline phases: wolframite-type ZnWO4, monoclinic WO3, and wurtzite ZnO. The refined fractions below are normalized over those modeled crystalline phases.

| Phase | Space group | Refined cell (A, degrees) | Weight fraction |
|---|---|---|---:|
| ZnWO4 | P 2/c (No. 13) | a=4.69968, b=5.72556, c=4.93732, beta=90.5996 | 0.72895 (72.90 wt%) |
| WO3 | P 21/n (No. 14) | a=7.29888, b=7.53498, c=7.69060, beta=90.9094 | 0.18871 (18.87 wt%) |
| ZnO | P 63mc (No. 186) | a=3.25287, c=5.22527 | 0.08234 (8.23 wt%) |

## Evidence and refinement

ZnWO4 accounts for the dominant wolframite reflections near 18.99, 24.59, 30.5-30.8, 36.4, and 38.4 degrees 2theta and is chemically consistent with reaction of the stated WO3 and ZnO precursors. The 23.2-24.6 degree cluster and further reflections around 33-34 degrees require residual monoclinic WO3. Weak but coherent wurtzite ZnO reflections near 31.8, 34.4, and 36.3 degrees remain after the first two phases are fitted. Omitting either precursor phase leaves multiple matched-series residual peaks; no fourth crystalline phase was supported by a coherent additional reflection set.

The Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio from the metadata were fixed. The refinement included phase scales and cells, a positive 12-term Chebyshev background, specimen displacement, polarization, peak width, crystallite size, WO3 uniaxial microstrain, and March-Dollase preferred orientation. Atomic coordinates were refined inside symmetry-preserving displacement bounds. A fresh atomic replay of `final.gpx` over all 8301 points gives Rwp=3.539%, Rp=2.470%, and goodness of fit=1.565; the counting-statistics Rwp floor is 2.267%. The replay reports no invalid-profile flags and the calculated background remains positive.

## Remaining uncertainty

The phase identities are secure, but the quoted covariance errors (about 0.06-0.08 wt% absolute) do not include model selection, texture, absorption, or profile correlations. A more realistic interpretation is roughly +/-1-2 wt% absolute, with the minor ZnO fraction the most sensitive. Without an internal standard, these values do not quantify amorphous material and must be read only as normalized crystalline fractions.

The cells and heavy-atom frameworks are better determined than oxygen coordinates. WO3 oxygen positions are especially correlated and sit at the allowed displacement bound; its CIF retains a short O-O contact of about 1.62 A inherited from the published monoclinic template, so it should be treated as a diffraction model rather than a definitive local-geometry determination. The refined angular zero also reached the allowed -0.25 degree boundary and is correlated with specimen displacement and cell constants. These limitations do not materially change the three-phase assignment, but they limit the reliability of fine structural interpretation and last-decimal fractions.
