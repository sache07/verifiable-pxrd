# Powder XRD phase analysis

The scan is described by three crystalline phases: wolframite ZnWO4, monoclinic WO3, and wurtzite ZnO. Fractions below are normalized over these modeled crystalline phases.

| Phase | Space group | Weight fraction | Refined cell |
|---|---:|---:|---|
| ZnWO4 (wolframite) | P 2/c | 0.7524 (75.24 wt%) | a = 4.70532, b = 5.73236, c = 4.94306 A; beta = 90.5992 degrees |
| WO3 (monoclinic) | P 21/c | 0.1807 (18.07 wt%) | a = 7.69957, b = 7.54369, c = 10.52906 A; beta = 136.0727 degrees (nonstandard setting) |
| ZnO (wurtzite) | P 63mc | 0.06684 (6.684 wt%) | a = 3.25694, c = 5.22423 A |

## Evidence and model selection

All available same-formula and analogue candidates were screened before the final refinement. For ZnWO4, the P 2/c wolframite analogue was decisively better than triclinic CuWO4-, scheelite-, fergusonite-, raspite-, and HgWO4-type models under common nuisance settings (screen Rwp 33.90% versus 51.65-55.54%). The available old Co/Ni wolframite records had incomplete/duplicated symmetry listings, so their four unique sites were repaired while retaining P 2/c multiplicities and topology, followed by Co/Ni-to-Zn substitution.

The residual after fitting ZnWO4 contained a coherent WO3 family at approximately 23.2-28.7, 33.4-34.3, 41.5, 50.0, and 56.0 degrees. Adding the best P 21/c WO3 candidate reduced Rwp from 21.41% to 7.46% with a stable positive scale. A P-1 WO3 candidate represented the same framework and fit slightly worse; higher-symmetry tetragonal/orthorhombic/hexagonal candidates were substantially worse or their scales collapsed. The remaining peaks at approximately 31.8, 34.5, 36.3, 47.6, 56.6, 62.8, and 67.9-69.1 degrees identify wurtzite ZnO; adding it reduced Rwp to 5.64%. Rocksalt and zincblende ZnO trials gave negligible or much smaller contributions.

No coherent positive residual family remains that requires a fourth phase. The largest residuals coincide with modeled reflections and are predominantly peak-shape/intensity discrepancies. Reduced tungsten oxides and other Zn-W-O stoichiometries were therefore not claimed; they remain untested rather than rejected.

## Refinement and validation

Refinement was staged through scale/background, zero and cells, limited coordinates, isotropic profiles, and only supported texture/anisotropy terms. Retained terms include March-Dollase texture for ZnWO4 [100] and weak WO3 [010] texture, isotropic size/strain terms, and uniaxial WO3 microstrain along [001]. ZnWO4 oxygen coordinates and WO3 tungsten coordinates were accepted only after geometry checks; WO3 oxygen refinement was rejected because it generated shifts up to 0.49 A and a 1.56 A W-O contact. The submitted structures instead have minimum contacts of 1.820 A (ZnWO4), 1.729 A (WO3), and 1.979 A (ZnO), with full occupancies and positive isotropic displacement parameters.

Additional specimen-shift, roughness, instrument-profile, polarization, ZnO texture, and extra anisotropy branches were not retained because they were unstable, boundary-hitting, strongly correlated, or gave negligible improvement. In particular, roughness was 96% correlated with scale, and a direct zero/shift branch was singular; a fixed-profile angular-curvature scan supported the simpler zero-only correction.

The final GSAS-II project converged with maximum shift/esd 0.009. Independent no-refinement replay of `final.gpx` regenerated the full 8301-point profile with Rwp = 3.1963%, Rexp = 2.2671%, goodness of fit = 1.4128, and no physical/profile review flags. `fit.csv` is that replayed observed/calculated/difference profile.

## Remaining uncertainty

The covariance-only fraction standard uncertainties are about 0.09, 0.05, and 0.09 absolute wt% for ZnWO4, WO3, and ZnO, respectively, but these do not include structural-model, texture, overlap, or profile systematics. A more realistic interpretation is roughly 1-2 absolute wt% precision for the minor-phase fractions. The monoclinic WO3 framework is secure, but its exact low-symmetry description and oxygen coordinates are less reliable than its phase identification; oxygen coordinates were kept at the physically valid parent values. ZnWO4 is an analogue-derived model because exact Zn-W-O references were unavailable in the supplied structure index. No amorphous fraction can be determined without an internal/external standard, so the reported fractions must not be interpreted as absolute bulk fractions if amorphous material is present.
