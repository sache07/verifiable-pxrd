# Powder XRD phase analysis

The pattern is modeled by three crystalline phases: wolframite ZnWO4, monoclinic WO3, and wurtzite ZnO. The refined fractions below are normalized only over those modeled crystalline phases; no amorphous fraction can be inferred from this measurement.

| Phase | Space group | Refined cell (A, deg) | Crystalline wt.% |
|---|---|---|---:|
| ZnWO4 (wolframite) | P 2/c | a=4.70054, b=5.73226, c=4.93140, beta=90.63746 | 81.799 |
| WO3 (monoclinic) | P 21/n | a=7.30814, b=7.52005, c=7.70274, beta=90.90974 | 13.098 |
| ZnO (wurtzite) | P 63 m c | a=3.25447, c=5.18194 | 5.103 |

The independently regenerated full-grid fit has Rwp=3.0353%, Rp=2.2327%, and GOF=1.1480 over 8301 observations. It reproduces the phase fractions in `result.json`, gives no negative-profile or geometry review flags, and all three CIFs pass the occupancy/contact screen.

## Evidence

ZnWO4 accounts for the dominant wolframite family, including reflections near 15.77, 19.19, 24.10/24.79, and 30.72/30.97 degrees 2-theta. A distinct WO3 family includes the split peaks near 23.40, 23.96, and 24.66 degrees and further reflections near 33.59-34.50 degrees. Weak but repeatable ZnO reflections occur at 32.03, 34.90, 36.56, 47.93, and 56.79 degrees. Its refined scale remains positive and stable, and residual ZnO is chemically economical given the WO3 + ZnO precursor mixture heated at 700 C. Every coherent residual reflection family is indexed by these phases, so no additional phase was added.

The ZnWO4 model was obtained by cross-chemistry transfer of wolframite prototypes and then adapted by staged cell, heavy-atom, oxygen-coordinate, displacement, texture, and profile refinement; distinct physical coordinate starts were tested. WO3 was initialized from a physical monoclinic reference (COD 2311041) transformed into the reduced P21/n setting. ZnO used a wurtzite reference (COD 9004178). Preferred orientation was required reproducibly for both monoclinic phases and ZnO. Isotropic microstrain and surface-roughness additions collapsed or became nonphysical and were rejected.

## Remaining uncertainty

The formal GSAS-II fraction standard uncertainties are only about 0.03-0.04 wt.%-point, but they omit model uncertainty. Texture, common displacement parameters, and the correlated specimen-height/zero/cell calibration moved trial fractions by roughly 0.5-1 wt.%-point, so the defensible reporting precision is approximately 81.8, 13.1, and 5.1 wt.% rather than all digits stored in `result.json`. The specimen displacement (-700 micrometers) lies in a shallow correlated minimum with zero (-0.07330 degrees); the refined cells are therefore conditional on that calibration model.

WO3 oxygen coordinates could not be refined independently without unstable/bound-limited motion and are retained from the physical reference; its topology, cell, and W sublattice are supported, but the detailed oxygen substructure is not reliably determined by this pattern. Likewise, the weak ZnO phase supports the wurtzite identity and fraction, but not an independent refinement of its O internal coordinate. No claim is made for unmodeled amorphous material.
