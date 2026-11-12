# Powder XRD phase analysis

## Result

The pattern is described by three crystalline phases. Weight fractions are normalized only over these modeled crystalline phases.

| Phase | Structural model | Weight fraction |
|---|---|---:|
| ZnWO4, wolframite | monoclinic `P 2/c` | 0.74648 (74.65 wt%) |
| WO3, gamma-monoclinic | monoclinic `P 21/c` | 0.19325 (19.33 wt%) |
| ZnO, wurtzite | hexagonal `P 63 m c` | 0.06027 (6.03 wt%) |

The full 9.9034–100.0949° 2theta range (8301 points) gives `Rwp = 5.6040%`, `Rp = 4.4694%`, `Rexp = 3.7916%`, and goodness of fit `Rwp/Rexp = 1.4780`. A fresh, no-optimization GSAS-II replay reproduced the exported profile and fractions exactly to numerical precision.

## Evidence and model selection

The 900 °C ZnO + WO3 context is chemically consistent with ZnWO4 formation and residual reactants, but the inventory was selected from the diffraction evidence. Wolframite ZnWO4 accounts for the dominant split families throughout the scan. A second coherent family at approximately 23.27/23.76/24.53°, 33.4–34.3°, 47–50°, and 55–56° is accounted for by gamma-WO3. Adding wurtzite ZnO accounts for its linked 31.92°, 34.58°, 36.40°, 47.68°, 56.71°, 62.98°, and 68–69° families and reduced Rwp from about 7.20% to 5.85% before final profile refinement.

Several WO3 records and polymorphs were challenged under the same nuisance model. Tetragonal, orthorhombic, and hexagonal alternatives gave substantially poorer fits. A triclinic `P -1` WO3 record was nearly profile-degenerate with the selected model, but its refined metric moved toward monoclinic symmetry and beyond the plausible source-cell perturbation. The room-temperature `P 21/c` gamma-WO3 record was therefore retained. Cubic rocksalt and zincblende ZnO trials refined to effectively zero scale; only wurtzite was supported.

The final baseline uses the supplied Cu Kalpha doublet, a smooth eight-term Chebyshev background, one specimen-displacement correction (-314.7 micrometres for a 200 mm radius), refined axial asymmetry and low-angle surface roughness, and phase-specific isotropic sizes. Coupled common-width trials were ill-conditioned, so a nonnegative low-dimensional instrument profile (`U = 0`, `W = 40`, `X = 1` in GSAS-II units) was fixed before refining the phase widths; these nuisance values and the resulting sizes are not interpreted as standalone materials measurements. Isotropic strain is retained only for WO3 (about 3630 ppm). Preferred-orientation trials returned ratios close to one. ZnWO4 anisotropic-strain trials drove one component to zero and lost their apparent improvement on replay, so texture and anisotropic broadening were pruned. Published, physically screened atomic coordinates and a common `Uiso = 0.005 A^2` were retained; releasing coordinates or ADPs did not give a stable replay improvement.

## Remaining uncertainty

The phase inventory and relative crystalline fractions are well supported, but these fractions do not measure amorphous material or absolute reaction yield. Conditional scale-factor standard uncertainties are only about 0.09–0.13 wt%, while profile/source correlations make realistic systematic uncertainties larger; approximately +/-2 wt% for ZnWO4, +/-1.5 wt% for WO3, and +/-1 wt% for ZnO are more defensible than the formal errors.

The exact low-symmetry description of WO3 is not uniquely resolved: a pseudo-triclinic description fits almost as well, so `P 21/c` should be regarded as the preferred physically constrained model rather than a symmetry proof. Oxygen coordinates, especially in WO3, are source-model values rather than independently precise results from this laboratory pattern. No fourth phase has coherent unique residual families, although a trace or completely overlapped component cannot be excluded. The largest remaining residuals alternate across strong split peaks and are more consistent with imperfect line-shape modeling than with an omitted phase.
