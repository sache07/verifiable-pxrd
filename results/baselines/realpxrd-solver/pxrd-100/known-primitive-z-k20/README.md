# RealPXRD-Solver: pXRD-100, known primitive-cell Z

This is the normalized presentation bundle for `realpxrd-pxrd100-lattice-free-oracle-20260824`. Artifact identities,
redistributable CIF bytes, and evaluation outcomes are copied from the frozen
source run without scientific postprocessing.

- Input: pXRD, composition, and known primitive-cell Z.
- Oracle input: `true`.
- Generated candidates per case: 20.
- Paper reporting cutoff: 8.
- Exact@1: 41/100.
- Exact@8: 62/100.
- Exact@20 over the full retained run: 65/100.

Files:

- `run.json`: condition, provenance, verifier, aggregate counts, and source summary.
- `cases.csv`: one normalized row per benchmark case.
- `candidates.csv`: one normalized row per sampled or solver candidate; sample indices are zero-based.
- `candidates/<case-id>/`: generated CIFs and a `verifier-results.json` record for every case.
- `artifacts.sha256`: checksums for every file in this bundle.
- `candidates.tar.zst`: complete frozen execution shards retained for raw provenance.

The case-first directory contains 2000 CIFs and 100 verifier-result files.
