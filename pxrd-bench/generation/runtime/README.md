# Fixed-profile generation runtime

This runtime is separate from the newer GSAS-II installation exposed to agents. It is
the exact Linux x86-64 package set and source revisions used to generate and replay the
committed fixedparams-v1 patterns:

- Python 3.11.9;
- NumPy 1.26.4 and SciPy 1.13.0;
- GSAS-II commit `1a0aeec6c61b54f68e6812704730a471187ac393`, revision 5806;
- Ab-PXRD-Solver commit `0d67964dfcbd2e2fa09e79bbbac2f5d020a121e9`.

The explicit Conda lock is platform-specific by design. Install it with:

```bash
pxrd-bench/generation/runtime/install.sh \
  "$HOME/.local/share/verifiable-pxrd/pattern-generation"
export VPBENCH_PATTERN_PYTHON="$HOME/.local/share/verifiable-pxrd/pattern-generation/bin/python"
export VPBENCH_PATTERN_GSASII="$HOME/.local/share/verifiable-pxrd/pattern-generation/GSAS-II/GSASII"
export VPBENCH_AB_PXRD_SOLVER="$HOME/.local/share/verifiable-pxrd/pattern-generation/Ab-PXRD-Solver"
```

The existing frozen runtime reproduced all 200 committed patterns with maximum absolute
error zero. The public install recipe must still receive a clean-machine release check;
that distinction is retained in `THIRD_PARTY.md`.
