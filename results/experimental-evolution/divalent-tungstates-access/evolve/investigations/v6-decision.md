# v6 fixed comparison and decision

Recorded after all 18 durable v6 solves completed and were collected. The
frozen package used prompt SHA-256 `799a091d...` and helper SHA-256
`c022d606...`.

## Fixed comparison

| Case | v6 mean | P0 mean | Difference | v6 state |
|---|---:|---:|---:|---|
| b001-c02 | 77.03 | 74.52 | +2.52 | inconsistent |
| b001-c03 | 48.19 | 84.12 | -35.93 | unrecovered |
| b001-c06 | 46.60 | 22.11 | +24.49 | inconsistent |
| b002-c01 | 44.46 | 72.28 | -27.82 | inconsistent |
| b002-c02 | 22.36 | 21.50 | +0.86 | unrecovered |
| b003-c01 | 45.41 | 45.75 | -0.34 | unrecovered |

Aggregate delta is -6.04 with noise 4.22; the required improvement is 8.43.
The lowest case difference is -35.93, below the fixed -15 regression limit.
v6 therefore fails both aggregate and casewise promotion conditions. P0
remains the incumbent and cycle 2 closes with all three candidate slots used.

## Prospective claims

- c02 passes its at-least-one-recovery and mean-at-least-70 claims, but only
  the recovering solve added calcite after prematurely invoking the helper.
- c03 retains exact inventory 3/3 but has 0/3 recovery and mean 48.19, failing
  both claims. A researcher-only five-pass diagnostic repairs rep3, not the
  premature/incomplete checkpoints in reps1/2.
- c06 selects R-3 2/3 but recovers only 1/3 and has mean 46.60, so its recovery
  and score claims fail. Rep1 deeply develops a wrong-formula Mn2WO5 model.
- harder Zn has exact inventory 3/3 and one recovery, but mean 44.46 misses the
  50-point claim. Calibration/profile boundaries dominate the two failures.
- harder Mn selects R-3 0/3 and has mean 22.36, failing both claims; local
  polish cannot repair an unconstructed topology.
- b003 has exact physical inventory and helper execution 3/3 but recovery 0/3
  and mean 45.41, failing the intended completion gain.

## Scientific decision

The bounded helper is safe when used on a physical checkpoint, but v6 does not
make checkpoint completion or terminal ordering reliable. Preserve its
rollback/convergence mechanism, test the isolated three-to-five-pass constant
on the prospectively recorded no-harm panel, and keep broader source-residue,
equal-depth parent-start, nuisance rollback and terminal-operation rules as
separate behavioral changes for the next cycle. Do not promote v6.
