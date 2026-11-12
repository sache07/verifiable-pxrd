# v8 six-case screen synthesis

## Outcome

v8 scored 48.28, 84.22, 28.78, 74.55, 81.35 and 88.29 on
b001-c03--c06 and b002-c01--c02. The aggregate mean is 67.58 with
population SD 21.69 and 3/6 scores above 80. All six projects are physical,
replay-verified and non-provisional. Four have strict full-framework
inventories; c05 omits a phase and c06 adds one false phase. The two transfer
controls average 84.82, while the four carried hard cases average 58.96.

| Case | Gap to noise floor | Sequence actually performed | Sequence supported by source/oracle diagnosis | Divergence |
|---|---|---|---|---|
| b001-c03 | Fresh atomic Rwp 5.241% vs 2.851%; D 2.359 | Ran the CIF gate, selected physical SrWO4/WO3/SrCO3 models, used neutral inactive HAP values, recovered the exact inventory and fractions, then fitted fourth-order spherical-harmonic SrWO4 texture. | Keep that chemistry, then compare no texture with symmetry-distinct low-index axial and diagonal March-Dollase models under a common profile and require fresh replay stability. | Two retained harmonic coefficients were 95.7% correlated and failed the solver's own support standard. Saved-array Rwp was 3.486%, but fresh reflection/atomic replay exposed the larger gap. |
| b001-c04 | Rwp 2.624% vs 2.487%; D 0.121 | Compared physical wolframite parents, adapted and coordinate-refined MnWO4, compared passing WO3 and Mn3O4 records, neutralized inactive HAP values, rejected bound Mn3WO6, tested size/strain/profile alternatives, and replayed twice. | The performed sequence is the supported sequence. Preserve the CIF, neutral-state, competitor, corrective-check and output gates. | No procedural divergence. The full MnWO4/WO3/Mn3O4 inventory is within 2.15 percentage points; score 84.22 is limited mainly by structural-site credit rather than profile execution. |
| b001-c05 | Rwp 8.537% vs 2.234%; D 16.692 | Rejected the short-contact WO3 source, neutralized HAP values, ran the analogue helper for several Ca-W-O formulas and ranked a Ca3WO6 parent first, but submitted only CaWO4/WO3 at GOF 3.80. | Treat reported precursor amounts/ratio as fixed balance evidence. Construct, justify, health-screen and scale-test the leading balance-motivated analogue before cell refinement or rejection, then reconverge profile and inventory. | It changed precursor coefficients to declare its two-phase inventory balanced and never constructed or scale-tested the helper's leading Ca3WO6 parent despite residuals at the omitted phase's families. |
| b001-c06 | Rwp 2.995% vs 2.509%; D 0.443 | Recovered all four true Pb phases with physical sources and fractions within 2.11 points, removed v7's duplicate WO3, then added 1.35 wt% of a Pnma Pb3WO6-like analogue. | Keep the four supported phases, remove any bound nuisance surrogate, and retain a weak adapted phase only when at least two independent non-coincident families support it after replay. | The trajectory first found the analogue's strongest predicted lines on negative residuals, then retained it chiefly for global fit/BIC gain and one residual near 29.31 degrees while polarization remained at its bound. |
| b002-c01 | Rwp 1.789% vs 1.514%; D 0.400 | Ran the source gate, used a literal neutral HAP baseline, recovered MgWO4/WO3/MgO within 1.17 points, and retained supported March texture, uniaxial strain and a limited replay-stable coordinate correction. | The performed sequence is supported. | No material divergence; score 81.35 is a prospective target pass. |
| b002-c02 | Rwp 3.174% vs 3.012%; D 0.124 | Rejected disordered exact BaWO4 and short-contact WO3, adapted an ordered scheelite, recovered BaWO4/WO3/Ba3W2O9/BaCO3 within 2.55 points, and retained only supported broadening. | The performed sequence is supported. | No material divergence; score 88.29 exceeds the v6 transfer mean and is a strong prospective pass. |

## Cross-case diagnosis

The machine-visible CIF screen and literal HAP state are validated. They were
used successfully on all six cases, eliminated every v7 source regression,
and enabled both transfer controls plus the severe Mn case to pass. The
representative numerical check also triggered real correction in the three
successful cases. These clauses and both helpers should remain unchanged.

The three failures are narrow decision-rule omissions introduced when v8
compressed v6. c05 discovers the right analogue but lacks v6's mandatory
constructed-model scale test. c03 uses a correlated high-order texture model
after v8 drops v6's explicit low-index March comparison. c06 applies the
polymorph competitor rule to WO3 but lacks a sufficiently concrete evidence
standard for a new weak analogue, and it searches phases under a bound nuisance
term. None requires a new executable or case-specific knowledge.

## v9 intervention

Keep both v8 helpers byte-identical and preserve the CIF, neutral-HAP,
corrective-check and schema wording. Add only five general guards: reported
precursor ratios cannot be varied to manufacture balance; a leading
balance-motivated analogue must be constructed, justified, health-screened and
scale-tested before rejection; weak new phases need at least two independent
non-coincident residual families; bound nuisance terms must be reset before
inventory judgment; and texture is limited to no-texture versus
symmetry-distinct low-index axial/diagonal March-Dollase comparisons. Screen
v9 first on unresolved c03/c05/c06, then validate the three set-aside successes
if those mechanisms pass.
