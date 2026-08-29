# Ab-PXRD-Solver: pXRD-100, reduced-composition solver

This is the normalized presentation bundle for `ab-pxrd-solver-20260722-v2-fourway-reduced-cpu4h`. Artifact identities,
redistributable CIF bytes, and evaluation outcomes are copied from the frozen
source run without scientific postprocessing.

- Input: pXRD and reduced composition.
- Oracle input: `false`.
- Generated candidates per case: 1.
- Paper reporting cutoff: 1.
- Exact@1: 42/100.

Files:

- `run.json`: condition, provenance, verifier, aggregate counts, and source summary.
- `cases.csv`: one normalized row per benchmark case.
- `candidates.csv`: one normalized row per sampled or solver candidate; sample indices are zero-based.
- `candidates/<case-id>/`: generated CIFs and a `verifier-results.json` record for every case.
- `artifacts.sha256`: checksums for every file in this bundle.
- `candidates.tar.zst`: complete frozen execution shards retained for raw provenance.

The case-first directory contains 77 CIFs and 100 verifier-result files.
