# Multiphase evidence in the expanded manuscript

This index extends the original [Baseline/v6 comparison](README.md). Folder labels
below are the public condition identifiers; historical P0/E/F names remain only
in preserved artifacts and source identifiers.

| Folder | Scored initial attempts | Interpretation |
| --- | ---: | --- |
| `baseline` | 45 | Sol-max, original task and scientific environment |
| `evolved` | 45 | Same baseline plus promoted v6 guidance/helper |
| `framework-access` | 45 | Baseline with the frozen evolution framework available for inspection/use |
| `framework-plus-v6` | 45 | Framework access plus the original v6 package |
| `evolved-framework-v5` | 45 | Later framework run's unpromoted v5 package |
| `baseline-sol-high` | 45 | Earlier Sol-high comparison, including its documented replacement |
| `baseline-opus` | 15 | Opus/Claude Code comparison, including resumed segments |

The five main conditions contribute 225 attempts. Sol-high and Opus bring the
scored initial comparison to 285. Each condition's `per_attempt.json` indexes
its readable submissions, compressed traces, saved evaluations and frozen
`condition/` contract. `replay-validation-20261111/` retains the earlier common
re-evaluation of the 225 initial Sol-max submissions.

## Follow-ups and failed attempts

`followups/` contains all 61 additional Sr/Pb attempt records across the three
follow-up campaigns, grouped by condition. Pb is retained even though the main
paper now emphasizes Sr. These attempts are not included in the full-panel means.

For the Sr display, framework-access attempt 10 replaces attempt 4, which produced
no submission. Both records remain available: 0/9 recovery among the displayed
completed solves and 0/10 including the failed attempt. Replicate 10 is not renamed
in the evidence. Other incomplete submissions likewise remain visible. Separate
`excluded-attempts` records retain dispatch retries and the cancelled Sol-high solve;
they are not additional samples in the primary comparison.

## Historical model comparison: an explicit evidence gap

The Sol-high case-015 r3 entry uses the previously reported replacement
`P0-exp-case-015-r3-replacement`. Its verified assessment, regenerated profile,
exported replay structures and source hashes survive. Its original workspace and
agent trace were moved to `pxrd-autonomous-v8-eval15-20261008-attempts.tar.gz`
(recorded SHA-256 `bf0809c84747dadb663bb7226a32b0c40ac1810846da05eb73d34100f6963955`),
which is unavailable in the current workspace. It is explicitly marked
`assessment_only_source_attempt_unavailable`. The numerical result is retained;
we do not claim a complete source bundle or substitute a new attempt. All other
main/model-comparison attempts should be checked against the release audit.

Opus uses the historical secondary grid tolerance of 1e-6 degrees rather than the
primary 1e-7-degree check. Observation values, sample counts, evaluation window and
residual definition remain unchanged. Runtime includes resumed session segments.

## Additional development records

`development/` separates the older October v6/v8 work and the documents-only
framework-access experiment from the paper's main comparisons. The saved
documents-only assessment has eight verified results and a stale dispatch ledger.
Available unassessed workspaces and traces are preserved separately, without
inventing final scores or treating that snapshot as a complete 45-attempt panel.

## Reproduction

See [the release guide](../../../docs/MULTIPHASE.md) for table/figure reproduction
and fresh public-bundle replay. `paper-data/` contains the compact inputs used by
the manuscript's figures, with source hashes. Saved solver records remain the
underlying evidence. The scripts never pool follow-ups into initial averages.

Ready-to-read outputs are in [`analysis/`](analysis/README.md), and the independent
replay audit and file manifest are in
[`results/release-checks/multiphase-20261112/`](../../release-checks/multiphase-20261112/README.md).
