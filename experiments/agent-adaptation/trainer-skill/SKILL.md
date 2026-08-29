---
name: train-pxrd-capability
description: Build and validate a minimal learned pXRD capability from blind, externally verified trainee episodes. Use when completing the pxrd-codex training baseline, analyzing pXRD attempts, revising the active package, running targeted behavioral checks, or freezing the held-out snapshot.
---

# Train the pXRD capability

Act as the trainer, not as a solver in trainee workspaces. The project prompt defines what
the package may contain; this skill defines the evidence and wave mechanics.

## Establish the baseline

1. Run `uv run vpbench train doctor --config <config>` and
   `uv run vpbench train status --config <config>`, then read the project prompt and ledger.
2. Keep held-out cases sealed. A baseline trainee receives only staged problem input, the
   fixed scientific environment, and the solve prompt. The verifier and trainer may read its
   reference only after the attempt closes.
3. If baseline problems remain, run:

```bash
uv run vpbench train baseline --config <config> --all-missing
```

This skips problem identifiers already represented by valid imported or native baseline
episodes. Do not revise the package until every declared baseline attempt has closed.

## Analyze and revise

Read prompts, chronological events, final responses, retained workspaces, verifier results,
and now-visible references. Reconstruct what was actually instantiated and scored. Compare
successes with failures so the package preserves useful unconstrained behavior. Strongly consider
the verifier design and behavioral failures to present verifier-accepted solutions.

Before editing, write a trainer-only synthesis under
`experiments/agent-adaptation/.state/notes/` that
identifies the motivating problems, observed mechanism, proposed intervention, explicit
behavioral prediction, expected transfer, and regression risk. Implement one coherent
revision within the project prompt's strict surface. Test executables locally, inspect the
complete diff, and commit the accepted revision with motivating problem identifiers in the
commit message. Keep oracle details outside the active package.

## Validate the revision

Launch a blind motivating-case wave with one `--problem <id>` argument per case:

```bash
uv run vpbench train wave --config <config> \
  --problem <id-1> --problem <id-2>
```

Use at most three waves, normally one or two. The first can include all motivators; later
waves should shrink to cases that still test package engagement or mechanics. Include only
the minimum prior successes needed for a concrete regression risk. Every member of a wave
uses the same committed capability snapshot.

Before every rerun, state what behavior should change. If the intervention did not engage
or its mechanics failed, revise or abandon it before another wave; do not repeat unchanged
runs. If the intended capability worked but the structure still missed for another reason,
record that result and move on. The purpose of motivating reruns is to validate the learned
capability, not to force every training problem to pass.

A sealed mechanical replay can test a tool contract but cannot replace a fresh blind rerun.
Preserve all outcomes. Once the package works as intended—or a proposed addition proves
intrusive or unsupported—repair, remove, or retain it according to the evidence and stop.
Run final tests, leave a clean commit, record the selected revision and budget, and freeze it
before opening held-out evaluation.
