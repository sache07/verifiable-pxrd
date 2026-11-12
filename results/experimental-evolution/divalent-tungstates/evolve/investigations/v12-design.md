# v12 design

## Objective

Repair the three prospective v11 failures without changing the validated helper
substrate or adding an always-on search burden. v12 is a 501-word guidance-only
replacement. Both helpers are byte-identical to v11.

## Changes from v11

1. **Exact-formula polymorph persistence.** A passing health result is explicitly
   separated from polymorph adequacy. If the first source for a context- or
   balance-plausible exact formula fits poorly or collapses, the solver must
   compare a structurally distinct physical record/polymorph when available
   before excluding the formula or constructing an analogue. This targets c06's
   wrong tetragonal-PbO test while remaining conditional and general.
2. **Source-rank anchoring.** Every serious source loop is also anchored at the
   neutral low-dimensional checkpoint. Lower symmetry must win both before and
   after elaboration. A rank reversal triggers cross-seeding of shared nuisance
   values and complete candidate-specific low-index axis replay; persistent
   disagreement is treated as coupling unless peak positions/splittings exclude
   the simpler source. This targets c03's triclinic flexibility trap.
3. **Baseline escape.** v6's successful rule is restored: if all phase-width
   trials collapse or hit bounds, return to the common baseline and inventory
   rather than advancing topology.
4. **Shared-intensity evidence.** Background order, polarization and roughness
   are compared from the same checkpoint. Retention requires a replayed angular
   trend across independent phase families, stable fractions, and no compensating
   high-angle/background error. Covariance alone neither rejects nor establishes
   the term. This targets c05 without forcing roughness into no-roughness c06.

All v11 chemistry, weak-phase, coexistence, reversible-coordinate, health, and
output-consistency gates remain. The analogue helper is still available only
after exact-formula challenges.

## Prospective predictions

- **c03:** neutral source ranking should retain the physical monoclinic WO3
  model; the elaborated loop should cross-check rather than overturn it through
  coupled triclinic metric/texture freedom. Expected score returns toward v6's
  83.76 rather than v11's 71.87.
- **c05:** exact inventory and cyclic size/strain recovery should persist.
  The shared-intensity comparison should retain genuine low-angle roughness only
  if it survives simpler background/polarization alternatives, pushing the score
  above v11's 77.55.
- **c06:** a failed first PbO record should trigger a distinct polymorph/source,
  recovering massicot before any non-1:1 analogue is promoted. With exact
  inventory restored, the cyclic loop should avoid the false-analogue detour and
  reopen finite size/strain. Expected score improves materially over 44.67.

Screen c03/c05/c06 once each. Do not spend c04 or the b002 controls unless all
unresolved mechanisms succeed with scores at or above the target, allowing only
small rollout slack.

## Mechanical audit

- Guidance words: 501/600.
- Guidance SHA-256: `733b3fbd1ba13aaea380e433c092c75617ee9669f0d16ca0dee6564b796eaf05`.
- CIF helper SHA-256: `2e2d8abc4d563ba2011772b21714716557ead17663556eb2db2d1c0c4ca2da7f`.
- Analogue helper SHA-256: `0d58e24b4c66dfc7d43567767635c32522c40d000b584912343304844794e5b8`.
- Helper diffs versus v11: empty.
- Case/source/fitted-value leakage scan: empty.
- Both helper CLIs, a CIF health run, and an analogue-query smoke test pass.
