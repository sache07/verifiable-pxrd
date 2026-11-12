# PXRD phase analysis

## Result

Rietveld refinement of the Cu Kα doublet pattern gives three crystalline phases. Fractions are normalized over those modeled crystalline phases.

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---:|---|---:|
| MgWO4 | P 2/c | a=4.68922, b=5.67308, c=4.92762, β=90.7734 | 0.7670(18) |
| WO3 | P -1 | a=7.30122, b=7.53170, c=7.68828, α=89.8580, β=90.8024, γ=90.0882 | 0.1593(13) |
| MgO | F m -3 m | a=4.21138 | 0.0737(16) |

The GSAS-II refinement statistics are Rwp=8.417%, Rp=6.074%, Rexp=2.864% and goodness-of-fit=2.946. The regenerated 8,301-point profile has Rwp=8.406%; `fit.csv` uses difference = observed − calculated.

## Evidence and model checks

The dominant wolframite MgWO4 model (COD 9013902) accounts for the strong line families throughout the scan. Restoring its source coordinates worsened Rwp from 8.47% to 9.07% in the matched monoclinic-WO3 stage, and restoring its ADPs worsened Rwp to 8.52%. Its refined geometry is plausible (shortest W–O 1.89 Å and Mg–O 1.92 Å), with full occupancy and no CIF-audit flags.

WO3 is required by multiple resolved peaks, notably the 23–25° and 33–35° groups; omitting it raises Rwp to 18.88%. A clean triclinic P -1 model (COD 2106293) was selected after matched complete-pattern tests. With identical positive common-WO3 ADP, strain, MgWO4 ADP constraint and nuisance model, P -1 gave Rwp=8.417% versus 8.430% for the close P 21/c alternative (COD 2311041). Orthorhombic and tetragonal alternatives were substantially worse or required excessive/unstable broadening. The final P -1 CIF has plausible W–O contacts (minimum 1.71 Å), full occupancy and no audit flags.

MgO is supported by six generated reflections, including independent intensity near 43.2°, 62.5°, 75.0° and 94.2°. Removing it raises Rwp to 9.33%, with degradation in more than one angular region. Its rocksalt model (COD 9000499) is chemically and geometrically clean.

The retained nuisance model is deliberately small: global U/W/X widths, specimen displacement, positive WO3 isotropic microstrain (~815 µstrain), and mild MgWO4 [110] March–Dollase orientation (r=1.0564). Size terms were singular, boundary-seeking or redundant with strain. Added V/Y/Z widths, polarization, surface roughness and axial divergence were rejected for negative/unphysical values or strong correlations. Individual WO3 coordinates/ADPs and MgO ADPs were also rejected as unstable. Positive displacement parameters were obtained with one common WO3 Uiso and tied MgWO4 oxygen Uiso values.

## Remaining uncertainty

The WO3 identity is reliable, but its exact low-symmetry assignment is not definitive: P -1 is the best complete-pattern model, while P 21/c is only 0.013 percentage point worse in Rwp and the refined triclinic metric is pseudomonoclinic. The submitted P -1 model should therefore be treated as preferred rather than uniquely proven.

The parenthesized fraction uncertainties are covariance-derived statistical standard uncertainties only. Because no pointwise uncertainties, calibrated instrument profile or internal standard were supplied, model/systematic uncertainty is larger and any amorphous content cannot be quantified. The reported fractions are conditional on the three modeled crystalline phases, not absolute sample mass fractions. Remaining residuals are predominantly peak-shape/intensity mismatch at modeled reflections; no additional coherent crystalline peak family was established reliably.
