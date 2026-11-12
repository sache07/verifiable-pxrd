# Public-release checks — 12 November 2026

- `project-replay.json`: fresh GSAS-II replay of all 284 available initial final
  projects, using only the normalized public bundles. Every residual is identical
  to its saved value, and every source workspace is unchanged by hash. The one
  unavailable Sol-high replacement project is listed as skipped.
- `followup-replay.json`: all 61 follow-up records agree with the saved evaluations:
  59 valid profiles reproduce their residuals exactly; the two unsuccessful
  submissions still have no eligible residual. Sr/Pb structure-recovery labels
  agree for all 345 checked initial/follow-up records.
- `manifest.json`: path, size and SHA-256 of the multiphase release files.
- `audit.json`: completeness checks and a credential-pattern scan of plaintext,
  compressed sessions and workspace archives. This is a safeguard, not a guarantee
  that arbitrary historical text contains no sensitive information.
- `gsas-runtime.lock.txt`: backend package pins for the replay check. The backend
  source is GSAS-II commit `c8f97a500d7e48fddbaf8586948c24b174d8bab3`.

The replay command was:

```bash
uv run python pxrd-bench/divalent-tungstates-PG15/evaluation/replay_bundle.py \
  --conditions baseline evolved framework-access framework-plus-v6 \
    evolved-framework-v5 baseline-sol-high baseline-opus \
  --output .runs/public-replay-full-20261112 --workers 4
```

The follow-up check uses the same command with condition names
`followups/baseline`, `followups/evolved`, `followups/framework-access`,
`followups/framework-plus-v6`, and `followups/evolved-framework-v5`, and a new
output directory. Missing or invalid submissions remain in the denominator;
agreement with their recorded failure is not a successfully fitted profile.

Additional checks passed: the 97 repository tests; six appendix profile-metric
tests; two phase-list alias tests; three fixed-background compatibility tests;
and hash/CIF audits of the 1,600-candidate StructSnap bundle and 5,760-candidate
CPU-refinement bundle. No new model sampling or refinement was run.

The pre-existing camera-ready experimental evidence is retained. Changes outside
the new multiphase directories are release documentation/index updates, binary
file handling, and the already prepared appendix organization.
