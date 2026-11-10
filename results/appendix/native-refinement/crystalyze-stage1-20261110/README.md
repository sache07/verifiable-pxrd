# Crystalyze / StructSnap: completed stage-one sweep

All 1,600 saved Crystalyze candidates have a completed first-stage output: eight
candidates for each of the 200 pXRD-Bench problems. No candidate was dropped or
replaced by its original because of a stage-one execution failure.

| Corpus | Problems | Pass@1 before → after | Pass@8 before → after |
| --- | ---: | ---: | ---: |
| pXRD-100 | 100 | 11 → 12 | 19 → 20 |
| pXRD-ood | 100 | 2 → 2 | 6 → 6 |
| Overall | 200 | 13 → 14 | 25 → 26 |

Pass@1 uses the original first candidate; pass@8 is oracle coverage among the
original eight, without reranking. Native cosine similarity improves from a median
of 0.235 to 0.427 across all candidates. Paired first-candidate GSAS-II Rwp medians
change from 95.66% to 86.23% on pXRD-100 and from 95.40% to 92.66% on pXRD-ood.
The native cosine objective and the independent Rwp diagnostic are different metrics.

## What was run

The reported stage optimizes cell lengths and peak width with fixed fractional
coordinates and angles during gradient updates. Native symmetry preprocessing
is retained. This is a single-schedule first-stage experiment, not the full
StructSnap multi-schedule procedure.

The initial two-stage campaign supplied 1,067 first stages. A continuation supplied
the remaining 533 with the same first-stage computation and an early return after
that stage. Cross-account controls verified the continuation against a saved first
stage. Both exact worker snapshots and the control records are included.

Second-stage coordinate-refinement results are retained for the original 1,067
candidates only. On that same subset, candidate-level exact matches change from
60 after stage one to 23 after stage two. These are not problem-level pass@k counts
and are not pooled into the stage-one recovery table.

## Files

- `candidates/`: every original CIF, `stage-1.cif`, available `stage-2.cif`, original
  worker result, compressed optimization trace, and compressed worker log. For
  two-stage runs, `refined.cif` is the second-stage output; use `stage-1.cif` for
  the results reported here.
- `scores.csv`, `summary.json`: candidate-level scores and final aggregate results.
  `structural-summary.json` is the earlier structural-only summary, before paired
  Rwp diagnostics were added.
- `inputs/`: portable original/reference locators and hashes. References are used
  only by the local evaluator, not by refinement workers.
- `runners/`, `provenance/`: both frozen worker versions, dependency/source locks,
  handoff controls, and preserved pre-packaging scores and summary. Historical
  `.runs/` paths in provenance identify the original local campaigns; the current
  `scores.csv` locators point to this bundle.
- `profile-checks/`: fresh paired-profile diagnostics for all 200 first candidates
  and four controls. Dense profile arrays remain in the raw archive and can be
  regenerated from the pinned code and inputs.
- `analysis-source/`: the current local scoring code used to verify the release;
  historical scorer and diagnostic hashes remain in `summary.json`.
- `manifest.json`, `audit.json`: file/runner integrity checks.

## Verify without rerunning refinement

From the repository root:

```bash
uv run python experiments/appendix/native-refinement/audit_bundle.py \
  results/appendix/native-refinement/crystalyze-stage1-20261110
uv run python experiments/appendix/native-refinement/summarize_structsnap_stage1.py \
  --inputs results/appendix/native-refinement/crystalyze-stage1-20261110/inputs \
  --runs results/appendix/native-refinement/crystalyze-stage1-20261110 \
  --output .runs/native-refinement/structsnap-structural-check \
  --structural-only --workers 4
```

The second command checks CIF hashes and recomputes all before/after structural
labels, without GPU access or GSAS-II. Its output should match this bundle's
`structural-summary.json`. Full launch and profile-diagnostic instructions are in
the [experiment README](../../../../experiments/appendix/native-refinement/README.md).
