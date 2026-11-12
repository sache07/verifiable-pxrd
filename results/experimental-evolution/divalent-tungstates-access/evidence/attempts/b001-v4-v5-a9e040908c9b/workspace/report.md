# Powder XRD phase analysis

The pattern is described by four crystalline phases: triclinic CuWO4 and WO3, cubic Cu3WO6, and minor monoclinic CuO. The normalized crystalline fractions are 64.13, 20.28, 13.12, and 2.48 wt%, respectively. The full-grid GSAS-II forward replay gives Rwp = 3.1435%, Rp = 2.3691%, Rexp = 1.6163%, and goodness of fit = 1.9449.

| Phase | Space group | Crystalline wt% | Main evidence |
|---|---:|---:|---|
| CuWO4 | P -1 | 64.13 | Accounts for the dominant low-symmetry tungstate reflections; the alternative high-pressure P2/c topology did not index or fit the full pattern comparably. |
| WO3 | P -1 | 20.28 | Accounts for the split low-symmetry WO3 families. In like-for-like four-phase refinements, this triclinic topology fit substantially better than the closest monoclinic and orthorhombic WO3 alternatives. |
| Cu3WO6 | P a -3 | 13.12 | Its (111), (210), and subsequent cubic reflections explain the formerly coherent residual family at approximately 15.18, 19.78, 32.50, 33.77, and 57.60 degrees 2theta. |
| CuO | C 2/c | 2.48 | Weak but stable scale from its characteristic reflection set, including the approximately 32.05 and 35.07/35.08 degree region, consistent with residual precursor. |

The Cu K-alpha1/K-alpha2 doublet and reported 0.5 intensity ratio were modeled over the complete 9.90-100.09 degree scan. Refinement included phase scales and cells, background, specimen displacement/angular calibration, polarization, heavy-atom coordinates, and only the supported profile broadening terms. One uniaxial microstrain family was retained for each of CuWO4 and WO3. Texture and surface-roughness trials were unsupported. All coherent peak families are assigned in the final model, and independent regeneration from `final.gpx` reproduces `fit.csv` to numerical precision.

The structures pass a bond-geometry screen: for example, CuWO4 has W-O = 1.78-2.15 A and Cu-O = 1.93-2.37 A, while Cu3WO6 has W-O = 1.78-2.10 A and Cu-O = 1.91-2.20 A. Unconstrained oxygen-coordinate refinement gave shorter, chemically impossible W-O contacts and was therefore rolled back; oxygen coordinates and weakly determined displacement parameters remain reference-model values rather than independently determined results. The formal scale-covariance uncertainties are only 0.02-0.04 wt% and underestimate model systematics. Practical uncertainty is closer to roughly 1-2 wt% absolute for the major phases and about 0.5 wt% for CuO; thus CuO's presence is supported, but its 2.48 wt% abundance is the least secure fraction.
