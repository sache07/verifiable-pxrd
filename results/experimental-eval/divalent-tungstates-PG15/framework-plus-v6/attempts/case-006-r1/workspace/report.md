# Powder X-ray diffraction phase analysis

## Result

The modeled crystalline material is **CuWO4, 95.80 wt%**, plus **WO3, 4.20 wt%**. The fractions are normalized over these two crystalline phases. GSAS-II gives a formal standard uncertainty of 0.11 percentage point for either fraction.

| Phase | Structural model | Refined cell | Weight fraction |
|---|---|---|---:|
| CuWO4 | Triclinic `P -1` | a = 4.71249 Å, b = 4.88555 Å, c = 5.84739 Å; α = 88.34498°, β = 82.75051°, γ = 87.46682° | 0.95798 |
| WO3 | Monoclinic `P 21/c` | a = 7.69934 Å, b = 7.54624 Å, c = 10.52149 Å; β = 136.01327° | 0.04202 |

## Evidence and model selection

The dominant peak sequence is the low-symmetry wolframite-related CuWO4 pattern expected from the CuO/WO3, 800 °C chemical context. Exact CuWO4 database records tested initially did not reproduce the complete line sequence. A composition/symmetry analogue search identified the Cu-rich `(Cu0.9Zn0.1)WO4` neutron model COD 2101690 in `P -1`; replacing the residual divalent-site Zn label with Cu gives the chemically appropriate CuWO4 model and matches the observed low-, middle-, and high-angle families. Its cell and all Cu/O coordinates were refined, with W fixed as the origin anchor.

The remaining coherent peaks are fitted by monoclinic WO3 (COD 2311041). Support includes separated or partly separated families near 23.42, 24.68, 33.56/33.83, 42.21, 56.21, and 76.95° 2θ. Adding this phase reduced Rwp from about 7.86% for the common-profile one-phase model to 6.97%; its supported anisotropic broadening reduced the final Rwp to 6.90%. Other physically viable low-symmetry WO3 records were inferior under the same nuisance model. CuO, Cu2O, Cu3WO6, Cu2WO4, and tetragonal/hexagonal WO3 watch-list challenges refined to zero or unsupported trace scales and were rejected.

The full 9.903–100.095° range was refined with the stated Cu Kα1/Kα2 doublet, count-based Poisson weights, a six-coefficient smooth background, one zero correction, common W/X peak-width terms, polarization, and a frozen converged roughness correction. Unsupported size and preferred-orientation terms were removed. Both exported structures pass the geometry/occupancy screen, the background remains positive, and an independent no-refinement GSAS-II replay reports no profile-review flags. Final statistics are Rwp = 6.9006%, Rp = 5.1289%, goodness of fit = 2.8426, and χ² = 66758.6 for 8301 observations and 39 varied parameters.

## Remaining uncertainty

The existence of both phases and the dominant CuWO4 structure are reliable. The formal fraction uncertainty does not include structural/profile model choice; a more realistic systematic uncertainty for the minor WO3 amount is roughly ±0.5 percentage point. At only about 4 wt% and with substantial overlap, the WO3 atomic coordinates cannot be determined reliably from this pattern, so they were retained from the physically screened parent while only its cell, scale, and symmetry-appropriate strain were refined. The elevated goodness of fit and small structured residuals indicate remaining line-shape/coordinate imperfections, but no additional phase has coherent support.
