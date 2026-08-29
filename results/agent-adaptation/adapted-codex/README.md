# adapted-codex

This condition is `pxrd-codex` plus the single capability produced by the disjoint
50-problem agent-adaptation experiment. The package was frozen before opening the
200-case pXRD-Bench evaluation.

## Frozen capability

- Trainer source commit: `4701bedb466d970174c78c0fc0743ba486e3d99e`
- Trainer source tag: `pxrd-capability-freeze-2026-08-24`
- Release artifact: `experiments/agent-adaptation/artifacts/adapted-codex/package/`
- Capability SHA-256: `a2803fd4807ccea23915e368d3c23455f80b88156df81bb4b744979df3ccd5aa`

The trainee-visible surface contains one short exact-periodic-CIF submission skill and
one neutral `dicvol14-adapter`. The adapter translates an ordinary peak list into native
DICVOL14 input while preserving the native files, logs, and provenance; it performs no
peak picking or scientific ranking.

The training baseline solved 30/50 problems. One frozen 23-attempt behavioral wave
recovered 6/20 baseline misses and preserved all three selected prior-success controls,
for 9/23 selected-exact outcomes. This targeted recovery is package-validation evidence,
not a held-out accuracy estimate.

## Blind pXRD-Bench evaluation

The frozen condition solved **138/200** cases with its primary `selected.cif` and
**141/200** when its declared alternatives are included. Results, submitted CIFs,
verifier records, final answers, launch metadata, and compressed chronological traces are
under `full-200-chatgpt-sol-high-r1/`.

The evaluation used GPT-5.6 Sol high, 2 vCPU and 5 GiB per attempt, a one-hour limit, and
16 parallel workers. It used ChatGPT authentication; the current frozen `pxrd-codex`
control used API authentication, so that difference is retained explicitly in the result
identifier and paired-comparison metadata.

Machine-readable training and artifact provenance is in
`experiments/agent-adaptation/artifacts/adapted-codex/manifest.json`.

The baseline, behavioral-validation, and judge-training first-pass evidence is retained
under `training/`; it is training provenance, not held-out benchmark evidence.
