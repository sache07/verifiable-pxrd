# Blind comparable-fit Rwp selector

The scientific implementation is `verifiable_pxrd.rwp_verifier`. It holds every submitted
structure fixed and applies the same bounded GSAS-II scale, background, zero-shift, and
profile schedule to every candidate. This is a blind test-time score: the reference CIF is
used only afterward to evaluate which ranked candidates match.

```bash
uv run vpbench rwp-verifier monkeys \
  --panel pxrd-bench/panels/inference-scaling-20/manifest.json \
  --source results/inference-scaling/sol-monkeys/adapted-codex-sol-high-api-reps1-8/replicate-01 \
  --source results/inference-scaling/sol-monkeys/adapted-codex-sol-high-api-reps1-8/replicate-02 \
  --output runs/rwp-selector \
  --parallel 16
```

`build_report.py` packages a completed blind ranking with post-hoc StructureMatcher
evaluation for reporting.
