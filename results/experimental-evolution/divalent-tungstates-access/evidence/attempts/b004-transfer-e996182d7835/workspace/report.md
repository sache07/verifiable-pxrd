# Powder XRD phase analysis

The crystalline pattern is described by three phases, normalized over the modeled crystalline material:

| Phase | Structural model | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| Ba₃W₂O₉ | trigonal `R -3 c` | a = 10.13193, c = 13.96503 | 0.72172 (72.17 wt%) |
| WO₃ | monoclinic `P 21/c` | a = 7.69304, b = 7.53702, c = 10.52036, β = 136.08435 | 0.22690 (22.69 wt%) |
| BaCO₃ | orthorhombic `P m c n` (Pnma-equivalent setting) | a = 5.30406, b = 8.91316, c = 6.44684 | 0.05139 (5.14 wt%) |

## Evidence

The dominant product was indexed and matched by the Ba₃W₂O₉ `R -3 c` model (COD 1533878), including the characteristic groups near 16.42, 17.71, 26.20, 27.70, 30.77, 40.74, and 42.95° 2θ. Monoclinic WO₃ (COD 2311041) accounts for the diagnostic 23.35/23.82/24.62° triplet and its higher-angle reflections. Orthorhombic BaCO₃ (COD 9010928) accounts for the remaining small but reproducible contribution, notably near 24.12° and associated weaker lines. No coherent set of unexplained peaks remains that warrants another crystalline phase.

The three-phase GSAS-II refinement used the stated Cu Kα doublet, refined phase cells/scales, smooth background, peak-width terms, and supported March–Dollase texture terms. A fresh atomic forward replay of `final.gpx` over all 8301 measured bins gives Rwp = 3.2687%, Rp = 2.4561%, Rexp = 2.3003%, and goodness of fit = 1.4210. The exported profile is that replay, not a cached calculated curve.

## Uncertainty and limits

The phase identities and the presence of all three components are reliable. The tabulated least-squares fraction e.s.d.'s are about 0.04 wt%, but they omit model and preferred-orientation uncertainty; realistic absolute uncertainties are closer to roughly 1–2 wt% for the two major phases and below 1 wt% for BaCO₃. The BaCO₃ fraction is therefore less precise than its formal e.s.d. suggests.

The heavy-atom frameworks and cells are constrained well by this X-ray pattern. Oxygen and carbon coordinates—especially in minor BaCO₃—cannot be determined independently with comparable reliability; they were retained as symmetry-preserving, physically screened perturbations of the identified parent structures. Isotropic displacement parameters were fixed at 0.003 Å² because they were strongly correlated with scale, polarization, and low-angle intensity. Fractions refer only to modeled crystalline phases; amorphous content, if any, cannot be quantified from these data alone.
