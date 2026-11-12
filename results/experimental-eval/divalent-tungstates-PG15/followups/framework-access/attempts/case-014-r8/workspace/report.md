# Powder X-ray diffraction phase analysis

## Result

The crystalline pattern is best described by four phases. Fractions are normalized over these modeled crystalline phases; they do not quantify amorphous material or any unmodeled component.

| Phase | Refined cell (Å, °) | Weight fraction | Assessment |
|---|---|---:|---|
| SrWO4 scheelite, I41/a | a = 5.42352, c = 11.97052 | 0.6287 (62.87 wt%) | Secure phase assignment |
| WO3 monoclinic, P21/c | a = 7.30886, b = 7.54955, c = 7.70308, beta = 90.8250 | 0.1172 (11.72 wt%) | Phase assignment secure; oxygen coordinates less secure |
| SrWO4 fergusonite-like, C2/c | a = 5.14410, b = 11.11471, c = 5.11460, beta = 90.2110 | 0.1124 (11.24 wt%) | Provisional polymorph/analogue assignment |
| Sr3WO6 cubic analogue, Pa-3 | a = 10.94470 | 0.1417 (14.17 wt%) | Provisional composition and structural model |

The final GSAS-II fit has Rp = 6.871%, Rwp = 10.190%, Rexp = 3.535%, and goodness of fit = 2.883 over all 8,282 points from 10.009 to 99.994° 2theta. The independently regenerated, zero-optimization GSAS-II profile exactly reproduces `fit.csv` and the phase fractions from `final.gpx`.

## Evidence

The dominant peak family, including the strong reflections at approximately 28.00, 30.23, 33.40, 45.47 and 47.76° 2theta, indexes as scheelite SrWO4 (COD 1546036). The resolved 23.48/23.95/24.74° triplet and its higher-angle families require monoclinic WO3; the retained COD 1528915 P21/c model fits better than a modern alternative monoclinic coordinate model (best Rwp 10.51% for the latter).

After those two phases, coherent residual families require a second, monoclinic SrWO4 lattice and a broad cubic Sr-W-O component. Adding the monoclinic SrWO4 model reduced Rwp from about 16.47% for the two-phase model to 13.83%. A C2/c SrWO4 model (COD 1546037), refined toward a cell also consistent with an Sr-expanded CaWO4 fergusonite prototype, accounts for this family. The remaining broad lines at about 29.80, 33.10, 51.80, 56.71 and 68.89° are described by a Pa-3 Sr3WO6 model derived by replacing Cu with Sr in the Cu3WO6 prototype (COD 1527404). The complete constrained model reaches Rwp = 10.19%.

As an independent chemical check, the refined phase amounts give nearly equal total Sr and W mole inventories (Sr/W about 1.006), consistent with the stated 1:1 SrCO3:WO3 precursor mixture. Trials with residual SrCO3, SrO2, Sr3W2O9 and alternative tungsten oxides did not yield a comparably stable, physically bounded whole-pattern solution. In particular, an expanded SrO2 or SrCO3 proxy could absorb a few residuals only by using cells well outside the reference-mismatch range; physically bounded versions refined to zero or negligible abundance.

## Remaining uncertainty

The two minor Sr-W-O structures are not uniquely established by this powder pattern. The fergusonite-like assignment uses an analogue/high-pressure structural family, while no exact Sr3WO6 entry was available and its Pa-3 atomic model is prototype-derived. The cubic component also refines to a small coherent domain size (about 0.041 micrometres) and a microstrain bound, making its intensities and fraction strongly model-dependent. Their quoted fractions—and, through overlap, all four fractions—should therefore be regarded as approximate with systematic uncertainty of several percentage points rather than as formal one-sigma values.

The retained historical WO3 coordinates contain a short O...O separation of about 1.56 Å. No impossible contact or occupancy is present, and changing to a geometrically cleaner monoclinic model worsens the fit, but the detailed oxygen sublattice is not reliably determined here. Several positive residuals remain, notably near 22.09, 34.11, 44.62, 53.44, 57.00 and 67.04° 2theta. They may reflect imperfect analogue coordinates/profile anisotropy or a very weak additional component; the data do not support a defensible fifth-phase identity or fraction. The refined angular zero (+0.1546°) and specimen displacement (-447 micrometres) are highly correlated, adding further lattice-parameter systematic uncertainty.
