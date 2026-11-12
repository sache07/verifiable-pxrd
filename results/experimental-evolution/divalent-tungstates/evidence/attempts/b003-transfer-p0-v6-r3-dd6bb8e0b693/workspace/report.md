# PXRD phase analysis

The pattern is best described by three crystalline phases. Weight fractions are normalized over these modeled crystalline phases:

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| γ-WO₃ | P 21/n (No. 14) | a = 7.29742, b = 7.54057, c = 7.68554, β = 90.9177 | 56.05 wt% |
| Cu₃WO₆ | Pa-3 (No. 205) | a = 9.78088 | 34.65 wt% |
| Tenorite CuO | C 2/c (No. 15) | a = 4.66704, b = 3.43013, c = 5.12498, β = 99.5062 | 9.30 wt% |

The final GSAS-II fit over 9.903–100.095° 2θ has Rwp = 3.171%, Rp = 2.415%, Rexp = 2.409%, and goodness-of-fit = 1.322. Because no pointwise uncertainties were supplied, the refinement used Poisson proxy weights, σ = √counts.

## Evidence and model

Monoclinic γ-WO₃ accounts for the characteristic 23.23/23.67/24.44° triplet and its repeated groups near 33–34°, 41–42°, 47–51°, and 53–56°. Its 002 reflection is strongly enhanced relative to 020 and 200, requiring an eighth-order spherical-harmonic preferred-orientation correction; the resulting correction remains positive over all modeled WO₃ reflections.

Cubic Cu₃WO₆ is identified independently by peaks at approximately 15.75, 18.18, 20.37, 22.32, 30.36, 36.81, 43.45, 58.19, 63.88, 70.80, and 87.62°. After fitting WO₃ and Cu₃WO₆, coherent residuals at the tenorite positions near 35.7, 38.9, 49.0, 53.6, and 58.4° established residual CuO. Adding CuO reduced Rwp from 6.52% to 5.32% before the final texture and phase-profile treatment.

The Cu Kα₁/Kα₂ wavelengths and 0.5 intensity ratio were fixed to the metadata values. Refined terms included phase scales and cells, zero/profile terms, relative isotropic phase broadening, WO₃ texture, and the heavy-cation coordinates in WO₃ and Cu₃WO₆. The fixed 0.17 µm Cu₃WO₆ size term sets the otherwise correlated profile-broadening reference; no absolute crystallite sizes are claimed. Oxygen coordinates and displacement parameters were retained from the reference structures because this overlapping, textured laboratory pattern does not determine them reliably. Zero displacement values inherited for WO₃ and Cu₃WO₆ are placeholders, not measured thermal parameters. CuO atomic coordinates were also fixed because it is the minor phase.

## Remaining uncertainty

The formal weight-fraction esds are only 0.10–0.13 wt%, but they do not include model choice. Strong WO₃ texture and the uncalibrated instrumental profile dominate the systematic uncertainty; a realistic reading is about ±2 wt% absolute for WO₃ and Cu₃WO₆ and about ±1.5 wt% for CuO. Without an internal standard, an amorphous fraction cannot be measured, so the reported values apply only to the modeled crystalline material.

CuWO₄ was explicitly tested and its scale refined to zero. Scale-only trials for Cu₂O and tetragonal WO₃ gave less than 0.1 and about 0.25 wt%, respectively, but those signals are below robust discrimination from profile/texture errors and overlapping WO₃ reflections; neither trace phase can be determined reliably and neither is included. No other unmatched peak family remains at a level supporting an additional crystalline phase.
