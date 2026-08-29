# PXRDGen

This folder reproduces the PXRDGen comparison using the known primitive-cell
formula-unit count and eight generated candidates per case.

```bash
uv run python baselines/pxrdgen/prepare.py download-all
uv run python baselines/pxrdgen/prepare.py install-gsasii
python baselines/pxrdgen/make_targets.py build \
  --corpus-root pxrd-bench/pXRD-100
uv run --with modal python baselines/pxrdgen/run.py preflight \
  --run-id pxrdgen-preflight
```

The source and checkpoints are pinned to the released Code Ocean capsule.
