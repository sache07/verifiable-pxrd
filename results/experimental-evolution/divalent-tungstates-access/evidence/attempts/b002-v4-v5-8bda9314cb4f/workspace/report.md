# Powder XRD phase analysis

The crystalline specimen is modeled as wolframite-type ZnWO4, monoclinic WO3, and minor wurtzite ZnO. Weight fractions are normalized over these modeled crystalline phases; amorphous material, if present, is not quantified.

| Phase | Space group | Weight fraction | Refined cell |
|---|---:|---:|---|
| ZnWO4 | P 2/c | 0.8431 (84.31 wt%) | a = 4.70143, b = 5.73337, c = 4.93228 A; beta = 90.6355 deg |
| WO3 | P 21/c | 0.1073 (10.73 wt%) | a = 7.70421, b = 7.52053, c = 10.53617 A; beta = 136.0710 deg |
| ZnO | P 63 m c | 0.04969 (4.97 wt%) | a = 3.25529, c = 5.18251 A |

## Evidence

The dominant family at approximately 15.78, 19.21, 24.11/24.79, 30.76/30.98, and 31.49 degrees 2theta is indexed by monoclinic wolframite ZnWO4. The chemically expected Zn-W-O product and the full reflection family support this assignment. Because the frozen reference index contains no exact-composition ZnWO4 entry, its P 2/c framework was transferred from a physical wolframite CoWO4 reference, Zn was substituted, and the cell and coordinates were refined with tight geometry bounds.

The residual family at 23.41, 27.00, 28.9-29.2, 33.60/34.49, 42.20, 44.85-45.70, and 47.47 degrees is indexed by P 21/c WO3. The submitted coordinates are from the physical exact-composition COD 2311041 model; attempts to refine its W coordinates were unstable and were rolled back. The unusual beta angle is the intact reference-cell setting, not a distorted local structure. Removing WO3 from the final model increases Rwp to 14.73%.

ZnO is supported by the coherent family at 32.05, 34.93, 36.60, 47.9, 56.81, 63.39, and 68.26 degrees. It uses the wurtzite COD 9004178 topology. Omitting ZnO from the final checkpoint and re-refining the other phases raises Rwp from 5.33% to 6.64% and leaves these peaks as positive residuals, so the approximately 5 wt% fraction is not an overlap artifact.

Relative intensities require moderate preferred orientation: March-Dollase coefficients are 0.712 for ZnWO4 [111] and 1.118 for WO3 [100]. Competing texture axes were tested and were distinctly worse. Every coherent reflection family is assigned to an accepted phase; the remaining residuals occur at their indexed peaks and reflect imperfect intensity/profile modeling rather than evidence for another phase.

## Fit quality and uncertainty

Fresh, read-only GSAS-II replay over all 8,301 observations gives Rwp = 5.3315%, Rp = 4.2372%, and goodness of fit = 2.0184. The final cycle converged with maximum shift/esd = 0.0041, and replay reported no negative-width, negative-background, or displacement-parameter warnings. The exported structures pass contact screening; representative metal-O ranges are 1.83-2.18 A (W-O) and 1.96-2.20 A (Zn-O) in ZnWO4, 1.71-2.16 A in WO3, and 1.976-1.980 A in ZnO.

Formal covariance-only standard uncertainties in the fractions are 0.10, 0.052, and 0.096 percentage points for ZnWO4, WO3, and ZnO, respectively. Texture, reference-model, and profile correlations are larger systematic effects, so reporting 84.3, 10.7, and 5.0 wt% is more realistic. The phase identities, topologies, and fractions are reliable at that precision. Exact oxygen coordinates are not independently reliable from this laboratory X-ray pattern: two ZnWO4 oxygen coordinates reached tight physical bounds, and the WO3 oxygen framework was retained from its reference. The CIFs should therefore be interpreted as physical Rietveld models, not unique high-precision light-atom determinations.

The submitted `final.gpx` is the converged project used for the CIFs, fractions, and `fit.csv`; a separate forward replay regenerated its profile without optimization and left the project unchanged.
