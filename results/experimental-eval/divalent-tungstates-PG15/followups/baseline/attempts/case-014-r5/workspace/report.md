# PXRD phase analysis

The modeled crystalline assemblage is scheelite SrWO4, monoclinic WO3, and orthorhombic SrCO3. The refined weight fractions, normalized only over these crystalline phases, are:

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| SrWO4 | I 41/a | a = 5.41862, c = 11.96096 | 80.05 wt% |
| WO3 | P 21/n | a = 7.30068, b = 7.53965, c = 7.69640, β = 90.7829 | 12.29 wt% |
| SrCO3 | P n m a | a = 6.06914, b = 5.13636, c = 8.08872 | 7.66 wt% |

## Evidence

The dominant pattern is indexed by scheelite SrWO4, including the strong 112, 004, 020, 024, 220, and 132 families near 27.95, 30.18, 33.36, 45.43, 47.72, and 56.06° 2θ. The diagnostic three-line region near 23.42, 23.91, and 24.69° and numerous higher-angle reflections require room-temperature monoclinic WO3. Residual SrCO3 is supported by the intense line at about 29.75° (200) and weaker/overlapped features near 35.3, 44.6, and 48.7°. Its unusual line ratios require strong [100] preferred orientation; the submitted model uses a fixed March–Dollase coefficient of 0.2377.

Starting structures were COD 1546036 (SrWO4), 1528915 (WO3), and 9008198 (SrCO3). Lattice parameters, displacement/profile terms, phase scales, background, and isotropic microstrain were refined in GSAS-II; atomic coordinates were retained from the reference structures because this laboratory pattern does not support stable coordinate refinement. Plausible alternatives including fergusonite SrWO4, SrO2, high-pressure SrCO3, SrO, and Sr3W2O9 were tested. The first two refined to zero, while SrO and Sr3W2O9 gave only sub-1-wt% scales, trivial fit improvements, and no unique diagnostic peak, so no fourth phase is claimed.

The final fit has Rwp = 13.52%, Rp = 9.28%, Rexp = 3.54%, and goodness of fit = 3.83 for 8,282 points. Because pointwise uncertainties were not supplied, weights used the Poisson approximation σ = √counts. The measured Cu Kα1/Kα2 wavelengths and 0.5 intensity ratio from the metadata were used.

## Uncertainty

The SrCO3 fraction is not reliably determined as a unique quantitative value. If its texture coefficient and scale are refined together, they correlate at 99.99%; equally defensible texture assumptions move its modeled fraction from below 1 wt% to roughly 10 wt%. The listed 7.66 wt% is therefore a semi-quantitative, physically plausible fixed-texture estimate, not a precise determination. Its b and c lattice parameters are likewise weakly constrained because most non-h00 lines are weak or overlap WO3. This texture ambiguity also shifts the normalized SrWO4 and WO3 fractions by several percentage points. Formal least-squares fraction uncertainties in `result.json` exclude this dominant systematic effect.

The elevated goodness of fit and structured residuals reflect the absent instrument-profile calibration, overlapping textured precursor peaks, and remaining profile/intensity mismatch. No amorphous fraction can be obtained without an internal standard, and an additional crystalline phase below about 1 wt% cannot be excluded.
