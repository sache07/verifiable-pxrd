# Powder XRD phase analysis

The pattern is best described by three crystalline phases. Weight fractions are normalized over these modeled crystalline phases; they do not quantify amorphous material.

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---:|---|---:|
| MnWO₄ | P2/c | a = 4.79662, b = 5.71099, c = 4.97782, β = 91.1212 | 0.73684 (73.68 wt%) |
| WO₃ | P2₁/c | a = 7.69412, b = 7.54696, c = 10.52665, β = 136.1040 | 0.16320 (16.32 wt%) |
| Mn₂WO₅ | Pnnm | a = 8.66202, b = 8.88720, c = 6.37465 | 0.09996 (10.00 wt%) |

The submitted atomic/profile model gives Rwp = 11.977%, Rp = 6.017%, χ² = 378407.7, and goodness-of-fit = 6.763 using count-based weights. A fresh, zero-optimization GSAS-II replay of `final.gpx` reproduces Rwp = 11.977% on all 8301 measured points; all submitted CIFs pass the contact/occupancy screen and match the project phases and fractions.

## Evidence

The dominant peak set matches monoclinic wolframite MnWO₄ (COD 1520200). A second set is reproduced by monoclinic WO₃; COD 2311041 gave both a better full-pattern result and credible local geometry compared with the older strongly distorted WO₃ entry. Refined cells differ only modestly from those references, as expected for specimen/reference mismatch.

After fitting MnWO₄ and WO₃, the remaining repeatable lines index on an orthorhombic cell near 8.66 × 8.89 × 6.37 Å. Substitution and full-pattern tests of M₂XO₅ relatives identify a Pnnm Mn₂WO₅-type framework. The submitted minor-phase model is derived from the Zn₂AsO₅ framework (COD 9015147) by Zn→Mn and As→W substitution, followed by symmetry-preserving bounded coordinate refinement. Alternative W-site orderings and Mn₃WO₆-type models fit substantially worse. A three-lattice Le Bail diagnostic accounts for the observed line positions, so there is no compelling evidence for a fourth crystalline cell.

## Remaining uncertainty

MnWO₄ and WO₃ are reliable phase identifications. The Mn₂WO₅ assignment is less secure: its cell, composition class, and cation ordering are supported, but no exact Mn₂WO₅ reference was available and several related Pnnm oxygen sublattices give similar fits. Its preferred-orientation and broadening terms approach allowed limits, and some minor-phase-sensitive peaks retain systematic intensity residuals. Accordingly, the detailed Mn₂WO₅ oxygen coordinates should be treated as provisional rather than a unique structure solution.

No pointwise uncertainties were supplied, and the goodness-of-fit remains well above one, so formal least-squares errors would understate model uncertainty. The reported fractions are defensible semi-quantitative values, but precision substantially better than a few weight-percent—especially for the approximately 10 wt% Mn₂WO₅ phase—cannot be claimed reliably.
