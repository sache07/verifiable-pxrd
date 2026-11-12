# Powder XRD phase analysis

The pattern is modeled by three crystalline phases. Fractions are normalized over those phases only:

| Phase | Space group | Weight fraction |
|---|---:|---:|
| ZnWO4, wolframite | P 2/c | 82.47% |
| WO3, monoclinic | P 21/c | 12.21% |
| ZnO, wurtzite | P 63 m c | 5.32% |

The dominant peak set indexes as wolframite ZnWO4. Because an exact Zn-W-O entry was not present in the accessible reference index, its starting atomic model was transferred from the isostructural CoMoO4 model COD 7205001 by Co→Zn and Mo→W substitution. It refined to a = 4.70263 Å, b = 5.73386 Å, c = 4.93351 Å, beta = 90.6161 degrees. This model fit better in common-state replacement tests than P2/c models transferred from InNbO4, FeNbO4, InTaO4, MnReO4, and InVO4. Its submitted geometry is physical (shortest W-O and Zn-O distances are about 1.906 and 1.907 Å).

Coherent residual peaks from the product-only fit identify monoclinic WO3 (COD 2311041); adding it reduced Rwp from about 19.1% to 16.1% before the subsequent profile/texture refinements. Competing WO3 references were tested as replacements in the same multiphase state; the submitted P21/c model was preferred, although the triclinic alternative was close enough to remain a structural-model uncertainty. The final WO3 cell is a = 7.31326 Å, b = 7.52202 Å, c = 10.53615 Å, beta = 132.9888 degrees. Unconstrained WO3 coordinate refinement produced nonphysical W-O distances, so the submitted WO3 fractional coordinates were retained from the reference while its cell and profile terms were refined. Individual WO3 coordinates therefore cannot be determined reliably from this overlapped pattern.

A final residual set matches wurtzite ZnO (COD 9004178). Adding fixed-cell ZnO to the physical ZnWO4+WO3 project lowered Rwp from about 10.15% to 9.78% and its scale remained nonzero after full refinement. The final cell is a = 3.25319 Å and c = 5.18501 Å. The ZnO internal coordinate and displacement tensor were retained from the reference because this approximately 5% component does not independently constrain them well. Distinct same-stoichiometry ZnWO4 prototypes (triclinic, scheelite, C2/c, and P21/c) were also screened as additions/replacements. Valid common-state trials did not support them; failed or aborted trials are treated as unknown, not as evidence of absence.

The final GSAS-II model uses the reported Cu K-alpha doublet, a refined empirical background and instrumental zero/profile terms, phase scales/cells, isotropic size, generator-supported uniaxial microstrain for the two monoclinic phases, and March-Dollase texture. A displacement grid was shallow because specimen displacement, zero, and lattice terms are correlated; the selected -500 micrometre displacement is therefore a nuisance model rather than an independently calibrated height. SH/L and zero remain highly correlated (about 97%).

Fresh native atomic replay of `final.gpx` over all 8301 measured points gives Rwp = 9.2595%, Rp = 5.1321%, and goodness of fit = 3.5097 using weights 1/max(Iobs,1); no negative-background, negative-width, or displacement-tensor review flags were raised. The strongest remaining residual near 41.6 degrees lies on overlapping indexed ZnWO4/WO3 reflections and is interpreted as unresolved line-shape/intensity mismatch rather than sufficient evidence for another phase.

The least-squares fraction standard uncertainties are approximately 0.20, 0.11, and 0.19 percentage points for ZnWO4, WO3, and ZnO, respectively, but they do not include structural choice, texture, background, or calibration systematics. The true fraction uncertainty is consequently larger, especially for ZnO and WO3. No internal standard was present, so amorphous material and absolute crystalline yield cannot be quantified.
