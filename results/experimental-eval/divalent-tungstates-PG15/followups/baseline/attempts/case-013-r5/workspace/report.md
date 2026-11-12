# PXRD phase analysis

## Result

The modeled crystalline material contains four phases. Fractions are normalized over these phases only.

| Phase | Space group | wt% | Refined cell |
|---|---:|---:|---|
| PbWO4 (scheelite) | I 41/a | 73.8 | a=5.46491, b=5.46491, c=12.05947 A; alpha=90.000, beta=90.000, gamma=90.000 deg |
| WO3 (monoclinic) | P 21/n | 11.0 | a=7.30012, b=7.54385, c=7.69132 A; alpha=90.000, beta=90.343, gamma=90.000 deg |
| PbO (litharge) | P 4/n m m | 5.4 | a=3.97358, b=3.97358, c=5.02469 A; alpha=90.000, beta=90.000, gamma=90.000 deg |
| PbO (massicot) | P b c m | 9.7 | a=5.89602, b=5.49456, c=4.75755 A; alpha=90.000, beta=90.000, gamma=90.000 deg |

The final whole-pattern fit gives Rwp = 15.07%, Rp = 10.82%, Rexp = 3.50%, and goodness-of-fit = 4.31 over 10.10-99.85 deg 2theta. Atomic coordinates and displacement parameters were retained from the cited COD starting models; unit cells, phase scales, background, zero offset, and a common peak profile were refined in stages. The physical common profile was then held fixed for the final scale covariance cycle because independent phase broadening made the weak PbO fractions strongly size-correlated. The litharge coordinates from COD 9012700 were transformed from its origin-choice-1 description into the standard P4/nmm setting; the exported model was checked to contain two Pb and two O atoms per cell.

## Evidence

Scheelite PbWO4 accounts for the dominant series at about 27.69, 29.91, 33.05, 45.02, 47.28, 51.48, 55.54, and 56.81 deg. Monoclinic WO3 is supported by the diagnostic 23.38/23.88/24.64 deg triplet and its higher-angle lines. Orthorhombic massicot and tetragonal litharge explain separate PbO line families, including features around 30.61/38.11/49.50 deg and 28.91/32.10/45.91/48.85 deg, respectively. This phase assemblage is chemically consistent with reaction of PbO and WO3 at the reported 500 C with incomplete conversion and both PbO polymorphs.

Alternative raspite PbWO4, Pb7W8O28.8, Pb3O4, PbO2, Pb2O3, WO2, and W3O8 models were tested; they either refined to negligible scale or failed to improve the full pattern consistently.

## Remaining uncertainty

The fit has structured residual intensity, most notably a sharp unassigned feature near 25.91 deg and additional intensity near 30-31 deg. Residual indexing suggests another line lattice may be present, but no available structural model matched enough reflections to identify or quantify it reliably. Its structure and fraction are therefore reported as undetermined rather than folded into a speculative phase.

The tabulated covariance errors in `result.json` are formal only. Missing pointwise uncertainties, lack of a calibrated instrumental profile, possible preferred orientation/microabsorption in this Pb/W-rich specimen, overlap, and the unidentified component dominate the true uncertainty. A phase-specific size model shifted litharge from about 5.4 to 8.3 wt% and encountered a broadening bound, so practical fraction uncertainties are several absolute wt% and larger than the formal errors. No amorphous fraction can be measured from this dataset without an internal standard.
