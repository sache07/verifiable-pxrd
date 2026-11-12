# Powder XRD phase analysis

## Result

The modeled crystalline material is single-phase **MnWO4, wolframite type** (monoclinic `P 2/c`, No. 13). Its weight fraction is **1.000 (100 wt%) after normalization over the modeled crystalline phases**. This is not an absolute crystallinity measurement: an amorphous fraction or a crystalline impurity below the pattern's detection sensitivity cannot be quantified without an internal standard.

The refined cell is `a = 4.829548(146) A`, `b = 5.755675(178) A`, `c = 4.995100(159) A`, `beta = 91.21771(104) deg`, and `V = 138.81898 A^3`. Formal standard uncertainties are conditional on the chosen calibration model.

## Evidence and model selection

The Mn-W-O reference index contains an exact-composition wolframite MnWO4 model (COD 1520200) and Mn3WO6 (COD 2002703). The wolframite model accounts for the complete observed reflection family, including the diagnostic low-angle lines near 15.67 and 18.63 deg 2theta and the dense higher-angle sequence. Mn3WO6 predicts strong lines near 19.95, 20.49, 28.75, and 35.24 deg that are absent. Separate Mn3O4, Mn oxides, or WO3 precursor phases did not form coherent residual families. After the full MnWO4 refinement, the remaining maxima are shoulders or intensity residuals at MnWO4 reflections rather than an independently indexable family, so phase searching was stopped.

COD 1520200 supplied the topology only; its reported high-pressure cell and all atomic parameters used here were refined against this specimen. The final geometry remains chemically ordinary: six Mn-O distances span about 2.120-2.315 A and six W-O distances span about 1.762-2.127 A. All occupancies are unity and all refined isotropic displacement parameters are positive (`Uiso`: Mn 0.0092, W 0.0059, O1 0.0062, O2 0.0135 A^2). A very weak, reproducible March-Dollase [100] term refined to 1.00708; no microstrain term was retained because the apparent gains were unstable or boundary-limited.

## Fit and uncertainty

The replayed atomic GSAS-II model gives `Rwp = 4.9536%`, `Rp = 3.7257%`, `chi-square = 17009.22`, and `GOF = 1.4346` on all 8301 measured points. The Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio from the metadata were fixed. The final project passed an independent no-refinement forward replay with no negative-width, negative-background, displacement-parameter, or scale flags.

Zero offset and reflection-geometry specimen displacement were highly correlated when varied together. The final stable checkpoint fixes the jointly converged displacement at -625.8 micrometres and refines the zero offset to -0.10952 deg. Consequently, the space group, phase identity, and relative crystalline fraction are reliable, but the quoted cell standard uncertainties do not include the larger systematic uncertainty from that calibration correlation. Oxygen coordinates are also less precise than the heavy-atom framework in this X-ray pattern.
