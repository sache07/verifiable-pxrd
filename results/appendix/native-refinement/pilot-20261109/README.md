# Completed pilot — 9 November 2026

Four cases per corpus, selected by candidate-size rank without looking at exact-match labels. Each uses its first available parseable candidate. This small diagnostic cohort is not a benchmark performance estimate.

| Method | Finished refinements | Exact before → after | Mean worker time |
| --- | ---: | ---: | ---: |
| Crystalyze / StructSnap | 8/8 | 0 → 0 | 9.9 min |
| PXRDGen | 7/8 | 4 → 1 | 41.6 s |
| Ab-PXRD-Solver | 8/8 | 3 → 4 | 8.8 s |
| RealPXRD-Solver adapter | 7/8 | 2 → 2 | 12.1 s |

Exact counts retain the original candidate when refinement fails. The two failures are preserved: PXRDGen could not standardize the first-stage result for `pxrd100-poly-10-a`; the RealPXRD candidate for `pxrdood-tn-wyc-003` had no calculated reflections in the observation range. All other CIF exports passed parsing, finite-cell, and composition checks. Every recomputed original match label agreed with the released label.

The StructSnap cases ran on Tesla T4 GPUs. All 16 stage profiles reproduce their stored native cosine losses; all 30 paired before/after profile sets reproduce their stored Rwp values. `audit.json` records these checks. StructSnap's full self-target control, run separately, retained structural equivalence; its processed cosine similarity changed from 0.978275 to 0.978466. A separate raw self-comparison was exactly 1.0. Native background subtraction explains why the processed target is no longer an identity test.

## Files and reproduction

- `scores.csv`, `summary.json`: local StructureMatcher evaluation, failures, and recovery counts.
- `candidates/`: original/refined and stage CIFs, profile arrays, results, and compressed stage traces/logs.
- `inputs/`: frozen pilot selection, original/reference paths and hashes, missing-input records, and exclusions from pilot selection. Reference structures are only used by the local scorer.
- `provenance/`, `runners/`: package/source/binary records and hash-verified copies of the actual image runners.
- `cost-estimate.json`: resource-time estimates and tentative full-run extrapolations.
- `manifest.json`, `audit.json`: integrity and metric checks.

From the repository root, with the pinned scoring environment:

```bash
python experiments/appendix/native-refinement/report.py \
  --inputs results/appendix/native-refinement/pilot-20261109/inputs \
  --results results/appendix/native-refinement/pilot-20261109
python experiments/appendix/native-refinement/audit_bundle.py results/appendix/native-refinement/pilot-20261109
```

The pilot's resource-time estimate is approximately $1.01, excluding image builds, startup/idle time, controls, and debugging reruns. The launcher reserved approximately $15.29 across pilot/debug calls, before a separate build allowance; reservations are not invoices. No full sweep was launched. At the pilot's mean runtime, the 7,360 available candidates would cost approximately $203 in compute, mostly StructSnap. This estimate is preliminary: eight size-spaced candidates per method cannot characterize the full runtime tail. Rates are recorded from [Modal pricing](https://modal.com/pricing).

The inference-time refinement diagnostic here fits scale and background against each method's observation. It is not the clean-reference fixedparams-v1 metric used by the separately preserved appendix distributions.

This is the historical pilot report; its cost projections and statement that no
full sweep had launched refer to that pilot checkpoint. The completed sweeps are
indexed in the [parent README](../README.md). Reproduction paths were updated
after relocation; the previous README and manifest are retained in
`provenance/pre-cleanup/`. Numerical results and experiment artifacts are unchanged.
