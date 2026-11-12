# Powder XRD phase analysis

The pattern is described by three crystalline phases. Weight fractions are normalized over these modeled crystalline phases:

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| Scheelite CaWO₄ | *I*4₁/*a* | *a* = 5.24178, *c* = 11.3777 | 0.1313 (13.13 wt%) |
| Calcite CaCO₃ | *R*-3*c* | *a* = 4.98776, *c* = 17.0622 | 0.3115 (31.15 wt%) |
| Monoclinic γ-WO₃ | *P*2₁/*c* | *a* = 7.30451, *b* = 7.53657, *c* = 10.5418, β = 133.149° | 0.5571 (55.71 wt%) |

## Evidence

The chemical context supports an incompletely reacted CaCO₃ + WO₃ mixture after firing at 500 °C. Scheelite CaWO₄ is required by its characteristic reflections near 18.89°, 29.02°, and 31.72° 2θ. Residual calcite is identified independently by the 29.71°, 39.72°, and 43.47° reflections. The dense set of remaining peaks, especially the resolved 23.42°/23.90°/24.67° triplet, is matched by monoclinic γ-WO₃. Alternative WO₃ reference structures were tested; the submitted *P*2₁/*c* model gave the correct peak splitting and the best whole-pattern agreement. No consistent unmodeled reflections required a fourth crystalline phase.

The quantitative model is a GSAS-II Rietveld refinement using the supplied Cu Kα₁/Kα₂ wavelengths and intensity ratio. It includes a smooth background, angular calibration and sample displacement, surface roughness, physically bounded instrumental broadening, phase-dependent crystallite-size/microstrain terms, and weak March–Dollase texture terms. Fractions were calculated from refined phase scale factors and unit-cell masses. Independent forward replay of `final.gpx`, with fresh reflection lists and structure factors, gives Rwp = 7.254%, Rp = 5.292%, and χ² = 76115.6 over 8293 points. The replay found no negative background, invalid peak width, or other profile-validity flag.

## Remaining uncertainty

The phase identities are robust, and all three fractions are determined, but their least-squares standard uncertainties (about 0.08, 0.15, and 0.13 wt-percentage points, respectively) understate systematic uncertainty from severe peak overlap, roughness, texture, and profile/size correlations. Differences smaller than roughly 1–2 wt-percentage points should therefore not be treated as reliable. The reported values do not quantify amorphous material because no external standard was supplied; they sum to 100% only across the modeled crystalline phases.

The unit cells and heavy-atom frameworks are well constrained by the peak positions and intensities. Oxygen coordinates, particularly in WO₃, are less precise from laboratory powder data, so the CIFs are defensible phase models rather than high-precision independent structure determinations. The CaWO₄ size term and one common instrumental-width term reached their physical bounds, so microstructural size/strain values should not be interpreted quantitatively; this does not alter the phase assignment.
