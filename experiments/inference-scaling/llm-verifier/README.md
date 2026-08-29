# LLM verifier

The LLM verifier reviews a completed first-pass attempt and predicts whether to
terminate (`stop`) or allocate another solver attempt (`continue`). Exact recovery
is scored afterward with StructureMatcher.

`judge-v1/` contains the frozen evidence wrapper, policy, and provenance manifest.
Run it with `vpbench llm-verifier`. The `gepa/` directory contains the optimizer,
prompts, frozen 30/10/10 split, and policy history used to obtain the frozen policy.

```bash
uv run vpbench llm-verifier run \
  --condition experiments/agent-adaptation/conditions/adapted-codex.toml \
  --panel pxrd-bench/panels/inference-scaling-20/manifest.json \
  --source results/inference-scaling/sol-monkeys/adapted-codex-sol-high-api-reps1-8/replicate-01 \
  --wrapper experiments/inference-scaling/llm-verifier/judge-v1/wrapper.md \
  --policy experiments/inference-scaling/llm-verifier/judge-v1/policy.md \
  --output runs/llm-verifier-adapted-r1 \
  --parallel 16 --timeout 1800
```
