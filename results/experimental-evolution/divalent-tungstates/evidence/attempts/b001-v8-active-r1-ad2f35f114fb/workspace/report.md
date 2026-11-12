# PXRD phase analysis

## Result

The modeled crystalline material is scheelite CaWO4 with residual monoclinic WO3. Fractions are normalized over these two modeled crystalline phases; amorphous material, if present, is not quantified.

| Phase | Structural model | Weight fraction | Refined cell (A, deg) |
|---|---|---:|---|
| CaWO4 | I 41/a, COD 7219229 | 0.8792 (87.92 wt%) | a = 5.242981, c = 11.374359 |
| WO3 | P 21/c, COD 2311041 | 0.1208 (12.08 wt%) | a = 7.683184, b = 7.531958, c = 10.504856, beta = 136.066772 |

The least-squares standard uncertainty is 0.00107 in weight fraction (0.11 wt%), but this is much smaller than the real model uncertainty. Scale and roughness are 95.6% correlated, and reasonable nuisance/profile choices move the WO3 fraction by roughly 1--2 wt%. A more realistic interpretation is therefore about 88/12 wt% with an absolute systematic uncertainty of approximately 2--3 wt% per phase.

## Identification and chemical checks

The precursor context gives the charge- and element-balanced relation

`x CaO + (x + y) WO3 -> x CaWO4 + y WO3`.

Thus CaWO4 plus excess or unreacted WO3 closes the Ca/W/O and charge balances without another product. Searches also considered Ca3WO6, Ca2WO5, CaW2O7, Ca2W3O11, and Ca4WO7 analogues, but no coherent residual family or physically credible record required one of them.

All likely source structures were screened with `learned/cif_health.py` before fitting. The retained CaWO4 and WO3 records passed. Passing tetragonal, orthorhombic, triclinic, and monoclinic WO3 competitors were fitted with the same restrained baseline; COD 2311041 gave the best physically acceptable result. A nominally competitive WO3 record (COD 1528915) was rejected because it contains full-occupancy O--O contacts of 1.575 A and gave no meaningful fit advantage. The exact ambient WO3 polymorph is not uniquely resolved: a clean triclinic model fitted only slightly worse, so the presence and amount of WO3 are more certain than its detailed distortion.

CaO was re-challenged as a weak phase. It refined to about 1.2 wt% but improved Rwp by only 0.017 percentage point while forcing its cubic cell about 5.4% below the source value, so it was rejected as an opportunistic residual match rather than retained as a phase.

## Refinement and profile evidence

GSAS-II used the full 9.9034--100.0946 deg 2theta range, the reported Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio, and Poisson weights because pointwise uncertainties were not supplied. Inactive size, strain, March, roughness, extinction, and related terms were first set to neutral values. A 10-term Chebyshev background and nonnegative U/W/X baseline were fitted; U reached zero and was fixed at zero. Only one angular correction (zero), W/X, polarization, roughness B, CaWO4 [001] March texture, and CaWO4 size broadening were retained. WO3 size and strain refined to their neutral bounds and were pruned. CaWO4 strain was inferior to size broadening (Rwp 9.182% versus 8.610%); a replay-stable [001] uniaxial size model further reduced Rwp to 8.537%, with domain-size parameters 0.992 and 0.766 micrometres.

Representative half-height checks below use lightly smoothed observed net counts only for numerical width measurement; refinement used the original unsmoothed counts.

| Target 2theta | Position obs/calc (deg) | FWHM obs/calc (deg) | Left/right half-width obs (deg) | Left/right half-width calc (deg) |
|---:|---:|---:|---:|---:|
| 18.434 | 18.4336 / 18.4336 | 0.2177 / 0.2291 | 0.1059 / 0.1118 | 0.1138 / 0.1153 |
| 24.225 | 24.2253 / 24.2253 | 0.1682 / 0.1601 | 0.0848 / 0.0834 | 0.0812 / 0.0789 |
| 46.930 | 46.9253 / 46.9361 | 0.3035 / 0.3067 | 0.1229 / 0.1806 | 0.1317 / 0.1751 |
| 76.030 | 76.0255 / 76.0363 | 0.4651 / 0.4558 | 0.2039 / 0.2612 | 0.2066 / 0.2492 |
| 90.370 | 90.3800 / 90.3691 | 0.7986 / 0.7090 | 0.4643 / 0.3343 | 0.4244 / 0.2846 |

These checks do not show a repeated directional asymmetry that justifies releasing SH/L. The final statistics are Rwp = 8.537%, Rp = 5.408%, Rexp = 2.247%, goodness of fit = 3.799, and reduced chi-squared = 14.436. The goodness of fit remains above counting expectation, with structured low-angle intensity residuals, notably near 19.30, 22.02, 31.41, and 45.13 deg. The first two do not form a convincing family for a charge-balanced third phase, while the latter two coincide with intensity/profile mismatch in retained-phase families. Consequently, no third phase is reported, but a trace phase below reliable quantification cannot be excluded.

## Structure health and output consistency

The final exported CIFs were re-run through `learned/cif_health.py`; both pass with full occupancy, no disorder flags, and no hard contacts. CaWO4 has tetrahedral W--O = 1.7624 A and Ca--O = 2.4685--2.4721 A. Monoclinic WO3 has six-coordinate W with W--O = 1.7129--2.1568 A. Atomic coordinates and displacement parameters were not independently determined by this mixed powder pattern; they remain inherited from the source models (including source-reported zero Uiso values for WO3), so only the lattice metrics were refined.

After pruning bound or unsupported terms, the project was saved, reopened, and replayed twice over the full range. The two replays changed Rwp by 0.0000024 percentage point and the WO3 fraction by 0.00000018. `CaWO4.cif`, `WO3.cif`, `fit.csv`, and `result.json` were then generated or checked against that reopened `final.gpx` project.
