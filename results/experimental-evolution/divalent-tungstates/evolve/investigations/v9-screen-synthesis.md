# v9 unresolved-case screen synthesis

v9 scored 10.63, 69.86 and 66.58 on b001-c03, c05 and c06. The
three-case mean is 49.02, population SD 27.18 and range 10.63--69.86;
all three submissions are physically valid, but none exceeds 80 and only c05
and c06 have strict full inventory. The package is rejected and v6 remains the
incumbent.

| Case | Scored result | Intended mechanism | What actually failed |
|---|---|---|---|
| b001-c03 | 10.63; D 53.455; fresh atomic Rwp 18.772% vs 2.851% floor | Health-screen sources, compare physical analogues, use neutral HAP values, reject correlated high-order texture, and retain only low-index March terms. | The solver began with the expected scheelite family but declared it a topology failure while its baseline was already grossly inadequate. It promoted a distorted C2/c analogue, selected orthorhombic rather than monoclinic WO3, and finally split SrWO4 between 59.00% C2/c and 10.48% scheelite. Strict full inventory is false and structural score is 23.83. A bound common-profile trial was disabled without restoring its value: final U is fixed at 100, W is 61.12 and X is zero, while every phase size/strain term is neutral. Its own low/middle/high audit and Le Bail ceiling remained catastrophic, but these failures triggered more topology and duplicate-phase searching instead of a saved-baseline/source reset. |
| b001-c05 | 69.86; D 0.671; Rwp 2.863% vs 2.234% floor | Construct, health-screen and scale-test the leading balance-motivated analogue before rejection. | This intervention passes: the exact three-formula inventory is restored and fractions are within 1.67 points. The remaining miss is allocation. True roughness was rejected solely because it correlated with scale, all phase strains were omitted, and inflated common U/X absorbed family-dependent width. |
| b001-c06 | 66.58; D 0.773; Rwp 3.319% vs 2.509% floor | Require two independent noncoincident families for a weak new phase. | This intervention passes: all four true phases remain and the v8 false analogue disappears. Profile allocation regresses. A near-boundary physical polarization branch was rejected automatically after the unconstrained optimizer crossed its limit; false roughness remained, and complementary size plus strain/anisotropy was treated as an either/or choice. |

## Causal interpretation

The c03 result is not a failure of the March-only texture guard. It is an
earlier source/profile comparison failure. v6 solved the same case with the
expected three-phase inventory at Rwp 3.04% by comparing leading scheelite
parents and WO3 polymorphs under one truly reset neutral baseline, then testing
size, strain, anisotropy and low-index texture one phase at a time. v9 instead
used fixed trial values as hidden active physics. Position and width mismatch
under that baseline was misread as evidence for a new topology and eventually
same-composition coexistence. Fresh replay agrees with the saved project, so
this is a scientific model-selection failure rather than an export mismatch.

Across c05 and c06, the new chemistry guards work as intended. Their shared
remaining defect is the compressed profile rule: it treats bounds and high
covariance as automatic rejection and compares size against strain rather than
allowing complementary terms with family-wise support. The v6 rule was more
robust: judge a saved baseline by isolated low/middle/high positions, FWHM and
asymmetry; restore actual parameter values after a failed branch; and combine
replay-stable size, strain and symmetry-compatible anisotropy where different
hkl families require them.

## v10 intervention

Keep the v9 CIF, balance, constructed-analogue, weak-phase, March-only and
schema mechanisms. Replace the profile section with four general guards:

1. A bound hit invalidates that branch. Restore the saved pre-trial values,
   not merely refinement flags; fixed profile values remain active physics.
   Rebuild the simpler baseline and, for a physically meaningful boundary,
   retest the term fixed at that boundary with complementary broadening.
2. Do not promote a new topology, polymorph or same-composition coexistence
   from residuals until leading physical source/analogue competitors have been
   reconverged under the same adequate common profile. A duplicate-composition
   phase must remain supported by two unique families after phase-specific
   broadening/texture challenges and must not merely split a poor parent.
3. Judge adequacy from representative isolated low/middle/high positions,
   widths, asymmetry and smooth background, not Rwp, interior values or
   covariance alone. A failed audit requires a saved-baseline corrective branch
   and repeat audit before inventory interpretation.
4. Compare size and strain from neutral values one phase at a time; combine
   complementary replay-stable terms and challenge symmetry-compatible
   anisotropy when hkl families differ. Compare coherent cross-phase angular
   intensity trends with background, polarization and roughness before texture.

Screen v10 first on c03/c05/c06. Do not spend c04 or the two transfer controls
until all three unresolved mechanisms pass prospectively.
