# Crystalline phase analysis

The pattern is described by four crystalline phases. Weight fractions are normalized over these modeled crystalline phases; they do not measure any amorphous content.

| Phase | Space group | Weight fraction | Refined cell (Å, °) |
|---|---:|---:|---|
| PbWO4, scheelite-type (stolzite) | I41/a (88) | 0.5795 (57.95 wt%) | a = 5.47384, c = 12.07545 |
| WO3, room-temperature monoclinic | P21/c (14) | 0.2019 (20.19 wt%) | a = 7.70232, b = 7.54527, c = 10.53822, beta = 136.1929 |
| Pb3O4, minium | P42/mbc (135) | 0.1695 (16.95 wt%) | a = 8.81440, c = 6.56815 |
| PbO, massicot | Pbcm (57) | 0.0491 (4.91 wt%) | a = 5.88686, b = 5.49252, c = 4.75679 |

The high-beta WO3 cell is the alternate setting used by the selected P21/c source structure, not a different polymorph.

## Evidence

The phase inventory is chemically consistent with partial reaction of the reported WO3 and Pb3O4 precursors at 500 °C. Scheelite PbWO4 accounts for the dominant families at approximately 27.81, 30.03, 33.15, 45.12, 47.37, and 55.61° 2theta. Monoclinic WO3 is required by its characteristic 23.54/24.02/24.84° triplet and families near 34.05–34.63, 47.63–50.43, and 55.87–56.50°. Residual precursor Pb3O4 has coherent diagnostic lines at 14.66, 26.81, 31.21, 32.55, and 52.51°. Massicot PbO is supported by several partly isolated families, including 15.50, 29.54, 30.80, 38.26, 45.58, 49.67, and 53.59°; removing it leaves the same-sign residual sequence at those positions.

Physical alternate structures were challenged under the same common profile. Raspite PbWO4, PbO2, and an isovalent Pb2MoO5-derived Pb2WO5 prototype refined to zero scale. Triclinic WO3 and alternate Pb3O4 records fit worse than the selected structures. Litharge PbO reached only 0.03 wt%. A U6+→W6+ Pb3WO6 analogue reached 0.18 wt% with unstable cell release. A 67-atom W18O49 trial absorbed 0.47 wt% but improved Rwp by only 0.006 percentage point after four cell variables; no reducing condition was reported, and the dense reflection set did not provide a defensible unique-family assignment. These candidates were therefore not retained.

## Refinement and uncertainty

The final dual-Cu-Kalpha GSAS-II refinement used a smooth six-coefficient Chebyshev background, one zero correction (+0.46029°), a nonnegative common width term, and one axial-asymmetry term. Roughness and preferred orientation were tested and returned to neutral. Only replay-stable isotropic size/strain terms were retained; atomic coordinates and displacement parameters were held at the source-structure values while cells, scales, background, and accepted profile terms were refined.

The reopened full-range replay converged without SVD truncation: Rwp = 2.8471%, Rp = 2.1897%, Rexp = 2.4864%, goodness of fit = 1.1471, with 8,284 observations and 29 refined variables. Low-, middle-, and high-angle isolated families have consistent positions, widths, and asymmetry; the remaining difference profile is small but correlated (Durbin–Watson = 1.575), so the counting-statistical formal errors in `result.json` are optimistic.

Practical phase-fraction uncertainty is dominated by profile/background overlap and the lack of a calibrated instrumental profile. About 1–2 wt% absolute is a more realistic systematic scale for the three major phases; the 4.91 wt% PbO fraction is the least robust and should be read to roughly ±1 wt%. The phase identities and space groups are well supported, but the powder data do not independently determine detailed atomic coordinates or subtle disorder. Unmodeled crystalline components below roughly 0.5–1 wt% cannot be excluded reliably.
