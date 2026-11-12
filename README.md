# Verifiable pXRD

Reproducible benchmarks and agent experiments for structure determination from
single-phase powder X-ray diffraction and phase analysis of experimental mixtures.

This repository separates four things that are easy to confound:

1. **Benchmarks**: structures, simulated patterns, panel manifests, and hidden-reference
   evaluation.
2. **Scientific environments**: the materials-science Python substrate with read-only
   Crystallography Open Database (COD) access, and the same substrate plus GSAS-II and DICVOL14.
3. **Agent adaptation**: the disjoint training evidence, trainer, and frozen learned
   capability layered on an otherwise identical environment.
4. **Results**: immutable run contracts, submitted CIFs, verifier outputs, and compact
   summaries.

The single-phase agent-adaptation comparison is:

| Condition | Harness | Scientific environment | Capability layer |
| --- | --- | --- | --- |
| LLM chat baseline | imported language-model result | no local environment or tools | solve prompt |
| `matsci-codex` | Codex | materials-science Python stack + read-only COD snapshot | minimal |
| `pxrd-codex` | Codex | materials-science stack + COD + GSAS-II + DICVOL14 | minimal |
| `adapted-codex` | Codex | materials-science stack + COD + GSAS-II + DICVOL14 | frozen learned package |

## Repository map

```text
pxrd-bench/          locked pXRD-100/OOD corpora, patterns, panels, builders
pxrd-bench/divalent-tungstates-PG15/   15 measured multiphase scans, deposited references, frozen evaluator
experiments/         adaptation, inference-scaling and experimental-evolution contracts,
                     prompts, and frozen artifacts
evaluation/          exact matcher and blind comparable-fit Rwp documentation
results/             normalized submitted artifacts, verifier outputs, and summaries
                     (including measured evaluations and three synthetic evolution runs)
src/                 reusable isolated runners, evaluators, and verifier engines
```

## Quick start

The supported distribution is a source checkout: experiment conditions, prompts, benchmark
manifests, and setup assets are resolved from the repository tree. A standalone wheel is not a
complete experiment distribution.

```bash
uv sync --group dev
codex login
uv run vpbench setup-runtime
source "$HOME/.local/share/verifiable-pxrd/runtime.env"
uv run vpbench validate-benchmark
uv run vpbench doctor \
  --condition experiments/agent-adaptation/conditions/portable/gsas-codex.toml
uv run vpbench run \
  --condition experiments/agent-adaptation/conditions/portable/gsas-codex.toml \
  --panel pxrd-bench/panels/inference-scaling-20/manifest.json \
  --output runs/portable-smoke \
  --parallel 1 \
  --dry-run
```

The setup command installs pinned materials-science and GSAS-II environments on macOS or Linux;
it intentionally does not install DICVOL. Remove `--dry-run` after inspecting the staged run.
References are never copied into trainee workspaces. See [SETUP.md](docs/SETUP.md),
[REPRODUCE.md](docs/REPRODUCE.md), [METHODS.md](docs/METHODS.md), and
[THIRD_PARTY.md](THIRD_PARTY.md).

The pXRD agent-adaptation experiment uses the shared isolated runner. Its 50 baseline attempts,
validation wave, and frozen output are indexed in
[experiments/agent-adaptation/README.md](experiments/agent-adaptation/README.md).

## Results and reproduction

The two 100-case benchmarks, exact StructureMatcher verifier, comparable-fit Rwp
selector, materials-science baseline prompt, 20-case scaling panel, 50-case training curriculum, canonical
training evidence, and frozen adapted capability are included in this source checkout.
Canonical result bundles and their checksums are indexed under [`results/`](results/README.md),
and the commands needed to reproduce them are documented in
[`docs/REPRODUCE.md`](docs/REPRODUCE.md).

## Experimental track

A second track evaluates multiphase quantitative phase analysis on measured data. The
15 Precursor Genome divalent-tungstate scans, their deposited references and the frozen
evaluator are in [`pxrd-bench/divalent-tungstates-PG15/`](pxrd-bench/divalent-tungstates-PG15/README.md).
A reflexive evolution process, in which the same model curates synthetic problems and evolves
its own package, is in [`experiments/experimental-evolution/`](experiments/experimental-evolution/README.md).
The release contains all three evolution campaigns, including the two that promoted
no package, their solver/evolver traces, and every frozen package. The measured
evaluations cover Baseline, Evolved v6, Framework access, Framework + v6, and
Evolved framework v5, with separate phase-recovery follow-ups and model comparisons.

Start with the [multiphase release guide](docs/MULTIPHASE.md) for the evidence index,
reproduction commands, evaluation boundaries, and known provenance limitations.
Tables and figures can be rebuilt without model calls or the original private archives:

```bash
uv run python experiments/experimental-evolution/analysis/reproduce.py --figures
```

## License and provenance

Repository-authored software and documentation are available under the
[Apache License 2.0](LICENSE). Benchmark source structures, external scientific
software, models, database snapshots, and normalized model outputs retain their
source-specific terms; see [THIRD_PARTY.md](THIRD_PARTY.md) for the scope and exact
resource provenance.
