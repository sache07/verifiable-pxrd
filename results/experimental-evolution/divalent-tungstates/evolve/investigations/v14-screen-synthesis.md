# v14 unresolved-screen synthesis

## Prospective outcome

| Case | Score | Profile evidence | Inventory result |
|---|---:|---|---|
| b001-c03 | 64.97 | D 0.4705; independent Rwp 3.4751% versus 2.851% floor | Physical, but false 5.73 wt% orthorhombic WO3 coexists with true monoclinic WO3; strict inventory fails |
| b001-c05 | 70.46 | D 0.6556; independent Rwp 2.8590% versus 2.234% floor | Physical strict CaWO4/WO3/Ca3WO6 inventory; max fraction error 1.35 points |
| b001-c06 | 40.89 | D 4.1229; independent Rwp 5.3753% versus 2.509% floor | Physical, but true 5.43 wt% massicot PbO is omitted; strict inventory fails |

The prospective mean is 58.77, population SD 12.84, and range 40.89--70.46.
All three projects are physical and replayable, but only 1/3 has strict full
inventory and 0/3 scores exceed 80. This is 16.88 points below v12 on the same
cases (75.65) and 15.61 below the v6 one-rollout screen (74.38).

## What the bounded intervention established

The primary completion intervention worked. c03, c05 and c06 exported valid
projects after 58, 70 and 70 progress messages, respectively, rather than the
294/316-message non-completions of v13 c03/c05. A schema-complete checkpoint,
compact axis basis, early source stopping and nonrecursive stabilization are a
viable execution pattern.

That execution repair did not preserve the scientific decision gates:

- **c03 over-split one formula.** Matched deletion tests made orthorhombic and
  monoclinic WO3 each appear necessary, but the extra orthorhombic phase is a
  profile surrogate. The split leaves 5.73% extra mass, assigns only 14.90% to
  the true WO3 framework, and lowers the structural score to 60.41. Profile
  support under a flexible nuisance model did not establish real polymorph
  coexistence.
- **c06 closed too early.** The worker never challenged a PbO or massicot
  record. It treated a broad residual near 30.82 degrees without a second
  family as insufficient and stopped at PbWO4/WO3/Pb3O4. The missing 5.43 wt%
  PbO then drove PbWO4 to 61.43%, zero to 0.440 degrees, and a poor 5.375% Rwp.
  This directly loses v12's successful exact-formula persistence behavior.
- **c05 kept chemistry but misallocated profile terms.** The exact inventory
  and fractions are strong, yet polarization 0.873, zero -0.204 degrees, an
  oscillatory eight-term background and three isotropic sizes stop at 2.859%
  Rwp. v12's simpler mature model reached 2.634%. The compact axis/collective
  search did not recover the diagnosed low-D basin.

## Decision

Reject v14 and retain v6 as the promoted incumbent. The bounded execution
pattern is useful evidence for a future cycle, but v14 is not a promotable
scientific package: opposite inventory errors on c03 and c06 outweigh its
completion reliability.

At the 30/30 development endpoint, complete the required three-rollout
evaluation on v12, the most promising post-v6 package. v12 is selected
prospectively because it has the best unresolved-case mean and is physical with
strict inventory on all three, not because of any evaluation outcome. Evaluate
the active panel: b001-c03/c04/c05/c06 and b002-c01/c02. v6 remains the fully
evaluated fallback and should only be displaced if v12 beats the corresponding
baseline evidence.
