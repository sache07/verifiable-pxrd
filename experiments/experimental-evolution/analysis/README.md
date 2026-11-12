# Multiphase result reproduction

Run from the repository root:

```bash
uv run python experiments/experimental-evolution/analysis/reproduce.py --figures
```

Outputs are written to `.runs/multiphase-reproduction/`:

- `aggregate_scores.csv`: mean/median measurement-level Rwp, mean best-of-three,
  and wall time for the five main conditions, Sol-high, Opus and deposited PG.
- `initial_attempts.csv`: all 285 scored initial agent attempts, with provenance status.
- `sr_repeats.csv`: the nine displayed Sr solves per condition, retaining actual
  replicate identifiers and the framework-access r10-for-r4 replacement.
- `sr_recovery_summary.csv`: completed-solve and all-recorded-attempt denominators.
- `synthetic_attempts.csv`: 327 job records across the three evolution campaigns,
  including the unscored early v9 job and interval-valued structural scores.
- `figures/` and `tables/`: manuscript plots and LaTeX table rows.

`paper_figures/` contains the manuscript's plotting code with repository-relative
inputs and a configurable output directory. Compact plotting inputs under
`results/experimental-eval/divalent-tungstates-PG15/paper-data/` retain their
source hashes. They are derived conveniences, not substitutes for attempt bundles.
`reproduce.py` independently reconstructs the numerical tables from the bundles
and checks the headline values before drawing figures.

The figure scripts' optional archive-refresh functions are maintainer utilities;
normal reproduction uses only the bundled inputs. `--output` changes the output
directory for both tables and figures. No refinement or model sampling occurs.
