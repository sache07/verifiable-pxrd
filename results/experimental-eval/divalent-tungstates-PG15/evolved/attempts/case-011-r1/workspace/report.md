# PXRD phase analysis

## Result

| Modeled crystalline phase | Space group | Weight % | Assessment |
|---|---:|---:|---|
| Monoclinic WO3 | P 21/c | 71.004 ± 0.214 | High confidence |
| beta-MnO2 (pyrolusite) | P 42/m n m | 26.618 ± 0.172 | High confidence |
| Mn2O3 (bixbyite) | I a -3 | 1.130 ± 0.115 | Moderate confidence |
| gamma-MnOOH (manganite) | P 21/c | 0.908 ± 0.129 | Moderate confidence |
| MnWO4 (wolframite type) | P 2/c | 0.340 ± 0.060 | Tentative trace assignment |

Fractions are normalized to 100% over the modeled crystalline phases. The quoted uncertainties are one-standard-deviation GSAS-II covariance estimates; they do not include phase-choice, texture, absorption, or amorphous-content uncertainty.

The final full-range fit has Rp = 4.429%, Rwp = 5.872%, Rexp = 2.693%, and goodness of fit = 2.184 for 8,301 points and 30 refined parameters. Reopening and replaying `final.gpx` gave maximum shift/standard uncertainty below 0.001, no frozen or bound parameters, and no SVD singularities.

## Evidence and model

The Cu K-alpha1/alpha2 doublet and reflection geometry in `metadata.json` were modeled explicitly. Monoclinic WO3 accounts for the diagnostic 23.44/23.92/24.69 degree triplet and its many low-, middle-, and high-angle families. Beta-MnO2 is independently required by families near 29.01, 37.68, 56.96, 59.66, and 72.53 degrees. Bixbyite Mn2O3 is led by an isolated 33.25 degree family with support near 45.45 and 55.45 degrees. Modern, chemically complete manganite MnOOH is led by the isolated 26.45 degree family and supported by partly overlapped families near 34.25, 55.19, and 62.05 degrees. The trace MnWO4 scale is carried mainly by coherent weak features near 30.31 and 30.75 degrees plus overlapped families, so it is retained but labeled tentative.

All selected records are ordered and fully occupied. Their refined or fixed geometries are physical: WO3 W-O = 1.741-2.156 A; beta-MnO2 Mn-O = 1.885-1.888 A; bixbyite Mn-O = 1.896-2.245 A; MnWO4 W-O = 1.782-2.121 A and Mn-O = 2.096-2.247 A; and manganite O-H = 0.982 A with Mn-O = 1.881-2.337 A.

The baseline uses a smooth six-term Chebyshev background, one specimen-displacement correction (-547.9 micrometres), refined polarization (0.7348), and a common nonnegative W/X profile (W = 5.752, X = 8.961; U, V, Y, and Z fixed at zero). Surface roughness and extra SH/L asymmetry were rejected as correlated or bound. Size, strain, texture, extinction, and Babinet terms were neutralized unless supported. Accepted phase terms are replay-stable [011] uniaxial microstrain for WO3 and [110] March-Dollase texture for beta-MnO2 (ratio 0.8069). Only the two major cells and the two W positions in WO3 were refined. Minor-phase cells, oxygen coordinates, and displacement parameters were fixed because their trials were insignificant, correlated, or unstable.

## Alternatives and remaining uncertainty

Monoclinic and near-triclinic WO3 descriptions are difficult to distinguish with these broadened powder data. The submitted P 21/c model was selected from physically plausible monoclinic, triclinic, and orthorhombic records using source conditions, geometry, and replay behavior, but the precise WO3 distortion and atomic displacement parameters are not reliably determined.

The submitted MnWO4 model comes from the only exact-composition COD record, measured at 2.4 GPa. An ambient FeWO4 wolframite parent with isovalent Fe2+ to Mn2+ substitution gave essentially the same result (0.376 wt%, Rwp = 5.871%). Attempts to refine the trace-phase cell wandered on replay, so the reference cell is fixed. Thus MnWO4 presence is plausible, but its exact structure and fraction are less reliable than its formal uncertainty suggests.

Manganite is supported by several families, but MnOOH is unexpected after nominal 300 C heating and could represent a residual precursor impurity or a phase with a very similar weak pattern. Groutite and ramsdellite were not supported. An obsolete Pnnm manganite record improved one residual feature but conflicted with other predicted families and was rejected as a duplicate/surrogate model. Mn3O4 and Mn3WO6 trials remained below reliable multi-family detection (about 0.27 ± 0.20 and 0.19 ± 0.08 wt%, respectively). The profile still has correlated residuals (Durbin-Watson 0.456), notably an intensity mismatch near 50.3 degrees. No amorphous fraction can be obtained from these data, and the exported CIFs should be treated as phase models rather than precision crystal-structure determinations.
