# Agent adaptation

This experiment trains a pXRD capability package on a disjoint, externally
verified 50-problem curriculum and evaluates the frozen package with the same
runner and scientific environment used for the unadapted control. The repository
includes:

- the training curriculum and exact verifier;
- conditions for baseline, training, and held-out evaluation;
- commands for importing attempts and launching evaluation waves;
- the trainer instructions and mutable working package; and
- normalized training evidence and the frozen capability.

The same source checkout can run locally or on a worker host satisfying the selected condition.
Authentication and scientific-runtime paths remain machine-local, while append-only run artifacts
can be copied between hosts. The harness does not require a resident service.

The condition registry is shared with the inference-scaling experiments.

## Layout

```text
experiments/agent-adaptation/
  conditions/                  llm, matsci-codex, pxrd-codex, adapted-codex
  prompts/                     shared first-pass solve prompts
  harness.toml                 baseline, capability, paths, and parallelism
  prompt.md                    strict pXRD capability-design contract
  trainer-skill/               trainer skill
  curriculum/train-50/        frozen development problems and external verifier
  working-package/             blank, mutable package used when reproducing training
  artifacts/adapted-codex/    frozen learned result used by the paper condition
  .state/                      ignored ledger, generated wave panels, trainer notes
  .runs/                       ignored imported episodes and fresh trainee waves

results/agent-adaptation/adapted-codex/training/
  pxrd-codex-baseline-50/      environment-only training baseline
  adapted-codex-r1-validation/ frozen behavioral validation
  adapted-codex-first-pass-50/ compact first-pass evidence used by judge training
```

Worker workspaces contain only each problem's `problem_input/`. Reference CIFs are
added to the trainer's evidence after an attempt closes; solutions to unattempted
problems remain unavailable. Held-out benchmarks are kept on separate infrastructure
until the capability is frozen.

On each worker host, copy `runtime.env.example` to `.state/runtime.env` and adapt its
non-secret scientific-runtime paths. Training commands load that ignored file
automatically. Codex authentication remains machine-local and is never stored there.

## Establish the pxrd-codex baseline

The `pxrd-codex` baseline uses the benchmark prompt, general scientific Python,
GSAS-II, and DICVOL14 without additional capability instructions. The 50 attempts
used by the trainer are preserved under
`results/agent-adaptation/adapted-codex/training/pxrd-codex-baseline-50/`; they scored
30/50 `selected_exact`. Complete attempts can also be imported as compact episodes
containing the trace, response, workspace, verifier result, and reference while
omitting Codex credential and state databases:

```bash
uv run vpbench train import-run \
  --config experiments/agent-adaptation/harness.toml \
  --source /path/to/pxrd-codex-training-run \
  --label pxrd-codex-baseline
```

Check the project and fill only missing baseline problems:

```bash
uv run vpbench train doctor --config experiments/agent-adaptation/harness.toml
uv run vpbench train status --config experiments/agent-adaptation/harness.toml
uv run vpbench train baseline \
  --config experiments/agent-adaptation/harness.toml --all-missing
```

Start a trainer task with: “Use `$train-pxrd-capability` to carry out
`experiments/agent-adaptation/prompt.md`.” The trainer analyzes every baseline episode before changing
the package.

## Validate one capability revision

Test named motivating cases under one frozen revision:

```bash
uv run vpbench train wave \
  --config experiments/agent-adaptation/harness.toml \
  --problem vp-004 --problem vp-002 \
  --label revision-001-targets
```

The runner snapshots the prompt, environment contract, active capability, Git revision,
resource limits, complete agent events, workspace, submitted CIFs, and verifier result.
Output directories are append-only; interrupted evidence remains visible and a replacement
wave receives a new label.

Executables placed in `working-package/bin/` are added to trainee `PATH` and expose neutral
`--help` contracts. The solve skill may reference them only when that is part of the frozen
capability design.

Training reruns are used to diagnose capability revisions. Held-out evaluation uses
one frozen capability with the same model, task prompt, compute allocation, and
GSAS-II/DICVOL environment as the `pxrd-codex` control.

The evaluated capability is stored at `artifacts/adapted-codex/package/`.
Training commands write revisions to `working-package/`.
