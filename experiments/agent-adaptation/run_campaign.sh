#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 OUTPUT_ROOT" >&2
  exit 2
fi

repository=$(cd "$(dirname "$0")/../.." && pwd)
output_root=$1
benchmark_root=$repository/pxrd-bench

required=(
  VPBENCH_CODEX
  VPBENCH_AUTH_HOME
  VPBENCH_MATSCI_ENV
  VPBENCH_GSAS_ENV
  VPBENCH_DICVOL_ROOT
  VPBENCH_COD_METADATA
  VPBENCH_COD_CIFS
  VPBENCH_UV_PYTHON
  VPBENCH_CODEX_STANDALONE
)
for name in "${required[@]}"; do
  if [[ -z ${!name:-} ]]; then
    echo "required environment variable is unset: $name" >&2
    exit 2
  fi
done

mkdir -p "$output_root"
if [[ -e "$output_root/heldout-reps1-8" || -e "$output_root/full-200" ]]; then
  echo "campaign output already exists under $output_root" >&2
  exit 2
fi

cd "$repository"
condition=experiments/agent-adaptation/conditions/adapted-codex.toml
uv run vpbench doctor --condition "$condition"
uv run vpbench validate-benchmark --root "$benchmark_root"

# Finish the compact scaling campaign first, then devote the same ten-worker pool
# to the full benchmark. Sequential arms avoid oversubscribing the 61 GiB host.
uv run vpbench run \
  --condition "$condition" \
  --panel "$benchmark_root/panels/inference-scaling-20/manifest.json" \
  --output "$output_root/heldout-reps1-8" \
  --parallel 10 \
  --replicates 8

uv run vpbench run \
  --condition "$condition" \
  --panel "$benchmark_root/panels/full-200.json" \
  --output "$output_root/full-200" \
  --parallel 10
