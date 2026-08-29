# Adapted-codex GPT-5.6 Luna max, eight samples

Eight independent API-authenticated GPT-5.6 Luna max attempts per case on the frozen
20-case `inference-scaling-20` panel. Every attempt used the adapted-codex capability,
the canonical short task prompt, the pXRD scientific environment, 2 vCPU and 5 GiB, and
a one-hour limit. Ten attempts ran concurrently.

## Results

| Replicate | `selected_exact` | `candidates_exact` |
| ---: | ---: | ---: |
| 1 | 6/20 | 8/20 |
| 2 | 9/20 | 9/20 |
| 3 | 6/20 | 6/20 |
| 4 | 8/20 | 9/20 |
| 5 | 8/20 | 9/20 |
| 6 | 9/20 | 9/20 |
| 7 | 9/20 | 9/20 |
| 8 | 9/20 | 9/20 |

Mean pass@1 is **8.0/20** for the primary selection and **8.5/20** including declared
alternatives. Both metrics reach an oracle pass@8 union of **14/20**. Forty-seven of
160 attempts reached the one-hour limit.

`selected/` and `candidates/` contain separately generated outcome matrices, expected
pass@k tables, and plots. `replicate-01/` through `replicate-08/` contain normalized
per-attempt submissions, verifier outputs, final answers, launch metadata, source
contracts, and compressed chronological Codex traces.
