# Powder X-ray diffraction analysis

The pattern is described by two crystalline phases: **wolframite MnWO4, 97.52 wt%**, and **monoclinic WO3, 2.48 wt%**. Fractions are normalized over these modeled crystalline phases; without an internal standard they do not measure amorphous material.

| Phase | Space group | Refined cell | Crystalline weight fraction |
|---|---|---|---:|
| MnWO4 | P 2/c | a = 4.83159 A, b = 5.75764 A, c = 4.99692 A, beta = 91.2203 deg | 0.975151 |
| WO3 | P 21/c | a = 7.30374 A, b = 7.54018 A, c = 10.52876 A, beta = 133.1236 deg | 0.024849 |

## Evidence and refinement

The dominant reflections index and fit as the wolframite MnWO4 structure expected from the MnO + WO3 reaction at 900 C. A MnWO4-only refinement stopped at about Rwp = 7.27%. Its structured residual included weak peaks near 23.45, 24.68, 33.5-34.5, 42.18, 50.21 and 56.23 degrees 2-theta. These are jointly accounted for by monoclinic P21/c WO3; adding that phase lowered the full-pattern Rwp to 3.9703%.

GSAS-II was refined against all 8,301 original points using the stated Cu K-alpha1/K-alpha2 wavelengths and 0.5 intensity ratio. The model includes a smooth 20-term Chebyshev background, specimen displacement and surface roughness, peak-profile terms, MnWO4 preferred orientation, phase cells and phase scales. Since no pointwise standard uncertainties were supplied, profile statistics use the Poisson count approximation, w = 1/max(Iobs, 1). The final statistics are Rwp = 3.9703%, Rp = 3.0095%, weighted chi-square sum = 17,192.32, and wRmin = 2.76%. `fit.csv` uses observed minus calculated for the difference column.

Candidate MnO, Mn3O4, Mn2O3 and Mn3WO6 additions did not give a reproducible third-phase signal. The best MnO trial was only about 0.2-0.3 wt% and changed Rwp by roughly 0.006 percentage point, which is below what can be distinguished from the remaining profile/background mismatch. No third crystalline phase is therefore claimed.

## Remaining uncertainty

The MnWO4 phase identity and lattice are well supported. WO3 is supported as a phase, but at only 2.4 wt% its internal coordinates cannot be determined independently from this powder pattern: the submitted WO3 CIF retains reference atomic positions while refining its lattice and scale. Unconstrained coordinate refinement was unstable, so detailed WO3 bond geometry should not be interpreted as newly measured.

The covariance estimate for either weight fraction is about 0.00045 (0.045 weight-percentage point), but that excludes model choice and profile systematics. Sensitivity tests moved the weak-phase abundance by several tenths of a weight-percent; a realistic interpretation is therefore approximately 2.5 +/- 0.4 wt% WO3 and 97.5 -/+ 0.4 wt% MnWO4, not sub-0.1 wt% precision. Trace phases below roughly a few tenths wt% cannot be determined reliably here.
