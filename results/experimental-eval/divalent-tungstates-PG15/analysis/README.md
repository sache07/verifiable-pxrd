# Rebuilt manuscript analyses

These tables and figures were rebuilt from the public bundles on 12 November
2026 with:

```bash
uv run python experiments/experimental-evolution/analysis/reproduce.py --figures
```

The command writes a fresh copy under `.runs/multiphase-reproduction/`; it does
not modify these saved outputs. `verification.json` records the numerical checks.
The score tables use all 285 initial scored attempts, with the known Sol-high
assessment-only record explicitly identified. Follow-ups are separate.

`sr_repeats_rows.tex` bolds structure-matched Sr2WO5 recoveries. Its dagger marks
framework-access replicate 10, displayed in the position of failed replicate 4;
the CSV retains both display positions and actual replicate identifiers.

Figures use published plotting inputs or the saved replay curves. The Zn
illustration uses r3 for both conditions; Cu uses each condition's median-residual
attempt; the Sr illustration uses Baseline r1, Framework access r2 and Evolved
v6 r2. These are illustrations, not additional evaluation samples.
