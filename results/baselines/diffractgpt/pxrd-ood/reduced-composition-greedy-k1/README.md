# DiffractGPT: pXRD-ood, single greedy decode

This is the normalized presentation bundle for `diffractgpt-20260720-ood-paper-greedy-l4`. Artifact identities,
redistributable CIF bytes, and evaluation outcomes are copied from the frozen
source run without scientific postprocessing.

- Input: pXRD and reduced composition.
- Oracle input: `false`.
- Generated candidates per case: 1.
- Paper reporting cutoff: 1.
- Exact@1: 6/100.

Files:

- `run.json`: condition, provenance, verifier, aggregate counts, and source summary.
- `cases.csv`: one normalized row per benchmark case.
- `candidates.csv`: one normalized row per sampled or solver candidate; sample indices are zero-based.
- `candidates/<case-id>/`: generated CIFs and a `verifier-results.json` record for every case.
- `artifacts.sha256`: checksums for every file in this bundle.

Generated CIFs are not redistributed: Generated artifacts are withheld pending clarification of the adapter's redistribution license.
Per-case verifier results, source paths, and SHA-256 identities remain available.

The case-first directory contains 0 CIFs and 100 verifier-result files.
