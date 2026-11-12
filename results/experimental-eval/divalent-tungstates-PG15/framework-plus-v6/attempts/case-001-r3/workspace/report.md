# Powder XRD phase analysis

The modeled crystalline material is predominantly unreacted witherite BaCO3 and monoclinic WO3, with two trace Ba-W-O reaction products. Fractions are normalized over the modeled crystalline phases only; amorphous content is not measured by this normalization.

| Phase | Space group | Weight fraction | Formal scale-covariance sigma |
|---|---:|---:|---:|
| BaCO3 (witherite) | Pnma, 62 | 54.5500 wt% | 0.1580 wt% |
| WO3 (monoclinic) | P21/c, 14 | 44.9840 wt% | 0.1557 wt% |
| BaWO4 (scheelite) | I41/a, 88 | 0.2743 wt% | 0.0320 wt% |
| Ba3W2O9 | R-3c, 167 | 0.1917 wt% | 0.0352 wt% |

## Evidence and model choice

The BaCO3 model accounts for the coherent families at about 24.21, 28.04, 42.29, 45.17, and 47.08 degrees 2theta. Monoclinic WO3 accounts for the characteristic 23.43/23.91/24.65 degree group and the 33-35 degree families. Source-record comparisons rejected a high-temperature orthorhombic WO3 model and a triclinic record whose angles collapsed toward monoclinic symmetry; COD 2311041 gave the physically coherent monoclinic model.

BaWO4 contributes independent or partly overlapped families near 26.83, 43.34, 53.98-54.87, and 69.38 degrees. Its final scale is 8.6 sigma above zero and, with all other final parameters fixed, lowers weighted chi-square by 304. The exact old BaWO4 database entry had split half-occupied oxygen sites with a 1.17 A alternative-site contact, so it was not used. The submitted ordered scheelite model was built from the 290 K neutron PbWO4 parent COD 9009811 by the isovalent Pb-to-Ba substitution, then its cell and scale were refined. It has W-O = 1.836 A and O-O = 2.986 A. Ordered BaMoO4, SrWO4, and CaWO4 parents gave essentially the same phase scale, but their oxygen geometry was less suitable after transfer.

Ba3W2O9 is weaker but supported by families near 26.27, 40.86, 42.86, 53.63/54.72, and 63.04 degrees. Its scale is 5.4 sigma above zero and lowers weighted chi-square by 128. The strongest calculated line near 30.94 degrees is overpredicted, so this assignment is lower confidence than BaWO4. Ba3WO6 was rejected because improvement required several-percent cell/angle distortion, and the Ba0.15WO3 bronze refined to zero scale.

## Refinement and uncertainty

The final model uses the measured Cu Kalpha1/Kalpha2 wavelengths and ratio, a smooth 10-term Chebyshev-1 background, one zero correction, a nonnegative common U/W/X profile, and axial asymmetry. Supported main-phase terms are isotropic size for both main phases, isotropic strain for WO3, and modest BaCO3 [110] March-Dollase texture. Trace-phase size/strain terms were pruned: free sizes collapsed below 0.01 micrometre or a phase scale collapsed, while free strains exceeded 77,000 ppm. Their submitted fractions therefore use neutral fixed trace-phase broadening.

Fresh atomic replay of [final.gpx](final.gpx) over all 8,301 observations gives Rwp = 6.7642%, Rp = 5.1820%, and goodness of fit = 1.9469, with no physical replay flags. [fit.csv](fit.csv) is the replayed observed/calculated/difference profile; the four submitted CIFs are exact fresh exports from the project.

The main-phase identities and relative fractions are reliable within this model. The BaWO4 oxygen coordinates are prototype-derived rather than independently determined, and neither trace-phase broadening nor trace fraction is reliable at the formal-sigma level; systematic scale/profile uncertainty is larger. Ba3W2O9 should be treated as a probable trace assignment. Absolute phase fractions, including any amorphous material, cannot be determined from this refinement.
