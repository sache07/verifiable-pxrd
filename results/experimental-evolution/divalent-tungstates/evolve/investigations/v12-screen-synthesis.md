# v12 unresolved-screen synthesis

## Outcome

v12 scores 70.68 / 76.46 / 79.81 on c03/c05/c06 (mean 75.65,
population SD 3.77). All three projects are physical, replay-consistent and
strict full-inventory solutions, but none exceeds 80. The package therefore
passes its three intended upstream interventions without satisfying the screen
condition.

| Case | Profile gap and successful sequence | Divergence from the noise-floor sequence |
|---|---|---|
| c03 | Rwp 3.492% versus 2.851% floor. Neutral/converged source checks preserve physical P21/c WO3; the elaborated triclinic source stays worse at 3.496% and about 25 AIC units. Fractions are within 1.63 points. | The texture script calls [112] a tetragonal diagonal but never tests the non-equivalent [111], and tests positive monoclinic [101] but not signed [10-1]. It accepts SrWO4 [110], inflates common X and rejects all sizes. A generic complete-axis diagnostic selects [111], lowers Rwp to 3.146% and D 0.463->0.219, and moves all fractions within 0.47 points. |
| c05 | Rwp 2.634% versus 2.234% floor. The correct CaWO4/WO3/Ca3WO6 inventory is retained; roughness and polarization each survive reopened deletion tests, so the covariance-neutral angular-evidence rule works. Fractions are within 1.29 points. | Phasewise width tests stop in a coupled basin: CaWO4/Ca3WO6 widths remain, but WO3 width is neutral and common X is inflated. A+B roughness is not causal (D changes only 0.001). Collective mature-basin strain reopening lowers Rwp to 2.569% and D 0.422->0.355 while activating all three strains and returning X to zero. |
| c06 | Rwp 2.820% versus 2.509% floor. The solver identifies massicot from independent families, compares litharge and a second orthorhombic PbO record, and retains exact PbWO4/WO3/Pb3O4/PbO before any analogue. The score 79.81 is the best v12 case and fractions are within 2.59 points. | The final profile is still low-dimensional: PbWO4 size, WO3 strain, Pb3O4 size+strain and PbO strain are isotropic. Finite WO3/PbO size and the generating anisotropic strains are omitted after individually coupled branches collapse or drift. The same collective-width/complete-axis repair is the smallest plausible remaining change. |

## Decision

Reject v12 as a promoted package but preserve its source, exact-formula,
inventory, reversible-loop and shared-intensity clauses. The successor should
make only two execution changes:

1. enumerate a complete symmetry-distinct simple axis basis, including signed
   directions when symmetry does not equate them and both equal- and
   unequal-index diagonals rather than one generic representative;
2. after phasewise width selection, collectively reopen every plausible phase
   size/strain term with common widths from low physical seeds, then delete
   terms one at a time from the interior collective solution. Any bound branch
   must still be restored and replayed rather than accepted.

No helper change is indicated. With 24/30 development solves used, screen the
successor once on c03/c05/c06. If successful, spend the final three slots on
held c04 and b002 c01/c02 controls.
