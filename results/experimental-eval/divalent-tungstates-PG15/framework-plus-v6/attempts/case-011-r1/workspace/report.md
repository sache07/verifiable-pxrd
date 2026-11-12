# Powder XRD phase analysis

## Result

| Crystalline phase | Space group | Refined cell | Weight fraction |
|---|---|---|---:|
| β-MnO₂ (pyrolusite) | P 4₂/m n m (No. 136) | a = b = 4.40595 Å, c = 2.87749 Å | 24.70 wt% |
| Monoclinic WO₃ | P 2₁/c (No. 14; nonstandard setting) | a = 7.70399 Å, b = 7.54723 Å, c = 10.55341 Å, β = 136.1084° | 75.30 wt% |

The fractions are normalized over the modeled crystalline material. They do not quantify amorphous material. The covariance-only uncertainty is about 0.17 wt% for either fraction; a more realistic uncertainty including model and inventory choices is approximately 0.5–1 wt%.

## Evidence and model selection

The resolved WO₃ triplet at 23.44°, 23.93°, and 24.69° 2θ, together with the 26.93° and split 33.6–34.5° families and coherent middle/high-angle peaks, selects monoclinic WO₃. A physically complete P 2₁/c neutron model (COD 2311041) gave a substantially better and more stable fit than alternate monoclinic/orthorhombic records. A triclinic trial relaxed toward the monoclinic metric and was rejected as unsupported extra symmetry freedom.

Rutile-type β-MnO₂ is independently supported by its families near 29.01°, 37.67°, 43.12°, 56.96°, 59.66°, and 67.53° 2θ. Two equivalent pyrolusite records were screened; COD 1514232 was retained. Thus the scan is dominated by residual precursor-like WO₃ and MnO₂, with no reliable MnWO₄ product phase.

MnWO₄ refined below about 0.2 wt% and worsened the fit; Mn₃WO₆, Mn₃O₄, and MnO scales collapsed to zero. A Pbca Mn₂O₃ trial could absorb roughly 0.6–0.8 wt%, but only through peaks overlapped by the two major phases, with branch-dependent scale/profile behavior and no coherent unique reflection family. It is therefore not claimed; an Mn₂O₃-like impurity below roughly 1 wt% remains a detection-limit uncertainty.

## Refinement and validation

The final model uses a smooth six-term Chebyshev background (positive over the full range), one effective angular zero correction (+0.39598°), Cu Kα₁/Kα₂ wavelengths and 0.5 doublet ratio from the metadata, and a nonnegative common W/X profile with SH/L asymmetry. Phase broadening was reparameterized to avoid the exact instrumental-X/crystallite-size degeneracy: MnO₂ is the neutral size reference and only the relative extra WO₃ size broadening is active. Symmetry-supported uniaxial strain was retained for MnO₂ [001] and WO₃ [010], as was MnO₂ [110] March–Dollase texture. Surface roughness was removed because its fitted term was 98.5% correlated with the WO₃ scale.

The two W positions were refined and converged; unrestricted WO₃ oxygen refinement produced implausibly large shifts, while the MnO₂ oxygen shift was below 1σ. Oxygen coordinates and isotropic displacement parameters were therefore retained from the parent structures and are not independently determined by this Cu X-ray scan. Both exported structures pass the contact/occupancy geometry screen.

An independent native GSAS-II replay of `final.gpx`, regenerating reflections and structure factors rather than using saved calculated arrays, gives Rwp = 5.8273%, Rp = 4.4165%, and goodness of fit = 2.1678 over all 8,301 points. The submitted CIFs, fractions, and `fit.csv` are exports from that replay.
