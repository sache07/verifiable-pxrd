# Powder XRD phase analysis

The pattern is best described by three crystalline phases:

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---:|---|---:|
| Wolframite ZnWO₄ | P2/c (13) | a = 4.70627, b = 5.73856, c = 4.93751, β = 90.6144 | 82.48 wt% |
| Triclinic WO₃ | P-1 (2) | a = 7.31816, b = 7.52761, c = 7.71332, α = 90.0956, β = 89.0471, γ = 90.0771 | 12.72 wt% |
| Wurtzite ZnO | P6₃mc (186) | a = 3.25661, c = 5.18863 | 4.80 wt% |

Fractions are normalized over the modeled crystalline phases. No amorphous fraction can be obtained from this refinement.

## Evidence and model selection

The dominant peak positions index on the wolframite ZnWO₄ cell. A P2/c CoMoO₄ framework transferred by Co→Zn and Mo→W was refined in the complete mixture. An independent wolframite transfer gave Rwp 16.72%, and scheelite/triclinic ZnWO₄ additions projected to only about 0.3 wt% while predicting strong peaks absent from the residual; they were not retained.

Adding wurtzite ZnO to the common ZnWO₄ + WO₃ state lowered fresh Rwp from 11.107% to 10.756% at positive scale. Its characteristic 31.8–36.3°, 47.5° and higher-angle lines remain supported after joint refinement, so it is residual precursor rather than a rejected zero-scale trial.

For WO₃, the initially close legacy P2₁/n reference contained 1.58 Å O–O contacts. Same-state full replacements were therefore tested. After bounded physical refinement, the contact-safe P-1 model reached Rwp 9.303%, substantially below the legacy model (9.68–9.75%) and below other tested monoclinic, orthorhombic, tetragonal and hexagonal WO₃ models. All three submitted CIFs pass the occupancy/contact screen.

Residual-directed ordinary W–O/Zn–O reference screens and same-stoichiometry prototype additions did not justify a fourth phase. Interrupted or parser-invalid trials were treated as unknown and were not used as exclusions.

## Refinement and uncertainty

The final independent, no-refinement replay of `final.gpx` gives Rwp = 9.3029%, Rp = 5.3010%, χ² = 102576.8 and goodness of fit = 3.515. The Cu Kα doublet was fixed to the metadata. The selected calibration has zero = +0.250° and specimen displacement = −233.6 µm; these terms are correlated, and the zero lies at its allowed boundary.

Fresh grids selected physical crystallite-size/texture states before the final ordinary restart. The fitted sizes are approximately 0.062 µm (ZnWO₄), 0.088 µm (WO₃) and 0.070 µm (ZnO). Preferred orientation is substantial, especially for WO₃ and ZnO, so scale fractions carry model uncertainty. Reasonable systematic uncertainties are roughly ±2 wt% for ZnWO₄, ±1.5 wt% for WO₃ and ±1 wt% for ZnO; the ZnO fraction is least secure.

ZnWO₄ heavy-atom and oxygen coordinates were refined and remain geometrically plausible, but oxygen positions correlate with texture. The many independent WO₃ coordinates were retained from the physical P-1 reference because this powder pattern does not determine them reliably; the WO₃ phase identity/cell and fraction are more reliable than its individual oxygen coordinates. Rwp remains above the counting-statistical minimum (2.646%), so small profile-systematic residuals remain even though no additional crystalline phase is defensibly resolved.
