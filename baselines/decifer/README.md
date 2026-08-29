# deCIFer

This folder reproduces the deCIFer comparison using the known conventional-cell
formula-unit count and eight generated candidates per case.

```bash
uv run python baselines/decifer/prepare.py download
uv run python baselines/decifer/make_targets.py build \
  --corpus-root pxrd-bench/pXRD-100
uv run --with modal python baselines/decifer/run.py preflight \
  --composition-mode full-cell-oracle \
  --run-id decifer-preflight
```

The oracle input is explicit in `baseline.json`; the runner also retains a
reduced-composition mode for diagnostic use.
