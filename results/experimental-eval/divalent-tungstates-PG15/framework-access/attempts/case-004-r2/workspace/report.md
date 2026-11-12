# PXRD phase analysis

## Result

| Crystalline phase | Structural model | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| CoWO₄ | Wolframite, `P 2/c` | a = 4.67134, b = 5.68675, c = 4.95265, β = 89.993 | 0.2914 (29.14 wt%) |
| WO₃ | Monoclinic, `P 21/n` | a = 7.30915, b = 7.54058, c = 7.69594, β = 90.810 | 0.7086 (70.86 wt%) |

The fractions are normalized over the two modeled crystalline phases. They do not measure any amorphous content.

## Evidence

The CoO + WO₃ chemical context and 900 °C treatment make CoWO₄ formation with residual WO₃ chemically plausible. The monoclinic WO₃ model accounts for the dominant group near 23–25° 2θ and its higher-angle sequence. The wolframite CoWO₄ model is required for the distinct reflections near 19.1°, 30.7°, 36.4°, and 54.2° 2θ. Adding CoO or Co₃O₄ did not produce a positive stable scale, and alternative WO₃ models fit materially worse, so no third crystalline phase is supported.

The CoWO₄ model was adapted from the isostructural MgWO₄ wolframite framework by replacing Mg with Co, then refining the cell and tightly bounded atomic coordinates. The WO₃ model derives from the monoclinic `P 21/n` reference (COD 1528915). A small `[111]` March–Dollase correction was retained for WO₃ (ratio 0.887). The final full-grid fit has Rwp = 6.168%, Rp = 4.544%, and GOF = 1.882 for 8,301 points. Independent GSAS-II replay of `final.gpx` regenerated the same curve and fractions, with no negative-background, negative-width, or other profile-review flags.

## Remaining uncertainty

The phase identities are high confidence. The relative fractions are moderately robust: reasonable profile/texture variants moved the CoWO₄ estimate by about one absolute weight percent, but a conservative systematic uncertainty is approximately ±2–3 wt% because the phases overlap strongly and polarization/profile parameters are not independently calibrated.

Fine oxygen coordinates are not reliably determined by this powder pattern alone. Unconstrained oxygen refinement produced chemically implausible displacements, so the submitted coordinates were kept within 0.008 fractional units of their reference frameworks. The CIFs are therefore defensible average structural models, but especially the detailed WO₃ oxygen geometry should be regarded as provisional rather than an independently solved structure.
