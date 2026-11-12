# PXRD phase analysis

## Result

| Retained crystalline phase | Structural model | Weight fraction |
|---|---|---:|
| Scheelite CaWO4 | I 41/a (No. 88) | 75.61 wt% |
| Monoclinic WO3 | P 21/c (No. 14) | 12.86 wt% |
| Ca3WO6-type double perovskite | P 21/n (No. 14), analogue-derived | 11.53 wt% |

The fractions are normalized only over the retained crystalline phases. Without an external standard, amorphous content and absolute crystalline yield cannot be determined.

## Evidence and model selection

The metadata identify CaO and WO3 precursors fired at 850 °C and a reflection-mode Cu K-alpha measurement. The refinement therefore used the reported K-alpha1/K-alpha2 wavelengths and 0.5 doublet ratio. Because no pointwise uncertainties were supplied, the weights use the counting-statistics approximation sigma = sqrt(counts).

Scheelite CaWO4 is identified by its coherent low-, middle-, and high-angle families, including the observed peaks near 18.43, 28.54, 31.27, 34.01, 46.93, 54.12, and 57.71 degrees 2-theta. The selected 298 K COD 7219229 structure is fully occupied and gives plausible final W-O (1.763 A) and Ca-O (2.470-2.473 A) distances. A high-pressure fergusonite record failed its diagnostic-reflection comparison.

The residual WO3 families require the room-temperature monoclinic phase. In particular, the splitting near 22.95/23.42/24.23 degrees and further middle-angle multiplets are represented better by the P 21/c neutron structure (COD 2311041) than by orthorhombic Pnma, the older P 21/n coordinates, or triclinic P -1. In the final physical-profile replay, replacing it with triclinic WO3 increased Rwp from about 5.62% to 5.71-5.72%. Its distorted final WO6 geometry (W-O about 1.71-2.16 A) is chemically reasonable.

No exact Ca3WO6 entry was present in the supplied index. `learned/stoichiometric_analogues.py` identified Ca3OsO6 (COD 1562666) as the best screened ordered double-perovskite parent; isovalent Os6+ was replaced by W6+, followed by scale and cell refinement. This model accounts for otherwise unexplained families near 19.29, 22.02, 30.72, 32.16, 36.60-37.53, 45.24, 49.83, 55.22, and 57.05 degrees. The final W-O distances are 1.924-1.939 A. A lower-symmetry Ca3UO6-derived P 21 alternative was slightly worse after the final profile and texture corrections.

## Refinement quality and uncertainty

The final full-range GSAS-II replay gives Rwp = 5.621%, Rp = 3.847%, and GOF = 2.502 over 8301 points. The final project has no bound-frozen variables; its largest absolute parameter correlation is 0.882. A zero-only angular correction was retained because specimen-displacement branches required an uncalibrated 0.25-0.33 mm offset and less plausible cells. The physical profile uses a positive common U/W/X model, refined polarization, a smooth positive eight-term background, CaWO4 isotropic size broadening (0.253(7) micrometres), and CaWO4 [110] March-Dollase texture (1.2542(26)). Roughness and all phase strain terms failed bound/replay tests.

The formal GSAS-II fraction uncertainties are approximately 0.10, 0.06, and 0.08 percentage point for CaWO4, WO3, and Ca3WO6, respectively, but they omit structural-model and preferred-orientation uncertainty. The Ca3WO6 topology and lattice are well supported, while its exact atomic coordinates and even the subtle P 21/n versus lower-symmetry description cannot be determined uniquely from this mixed powder pattern; its fraction should therefore be regarded as model-dependent.

CaO was repeatedly re-challenged after the physical profile was fixed. It refined to only about 0.13 +/- 0.10 wt%, lacked a resolved unique reflection, and improved Rwp by only about 0.004 percentage point, so neither its presence nor fraction is reliable and it is not included. The calcium tungsten bronze candidate returned to zero scale and its predicted strong 16.1-degree line is absent. GOF above one and a Durbin-Watson statistic of 0.331 show that correlated systematic residuals remain, especially around intense overlapping low-angle peaks.
