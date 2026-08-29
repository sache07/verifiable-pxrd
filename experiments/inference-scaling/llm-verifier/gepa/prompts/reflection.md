Improve the general pXRD judge policy using the completed training cases below.

For each case you have read-only access to the evidence available to the blind
judge, the original solver and judge traces, the submitted CIFs, and a separate
oracle directory containing the reference CIF and exact verifier result. Inspect
the actual files and use scientific Python tools when helpful. Determine what the
submitted structure got right or wrong, what the solver and judge actually
established, and why the current decision succeeded or failed.

Use the reference only for training-time diagnosis. The replacement policy must
express transferable checks that a future judge can perform from its blind
inputs; it must not depend on a hidden reference or encode case-specific formulas,
identifiers, cells, or space groups. Preserve useful behavior on correctly
handled cases, and do not improve apparent accuracy by simply always stopping or
always continuing.

The immutable reviewer wrapper and `decision.json` schema cannot change. Write
only the complete replacement policy to `judge-policy.md`, using at most
{max_policy_words} words. Do not write case analyses or modify any evidence.

Current policy:

```text
{current_policy}
```

Training cases, outcomes, and artifact directories:

```json
{reflective_examples}
```
