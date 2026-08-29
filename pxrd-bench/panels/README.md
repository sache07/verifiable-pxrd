# Evaluation panels

- `inference-scaling-20/` is the frozen, self-contained panel used for the initial
  inference-time scaling study. It has been inspected repeatedly and is now a
  development/validation panel, not an untouched final test set.
- `full-200.json` addresses all committed pXRD-100 and pXRD-ood cases without copying
  their patterns or references.

Use `pxrd-bench/generation/make_panel.py` to make additional deterministic subsets.
Record the generated panel file with every run.
