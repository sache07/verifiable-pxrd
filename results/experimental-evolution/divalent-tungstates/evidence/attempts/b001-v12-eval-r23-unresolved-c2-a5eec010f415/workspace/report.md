# PXRD phase analysis

## Result

The pattern is described by three crystalline phases. Weight fractions are normalized over these modeled crystalline phases only.

| Phase | Structural model | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| SrWO₄ | scheelite, *I*4₁/*a* | a = 5.383733, c = 11.879641 | 0.60133 (60.13 wt%) |
| WO₃ | monoclinic, *P*2₁/*c* | a = 7.680412, b = 7.541726, c = 10.496564, β = 136.12080 | 0.24645 (24.65 wt%) |
| SrCO₃ | orthorhombic, *Pnma* | a = 6.012135, b = 5.089066, c = 8.379350 | 0.15222 (15.22 wt%) |

This inventory is chemically consistent with incomplete reaction of the reported SrCO₃ and WO₃ precursors to SrWO₄ at 650 °C. No precursor amounts were reported, so no mass-balance closure or precursor ratio was varied or imposed.

## Evidence and model selection

Scheelite SrWO₄ accounts for the dominant families at approximately 17.456, 27.203, 29.452, 32.647, 44.828, 47.143, 51.402 and 55.542° 2θ. Monoclinic WO₃ is required by the resolved 22.51/22.94/23.83° triplet and independent middle- and high-angle families. Orthorhombic SrCO₃ is supported by non-coincident families near 24.63/25.28, 36.08 and 43.65°; removing SrCO₃ and reconverging the other terms raises Rwp from 3.30% to 4.79%.

The SrWO₄ model was constructed by the isovalent Ca²⁺→Sr²⁺ substitution in COD 7219229 (CaWO₄ scheelite), then health-screened. It outperformed the independent SrMoO₄-derived scheelite model both before and after identical broadening/texture treatment (final elaborated Rwp 3.30% versus 3.55%). A lower-symmetry fergusonite competitor remained very poor even after its own axial texture trials (best Rwp about 17.4%). For WO₃, COD 2311041 was decisively preferred: the next monoclinic and triclinic records remained at least about 7.4% and 7.6% Rwp after their own profile and texture loops; orthorhombic, tetragonal and hexagonal records were worse and did not reproduce the observed splittings. The trigonal SrCO₃ alternative collapsed, while the orthorhombic record reproduced the observed splitting.

Exact Sr₃W₂O₉ and two independently constructed Sr₃WO₆ watch-list models collapsed to zero scale in the final four-phase rebuild. A rhombohedral Sr₃W₂O₉ analogue refined below 0.12 wt%, but its scale changed by more than fivefold when its cell was opened and it had no two independent residual families. It was therefore rejected as replay-unstable. No same-formula coexistence survived the source/texture challenges.

The final full-range refinement used the reported Cu Kα1/Kα2 wavelengths and fixed 0.5 intensity ratio, one shared zero correction (−0.63710°), nonnegative U/W/X, a smooth 12-term Chebyshev background, and one physical surface-roughness term. Only WO₃ required phase-specific isotropic microstrain (about 4555 microstrain). SrWO₄ and SrCO₃ size/strain terms were left neutral (10 µm and zero strain). Single March–Dollase terms were retained only where replay-stable: [111] for SrWO₄, [10-1] for WO₃ and [001] for SrCO₃. Competing low-index axes gave materially worse fits. SH/L was not released because low-, middle- and high-angle peak asymmetry was not repeated systematically.

An isolated-family shape audit also supports the common profile model:

| Family region | Observed position | Calculated position | Observed FWHM | Calculated FWHM | Observed left/right HWHM | Calculated left/right HWHM |
|---|---:|---:|---:|---:|---:|---:|
| low angle | 17.4556° | 17.4556° | 0.1721° | 0.1776° | 0.0827 / 0.0895° | 0.0917 / 0.0859° |
| middle angle | 44.8280° | 44.8172° | 0.2403° | 0.2360° | 0.1109 / 0.1294° | 0.0965 / 0.1395° |
| high angle | 95.0091° | 94.9982° | 0.2420° | 0.2424° | 0.1169 / 0.1251° | 0.1158 / 0.1266° |

Final statistics are Rwp = 3.2964%, Rp = 2.5077%, Rexp = 2.8612%, and reduced χ² = 1.3274 over 8301 points. The low/middle/high-angle segmented Rwp values are 3.72%, 3.06% and 3.13%, respectively. No coherent unmodeled sharp family remains.

## Remaining uncertainty

Pointwise uncertainties were not supplied, so refinement used the Poisson approximation σ = √counts. The GSAS-II covariance-only fraction uncertainties are about 0.13 wt%-points, but they do not include source-model, texture, roughness or counting-systematic uncertainty; a more realistic precision is roughly 1–2 wt%-points. Fractions do not quantify amorphous material.

The SrWO₄ polymorph and cell are well determined by its peak positions and systematic absences, but its submitted atomic coordinates come from a chemically justified scheelite analogue rather than an exact SrWO₄ database record, so fine oxygen coordinates are less secure than the phase identity. All candidate and final CIFs passed the supplied geometry/occupancy health screen. A trace phase below the practical detection level (approximately 0.5–1 wt% here) cannot be excluded reliably, but none of the chemically plausible challenged models met the required scale and family-evidence gates.
