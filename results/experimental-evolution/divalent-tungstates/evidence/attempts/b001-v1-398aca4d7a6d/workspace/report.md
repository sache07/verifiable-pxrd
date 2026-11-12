# PXRD phase analysis

## Result

The modeled crystalline product is single-phase scheelite **CaWO4**, space group *I* 41/*a* (No. 88), at a normalized crystalline weight fraction of **1.0000**. The refined cell is *a* = *b* = 5.24869(3) Å and *c* = 11.38560(6) Å. The final fit has Rwp = 2.3034%, Rp = 1.7669%, Rexp = 2.2782%, and goodness of fit = 1.0111 over 8,301 points.

The 100 wt% value is normalized only over phases retained in the crystalline model. It is not an absolute bulk assay: amorphous material and crystalline phases below the detection supported by this pattern cannot be quantified without an internal standard.

## Evidence and candidate screening

The observed families at 18.607, 28.702, 29.028, 31.419, 34.157, 39.167, 47.077, 49.055, 54.260, 57.824, and 59.422° 2theta, together with the higher-angle multiplets, are all accounted for by ambient scheelite CaWO4. Formation of CaWO4 is also the 1:1 reaction product expected from the listed CaO and WO3 precursors after heating at 900 °C.

COD 7219229 was selected as the parent: it is an ambient 298 K powder-refined scheelite record with full occupancy, no disorder, and the correct Ca:W:O = 1:1:4 composition. The other exact ambient scheelite record (COD 5910088) is a legacy CIF that redundantly enumerates symmetry-equivalent sites and fails modern occupancy/structure validation. The exact fergusonite record (COD 1546035) was measured at 11.3 GPa; its split 19.3° and 29.8° families are absent, and its added scale refined to zero.

Other chemically plausible additions were reconverged with background, all scales, zero correction, and cells:

| Trial phase | Diagnostic result |
|---|---|
| Ca3WO6 | Its strong 22.13° family is absent; 0.048(51) wt%, statistically zero. |
| Monoclinic WO3 | The 23.1–24.4° triplet is absent; 0.033(33) wt%, statistically zero. |
| CaO | 0.143(66) wt% (2.15 sigma), but Rwp improves by only 0.0007 percentage point and the 32.1, 37.2, 53.7, 63.9, and 67.1° residuals do not form a consistent family. This is not a reliable phase identification and was excluded. |

After the final one-phase refinement, the standardized residual has RMS 1.010 and no coherent unmatched peak family. A rough record-specific three-sigma upper level for CaO is about 0.3 wt%; limits for arbitrary unknown or amorphous phases cannot be inferred from that value.

## Refinement and physical checks

The Cu Kalpha1/Kalpha2 wavelengths and reported 0.5 intensity ratio were fixed. Matched trials marginally favored zero shift over specimen displacement (Rwp 3.86629% versus 3.86642% at that stage), so only zero was retained. The final global width uses positive U, W, and Z terms; the Gaussian variance remains 33.77–91.40 centidegree squared over the fitted range, and the Lorentzian width is positive. A V term was rejected because it correlated above 95% with U/W, and axial-divergence refinement was rejected because it correlated 96.5% with zero. Preferred orientation and phase-specific size/strain were not used. The saved HAP has microstrain fixed at zero and isotropic size fixed at the largest useful GSAS-II value (10 micrometres), so neither acts as compensating broadening.

Only the oxygen position and oxygen Uiso were released after the inventory and global profile stabilized. The final fully occupied model has O at (0.1543(4), 0.0107(3), 0.20849(16)) and Uiso(O) = 0.0146(8) Å². Its geometry is physical: four W–O bonds are 1.771 Å, and the eight Ca–O bonds split into four at 2.463 Å and four at 2.474 Å. No refined parameter is frozen or at a bound; the largest non-background correlation is 0.84 (global W/Z profile terms).

The CIF and `fit.csv` were exported from `final.gpx`. In `fit.csv`, difference is observed minus calculated. A reload-and-refine replay changed Rwp by only 0.000006 percentage point and produced no frozen variables.
