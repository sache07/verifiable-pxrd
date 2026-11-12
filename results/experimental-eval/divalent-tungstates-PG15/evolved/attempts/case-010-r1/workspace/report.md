# PXRD phase analysis

## Result

The modeled crystalline material is predominantly triclinic WO3 and bixbyite Mn2O3, with minor wolframite-type MnWO4. Fractions are normalized only over these modeled crystalline phases; no amorphous fraction can be obtained from this scan without an internal standard.

| Phase | Space group | Weight fraction | Refined cell (angstrom, degrees) |
|---|---:|---:|---|
| WO3 | P -1 (2) | 70.704(31)% | a=7.30251, b=7.53456, c=7.69117; alpha=89.9843, beta=90.6720, gamma=89.9923 |
| Mn2O3 (bixbyite) | Ia-3 (206) | 28.001(28)% | a=9.41016 |
| MnWO4 (wolframite) | P2/c (13) | 1.295(14)% | a=4.80101, b=5.77916, c=4.99892; beta=91.1246 |

Parent structures were COD 2106293 (WO3), 1514230 (Mn2O3), and 1520200 (MnWO4). The quoted parentheses are one-sigma least-squares uncertainties and do not include model-selection error. A more realistic interpretation is roughly +/-1–2 weight-percentage points for either major phase and +/-0.3–0.5 percentage point for MnWO4.

## Evidence

The 23.43/23.91/24.68 degree splitting and many higher-angle families require low-symmetry WO3. Under one common nuisance model, triclinic COD 2106293 gave Rwp 11.03% as a one-phase source screen, compared with 11.67% for monoclinic WO3 and 17.04% for orthorhombic WO3; the other triclinic record and W10O29/W18O49 models were much poorer.

Residual families at approximately 33.26, 38.53, 45.49, 49.62, 55.47, and 66.03 degrees identify Mn2O3. The centrosymmetric Ia-3 bixbyite record fit better than the I213 alternative under the same profile (Rwp 7.575% versus 7.775% at that inventory stage).

MnWO4 is supported by several separate weak families or shoulders, especially near 18.76, 30.13, 30.57, and 36.2 degrees. Its available reference was measured at 2.4 GPa, so its cell—not its atomic coordinates—was refined for the present ambient-pressure scan. The refined geometry remains sensible (shortest W-O 1.79 A and Mn-O 2.11 A). This is the least certain assignment and its fraction should be treated as approximate.

The direct reaction composition Mn2WO6 has no exact local record. Isovalent Mn-for-Cr/Fe/V substitutions were therefore tested in Cr2WO6 and V2WO6 trirutile and Fe2WO6 orthorhombic prototypes. They were geometrically plausible and obtained small formal scales (about 0.2–0.6 wt%), but the fitted cells depended on the parent, their strongest diagnostic families were absent or worsened the residual, and replacing MnWO4 raised Rwp to 7.476–7.479%. Mn2WO6 is therefore not determined reliably and is excluded. Mn3O4 and Mn3WO6 likewise gained scale only from overlaps while their diagnostic lines were unsupported; MnO and reduced tungsten oxides failed their scale/source challenges.

## Refinement and uncertainty

The final full-range GSAS-II replay used all 8301 points from 9.9034 to 100.0949 degrees with the supplied Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio. It refined a smooth six-term Chebyshev background, all phase scales and cells, one specimen displacement (-515.76 micrometres), and a common nonnegative U/W/X profile. The common instrumental FWHM rises smoothly from 0.151 degrees at 15 degrees to 0.437 degrees at 95 degrees; the calculated background remains positive (716–2275 counts). Isotropic size terms were retained only where replay-stable and family-supported: about 138 nm for Mn2O3 and 73 nm for MnWO4.

Texture, strain, roughness, extinction, and extra asymmetry were pruned. In particular, WO3 strain forced a negative strain and negative W, WO3 size hit its neutral upper bound, and released SH/L was 98% correlated with displacement. Atomic coordinates and occupancies were kept at the full-occupancy reference values because grouped displacement refinements drove WO3 W or Mn2O3 O to negative Uiso. Exported structures have reasonable nearest-neighbor geometry (minimum W-O 1.72 A in WO3 and Mn-O 1.90 A in Mn2O3).

The exact submitted replay converged with Rwp=7.4238%, Rp=5.5648%, Rexp=2.6624%, goodness of fit=2.7928, and maximum shift/esd=0.041. The elevated goodness of fit and visible intensity mismatch in parts of the strong 23–25 degree WO3 cluster show that the model is not unique at the level of atomic displacement/intensity details. Phase fractions exclude amorphous material and any unmodeled phase below the practical detection limit. `fit.csv`, all three CIFs, and `result.json` were exported after reopening the same `final.gpx` state.
