# v15 package review

## Change

v15 retains the promoted v6 inventory, source-selection, analogue, reversible
profile and texture workflow. It sharpens the phase-width comparison to include
neutral, size, strain and combined size-plus-strain from one checkpoint; adds a
late guarded heavy-atom coordinate helper; and makes exact-grid/final-project
re-export requirements explicit. The analogue helper is byte-identical to v6.

The new helper uses only solver-visible projects and observed-profile Rwp. It
orders phases by fitted abundance, challenges previously fixed sites with
atomic number at least 20 one at a time, and accepts only an Rwp reduction of at
least 0.003 percentage point with a maximum coordinate movement of 0.15
angstrom, no newly frozen variable, no new short contact, and repeated
save/reopen refinement. It contains no formulas, source IDs, coordinates,
fractions, case paths or lookup rules.

## Evidence

The unchanged helper was tested diagnostically on 18 incumbent-v6 projects
covering six cases. All 18 outputs remained physical; 17 improved and one was
effectively unchanged, with no regression. On six new-transfer projects,
median D changed from 0.516964 to 0.360261; the mature best control rejected all
new sites and changed D by only -0.00011. On 12 historical carryover projects,
all 12 improved and median D changed from 0.627464 to 0.552958; every case
median improved.

A representative synchronized post-coordinate workspace was independently
replayed by scorer 7.0.1. Its score rose from 71.795753 to 89.222226, D from
0.449901 to 0.115194, independent Rwp from 2.873447% to 2.511181%, and
structural score from 76.034 to 88.550. The two parent-mismatch phases' site
accuracies rose from about 50.57%/57.37% to 83.49%/80.27%. Inventory remained
strict, fractions stayed within 1.50 percentage points, and all physical audits
passed.

## Risks and prospective test

These are oracle-scored diagnostics on existing projects, not proof that a
fresh solver will run the helper, invoke it late enough, or correctly re-export
all artifacts. Runtime and attention cost are the main risks. The helper's
conservative rejection path limits damage to mature or special-position models,
but its profile-driven acceptance cannot establish structural uniqueness.

Freeze v15 and screen one fresh solve on each active case: four unresolved
historical carryovers plus the two newest transfer cases. Require complete
artifacts, inspect whether the helper actually ran after profile stabilization,
and separate coordinate-stage gains from inventory/profile regressions. Do not
promote on the diagnostic evidence alone.
