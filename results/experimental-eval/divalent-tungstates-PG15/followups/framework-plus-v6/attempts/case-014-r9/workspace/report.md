# Powder-XRD phase analysis

The pattern is best represented by four crystalline phases. Fractions are normalized over those modeled crystalline phases; they do not quantify any amorphous material.

| Phase model | Space group | Weight fraction | Confidence |
|---|---:|---:|---|
| SrWO4, scheelite | I 41/a | 0.7293 (72.93 wt%) | high |
| WO3, monoclinic | P 21/c | 0.1141 (11.41 wt%) | high |
| Sr3WO6-like | P 21/c | 0.0595 (5.95 wt%) | moderate |
| Sr3W2O9-like | C 2/c | 0.0971 (9.71 wt%) | moderate |

## Evidence and model selection

Scheelite SrWO4 accounts for the dominant peak families over the full angular range. Monoclinic WO3 is required by its characteristic low-angle multiplet and additional separated lines. A physically valid WO3 record (COD 2311041) was chosen over a marginally better-fitting older, rounded record that produced an implausible 1.58 Å O–O contact. COD 2311041 uses a valid but non-reduced monoclinic setting; its refined volume is 423.888 Å3.

Neither remaining Sr–W–O lattice can be removed without coherent residual families returning. In inventory-removal trials, omission of the Sr3WO6-like component raised Rwp to about 13.8%, while omission of the Sr3W2O9-like component raised it to about 15.0%. Their combined chemistry is also consistent with the nominal 1:1 Sr:W precursor ratio: the four-phase result gives a bulk crystalline Sr:W molar ratio of about 0.95.

No exact Sr3WO6 entry was available. A cross-chemistry search identified Sr3UO6 (COD 2001752), and isovalent U6+ -> W6+ substitution produced the submitted Sr3WO6 model. Both P21 and P21/c parents fit nearly equally; the centrosymmetric P21/c parent was selected because it has sound oxide geometry and fewer independent parameters. Thus the lattice and presence of this component are supported, but its exact symmetry and atomic coordinates are not uniquely determined from this powder pattern.

The Sr3W2O9-like model is based on COD 2311977. Its reflections form a coherent family from roughly 30 to 95 degrees 2theta, and the refined model passes the geometry/occupancy screen. However, the parent record was reported from high-pressure synthesis, whereas this sample was heated at 900 C under unspecified ambient-pressure conditions. The exact composition/structure and its fraction are therefore less secure than those of SrWO4 and WO3.

SrCO3, SrO, scheelite/fergusonite alternatives, other WOx records, and several Sr-W-O analogue models were challenged under the final common profile. Carbonate refined to zero. SrO acquired a small apparent scale (~0.8 wt%), but its three strongest expected lines did not show a coherent positive-residual family; the apparent gain came from heavily overlapped high-angle residuals, so SrO was rejected as a profile surrogate.

## Refinement and uncertainty

The final model uses the metadata Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio, an eight-term smooth Chebyshev background, one specimen-displacement correction, a nonnegative common U/W/X profile with U fixed at zero, and one surface-roughness degree of freedom. WO3 alone retains a supported isotropic size term (0.131 micrometres). Texture, atomic-coordinate shifts, phase-specific strain, additional asymmetry/polarization terms, and broadening for the other phases were rejected because they were unsupported, boundary-driven, correlated, or not replay-stable. All scales and unit cells were refined.

The final full-range statistics are Rwp = 13.082%, Rp = 9.212%, Rexp = 3.528%, and goodness of fit = 3.708 for 8,282 points and 31 refined variables. The fit is not at the counting-noise floor: structured intensity/shape residuals remain, especially near 28–31 degrees and in several overlapped middle- and high-angle regions. Acceptable nuisance/source branches move the minor-phase split by roughly 1–2 wt% absolute; this model spread is more realistic than the formal least-squares errors. Atomic coordinates for the two Sr-rich minor phases, and their exact fractions, therefore cannot be claimed with high reliability.

All four exported CIFs pass the necessary geometry/occupancy screen. A fresh read-only GSAS-II replay from `final.gpx` reproduced `fit.csv` to below 5e-9 counts, mapped the four project phases one-to-one to the submitted CIFs, and returned the same normalized fractions with no profile-review flags.
