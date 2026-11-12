# Powder XRD phase analysis

## Result

The crystalline pattern is modeled by three phases, normalized over the modeled crystalline material:

| Phase | Space group | Weight fraction |
|---|---:|---:|
| MnWO4 (wolframite) | P 2/c (No. 13) | 64.10% |
| monoclinic WO3 | P 21/c (No. 14) | 17.73% |
| Mn3WO6 | R -3 (No. 148) | 18.18% |

The full-grid native GSAS-II replay gives Rwp = 2.643%, Rp = 1.913%, and sqrt(chi-square/N) = 1.853 using Poisson count weights. The counting-statistics Rwp floor is 1.426%. Because pointwise standard uncertainties were not supplied, these statistics use `1/max(Iobs,1)` and the goodness-of-fit value is an approximate Poisson diagnostic.

## Evidence and model

The precursor chemistry (WO3 + Mn3O4, 800 C) supports manganese tungstates plus residual WO3. Wolframite MnWO4 accounts for the dominant lines, including the groups near 18.25, 23.46-24.00, 29.77-30.23, 36.00, and 51.43 degrees 2theta. Monoclinic WO3 is required by the 22.9-24.2 degree triplet and its higher-angle partners. After fitting those two phases, distinct residual maxima near 19.67, 20.20, 28.48, 35.02, 46.43, and 54.4 degrees are indexed by rhombohedral Mn3WO6. No fourth crystalline phase is demanded by the remaining residual.

Starting models were COD 1520200 (MnWO4), 1528915 (WO3), and 2002703 (Mn3WO6). The Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio from the metadata were retained. The refinement included unit cells, phase scales, background, specimen displacement/surface roughness, polarization, peak shape, crystallite size/microstrain, and supported March-Dollase texture. Refined cells are MnWO4 a=4.79603, b=5.70693, c=4.97450 A, beta=91.1623 deg; WO3 a=7.28636, b=7.52859, c=10.52036 A, beta=133.0758 deg; and Mn3WO6 a=8.88757, c=10.47965 A.

## Uncertainty

The three phase identities are well supported, but the quantitative fractions should be treated as semiquantitative (roughly +/-1-2 absolute wt%) because the minor phases overlap strongly and scale, texture, polarization, and surface-roughness terms are correlated. Fractions refer only to the modeled crystalline phases; amorphous content was not determined.

The MnWO4 atomic model is the best constrained. WO3 heavy-atom positions are supported, but its oxygen coordinates could not be refined stably and were retained from the parent model. That parent WO3 model contains a 1.575 A O-O contact, so its detailed local oxygen geometry is not reliable even though its diffraction fingerprint and phase assignment are convincing. The Mn3WO6 space group and phase contribution are supported, but its oxygen shifts are weakly determined and should not be interpreted as a high-precision structure determination.
