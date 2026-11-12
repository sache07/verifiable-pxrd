# Powder XRD phase analysis

The crystalline model contains three phases. Weight fractions are normalized over these modeled crystalline phases; parenthesized uncertainties below are conditional 1-sigma least-squares estimates and do not include model/background systematics.

| Phase | Space group | Weight fraction |
|---|---:|---:|
| CaWO4, scheelite | I 41/a | 79.31(16) wt% |
| WO3, monoclinic | P 21/n | 14.78(6) wt% |
| CaCO3, calcite | R -3 c | 5.91(18) wt% |

The independently regenerated full-grid profile gives Rwp = 3.710%, Rp = 2.804%, Rexp = 3.138%, and Rwp/Rexp = 1.182. Replay made no parameter changes and raised no profile-review flags.

## Evidence

Scheelite CaWO4 accounts for the dominant broadened family, including reflections near 18.30, 28.43, 31.21, 33.87, 46.89, and 48.83 degrees 2theta. Monoclinic WO3 is fixed by the resolved 22.77/23.19/23.98 degree triplet and its companions around 32.88-33.78, 46.91-49.52, and 54.88-55.73 degrees. Calcite supplies a coherent weaker family at 29.08, 35.68, 42.88, 47.20, 48.22, 57.15, 64.43, and 65.32 degrees. Its refined scale is decisively nonzero, while explicit CaO and Ca3WO6 additions collapsed to the non-negative scale bound. No coherent residual family remained that justified another crystalline phase.

The result is also reaction-balanced: residual WO3 and CaCO3 correspond to 0.0637 and 0.0591 mol per 100 g of crystalline material (relative mismatch 7.6%), consistent with incomplete CaCO3 + WO3 -> CaWO4 + CO2 conversion at the reported 650 C treatment.

## Remaining uncertainty

Phase identities and the three-phase inventory are reliable. The exact light-atom coordinates are less secure: CaWO4 oxygen and WO3 tungsten shifts were capped at the stated physical reference-perturbation limits, and the minor WO3 oxygen substructure was retained from the low-precision reference because free oxygen refinement was unstable. That WO3 reference also retains a short O-O contact (~1.58 A), so its oxygen coordinates should not be used as a definitive local-structure determination. A higher-precision monoclinic WO3 coordinate start was tested but did not reproduce the observed profile under fresh GSAS-II replay. Calcite size and microstrain are strongly correlated, so its coherent-domain/profile values are not interpreted quantitatively. Fractions may therefore have larger systematic uncertainty than the formal errors, especially for calcite, but the calcite phase itself is well supported.

The angular zero refined to the allowed -0.25 degree boundary together with a 180.5 micrometre specimen displacement; their correlation is an additional source of lattice-parameter systematic uncertainty.
