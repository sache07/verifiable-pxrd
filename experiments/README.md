# Experiments

This directory contains experiment conditions, prompts, frozen capabilities, and
analysis scripts. Shared execution and evaluation code is under
`src/verifiable_pxrd/`, and normalized outputs are under `results/`.

- `agent-adaptation/` contains the four primary agent conditions, the disjoint training
  curriculum, continual-learning contract, and frozen `adapted-codex` capability.
- `inference-scaling/` contains repeated sampling, blind comparable-fit Rwp selection,
  verifier-gated continuation, and LLM-verifier experiments.

Conditions shared by both experiment groups are stored under
`agent-adaptation/conditions/` and resolved relative to the repository root.
