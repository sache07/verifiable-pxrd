# Powder XRD phase analysis

## Result

The pattern is described by three crystalline phases. Weight fractions are normalized over these modeled crystalline phases; they do not measure amorphous material.

| Phase | Space group | Refined cell | Crystalline weight fraction |
|---|---|---|---:|
| Ba₃W₂O₉ | R−3c (No. 167) | a=10.12556, c=13.95637 Å | 72.5777 ± 0.0294 wt% |
| WO₃ | P2₁/c (No. 14) | a=7.68812, b=7.53223, c=10.51366 Å, β=136.08379° | 22.5836 ± 0.0258 wt% |
| BaCO₃ | Pmcn setting of No. 62 | a=5.30090, b=8.90748, c=6.44324 Å | 4.8386 ± 0.0244 wt% |

The final fit has Rwp = 2.91091%, Rp = 2.21885%, GOF = 1.2673, and χ² = 13293.35 for 8,301 observations. The quoted fraction uncertainties are formal one-standard-deviation scale/covariance estimates; model and texture systematics are larger than those formal errors.

## Evidence

- Ba₃W₂O₉ (starting COD 1533878) accounts for the dominant broad family at approximately 16.42, 17.72, 26.20, 27.70, 30.78, 32.99, 37.60, 40.75, and 42.96° 2θ.
- Monoclinic WO₃ accounts for the characteristic 23.35/23.82/24.61° triplet and its higher-angle family. Equally developed WO₃ parents were compared: the 1966 neutron topology (COD 2311041) reached about 3.7% Rwp before final polish, versus about 5.0% for the 1960 parent (COD 1528915), so the latter basin was discarded.
- Orthorhombic BaCO₃ (starting COD 9010928) is supported by a narrow, positive family near 19.69, 24.13, 34.81, 42.23, and 45.07° 2θ. Its refined contribution remains positive across that family.
- The phase inventory gives Ba:W ≈ 1.02:1 on a molar basis, consistent with the stated 1:1 BaCO₃/WO₃ precursor ratio. No independent coherent family remains for BaWO₄ or another crystalline phase.

## Model completion and checks

Cells, scales, a 12-term smooth background, bounded specimen displacement, profile terms, and supported March–Dollase texture were developed before the required polish. Ba₃W₂O₉ and WO₃ prefer [110] texture axes; minor BaCO₃ prefers [001]. Isotropic strain is retained because deleting it produces large, reproducible fit losses, while tested uniaxial axes were not distinguishable within uncertainty. Surface roughness was discarded because all physical starts ran to bounds or became singular. Joint zero/displacement and polarization/Uiso alternatives were also rejected as inseparable; zero was fixed at 0°, polarization at 0.7, and the bounded displacement is −398.79 μm.

The single supplied bounded polish selected its all-coordinate branch. It converged with maximum shift/esd 0.030, no frozen variables, no catastrophic contacts, no pair contraction over 0.18 Å, and no fraction collapse. A fresh native GSAS-II replay regenerated reflections without optimization, left `final.gpx` unchanged, raised no profile-review flags, and reproduced Rwp to better than 0.000001 percentage point.

## Remaining uncertainty

The phase identities and three-phase fraction vector are well supported, but the formal fraction errors do not include uncertainty from correlated texture, Uiso, background, or overlapping peaks. The WO₃ coherent-domain size could not be determined reliably (its test reached a bound and was rolled back), and anisotropic strain is not resolved. Oxygen coordinates—especially in 4.8 wt% BaCO₃—should be regarded as bounded powder refinements rather than single-crystal precision. No amorphous fraction can be inferred from this refinement.
