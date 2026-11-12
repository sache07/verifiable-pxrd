# Powder XRD phase analysis

The 700 °C product from WO3 and CuO is modeled as three crystalline phases. Fractions are normalized over those modeled phases; no amorphous fraction was measured.

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| CuWO4 | P -1 | 4.61678, 5.74196, 4.85486; 91.3226, 91.4807, 84.7026 | 0.6635 |
| Cu3WO6 | P a -3 | a = 9.78197 | 0.1373 |
| WO3 | P 21/c, nonstandard setting | 7.67788, 7.55262, 10.49827; beta = 136.0151 | 0.1992 |

The independently regenerated GSAS-II profile gives Rwp = 4.6226%, Rp = 2.7562%, and goodness-of-fit = 2.8658 using provisional Poisson weights. The replay covers all 8,301 measured points and reports no negative-width, negative-background, ADP, polarization, or other physical-review flag.

## Evidence and phase closure

Cu3WO6 is required by its distinctive reflections near 15.18, 19.80, 32.51, 33.77, 49.67, 57.60, and 63.28° 2theta. Low-symmetry WO3 is required by the 22.67/23.07/23.89° triplet and the 28.14/28.48° pair. The remaining dominant families are indexed by triclinic CuWO4. Under a common screening protocol, CuWO4 + Cu3WO6 alone gave Rwp = 25.52%; adding the selected WO3 model reduced it to 9.06% before coordinate and profile refinement. All three refined scales remain positive.

After the three-phase inventory was introduced, the largest residuals became adjacent positive/negative lobes at modeled reflections rather than a coherent family of new reflections. CuO additions were therefore not retained. Bounded coordinate, texture, roughness, axial-divergence, and specimen-height branches either failed independent replay, gave negligible improvement, hit bounds, or were unstable; the simpler rollback was retained.

## Candidate ledger

| Candidate or branch | Status | Main result |
|---|---|---|
| CuWO4, COD 4000806, P -1 | accepted | Best same-formula model and dominant phase. |
| CuWO4, COD 4000807, P 2/c | rejected | Common screen Rwp 53.99% with substantial cell drift. |
| Cu3WO6, COD 1527404, P a -3 | accepted | Explains multiple otherwise unindexed peak families. |
| Cu2WO4, COD 2002403, P1 | rejected | Oxidation labels were repaired for import; Rwp 55.33% and distorted trial cell. |
| WO3, COD 2311041, P 21/c | accepted | Best fixed-atom WO3 screen, Rwp 9.06% in the three-phase inventory. |
| WO3, COD 2106293, P -1 | rejected | Rwp 9.30%, but required implausible angular cell changes beyond the analogue-mismatch allowance. |
| WO3, COD 1528915, P 21/c | rejected | Common three-phase screen Rwp 10.28%. |
| WO3, COD 2107312 / 1521533 / 1521532 | rejected | Common-screen Rwp 18.39%, 21.66%, and 24.13%, respectively. |
| WO3, COD 1004057, P 6/mmm | rejected | Scale collapsed; a later invalid-cell trial was not used as evidence. |
| WO3, COD 1010618 and 1563541 | unknown | One cell trial diverged and one CIF had an oxidation-label import fault; neither was counted as rejected. Fixed/source-pattern checks were much poorer than the selected model. |
| CuO, COD 1011194 and 9016057 | rejected | No residual CuO family; individual common screens remained near Rwp 55.9%. |

No foreign-composition prototype substitution was nominated after closure because there was no remaining coherent unindexed reflection family; the residuals track already modeled peaks.

## Refinement and uncertainty

The final model uses the stated Cu Kalpha1/Kalpha2 wavelengths and intensity ratio, a 12-term Chebyshev background, refined phase scales and cells, and isotropic phase profiles. Coordinate shifts were regularized to physically plausible parent-model displacements, and all final coordinates and occupancies pass the geometry screen. Effective domain sizes are about 0.102, 0.296, and 0.188 micrometres for CuWO4, Cu3WO6, and WO3. The CuWO4 and Cu3WO6 isotropic microstrains are about 303 and 537 ppm; WO3 strain was held at 1000 ppm. These profile values are an effective decomposition, not uniquely measured instrument/specimen properties.

The phase inventory is reliable, but the exact WO3 polymorph is less secure than its WO3 composition because another low-symmetry model was metrically close only after excessive cell distortion. Oxygen coordinates, especially in WO3 and Cu3WO6, are weakly constrained by laboratory X-ray data and should not be treated as a unique structure solution. The fitted angular zero of -0.4798° is an effective correction and may absorb specimen-height error; attempts to separate those terms were unstable and were not retained. Because pointwise uncertainties were not supplied and systematic residuals remain, formal fraction errors would be misleading; profile/candidate trials suggest approximately 1–2 weight-percentage-point model dependence in the reported fractions.
