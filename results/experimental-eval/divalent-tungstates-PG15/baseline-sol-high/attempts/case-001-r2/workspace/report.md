# Powder diffraction phase analysis

## Result

The modeled crystalline material is predominantly unreacted orthorhombic BaCO3 and monoclinic WO3, with a tentative trace of scheelite BaWO4. Fractions are normalized over the modeled crystalline phases; they do not quantify any amorphous material.

| Phase | Structural model | Weight fraction | Refined cell (A, degrees) |
|---|---|---:|---|
| WO3 | monoclinic P21/c (COD 2311041) | 44.65 wt% | a=7.69815, b=7.54196, c=10.54696, beta=136.1189 |
| BaCO3 | orthorhombic Pmcn/Pnma setting (COD 9010928) | 54.73 wt% | a=5.31088, b=8.92088, c=6.43701 |
| BaWO4 | scheelite I41/a (COD 1527204), tentative | 0.62 wt% | a=5.614, c=12.719 (held at reference values) |

The formal least-squares standard uncertainties on the fractions are 0.15, 0.15, and 0.05 wt%, respectively. These describe counting-statistical precision within this model and are smaller than the realistic uncertainty discussed below.

## Evidence and refinement

The 23.43-24.66 degree multiplet and the group of lines from 33.57 to 34.89 degrees are characteristic of monoclinic WO3. Strong additional peaks at 42.29, 45.18, and 47.08 degrees are accounted for by orthorhombic BaCO3. This assignment is also chemically consistent with the reported BaCO3 + WO3 precursor mixture heated at only 400 C. Candidate WO3 polymorphs and the expected BaWO4 product were explicitly tested against the full pattern rather than selected from chemistry alone.

Adding BaWO4 to the final profile model lowers Rwp from 8.786% to 8.715% and accounts for weak residual intensity at its expected reflections. Its refined abundance is only 0.62 wt%, however, and its strongest lines overlap those of the major phases. The presence of a small scheelite contribution is plausible, but its exact fraction and independently refined lattice/atomic structure cannot be determined reliably from this pattern.

GSAS-II refinement used the reported Cu K-alpha1/K-alpha2 wavelengths and 0.5 intensity ratio, an eight-term smooth Chebyshev background, a refined zero offset, positive U/W/X peak-width terms, major-phase lattice parameters, and phase scales. Atomic coordinates were retained from the cited COD structures because the overlapping laboratory data do not support stable independent coordinate refinement. The final refinement converged with maximum shift/s.u. 0.007 and gave Rwp=8.715%, Rp=6.771%, Rexp=3.478%, goodness-of-fit=2.506, and reduced chi-square=6.280 over 9.903-100.095 degrees 2-theta.

## Remaining uncertainty

No calibrated instrument profile or pointwise standard uncertainties were supplied. GSAS-II therefore used counting-based weights, and the refined 0.313 degree zero offset and profile/background choices contribute systematic uncertainty. A practical uncertainty of a few weight percent is more appropriate for each major-phase fraction than the formal values. The sub-1 wt% BaWO4 result should be treated as tentative (roughly detection-limit level), not as a precise quantitative determination. Preferred orientation, microabsorption, and amorphous content were not independently measurable here.

All submitted CIFs, fractions, and the observed/calculated/difference profile were exported from `final.gpx`.
