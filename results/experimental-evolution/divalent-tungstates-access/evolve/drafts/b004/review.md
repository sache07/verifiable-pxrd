# Batch b004 prospective review

## Scope and role

This one-case transfer batch was curated before any b004 solver rollout and before reading any v6 outcome. It is intended to fill one active-panel slot only if the completed cycle-2 evidence supports setting aside at least one stalled older case. It introduces a new divalent-metal source and a different cation-rich tungstate stoichiometry without repeating the Mn3WO6 topology ladder.

| Case | Inventory (wt%) | Difficulty or control role | Fit to the lab priorities |
|---|---:|---|---|
| b004-c01 | Ba3W2O9 71.24, BaCO3 5.00, WO3 23.76 | Full-reference three-phase partial BaCO3 reaction. The unusual R-3c Ba3W2O9 product is major, residual carbonate is weak but identifiable, and compensating WO3 preserves global Ba:W = 1:1. | Tests unfamiliar off-stoichiometric phase recognition, minor-precursor persistence, and coordinate/profile completion in a heavy-atom mixture without confounding the result with missing-reference topology transfer. |

The exact published Ba3W2O9, BaCO3, and WO3 references remain available. A missing-reference form was considered and rejected prospectively: after withholding COD 1533878, the frozen topology matcher found no surviving framework relative at tiers 0–2. That would turn the case into ab initio structure solution, which LAB.md excludes as a priority.

## Source review

- COD 1533878 is the published, ordered R-3c Ba6W4O18 structure, reduced to Ba3W2O9 by registration. It has 84 occupied sites in the conventional cell, minimum registered separation 1.901 A, and no parsing warning.
- COD 9010928 is a synthetic 298 K Pmcn witherite BaCO3 structure. Its 1.275 A minimum separation is the expected intracarbonate C-O distance, not a short nonbonded contact.
- COD 2311041 is the physically screened P21/c WO3 neutron model used in the earlier batches.
- The filtered COD's sole BaWO4 entry, COD 1527204, was examined but excluded: it represents oxygen with two split half-occupied sites and registers as disordered with a 1.167 A minimum separation. An ordered SrWO4-derived diagnostic model passed broad geometry, but neither model is needed for this case and neither is included in the final three-record source manifest.

Published structures establish defensible candidate geometries, not equilibrium phase stability. The simulated mixture represents a possible incomplete one-hour reaction: the cation-rich product is balanced by residual WO3, and retained BaCO3 accounts for carbon from the stated precursor.

## Prospective generation audit

The recipe, seed, count level, and source set were fixed before generation and were not selected from private specimen effects. The case passed the frozen strict-recovery checks.

| Case | Oracle max fraction error | Oracle Rwp (%) | Omission RMS, Ba3W2O9 / BaCO3 / WO3 (noise units) | Strict eligible |
|---|---:|---:|---:|---|
| b004-c01 | 0.000425 | 2.312 | 20.720 / 2.643 / 10.986 | yes |

The omission audit uses the known generating structures and background family. It establishes detectability under this realization, not structural uniqueness.
