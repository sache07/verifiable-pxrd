# v5 inventory-gated analogue screen

Frozen package prompt SHA256: `e92adbb355ee5b62df0e80d712f74d31729913c93b968be35b1a9f16c268ad22`.

Prospective success rule: c05 must score at least 80, pass physical review, close the inventory before expensive source/coordinate work, and complete matched profile-plus-coordinate adaptation for credible element-mapped analogue finalists. Leakage, review-trigger sources, frozen invalid branches, chemically fixed fractions, silent parent elimination, or unconstrained coordinate overfit fail regardless of score.

| Attempt | Case | Score | D / Rwp | Scientific result | Intended-behavior audit | Decision |
|---|---|---:|---|---|---|---|
| b001-v5-inventory-coordinate-bfee8b73f7df | c05 | 70.09 | D 0.641 / Rwp 3.322% | Correct CaWO4 + WO3 + Ca3WO6 inventory and essentially exact fractions; physical, converged, replay-clean project | Passed the inventory gate; compared seven mapped parents and gave the four credible low-symmetry finalists equal cumulative Ca/O coordinate blocks. A failed Mg branch was restaged, and Co/Ni/Sr/Mg lineages converged to one framework. It then selected the Sr-derived representative by provenance. However, coordinate recovery for the retained known phases was incomplete and the final nuisance model became very flexible before structural residuals were exhausted. | Reject: scientifically strong and intended analogue behavior, but below the prospective 80-point rule |

## Post-result diagnosis

The score decomposes into a 60.95 profile component and 83.80 structural component. Inventory assignment is complete, the fractions are accurate, and all three cells are close. Site accuracy is 94.1 for CaWO4, 54.4 for WO3, and 64.5 for Ca3WO6. Returned-artifact and oracle-informed inspection shows the remaining structural error is concentrated in several independent oxygen orbits rather than phase identity. In the run, WO3 coordinate work retained only selected W/O blocks; one isolated oxygen block was rejected after producing a short bond, and other oxygen blocks were not jointly recovered. The mapped Ca3WO6 lineages received equal blocks but converged to a local coordinate solution. The final project then used 64 background coefficients, directional size terms for all phases, WO3 texture, roughness, and correlated instrumental widths.

This establishes a new mechanism: after inventory closure, isolated-site coordinate trials under an already flexible nuisance model can trap physically coupled ligand coordinates. A transient bad contact with neighboring sites fixed is not evidence that the whole connected coordinate block is unsupported. The successor should recover coordinates in chemistry-connected, softly restrained blocks under a moderate nuisance model, from multiple starts, before escalating background/profile complexity; it should apply this to every phase with modeled-reflection intensity residuals, not only mapped missing-composition finalists.

v5 is not sent to set-aside validation because it failed the frozen score rule. v6 will retain v5's successful inventory and analogue-finalist behavior while replacing the coordinate/profile ordering.
