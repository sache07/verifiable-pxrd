# Experiments

This tree contains reproducible experimental inputs: conditions, prompts, frozen learned
artifacts, and analysis recipes. Reusable execution and evaluation machinery belongs in
`src/verifiable_pxrd/`; normalized outputs belong in `results/`.

- `agent-adaptation/` owns the four primary agent conditions, the disjoint training
  curriculum, continual-learning contract, and frozen `adapted-codex` capability.
- `inference-scaling/` owns repeated sampling, blind comparable-fit Rwp selection,
  verifier-gated continuation, and LLM-verifier experiments.
- [`appendix/`](appendix/README.md) groups specialist native-refinement experiments
  and native/shared fixed-profile Rwp distribution analyses.
- `experimental-evolution/` owns the reflexive evolution framework for multiphase
  analysis of measured data and its divalent-tungstate lab. The packages a run freezes are
  outputs, so they stay with the run under `results/experimental-evolution/`; the `evolved`
  package evaluated on `pxrd-bench/divalent-tungstates-PG15` is that run's `policies/v6/`.
  Its [`analysis/`](experimental-evolution/analysis/README.md) directory rebuilds the
  expanded manuscript's tables and figures from public evidence, including
  framework-access controls, both unpromoted campaigns, and phase-recovery repeats.

Experiments may reuse the condition registry under `agent-adaptation/conditions/`. A
condition is resolved relative to the repository root even when its TOML is nested here.
