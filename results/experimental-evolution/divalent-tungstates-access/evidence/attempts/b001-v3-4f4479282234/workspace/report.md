# Powder XRD phase analysis

## Result

The pattern is described by three crystalline phases. Weight fractions are normalized over those phases; parenthesized uncertainties below are internal 1σ scale-covariance estimates and do not include model-choice systematics.

| Phase | Structure | Weight fraction | Refined unit cell (Å, °) |
|---|---|---:|---|
| CaWO4 | scheelite, I 41/a | 80.24(0.15) wt% | a = 5.23780, c = 11.33416 |
| WO3 | monoclinic gamma-WO3, P 21/c | 13.58(0.05) wt% | a = 7.69379, b = 7.55681, c = 10.51781, beta = 135.94707 |
| CaCO3 | calcite, R -3 c | 6.19(0.17) wt% | a = 4.98626, c = 17.05894 |

## Evidence and chemical interpretation

CaWO4 is the dominant fired product. Monoclinic WO3 and calcite account for coherent residual families from unreacted precursors. In particular, calcite indexes the previously unassigned family at approximately 22.74, 29.08, 31.11, 35.67, 39.11, and 42.86° 2θ; its scale remained positive after independent cell, size, strain, texture, coordinate, and displacement-factor tests.

The inventory is chemically economical for CaCO3 + WO3 -> CaWO4 + CO2. Per 100 g of crystalline material, the model contains 0.3405 mol Ca and 0.3372 mol W, a 0.96% relative mismatch. No cross-chemistry transferred phase is needed.

Starting prototypes were COD 7219229 (scheelite CaWO4), COD 2311041 (monoclinic WO3), and COD 1547347 (calcite), followed by symmetry-preserving cell, coordinate, displacement, and profile refinement. The final structures pass the necessary contact/occupancy screen; refined W-O distances in WO3 are 1.73-2.21 Å and the calcite C-O distance is 1.253 Å.

## Fit and validation

The final native replay gives Rwp = 3.1996%, Rp = 2.4654%, and GOF = 1.0210 over 8301 points from 9.903 to 100.095° 2θ. `final.gpx` was replayed without parameter optimization or hidden-input access, and regenerated the submitted CIFs and fractions. The background and total calculated pattern remain positive, and there are no profile-review flags.

After smoothing the standardized residual over about 0.04° 2θ, the largest positive maximum is 1.44σ and no maximum exceeds 2σ. The remaining maxima coincide with reflections of the accepted phases, so there is no coherent unassigned reflection family warranting another phase.

## Remaining uncertainty

The formal fraction uncertainties are optimistic. Calcite is weak and its scale is correlated with crystallite size and a uniform Uiso near the allowed upper range; a practical uncertainty of roughly 0.5-1 wt% is more realistic than its internal 0.17 wt% standard uncertainty. WO3 oxygen coordinates are less secure than its cell and W sublattice because Cu Kα scattering is W-dominated, although site-by-site refinements remained physically valid. Instrument zero and specimen displacement are 99.6% correlated; they should be treated as joint nuisance calibration. The Gaussian U profile term reached the physical boundary U = 0 and was fixed there, while all total peak widths remained positive.

The delivered `fit.csv`, CIFs, fractions, and statistics all derive from the same saved `final.gpx` replay.
