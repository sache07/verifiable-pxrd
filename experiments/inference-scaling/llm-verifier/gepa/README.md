# GEPA optimization of a pXRD continuation reviewer

This experiment optimizes the policy text used by a blind stop/continue reviewer.
It uses the frozen Codex condition, StructureMatcher evaluator, and scientific
runtime from the main repository.

The v1 optimization is complete. All agent-facing source text is preserved under
[`prompts/`](prompts/):

- `reviewer-wrapper.md`: immutable task inputs and output contract;
- `seed-judge-policy.md`: the initial policy optimized by GEPA;
- `reflection.md`: instructions for an oracle-aware agent to inspect complete
  training-case artifacts and propose transferable policy mutations;
- `evaluator-feedback.md`: compact outcome and artifact-navigation feedback;
- `continuation-policy.md`: frozen second-pass policy for a later end-to-end test.

[`PROMPTS.md`](PROMPTS.md) records the prompt supplied to each actor and identifies
the text GEPA may change. GEPA candidate merging is disabled for this experiment.

## Frozen experiment

1. Assemble blind first-pass attempts from nonbenchmark pXRD problems.
2. Split by **problem identity**, never by trajectory.
3. Label an attempt `stop` when any declared CIF passes the benchmark
   StructureMatcher and `continue` otherwise.
4. Evaluate the seed reviewer in the frozen adapted-Codex environment.
5. Give GEPA full blind trajectories plus post-hoc evaluator feedback, allowing
   it to mutate only `judge_policy`.
6. Select prompt candidates on structure-disjoint validation problems.
7. Re-evaluate the seed and top three prompts three times on a held-out
   development split before freezing anything.
8. Evaluate the frozen prompt once on the untouched inference-scaling panel,
   then measure actual continuation recovery and compute against blind pass@2.

## Data contract

`data/examples.jsonl` indexes the compact first-pass evidence retained in the parent
repository. To rebuild it, use `scripts/build_training_examples.py`. Paths may be absolute
or relative to the manifest.
Every attempt from the same `problem_id` must remain in one split. Copy
`data/splits.example.json` to `data/splits.json` and assign problem identifiers
to `train`, `validation`, and `development_test`.

References are consumed only by the external evaluator. Reviewer sandboxes can
read staged evidence but cannot read their control/reference directories.

## Runtime contract

The experiment reuses the read-only `adapted-codex` condition for its capability,
scientific software, isolation rules, Codex authentication, and compute limits.
On the execution host, export the same `VPBENCH_*` runtime variables documented in
`verifiable-pxrd/docs/ENVIRONMENTS.md`. The condition's ordinary solve prompt is
deliberately overridden by this experiment's visible reviewer wrapper.

`doctor` fails closed unless the runtime variables and installations documented in the
parent repository are available.

## Configuration

[`experiment.toml`](experiment.toml) records the frozen model, resource limits,
GEPA budget, prompt paths, and benchmark integration. The initial budget of 180
metric calls corresponds to roughly a dozen reflective mutations with a
three-example reflection batch and ten-example full validation set.

## Commands

After reviewing the prompts:

```bash
cd experiments/inference-scaling/llm-verifier/gepa
uv sync --dev
uv run pxrd-gepa doctor --config experiment.toml
uv run pxrd-gepa validate-data --config experiment.toml
uv run pxrd-gepa render --config experiment.toml --example EXAMPLE_ID
uv run pxrd-gepa optimize --config experiment.toml --dry-run
```

The optimizer refuses to overwrite an existing run. New optimizations should use a new
experiment identifier or archive root; never mutate the frozen v1 artifact in place.
