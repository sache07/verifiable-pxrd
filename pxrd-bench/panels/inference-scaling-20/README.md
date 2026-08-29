# Verifiable pXRD held-out checkpoint panel

This is a locked 20-case checkpoint-evaluation panel selected from the actual
200-case `pXRD-100 + pXRD-ood` benchmark. It is disjoint from the 50 development-
v2 training problems. Selection used benchmark metadata and raw-run availability,
but never raw-agent success, failure, fit, or trace content.

The layout and verifier contract match `verifiable-pxrd-problems`. Only
`problem_input/` should enter an agent sandbox; `solution/` and collection
metadata remain private to the evaluator. Exact `alternative-<n>.cif` outputs
count as successes.

This panel is intended for frozen-pack checkpoints. Once results from it are used
to steer training, it is a validation set—not a final test set. Do not expose it
to the trainer or turn its individual misses into lessons during the 50-problem
training run. The other 180 actual-benchmark cases remain outside this panel for
a final evaluation.

`selection-freeze.json` binds the outcome-blind roster. `raw-agent-baseline.json`
was attached only afterward and reports both the prior scale=True tally and a
re-evaluation under the current scale=False verifier. With only 20 cases, overall
and especially category-level changes will be noisy; use the panel to detect
directional learning, not fine-grained scaling laws.
