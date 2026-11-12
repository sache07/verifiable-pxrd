# v13 unresolved-screen synthesis

## Prospective outcome

| Case | Score | Profile evidence | Prospective result |
|---|---:|---|---|
| b001-c03 | 0.00 | No submission after the 14,400 s worker limit | Invalid submission; no physical/profile score |
| b001-c05 | 0.00 | No submission after the 14,400 s worker limit | Invalid submission; no physical/profile score |
| b001-c06 | 67.85 | D 0.7051; independent Rwp 3.2699% versus 2.509% floor | Physical strict four-phase inventory; target regression |

The prospective mean is 22.62, population SD 31.99, and range 0--67.85.
There are 0/3 scores above 80 and only one scorable/physical submission. This is
far below v12 on the same cases (75.65 mean, 3/3 physical and complete) and
cannot displace the evaluated v6 incumbent.

## What each solve actually did

### c03: complete axes became an unbounded search

The worker recovered the strict SrWO4/monoclinic-WO3/SrCO3 basis and did find
the intended directional signal. It completed a 189-branch elaborated loop,
accepted three independently necessary texture terms, rejected bound phase
widths, and selected monoclinic WO3 over tetragonal at matched neutral and
elaborated checkpoints. After polarization/background changes it repeated the
axis/width loops, finding an SrWO4 `<1 -1 -1>` direction and stable SrCO3 [001]
texture. It then reopened the watch list, promoted a second triclinic WO3 phase
at about 5 wt%, and began another complete 147-branch texture/size/strain and
replacement sequence. At timeout it was still challenging orthorhombic WO3 and
had not written `result.json` or `final.gpx`.

Thus the axis mechanism was visible, but v13 did not turn it into a solution.
Recursive equal-treatment of every source and every changed checkpoint consumed
the entire run and encouraged a false same-formula coexistence branch before a
deliverable was frozen.

### c05: a promising physical basin was found but never exported

The worker retained CaWO4/monoclinic-WO3/Ca3WO6 and established that Ca3WO6 was
essential. It ran full monoclinic and triclinic source-parity loops, repeated
complete texture and anisotropic-size inventories after each model change, and
rejected collective branches with invalid Ca3WO6 metrics or nonphysical
strains. A shared-intensity challenge then found physical roughness A/B at Rwp
3.166%, and the subsequent axis restart found CaWO4 [1 -1 0] at nominal Rwp
2.779%, consistent with the generating [110]-family texture. The run timed out
during that renewed full inventory before any final project, CIFs, fractions,
or JSON were exported.

This is useful mechanistic evidence, not a prospective success. The package
made the worker spend 316 progress messages auditing parity and full axis sets
instead of preserving and submitting its best valid checkpoint.

### c06: more search did not imply a better predictive model

The worker completed and retained the exact PbWO4/WO3/Pb3O4/massicot-PbO
inventory, but scored 67.85, 11.96 points below v12. Its all-width branch had a
nominal Rwp of 2.778% only by driving polarization to 1, X to zero, PbO strain
to its ceiling, and creating frozen/singular correlations. The literal validity
gate correctly restored that branch; the accepted clean model then over-pruned
WO3 broadening and ended at independent Rwp 3.270%.

An oracle-informed export-only diagnostic tested the apparently cleaner saved
WO3-strain checkpoint. Although its saved calculated array reported Rwp 2.951%,
fresh atomic replay gave Rwp 3.574%, D 1.079, and score 61.76. The boundary and
fresh-replay gate was protective. A lower stored residual is not sufficient
evidence for a selective-salvage rule.

## Cross-case diagnosis

The causal failure is instruction-induced combinatorial expansion. v13 combined:

- every symmetry-distinct signed/equal/unequal low-index direction;
- texture, size, and strain for each phase;
- neutral and elaborated checkpoints;
- equal loops for every serious source; and
- a full restart after any accepted source, intensity, texture, or width change.

Those clauses form a Cartesian product rather than a focused diagnostic. c03
and c05 produced 610 progress messages and both reached the hard four-hour
limit without a submission. The complete-axis insight itself remains valid—the
v12 c03 diagnostic reduced D from 0.463 to 0.219—but exhaustive enumeration and
recursive parity are not a viable learned procedure. The collective-width
addition is also not generally validated: it collapsed reproducibly on c03 and
c05, and its attractive c06 basin failed fresh replay.

## Decision and final-cycle hypothesis

Reject v13 and do not spend the held slots on set-aside controls. A failed
unresolved screen provides no basis for validation. v6 remains incumbent.

Use the final three development slots on one bounded successor, v14, on
c03/c05/c06. Start from the validated v12 chemistry/source guards, preserve one
collective-width challenge, but replace v13's exhaustive clauses with:

1. At one mature winning-source checkpoint, test a compact symmetry-aware axis
   basis: principal axes, an equal-index diagonal, an unequal-index diagonal,
   and a sign partner only when symmetry does not equate it. Expand once only
   for the single phase with coherent directional residuals; keep the best
   replay-stable leader rather than enumerating every primitive direction.
2. Give competing sources the same compact basis. If one is decisively worse,
   stop; equal opportunity does not require exhaustive parity on a source that
   cannot alter the topology decision.
3. Run one collective low-seed width release and one deletion pass. Do not
   recursively restart complete source/axis inventories after every nuisance
   change; recheck only the affected retained terms.
4. Preserve a replayable, schema-complete best checkpoint before optional
   watch-list or elaboration work, so additional uncertainty analysis cannot
   erase a valid deliverable.

The primary prospective prediction is completion reliability: 3/3 valid
physical submissions while retaining v12's exact inventories. A profile gain is
plausible on c03/c05 because the compact basis includes their diagnosed
directions, but it must be measured rather than inferred from the timed-out
intermediate residuals.
