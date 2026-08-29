# llm: full pXRD-Bench

GPT-5.6 Sol at high reasoning was evaluated once on each of the 200 released
pXRD-Bench cases. Each independent response received one user message containing
the unchanged benchmark prompt followed by the complete numerical contents of
`pattern.csv`. No tools, developer message, code execution, retrieval, or
persistent workspace were available.

## Result

| Dataset | Selected exact | Including declared alternatives |
| --- | ---: | ---: |
| pXRD-100 | 30/100 | 33/100 |
| pXRD-ood | 24/100 | 25/100 |
| **Combined** | **54/200 (27.0%)** | **58/200 (29.0%)** |

Alternative-only successes were `pxrd100-poly-16-b`, `pxrd100-poly-17-b`,
`pxrd100-rep-013`, and `pxrdood-cf-sub-008`. The selected CIF was parseable for
184/200 cases, and at least one declared CIF was parseable for 185/200 cases.
All 200 API responses and verifier evaluations completed without infrastructure
failures.

`category-summary.csv` gives the benchmark-panel and OOD-stream breakdown.
`bundle.json` contains the normalized per-case outcomes. Each
`attempts/<case-id>/` directory retains the response, sanitized request and
launch records, extracted submission, and frozen verifier result. Traces are not
available because this condition exposes no coding-agent event stream.

## Cost and latency

- Total input tokens: 27,965,682.
- Total output tokens: 4,292,966, including 4,093,775 reasoning tokens.
- Mean/median per-case duration: 6.94/6.95 minutes.
- Longest response: 11.90 minutes.
- Thirty-two-way parallel wall time: 47.55 minutes.

The numerical patterns were supplied inline because Responses API spreadsheet
augmentation exposes only the first 1,000 rows and would truncate each 8,501-row
pattern. The wrapper text merely identifies the following block as the complete
contents of `pattern.csv`.
