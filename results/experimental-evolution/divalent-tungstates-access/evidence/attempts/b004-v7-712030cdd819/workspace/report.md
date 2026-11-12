# Powder XRD phase analysis

The pattern is described by three crystalline phases. Weight fractions are normalized only over these modeled crystalline phases:

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| Ba₃W₂O₉ | R -3 c | a = 10.13201, c = 13.96519 | 0.72456 (72.46 wt%) |
| monoclinic WO₃ | P 21/c | a = 7.69331, b = 7.53729, c = 10.52053, β = 136.08517 | 0.22788 (22.79 wt%) |
| BaCO₃ (witherite) | P m c n | a = 5.30496, b = 8.91362, c = 6.44809 | 0.04757 (4.76 wt%) |

## Evidence

The starting chemistry (WO₃ + BaCO₃, 800 °C) is consistent with a partially reacted mixture. Ba₃W₂O₉ accounts for the dominant reflection family, including peaks near 17.72, 26.21, 27.71, 30.78, 32.99, 37.62, 40.75, 42.96, 53.67 and 54.51° 2θ. Monoclinic WO₃ is identified particularly by its 23.35/23.82/24.62° triplet and the corresponding higher-angle family. After fitting those phases, a coherent residual family at approximately 19.70, 24.12/24.50, 34.8, 42.2, 44.4, 45.1 and 46.96° indexed to witherite BaCO₃; adding it reduced the pre-profile Rwp from about 6.74% to 4.80%. No coherent family remains unassigned, so no missing-topology substitution search was warranted.

Starting structures were COD 1533878 (Ba₃W₂O₉), 2311041 (WO₃), and 9010928 (BaCO₃). Cells, supported coordinates, scales, smooth background, polarization, phase broadening and supported March–Dollase terms were developed before the required bounded polish. The polish selected its converged all-coordinate branch after restoring bound-hit coordinates; its geometry audit found no catastrophic contacts. Independent read-only GSAS-II replay regenerated the full pattern from atomic structure factors with no optimized parameters and no profile-review flags.

The final statistics over all 8,301 points are Rwp = 2.836%, Rp = 2.140%, Rexp = 2.294%, goodness-of-fit = 1.236, and χ² = 12,621.05. The final project converged with maximum shift/esd = 0.071.

## Uncertainty and limitations

Formal covariance standard uncertainties on the fractions are approximately 0.00030, 0.00026 and 0.00024, respectively, but these understate model uncertainty from overlap, background, texture and profile correlations. A practical interpretation is roughly ±0.5–1 wt% for the major phases and about ±0.5 wt% for minor BaCO₃. The BaCO₃ phase and fraction are supported by several reflections, but its low abundance makes its individual atomic coordinates less precise than those of the major phases.

Specimen displacement was rejected because it was 99.91% correlated with zero offset. Surface roughness was also rejected because its two parameters were 99.6–99.97% correlated, start-dependent and bound-hitting. Joint polarization/Uiso refinement was 98.6% correlated and forced Uiso outside the supplied range, so the previously stable common-per-phase Uiso values were retained as fixed; the displacement parameters are not independently determined. Further profile refinement moved uphill and was rejected. Residual extrema coincide with accepted-phase reflections and are attributed to remaining profile/intensity imperfections rather than another phase.

Fractions exclude any amorphous material and cannot quantify it. The submitted `fit.csv`, CIFs and fractions all come from the same replay-verified `final.gpx` (SHA-256 `94f73786a26e5ee65448d9a6238d869b31042456a0fd90d28747ad7fab58480c`).
