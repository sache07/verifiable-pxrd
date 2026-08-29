# Ab-PXRD-Solver

This folder reproduces the composition-conditioned, single-output
Ab-PXRD-Solver comparison.

```bash
uv run python baselines/ab-pxrd-solver/prepare.py download
uv run python baselines/ab-pxrd-solver/make_targets.py build \
  --corpus-root pxrd-bench/pXRD-100
uv run --with modal python baselines/ab-pxrd-solver/run.py preflight \
  --run-id ab-pxrd-solver-preflight
```

The released solver has a specialized CPU execution path, retained as
`run_cpu.py`. `PATCHES.md` records the compatibility changes applied around the
unchanged pinned upstream checkout.
