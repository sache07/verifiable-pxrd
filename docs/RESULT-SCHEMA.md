# Run and result schema

Each run directory contains:

```text
run.json                 condition/panel hashes and resource limits
condition.toml           copied self-contained condition
panel.json               copied panel manifest
contract/                copied prompt and optional capability
progress.json            one row per attempt
attempts/<attempt-id>/
  control/assignment.json
  control/reference.cif  hidden from the agent; makes evaluation portable
  prompt.txt
  workspace/             pattern and submitted CIFs
  run/
    codex-events.jsonl
    final-answer.md
    launch.json
    verifier-result.json
evaluation/
  summary.json
  comparable-rwp/         optional blind candidate-ranking output
```

Large session rollouts may be stored in an external artifact archive. Every external
object must be referenced by URL and SHA-256 in `artifact-manifest.json`.

Published bundles under `results/` use the corresponding compact schema:
`bundle.json`, one directory per problem with its submitted CIFs and verifier result,
and an optional deterministic `codex-events.jsonl.gz` chronology.
