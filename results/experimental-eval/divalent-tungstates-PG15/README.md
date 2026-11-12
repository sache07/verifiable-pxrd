# divalent-tungstates-PG15 results

The full expanded-manuscript release is indexed in [RELEASE.md](RELEASE.md): five
main conditions, phase-recovery follow-ups, Sol-high/Opus comparisons, and historical
development records. See the [reproduction guide](../../../docs/MULTIPHASE.md) for
all-condition analyses and independent replay.

The original baseline-versus-evolved comparison below contains two 45-attempt
panels on the 15 measured scans in [`pxrd-bench/divalent-tungstates-PG15`](../../../pxrd-bench/divalent-tungstates-PG15/README.md), with three independent attempts per scan:
- **`baseline/`:** GPT-5.6 Sol at Max reasoning effort, using the plain P0 prompt.
- **`evolved/`:** the same model and harness, plus v6, the package promoted by the evolution run in [`results/experimental-evolution/divalent-tungstates`](../../experimental-evolution/README.md) (its `policies/v6/`). The framework that ran it is in [`experiments/experimental-evolution`](../../../experiments/experimental-evolution/README.md).

`summary.json` is regenerated from the two `per_attempt.json` files by `python scripts/summarize_experimental_eval.py`.

## Conditions

| | Baseline | Evolved |
|---|---|---|
| Model | `gpt-5.6-sol`, effort `max` | same |
| Harness | Codex CLI 0.154.0, same runner and sandbox probe | same |
| Prompt | P0 bytes (SHA-256 `0c5def00…`) | P0 bytes followed by the 331-word package guidance (prompt SHA-256 `06abcffc…`) |
| Tools | Python materials stack, GSAS-II, DICVOL14 | same, plus the read-only helper `stoichiometric_analogues.py` |
| References | Frozen DARA-filtered COD 2024 index, no masks | same |
| Inputs | `pattern.csv`, `metadata.json` (byte-identical) | same |
| Resources | 2 CPU, 5 GiB, 128 tasks, no time limit | same |
| Dispatch | up to 10 concurrent | up to 16 concurrent |
| Dates | 2026-10-19/20 | 2026-11-04 |

## Headline

Values are replayed observed-data Rwp (%) on 10.1–99.9°. Lower is better. Each scan contributes the mean of its three attempts.

| | Baseline | Evolved |
|---|---:|---:|
| Mean of per-scan means | 7.90 | **6.71** |
| Median of per-scan means | 7.20 | **5.86** |
| Replayable attempts | 45 / 45 | 45 / 45 |
| Sr₂WO₅ recovered on case-014 | 0 / 3 | 2 / 3 |
| Pb₂WO₅ recovered on case-013 | 2 / 3 | 2 / 3 |
| Pb₃WO₆ recovered on case-013 | 0 / 3 | 0 / 3 |

Paired over the 15 scans (evolved − baseline):
- **Difference:** mean −1.19; evolved is lower on 10 of 15 scans.
- **Tests:** exact two-sided Wilcoxon signed-rank p = 0.026; two-sided sign test p = 0.30.
- **Bootstrap 95% CI** of the mean difference (seed 20261104): −2.14 to −0.41.

