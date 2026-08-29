# Runtime compatibility corrections

The EC2 benchmark bundle applies one behavior-preserving error-path correction
to the pinned upstream commit `0d67964dfcbd2e2fa09e79bbbac2f5d020a121e9`:

- `pxrd_app/core.py`: initialize `total_count` to zero before the optional
  seed-cell planning block.  Without this initialization, cases for which no
  inferred space group yields a seed cell crash at the final `Total_est`
  assignment with `UnboundLocalError`.  The correction lets the existing
  upstream `No valid cells are found` outcome execute; it does not alter any
  generated structure, search setting, score, or successful path.

The source checkout remains pinned to the stated upstream commit, and the
bundle manifest records hashes after this explicitly documented correction.
