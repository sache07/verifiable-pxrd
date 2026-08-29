# Crystalyze

This folder reproduces the element-set-conditioned Crystalyze comparison with
eight generated candidates per case.

```bash
uv run --with gdown python baselines/crystalyze/prepare.py download
python baselines/crystalyze/make_targets.py build \
  --corpus-root pxrd-bench/pXRD-100
uv run --with modal python baselines/crystalyze/run.py preflight \
  --run-id crystalyze-preflight
```

The Modal adapter constructs the pinned upstream Python environment and invokes
`worker.py` inside that environment.
