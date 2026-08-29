# Inference-time scaling

This directory contains repeated-sampling experiments on the frozen 20-case
`inference-scaling-20` panel. Each campaign preserves independently verifiable replicate
bundles and derives its outcome matrices and pass@k curves directly from those bundles.

Primary-answer accuracy (`selected_exact`) and candidate-set coverage
(`candidates_exact`) are reported separately. The latter counts a reference match in
either `selected.cif` or a declared `alternative-<n>.cif`; it does not replace the primary
metric.

- `verifier-gated-scaling/`: the reported gated trajectory, including the full
  case-level execution matrix, agent artifacts, cumulative candidate pool, and
  token-cost curve.
- `verifier-200/adapted-codex-r1/`: the full case-level Figure 3a verifier table,
  both LLM policies' 401 sanitized judge traces (including one retried capacity
  error), and the deterministic comparable-Rwp scores and protocol.

- `sol-monkeys/pxrd-codex-sol-high-api-reps1-8/`: eight GPT-5.6 Sol high samples using
  the pxrd-codex condition.
- `luna-monkeys/pxrd-codex-luna-max-api-reps1-8/`: eight GPT-5.6 Luna max samples using
  the pxrd-codex condition.
- `sol-monkeys/adapted-codex-sol-high-api-reps1-8/`: eight GPT-5.6 Sol high samples
  using the frozen adapted-codex condition.
- `luna-monkeys/adapted-codex-luna-max-api-reps1-8/`: eight GPT-5.6 Luna max samples
  using the same frozen adapted-codex condition.
- `rwp-selector/adapted-codex-sol-high-api-reps1-8/`: blind, frozen-structure Rwp
  selection over all 213 candidates submitted by the eight adapted-codex Sol samples;
  minimum-Rwp selection recovers the full 18/20 oracle union.

Each campaign contains both `selected/` and `candidates/` reports. The paper's
inference-scaling figure uses `candidates/`, so an exact structure in either the primary
submission or a declared alternative counts as recovered.
