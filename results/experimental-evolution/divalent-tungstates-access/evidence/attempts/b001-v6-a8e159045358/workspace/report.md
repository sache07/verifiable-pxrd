# Powder XRD phase analysis

The 700 °C CuO/WO₃ specimen is a four-phase crystalline mixture. Weight fractions are normalized over the modeled crystalline material; the pattern does not determine an amorphous fraction.

| Phase | Structural model | Refined cell | Crystalline wt.% |
|---|---|---|---:|
| CuWO₄ | triclinic *P* -1, COD 4000806 | a = 4.62219 Å, b = 5.74808 Å, c = 4.85990 Å; α = 91.3239°, β = 91.4796°, γ = 84.7019° | 65.29 ± 0.04 |
| WO₃ | monoclinic *P* 2₁/c, COD 2311041 | a = 7.68519 Å, b = 7.55933 Å, c = 10.5088 Å; β = 136.008° | 19.08 ± 0.03 |
| CuO | monoclinic *C* 2/c, COD 1011194 | a = 4.66971 Å, b = 3.43077 Å, c = 5.11967 Å; β = 99.5388° | 2.42 ± 0.03 |
| Cu₃WO₆ | cubic *Pa* -3, COD 1527404 | a = 9.79228 Å | 13.22 ± 0.03 |

The quoted uncertainties are covariance-only formal standard uncertainties. They do not include model selection, calibration, or coordinate/profile correlation and therefore understate the practical uncertainty, most notably for the minor CuO fraction.

## Evidence

CuWO₄ accounts for the dominant low-symmetry family at approximately 15.01, 18.81, 25.46, 29.09, 30.08, and 31.4° 2θ. Monoclinic WO₃ is required by its characteristic 22.7–23.9° triplet and its associated higher-angle family. CuO has a positive stable scale and explains the coherent minor family near 35.09, 38.31, 48.1, and 61.17°. Cu₃WO₆ is required by reflections near 15.18, 19.79, 32.49, 33.77, 42.85, 49.69, 50.61, 57.61, and 60.06°; adding it removes the large residual family left by a CuWO₄/WO₃/CuO model. No coherent residual reflection family remained after these four phases were included.

Exact-composition reference checks favored COD 4000806 for CuWO₄ and COD 2311041 for WO₃. The two tested CuO descriptions fitted almost identically, so the conventional higher-symmetry *C* 2/c tenorite model was selected over the lower-symmetry alternative. All submitted models have ordinary oxide coordination and no catastrophic short contacts: minimum Cu–O and W–O distances are 1.92–1.95 Å and 1.72–1.79 Å, respectively.

## Refinement and uncertainty

The GSAS-II model uses the reported Cu Kα₁/Kα₂ doublet and Bragg–Brentano geometry. Phase scales and cells, angular zero, a smooth 15-term background, common instrumental profile, polarization, per-phase size/strain terms, and one common isotropic displacement parameter per phase were stabilized. Only WO₃ showed supported directional microstrain, along its unique b axis. Preferred-orientation tests gave ratios effectively equal to one. Surface roughness refined to opposing bounds and was rejected as non-identifiable.

The converged submitted checkpoint has Rwp = 3.439%, Rp = 2.479%, Rexp = 1.614%, and goodness of fit = 2.131 over 8,301 observations. The angular zero is -0.01859° and the specimen-displacement term is +800 µm, at the physical search limit; because no calibrated instrument profile was supplied, these correlated calibration terms should not be over-interpreted.

The required bounded coordinate polish was run once. All three coordinate orders reached essentially the same lower Rwp (~1.857%) and stable phase fractions, but each failed the helper's final coordinate convergence criterion after bound rollbacks (maximum shift/esd ~1.52, required ≤1). The helper therefore retained the fully converged pre-polish checkpoint. Consequently, the phase identities, cells, and fractions are reliable at the stated practical level, but atom positions beyond the selected reference topologies cannot be claimed as independently refined from this pattern.
