# v5 prospective review

## Intervention

v5 is guidance-only and restores the successful v3 ordering while narrowing v4's coordinate rule. It adds an explicit inventory-closure gate: when coherent unassigned line families remain and the fit is well above counting noise, the solver must return to chemistry-guided missing-phase search before spending substantial effort on known-source polymorphs, coordinates, or nuisance terms.

Equal restrained coordinate adaptation is now scoped only to element-mapped missing-composition analogue finalists. Ordinary same-composition sources keep fixed coordinates until source selection. This preserves v4's valid mechanism—that inherited analogue coordinates can confound framework ranking—without inviting exhaustive coordinate work on already known phases before the inventory is complete. No case answer, source identifier, hidden coordinate, fraction, nuisance value, or lookup rule is included.

## Evidence from prior screens

| Case / package | Result | Prospective diagnosis used for v5 |
|---|---:|---|
| b001-c04 / v3 | 96.4, pass | Inventory closure preceded equal analogue comparison; distinct wolframite lineages converged under equal coordinate flexibility. Preserve this behavior. |
| b001-c05 / v3 | 33.4, fail | Found the missing composition, but selected among analogue parents with inherited coordinates fixed. Preserve discovery; repair final parent ranking. |
| b001-c05 / v4 | 23.5, fail | Never sought a missing composition and instead spent 33 coordinate blocks comparing known WO3 sources at Rwp 10.64% versus a 2.62% counting floor. The coordinate rule was applied before inventory closure and to the wrong class of candidates. |

Independent baseline evidence supports coordinate-adapted analogue ranking: two ordered-parent lineages that differed before adaptation converged to essentially the same physical structure and profile after matched coordinate refinement. The v4 result separately demonstrates that this step must not displace residual-led inventory completion.

## Prospective unresolved-case prediction

| Case | Predicted v5 behavior | Success evidence |
|---|---|---|
| b001-c05 | Reopen inventory while coherent residual lines remain; construct mapped missing-composition frameworks before exhaustive known-source work; then compare several credible analogue parents with matched profile restarts and equal restrained coordinate blocks | Correct physical inventory, materially improved hidden-phase geometry and noise-floor-directed profile, score at least 80 |

Prospective rule: c05 must score at least 80, pass physical review, close the inventory before expensive source/coordinate work, and complete matched profile-plus-coordinate adaptation for credible mapped analogue finalists. Leakage, review-trigger sources, frozen invalid branches, chemically fixed fractions, silent parent elimination, or unconstrained coordinate overfit fail regardless of score.

If c05 passes, run one v5 solve on set-aside c01/c02/c03/c04/c06 to complete the six-case one-rollout validation under one package before evaluation replicas.
