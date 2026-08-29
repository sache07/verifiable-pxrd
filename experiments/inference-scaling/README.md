# Inference scaling

This directory contains experiment definitions for repeated solver sampling, Rwp
scoring, LLM review, and verifier-gated continuation. Shared implementations are
provided by `vpbench`.

- `monkeys/`: repeated independent solver sampling and pass@k reporting.
- `rwp-selector/`: blind, common-schedule whole-pattern candidate ranking.
- `llm-verifier/`: frozen stop/continue judge plus the GEPA optimization that produced it.
- `verifier-gated-scaling/`: the frozen gated schedule, normalization code, and
  reproducibility contract for the reported 20-case result.

Reported outputs are under `results/inference-scaling/` and bind their condition, prompt,
panel, and verifier contracts by hash.
