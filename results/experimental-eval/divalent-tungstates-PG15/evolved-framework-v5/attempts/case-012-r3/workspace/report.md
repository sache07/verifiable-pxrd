# Powder X-ray diffraction phase analysis

## Result

The specimen is modeled as two crystalline phases. Weight fractions are normalized over these modeled crystalline phases; they do not measure any amorphous content.

| Phase | Structural model | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| Nickel tungstate, NiWO₄ (wolframite) | Monoclinic P2/c; COD 5910277 topology | a = 4.60092, b = 5.66368, c = 4.91140, β = 89.9803 | 0.7651 (76.51 wt%) |
| Tungsten(VI) oxide, WO₃ | Monoclinic P2₁/c; COD 2311041, non-conventional source setting | a = 7.68971, b = 7.53448, c = 10.5294, β = 136.089 | 0.2349 (23.49 wt%) |

The native GSAS-II atomic forward replay over the complete 10.0094–99.9944° 2θ grid gives Rwp = 4.06896%, Rp = 3.13231%, Rexp = 3.47879%, and Rwp/Rexp = 1.16965. The replay regenerated the structure factors and reflection lists rather than using a cached calculated curve. It returned no physical profile-review flags; the calculated profile and background are positive throughout.

## Evidence

The NiO + WO₃ precursor chemistry and 900 °C firing make NiWO₄ the ordinary reaction product. The P2/c wolframite model accounts for the majority family, including peaks near 19.19, 23.91, 24.85, 30.87, 36.52, 41.63, and 54.58° 2θ. A NiWO₄-only refinement left a coherent second family: the diagnostic 23.06/23.53/24.28° triplet, the 33.20–34.09° group, and reflections near 49.87 and 55.88°. These are jointly indexed by monoclinic WO₃. After adding it, no coherent residual reflection family remains.

Alternative WO₃ references were checked. A triclinic same-composition model gave only a marginal preliminary Rwp decrease (4.426% versus 4.432%), while its refined α and γ angles collapsed toward 90°. The physically ordinary room-temperature monoclinic P2₁/c model was therefore retained. An older monoclinic WO₃ model was materially worse (Rwp 4.818% at the same checkpoint).

A rocksalt NiO trial refined to only 0.17 wt% and changed Rwp from 4.06896% to 4.06844%, without support from a broad independent peak family. NiO is therefore not reported as a determined phase; a trace fraction at roughly the sub-percent level cannot be established reliably from this pattern.

## Refinement and uncertainty

Cells, phase scales, background, physically bounded profile terms, heavy-atom coordinates, and the NiWO₄ oxygen coordinates were refined. The final geometries are chemically reasonable: Ni–O = 1.979–2.072 Å and W–O = 1.830–2.151 Å in NiWO₄; W–O = 1.726–2.145 Å in WO₃. Texture trials relaxed to unity and were omitted.

The phase identities are high confidence, and the phase fractions were stable across accepted profile/calibration branches. A conservative model-dependent uncertainty is about ±1 wt% absolute for each normalized crystalline fraction. The detailed WO₃ oxygen displacements are less well determined by these Cu-radiation powder data: unconstrained oxygen refinement lowered Rwp slightly but generated a 1.656 Å W–O contact, so the physically credible reference oxygen framework was retained. Thus the WO₃ cell, heavy-atom framework, and phase amount are supported, but its fine oxygen-coordinate details should not be interpreted as independently determined. Possible amorphous material and unsupported sub-percent crystalline traces are outside the reported normalization.
