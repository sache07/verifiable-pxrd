# v7 six-case screen synthesis

## Outcome

v7 scored 65.08†, 19.36, 61.83†, 71.27, 55.75 and 58.85† on
b001-c03--c06 and b002-c01--c02 (mean 55.36, population SD 16.82,
0/6 above 80).  Every project replayed and every result schema was valid, but
only b002-c01 retained a strict full-framework inventory.  The intervention
therefore improved observability and export discipline without improving the
scientific stopping decisions.

| Case | Gap to noise floor | Sequence actually performed | Sequence supported by source/oracle diagnosis | Divergence |
|---|---|---|---|---|
| b001-c03 | Rwp 3.648% vs 2.851%; D 0.600 | Recovered SrWO4/WO3/SrCO3, audited low/mid/high peaks, tested texture and generalized broadening. | Screen exact records geometrically, retain the physical monoclinic WO3 source, then fit the neutral common profile and supported phase texture/anisotropic strain before re-auditing. | It never challenged the short-contact WO3 record against the available physical exact source and retained a large zero/profile surrogate. |
| b001-c04 | Rwp 22.462% vs 2.487%; D 101.30 | Built MnWO4, added WO3, rejected Mn3O4 under a poor baseline, invented tentative Mn2WO6, ran exhaustive width/texture/audit branches, and submitted at GOF 9.02. | Set every inactive HAP term to a genuinely neutral value before inventory tests, re-establish a narrow common profile, recover Mn3O4 from its coherent families, then assign supported phase size/strain and re-audit. | All phases retained active GSAS defaults (1 micrometre size and 1000 ppm strain) after their refine flags were disabled. The audit visibly showed calculated peaks too broad, but did not trigger the required reset/reinventory. |
| b001-c05 | Rwp 3.103% vs 2.234%; D 0.934 | Used precursor balance, enumerated non-1:1 formulas, invoked the analogue helper, and recovered Ca3WO6 with accurate fractions; then audited and refined texture/size/strain. | Keep the successful balance/helper path, replace the short-contact WO3 source, explicitly neutralize inactive HAP terms, and only then resolve common width, CaWO4 texture, phase broadening and low-angle intensity. | Source geometry was judged only from cation--oxygen bonds, missing four 1.576 A O--O contacts; inactive terms again remained at 1 micrometre/1000 ppm. |
| b001-c06 | Rwp 3.026% vs 2.509%; D 0.476 | Recovered PbWO4/WO3/Pb3O4/PbO with physical sources, neutral HAP state and useful size/texture branches, then added 2.58 wt% triclinic WO3. | Retain the four independently supported phases, reject an alternate WO3 model as a coexisting phase without unique families, and use remaining family-dependent mismatch to challenge physical broadening. | The report's own audit says the duplicate WO3 has no isolated middle/high-angle evidence, but cell stability and a small global Rwp gain were allowed to outweigh identifiability. |
| b002-c01 | Rwp 2.329% vs 1.514%; D 1.359 | Recovered the exact MgWO4/WO3/MgO inventory and accurate fractions; supplied the required nine-row width audit and acknowledged high-angle mismatch/GOF 1.53. | From the saved baseline, act on the directional mismatch with the compatible anisotropic width branch, replay, and repeat the spot check before completion. | The audit was treated as a reporting requirement; the indicated corrective branch was not run. |
| b002-c02 | Rwp 4.168% vs 3.012%; D 0.944 | Recovered all four formulas/fractions and used balance, watch-list, texture and broadening challenges. | Reject the split/disordered exact BaWO4 and short-contact WO3 sources, adapt an ordered scheelite parent, then reconverge the same inventory/profile sequence (the v6 transfer did this 3/3). | No occupancy/contact screen was executed. The final BaWO4 has 32 partial sites and 16 short O--O contacts; WO3 has four more. |

## Cross-case diagnosis

The successful v7 additions are narrow: c05's balance plus charge-balanced
formula enumeration repairs the v6 missing-formula failure, and the literal
schema guard eliminates malformed submissions.  The mandatory table is not a
corrective mechanism.  All six solvers produced extensive numerical audits,
yet none passed 80; c04 even documented a gross mismatch and still froze it.
The table also consumed attention that v6 had spent on source screening.

Three failures are caught by one generic source check.  The investigation-only
`v8-cif-audit/cif_health.py` reports partial/mixed occupancies, impossible
contacts and close O--O sites.  Retrospectively it flags every v7 source
regression and passes 18 directly relevant physical v6 structures.  This is a
read-only necessary screen, not an automatic repair or stability certificate.

The second replicated failure is semantic: GSAS-II phase size = 1 micrometre
and strain = 1000 ppm still broaden peaks when refinement is off.  “Prune” and
“neutralize phase terms” were insufficiently concrete.  The package must name
the neutral state (large size, zero strain, March ratio one, zero roughness) and
require checking the values, not only flags.

## v8 intervention

Use one executable only: ship the generic CIF health report and require it on
candidate and final CIFs.  Preserve c05's precursor/charge-balance and analogue
path, plus the concise schema check.  Replace the per-phase report table with a
few representative numerical spot checks and an explicit stopping rule: a
structured mismatch or materially excessive goodness-of-fit requires one
causal correction from the same baseline and a repeated check before
submission.  State that alternate records and polymorphs are competitors unless
independent unique families establish coexistence.  Keep all case identities,
sources and fitted values out of the package.
