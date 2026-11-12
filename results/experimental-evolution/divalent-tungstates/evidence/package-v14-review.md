# v14 package review

## Rationale

v13 failed prospectively through instruction-induced combinatorial expansion:
c03 and c05 each exhausted the 14,400-second worker limit without a submission,
while c06 completed but regressed. The complete-axis mechanism remains real,
but exhaustive source-by-phase-by-model-by-axis parity and recursive restarts
are not a viable solver procedure.

v14 returns to v12's validated chemistry, exact-formula polymorph, weak-phase,
source-ranking, and physical-boundary core. It replaces the recursive
convergence section with a bounded mature-checkpoint procedure:

- preserve a schema-complete replayable checkpoint as soon as the physical
  inventory converges;
- test one compact symmetry-aware texture basis, with at most one conditional
  expansion for the phase that retains directional residuals;
- stop a decisively inferior source after the matched compact comparison;
- run one collective-width release and one deletion pass; and
- after accepted changes, recheck only affected terms and retained leaders.

The primary prospective prediction is 3/3 valid physical submissions on the
unresolved cases while retaining v12's exact inventories. Profile improvement
is plausible but not assumed from v13's unsubmitted intermediate residuals.

## Audit

- Guidance: 529/600 words; SHA-256
  `a985480bc783cada6d533f1ae854b43a9e06b4c06c958bdd5789b854afe00670`.
- CIF-health helper: unchanged; SHA-256
  `2e2d8abc4d563ba2011772b21714716557ead17663556eb2db2d1c0c4ca2da7f`.
- Analogue helper: unchanged; SHA-256
  `0d58e24b4c66dfc7d43567767635c32522c40d000b584912343304844794e5b8`.
- Package contains only `guidance.md` and the two reusable helpers.
- Case-ID/formula/source leakage scan is empty.
- Both helpers compile in-memory; both CLI help checks pass.
- CIF health passes on a physical exported CIF; the analogue helper returns
  valid limited results against the solver database.

## Prospective use

Freeze unchanged, then run one development solve each on b001-c03, b001-c05,
and b001-c06. These are the final three development slots in cycle 2. Do not
spend them on held controls because v13 never passed the unresolved screen.
