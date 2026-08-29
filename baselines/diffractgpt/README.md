# DiffractGPT

This folder reproduces the released formula-conditioned DiffractGPT comparison.
The paper-aligned condition uses one greedy decode.

```bash
uv run python baselines/diffractgpt/prepare.py download --include-base
python baselines/diffractgpt/make_targets.py build \
  --corpus-root pxrd-bench/pXRD-100
uv run --with modal python baselines/diffractgpt/run.py preflight \
  --run-id diffractgpt-preflight
```

The exact base-model and adapter revisions are immutable and listed in
`artifacts.lock.json`.
