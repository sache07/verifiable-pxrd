# Powder X-ray diffraction phase analysis

## Result

The specimen contains two resolved crystalline phases. Fractions below are normalized over those modeled crystalline phases; they do not measure amorphous content.

| Phase | Structural model | Weight fraction | Statistical s.u. | Estimated model uncertainty |
|---|---|---:|---:|---:|
| CoWO4 | wolframite, P2/c | 0.30758 (30.76 wt%) | 0.00108 (0.11 percentage point) | about 0.015 (1.5 percentage points) |
| WO3 | monoclinic, P21/c | 0.69242 (69.24 wt%) | 0.00108 (0.11 percentage point) | about 0.015 (1.5 percentage points) |

The final full-grid fit has Rwp = 5.2573%, Rp = 4.1345%, Rexp = 3.2802%, and goodness-of-fit chi-square = 2.5687. Refined cells are a = 4.67090, b = 5.68569, c = 4.95198 A, beta = 90.0229 degrees for CoWO4, and a = 7.69604, b = 7.53910, c = 10.54010 A, beta = 136.1005 degrees for the selected P21/c setting of WO3.

## Evidence and model selection

The monoclinic WO3 model accounts for the characteristic split families at 23.181/23.666/24.422 degrees 2theta, 33.330/34.125/34.229 degrees, and 41.511/41.915 degrees. The wolframite CoWO4 model independently accounts for reflections at 19.068, 23.893, 24.730, 30.706/30.715, 31.527, 36.336/36.496, 41.465, 52.116, and 54.120/54.132 degrees. Together these phases account for all coherent reflection families over 9.90-100.09 degrees.

The WO3 starting structure was frozen-index COD 2311041. No exact CoWO4 entry was present in the supplied frozen reference index, so the chemically appropriate wolframite topology was generated from ZnWO4 COD 1520641 by Zn-to-Co substitution and then refined. Alternative wolframite analogues and WO3 references were screened; the submitted pair gave the best combination of whole-pattern agreement and physical geometry. CoO and Co3O4 precursor/product checks were not accepted: CoO refined to only 0.23 wt% with a scale uncertainty of comparable size and negligible fit improvement, while Co3O4 refined to a negative scale. Neither supplied a broad residual-reflection family.

Refinement proceeded through scale/background, cells and zero offset, heavy-atom coordinates, bounded oxygen-coordinate starts, then phase sizes and supported specimen/profile terms. The final models give Co-O = 2.032-2.173 A, CoWO4 W-O = 1.826-2.135 A, and WO3 W-O = 1.739-2.200 A; the shortest O-O contacts are 2.491 and 2.542 A. These checks support physical octahedral geometries.

## Uncertainty and reproducibility

The statistical fraction uncertainty is smaller than realistic model uncertainty. The latter was estimated conservatively from the spread among accepted physical profile/structure checkpoints and includes preferred-orientation, roughness, and line-broadening correlations. Trace CoO at the level tested cannot be determined reliably and is therefore not reported as a phase. A trace crystalline impurity below the pattern's practical sensitivity, or amorphous material, cannot be excluded.

The phase identities, topologies, cells, and relative crystalline fractions are well constrained. Fine oxygen shifts are less strongly constrained than Co/W positions, and absolute WO3 atomic displacement parameters could not be refined reliably; they remain fixed at the source-model value and should not be interpreted physically.

As a final validation, `final.gpx` was replayed from saved atoms and profile parameters with cached calculated intensities ignored. It regenerated all reflections over the original 8,301-point grid, reproduced Rwp = 5.2573% and both fractions exactly, and produced no profile-review flags. The replay-exported CIFs were byte-identical to the submitted CIFs.
