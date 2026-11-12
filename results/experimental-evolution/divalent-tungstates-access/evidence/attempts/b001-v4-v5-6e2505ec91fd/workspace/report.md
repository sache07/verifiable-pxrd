# Powder XRD phase analysis

The pattern is described by four crystalline phases. Weight fractions are normalized over these modeled crystalline phases:

| Phase | Structural model | Weight fraction |
|---|---|---:|
| CuWO4 | triclinic `P -1`, COD 4000806 | 64.892 wt% |
| Cu3WO6 | cubic `P a -3`, COD 1527404 | 13.328 wt% |
| WO3 | monoclinic `P 21/c`, COD 2311041 | 19.148 wt% |
| CuO | monoclinic `C 2/c`, COD 1011194 | 2.633 wt% |

## Evidence and refinement

The inventory is chemically consistent with the CuO + WO3, 700 °C synthesis context. CuWO4 accounts for the dominant family (including reflections near 15.01, 18.81, 25.46, 29.09, and 30.08° 2θ). Independent families require Cu3WO6 (15.18, 19.80, 21.76, 32.51, and 33.76°), WO3 (especially the 22.67/23.07/23.89° group), and residual CuO (notably near 35.1, 38.3, and 61.2°). Each accepted phase has a positive stable scale and broad reflection-family support; no coherent family remains unassigned.

The final full-grid GSAS-II fit has `Rwp = 1.8169%`, `Rp = 1.3719%`, `Rexp = 1.6163%`, and goodness of fit `1.1260` for 8301 points. The model includes refined cells and symmetry-constrained coordinates, one isotropic Uiso per phase, CuWO4 crystallite size (0.169 µm), and WO3 [001] uniaxial microstrain (1543/2126 ppm). Preferred orientation and surface roughness were tested but rejected because they returned unity/boundary values without material improvement. An independent atomic forward replay of `final.gpx` reproduced the reported Rwp and found no negative background, negative analytic peak width, or nonphysical displacement tensor. Shortest final contacts are chemically reasonable: W–O 1.736–1.793 Å, Cu–O 1.921–1.938 Å, and O–O at least 2.436 Å across the four structures.

## Uncertainty

Formal 1σ scale-covariance uncertainties are 0.036, 0.023, 0.023, and 0.032 percentage points for CuWO4, Cu3WO6, WO3, and CuO, respectively. These omit systematic effects from overlap, background choice, and reference-model imperfections; realistic fraction uncertainty is therefore larger, particularly for the 2.63 wt% CuO minor phase. The P21/c WO3 model is the best physical broad-family fit among the tested WO3 references, but its detailed oxygen coordinates are less uniquely constrained than those of the dominant CuWO4 phase. No amorphous content or absolute crystalline yield can be inferred from this scan, so the reported fractions must not be interpreted as whole-specimen absolute fractions.
