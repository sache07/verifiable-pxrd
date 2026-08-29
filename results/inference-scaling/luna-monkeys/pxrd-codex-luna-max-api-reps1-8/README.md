# pXRD-codex GPT-5.6 Luna max, eight samples

Eight independent API-authenticated GPT-5.6 Luna max attempts per case on the frozen
20-case `inference-scaling-20` panel. Every attempt used the pxrd-codex condition, the
canonical short task prompt, the pXRD scientific environment, 2 vCPU and 5 GiB, and a
one-hour limit. Ten attempts ran concurrently.

## Results

| Replicate | `selected_exact` | `candidates_exact` |
| ---: | ---: | ---: |
| 1 | 9/20 | 9/20 |
| 2 | 7/20 | 7/20 |
| 3 | 5/20 | 5/20 |
| 4 | 6/20 | 6/20 |
| 5 | 5/20 | 5/20 |
| 6 | 6/20 | 6/20 |
| 7 | 6/20 | 6/20 |
| 8 | 7/20 | 7/20 |

Primary and candidate-set recovery are identical in this campaign: mean pass@1 is
**6.375/20**, and the oracle pass@8 union is **12/20**. Twenty-nine of the 160 attempts
reached the one-hour limit.

`selected/` and `candidates/` contain separately generated outcome matrices, expected
pass@k tables, and plots. `replicate-01/` through `replicate-08/` contain normalized
per-attempt submissions, verifier outputs, final answers, launch metadata, source
contracts, and compressed chronological Codex traces.
