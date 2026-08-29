#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 INSTALL_ROOT" >&2
  exit 2
fi

install_root=$1
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
gsas_commit=1a0aeec6c61b54f68e6812704730a471187ac393
solver_commit=0d67964dfcbd2e2fa09e79bbbac2f5d020a121e9

command -v conda >/dev/null || { echo "conda is required" >&2; exit 1; }
command -v git >/dev/null || { echo "git is required" >&2; exit 1; }
if [[ -e "$install_root" ]]; then
  echo "refusing to overwrite $install_root" >&2
  exit 1
fi

conda create --yes --prefix "$install_root" --file "$script_dir/conda-linux-64.lock"
git -C "$install_root/GSAS-II" fetch origin "$gsas_commit"
git -C "$install_root/GSAS-II" checkout --detach "$gsas_commit"
git clone https://github.com/MaterSim/Ab-PXRD-Solver.git \
  "$install_root/Ab-PXRD-Solver"
git -C "$install_root/Ab-PXRD-Solver" checkout --detach "$solver_commit"

PYTHONPATH="$install_root/GSAS-II/GSASII" "$install_root/bin/python" -c \
  'import numpy; import GSASIIpath; print(numpy.__version__, GSASIIpath.GetVersionNumber())'
echo "fixed-profile generation runtime installed at $install_root"
