# PXRD phase analysis

The refined crystalline model contains five phases. Weight fractions are normalized over these modeled crystalline phases only.

| Phase | Space group | Weight fraction | Refined cell (Å, °) |
|---|---:|---:|---|
| PbWO₄, scheelite | I4₁/a | 60.538(232)% | a = 5.46137, c = 12.05282 |
| Pb₂WO₅, monoclinic | C2/m | 13.440(178)% | a = 14.22120, b = 5.80590, c = 7.35213, β = 113.8735 |
| WO₃, monoclinic | P2₁/c | 9.404(159)% | a = 7.69654, b = 7.54116, c = 10.56321, β = 136.2956 |
| PbO, massicot | Pbcm | 8.591(194)% | a = 5.89585, b = 5.48650, c = 4.75500 |
| PbO, litharge | P4/nmm | 8.026(204)% | a = 3.97462, c = 5.03321 |

The final Rietveld fit has Rwp = 10.708%, Rp = 7.130%, and goodness-of-fit = 3.065 (8,280 fitted observations, 38 variables). The final cycle converged with no SVD-dropped variables and maximum shift/esd 0.013. Calculated Gaussian and Lorentzian widths remain positive over the measured range.

## Evidence

Scheelite PbWO₄ accounts for the dominant line family, including the intense peaks near 27.70°, 45.03°, 51.49°, 55.54°, and 72.27° 2θ. Monoclinic WO₃ accounts for the low-angle multiplet near 23.4–24.6° and many independent higher-angle lines. The retained WO₃ model (COD 2311041) fits better than the near-tied older model under identical nuisance conditions and passes the occupancy, duplicate-site, symmetry, and contact audit.

Massicot and litharge PbO are supported by distinct multi-peak sets and retain positive scales in the complete model. The COD 9012700 litharge coordinates were converted to an equivalent GSAS-II origin setting; this repairs an import-setting error while preserving the published P4/nmm PbO structure. The exported litharge CIF expands to Pb₂O₂, has plausible contacts, and passes the CIF audit. Broad massicot peaks support 5,249 µstrain isotropic microstrain, while litharge supports a 0.0376 µm coherent-domain size. Matched removal of either term materially worsens the full-pattern fit. No preferred-orientation term survived the multi-region test.

Pb₂WO₅ was recovered through an isovalent, charge-balanced Mo⁶⁺→W⁶⁺ substitution in the C2/m Pb₂MoO₅ topology (COD 7220560). Its CIF audit finds no occupancy, symmetry, duplicate-site, or contact flags. With the cell fixed, adding this model reduced Rwp from 14.271% to 13.085%; cell refinement then reduced Rwp to about 11.56% before later profile/model corrections. It explains independent residual lines around 25.9°, 29.3°, 31.0°, 43.4°, 47.3°, 54.8°, and 60.1° without cell collapse. This is strong phase evidence, but its atomic coordinates are inherited from the isostructural molybdate analogue and were not independently refined, so this assignment is less secure than the four direct database matches.

The angular comparison retained specimen displacement alone (about −451 µm). Zero plus displacement was rejected at 99.8% correlation, and zero-only fit worse. Global X/Y Lorentzian terms and polarization passed matched-removal tests; U, V, W, axial-divergence, roughness, and texture additions were negligible, correlated, nonphysical, or region-local.

Mature-baseline retests drove raspite PbWO₄, WO₂, and Pb₇W₈O₂₈.₈ to the phase-scale lower bound. Pb₃O₄ retained a positive scale but was rejected despite a lower Rwp: it helped residuals near 26.68°, 31.01°, and 46.46° while adding its strongest lines at 52.44° and 32.48° where the baseline was already overpredicted. Pb₃WO₆/Pb₅WO₈ analogue patterns likewise predicted strong absent lines.

## Remaining uncertainty

Coherent positive residual intensity remains near 30.16° 2θ, with a weaker feature near 31.39°. No chemically plausible atomistic candidate passed the complete-pattern test for it, so its structure and weight fraction cannot be determined reliably and it is excluded from the normalization.

All five submitted CIFs pass the final occupancy, duplicate-site, symmetry, and contact screen. Atomic coordinates and ADPs were held at the audited source/analogue values because this overlapped multiphase laboratory pattern does not support their independent refinement. The parenthetical uncertainties are formal GSAS-II one-sigma values; true fraction uncertainty is larger because of phase overlap, PbO broadening, the unresolved residual component, and the analogue-derived Pb₂WO₅ model. The fractions are therefore conditional on the five-phase crystalline model rather than absolute bulk composition.
