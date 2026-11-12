# Powder XRD phase analysis

## Result

The 500 °C product is best described as an incompletely reacted precursor mixture. The modeled crystalline fraction contains:

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---:|---|---:|
| WO₃, triclinic | P -1 (No. 2) | a=7.30693, b=7.53812, c=7.69504; α=89.9192, β=90.6948, γ=89.9990 | 0.76738 (76.74 wt%) |
| Co₃O₄ spinel | F d -3 m (No. 227) | a=8.08566 | 0.23262 (23.26 wt%) |

These fractions are normalized over the two modeled crystalline phases. They do not quantify amorphous material. A realistic systematic uncertainty from the coupled low-angle attenuation, phase Uiso, and scale terms is about ±0.02 absolute fraction (roughly ±2 percentage points), larger than the formal least-squares errors.

## Evidence and model selection

The triclinic WO₃ model accounts for the diagnostic 23.465/23.954/24.714° triplet and its repeated middle- and high-angle families. Co₃O₄ is independently required by families at approximately 19.368, 31.625, 37.200, 45.154, 59.672, and 65.550° 2θ. Their centers agree with the calculation to within one data step (0.01087°) in checks of isolated low-, middle-, and high-angle peaks.

Physical WO₃ alternatives were compared under the same restrained nuisance model. COD 2106293 (P -1) gave a small but repeatable advantage over physical monoclinic P2₁/c COD 2311041; orthorhombic and small-cell monoclinic records were substantially worse. Consequently, the exact low-symmetry WO₃ polymorph is less certain than the WO₃ identification itself. The final P -1 geometry passes the contact screen (minimum W–O 1.695 Å; minimum O–O 2.565 Å). The selected Co₃O₄ model, COD 9005896, also passes (minimum Co–O 1.921 Å; minimum O–O 2.557 Å).

No exact CoWO₄ database entry was available, so isovalent CoMoO₄, FeWO₄, and ZnWO₄ parents were converted and challenged as wolframite-type CoWO₄ models. The Fe- and Zn-derived models refined to zero scale. The CoMoO₄-derived model was only 0.00085 fraction before cell refinement; its apparent increase required an implausible ~5% b-axis contraction and is interpreted as residual fitting. CoWO₄ therefore has neither a reliable structure nor a reliable fraction in this pattern and is not included; any crystalline amount is below a defensible quantitative detection level (approximately sub-1 wt% here).

## Refinement and uncertainty

The final GSAS-II model uses both Cu Kα wavelengths, a smooth six-term Chebyshev background, one specimen-displacement correction (-663.96 µm at 200 mm radius), polarization 0.6751, and a nonnegative U/W/X profile. Reversible trials supported a 0.440 µm Co₃O₄ size term and uniaxial WO₃ microstrain along [010] (about 4188 ppm perpendicular and 2984 ppm parallel). Alternative strain axes, texture, extra phase-size terms, and additional atomic displacement refinements were pruned when neutral, unstable, or bound-limited. A small effective roughness correction was retained but fixed after its strong correlation with absolute scale was mapped.

Restrained W-coordinate refinement was supported and retained. WO₃ oxygen-coordinate groups repeatedly reached their displacement bounds, and the Co₃O₄ oxygen coordinate was unsupported; those coordinates remain at the published parent values and should not be interpreted as independently determined by this powder pattern.

Native no-refit replay of `final.gpx` over all 8,301 original points gives Rwp=3.2779%, Rp=2.3824%, Rexp=1.7205%, and GOF=1.9052. The replay reports no negative-background, peak-width, displacement-tensor, or other profile-review flags; the background remains positive (minimum 2681 counts). Some correlated residual structure remains, especially around strong low-angle peaks and the resolved high-angle Kα doublets, so the fit is not evidence for uniquely determined oxygen positions or trace phases.
