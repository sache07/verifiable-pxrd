# pXRD-codex GPT-5.6 Sol high, eight samples

Eight independent API-authenticated GPT-5.6 Sol high attempts per case on the frozen
20-case `inference-scaling-20` panel. Every attempt used the pxrd-codex condition, the
canonical short task prompt, the pXRD scientific environment, 2 vCPU and 5 GiB, and a
one-hour limit.

## Results

| Replicate | `selected_exact` | `candidates_exact` |
| ---: | ---: | ---: |
| 1 | 10/20 | 10/20 |
| 2 | 11/20 | 11/20 |
| 3 | 9/20 | 9/20 |
| 4 | 9/20 | 9/20 |
| 5 | 10/20 | 10/20 |
| 6 | 11/20 | 11/20 |
| 7 | 11/20 | 12/20 |
| 8 | 12/20 | 12/20 |

Mean pass@1 is **10.375/20** for the primary selection and **10.5/20** including
declared alternatives. Both metrics reach an oracle pass@8 union of **15/20**. Two of
160 attempts reached the one-hour limit.

`selected/` and `candidates/` contain separately generated outcome matrices, expected
pass@k tables, and plots. `replicate-01/` through `replicate-08/` contain normalized
per-attempt submissions, verifier outputs, final answers, launch metadata, source
contracts, and compressed chronological Codex traces.
