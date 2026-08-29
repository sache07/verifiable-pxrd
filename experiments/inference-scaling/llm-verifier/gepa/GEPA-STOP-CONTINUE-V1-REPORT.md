# GEPA stop/continue judge, experiment v1

## Bottom line

GEPA produced a materially better pXRD inference-time judge on the frozen validation and development panels. The validation-selected policy preserved every missed first-pass solve while stopping substantially more exact first-pass solves than the seed policy.

On three sealed-development repeats, the learned judge averaged **86.7% decision accuracy** versus **70.0%** for the seed. Both continued every miss. The learned judge stopped **81.0% of exact submissions** versus **57.1%** for the seed, reducing the mean continuation rate from **60.0% to 43.3%**.

This is encouraging evidence for more efficient coverage-directed inference, not yet a final 200-case result. The panels contain only three misses and seven exact cases each, and repeated rollouts on the same ten cases are not independent test examples.

## Frozen experiment

- Inputs: 50 adapted-Codex first-pass pXRD trajectories and submitted CIF sets.
- Split: 30 train, 10 validation, 10 sealed development.
- Validation and development composition: 3 missed submissions requiring `continue`, 7 exact submissions requiring `stop`.
- Reviewer and reflector: `gpt-5.6-sol`, high reasoning, ChatGPT authentication.
- GEPA budget: 180 metric calls, epoch-shuffled three-case reflection minibatches.
- Objective: correct decision `1.0`; false stop `0.0`; false continue `0.5`; invalid output `0.0`.
- Prompts were not edited during optimization.
- GEPA generated 10 policies. Candidate 3 was selected on validation before development was opened.

The reviewer was oracle-unaware. It received only the pattern, first-pass trace and final response, submitted CIFs, and any blind comparable-fit report. The reference CIF and structure-matcher result were kept in a separate control directory excluded from the reviewer sandbox and were read only after `decision.json` was finalized. An audit of the selected-policy reviewer event logs found no reference/oracle access.

The objective deliberately makes a false stop more costly than a false continue: the former strands a potentially recoverable structure, while the latter spends another solver run.

## Validation finalist test

Four finalists—the seed and three learned policies—received two fresh validation repeats. Candidate 3 was the only learned policy that preserved all misses while improving exact-case stopping reliably.

| Policy | Accuracy | Balanced accuracy | Miss recall | Exact stop recall | False-stop rate | Continuation rate | Utility |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Seed | 50.0% | 64.3% | 100% | 28.6% | 0% | 80.0% | 0.750 |
| Selected candidate 3 | **75.0%** | **82.1%** | **100%** | **64.3%** | **0%** | **55.0%** | **0.875** |
| Candidate 6 | 60.0% | 61.9% | 66.7% | 57.1% | 33.3% | 50.0% | 0.750 |
| Candidate 9 | 70.0% | 59.5% | 33.3% | 85.7% | 66.7% | 20.0% | 0.750 |

Candidate 3's original GEPA validation rollout was also consistent: all 3 misses continued and 5/7 exact submissions stopped, for utility 0.90. Across the original and two fresh validation rollouts it never false-stopped a miss and stopped 4–5 of seven exact cases each time.

## Sealed-development result

The seed and validation-selected policy each received three independent development repeats.

| Policy | Accuracy | Balanced accuracy | Miss recall | Exact stop recall | False-stop rate | Continuation rate | Utility |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Seed | 70.0% | 78.6% | 100% | 57.1% | 0% | 60.0% | 0.850 |
| Selected candidate 3 | **86.7%** | **90.5%** | **100%** | **81.0%** | **0%** | **43.3%** | **0.933** |

Per-repeat decision accuracy was `9/10`, `7/10`, and `5/10` for seed, versus `8/10`, `9/10`, and `9/10` for candidate 3. Across 21 exact-case decisions, candidate 3 stopped 17 and seed stopped 12. Across nine miss decisions, both continued all nine.

If the alternative were to rerun every first-pass solve, candidate 3 would have avoided about **56.7% of second solver calls** on this panel while preserving every opportunity to recover a miss. This measures allocation only; whether the resulting continuations actually solve the missed structures still requires the coverage-directed solver experiment.

The judge is not free. On the 30 development calls per policy, seed reviews averaged 187 seconds and candidate-3 reviews averaged 298 seconds (medians 179 and 275 seconds). The learned policy therefore used about 59% more reviewer wall-compute per case because it prompted deeper audits. Its efficiency claim should be evaluated in total tokens/compute as well as avoided solver calls; it is promising mainly because a full second structure solve is usually much more expensive than a five-minute review.

## What the learned policy changed

The seed was short and appropriately conservative, but tended to continue whenever exhaustive proof was absent. The learned policy established a more useful boundary:

- peak positions and indexing are not enough; an instantiated CIF needs atomic-intensity or whole-profile support;
- flexible Pawley/profile fits are bounds, not evidence that the submitted coordinates are correct;
- demonstrable overlaps, impossible bonding, stoichiometry, or occupancy failures are vetoes, while unconventional density or coordination alone are not;
- settings and supercells must be standardized before treating them as distinct structures;
- discrete ordering, symmetry, occupancy, or framework ambiguities matter only when a concrete compatible alternative survives;
- imagined polymorphs or arbitrary larger `Z` values do not justify another solve.

This is a compact scientific verification policy rather than a benchmark-specific list of compounds.

## Usefulness of the reasons

For all three development misses (`vp-048`, `vp-047`, and `vp-015`), every candidate-3 repeat correctly localized the gap: the lattice/indexing was credible, but the atomic-coordinate model had large intensity discrepancies and/or chemically invalid geometry. These are useful instructions for a continuation agent because they preserve supported upstream work and redirect effort to coordinate/framework recovery.

The judge usually left `proposed_branch` null on these misses because the first trace did not establish a specific viable alternative. Thus the reason field is already useful for **uncertainty localization**, but this experiment does not show reliable oracle-containing branch prediction.

The remaining false continuations were scientifically understandable. They concerned concrete near-equivalent alternatives such as a half-cell realization, Cu/S antisite occupancy, or a higher-symmetry metric. Conservatism here spends compute but does not strand misses, which matches the chosen objective.

## Train evidence

After candidate 3 was created, optimizer minibatches exercised it on 30 decisions spanning 21 unique training problems. It continued all five sampled miss decisions and stopped 15/25 exact decisions. This is descriptive rather than a frozen full-train evaluation because the sampling was part of optimization.

## Artifacts

- Stable selected policy: `../judge-v1/policy.md`
- Normalized optimizer output: `provenance/result.json`
- Repeated finalist and development results: `provenance/finalist-summary.json`

The corresponding gated solve schedule and normalized result are documented under
`../../verifier-gated-scaling/` and `results/inference-scaling/verifier-gated-scaling/`.
