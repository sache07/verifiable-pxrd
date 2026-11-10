# Results

`agent-adaptation/` contains the 200-case results for the evaluated agent
conditions. `inference-scaling/` contains repeated sampling, Rwp selection, and
verifier-gated experiments on the 20-case development panel.

`baselines/` contains non-agent comparison bundles, organized by
framework, corpus, and condition. Each bundle includes normalized run metadata,
case- and candidate-level evaluation indexes, checksums, and a case-first
`candidates/<case-id>/` tree containing generated CIFs and verifier results. Frozen
execution-shard archives are retained separately where redistribution is permitted.

[`appendix/`](appendix/README.md) contains the specialist native-refinement bundles
and Rwp distribution data, figures, and verification results. The as-submitted
distributions remain separate from refinement results; Crystalyze's completed
stage-one sweep and second-stage subset are documented separately from the CPU report.

Normalized replicate bundles retain the run contract, per-case verifier outcome,
submitted CIFs, final response, and compressed chronological agent event trace. The
`matsci-codex` bundle contains the 200 per-case attempts declared by its
progress ledger. Large intermediate workspaces and redundant rollout streams are not
part of the published result bundles.
