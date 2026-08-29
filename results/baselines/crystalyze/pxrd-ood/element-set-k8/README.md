# Crystalyze: pXRD-ood, element-set conditioning

This is the normalized presentation bundle for `crystalyze-20260720-ood-paper-bof8-t4`. Artifact identities,
redistributable CIF bytes, and evaluation outcomes are copied from the frozen
source run without scientific postprocessing.

- Input: pXRD and supplied element set.
- Oracle input: `false`.
- Generated candidates per case: 8.
- Paper reporting cutoff: 8.
- Exact@1: 2/100.
- Exact@8: 6/100.

Files:

- `run.json`: condition, provenance, verifier, aggregate counts, and source summary.
- `cases.csv`: one normalized row per benchmark case.
- `candidates.csv`: one normalized row per sampled or solver candidate; sample indices are zero-based.
- `candidates/<case-id>/`: generated CIFs and a `verifier-results.json` record for every case.
- `artifacts.sha256`: checksums for every file in this bundle.
- `candidates.tar.zst`: complete frozen execution shards retained for raw provenance.

The case-first directory contains 800 CIFs and 100 verifier-result files.