| Scan | Precursors | °C | Deposited reference | Baseline | Evolved | Evolved − baseline |
|---|---|---:|---:|---:|---:|---:|
| case-001 | BaCO3 + WO3 | 400 | 8.00 | 7.20 | 7.32 | +0.12 |
| case-002 | BaO2 + WO3 | 200 | 7.20 | 9.12 | 7.83 | -1.30 |
| case-003 | CaCO3 + WO3 | 500 | 18.28 | 7.89 | 7.84 | -0.04 |
| case-004 | CoO + WO3 | 900 | 6.37 | 6.81 | 5.17 | -1.65 |
| case-005 | Co3O4 + WO3 | 500 | 3.78 | 3.46 | 3.32 | -0.14 |
| case-006 | CuO + WO3 | 800 | 45.05 | 6.80 | 5.40 | -1.40 |
| case-007 | MgO + WO3 | 900 | 13.12 | 9.00 | 7.37 | -1.64 |
| case-008 | MnO + WO3 | 900 | 10.22 | 7.42 | 5.86 | -1.56 |
| case-009 | Mn3O4 + WO3 | 900 | 11.38 | 5.20 | 5.26 | +0.06 |
| case-010 | Mn2O3 + WO3 | 500 | 8.27 | 7.05 | 7.16 | +0.11 |
| case-011 | MnO2 + WO3 | 300 | 7.43 | 6.11 | 5.82 | -0.29 |
| case-012 | NiO + WO3 | 900 | 6.74 | 4.42 | 4.61 | +0.19 |
| case-013 | PbO + WO3 | 500 | 11.54 | 12.51 | 12.56 | +0.05 |
| case-014 | SrCO3 + WO3 | 900 | 15.81 | 15.37 | 9.89 | -5.48 |
| case-015 | WO3 + ZnO | 900 | 15.70 | 10.13 | 5.24 | -4.89 |

The evaluation code and replay instructions are in
[`evaluation/`](../../../pxrd-bench/divalent-tungstates-PG15/evaluation/README.md).
Evaluation outputs include the scorer hashes and unchanged-submission checks.

## Attempt bundles

Each `<condition>/attempts/case-NNN-rK/` contains:

| Path | What |
|---|---|
| `attempt.json` | Normalized summary: timing, tokens, replayed Rwp, phases, checks, and SHA-256 of every raw source file. |
| `prompt.txt`, `job.json`, `run/launch.json`, `run/frozen.json`, `run/preflight.*` | Contract and launch records. |
| `run/codex-events.jsonl.gz`, `run/messages.log`, `run/final-answer.md` | The Codex event stream and the final answer. |
| `agent-session/rollout.jsonl.gz` | The native Codex session, including the images the agent viewed. |
| `workspace/` | Deliverables: `result.json`, `report.md`, `fit.csv`, the submitted CIFs and `final.gpx`. `workspace-files.tar.gz` holds every other workspace file: scripts, logs, `.lst` listings and plots. |
| `evaluation/` | Evaluator output: replay request and result, replayed phase CIFs, curves, assessment log. |

`<condition>/condition/` holds the prompt or package, the job manifest, protocol, settings, input manifest, runner, probe, sandbox harness and pre-launch checks. `evolved/condition/policies/evolved/` is the package as launched; it is byte-identical to the run's `policies/v6/`.

## Normalization

These public bundles differ from the raw records in these ways:
- **Paths:** absolute paths are replaced with the placeholders used across this repository (`<ATTEMPT_WORKSPACE>`, `<PANEL>`, `<HOME>`, `<SOURCE_ARTIFACT>`, …). Host names are removed.
- **Identifiers:** attempt and condition ids are the labels above.
- **Session data:** session and thread ids are dropped, and opaque encrypted reasoning blobs are replaced with `<OMITTED_ENCRYPTED_REASONING>`.
- **Launcher fields:** fields that only concern dispatch are dropped, such as the systemd unit, the host, and free-text authorization or comparison notes.
- **GSAS-II projects:** `final.gpx` files are string-mapped in the same way, and each rewritten project is verified to have an unchanged numerical tree.
- **Left out:**
  - intermediate GSAS-II projects (every other `*.gpx` and every `*.bakN.gpx`);
  - the workspace copies of `inputs/` and of the package's `learned/` helper, which are hash-checked against the released copies (`attempt.json: workspace_copy_checks`);
  - transports that the service rejected for capacity before any model work. `infrastructure_retries` counts them: 25 for the baseline, 0 for the evolved panel.

## Caveats

- **Development evaluation:** these scans informed earlier framework choices (see the benchmark README).
- **Noncontemporaneous runs:** the two panels ran about two weeks apart on the same model alias, which does not guarantee an unchanged backend.
