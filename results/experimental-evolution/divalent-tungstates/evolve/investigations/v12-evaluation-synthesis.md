# v12 cycle-2 evaluation synthesis

## Outcome

The locked post-budget evaluation contains 18 v12 rollouts: three on each of
b001-c03--c06 and b002-c01--c02. Every scientific failure and the c02 partial
submission remains in the prospective mean.

| Condition on the same six cases | Mean | Population SD | Range | Scores >80 |
|---|---:|---:|---:|---:|
| P0 | 45.75 | 17.16 | 24.11--87.56 | 2/18 |
| Incumbent v6 | 68.35 | 22.26 | 11.60--93.42 | 8/18 |
| v12 | 61.57 | 18.77 | 33.06--93.16 | 2/18 |

v12 is 15.82 points above P0 but 6.78 below v6 on the identical panel. It has
17 physical passes plus one physical-review result, strict full-framework
inventory in 14/18, one partial submission, and one adjudication-status score.
None of its six case means exceeds 80. The strong-condition and incumbent-
improvement criteria both fail.

| Case | P0 mean | v6 mean | v12 scores; mean (SD) | v12 - v6 | Evaluation |
|---|---:|---:|---|---:|---|
| b001-c03 | 46.31 | 73.53 | 70.68/72.41/76.14; 73.08 (2.28) | -0.46 | Stable chemistry/source/axis execution, but no target pass |
| b001-c04 | 40.95 | 61.87 | 37.36/33.09/33.06; 34.50 (2.02) | -27.36 | Decisive held-case profile regression; one inventory omission |
| b001-c05 | 26.41 | 52.37 | 76.46/67.19/76.28; 73.31 (4.33) | +20.94 | Clear gain, though one false trace CaO and no >80 run |
| b001-c06 | 43.25 | 77.47 | 79.81/43.08/51.60; 58.16 (15.70) | -19.31 | Massicot/source recovery not reproducible |
| b002-c01 | 56.41 | 60.15 | 58.54/56.41/58.26; 57.74 (0.94) | -2.41 | Stable strict inventory, stable profile failure |
| b002-c02 | 61.17 | 84.73 | 93.16/35.65 partial/89.11; 72.64 (26.21) | -12.09 | Two excellent transfer passes, one exact-grid export failure |

## Cross-case diagnosis

### b001-c03: source and directional mechanism stable, profile/structure capped

All three rollouts recover physical SrWO4/monoclinic-WO3/SrCO3 with strict
inventory and close fractions. The two added runs execute the intended SrWO4
[111], signed WO3 [10-1], and SrCO3 [001] challenges. The best run reaches
Rwp 3.296% versus the 2.851% oracle floor (D 0.342). The noise-floor sequence is
the same correct inventory and source ranking followed by a compact collective
width/complete-axis replay and a higher-fidelity adapted SrWO4 parent. v12
diverges by spending attention on many reversible trials while leaving residual
profile and site-model error. This is parity with v6, not a replicated gain.

### b001-c04: the cyclic loop does not recover the compact good basin

The best score is only 37.36, with Rwp 7.447% versus a 2.487% floor and D 8.589.
Two runs recover MnWO4/WO3/Mn3O4; the third omits true 6.27 wt% Mn3O4. All three
retain elaborate combinations of background, displacement, roughness, common
widths, texture, and phase broadening while remaining far from the signal.
The demonstrated near-floor sequence is v6's concise one: adapt physical
wolframite, retain Mn3O4 after the clean-profile watch-list challenge, select
the correct WO3 source, then rebuild a compact profile. v12's broader reversible
loop increases work without reliably returning to that basin. Inventory recovery
alone does not rescue the profile.

### b001-c05: genuine chemistry gain, remaining collective-width gap

v12 reliably improves the difficult Ca case. All runs retain the three true
formulas, two are strict, and the best reaches 76.46 (D 0.422, Rwp 2.634% versus
2.234% floor). One rollout adds false 0.285 wt% CaO; another explicitly rejects
the same trace hypothesis. The successful sequence is chemistry closure,
Ca3WO6 analogue construction, source challenge, and reopened shared-intensity/
width tests. The remaining noise-floor sequence requires collective phase-width
reopening from an interior common-profile basin, then deletion, rather than
independent phasewise trials. This is v12's only clear case-level gain.

### b001-c06: exact-formula persistence is not rollout-stable

The original screen run nearly passes at 79.81 with exact four-phase inventory.
A second run omits true massicot PbO and scores 43.08; the third finds all four
formulas but uses nonmatching WO3/Pb3O4 frameworks with short-contact review
flags and scores 51.60. The near-floor sequence is exhaustive four-formula
inventory, distinct physical source competition for each formula, followed by
finite sizes and symmetry-appropriate Pb-oxide/WO3 strain from a common profile.
v12 sometimes stops after the wrong passing source or lets angular/width terms
absorb the missing phase. The exact-formula clause changes behavior but is not
reliable enough to replace v6.

### b002-c01: chemistry is reproducible, profile inadequacy is reproducible

Every rollout gives strict physical MgWO4/WO3/MgO inventory and fractions within
1.45 points, but all score 56--59. Rwp remains 2.219--2.305% versus a 1.513%
floor, with D 1.14--1.31. The worker repeatedly retains MgWO4 [010] texture and
different WO3 strain allocations. The noise-floor sequence needs the same phase
list followed by direct family-wise evidence that rejects the stable but wrong
profile allocation. Additional chemistry/source prose cannot repair this case.

### b002-c02: strong scientific transfer, catastrophic export variance

Two runs are excellent strict four-phase solutions: 93.16 (D 0.0547, Rwp
3.083%) and 89.11 (D 0.1297, Rwp 3.180%) against a 3.009% floor. Both reject the
split exact BaWO4 record, adapt an ordered scheelite, retain Ba3W2O9/WO3/BaCO3,
and quantify every phase within 1.36 points in the latter run. The other run has
the same strict inventory, structural score 89.12, and fractions within 1.95
points, but writes the raw pattern to XYE with only eight significant digits.
Every one of 8,301 2theta values changes by up to 4.82e-6 degrees, so its GPX no
longer contains the original observations and receives zero profile credit
(35.65 partial). The noise-floor sequence is otherwise demonstrated; the missing
step is an exact original-grid/project replay gate, not more phase-search logic.

## Decision and carried hypotheses

Do not promote v12. Retain v6 as incumbent. v12 improves P0 and contains useful
mechanisms, but it regresses four of six case means versus v6, has no case mean
above 80, and turns a successful source/inventory substrate into a longer,
less-reliable profile process.

The evidence worth carrying into the next cycle is deliberately small:

1. preserve v6's validated analogue/source/watch-list substrate;
2. retain the c05 lesson that a compact collective-width reopening can succeed
   where independent phasewise trials stall;
3. require exact preservation of the original observation grid and, when a
   project has any ambiguity, an explicit `refinement_histogram` selector;
4. avoid v12's exhaustive cyclic expansion unless the prospective b003 results
   identify one narrow, replicated correction.

No successor package is designed before the blinded b003 P0/v6 comparison
finishes. The next active panel is b001-c03--c06 plus b003-c01--c02.
