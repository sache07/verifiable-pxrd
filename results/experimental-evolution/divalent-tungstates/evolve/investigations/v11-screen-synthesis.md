# v11 unresolved-screen synthesis

## Aggregate

The prospective v11 screen on b001-c03/c05/c06 is complete.

| Case | Score | D | Atomic Rwp | Physical | Strict inventory | Main outcome |
|---|---:|---:|---:|---|---|---|
| c03 | 71.87 | 0.311 | 3.271% | pass | yes | cyclic recovery, but wrong triclinic WO3 after source-rank reversal |
| c05 | 77.55 | 0.398 | 2.612% | pass | yes | strong cyclic size/strain recovery; residual shared-intensity error |
| c06 | 44.67 | 2.859 | 4.671% | pass | no | true PbO omitted after testing the wrong polymorph; false analogue distraction |

Mean is 64.6957, population SD 14.3493, range 44.67--77.55. All three
submissions are physical, two have strict full inventory, and none exceeds 80.
Relative to v10 on the same cases, v11 changes c03/c05/c06 by +14.52/+23.59/
-4.19 points and raises the mean by 11.31. It is rejected; v6 remains incumbent.

## What passed

- The saved-checkpoint coordinate-descent instruction is executable. On c05 it
  repeatedly reopens common, broadening, texture, and source coordinates and
  recovers complementary size plus strain terms across all three phases. This
  lowers D from v10's 1.833 to 0.398 while preserving exact inventory and
  sub-one-point fraction error.
- Chemistry, health, weak-phase, coexistence, and output gates remain strong in
  c03/c05. c03 recovers from v9's duplicated-formula catastrophe and c05 again
  constructs and retains the withheld non-1:1 phase.
- c06 correctly rejects roughness and retains the physical monoclinic WO3 and
  tetragonal Pb3O4 sources. Its polarization is close to the generating value.

## What failed

### Source rank reversal in c03

v6 first ranks monoclinic WO3 over triclinic under a neutral profile (6.475%
versus 7.304% Rwp), then reaches 3.039% with the correct monoclinic source.
v11 allows separately elaborated texture/strain loops to reverse the ranking:
triclinic reaches 3.271% versus 4.052% for its monoclinic branch. A coupled
SrWO4 [110] texture/strain basin and extra triclinic metric freedom manufacture
apparent split-family evidence. Both v6 and v11 prune finite size, so size
omission is a warning rather than the sole cause. See
`investigations/v11-c03-diagnosis.md`.

### Exact-formula source failure in c06

The true fourth phase is 5.43 wt% orthorhombic massicot PbO, COD 2310433. v11
tests only passing tetragonal P4/nmm PbO COD 9012700; it refines to 0.3 wt% in
the early two-phase test and zero against the final three-phase checkpoint.
The solver then treats PbO as absent even though the package says that zero
scale rejects a record, not plausible chemistry. v9 and v10 both test the
orthorhombic massicot record, recover 4.86/4.71 wt%, and document six independent
families plus decisive removal penalties.

The unmodeled massicot families instead promote an adapted Pnma Pb3WO6 model.
It initially appears at 3.2 wt% and passes the two-family gate, but exhaustive
loops move it between roughly 2--6 wt%, swap size/strain, and drive texture,
scale, or polarization to boundaries. It is eventually rejected, but massicot
is never rebuilt. The submitted three-phase model overassigns PbWO4 by 6.03
points and has GOF 1.88/D 2.859.

The final c06 profile also remains incomplete: PbWO4 and Pb3O4 finite sizes are
retained, but WO3 broadening and every true anisotropic strain are omitted;
common U is fixed at 2 instead of the generating 27.38 while X rises to 5.90.
Thus cyclic breadth alone does not guarantee recovery when inventory is wrong.

### Shared intensity in c05

c05's remaining D 0.398 is dominated by the true low-angle roughness trend.
v11 rejects roughness chiefly for 96% correlation with dominant scale, while a
high polarization and flexible background absorb the trend. c06 truth has no
roughness and v11 correctly rejects it, so the repair must not retain roughness
from covariance or global Rwp alone. It should compare simple plausible
background orders and polarization under fixed/reopened scales and require a
replayed low-angle trend across independent phase families with stable
fractions; covariance alone is not a veto when that evidence exists.

## Successor requirements

A minimal successor should preserve v11's reversible loop and all chemistry/
output gates, then add only three general guards:

1. Before excluding a context- or balance-plausible exact formula, compare at
   least one structurally distinct physical record/polymorph when available;
   a health pass does not establish that the first record represents the phase.
   Do this before promoting an adapted analogue from the same residuals.
2. A lower-symmetry source must beat the simpler physical source at both the
   neutral low-dimensional checkpoint and after converged loops. If ranking
   reverses, cross-seed shared nuisance terms, reopen complete axis sets, and
   treat unresolved disagreement as coupling rather than phase evidence.
   Restore v6's return-to-baseline rule when all width trials collapse/bound.
3. Compare roughness, polarization, and a few simple background orders under
   replayed angular evidence and stable fractions. Covariance alone cannot
   reject an angularly supported term, but Rwp/covariance alone cannot retain it.

Re-screen c03/c05/c06 only. Keep c04 and both b002 controls set aside until the
unresolved mechanism screen succeeds.
