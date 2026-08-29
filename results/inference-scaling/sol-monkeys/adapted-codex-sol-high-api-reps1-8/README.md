# Adapted-codex GPT-5.6 Sol high, eight samples

Eight independent API-authenticated GPT-5.6 Sol high attempts per case on the frozen
20-case `inference-scaling-20` panel. Every attempt used the adapted-codex capability,
the canonical short task prompt, the pXRD scientific environment, 2 vCPU and 5 GiB, and
a one-hour limit. Sixteen attempts ran concurrently.

## Results

| Replicate | `selected_exact` | `candidates_exact` |
| ---: | ---: | ---: |
| 1 | 13/20 | 13/20 |
| 2 | 13/20 | 13/20 |
| 3 | 13/20 | 14/20 |
| 4 | 14/20 | 14/20 |
| 5 | 15/20 | 16/20 |
| 6 | 13/20 | 13/20 |
| 7 | 14/20 | 14/20 |
| 8 | 12/20 | 13/20 |

Mean pass@1 is **13.375/20** for the primary selection and **13.75/20** including
declared alternatives. Both metrics reach an oracle pass@8 union of **18/20**. Three of
160 attempts reached the one-hour limit.

`selected/` and `candidates/` contain separately generated outcome matrices, expected
pass@k tables, and plots. `replicate-01/` through `replicate-08/` contain normalized
per-attempt submissions, verifier outputs, final answers, launch metadata, source
contracts, and compressed chronological Codex traces.
