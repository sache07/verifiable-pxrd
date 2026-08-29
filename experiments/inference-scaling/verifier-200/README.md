# Full-benchmark verifier evaluation

This directory contains the normalization and integrity checks for the case-level
evidence reported in Figure 3a. Reviews are run with `vpbench llm-verifier`; the
normalizer combines reviewer outputs with deterministic Rwp scores in a portable
result bundle.

```bash
uv run python experiments/inference-scaling/verifier-200/normalize.py \
  --raw-root /path/to/raw-verifier-runs \
  --output results/inference-scaling/verifier-200/adapted-codex-r1

uv run python experiments/inference-scaling/verifier-200/normalize.py \
  --check results/inference-scaling/verifier-200/adapted-codex-r1
```

The raw root must contain the four source directories named in `experiment.toml`.
The normalizer retains decisions, prompts, cleaned launch metadata, deterministic
Rwp scores, and sanitized chronological judge events. Hidden references, Codex
runtime state, credentials, duplicated solver traces, and duplicated candidate CIFs
are excluded.
