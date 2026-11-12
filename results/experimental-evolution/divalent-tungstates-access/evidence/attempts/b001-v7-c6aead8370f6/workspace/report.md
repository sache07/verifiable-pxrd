# Powder XRD phase analysis

The pattern is explained by three crystalline phases. Weight fractions are normalized over these modeled crystalline phases; no amorphous fraction can be obtained without an internal standard.

| Phase | Space group | Refined cell (Å, °) | Crystalline weight fraction |
|---|---|---|---:|
| MnWO₄ (wolframite) | P2/c | 4.79611, 5.71102, 4.97907; β = 91.12595 | 0.686649 ± 0.000206 |
| γ-WO₃ | P2₁/n | 7.30196, 7.53866, 7.69336; β = 90.86749 | 0.156734 ± 0.000171 |
| Mn₃WO₆ | R-3 | 8.89343, 8.89343, 10.46078; γ = 120 | 0.156617 ± 0.000165 |

The quoted uncertainties are conditional least-squares standard uncertainties from the final scale covariance. They do not include phase-model, absorption, microabsorption, or amorphous-content systematics, so realistic compositional uncertainty is larger.

## Evidence and model selection

The ordinary phases were identified first. Wolframite MnWO₄ matches the complete P2/c reflection family (starting structure COD 1520200). Monoclinic γ-WO₃ accounts for a second family. At equal development, the transformed P2₁/n neutron parent COD 2311041 gave Rwp 2.523% versus 3.166% for the lower-precision COD 1528915 parent, and was retained.

The two-phase model left a coherent third family. Eleven independent residual reflections indexed together to an R-3 hexagonal cell near a = 8.89 Å and c = 10.46 Å (position RMS about 0.016°). The chemically balanced relationship Mn₃WO₆ + 2 WO₃ ↔ 3 MnWO₄ makes Mn₃WO₆ plausible for the WO₃/Mn₃O₄ synthesis. Because no direct suitable Mn₃WO₆ reference was available, symmetry-diverse substituted parents were compared after identical cell/coordinate adaptation. The R-3 Mn₃TeO₆-derived start (COD 2211528, Te→W) was stable and outperformed the alternative R-3 Cd₃TeO₆-derived start at equal checkpoints. C2/c, Pa-3, and P2₁/c alternatives lost their positive candidate scales and left the same residual family, so they were discarded. After accepting R-3 Mn₃WO₆, no coherent unassigned reflection family remained; the residual extrema are center/wing mismatches on accepted peaks rather than evidence for a fourth phase.

## Refinement and checks

The Cu Kα1/Kα2 wavelengths (1.540598/1.544426 Å) and 0.5 intensity ratio were taken from the metadata. Since point uncertainties were not supplied, count-statistical weights were used. A ten-term Chebyshev background was selected against orders 8, 12, and 14. Zero was fixed at 0°, while the specimen displacement refined to -654.79 µm, inside the supplied ±800 µm range. Bound-seeking or correlated nuisance/profile refinements were rolled back: in particular SH/L was fixed at 0.02, and common profile U was retained at its last interior value (36.9933) rather than its joint-refinement upper bound. The only retained preferred-orientation correction is a weak, uniquely favored γ-WO₃ [100] March–Dollase term of 1.00658.

The required bounded polish selected its converged phasewise-coordinate branch. Bound-hit coordinate components were restored before selection; the accepted branch has no short contacts or negative displacement parameters and settled with maximum shift/esd 0.0346. A zero-optimization GSAS-II replay regenerated the whole profile from the saved atomic models, left `final.gpx` unchanged, and raised no profile-review flags.

Final fit statistics are Rwp = 1.93115%, Rp = 1.44405%, Rexp = 1.77150%, goodness of fit = 1.09012, and χ² = 9837.30 for 8301 observations (23 variables in the final settle).

## Remaining uncertainty

MnWO₄ and γ-WO₃ are well supported in phase identity and topology. The R-3 Mn₃WO₆ phase is strongly supported by its unique reflection family and stable positive scale, but its detailed oxygen geometry is less secure because the starting topology is analogue-derived; the CIF should not be treated as a high-precision standalone structure determination. Some γ-WO₃ oxygen components also remained at their neutron-parent values when bounded coordinate trials were unstable. The three relative crystalline fractions are supported by multiple reflections, but absolute specimen fractions—and any amorphous material—cannot be determined reliably from this scan alone.
