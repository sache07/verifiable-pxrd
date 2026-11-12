# b003 prospective transfer synthesis

## Outcome

The frozen comparison contains all 12 predeclared rollouts: three P0 and three
incumbent-v6 solves on each new b003 case. Scientific failures and the one
provisional physical-review result remain in the means.

| Case / condition | Scores; mean (population SD) | Range | >80 | Physical pass | Strict inventory |
|---|---|---:|---:|---:|---:|
| b003-c01 P0 | 0.00 / 57.23 / 64.39; **40.54 (28.81)** | 0.00--64.39 | 0/3 | 2/3 | 2/3 |
| b003-c01 v6 | 45.52 / 78.03 / 85.32; **69.62 (17.30)** | 45.52--85.32 | 1/3 | 3/3 | 3/3 |
| b003-c02 P0 | 29.34† / 65.42 / 41.73; **45.50 (14.97)** | 29.34--65.42 | 0/3 | 2/3 | 2/3 |
| b003-c02 v6 | 63.49 / 71.80 / 69.68; **68.32 (3.52)** | 63.49--71.80 | 0/3 | 3/3 | 3/3 |

Across both cases P0 averages 43.02 (population SD 23.09, range 0--65.42)
and v6 averages 68.97 (SD 12.50, range 45.52--85.32). Thus v6 gains 25.95
points overall, is physical and strict in all six rollouts, and reduces the
condition-level variance. It beats P0 by 29.08 points on the Ni case and 22.82
on the Cu case. The transfer is positive, but the strong target is not met:
neither v6 case mean exceeds 80 and only one of six v6 rollouts does.

The independent profile floors are Rwp 1.4372% for c01 and 2.3880% for c02.
The exact rollout diagnostics are:

| Case / condition | D values | Independent Rwp values (%) | Maximum matched fraction error |
|---|---|---|---:|
| c01 P0 | 0.554 / 1.714 / 1.147 | 1.788 / 2.372 / 2.128 | 0.456 percentage point; r1 has a missing/extra framework despite close nominal fractions |
| c01 v6 | 5.299 / 0.503 / 0.280 | 3.636 / 1.747 / 1.614 | 0.784 percentage point |
| c02 P0 | 79.923 / 0.883 / 2.433 | 18.546 / 3.307 / 4.476 | 2.921 percentage points |
| c02 v6 | 0.812 / 0.450 / 0.531 | 3.226 / 2.873 / 2.960 | 1.811 percentage points |

## b003-c01: NiWO4 analogue/source control

All six runs identify NiWO4, monoclinic WO3 and rocksalt NiO. v6 satisfies the
predeclared mechanism in every rollout: it does not trust the malformed exact
NiWO4 file as a complete structure, uses physical wolframite relatives to
repair or reconstruct the missing site model, retains all three phases, and
exports physical CIFs. One run adapts a FeWO4 parent; the other two reconstruct
the exact-composition model with Zn/Fe/Mn/Mg wolframite evidence. Refining the
symmetry-allowed NiWO4 coordinates raises its site accuracy from about 81% in
the conservative run to 93.58% and 94.71% in the two stronger runs. The latter
two reach D 0.503 and 0.280, close to the clean specimen-control floor.

The low v6 run is not an inventory or source failure. It has strict fractions,
physical models and structural score 89.99, but stops at Rwp 3.636% after
retaining a conservative heavy-atom-only NiWO4 model plus small texture/strain
terms. The two stronger runs refine the complete supported NiWO4 coordinate
set, rebuild the source/profile hierarchy, and score 78.03 and 85.32. This is a
replicated structural-coordinate lesson, with remaining rollout variance in
how far the refinement proceeds.

P0 also finds the phase list, but source/geometry validation is unreliable.
Its first run achieves an apparently excellent Rwp 1.788% by freely refining
both low-symmetry structures. The exported WO3 then contains four fully
occupied O--O contacts of 0.685 angstrom. The hard physical gate correctly
sets the score to zero. The other P0 runs remain physical but retain less
accurate NiWO4 and WO3 site models (structural scores 87.81 and 91.13) and
profile D 1.714/1.147. This is not a failure to see the phases; it is failure to
combine coordinate recovery with a complete contact screen.

## b003-c02: Cu3WO6 intermediate / nominal-CuWO4 decoy

Every run, including P0, identifies the exact Pa-3 Cu3WO6 intermediate,
residual monoclinic WO3 and tenorite CuO. Every run explicitly tests and rejects
CuWO4; no false nominal product is submitted. The new chemistry/decoy question
is therefore solved by both conditions. v6's gain comes from reproducibility:
all three runs retain the exact three-phase inventory, choose the ambient
Cu3WO6/CuO and neutron-derived monoclinic-WO3 sources, and converge related
profile models. Their D values are 0.812/0.450/0.531 and their scores have only
3.52 points of population SD.

The v6 ceiling is structural. All three final projects preserve the published
Cu3WO6 and WO3 parent coordinates after coordinate/ADP trials are rejected as
correlated or nonphysical. Consequently the scorer reports virtually identical
site accuracies in every run: about 50.57% for Cu3WO6, 57.37% for WO3 and
92.49% for CuO. Structural scores are only 75.94--76.19 even when the profile
is good. The exact database entries are the correct frameworks, but this case's
ordinary registered-to-sample perturbations still require restrained,
symmetry-aware coordinate recovery. The successful Ni runs show that such
recovery can be both physical and high-value; freeing every atom at once is not
the reliable route.

P0's c02 variance has two distinct causes. Run 2 is a physical strict solution
with structural score 83.88, but its fractions miss by as much as 2.92 points
and D remains 0.883. Run 3 selects a near-monoclinic triclinic WO3 model and
retains poor parent coordinates, giving structural score 60.63 and D 2.433.
Run 1 refines Cu3WO6 cations and reports stored Rwp 3.171%, but carries an
eighth-order spherical-harmonic WO3 texture and directly refined structures
whose fresh evaluator reflection regeneration replays at Rwp 18.546% and
D 79.923. Its WO3 also has four 1.577 angstrom O--O contacts and requires
physical review. The provisional 29.34 score is retained. A reopen/refine of
cached project arrays was not a sufficient replay gate; reflection-list
regeneration and full geometry validation are necessary after coordinate or
high-order texture changes.

## Transfer decision and next-package implications

v6 transfers materially better than P0 and remains the incumbent. The
prospective source/inventory substrate is validated beyond the original
chemistries:

1. tier-1 wolframite adaptation survives the malformed-exact-source control;
2. off-stoichiometric Cu3WO6 is found from residual families rather than
   replaced by nominal CuWO4;
3. weak residual NiO/CuO is retained in all six v6 rollouts;
4. all v6 projects are physical, strict and replay-verifiable.

The comparison also gives a narrow replicated correction for cycle 3. Preserve
v6's inventory/source/profile workflow and add a late structural-coordinate
stage: after inventory, source, cells and a physically adequate profile are
stable, challenge symmetry-allowed high-scattering coordinates in small
groups, replay from the parent on failure, and accept only improvements that
survive full contact/coordination checks and fresh reflection regeneration.
Do not free all coordinates or ADPs together. Also carry the exact observation
grid/histogram gate and the earlier c05 collective-width lesson, but do not
revive v12's exhaustive cyclic search.

The active development panel is b001-c03--c06 plus b003-c01--c02. The new Ni
case needs lower variance in coordinate/profile completion; the Cu case needs
site recovery without losing its stable inventory/profile solution. Results on
the two new cases remain reported separately from the learned b001 carryovers.
