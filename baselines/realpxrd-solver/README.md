# RealPXRD-Solver

This folder reproduces the lattice-free RealPXRD-Solver comparison using the
known primitive-cell formula-unit count. The runner retains 20 samples; the
paper reports exact@1 and exact@8.

```bash
uv run --with gdown python baselines/realpxrd-solver/prepare.py download
uv run python baselines/realpxrd-solver/make_targets.py build \
  --corpus-root pxrd-bench/pXRD-100
uv run --with modal python baselines/realpxrd-solver/run.py preflight \
  --input-mode lattice-free-primitive-formula-oracle \
  --run-id realpxrd-solver-preflight
```

`exposure.lock.json` preserves the separate training-exposure audit.
