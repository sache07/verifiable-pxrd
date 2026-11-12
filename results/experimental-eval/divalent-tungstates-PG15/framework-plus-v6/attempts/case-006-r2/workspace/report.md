# Powder XRD phase analysis

## Result

The crystalline product is modeled as triclinic CuWO4 (space group P -1) with a small amount of unreacted monoclinic WO3 (space group P 21/c). Fractions are normalized over these modeled crystalline phases:

| Phase | Refined cell (angstrom, degrees) | Crystalline weight fraction |
|---|---|---:|
| CuWO4 | a = 4.70815, b = 5.84233, c = 4.88129; alpha = 91.6549, beta = 92.5339, gamma = 82.7488 | 0.97582 (97.58 wt%) |
| monoclinic WO3 | a = 7.68860, b = 7.53800, c = 10.51937; beta = 136.0538 | 0.02418 (2.42 wt%) |

The final full-range fit (9.9034-100.0949 degrees 2-theta, 8301 points) has Rwp = 6.879%, Rp = 5.030%, Rexp = 2.433%, and goodness of fit = 2.827. The quoted Rexp and goodness of fit use 1/max(counts, 1) weights because pointwise uncertainties were not supplied.

## Evidence and model selection

The CuO + WO3 reaction context at 800 degrees C is consistent with CuWO4 plus a small residual WO3 fraction. The dominant peak positions are indexed by the ambient triclinic CuWO4 cell across the full angular range. The available exact-composition CuWO4 parent (COD 4000806) was measured under pressure, so its coordination topology was retained but its source cell was rejected and the ambient cell and symmetry-preserving coordinates were refined against this pattern. The resulting model is physically plausible: representative nearest Cu-O and W-O ranges are approximately 1.89-2.45 and 1.80-2.25 angstrom, respectively.

A CuWO4-only baseline gave Rwp = 8.533%. Adding monoclinic WO3 COD 2311041 accounted for coherent unique and partly overlapped reflection families and reduced the comparable baseline Rwp to 7.809%; two other WO3 records gave 7.861% and 8.038%. The selected WO3 model remains geometrically sound (shortest W-O approximately 1.71 angstrom). Subsequent common-profile refinement produced the final Rwp above.

The final inventory was re-challenged after rebuilding the shared profile. CuO, Cu2O, Cu2WO4, and a high-pressure CuWO4 polymorph refined to zero scale. Cu3WO6 refined to only 0.076 wt%, and Cu4O3 to 0.276 wt%, with negligible Rwp changes and no convincing set of isolated reflections; neither was retained. Thus Cu4O3 remains, at most, a sub-quantification-limit watch-list possibility rather than an identified phase.

The physically adequate profile uses one specimen-displacement correction, a smooth eight-term Chebyshev background, nonnegative W/X peak-width terms, and axial-divergence asymmetry. Low-angle surface roughness, CuWO4 [100] uniaxial microstrain, weak [110] March-Dollase texture, and WO3 isotropic size broadening were accepted only after full-range replay; unsupported U broadening, main-phase size, WO3 strain, and refined polarization were pruned. The final project was reopened and independently regenerated from atomic structure factors and fresh reflection lists without optimization; it reproduced both fractions exactly and raised no profile-review flags.

## Remaining uncertainty

The minor-phase amount is robustly nonzero, but its practical model sensitivity is about 2.2-2.6 wt% WO3 (roughly 2.4 +/- 0.3 wt%, not a formal one-sigma uncertainty). The complementary CuWO4 fraction has the same absolute uncertainty. These values exclude amorphous material and any crystalline phase below the defensible detection/quantification level.

At only about 2.4 wt%, the WO3 atomic coordinates and displacement parameter cannot be refined reliably from this pattern; the exported CIF therefore uses the selected source coordinates with a refined cell, scale, and peak-size term. Its approximately 0.44 micrometre apparent size is only moderately supported and should not be treated as a precise microstructural measurement. For CuWO4, the cell and framework are well constrained by many reflections, but correlated powder intensities do not support single-crystal-level coordinate or displacement precision; a W positional anchor and a fixed common isotropic displacement parameter were retained. Surface-roughness parameters are also strongly correlated, which is included in the conservative fraction range above.
