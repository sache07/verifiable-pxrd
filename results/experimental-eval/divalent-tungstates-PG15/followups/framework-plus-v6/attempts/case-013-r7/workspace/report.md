# Powder XRD phase analysis

The 500 °C PbO–WO3 product is modeled with eight crystalline phases. Weight fractions are normalized to the modeled crystalline material; without an internal standard, amorphous material cannot be quantified.

| Phase | Space group | Crystalline weight fraction |
|---|---:|---:|
| PbWO4, stolzite/scheelite type | I 41/a (88) | 56.25% |
| Pb2WO5 | C 2/m (12) | 13.22% |
| PbO, massicot | P b c m (57) | 7.25% |
| WO3, monoclinic | P 21/c (14) | 8.70% |
| alpha-PbO2 | P b c n (60) | 0.91% |
| Pb3WO6 | P n m a (62) | 7.74% |
| Pb3O4, orthorhombic | P b a m (55) | 0.76% |
| PbO, long-period alpha-PbO approximant | P b c m (57) | 5.17% |

## Evidence

PbWO4 accounts for the dominant pattern. The inventory was expanded only when coherent residual families remained after reconverging the common background, scales, angular correction, cells, and profile. Massicot PbO accounts for families near 29.33, 30.61, 38.11, 53.36, 56.30, and 63.28° 2theta; monoclinic WO3 accounts especially for the 23.36/23.89/24.65° triplet. Pb2WO5 is supported by partly unique families around 25.9, 29.4, 30.7–31.2, 39.5, 42.0–43.5, 52.2, and 59.8°.

The initially selected conventional massicot record could reproduce its principal peaks only by driving both size and strain to opposite physical bounds. Re-screening all PbO records identified COD 1533609, a 44.9 Å commensurate approximant to incommensurate alpha-PbO. At positive scale it explains repeated superlattice-sensitive families near 28.93, 32.06–32.18, 36.06, 45.90, 48.85–48.93, 54.94–55.09, 60.22, and 66.6–66.9°, and lowered Rwp by about 0.6 percentage point before bounded cell/coordinate refinement. Both PbO models remain necessary under the final common profile.

No exact database entries were available for two tungstates. Pb2WO5 was built from the isovalent MoPb2O5 C2/m prototype (COD 7220560, Mo6+ to W6+), and Pb3WO6 from the U(PbO2)3 Pnma prototype (COD 2310493, U6+ to W6+). Pb3WO6 removes coherent groups at 28.9–30.2, 44.36/45.97, 53.65/55.05, 59.43, and 78.05°. The much weaker alpha-PbO2 and orthorhombic Pb3O4 models each worsen the reconverged fit when removed and retain support from several partly resolved families, but their assignments are tentative. Raspite PbWO4, a duplicate PbWO4 record, Pb2O3, litharge PbO, and tetragonal Pb3O4 refined to negligible or unstable scale or failed to reproduce those families under the same nuisance model.

## Refinement and verification

The refinement used the reported Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio over the complete 10.009–99.994° scan. The accepted baseline has a smooth positive ten-term Chebyshev background, one zero correction, nonnegative U/W/X terms, axial asymmetry, and polarization. One in-range isotropic strain term (2576 ppm) was retained for Pb3WO6. Axis challenges retained March–Dollase corrections for Pb2WO5 [100], massicot PbO [100], Pb3WO6 [100], and long-period PbO [010]; the last three were fixed at the stated physical trial limits after unconstrained refinements crossed them. Unsupported strain, roughness, other texture axes, and alternative width terms were pruned. Atomic shifts were projected into restrained local neighborhoods, and cells were frozen after convergence to prevent a reflection-list discontinuity.

The final project was saved, reopened, and reconverged to a maximum shift/esd of 0.017. An independent native GSAS-II forward replay, with no optimization, regenerated the complete profile on all 8,282 observations. It exactly reproduces the exported fractions and gives Rwp = 9.0586%, Rp = 6.4117%, chi-squared = 55,428.79, and GOF = 2.5906 for 23 refined parameters. The replay reports no physical-profile flags, all eight CIFs pass the occupancy/contact screen, and `fit.csv` comes from the fresh replay rather than cached calculated intensities.

## Remaining uncertainty

Pb2WO5 and Pb3WO6 are physically screened, profile-supported substituted prototypes, not unique structure determinations; their detailed oxygen geometries are only weakly constrained. The long-period PbO model is likewise a commensurate approximant and does not determine the true modulation. Alpha-PbO2 (0.91%) and orthorhombic Pb3O4 (0.76%) are the least secure identifications and their fractions are only semiquantitative because most of their intensity overlaps stronger phases. Exact fractions of massicot PbO, Pb3WO6, and long-period PbO are correlated with preferred orientation.

Instrument U and X reached the allowed upper limits, and several minor-phase size descriptors reached the 0.04 micrometre lower limit. Reversible width challenges were therefore used for model selection only; those crystallite sizes should not be interpreted physically. Bound profile/texture terms, extensive overlap, and prototype substitution make covariance-only fraction errors misleading. The table gives the best normalized crystalline estimates, but its final digits are not a statement of accuracy, and absolute phase fractions including amorphous content cannot be determined from this scan.
