# v6 and v8 on eval15 with GPT-5.6 Sol Max

90 fresh solves: three independent attempts on each of the 15 experimental Precursor Genome scans under each of two frozen packages from the `pxrd-evolution` divalent-tungstates run (2026-10-24/25): **v6** (promoted incumbent at the time of launch; prompt SHA256 `cc6d4b26…`) and **v8** (cycle-2 consolidation package; `eb14ae1b…`). The packages were developed on synthetic cases only; the researcher that wrote them never saw these scans.

| Parameter | Condition |
|---|---|
| Model | `gpt-5.6-sol`, reasoning effort `max` (as the evolution solvers and the Sol-max P0 panels) |
| Harness | Same pinned Codex CLI 0.154.0, runner and scientific condition as the Sol-max P0 panel; condition TOML byte-identical to the evolution solvers' |
| Prompt | Exact P0 bytes (`0c5def00…`) followed by the package guidance, exactly as frozen in the run |
| Helpers | The package's six scripts, read-only at `learned/`, byte-identical to the freeze |
| Inputs | Original `pattern.csv` and `metadata.json`, byte-identical to every earlier eval15 panel |
| References | Same frozen DARA-filtered COD 2024 index/CIFs, no masks; no DARA solver, web or ICSD |
| Resources | 2 CPU cores of quota, 5 GiB memory, no swap, 128 tasks per solve; no elapsed-time limit |
| Dispatch | Up to 8 solves concurrently until 21:38 UTC on 2026-10-25, then up to 16 (dispatcher restarted; the 8 running solves were unaffected, and only scheduling changed, not the per-solve condition); hold new starts below 6 GiB free disk or 8 GiB available RAM; capacity rejections retried once per minute via the established recovery path |
| Required outputs | CIFs, fractions and fit statistics in `result.json`, `fit.csv`, `report.md`, `final.gpx` |
| Isolation | Private workspace and session per attempt; inputs and helpers read-only; network, other workspaces, the evolution run's files and all answers inaccessible (probed before launch) |

Workers receive nothing beyond the package: no tool guide, output checker, calibrated instrument file, deposited structures or fractions, prior solutions or scoring information.

## Assessment

Independently replay each `final.gpx` with the solver's fitted calibration and model retained, without refinement, and report observed-data Rwp on 10.1–99.9° with weights `1/max(counts,1)`, alongside inventory and fractions against the deposited Ceder models and physical flags (`control/evaluate_attempt.py`, `scoring_v5`, unchanged from the Sol-max P0 panel). Comparators: the Sol-max P0 panel (`pxrd-sol-max-p0-eval15-repeat2-20261019`) and the matched High P0 panel. No synthetic score is applied. This is development evaluation: these scans informed earlier research choices.

The dispatcher runs on the EC2 host (`control/dispatch.py`, queue in `control/queue.json`); `control/follow.py` mirrors artifacts here every five minutes, rebuilds a partial `report/COMPARISON.md` from the attempts already finished (`assess.py --partial`, same evaluator), and runs the full `control/assess.py` when all 90 slots are terminal. The evolution controller is left running; lower `max_concurrent_solvers` if the researcher is resumed.

## Change on 2026-10-26: v8 cut to two replicates

At 02:20 UTC the user cancelled v8 replicate 3 on every scan to save model budget, so the panel is 75 attempts: v6 3 per scan, v8 2 per scan. The seven v8 r3 solves already running (cases 001–007, 11–76 minutes in) were stopped through their sandbox scopes; their runners recorded `failed` (rc −15) and they are not scored. The eight queued v8 r3 slots never started. `control/dispatch.py` gained a `cancelled` slot state that is terminal and never refreshed, relaunched or retried; the slots and reason are in `control/CANCELLED_SLOTS.json`. `control/assess.py` skips cancelled slots and marks them × in `report/COMPARISON.md`. Nothing about any other attempt's condition changed.
