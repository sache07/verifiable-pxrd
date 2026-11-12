# Frozen-submission replay validation, 2026-11-11

All 225 initial Sol submissions were re-evaluated with the released PG15 evaluator.
No solver, refinement, phase selection or background fitting was performed.
Original submissions and archived evaluation records were left unchanged.

| Condition | Verified attempts | Mean per-measurement Rwp (%) |
|---|---:|---:|
| P0 baseline | 45/45 | 7.898883 |
| Evolved v6 | 45/45 | 6.708885 |
| Framework access | 45/45 | 5.978864 |
| Framework + v6 | 45/45 | 6.487135 |
| Framework + own v5 | 45/45 | 6.441631 |

The 223 previously verified profiles reproduce exactly, including every predicted
count and the scored residual. The two newly verified baseline attempts are
case-004 r1 (7.359063%) and case-012 r2 (4.593047%). Their exported-profile versus
replay RMS differences are 1.43e-7 and 9.50e-4 counts, respectively. All source-file
hash checks pass.

`summary.json` records comparisons with archived evaluations. Each condition has
`per_attempt.json` and `attempts/<original-id>/`, including evaluator/source hashes,
verification checks and regenerated profiles. The original attempt selection
(including transport retries) is preserved.

Reproduction instructions and the two representation fixes are documented in
[`evaluation/README.md`](../../../../pxrd-bench/divalent-tungstates-PG15/evaluation/README.md).
The baseline/evolved public bundles and manuscript snapshots were refreshed from
these results. The separate Opus evaluation and targeted phase-recovery follow-ups
are not part of this 225-attempt replay.
