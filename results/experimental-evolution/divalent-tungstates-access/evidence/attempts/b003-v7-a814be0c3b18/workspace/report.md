# Powder XRD phase analysis

## Result

The crystalline pattern is accounted for by three phases. Weight fractions are normalized over these modeled crystalline phases; no amorphous fraction was determined.

| Phase | Structural model | Refined cell | Weight fraction |
|---|---|---|---:|
| MnWO4, wolframite | COD 1520200; P 2/c (No. 13) | a = 4.79570 Å, b = 5.70670 Å, c = 4.97430 Å, beta = 91.1638° | 0.63573 (63.57 wt%) |
| WO3 | COD 2311041; P 21/c (No. 14) | a = 7.68510 Å, b = 7.52723 Å, c = 10.52073 Å, beta = 136.1701° | 0.17941 (17.94 wt%) |
| Mn3WO6 | COD 2002703; R -3 (No. 148) | a = 8.88816 Å, c = 10.48088 Å | 0.18486 (18.49 wt%) |

The independently regenerated full-grid profile has Rwp = 3.05445%, Rp = 2.24284%, and weighted residual sum 38070.03 for 8301 points, using weights 1/max(Iobs,1). The saved GSAS-II Rwp is 3.05445%. Read-only replay returned no profile-review flags and did not change `final.gpx`.

## Evidence and model selection

The dominant wolframite MnWO4 family accounts for the reflections near 18.28°, 23.41°, 29.78°, and 30.23° 2theta and their higher-angle partners. Monoclinic WO3 accounts for the dense 22.8–24.2° region and its 28–34° and higher-angle families. A third coherent family at approximately 19.76/20.32°, 28.5°, 45.8/46.4°, and 54–56° is consistently indexed by rhombohedral Mn3WO6. No coherent reflection family remains that requires a fourth crystalline phase.

Two symmetry-distinct exact-composition WO3 parents were developed to the same checkpoint. COD 2311041 (P 21/c) converged at Rwp 3.457%, compared with 3.639% for COD 1528915 (P 21/n), and remained the better physical basin after texture/profile development. The rejected parent was not selected from an early substitution count or an unconverged coordinate fit.

The final fractions also satisfy the synthesis context: converting the three mass fractions to formula amounts gives Mn:W approximately 1.02:1, close to the stated 1:1 metal feed. Every retained phase has positive scale and multiple supporting reflections.

## Refinement controls and uncertainty

The accepted specimen displacement is +425.3 micrometres. Joint zero/displacement refinement was rejected because the two corrections were 99.99% correlated and both reached limits; zero was restored to 0°. Instrumental W refined stably to 12.975, while X was restored to 1.5 because refining it produced 98.4% correlation with MnWO4 crystallite size. Surface-roughness A/B were rejected after 100% correlation and lower-bound pinning. Microstrain was unsupported and removed. Stable March–Dollase terms were retained for MnWO4 [111] (1.1679), WO3 [010] (1.3522), and Mn3WO6 [001] (0.9270).

The supplied bounded polish selected its converged all-coordinate branch over the heavy/light branch; the phasewise branch was explicitly rejected for coordinate nonconvergence. Bound-hit sites were returned to their starting coordinates. Final maximum coordinate changes from the physical checkpoint were 0.080 Å (MnWO4), 0.061 Å (WO3), and 0.012 Å (Mn3WO6), with no GSAS short contacts; exported minimum interatomic distances are 1.793, 1.748, and 1.903 Å, respectively.

Phase presence and topology are reliable. Exact fractions have systematic uncertainty from peak overlap, preferred orientation, broad Mn3WO6 reflections, and the absence of supplied pointwise standard uncertainties or an internal standard; a defensible numerical fraction uncertainty cannot be obtained from this scan alone. The remaining difference intensity is concentrated on accepted reflections, especially the strongest low-angle peaks, so it is more consistent with residual structure-factor/profile limitations than with an unmodeled crystalline phase. WO3 oxygen-coordinate refinement repeatedly sought bounds and was rolled back; its topology and cell are supported, but detailed oxygen positions should not be interpreted as a high-precision single-crystal determination.
