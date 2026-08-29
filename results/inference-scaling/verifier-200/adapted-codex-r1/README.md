# Full-200 inference-time verifier results

This bundle contains the case-level evidence behind Figure 3a for the 200 frozen
`adapted-codex` pXRD-Bench candidate sets. A reference match anywhere in the declared
candidate set is the positive class: `stop` is correct for the 141 exact candidate sets,
and `continue` is correct for the 59 misses.

| Method | Accuracy | False stops | False continues |
| --- | ---: | ---: | ---: |
| Rwp <= 5.924% | 127/200 (63.5%) | 1/59 (1.7%) | 72/141 (51.1%) |
| 102-word seed | 126/200 (63.0%) | 1/59 (1.7%) | 73/141 (51.8%) |
| Rwp <= 6.66% | 149/200 (74.5%) | 7/59 (11.9%) | 44/141 (31.2%) |
| Final judge-v1 | 155/200 (77.5%) | 7/59 (11.9%) | 38/141 (27.0%) |

The two Rwp cutoffs were selected retrospectively to match the LLM policies' false-stop
counts. Missing candidate CIFs are assigned `continue`. These rows are descriptive
comparators, not held-out threshold estimates.

## Inputs and provenance

Both reviewers received the composition, wavelength, observed pattern, chronological
solver trace, final response, and submitted CIF set; neither received the hidden
reference or StructureMatcher result. Both received an explicit `not supplied`
sentinel for the precomputed blind comparable-Rwp report and could perform their own
calculations. The comparison is therefore a prompt-only ablation between the seed and
final policies.

The initial judge-v1 call for `pxrdood-tn-css-014` ended with a model-capacity error and
no decision. Its fresh retry supplied the canonical `stop` decision; both sanitized
traces are retained.

## Files

- `case-results.csv`: all labels, Rwp values, decisions, and correctness flags.
- `figure-3a.csv` and `summary.json`: the aggregate values reported above.
- `attempts/<case>/seed/` and `judge-v1/`: sanitized prompts, decisions, final answers,
  launch metadata, comparable-Rwp input, and compressed chronological judge traces.
- `attempts/pxrdood-tn-css-014/judge-v1-initial-invalid/`: the superseded failed call.
- `rwp-candidate-scores.csv` and `source-metadata/rwp-protocol.json`: deterministic
  blind comparable-fit evidence and its shared fitting protocol.
- `source-metadata/`: frozen policies, wrapper, conditions, run contracts, solver-bundle
  identity, and the normalization contract.
- `SHA256SUMS`: hashes for every normalized artifact.

The source solver trajectories, verifier outputs, and CIFs are not duplicated here.
They are keyed by the same case IDs in
`results/agent-adaptation/adapted-codex/full-200-chatgpt-sol-high-r1/`.
