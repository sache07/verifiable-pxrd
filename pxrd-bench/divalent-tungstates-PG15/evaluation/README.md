# Experimental project replay

`evaluate_attempt.py` regenerates a submitted GSAS-II project's calculated profile
without refinement. It checks the original observations, submitted CIFs and phase
fractions, and reports observed-data Rwp on 10.1–99.9 degrees using
`w = 1/max(observed_counts, 1)`. Deposited PG curves are rescored separately.

The GSAS-II backend defaults to
`$HOME/.local/share/characterizagent/backends/gsas2`; set `PXRD_GSASII_BACKEND`
and, if needed, `PXRD_UV_PYTHON_ROOT` for another installation. The replay worker
runs with read-only inputs and no network in `bwrap`. The parent Python needs
NumPy, SciPy and pymatgen; the backend Python supplies GSAS-II.

## Replay the released bundles

No private archive is required for the normalized public submissions:

```bash
uv run python pxrd-bench/divalent-tungstates-PG15/evaluation/replay_bundle.py \
  --output .runs/public-replay --workers 4
```

This checks all 225 initial attempts across the five Sol-max conditions. Use
`--conditions baseline --cases case-014 --replicates 2` for a single attempt.
Add `baseline-sol-high baseline-opus` to an explicit condition list to check the
historical model comparisons. The one Sol-high assessment without its original
project is recorded as skipped, never as a successful replay.

The published Opus comparison uses its documented 1e-6-degree grid tolerance;
other conditions use 1e-7 degrees. Every source workspace is hash-checked before
and after replay. Numerical comparisons, generated profiles and skip records are
written to the new output directory. Inputs remain unchanged. The worker does
not refine the project or call a model.

## Maintainer replay from original archives

From the repository root:

```bash
.venv/bin/python pxrd-bench/divalent-tungstates-PG15/evaluation/replay_panels.py \
  --archive-root /path/to/archive/results/experimental-eval/divalent-tungstates-PG15 \
  --output /path/to/new-replay-results --workers 4
```

The original `analysis/per_attempt.json` selects the 45 scored attempts in each
panel, including successful transport retries. No new attempt is selected.
Outputs include per-attempt verification, regenerated curves, evaluator/source
hashes, and a comparison against the archived scores. Existing archive files are
not overwritten. `--conditions P0 --cases case-004 case-012` runs a small pilot.

`publish_replay.py` can refresh the derived baseline/evolved public-bundle records
from this output using `--replay-results`, `--archive-root`, and `--public-root`.
It preserves solver artifacts and uses the bundle importer's path normalization.
Then regenerate aggregate statistics with `python scripts/summarize_experimental_eval.py`.

## Compatibility validation (2026-11-11)

Two representation fixes retain the original scoring rules:

- Accept `modeled_crystalline_phases` as a phase-list alias, alongside `phases`
  and `crystalline_phases`. Conflicting lists are rejected; all existing CIF,
  occupancy and mass-fraction checks still apply.
- Replay an auxiliary fixed-background histogram from its saved intensity
  vector, after checking its grid and finite values. The saved GSAS-II multiplier
  is applied by the native forward calculation. This does not estimate a new
  background, interpolate it, or fit any parameter. The Co baseline's auxiliary
  curve was estimated by the original solver from the observed scan.

Original experiment snapshots remain archived. Tests:

```bash
.venv/bin/python pxrd-bench/divalent-tungstates-PG15/evaluation/tests/test_submission_aliases.py
/path/to/gsas2/venv/bin/python pxrd-bench/divalent-tungstates-PG15/evaluation/tests/test_fixed_background.py
```
