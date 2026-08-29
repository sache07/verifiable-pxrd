# Canonical pxrd-codex training baseline

This bundle contains one blind `pxrd-codex` attempt for each of the 50 disjoint training
problems. It is the evidence reviewed before the learned package was created.

| Cohort | Cases | Contract | `selected_exact` |
| --- | ---: | --- | ---: |
| Imported first cohort | 20 | Same short prompt and pXRD scientific environment; legacy runner without a wall-time cap | 12 |
| Remaining cohort | 30 | Same condition with the canonical one-hour cap | 18 |
| Combined | 50 | GPT-5.6 Sol high, 2 vCPU, 5 GiB, ten parallel workers | 30 |

Both cohorts used direct GSAS-II and bare DICVOL14 with no README, helper, or pXRD skill.
Historical source labels are retained under `sources/` only as provenance. `bundle.json`
provides the canonical `pxrd-codex-baseline-50` identity and exact source-bundle hashes.

Each `attempts/<id>/` directory contains the prompt, assignment and launch records,
compressed chronological Codex events, submitted CIFs, and the canonical verifier result.
The source records are sanitized of machine-specific absolute paths.
