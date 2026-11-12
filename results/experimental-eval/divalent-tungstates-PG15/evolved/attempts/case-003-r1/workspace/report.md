# Quantitative phase analysis

Three crystalline phases are required. Fractions are normalized over those modeled crystalline phases.

| Phase | Space group | wt% (formal ESD) | Refined cell | CIF |
|---|---:|---:|---|---|
| CaWO4 | I 41/a | 13.04 ± 0.13 | a=5.24584, c=11.38482 Å | `CaWO4.cif` |
| WO3 | P 21/c | 56.78 ± 0.23 | a=7.69758, b=7.54160, c=10.54942 Å, β=136.1471° | `WO3.cif` |
| CaCO3 | R -3 c (hexagonal setting) | 30.17 ± 0.29 | a=4.99038, c=17.07540 Å | `CaCO3.cif` |

The formal scale-factor uncertainties understate model uncertainty. A conservative sensitivity estimate is about ±1 wt% for CaWO4 and ±2.5 wt% each for WO3 and CaCO3, mainly from overlap and preferred-orientation modeling. No amorphous fraction or absolute crystalline content can be obtained without an internal standard.

## Evidence

The chemistry is consistent with partial reaction of the stated CaCO3 + WO3 precursors at 500 °C. Scheelite CaWO4 is fixed by its 18.9°, 29.0°, 31.7°, 34.5°, 47.5° and 58.2° families. Monoclinic WO3 is especially diagnostic through the resolved 23.42°/23.90°/24.67° triplet and many higher-angle split families. Calcite is required by 29.71°, 39.72°, 43.47°, 47.8°, 48.8° and 57.7° families.

Ambient, fully occupied COD models 7219229 (scheelite), 2311041 (monoclinic WO3) and 1547347 (calcite atom model) were physically screened and used. Alternative source records or polymorphs were replayed under the same nuisance model: triclinic WO3 gave Rwp 8.99%, an alternate monoclinic WO3 record 11.03%, high-pressure fergusonite CaWO4 8.84%, aragonite 14.92%, and monoclinic CaCO3 11.29%, versus 8.74% for the corresponding common-profile inventory. The selected records also give chemically sensible density and coordination after cell refinement.

## Refinement and fit

The final GSAS-II replay used the full 9.990–100.095° range, the supplied Cu Kα1/Kα2 wavelengths and 0.5 Kα2/Kα1 ratio, a smooth six-term Chebyshev background, one zero correction (0.3025°), nonnegative common W broadening with U=X=0, and refined polarization (0.593). Supported phase broadening was retained as uniaxial CaWO4 size along [001], isotropic WO3 size plus uniaxial WO3 microstrain along [011], and isotropic calcite strain. March–Dollase terms were retained only after no-texture and symmetry-distinct-axis comparisons: CaWO4 [110], WO3 [010], and calcite [104]. Releasing U made it negative; releasing X made it >0.94 correlated with phase width terms. A second WO3 anisotropic size term was >0.90 correlated with strain and was pruned.

Final statistics are Rwp=8.122%, Rp=6.273%, Rexp=2.394%, GOF=3.398, with 8293 points and 29 refined parameters. Pointwise uncertainties were not supplied, so these statistics use count-statistical weights; the GOF above one reflects residual systematic mismatch as well as counting noise.

## Remaining uncertainty

Plausible trace phases were re-challenged against the final common profile. Ca3WO6 and W18O49 refined to zero. Nominal CaO and Ca–W bronze contributions were below 0.3 wt% and strongly width-dependent. Ca(OH)2 ranged from 0.45 to 1.79 wt% when its fixed crystallite size was changed from 10 to 0.03 µm; moreover, its strongest unique 001 line at 18.36° worsened rather than improved the residual, while most apparent gain came from overlapped peaks. Their structures/fractions therefore cannot be determined reliably and they are not included. Sharp-phase sensitivity is roughly sub-1 wt%; a non-specific broad-phase surrogate can approach 2 wt%.

Atomic coordinates, occupancies and displacement parameters were held at their physically screened source values; only lattice metrics and powder/profile terms were refined. Thus the phase identities and cells are supported, but local atomic geometry is not independently determined by this multiphase pattern. `final.gpx`, the submitted CIFs, fractions and `fit.csv` all come from the same reopened final project state.
