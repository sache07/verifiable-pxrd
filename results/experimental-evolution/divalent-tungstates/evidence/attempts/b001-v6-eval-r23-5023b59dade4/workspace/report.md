# PXRD phase analysis

## Result

The pattern is modeled as four crystalline phases. Weight fractions are normalized over these modeled crystalline phases only.

| Phase | Structural model | Weight fraction (wt%) | Formal 1σ (wt%-point) | Refined cell (Å, °) |
|---|---|---:|---:|---|
| PbWO₄ | Scheelite, `I 41/a`, COD 9009811 | 58.8645 | 0.1147 | a = 5.46604, c = 12.05797 |
| WO₃ | Monoclinic, `P 21/c`, COD 2311041 | 19.5871 | 0.0862 | a = 7.69096, b = 7.53470, c = 10.52297, β = 136.19286 |
| Pb₃O₄ | Minium, `P 42/mbc`, COD 9012124 | 17.2379 | 0.1136 | a = 8.80032, c = 6.56143 |
| PbO | Massicot, `Pbcm`, COD 2310433 | 4.3105 | 0.0707 | a = 5.48045, b = 5.87961, c = 4.75286 |

The unusual-looking WO₃ cell is a valid nonstandard setting of the room-temperature monoclinic structure. Exported CIFs retain this setting.

## Evidence for the inventory

The chemistry is consistent with partial reaction of the reported WO₃ and Pb₃O₄ precursors at 500 °C. Scheelite PbWO₄ accounts for the dominant families near 27.81, 33.17, 45.13, 55.63, 72.36, 86.01, and 94.04° 2θ. Monoclinic WO₃ is required by its low-angle triplet near 23.53, 24.02, and 24.85° and supporting families around 29–35 and 41–42°. Minium Pb₃O₄ is supported by coherent families near 26.81, 31.25, 32.55, 34.47, 47.90, 52.52, 58.48, and 66.52°. Massicot PbO contributes repeatable intensity near 29.56, 38.25, 45.57, 53.56, 60.82, and 63.65°.

Alternative physical records and polymorphs were challenged under the same restrained nuisance model. The selected room-temperature scheelite and monoclinic WO₃ records outperformed older or alternative scheelite, raspite, triclinic, and orthorhombic candidates. Raspite and a lead-deficient scheelite record refined to zero scale. A litharge PbO challenge refined to only about 0.04 wt%, improved Rwp by about 0.0014 percentage point, and lacked a coherent unique family; it is therefore not reliably determined and was excluded. Litharge or another trace crystalline impurity below roughly 0.1 wt% cannot be ruled out.

All selected source structures have chemically plausible occupancy and geometry. The exported models recover space groups 88, 14, 135, and 57, respectively. Shortest principal cation–oxygen contacts are W–O 1.775 Å in PbWO₄, W–O 1.714 Å in WO₃, Pb–O 2.128 Å in Pb₃O₄, and Pb–O 2.029 Å in PbO. Atomic coordinates and displacement parameters were retained from the source records; the powder data refined cells, scales, and profile terms, not an independent atomic-coordinate solution.

## Refinement and fit quality

The final GSAS-II replay used the full 9.9034–100.0946° range, Cu Kα₁/Kα₂ wavelengths and the reported 0.5 intensity ratio. Because pointwise uncertainties were not supplied, σ = √max(counts, 1) was used. The accepted baseline has a smooth six-term Chebyshev background, one specimen-height correction (−729.23 µm), a nonnegative common profile (`U = 5`, `W = 4`; other U/V/W/X/Y/Z terms zero), `SH/L = 0.002`, and effective polarization 0.996889. Background values remain positive and smooth (about 3655 to 671 counts across the range).

Only phase scales, cells, phase-size broadening, background, and specimen height are refined in the final project. Isotropic size broadening is used for PbWO₄, WO₃, and PbO; Pb₃O₄ has supported [001] uniaxial size broadening. Size L/G mixing values were fixed after profile trials because simultaneous size/mixing refinement was highly covariant. Strain, roughness, extinction, and preferred orientation were neutralized; texture-axis trials were indistinguishable from no texture. Refined effective coherent-domain sizes are approximately 35 nm (PbWO₄), 76 nm (WO₃), 27/21 nm (Pb₃O₄ equatorial/axial), and 27 nm (PbO), but these are not reliable absolute particle sizes because no calibrated instrumental profile was supplied.

After save, reopen, and full-range replay, the final statistics are Rwp = 3.3207%, Rp = 2.5095%, goodness of fit = 1.3383, and χ² = 14819.69 for 8301 observations and 27 refined parameters. Peak positions, widths, and asymmetry are reproduced across isolated low-, middle-, and high-angle families. Remaining residuals are small and do not form a coherent unassigned phase family.

## Uncertainty and limits

The tabulated uncertainties are formal covariance estimates conditional on this phase inventory, fixed source coordinates, assumed Poisson weights, and the empirical profile. Replays with plausible records and profile choices suggest a more realistic phase-fraction uncertainty of approximately 1 wt%-point absolute, larger than the formal values. The near-unity effective polarization and uncalibrated instrumental profile are additional sources of systematic uncertainty. Fractions apply only to the modeled crystalline material: amorphous content, if present, and unsupported trace phases cannot be quantified from this refinement.

## Submitted files

- `final.gpx`: exact final GSAS-II project used for all exports
- `fit.csv`: observed, calculated, difference, and background profiles
- `result.json`: phase paths, normalized fractions, cells, and fit statistics
- `phase_1_PbWO4_scheelite.cif`
- `phase_2_WO3_monoclinic.cif`
- `phase_3_Pb3O4_minium.cif`
- `phase_4_PbO_massicot.cif`
