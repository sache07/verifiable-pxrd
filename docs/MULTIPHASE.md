# Experimental multiphase pXRD: release guide

This track studies synthetic-experience adaptation and experimental phase analysis
on 15 Precursor Genome measurements. It is separate from the simulated single-phase
pXRD-Bench experiments. Measurements informed earlier framework development; these
comparisons are development evaluations, not a sealed experimental test set.

## Where to start

| Purpose | Location |
| --- | --- |
| Measurements, precursor metadata, deposited profiles, phase-reference checks | [`pxrd-bench/divalent-tungstates-PG15`](../pxrd-bench/divalent-tungstates-PG15/README.md) |
| Framework, laboratory specification, generator/scorer source, historical design decisions | [`experiments/experimental-evolution`](../experiments/experimental-evolution/README.md) |
| Three synthetic evolution campaigns, packages, solver/evolver traces | [`results/experimental-evolution`](../results/experimental-evolution/README.md) |
| Initial measured evaluations, follow-ups, and model comparisons | [`results/experimental-eval/divalent-tungstates-PG15`](../results/experimental-eval/divalent-tungstates-PG15/RELEASE.md) |
| Table/figure reproduction | [`experiments/experimental-evolution/analysis`](../experiments/experimental-evolution/analysis/README.md) |
| Fresh replay of published final projects | [`evaluation/replay_bundle.py`](../pxrd-bench/divalent-tungstates-PG15/evaluation/replay_bundle.py) |

## Conditions and boundaries

The five main conditions each have three independent solves per measurement:
Baseline, Evolved v6, Framework access, Framework + v6, and Evolved framework v5.
All use Sol at maximum reasoning effort. `v6` is the promoted package from the
original evolution run; `v5` is an **unpromoted** package from the later
framework-access run. The two framework-evolution campaigns have different
curricula and promotion rules. Their version numbers are not a shared time axis.

Sol-high (45 scored attempts) and Opus (15) are separate historical comparisons.
Model aliases, harnesses, dates, and compute differ; neither comparison isolates
model strength alone. The Opus condition retains resumed sessions and its declared
secondary grid tolerance. Follow-up Sr/Pb solves were selected after inspecting
the initial results and never enter the 15-measurement averages.

## Reproduce the reported results

From a source checkout with the development dependencies installed:

```bash
uv sync --group dev
uv run python experiments/experimental-evolution/analysis/reproduce.py --figures
```

This reads released evidence and writes CSV tables, verification results and PDFs
to `.runs/multiphase-reproduction/`. No language-model call, refinement, private
archive, network access, or Overleaf checkout is used. Mean/median residuals are
computed from per-measurement means; best-of-three uses each measurement's minimum.

To independently regenerate calculated profiles, install the GSAS-II backend
described in the [replay guide](../pxrd-bench/divalent-tungstates-PG15/evaluation/README.md):

```bash
uv run python pxrd-bench/divalent-tungstates-PG15/evaluation/replay_bundle.py \
  --conditions baseline evolved framework-access framework-plus-v6 evolved-framework-v5 \
  --output .runs/my-public-replay --workers 2
```

`--cases case-014 --replicates 2` is a small check. Source submissions are copied
to temporary evaluation workspaces, remain unchanged, and are checked by hash.
The evaluator retains the submitted atomic model and all fitted nuisance parameters;
it performs no optimization. The published Opus tolerance is selected only for
`baseline-opus`. Historical scores and the new replay are separate records.

## What is preserved

Each available measured solve includes the prompt and launch contract, submitted
CIFs, `final.gpx`, result/report/profile, evaluator output, chronological events,
and native agent sessions. Additional scripts, plots and logs are compressed in
`workspace-files.tar.gz`. Packages and measurement inputs are stored once and
linked by hashes. Solver-created modifications to a supplied helper are retained
under `workspace/learned-changes`, rather than treated as the frozen package.

Evolution bundles retain curricula and seeds, hidden generating structures,
scorer/generator code, all package revisions, decisions, investigations, and
solver/evolver traces. Oracle-assisted investigations are distinct from fresh
blind solver attempts. They are evidence about development, not extra evaluation
replicates. An unscored job is not converted into a zero or a completed solve.

Normalization replaces machine paths and strips credentials, opaque encrypted
reasoning, and session identifiers. It does not alter numerical project contents.
Intermediate GSAS-II backups, installed software, large caches, credential homes,
and redundant input/helper copies are excluded. Original source hashes and
workspace-copy checks are retained. The historical source directories are not
edited by the import.

Archived `.gitignore` files are retained as `.gitignore.source`: their original
rules would otherwise hide evolver notes, drafts and investigations from a public
commit. Only cache/temporary directories stay excluded. The release audit checks
that no intended evidence is hidden by Git ignore rules.

## Running new experiments versus reproducing saved results

The released framework and run snapshots document the executed protocol, including
Linux sandboxing, EC2 dispatch, model/harness versions and runtime configuration.
Starting a new paid evolution campaign additionally requires your own authentication,
scientific installations, reference library and compute host. The archived host/path
placeholders are not a working deployment configuration. Follow the framework's
new-run procedure in a new directory; never operate on an archived run in place.

## Maintainer import and release checks

`scripts/prepare_multiphase_release.py` imports original archives into the public
layout. Its `--workspace` argument is only for maintainers with those archives;
readers do not need them. Imports preserve failed/cancelled attempts and clearly
identify any assessment-only records. `scripts/audit_multiphase_release.py` checks
the released evidence and generates a file/checksum manifest. The saved audit and
the [release notes](../results/experimental-eval/divalent-tungstates-PG15/RELEASE.md)
identify any remaining provenance limitations.

Saved [release checks](../results/release-checks/multiphase-20261112/README.md)
include the file manifest and independent replay verification. The
[rebuilt analyses](../results/experimental-eval/divalent-tungstates-PG15/analysis/README.md)
provide readable tables and figures without running any code.
