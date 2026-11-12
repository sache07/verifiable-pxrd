# divalent-tungstates-PG15: multiphase quantitative phase analysis on measured scans

Fifteen measured laboratory powder XRD scans of divalent-metal tungstate syntheses. Each case asks an agent to identify the crystalline phases and refine their weight fractions. The product identities and the number of phases are not given.

The name gives the sample family, the source (PG, Precursor Genome) and the number of scans.

This set complements the simulated single-phase pXRD-100/pXRD-ood corpora. It uses real data, mixtures of two to six phases, and has no noise-free ground truth.

## Source and license

The scans and deposited refinements come from the Precursor Genome dataset:
- paper: arXiv:2607.09903;
- ledger and schema: `lauren-walters/precursor-genome`;
- measurements: Zenodo record 21285546, released under **CC BY 4.0**.

Reference crystal structures come from the Crystallography Open Database (COD), which is public domain. `provenance/SELECTION-AUDIT.md` records why this 15-reaction family was chosen from the 996 usable ledger samples. `provenance/selection/` holds the ledger checksum and the selected cases.

## Contents

| Path | What |
|---|---|
| `cases/case-NNN/{pattern.csv,metadata.json}` | Solver inputs. The metadata gives the precursors, the reported heating temperature and the radiation/instrument description. Checksums are in `input-hashes.json`. |
| `case-metadata.json` | Precursors and temperature per case. |
| `references/case-NNN.json`, `references/case-NNN-reference-data.json` | The deposited refinement for each scan: phase labels, weight fractions, BGMN Rwp and quality flags. |
| `references/ceder_summary.json` | Deposited fits re-scored under the evaluation metric. |
| `references/diagnostic_structures/` | Canonical structures for the hidden-phase targets, and the COD analogues they were checked against. |
| `hidden-phase-targets.json` | Pb₂WO₅ and Pb₃WO₆ on case-013, and Sr₂WO₅ on case-014. These are product phases that the solvers' frozen COD index does not contain. |
| `evaluation/` | The frozen evaluator: `evaluate_attempt.py` and the scoring package it imports. |
| `provenance/pb3wo6-adjudication/` | The post hoc, reference-assisted adjudication that kept Pb₃WO₆ in the case-013 label. |

Agent results on this set are in [`results/experimental-eval/divalent-tungstates-PG15`](../../results/experimental-eval/divalent-tungstates-PG15/README.md).

## Evaluation

The evaluator replays the solver's native GSAS-II `final.gpx` without further refinement, keeping the solver's own calibration and model. It reports:
- observed-data **Rwp on 10.1–99.9° 2θ**, with weights 1/max(counts, 1);
- wider-window and exported-profile diagnostics;
- a necessary geometry and occupancy screen for every submitted CIF;
- a structure-matcher check of the hidden-phase targets.

Projects that are missing or can't be replayed count as explicit failures; reported Rwp is never substituted. Because the data have no noise-free truth, no synthetic structural score is assigned.

## Caveats

**This is development evaluation, not a sealed test set.** These scans informed earlier research choices, including generator ranges and case types for the evolution framework. See `experiments/experimental-evolution/DECISIONS.md`, which calls this set "eval15"; decision 34 widened the generator's peak-asymmetry range after solves on these scans were seen.

The deposited refinements are useful references, but they are not always the best fit under this metric. On case-006, for example, the deposited model's Rwp in this window is 45%.
