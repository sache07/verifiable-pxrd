# Environment separation

Experiment conditions specify the scientific runtime and capability instructions
separately. Each condition records filesystem access, environment variables, package
locks, and installation scripts.

- **matsci**: Python 3.11 with NumPy, SciPy, pymatgen, spglib, ASE, PyXtal, and related
  general scientific libraries.
- **pxrd**: the identical materials-science environment plus GSAS-II and DICVOL14.
- **portable GSAS**: the `matsci` environment plus the pinned GSAS-II revision, installed by
  `vpbench setup-runtime` on macOS or Linux. It excludes DICVOL and is exercised by
  `experiments/agent-adaptation/conditions/portable/gsas-codex.toml`.
- **capability layer**: prompts, instructions, examples, and thin interfaces selected by
  a condition and versioned independently of the scientific runtime.
- **pattern-generation**: the separately locked GSAS-II runtime that created the
  fixed benchmark inputs. This runtime is distinct from the agent and blind-Rwp
  environments.

`pxrd-codex` and `adapted-codex` use the same scientific binaries and differ in
their capability instructions.

## Runtime variables

The checked-in condition files contain no machine-specific paths. Set:

```bash
export VPBENCH_CODEX=/usr/local/bin/codex
export VPBENCH_MATSCI_ENV="$HOME/.local/share/verifiable-pxrd/matsci"
export VPBENCH_GSAS_ENV="$HOME/.local/share/verifiable-pxrd/gsas2/venv"
export VPBENCH_DICVOL_ROOT="$HOME/.local/share/verifiable-pxrd/dicvol14"
```

`VPBENCH_COD_METADATA` and `VPBENCH_COD_CIFS` specify the read-only local COD
resources used by the coding-agent conditions. Internet retrieval is not substituted
when these resources are unavailable. `vpbench doctor` reports unresolved required
variables. Condition policies also deny access to example structure stores bundled
with scientific libraries. The frozen COD resource is identified in
[`THIRD_PARTY.md`](../THIRD_PARTY.md).

For a generated, sourceable version of the first three paths (plus optional COD paths), follow
[SETUP.md](SETUP.md). `vpbench doctor` reports whether resource limits are enforced by systemd or
the runner is using the portable direct backend.
