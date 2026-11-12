# v1 profile diagnostics

## Staged dual-angular test (fixed before outcomes)

Evidence from completed v1 cases c02, c03, and c05 shows the same pattern: the
solver selected either specimen displacement or constant zero, while the
synthetic measurements contain both. The selected single term approximates the
combined low-angle offset but cannot reproduce its angular dependence. This may
then bias cells, fractions, global width, and phase-specific broadening.

`ptest-angular-v1-01` retains each submitted inventory, structure, background,
and profile model. Starting from the converged project, it releases both zero
and specimen displacement and reconverges. c01 is the noise-floor regression
control. The hypothesis is supported if D decreases materially for at least two
of c02/c03/c05, fitted corrections remain inside generator-scale ranges, and
c01 remains near its existing D=0.025. A lower D accompanied by boundary values,
physical-review flags, or gross instability does not support packaging the
rule.

### Outcome

All four projects remained physical and D decreased, but only trivially:
c01 0.0250->0.0238, c02 0.4186->0.4117, c03 0.7348->0.7311, and
c05 3.2137->3.1879. Zero--shift covariance correlations were 0.9985--0.9998;
several fitted pairs moved away from the generating values while preserving
nearly the same combined low-angle offset. The predeclared material-effect and
identifiability criteria therefore fail. Do not add dual co-refinement to v2;
retain the one-term choice and diagnose phase-profile allocation instead.

## Sharp-phase common-profile anchor test (fixed before outcomes)

Across c02--c06, common widths repeatedly absorb between-phase width
differences, after which phase size/strain can only broaden an already broad
baseline. `ptest-profile-anchor-v1-01` tests a non-oracle escape from that local
allocation. It enumerates each submitted phase as the sharp-peak anchor, rebuilds
an everywhere-positive U/W/X/SH-L common profile from a narrow start, releases
isotropic size and strain for all non-anchor phases, reconverges, and returns the
lowest-Rwp anchor. Inventory, structures, angular model, background family, and
texture are unchanged.

The mechanism is supported only if c04 improves materially (D reduced by at
least half), at least two of c02/c03/c05/c06 also improve, c01 stays near its
noise floor, and selected parameters are not merely bounds or grossly
correlated surrogates. Improvement without stable phase attribution supports a
guidance change to anchor the common profile, but not packaging this exhaustive
diagnostic script as an automatic helper.

## c04 profile-allocation ceiling (fixed before outcomes)

To distinguish profile allocation from adapted-structure error in the severe
c04 regression, an investigation-only oracle probe will fix the generating
U/W/X/SH-L values and isotropic phase size/strain values in both the v1 project
and the strongest-profile P0 replicate, while retaining each project's phase
structures, fractions as refinable scales, background, cells, and angular
choice. If the v1 D falls from 8.89 to near the best P0 range (about 2 or lower),
profile allocation is causal; if it remains high, adapted coordinates or
intensity modeling dominate. The hidden values and case mapping are excluded
from every reusable package.

### Anchor-test outcome

The exhaustive script fails its predeclared robustness criterion. c02 timed out
at 20 minutes. c01 remained stable (D 0.0250->0.0248), c03 changed little
(0.7348->0.7284), and c05/c06 improved (3.2137->2.1757 and
0.5899->0.4505). However c04's selected candidate stored Rwp 6.95% yet fresh
atomic replay gave Rwp 13.38% and D 28.90, much worse than 8.89. Multiple
unselected candidates and active terms also hit bounds. Do not package this
enumeration script. The successful c05/c06 selections support only the narrower
principle: establish the common profile from empirically sharp resolved peaks,
then add and prune one phase term at a time with mandatory fresh replay.

### c04 ceiling outcome

The profile-allocation mechanism is confirmed. Fixing only the generating
common and phase widths reduced v1 c04 from D 8.892/Rwp 7.731% to
D 0.082/Rwp 2.570%, with physical replay and fractions 75.04/18.17/6.79 wt%.
The P0 contrast improved from D 1.904 to 0.496 but retained its pre-existing
flagged WO3 source. Thus the v1 structures and inventory support a near-noise-
floor solution; allocation and replay discipline, not prototype identity, are
the dominant remaining failure. The oracle values remain diagnostic-only.
