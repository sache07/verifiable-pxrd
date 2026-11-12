# Powder XRD phase analysis

The pattern is described by four crystalline phases. Weight fractions are normalized over the modeled crystalline material:

| Phase | Space group | Weight fraction |
|---|---:|---:|
| CuWO4 | P -1 | 0.6560 (65.60 wt%) |
| WO3 | P 21/c | 0.1926 (19.26 wt%) |
| Cu3WO6 | Pa -3 | 0.1259 (12.59 wt%) |
| CuO | C 2/c | 0.02548 (2.55 wt%) |

The final full-range Rietveld fit has Rwp = 1.7441%, Rp = 1.3062%, and goodness of fit = 1.0791 over all 8301 supplied points (9.9034-100.0946 degrees 2-theta). Cu K-alpha1/K-alpha2 wavelengths and the stated 0.5 intensity ratio were used. The refined zero offset is -0.19629 degrees and specimen displacement is +518.8 micrometres.

## Evidence for the phase inventory

Exact-composition structures from the frozen reference index were used as starting models: CuWO4 (COD 4000806), monoclinic WO3 (COD 2311041), CuO (COD 1011194), and Cu3WO6 (COD 1527404). The dominant pattern is the triclinic CuWO4 family. Monoclinic WO3 accounts for the characteristic group near 22.7-23.9 degrees, while CuO accounts for a weaker but repeated family near 35-39, 48, and 61-68 degrees. A coherent residual family near 15.2, 19.8, 32.5, 33.8, 49.7, and 57.6 degrees is jointly indexed by cubic Cu3WO6. Adding Cu3WO6 reduced the preliminary three-phase Rwp from about 18.2% to 7.33% before detailed coordinate and line-profile refinement. No coherent reflection family remains unassigned in the final difference curve.

The phase assemblage is chemically consistent with the reported CuO/WO3 precursor system: its fraction-derived bulk Cu:W molar ratio is approximately 1.008. Alternative WO3 polymorphs fit less well, and a low-temperature, lower-symmetry CuO model offered only a negligible numerical gain over the physically appropriate ambient C2/c structure.

Refinement was staged through scales/background, cells and calibration, heavy- then light-atom coordinates, displacement parameters, and supported profile terms. All sites have unit occupancy and positive isotropic displacement parameters (0.0081-0.0175 A^2). The shortest refined cation-oxygen distances are physically reasonable: 1.785 A in CuWO4, 1.715 A in WO3, 1.950 A in CuO, and 1.803 A in Cu3WO6. Independent replay of `final.gpx` regenerated the reflection lists and native GSAS-II structure factors and reproduced `fit.csv` and all fractions exactly.

## Remaining uncertainty

Fractions are relative to the four modeled crystalline phases; an amorphous fraction or absolute crystalline yield cannot be obtained without an internal standard. Pointwise uncertainties were not supplied, so counting-statistical weights were used. CuO is the weakest component and its 2.55 wt% fraction is consequently the least precise. The identities and structure families are well supported, but unconstrained light-atom coordinates, especially in WO3 and Cu3WO6, are not uniquely determined at high precision by this overlapping powder pattern; the submitted coordinates are bounded, physically screened refinements of reference structures. Zero offset and specimen displacement are correlated, although bounded multistart refinements converged to the reported solution.
