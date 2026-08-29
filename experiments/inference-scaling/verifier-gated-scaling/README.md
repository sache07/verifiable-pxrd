# Verifier-gated scaling

This directory freezes the paper-reported verifier-gated inference-scaling
experiment. It begins with one ordinary adapted-Codex solve per problem and
uses the blind `judge-v1` verifier to decide whether additional solver calls are
warranted.

The schedule is:

```text
S0 -> J0 -> C1 -> J1 -> S2 -> J2 -> S3
```

- `S0` is the initial ordinary solve.
- `J0` reviews `S0`.
- `C1` is an evidence-conditioned continuation. It receives the `S0` trace,
  response, submitted CIFs, and the `J0` decision.
- `J1` reviews `C1`.
- `S2` is a fresh ordinary solve that receives only the original task.
- `J2` reviews `S2`.
- `S3` is a second fresh ordinary solve that receives only the original task.

A `stop` decision terminates the case. CIFs accumulate across every completed
solver stage, and submitted alternatives count toward exact-candidate recovery.
The hidden reference is unavailable to all agents and is used only for
retrospective scoring.

## Reproduce the run

First validate the adapted-Codex environment described in
[`experiment.toml`](experiment.toml). Then run:

```bash
uv run python experiments/inference-scaling/verifier-gated-scaling/run.py \
  --output /absolute/path/to/raw-run
```

The runner permits at most 16 concurrent agent calls. Judges receive 2 CPU,
5 GiB, and 30 minutes; solvers receive 2 CPU, 5 GiB, and 60 minutes.

## Normalize a completed run

```bash
uv run python experiments/inference-scaling/verifier-gated-scaling/normalize.py \
  --raw-root /absolute/path/to/raw-run \
  --initial-source /absolute/path/to/frozen-initial-bundle \
  --output results/inference-scaling/verifier-gated-scaling
```

Normalization retains prompts, decisions, compressed chronological traces,
submitted CIFs, verifier results, launch metadata, and the cumulative candidate
pool. It removes runtime homes, copied workspaces, duplicated evidence, hidden
references, credentials, and machine-specific paths. Re-run the integrity
checks without writing anything using `normalize.py --check RESULT_DIRECTORY`.

The frozen judge is in
[`../llm-verifier/judge-v1/`](../llm-verifier/judge-v1/), and the published
normalized result is in
[`../../../results/inference-scaling/verifier-gated-scaling/`](../../../results/inference-scaling/verifier-gated-scaling/).
