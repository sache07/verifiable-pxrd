# Repeated solver sampling

`vpbench run` is the monkey runner. Replicates are isolated attempts under the same frozen
condition; the report builder derives outcome matrices and order-invariant expected
pass@k curves from normalized bundles.

```bash
uv run vpbench run \
  --condition experiments/agent-adaptation/conditions/pxrd-codex.toml \
  --panel pxrd-bench/panels/inference-scaling-20/manifest.json \
  --output runs/pxrd-codex-sol-reps1-8 \
  --replicates 8 --parallel 16

uv run python experiments/inference-scaling/monkeys/build_report.py \
  results/inference-scaling/sol-monkeys/pxrd-codex-sol-high-api-reps1-8 \
  --family pxrd-codex-sol-high-api \
  --title "pxrd-codex, GPT-5.6 Sol high"
```

Run-specific model, authentication, and time variants are recorded in each result bundle's
`source-metadata/condition.toml`.
