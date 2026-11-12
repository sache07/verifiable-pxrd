# PXRD phase analysis and refinement report

## Result

Four crystalline phases are required. Weight fractions are normalized only over these modeled crystalline phases.

| Phase | Space group | Weight fraction | Formal ESD |
|---|---:|---:|---:|
| PbWO4, scheelite | I41/a (88) | 58.59 wt% | 0.13 wt% |
| WO3, monoclinic | P21/c (14) | 19.77 wt% | 0.09 wt% |
| Pb3O4, minium | P42/mbc (135) | 17.04 wt% | 0.12 wt% |
| PbO, massicot | Pbcm (57) | 4.60 wt% | 0.07 wt% |

The final fit over 10.001–100.008° 2theta has Rp = 2.421%, Rwp = 3.149%, Rexp = 2.486%, and goodness of fit = 1.269 (8,284 observations and 34 variables). These values, fractions, CIFs, and `fit.csv` were all reloaded and exported from `final.gpx`.

## Evidence for the phase inventory

The dominant PbWO4 phase is the ordered, fully occupied scheelite structure from COD 9009811, measured on a synthetic room-temperature specimen. Its 27.8° (112), 30.0° (004), 33.1° (200), 45.1° (204), and higher-angle families account for the dominant pattern. Refined cell dimensions are about a = 5.4660 and c = 12.0580 A; W–O is 1.775 A for the tetrahedral first shell and Pb–O is 2.612–2.655 A. Raspite (COD 9007617) gave Rwp about 25.0% versus 16.0% for scheelite under the same modest fixed-profile comparison and failed the 24.5–25.5° diagnostics. Partially disordered Pb7W8O28.8 (COD 9016035) did not improve that comparison and predicts absent low-angle peaks.

Monoclinic WO3 is fixed by the resolved 23.52/24.01/24.83° triplet and the 33–35° splitting. COD 2311041 is fully occupied and has a physically sound distorted WO6 network (W–O 1.714–2.158 A after cell refinement). An older monoclinic record contained implausible approximately 2.9 A first-shell W–O contacts; triclinic and orthorhombic records also fit worse under the same nuisance model (Rwp about 16.7% and 16.9%, respectively, versus 16.0% for this monoclinic model).

Pb3O4 (COD 9012124) is ordered and fully occupied; its distinctive approximately 14.7°, 26.8°, 31.2°, 32.5°, and 52.5° families are present. Minor orthorhombic massicot PbO (COD 2310433) is supported by the approximately 15.6°, 29.6°, and 38.3° reflections. Adding massicot lowered the inventory-stage Rwp from about 16.28% to 16.05%; removing it after broadening caused coherent residuals. Litharge was tested with a corrected standard origin and refined to zero scale after full reconvergence.

The inventory is chemically consistent with PbWO4 formation plus residual WO3/Pb3O4 and partial Pb3O4-to-PbO conversion at 500 °C. Cross-chemistry searches were also made where no compelling exact product entry was present. Ordered Pb2WO5 was built by the chemically direct Mo-to-W substitution in Pb2MoO5 (COD 7220560), and Pb3WO6 by U-to-W substitution in Pb3UO6 (COD 2310493). Both adapted models passed basic geometry screening, but Pb2WO5 refined to zero scale. Pb3WO6 gave at most a transient sub-0.5 wt% overlapping contribution and also went to zero when one supported size term was released. Neither has an independent peak family here, so neither is reported.

## Profile model and uncertainty

Cu Kalpha1/Kalpha2 wavelengths and the reported 0.5 intensity ratio were used directly. Because point uncertainties were not supplied, counting-statistical weights were used. A 12-term Chebyshev background remained positive over the fit range. Specimen displacement was selected instead of zero because its angular dependence fit substantially better under the same four-phase profile (Rwp 5.92% versus 8.02%); zero and displacement were never refined together. The final displacement is -0.730 mm on the 200 mm GSAS-II radius.

The supported common width terms are U = 59.11, V = 0, W = 5.96, and X = 4.67 in GSAS-II profile units. The Gaussian variance is positive throughout the fitted range (minimum 6.41). Isotropic size terms refine to approximately 62 nm for PbWO4, 34 nm for Pb3O4, and 53 nm for massicot; WO3 is left at the neutral 10 micrometre value. Every unused microstrain term is zero, and no preferred orientation, anisotropic broadening, or frozen variable remains. A scheelite displacement-factor trial ran to its zero bound and was rejected. The unknown effective polarization instead improved all four phase fits and refined to the physical upper limit; it was therefore fixed at 1.0 in the final project. This likely represents the combined instrument-optics intensity response, not an independently calibrated polarization measurement.

The structures and presence of all four phases are reliable, including minor massicot. The formal fraction ESDs above are not realistic total uncertainties: the uncalibrated profile, polarization at its physical limit, large displacement correction, possible Pb/W microabsorption, fixed literature atomic coordinates, and peak overlap dominate. Sensitivity trials indicate roughly 1–2 wt% absolute uncertainty for each major phase and about 0.5 wt% for PbO is more defensible than the formal ESDs. No amorphous fraction can be determined without an internal standard, so the values must not be interpreted as whole-sample absolute crystallinity.
