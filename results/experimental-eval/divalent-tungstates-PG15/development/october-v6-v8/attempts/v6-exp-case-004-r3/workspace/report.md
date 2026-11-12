# PXRD phase analysis

## Result

The crystalline pattern is modeled as **29.82 wt% CoWO4** (wolframite, P 2/c) and **70.18 wt% WO3** (triclinic, P -1). Fractions are normalized over these two crystalline phases only. The final fit has Rwp = 4.9194%, Rp = 3.8017%, Rexp = 3.2743%, and GOF = 1.5024.

## Evidence and model selection

CoWO4 is supported by a coherent set of peaks near 19.09, 30.71, 36.44, 41.47, 47.27, 52.13, and 54.15 degrees 2-theta. The atomistic model uses the wolframite MgWO4 topology from COD 9013902 with a charge-balanced Mg2+ to Co2+ substitution; the directly retrieved CoWO4 CIF was malformed and was rejected. The refined cell is a = 4.66874, b = 5.68270, c = 4.94857 A, beta = 89.9986 degrees.

WO3 accounts for the strong 23.18/23.67/24.42 degree triplet and the related 33–34, 47–50, and higher-angle families. Geometry-clean monoclinic and triclinic atomistic models were carried through the same nuisance refinement. The triclinic model gave material complete-pattern improvement (matched mature-model Rwp about 4.93% versus 5.25% for monoclinic WO3), so COD 2106293 was selected. Its refined cell is a = 7.30535, b = 7.53490, c = 7.69114 A, alpha = 89.7487, beta = 90.8062, gamma = 90.2072 degrees.

CoO and Co3O4 were retested individually from the mature two-phase model. Co3O4 refined to a scale statistically indistinguishable from zero. CoO produced a nominal trace estimate of about 0.35 wt%, but its strongest relatively unique prediction near 42.47 degrees worsened the local fit; improvements occurred only at peaks already overlapped by the accepted phases. It therefore fails the multi-peak/absence test and is not reported as a phase. No additional crystalline-phase fraction can be determined reliably from this pattern.

## Refinement and uncertainty

The GSAS-II refinement used the reported Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio, Poisson counting weights, empirical background, refined cells and phase scales, specimen displacement, positive Gaussian/Lorentzian width terms, a Suortti surface-roughness correction, and isotropic WO3 size broadening (~0.152 micrometre). Microstrain, preferred orientation, polarization refinement, axial divergence, and extra oxide phases were rejected as unsupported, unphysical, or correlated. Removing each retained optional term materially degraded the complete-pattern fit.

The formal conditional fraction esd is about 0.13 percentage point for each phase. This is smaller than the likely systematic uncertainty because no pointwise uncertainties, calibrated instrumental profile, or internal standard were supplied. The fractions do not quantify amorphous material, and the fixed library atom coordinates are less strongly constrained than the phase identities, cells, and relative crystalline fractions. Both exported CIFs pass composition, occupancy, symmetry, duplicate-site, and contact audits; the final project passes convergence, profile-regeneration, and positive-width checks with no SVD-dropped variables.
