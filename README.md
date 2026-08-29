# Verifiable pXRD

Verifiable pXRD provides benchmarks, evaluation code, and reproducible agent
experiments for crystal-structure determination from single-phase powder X-ray
diffraction patterns and composition. It includes the 100-case pXRD-100 benchmark,
the 100-case pXRD-ood benchmark, six non-agent baselines, coding-agent evaluations,
a 50-problem adaptation curriculum, and inference-time scaling experiments.

## Repository map

```text
pxrd-bench/          locked pXRD-100/OOD corpora, patterns, panels, builders
experiments/         adaptation and inference-scaling contracts, prompts, and frozen artifacts
evaluation/          exact matcher and blind comparable-fit Rwp documentation
results/             normalized submitted artifacts, verifier outputs, and summaries
src/                 reusable isolated runners, evaluators, and verifier engines
```

## Installation

Clone the repository and install its development dependencies. Experiment conditions,
prompts, benchmark manifests, and runtime setup files are read from the checkout.

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

`vpbench setup-runtime` installs the pinned materials-science and GSAS-II
environments on macOS or Linux. DICVOL14 must be supplied separately for conditions
that require it. A local Crystallography Open Database (COD) snapshot can be
configured as a read-only resource. Remove `--dry-run` to launch the staged
experiment. Detailed setup and reproduction instructions are provided in
[SETUP.md](docs/SETUP.md) and [REPRODUCE.md](docs/REPRODUCE.md).

## Results and reproduction

Exact recovery is evaluated with the StructureMatcher contract in
[METHODS.md](docs/METHODS.md). A blind comparable-fit Rwp implementation is included
for candidate ranking. Experiment definitions are under [`experiments/`](experiments/README.md),
and normalized result bundles, submitted CIFs, verifier outputs, and checksums are
indexed under [`results/`](results/README.md).

## License and provenance

Repository-authored software and documentation are available under the
[Apache License 2.0](LICENSE). Benchmark source structures, external scientific
software, models, database snapshots, and normalized model outputs retain their
source-specific terms; see [THIRD_PARTY.md](THIRD_PARTY.md) for the scope and exact
resource provenance.
