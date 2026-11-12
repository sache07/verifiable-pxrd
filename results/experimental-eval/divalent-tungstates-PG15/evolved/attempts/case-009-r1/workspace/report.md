# PXRD phase analysis

## Result

The crystalline product is predominantly wolframite MnWO4 with a weak alpha-Mn2O3 impurity. Fractions are normalized only over these modeled crystalline phases.

| Phase | Structural model | Weight fraction |
|---|---|---:|
| MnWO4 (wolframite) | P2/c, refined cell and coordinates | 99.36(12)% |
| alpha-Mn2O3 (orthorhombically distorted bixbyite) | Pbca reference cell and coordinates | 0.64(12)% |

The parenthetical values are formal 1-sigma uncertainties from the refinement with sigma = sqrt(counts). Because experimental pointwise uncertainties and an instrument calibration were not supplied, systematic uncertainty is larger than these formal values, especially for the trace phase.

## Evidence and structural models

The precursor chemistry (Mn3O4 + WO3 heated at 900 C) and the complete peak sequence support MnWO4. The wolframite model accounts for the characteristic families at approximately 18.6, 23.8/24.3, 30.0/30.5, 36.2, 41.1, and 51--53.5 degrees 2theta and the dense high-angle pattern. The only exact-composition P2/c record in the screened COD inventory was COD 1520200. It was measured at 2.4 GPa, so its source cell was not accepted as an ambient cell: the cell and all symmetry-independent coordinates were refined. The final cell is a = 4.831061, b = 5.757516, c = 4.996671 A, beta = 91.21777 degrees, V = 138.95058 A3. A cross-chemistry ambient ZnWO4 prototype with Zn-to-Mn substitution was also tested and fit substantially worse. The submitted MnWO4 geometry is physical: Mn-O = 2.148--2.331 A and W-O = 1.744--2.098 A, with sixfold coordination and full occupancy.

The Mn2O3 scale is supported by coherent residual reductions at its strongest separated or partly separated families near 33.2, 55.4, and 66.0 degrees, with weaker corroboration near 23.4 and 38.5 degrees. Cubic Ia-3/I213 approximations and the physical ambient Pbca distortion were compared under the same common profile. They give similar sub-percent scales; Pbca COD 1514103 was retained because it is the established ambient alpha-Mn2O3 structure and has sensible fully occupied MnO6 geometry (Mn-O = 1.875--2.306 A). At this signal level, free cell parameters drifted without improving the fit, so the Mn2O3 cell and coordinates were fixed to the reference. The diffraction data do not independently resolve its small orthorhombic distortion; depending on the cubic/Pbca reference, the modeled amount is approximately 0.5--0.7 wt%.

Mn3O4, MnO, Mn3WO6, monoclinic WO3, and triclinic WO3 were re-challenged after establishing the common profile. Mn3O4 and MnO scales were not significant, and Mn3WO6 collapsed to an unstable/negative scale. WO3 records produced formal 0.3--0.5 wt% scales, but their improvement was concentrated in overlapped low-angle MnWO4 shoulders while expected separated WO3 families were absent or worsened; they were therefore rejected as residual-fitting surrogates rather than retained phases.

## Refinement and uncertainty

The final GSAS-II model uses the reported Cu Kalpha1/Kalpha2 wavelengths and fixed 0.5 intensity ratio over the complete 9.9034--100.0949 degree range. It contains a smooth positive 10-term Chebyshev background, one specimen displacement, surface-roughness B, nonnegative common W/X broadening, and the replay-stable SH/L axial-asymmetry term. U, V, Y, and Z were fixed at zero. Size, microstrain, extinction, and preferred orientation were left neutral: isotropic size was exactly degenerate with X, strain refined negative, and symmetry-distinct texture-axis trials stayed within about 1% of random orientation without support from multiple isolated families. The last save/reopen replay converged with maximum shift/esd = 0.00072.

Final statistics are Rwp = 5.2826%, Rp = 3.9800%, Rexp = 3.4605%, and goodness of fit = 1.5292 for 8301 observations and 29 variables. Positions and widths are coherent through the middle- and high-angle isolated families. Some repeatable low-angle intensity/asymmetry residual remains at the strongest MnWO4 peaks. SH/L and specimen displacement are 96.9% correlated, so the absolute cell and low-angle line-shape parameters should not be interpreted at single-crystal precision. Sub-percent additional phases cannot be excluded, and no amorphous fraction can be obtained without an internal standard. `fit.csv`, both CIFs, the fractions, and the statistics were exported from the final reopened `final.gpx` state.
