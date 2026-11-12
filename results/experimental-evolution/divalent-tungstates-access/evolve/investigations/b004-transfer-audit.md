# b004 P0 transfer audit

The frozen predictions are in `investigations/b004-p0-predictions.md`. This
audit is updated as the three durable `b004-transfer` attempts complete.

## Replicate 3: `b004-transfer-ba15aa17dad7`

Score 78.36, hidden D 0.405, independently replayed Rwp 2.728%. The output is
physical, has the exact three-framework inventory, and is formally recovered
but not at the noise floor. Final fractions are 72.11% Ba3W2O9, 22.95% WO3,
and 4.94% BaCO3; the maximum absolute fraction error is 0.86 percentage point.
Site accuracies are 90.1%, 76.9%, and 70.6%, respectively.

The solve selected the exact available references COD 1533878 Ba3W2O9, COD
2311041 monoclinic WO3, and COD 9010928 witherite. It first identified the
major and WO3 families, then recognized BaCO3 from the coherent residual lines
near 24.11/24.49, 34.80, 42.24, and 45.06 degrees and rebuilt the common model
with the retained precursor. Thus the retained-source closure mechanism works
in this replicate rather than succeeding by formula-only reporting. No
submitted structure has a physical flag, and the collected project, scorer
fingerprint, CIFs, fractions, and replay are consistent.

The remaining gap is downstream. The final project uses zero 0.2663 degrees
with specimen shift fixed at +42.4 micrometres, whereas the synthetic
realization used zero 0.1749 degrees and shift -110.0 micrometres. This is a
correlated calibration split, and the zero lies outside the lab's stated
range. WO3 also retains a weak [100] texture term rather than the generating
[110] family, and light-atom precision remains moderate. The exact inventory
therefore reaches recovery without reaching the noise floor, supporting v7's
separate nuisance-bound/correlation rollback and terminal-completion gates.

## Replicate 2: `b004-transfer-e996182d7835`

Score 62.88, hidden D 1.021, independently replayed Rwp 3.269%. The output is
physical and has the exact three-framework inventory, but misses formal
recovery by 0.021 D. Final fractions are 72.17% Ba3W2O9, 22.69% WO3, and
5.14% BaCO3; the maximum absolute fraction error is 1.07 percentage points.
Site accuracies are 74.6%, 66.6%, and 74.2%, respectively.

This solve independently selected the same exact clean references: COD 1533878
Ba3W2O9, COD 2311041 monoclinic WO3, and COD 9010928 witherite. It identified
the weak BaCO3 family before final profile work and retained it through the
full refinement. It also explicitly rejected an unconstrained WO3 oxygen
branch after it produced unphysical contacts and compared the clean monoclinic
parent against triclinic and other lattice competitors. No submitted structure
has a physical flag, and project/export hashes are consistent.

The miss is downstream. Instrument U and X remain fixed at their lower profile
bounds while W absorbs width; WO3 and BaCO3 microstrain are substantially
over-broadened relative to the synthetic realization, and a weak non-generating
BaCO3 texture term remains. Light-atom precision is moderate. This independently
supports v7's boundary/correlation rollback and terminal-completion gates.

## Replicate 1: `b004-transfer-858bd19fdd83`

Score 86.51, hidden D 0.203, independently replayed Rwp 2.511%. The output is
physical, has the exact three-framework inventory, and is recovered but not at
the noise floor. Final fractions are 71.37% Ba3W2O9, 23.66% WO3, and 4.98%
BaCO3; the maximum absolute fraction error is only 0.13 percentage point. Site
accuracies are 99.1%, 76.5%, and 55.4%, respectively.

The solve again selected exact COD 1533878 Ba3W2O9, COD 2311041 monoclinic
WO3, and COD 9010928 witherite. Adding BaCO3 lowered an early common-state Rwp
from 11.21% to 9.38%, while an alternative carbonate refined toward zero and
fit substantially worse. The worker recognized a strong correlation when
zero, displacement, instrument width, and phase broadening were released
together, then separated parameter blocks. No submitted structure has a
physical flag, and project/export hashes are consistent.

The best profile still retains an incomplete correlated solution: zero is
0.2417 degrees with specimen shift fixed at zero, instrument U/X are elevated,
and WO3 size and strain sit at tested upper/lower boundaries. Its D 0.203 is
strong but not the noise floor. Together with the other replicates, this shows
that source retention is reliable on b004 while calibration/profile/coordinate
completion remains variable.

## Running tally

| Gate | Current evidence |
|---|---|
| Ba3W2O9 + WO3 selected 3/3 | Pass: 3/3 |
| BaCO3 and exact physical inventory at least 2/3 | Pass: 3/3 |
| At least one recovery and mean at least 60 | Pass: 2/3 recovery, mean 75.92 |
| No flagged substitute | Pass: 3/3 physical exact references |

All frozen predictions pass. The held-out transfer evidence does not expose a
new source-residue failure: P0 retains carbonate in all three solves. It does
expose reproducible downstream variance, from D 0.203 to 1.021, despite exact
inventory and fractions. Cycle-3 development should therefore keep b004 as a
no-harm/completion case and avoid adding source-specific attention solely for
this case.
