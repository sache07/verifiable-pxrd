# v7 post-profile connected-coordinate screen

Frozen package guidance SHA256: `2bbe77554ca21c12a0423fbcd9ed6d1ec918b17bff0a7803a658cdc52b3d40f4`. Prompt SHA256: `03841c47190c190f59917038e93ffb653c76f8e9b9b4f19df21ed51e9b79f103`.

Prospective success rule: c05 must score at least 80, pass physical review, reproduce inventory-first closure and equal credible-analogue treatment, complete the mechanism profile pass, and execute the site-orbit ledger plus connected retries without arbitrary parent caps. Leakage, review-trigger sources, fixed/chemically imposed fractions, silent credible-parent elimination, unconstrained coordinate overfit, or frozen invalid branches fail regardless of score.

| Attempt | Case | Score | D / Rwp | Scientific result | Intended-behavior audit | Decision |
|---|---|---:|---|---|---|---|
| b001-v7-connected-ledger-c85bf110707e | c05 | 0 invalid | Not evaluated; `result.json` absent | No submitted project or report after a four-hour analysis; partial work found the true three compositions but later accumulated duplicate same-composition populations | Initially followed inventory-first search and compared many analogue parents. It later over-applied the site ledger and inventory-closure rules: after a physical three-phase branch near Rwp 6.21%, residuals at existing Ca3WO6 reflections triggered repeated duplicate Ca3WO6 populations, false wolframite/fergusonite searches, and extensive broadening/texture branches. Finalization never began. | Reject: invalid submission, failed time-bounded finalization and residual classification |

## Post-result diagnosis

The evaluator could not run because `result.json` and all final deliverables were absent. This is not an infrastructure-recovery case: the worker remained active, generated extensive analysis artifacts, and exhausted its solve time on scientific branches. It therefore counts as a failed development rollout.

v7 did preserve several intended behaviors. It identified CaWO4 + WO3 + Ca3WO6, rejected a physical-review WO3 source, restaged failed analogue and cubic branches, compared six monoclinic parents under matched swaps, and tested connected coordinate blocks. However, the exhaustive site-orbit ledger had a severe attention cost. When connected oxygen blocks remained unstable and the three-phase profile still showed extrema centered on Ca3WO6 reflections, the worker interpreted those extrema as new line families. It explored false CaWO4 polymorphs and multiple duplicate Ca3WO6 populations, repeatedly re-opening source, profile, texture, broadening, and deletion branches. The run never reserved time for replay or export.

The successor should again start from v5, not v7. It should permit exactly one connected neighboring-ligand retry when an isolated block creates contacts, then restore the parent and move on if instability persists. Residual extrema centered on already modeled reflections must trigger structure/profile alternatives rather than duplicate phases; inventory reopens only for a distinct unindexed multi-line family. The guidance must explicitly reserve time to replay and export the best physical project, even when uncertainty remains.
