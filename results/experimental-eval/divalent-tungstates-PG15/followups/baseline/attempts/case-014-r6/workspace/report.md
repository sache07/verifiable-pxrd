# PXRD phase analysis and Rietveld refinement

## Result

Three crystalline phases were required. Weight fractions are normalized only over these modeled crystalline phases.

| Phase | Structural model | Refined cell (Å, °) | Weight fraction | Formal 1σ |
|---|---|---|---:|---:|
| SrWO4 | scheelite, I 41/a | a = 5.423930, c = 11.971671 | 79.76 wt% | 0.26 wt% |
| WO3 | monoclinic, P 21/n | a = 7.309064, b = 7.547169, c = 7.703147, β = 90.80159 | 12.38 wt% | 0.18 wt% |
| Sr3WO6 | ordered double-perovskite working model, P 21/n | a = 6.076316, b = 5.542786, c = 8.344259, β = 89.54593 | 7.86 wt% | 0.20 wt% |

The final fit statistics are Rwp = 12.533%, Rp = 8.586%, Rexp = 3.536%, and GOF = 3.553 (8270 observations, 36 refined variables). The last maximum shift/standard uncertainty was 0.010. Phase R(F) values are 5.47% for SrWO4, 15.95% for WO3, and 22.90% for Sr3WO6.

## Evidence

Scheelite SrWO4 accounts for the dominant pattern, including the strong lines near 18.32, 28.00, 30.22, 33.39, 38.23, 45.45, 47.75, 51.98, 56.08, and 57.34° 2θ and the corresponding high-angle sequence. The refined I 41/a metric is internally consistent across the full measured range.

Monoclinic WO3 is identified particularly by the resolved 23.45/23.97/24.73° group and its higher-angle splitting. P 21/n gave a better whole-pattern fit than the tested triclinic, orthorhombic, tetragonal, and alternative monoclinic WO3 models.

After those two phases were fitted, a coherent residual series remained near 22.09, 29.75, 30.90, 32.63, 44.67, 56.99, and 67.04° 2θ. It indexes to a monoclinic double-perovskite cell and is chemically consistent with Sr3WO6 in the SrO-WO3 system. Sr3W2O9, SrCO3, SrO, and monoclinic SrWO4 alternatives did not account for this series comparably. The unusually strong 200 line at 29.75° required a March-Dollase [100] preferred-orientation correction for Sr3WO6 (ratio 0.4689), physically plausible for the measured reflection specimen.

## Refinement and limitations

GSAS-II modeled Cu Kα1/Kα2 radiation at 1.540598/1.544426 Å with the reported 0.5 intensity ratio over 10.05–99.90° 2θ. Refined terms included phase scales and unit cells, zero and common U/V/W/X profile terms, a 15-term Chebyshev background, Suortti surface roughness, and the Sr3WO6 texture term. Because pointwise uncertainties were not supplied, sqrt(counts) uncertainties were used. The U and V profile terms remain strongly correlated (98.1%), so those individual profile coefficients should not be interpreted physically.

SrWO4 and WO3 atomic coordinates were retained from reference structures while their cells were refined. No exact Sr3WO6 reference was available in the local structure collection: its CIF is a working P 21/n model made by replacing Ca with Sr in isostructural Sr2CaWO6, followed by cell and intensity refinement. The phase identity and lattice are supported, but the Sr3WO6 atomic coordinates are not independently determined by this pattern; that structure should not be treated as a definitive coordinate-level solution.

The tabulated fraction uncertainties are covariance-derived formal errors and are too optimistic. Surface roughness, microabsorption, preferred orientation, the assumed intensity errors, and the analogue-based Sr3WO6 model are not included. In particular, the Sr3WO6 amount is best regarded as approximately 8 wt% with roughly 2–3 wt% systematic uncertainty; plausible texture variants placed it in the approximate 6–11 wt% range. SrWO4 and WO3 were correspondingly stable near 78–81 and 12–13 wt%. With no internal standard, amorphous content cannot be measured, so these are not absolute bulk fractions.

The submitted CIFs, `fit.csv`, and fractions were exported from `final.gpx` after the final converged refinement.
