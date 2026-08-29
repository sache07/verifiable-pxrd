# Reproducing experiments

## 1. Install the repository

Clone the source repository because the CLI reads experiment conditions, prompts,
benchmark manifests, and setup files from the checkout.

```bash
uv sync --group dev
```

## 2. Prepare a scientific environment

For the portable macOS/Linux path, install the pinned materials-science and GSAS-II runtimes and
load their generated machine-local paths:

```bash
codex login
uv run vpbench setup-runtime
source "$HOME/.local/share/verifiable-pxrd/runtime.env"
uv run vpbench doctor \
  --condition experiments/agent-adaptation/conditions/portable/gsas-codex.toml
```

This route intentionally leaves out DICVOL. See [SETUP.md](SETUP.md) for prerequisites, optional
COD paths, and platform notes.

For exact reproduction of a frozen experiment, use its archived condition. The condition TOMLs
contain complete locked package lists and installation scripts. Conditions that declare DICVOL
require the user to provide that separately and set its machine-local path. The full set of
runtime variables used by the frozen conditions is:

```bash
export VPBENCH_MATSCI_ENV=/absolute/path/to/matsci/venv
export VPBENCH_GSAS_ENV=/absolute/path/to/gsas2/venv
export VPBENCH_DICVOL_ROOT=/absolute/path/to/dicvol14
export VPBENCH_CODEX=/absolute/path/to/codex
export VPBENCH_COD_METADATA=/absolute/path/to/cod-metadata.json.gz
export VPBENCH_COD_CIFS=/absolute/path/to/cod-cif-directory
```

The named coding-agent results used DARA 1.3.0's 62,098-entry filtered COD-2024
metadata and matching local CIF mirror. Exact metadata, mirror, and ID-list hashes
are recorded in [`THIRD_PARTY.md`](../THIRD_PARTY.md). A current COD mirror is
suitable for new experiments but may not reproduce the exact historical bytes.

Authenticate Codex independently on each machine with `codex login`; do not copy an `auth.json`
credential cache between machines.

For an API-key experiment, authenticate a dedicated credential home and export it:

```bash
export VPBENCH_AUTH_HOME="$HOME/.codex-vpbench-api"
CODEX_HOME="$VPBENCH_AUTH_HOME" codex login status
```

## 3. Validate inputs and runtime

```bash
uv run vpbench validate-benchmark
uv run vpbench doctor --condition experiments/agent-adaptation/conditions/pxrd-codex.toml
```

## 4. Launch or inspect a run

```bash
uv run vpbench run \
  --condition experiments/agent-adaptation/conditions/pxrd-codex.toml \
  --panel pxrd-bench/panels/inference-scaling-20/manifest.json \
  --output runs/sol-high-r1 \
  --parallel 10
```

Add `--dry-run` to stage inputs, prompts, condition metadata, and agent
configuration without launching Codex. The output directory is append-only: the runner
refuses to overwrite a nonempty run.

Use `--replicate-start 3 --replicates 6` to label six attempts per problem as
replicates 3 through 8 while preserving earlier runs elsewhere.

The reported verifier-gated experiment contract is under
`experiments/inference-scaling/verifier-gated-scaling/`.

## 5. Evaluate

Exact evaluation uses the benchmark StructureMatcher contract.

```bash
uv run vpbench evaluate runs/sol-high-r1
```

To rank all submitted CIFs from one or more monkey replicates with the blind,
test-time-appropriate comparable-fit Rwp protocol:

```bash
uv run vpbench rwp-verifier monkeys \
  --panel pxrd-bench/panels/inference-scaling-20 \
  --source results/inference-scaling/sol-monkeys/adapted-codex-sol-high-api-reps1-8 \
  --output runs/sol-rwp-selector \
  --parallel 10
```

Set `VPBENCH_GSAS_ENV` as above or pass `--gsas-python` explicitly. The verifier does
not read reference CIFs, exact-match outcomes, or the synthetic generator profile.
`--source` accepts either one replicate directory or a campaign directory containing
`replicate-*/bundle.json`, and may be repeated to pool different campaigns.
