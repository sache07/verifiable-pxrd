# Results

`agent-adaptation/` contains the full 200-case accuracy ladder, while
`inference-scaling/` contains repeated sampling on the frozen 20-case development panel.

`baselines/` contains the canonical non-agent comparison bundles, organized by
framework, corpus, and condition. Each bundle includes normalized run metadata,
case- and candidate-level evaluation indexes, checksums, and a case-first
`candidates/<case-id>/` tree containing generated CIFs and verifier results. Frozen
execution-shard archives are retained separately where redistribution is permitted.

[`appendix/`](appendix/README.md) groups the specialist native-refinement bundles
and Rwp distribution data, figures, and verification results. The as-submitted
distributions remain separate from refinement results; Crystalyze's completed
stage-one sweep and second-stage subset are documented separately from the CPU report.

Normalized replicate bundles retain the run contract, per-case verifier outcome,
submitted CIFs, final response, and compressed chronological agent event trace. The
`matsci-codex` bundle contains the 200 canonical per-case attempts declared by its
progress ledger. Large intermediate workspaces and redundant rollout streams are not
part of the published result bundles.

`experimental-eval/` holds agent panels on measured data, one folder per dataset.
[`experimental-eval/divalent-tungstates-PG15/`](experimental-eval/divalent-tungstates-PG15/RELEASE.md)
contains five 45-attempt main panels, separate Sol-high/Opus comparisons, 61 Sr/Pb
follow-up records, and clearly separated development evidence. The paper's
15-measurement means never pool follow-ups or unfinished development panels.

[`experimental-evolution/`](experimental-evolution/README.md) contains all three
synthetic evolution campaigns: the original promoted-v6 run and both unpromoted
framework-access runs. These bundles retain native agent sessions alongside event
streams, final submissions, intermediate scripts and logs. Intermediate GSAS-II
backups, installed environments and redundant input copies are omitted; the
[release guide](../docs/MULTIPHASE.md) documents normalization and evidence gaps.
