# Experimental evolution: three divalent-tungstate campaigns

| Directory | Saved job records | Completed solves | Final incumbent | Role |
| --- | ---: | ---: | --- | --- |
| `divalent-tungstates/` | 135 | 135 | v6 | Original baseline evolution; v6 evaluated on measured scans. |
| `divalent-tungstates-fw/` | 36 | 35 | P0 | Earlier framework-access evolution, screened through v9; one final job has no saved score. |
| `divalent-tungstates-access/` | 156 | 156 | P0 | Later framework-access evolution, three repeats per evaluated case; unpromoted v5 also evaluated on measured scans. |

All three include their frozen protocol, packages, synthetic cases, scorer,
solver traces and evolver session. Version numbers belong to individual campaigns;
the curricula and promotion rules differ. The later campaign retains its v7 score
interval instead of treating that assessment as a point estimate.

`researcher/` is the historical on-disk name for the **evolver** session, not an
additional agent condition. See the [multiphase guide](../../docs/MULTIPHASE.md)
and [analysis commands](../../experiments/experimental-evolution/analysis/README.md).

## Original campaign

`divalent-tungstates/` is the complete record of the evolution run that produced the `evolved` package (its `policies/v6/`), using the framework in [`experiments/experimental-evolution`](../../experiments/experimental-evolution/README.md). The layout mirrors the run folder, so paths quoted in STATE.md, the investigations and the researcher session resolve inside this bundle.

### Run summary

- **Researcher:** GPT-5.6 Sol at Max effort in one Codex session. It started at 2026-11-02 19:43 UTC, and its last tool call was at 2026-11-04 02:07 UTC (4,983 tool calls). The operator stopped the run at 04:48 UTC, while the v15 screen was 5 of 6 complete.
- **Problems:** ten synthetic cases in three batches (b001–b003). They were generated from LAB.md, have hidden truths, and were scored by the framework's profile-primary scorer.
- **Solves:** 135 by the same model and effort, in these roles:

  | Role | Packages | Solves |
  |---|---|---:|
  | P0 baseline | P0 | 18 |
  | Development screens | v1–v15 | 66 |
  | Evaluations | v6 (12), v12 (15) | 27 |
  | Prospective transfer on b002/b003 | P0 (12), v6 (12) | 24 |
- **Outcome:** v6 was promoted on 2026-11-03 and remained the incumbent when the run stopped. It is the package evaluated as `evolved` in [`results/experimental-eval/divalent-tungstates-PG15`](../experimental-eval/divalent-tungstates-PG15/README.md).
  - On the six b001 cases, its 18-rollout evaluation averaged 74.1, against 50.0 for P0.
  - On the held-out transfer batches it led P0 by 13.7 (b002) and 26.0 (b003).
  - STATE.md records that promotion was the budget-exhaustion fallback: four b001 cases remained unresolved.

## Contents

| Path | What |
|---|---|
| `researcher/session.jsonl.gz` | The researcher's complete Codex session. |
| `evolve/STATE.md`, `evolve/drafts/`, `evolve/investigations/`, `evolve/requests/`, `evolve/packages/` | The researcher's working state, package drafts, its own analyses and the requests it sent. |
| `evolve/{PROMPT,TOOLS,P0,AGENTS,LAB}.md` | The run's frozen copy of the researcher-facing documents. |
| `policies/P0`, `policies/v1`–`v15` | Every frozen package. `policies/v6/` is the `evolved` package. |
| `batches/`, `cases/` | Batch definitions and the synthetic cases, with truths. |
| `evidence/STATUS.md`, `evidence/package-vN-review.md`, `evidence/decisions/`, `evidence/groups/`, `evidence/responses/` | Broker status, package reviews and decision records. |
| `evidence/investigations/`, `evidence/procedure-tests/` | Broker-run investigations and procedure tests that the researcher requested. |
| `evidence/attempts/<id>/` | Each solve: `record.json`, `score.json`, `launch.json`, `run/codex-events.jsonl.gz`, `run/final-answer.md`, the independent fit, scorer logs, and `workspace/` (deliverables plus `workspace-files.tar.gz`). |
| `scorer/`, `runtime/`, `control/` | The run's frozen scorer, generator and broker code, state and settings. |

## Normalization and omissions

Paths, identifiers, session ids and encrypted reasoning are normalized exactly as in [`results/experimental-eval/divalent-tungstates-PG15`](../experimental-eval/divalent-tungstates-PG15/README.md#normalization).

Left out of this bundle:
- intermediate GSAS-II projects: 26,846 files, every `*.gpx` except each solve's `final.gpx`, and all `*.bakN.gpx`;
- process-monitor snapshots, forward-simulation caches, staging folders, reservations and lock files;
- the workspace copies of solver inputs and of the package helper.

The researcher's three other short sessions on 2026-11-02 are also not included. One belongs to an aborted earlier draw in the same folder. The other two are false starts with at most one tool call.

`EXPORT.json` gives the counts. The raw run is kept privately.
