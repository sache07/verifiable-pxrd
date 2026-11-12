# Powder XRD phase analysis

The 900 °C product from NiO + WO3 is modeled as two crystalline phases: dominant wolframite NiWO4 and residual monoclinic gamma-WO3. Fractions below are normalized over these modeled crystalline phases; this experiment does not determine an amorphous fraction.

| Phase | Structural model | Refined cell | Crystalline weight fraction |
|---|---|---|---:|
| NiWO4 | Wolframite, P 2/c (No. 13) | a = 4.60087 Å, b = 5.66355 Å, c = 4.91078 Å, beta = 89.98899° | 0.75617 (75.62 wt%) |
| gamma-WO3 | Monoclinic, P 21/c (No. 14), source setting | a = 7.68998 Å, b = 7.53424 Å, c = 10.52981 Å, beta = 136.08995° | 0.24383 (24.38 wt%) |

## Evidence and model selection

The dominant families at approximately 15.60, 19.19, 23.91, 24.85, 30.87, 36.52, 54.58, and 62.28° 2theta index coherently as wolframite NiWO4. No exact NiWO4 record was present in the accessible filtered COD index. A required stoichiometric-analogue search returned ambient wolframites; the ZnWO4 model COD 1520641 was adapted by the chemically conservative Zn2+ -> Ni2+ substitution and then refined in P 2/c. Its final geometry is physical: Ni-O = 1.999-2.045 Å and W-O = 1.868-2.211 Å.

A NiWO4-only fit left the diagnostic WO3 cluster at about 23.06, 23.53, and 24.28°, together with coherent peaks near 26.53, 28.82, 33.2-34.1, 49.87, and 55.88°. Under the same restrained nuisance model, the room-temperature neutron gamma-WO3 record COD 2311041 (P 21/c) outperformed the older coarse monoclinic record COD 1528915. A triclinic candidate gave nearly the same preliminary Rwp but refined metrically toward the monoclinic cell; tetragonal and high-pressure alternatives did not reproduce the peak splitting or had inappropriate source conditions. The accepted WO3 model has two plausible distorted WO6 environments, with W-O = 1.736-2.179 Å.

Rock-salt NiO was re-challenged after the common profile was established. It refined to only 0.057 wt%, with scale/ESD = 0.95, no fit improvement, and no convincing 43.3° unique peak. NiO is therefore not reliably detected and is excluded rather than reported as a phase.

## Refinement and fit

The final GSAS-II refinement used all 8,282 points from 10.0094 to 99.9944° 2theta with the stated Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio. A positive six-parameter power-law continuum was represented in `final.gpx` by a fixed high-accuracy Chebyshev expansion; it spans 408-2293 counts and was not allowed to absorb individual peaks. One specimen-displacement correction, nonnegative U/W/X peak widths, SH/L asymmetry, polarization, phase cells/scales, and only supported phase broadening were retained. Preferred orientation, extinction, NiWO4 strain, and unsupported size/strain combinations were neutralized. The final project converged with maximum shift/ESD = 0.08 and replays without physical-review flags.

The fresh full-grid replay gives Rwp = 4.34055%, Rp = 3.37697%, Rexp = 3.47312%, and goodness of fit = 1.24976 for Poisson weights `1/max(Iobs,1)`. `fit.csv` is generated from that replay rather than from a cached GSAS-II profile.

## Remaining uncertainty

The formal covariance uncertainty of either phase fraction is about 0.12 wt%; variation across accepted background/roughness/profile alternatives is larger, about 0.3 wt%, and is the more realistic precision. Surface-roughness A and B are not individually identifiable, although their combined low-angle correction is supported. Instrument X and phase-size broadening have an exact gauge tradeoff, so the saved crystallite sizes should not be interpreted independently.

The NiWO4 atomic model is analogue-derived rather than matched to an exact database record, though its cell, peak families, and octahedral geometry are well supported. For WO3, the published oxygen framework was retained because releasing all oxygen coordinates produced poorly determined shifts for negligible improvement; W coordinates were profile-refined collectively and then frozen after correlated oscillation. Thus the WO3 phase identity and abundance are reliable, but its individual oxygen coordinates are not independently determined by this powder pattern. Small coherent residuals remain at a few overlapped peaks, but they do not form a unique third-phase family.
