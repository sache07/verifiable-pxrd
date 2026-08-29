# Portable setup

The supported local setup path installs the locked materials-science Python environment and
GSAS-II revision used by the coding-agent experiments. It works on macOS and Linux and does not
install or require DICVOL.

Run the setup commands from a source checkout. Experiment commands read their
conditions, prompts, benchmark manifests, and setup files from that checkout.

## Prerequisites

- macOS or Linux;
- Git;
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/);
- the [Codex CLI](https://developers.openai.com/codex/cli/).

From a repository checkout, install the package and authenticate Codex on this machine:

```bash
cd /path/to/verifiable-pxrd
uv sync --group dev
codex login
```

Do not copy a Codex credential cache from another computer. Run `codex login` separately on every
machine.

## Install the scientific runtime

```bash
uv run vpbench setup-runtime
source "$HOME/.local/share/verifiable-pxrd/runtime.env"
```

The command installs two pinned components under
`~/.local/share/verifiable-pxrd/`, validates their imports and the GSAS-II source revision, and
writes the machine-local paths to `runtime.env`. Re-running it reuses a valid installation and
refuses to overwrite an invalid or different one. Use `--prefix PATH` to install elsewhere and
`--dry-run` to inspect the plan without writing anything.

A local COD snapshot is optional. To expose one read-only to agents, supply both paths while
setting up:

```bash
uv run vpbench setup-runtime \
  --cod-metadata /absolute/path/to/cod-metadata.json.gz \
  --cod-cifs /absolute/path/to/cod-cifs
```

The repository does not download COD data or silently substitute internet search.
The frozen experiment used DARA 1.3.0's 62,098-entry filtered COD-2024 inventory;
its hashes, license, and reconstruction notes are in
[`THIRD_PARTY.md`](../THIRD_PARTY.md).

## Verify and run

```bash
source "$HOME/.local/share/verifiable-pxrd/runtime.env"
uv run vpbench doctor \
  --condition experiments/agent-adaptation/conditions/portable/gsas-codex.toml
uv run vpbench run \
  --condition experiments/agent-adaptation/conditions/portable/gsas-codex.toml \
  --panel pxrd-bench/panels/inference-scaling-20/manifest.json \
  --output runs/portable-smoke \
  --parallel 1 \
  --dry-run
```

Remove `--dry-run` when the staged contract looks correct. Linux hosts with systemd enforce the
condition's CPU and memory limits. macOS and Linux hosts without `systemd-run` use the same
scientific and agent contract but cannot enforce those per-worker limits; `vpbench doctor` reports
the active resource backend. Start with `--parallel 1` on a laptop and increase it only when memory
and CPU headroom are clear.

The portable condition supports local macOS and Linux use. Reproducing a named result requires
its checked-in condition and every resource declared by that condition.
