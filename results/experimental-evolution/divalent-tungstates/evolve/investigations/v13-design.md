# v13 design

## Objective

Convert v12's correct chemistry/source behavior into complete profile execution
without adding a helper or a broad new checklist. v13 is a 519-word
guidance-only replacement. Both helpers are byte-identical to v12.

## Evidence and changes

1. **Complete symmetry-distinct axes.** v12's c03 script interpreted
   “axial/diagonal” as a small representative set: it tested tetragonal [112]
   but omitted [111], and positive monoclinic [101] but not signed [10-1]. The
   completed researcher diagnostic selects [111] from the unchanged mature
   project, lowering observed Rwp 3.492->3.146% and hidden D 0.463->0.219 with
   physical replay and much better fractions. v13 therefore requires a complete
   symmetry-inequivalent simple low-index set, including equal- and
   unequal-index diagonals and sign-distinct directions when inequivalent.
2. **Collective mature-basin widths.** v12 performs extensive phasewise loops,
   yet c05 leaves WO3 width neutral and inflated common X. Jointly releasing
   all phase strains from the mature model lowers Rwp 2.634->2.569% and D
   0.422->0.355; all three phase strains become interior while X returns to
   zero. c06 similarly stops at isotropic selected widths just below the target.
   v13 adds one collective low-seed release of every width with family support
   or common-width tradeoff, followed by one-term deletion from the interior
   collective solution and independent reseeding. Existing bound restoration
   remains mandatory.

v12's exact-formula polymorph persistence, neutral/elaborated source ranking,
weak-phase evidence, analogue construction, shared-intensity evidence,
literal inactive HAP state and output checks are preserved. The explicit
return-to-common-baseline rule remains when all width branches collapse.

## Prospective predictions

- **c03:** physical monoclinic WO3 and exact inventory should persist; complete
  axes should recover the dominant diagonal texture and move the score from
  70.68 toward or above 80.
- **c05:** exact CaWO4/WO3/Ca3WO6 and supported intensity terms should persist;
  collective widths should remove the common-X surrogate and lift 76.46 toward
  the target.
- **c06:** massicot and the exact four-phase inventory should persist; the
  complete/collective profile pass needs only a small improvement over 79.81.

Screen c03/c05/c06 once. If all mechanisms pass with scores at or around the
target, spend the three remaining development slots on the held c04 and b002
c01/c02 controls. Otherwise the cycle is at its budget boundary and v6 remains
the evaluation fallback.

## Mechanical audit

- Guidance words: 519/600.
- Guidance SHA-256: `63415e0d091f311a28d67b081ec7f3ab7dbc7fe0c50f29228e30549d2348f412`.
- CIF helper SHA-256: `2e2d8abc4d563ba2011772b21714716557ead17663556eb2db2d1c0c4ca2da7f`.
- Analogue helper SHA-256: `0d58e24b4c66dfc7d43567767635c32522c40d000b584912343304844794e5b8`.
- Helper diffs versus v12: empty.
- Case/source/fitted-value leakage scan: empty.
- Both helpers compile; CLI, CIF-health and analogue-query smoke tests pass.
