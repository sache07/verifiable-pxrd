# v7 rollout audit

Prospective gates are in `investigations/v7-predictions.md`. This file is
updated as the 18 durable cycle-3 slots complete.

## b004-c01 replicate 1: `b004-v7-e7c34827d991`

Score 72.83, hidden D 0.587, independently replayed Rwp 2.911%; physical and
recovered, not at the noise floor. It selects exact COD 1533878 Ba3W2O9, COD
2311041 monoclinic WO3, and COD 9010928 BaCO3 at 72.58/22.58/4.84 wt%. The
maximum fraction error is 1.33 percentage points. Site accuracies are
91.1/76.3/59.4% for major/WO3/carbonate.

The package behavior is compliant. The solver compares two WO3 parents after
equal development, rejects the poorer physical basin, rolls back inseparable
zero/displacement and polarization/Uiso branches, rejects bound/singular
surface roughness, and finishes profile checks before polishing. The shipped
helper hash is exactly `954ecebf...`; it is invoked once on a physical
replay-stable Rwp-3.5157 endpoint. All three non-baseline branches are eligible.
The selected all-coordinate branch reaches Rwp 2.9109, converges with final
shift/esd 0.030, has no frozen variables or violations, and preserves positive
fractions. The submitted `final.gpx`, result Rwp, collected hash, and scorer
fingerprint all match that selected project. Subsequent work is read-only audit
and export.

This passes the per-solve b004 inventory, recovery, physical, helper, and
terminal-ordering expectations. It is 3.09 score points below the P0 case mean
75.92, so the frozen v7 mean >=70 gate remains viable. Its remaining gap is
downstream precision: cell accuracies are about 81-82%, carbonate/WO3 light
sites remain moderate, and a weak BaCO3 texture term is retained despite the
synthetic realization having none. The safe helper improves observed fit but
does not by itself guarantee floor-level hidden agreement.

## b003-c01 replicate 1: `b003-v7-a814be0c3b18`

Score 45.66, hidden D 3.595, independently replayed Rwp 3.054%; physical but
unrecovered. It selects the exact published parents COD 1520200 MnWO4, COD
2311041 monoclinic WO3, and COD 2002703 R-3 Mn3WO6 at
63.57/17.94/18.49 wt%. The complete framework inventory and fractions are
correct, with maximum fraction error 0.83 percentage point. Site accuracies are
78.9/30.3/92.3% for MnWO4/WO3/Mn3WO6; the WO3 coordinate precision is the
dominant structural deficit despite 95.0% cell accuracy.

The package behavior is compliant. The solver develops two symmetry-distinct
WO3 parents to matched checkpoints, rejects their bound-driven oxygen branches,
then selects the exact COD 2311041 basin after equal profile/texture
development. It rejects correlated joint zero/displacement, X/size and
roughness branches and rolls back a boundary WO3 Uiso before declaring physical
closure. The exact helper hash `954ecebf...` is invoked once on the terminal
Rwp-3.2530 checkpoint. Its all-coordinate branch is eligible, converges with
final shift/esd 0.074 and no frozen variables or physical/fraction violations,
and improves Rwp to 3.0544. The result Rwp, submitted project, collection hash
and scorer fingerprint agree; all subsequent work is read-only validation and
export.

Thus the exact-inventory, physical, one-shot-helper and ordering expectations
pass, while this replicate does not supply the preregistered b003 recovery. It
isolates a downstream parameter-recovery miss rather than a discovery or parent
selection miss: the correct WO3 parent is present, but bounded oxygen shifts
were unstable and rolled back, leaving its light-atom sites poorly recovered.
The b003 case still needs at least one recovery among the two remaining solves;
to reach the frozen mean >=52 gate, they must average at least 55.17.

## b003-c01 replicate 2: `b003-v7-6247417cb2e3`

Score 41.91, hidden D 3.950, independently replayed Rwp 3.165%; physical but
unrecovered. It retains the correct three formulas and exact MnWO4/Mn3WO6
parents, but selects physical triclinic COD 2106293 WO3 instead of the
generating monoclinic COD 2311041 parent. Fractions are
62.47/18.83/18.71 wt% for MnWO4/Mn3WO6/WO3, with maximum error 0.83 point.
Site accuracies are 77.9/79.5/18.3%, and the triclinic WO3 also has only 69.9%
cell accuracy. Thus the scorer's broad full-framework inventory passes, but the
discrete WO3 parent choice is a major hidden-precision error.

The solver enumerates COD 2311041 in its source survey but never constructs it:
the five developed WO3 workspaces are COD 1010618, 1528915, 1563541, 2106293
and 2107312. It then compares the physical triclinic basin with the physically
flagged COD 1528915 monoclinic basin, whose 1.57-A O-O contact makes that
comparison non-diagnostic for the clean monoclinic alternative. The triclinic
choice therefore reflects an incomplete ordinary-phase parent screen, not a
failure of equal-depth refinement among the candidates actually built.

Terminal behavior is otherwise compliant. Correlated or boundary nuisance
branches are rolled back before a replay-stable Rwp-3.1904 checkpoint. The
exact helper hash `954ecebf...` is invoked once; all-at-once and phasewise
branches are rejected for coordinate nonconvergence, while heavy/light becomes
eligible at coordinate shift/esd 0.973, has no final frozen variables or
physical/fraction violations, and improves Rwp to 3.1651. The selected result,
submitted project, collection hash and scorer fingerprint agree, and later
work is read-only.

The case now has exact formula inventory 2/2 but no recoveries. Replicate 3
must recover to pass the frozen >=1/3 recovery gate and must score at least
68.42 to reach mean >=52. Replicates 1 and 2 expose distinct downstream modes:
exact-parent light-atom recovery versus omission of the clean exact parent from
the developed shortlist.

## b003-c01 replicate 3: `b003-v7-86114fb931d0`

Score 30.91, hidden D 21.684, independently replayed Rwp 6.801%; physical but
severely unrecovered. It retains exact COD 1520200 MnWO4 and COD 2002703 R-3
Mn3WO6 but precommits to orthorhombic Pnma COD 2107312 WO3. Fractions are
63.46/19.08/17.46 wt% for MnWO4/Mn3WO6/WO3, with maximum error 1.31 points.
Site accuracies are 85.2/64.6/14.4%, and the wrong WO3 parent has only 3.4%
cell accuracy.

The solver's source survey includes clean exact COD 2311041, but its refinement
script exposes only Pnma COD 2107312 and short-contact monoclinic COD 1528915
as WO3 options. In practice it runs only the Pnma three- and four-phase models,
having selected Pnma from calculated line-family resemblance before any
equal-depth Rietveld parent comparison. It then spends the remaining work on
coordinate, texture, width, background and nuisance development inside that
wrong discrete basin. A small Mn3O4 test is properly rejected, and no prototype
sprawl occurs, but accepted-reflection center/wing residuals are incorrectly
treated as entirely profile-limited despite the Rwp-6.80 floor.

Terminal execution is compliant and no-harm. The exact helper hash
`954ecebf...` is invoked once after replay stability. All-at-once and
heavy/light are eligible and physical but improve Rwp by only 0.0087/0.0086
point, below the fixed 0.02 acceptance threshold; phasewise is ineligible for
coordinate nonconvergence. The helper correctly returns baseline. Submitted
Rwp, project hash, collection hash and scorer fingerprint agree, followed only
by read-only validation/export.

## b003-c01 case conclusion

Scores are 45.66/41.91/30.91, mean 39.50 versus the frozen >=52 gate and P0
mean 45.75; D values are 3.595/3.950/21.684. Recovery is 0/3. Only replicate 1
uses the exact physical three-parent inventory; replicates 2/3 choose
triclinic/orthorhombic WO3 after failing to develop clean exact COD 2311041.
Thus all three prospective b003 gates fail: exact physical inventory 1/3,
recovery 0/3, and mean 39.50. Formula-level inventory and R-3 Mn3WO6 retention
are nevertheless 3/3, and one-shot terminal helper behavior is 3/3.

The case distinguishes two unresolved mechanisms. Even exact-parent rep1 is
light-atom limited, while reps2/3 show that the ordinary-source shortlist is
not reliably completed before nuisance refinement. The five-pass helper is
safe but cannot repair either a wrong discrete parent or a terminal checkpoint
whose supported coordinates remain poorly determined. This case is 6.25
points below P0, so it fails its mechanism gates but does not by itself cross
the fixed promotion rule's -15 per-case boundary.

## b001-c03 replicate 3: `b001-v7-6bd695673cfb`

Score 81.19, hidden D 0.341, independently replayed Rwp 1.877%; physical and
recovered. It selects the exact physical CuWO4/Cu3WO6/WO3/CuO inventory at
65.41/13.13/19.18/2.29 wt%, with maximum fraction error 0.54 point. Site
accuracies are 96.1/83.9/63.6/91.4% for CuWO4/Cu3WO6/WO3/CuO.

The solve follows the intended sequence closely. It develops symmetry-distinct
WO3 references at equal profile checkpoints and keeps clean exact COD 2311041;
after the three major phases are mature, it recognizes a coherent four-line
CuO residual family, compares two CuO sources equally, and keeps exact COD
1011194 before closure. It then rebuilds the complete-state profile, rejects
start-dependent or bound-seeking anisotropy, roughness, CuO size and WO3 Uiso,
and separates correlated calibration/asymmetry blocks. The terminal checkpoint
replays at Rwp 2.1263 with max shift/esd 0.055 and no strong remaining
correlations.

The exact helper hash `954ecebf...` is invoked once at that terminal point.
All three coordinate orders are eligible and physical; phasewise is selected
at Rwp 1.8768 with final settle shift/esd 0.126, no frozen variables or
violations, and stable fractions. Submitted result/project hashes, selected
Rwp and scorer fingerprint agree, and all later work is read-only. The branch
converges after three interior settle passes, so this fresh success validates
terminal one-shot use and no harm but does not specifically require the newly
licensed fourth or fifth pass.

This passes every per-solve c03 expectation and supplies the first of two
required recoveries. The two remaining c03 solves must contribute at least one
more recovery and average at least 71.91 for the frozen mean >=75 gate. The
result prospectively reproduces the intended completion gain without the
premature-polish behavior seen in v6.

## b001-c06 replicate 3: `b001-v7-0bd2cb54359a`

Score 16.59, hidden D 172.824, independently replayed full-grid Rwp 19.032%;
physical but severely unrecovered. It submits only MnWO4 plus an analogue-
derived P21/c Mn2WO5 phase at 85.63/14.37 wt%, omitting both the true R-3
Mn3WO6 and WO3 frameworks. Strict phase F1 is 0.4, matched MnWO4 is over by
17.21 points, and the Mn2WO5 substitute has only 19.0% site accuracy.

The solver correctly recognizes one large coherent residual and activates the
conditional reaction/topology workflow. It screens Mn2WO5, Mn3WO6 and MnW2O7
formulas and enumerates both the tier-1 R-3 Mn3TeO6 COD 2211528 route and an
R-3 Cd3TeO6 COD 2242674 route. However, its hard-coded developed shortlist for
Mn3WO6 contains only two C2/c parents, Zn3TeO6 COD 2211529 and Co3TeO6 COD
2015468. The two R-3 candidates actually have better position-screen scores
(0.391/0.333 versus 0.467/0.431) but are never constructed. This violates the
intended symmetry-diverse serious-topology comparison and repeats the exact
c06 mechanism v7 was designed to repair.

The solve instead gives most development to three Pnnm, one P21/c and one C2/m
Mn2WO5 starts, selects P21/c at an already poor Rwp 22.04, and closes a two-
phase model despite a terminal Rwp above 19 and an imbalanced assemblage that
requires hypothesized unquantified W-rich material. Thus it under-segments the
residual into one wrong-formula phase rather than retaining the distinct
Mn3WO6 and WO3 families.

Mechanical terminal behavior is compliant. After nuisance rollback it invokes
the exact helper hash `954ecebf...` once at fit-range Rwp 19.127. All coordinate
orders are eligible; heavy/light is selected at fit-range Rwp 19.0367 with no
violations or final frozen variables, and full-grid replay gives Rwp 19.0320.
The submitted project, collection and scorer hashes agree, and only read-only
checks/exports follow. The generic audit reports a missing result Rwp only
because this solve stores it under `Rwp_percent_full_grid_replay`; manual schema
inspection confirms consistency with the selected project.

This fails every per-solve c06 mechanism expectation: R-3 is neither built into
the serious shortlist nor selected, and the solve is unrecovered. Both remaining
c06 solves must select R-3 and recover to reach the frozen >=2/3 route/recovery
gates; they must average at least 78.71 to reach mean >=58.

## b002-c01 replicate 2: `b002-v7-ca9876455e52`

Score 45.71, hidden D 3.109, independently replayed Rwp 5.301%; physical but
unrecovered. It selects the correct ZnWO4/WO3/ZnO framework inventory at
82.41/11.69/5.89 wt%, with maximum fraction error 1.63 points. Site accuracies
are 84.2/31.7/98.9% for ZnWO4/WO3/ZnO; cells are much stronger at
99.7/88.5/98.7%, isolating coordinate/profile rather than metric failure.

The requested physical-start behavior occurs. Two independent P2/c wolframite
analogues, CoMoO4 and MnReO4, are eventually given the same observed cell and
calibration seed and identical coordinate depth after early setup failures are
classified as unknown. Bound-hit coordinate components are rolled back, and
the MnReO4-derived ZnWO4 basin wins reproducibly. The solver also retains ZnO
from five reflection windows and compares multiple WO3 starts, selecting clean
COD 2311041 over short-contact COD 1528915 and a worse triclinic basin.

The remaining failure is terminal profile completion. Major-phase [111]
texture is strongly supported, but correlated X/size tests reach X=6 or minor
size floors; the solver then fixes X=5.8 just inside the upper range and settles
U=20.66. Roughness, minor-phase texture and several broadening terms are
rejected, leaving a replay-stable but still poor Rwp-7.3199 checkpoint.
Oracle-informed diagnosis confirms the synthetic realization instead uses
X=0.186, U=0.709, strong roughness and texture on both minor phases. Those
case-specific values are diagnostic only, but they show that boundary-adjacent
profile compensation survived despite correct source selection.

The exact helper hash `954ecebf...` is then invoked once and terminally. All
three branches are eligible and physical; heavy/light is selected at Rwp
5.30085 with no violations or final frozen variables. It makes a large safe
coordinate gain, but cannot repair the upstream profile basin or weak WO3
light-atom precision. The selected/result Rwp values, project, collection and
scorer hashes agree, followed only by read-only replay/export.

This passes the per-solve inventory, physical-start, source-validation, helper
and ordering expectations but fails recovery. Both remaining harder-Zn solves
must recover to meet the frozen >=2/3 recovery gate and must average at least
74.65 to reach mean >=65. The fixed no-case-below-minus-15 gate remains
mathematically possible if they average at least 63.07.

## b001-c03 replicate 1: `b001-v7-4052ea72aa72`

Score 55.79, hidden D 1.499, independently replayed Rwp 2.563%; physical but
unrecovered. It submits the correct CuWO4/Cu3WO6/WO3/CuO formula inventory at
64.24/13.33/20.03/2.39 wt%, with maximum fraction error 1.23 percentage
points. COD 4000806 CuWO4, COD 1527404 Cu3WO6 and COD 1011194 CuO are exact
parents, but the WO3 phase is physical triclinic COD 2106293 rather than the
generating clean monoclinic COD 2311041 parent. Site accuracies are
91.7/82.9/94.8/20.4% for CuWO4/Cu3WO6/CuO/WO3, so the wrong WO3 oxygen
registry dominates the structural deficit.

The phase-discovery sequence otherwise succeeds. CuWO4 and Cu3WO6 explain two
full families; a third WO3 family and then the 2.4 wt% CuO family are retained
before closure. The solver compares exact C2/c and Cc CuO starts and keeps the
exact higher-symmetry source. Its WO3 source workflow is incomplete, however.
The frozen-index survey explicitly lists clean COD 2311041, but the detailed
source inspection and GSAS-II candidate script omit it. Only short-contact
monoclinic COD 1528915 and triclinic COD 2106293 are built. Triclinic wins at
an early cell/scale/background checkpoint, Rwp 9.515 versus 10.475, and is
then developed exclusively. Thus the report's claim of equally developed
serious WO3 starts does not cover the available clean exact parent and the
solve repeats the ordinary-source shortlist failure seen twice on b003.

The terminal workflow is mechanically compliant. Unsupported texture,
roughness and bound-limited profile terms are rolled back, and repeated
profile/lattice cycles reach a replay-stable Rwp-2.5634 checkpoint with no
frozen variables. The exact helper hash `954ecebf...` is invoked once at that
point. All-at-once, heavy/light and phasewise reach lower final Rwp values near
2.532, but each remains ineligible after five interior passes because final
coordinate shift/esd is 2.88-3.07; the helper correctly selects baseline.
Submitted and selected Rwp, final project, collection hash and scorer
fingerprint agree, and all later work is read-only validation/export.

This solve passes formula closure, weak-CuO retention, physical validity,
terminal one-shot ordering and helper no-harm behavior, but fails exact-parent
inventory and recovery. Together with recovered replicate 3, c03 is now 1/2
recovered and only 1/2 exact-parent. The preregistered 3/3 exact physical
inventory gate is impossible; replicate 2 must recover and score at least
88.02 to reach both the >=2/3 recovery and mean >=75 gates. It must score about
70.38 merely to keep the final case mean within 15 points of P0.

## b001-c03 replicate 2: `b001-v7-126599b58db7`

Score 59.78, hidden D 1.238, independently replayed Rwp 2.421%; physical but
unrecovered. It selects all four exact parents: COD 4000806 CuWO4, COD 1527404
Cu3WO6, clean COD 2311041 monoclinic WO3 and COD 1011194 CuO at
64.66/13.23/19.76/2.35 wt%. Maximum fraction error is 0.82 percentage point.
Site accuracies are 81.8/80.3/87.2/48.2% for CuWO4/Cu3WO6/CuO/WO3; even with
the correct source, WO3 light-atom precision remains the principal structural
deficit.

The solve follows the intended discovery sequence. It gives physical
monoclinic COD 2311041 and triclinic COD 2106293 equally developed
three-phase checkpoints, keeps the monoclinic basin at Rwp 7.42 versus about
13.8, and marks short-contact COD 1528915 diagnostic-only. It initially
declares three-phase closure, but reopens it when the positive 35.10/38.32
degree family remains coherent. A full eight-line family then supports 2.4
wt% tenorite; exact C2/c COD 1011194 and Cc COD 9016057 are developed to near-
tied Rwp 3.179/3.182 checkpoints, and the higher-symmetry exact source wins.
No post-closure prototype sprawl occurs.

Profile completion is conservative but not floor-level. Unsupported texture,
roughness, CuO strain/size and a boundary common-U branch are rejected. The
solver retains uniaxial strain on CuWO4 [100] and WO3 [001], fixes the
specimen displacement after a competing calibration branch reaches the +800
micrometre bound, and reaches a replay-stable Rwp-2.9706 terminal checkpoint.
The exact helper hash `954ecebf...` is then invoked once. All three coordinate
orders are eligible and physical; phasewise converges after two interior
passes, has final settle shift/esd 0.010 with no frozen variables or
violations, and improves Rwp to 2.4213. Selected/result Rwp, final project,
collection hash and scorer fingerprint agree, followed only by read-only
validation and export.

Thus exact-source selection, weak-phase closure, nuisance rollback, terminal
ordering and helper benefit all pass, but recovery still fails because the
correct WO3 parent remains light-atom limited. The helper makes a large safe
observed-profile gain but cannot by itself establish floor-level hidden
agreement.

## b001-c03 case conclusion

Scores are 55.79/59.78/81.19, mean 65.59 versus the frozen >=75 gate and P0
mean about 84.12; D values are 1.499/1.238/0.341. Formula inventory and weak
CuO retention are 3/3, exact-parent inventory is 2/3, and recovery is 1/3.
Every preregistered c03 gate therefore fails. Replicate 1 omits the clean exact
WO3 source from its developed shortlist, while exact-parent replicate 2 still
misses on WO3 oxygen precision; only replicate 3 combines exact source choice
with floor-directed completion.

The case mean is about 18.54 points below P0, violating the fixed no-case-more-
than-15-below-incumbent rule. Consequently v7 is definitively unpromotable
regardless of the nine remaining outcomes. The durable rollout should still
finish for mechanism evidence and to design cycle-3 candidate 2/3.

## b002-c01 replicate 1: `b002-v7-c8e1c1076ea3`

Score 83.25, hidden D 0.260, independently replayed full-grid Rwp 2.928%;
physical and recovered. It submits ZnWO4/WO3/ZnO at 83.11/12.05/4.83 wt%,
with maximum fraction error 1.27 percentage points. Site accuracies are
94.4/97.2/49.3% for ZnWO4/ZnO/WO3. The exact clean WO3 parent remains
light-atom limited, but the dominant adapted framework and ZnO are highly
accurate and the complete profile is close to the hidden signal.

The decisive mechanism is cation registry rather than formula or metric
discovery. A first normal wolframite assignment leaves the calculated
intensities of the accepted 41.56/41.81 degree ZnWO4 pair reversed. Local
oxygen continuation improves that basin but does not close the family.
Following the conditional unassigned-family rule, the solver rejects unstable
trace W3O8/P21/m WO3 additions, screens symmetry-diverse substituted ABO4
parents, and tests the same P2/c topology with Zn and W interchanged between
its ordered octahedral sites. That inverse assignment lowers matched-state
Rwp from 10.15 to 5.71. Five physical inverse starts derived from CoMoO4,
FeNbO4, MnReO4, InNbO4 and InTaO4 are then adapted at equal depth; the
FeNbO4-derived basin wins fully settled checkpoints at Rwp 3.818 versus
4.010-4.415 and has interior, contact-free oxygen coordinates. Search stops
once that model closes the residual family.

This explains the same-package split from replicate 2. The failed solve
compares two normal P2/c registries and never tests cation interchange;
replicate 1 recognizes the discrete ordering alternative and raises major-
phase site accuracy from 84.2 to 94.4%. It also re-screens the accepted
profile after the structural change and retains interior texture on all three
phases: ZnWO4 [111], WO3 [110] and ZnO [001]. Replicate 2 retains only the
major texture and enters a compensating U/X basin. Replicate 1 still rejects
the generating roughness and retains non-generating profile compensation, so
its recovered D=0.260 does not make the nuisance model uniquely correct.

Terminal execution is compliant. The replay-stable checkpoint has Rwp 3.1163,
maximum shift/esd 0.042, positive scales and no frozen variables or geometry
flags. The exact helper hash `954ecebf...` is invoked once; all coordinate
orders are eligible and physical, and phasewise is selected at Rwp 2.9287
after two interior passes with final shift/esd 0.012 and no violations. Native
full-grid replay is 2.9282. A nominally read-only GSAS-II indexing call changes
serialization metadata after polish, but the solver detects this and restores
the exact accepted `polished.gpx`; final project, collection and scorer hashes
agree, with no scientific post-polish mutation.

This passes every per-solve harder-Zn mechanism gate and provides the first of
two required recoveries. With replicate 2 at 45.71, replicate 3 must preserve
the exact physical inventory, recover, and score at least 66.05 for the
preregistered >=2/3 recovery and mean >=65 gates. The result prospectively
validates equal-depth physical starts, while adding a more specific lesson:
when positions index but accepted-reflection intensities remain reversed,
ordered site assignment is a discrete basin that coordinate polish cannot
repair.

## b004-c01 replicate 2: `b004-v7-712030cdd819`

Score 75.34, hidden D 0.506, independently replayed Rwp 2.836%; physical and
recovered. It selects the exact COD 1533878 Ba3W2O9, COD 2311041 monoclinic
WO3 and COD 9010928 witherite BaCO3 parents at 72.46/22.79/4.76 wt%, with
maximum fraction error 1.21 percentage points. Site accuracies are
88.8/75.2/85.7% for Ba3W2O9/WO3/BaCO3.

The solve independently reproduces the intended closure sequence. Ba3W2O9
and WO3 establish two complete families; after their profile matures, a
coherent residual at about 19.70, 24.12/24.50, 34.8, 42.2, 44.4, 45.1 and
46.96 degrees identifies BaCO3. Adding it lowers pre-profile Rwp from about
6.74 to 4.80 at stable positive scale. No coherent family remains, so the
conditional missing-topology search is correctly not activated.

The terminal model is also disciplined. Specimen displacement is rejected at
99.91% correlation with zero for only 0.001 Rwp-point gain; roughness is
rejected after 99.6-99.97% A/B correlation, boundary hits and start
dependence. Joint polarization/Uiso is rolled back at 98.6% correlation after
forcing Uiso outside the lab range. The solver retains stable polarization,
one Ba3W2O9 uniaxial-strain term and the minimum BIC-supported positive smooth
background, reaching a replay-stable Rwp-3.9616 checkpoint.

The exact helper hash `954ecebf...` runs once and terminally. All three
coordinate orders are eligible and physical; all-coordinate wins at Rwp
2.83635 after one interior pass, final shift/esd 0.071, no frozen variables or
violations, and fractions remain stable. The result stores Rwp under lowercase
`rwp_percent`, so the generic audit's null result field is a schema-only false
negative; manual inspection confirms 2.83634509 and exact selected-project
agreement. Final project, collection and scorer hashes match, followed only by
read-only replay/export.

This passes every per-solve b004 gate. With replicate 1 also recovered and
exact, recovery >=2/3 is already secured. Replicate 3 must retain the exact
inventory and score at least 61.83 to complete the preregistered 3/3 inventory
and mean >=70 gates.

## b001-c06 replicate 2: `b001-v7-c6aead8370f6`

Score 87.45, hidden D 0.169, independently replayed Rwp 1.931%; physical and
recovered. It selects MnWO4, R-3 Mn3WO6 and clean monoclinic WO3 at
68.66/15.66/15.67 wt%, with maximum fraction error 0.45 percentage point and
full framework inventory. Site accuracies are 97.1/87.8/53.0% for
MnWO4/Mn3WO6/WO3. The remaining structural imprecision is concentrated in the
light-atom WO3 model rather than phase identity or quantification.

This solve executes the intended missing-reference mechanism completely. It
first establishes wolframite MnWO4 and clean COD 2311041 WO3, then preserves
an eleven-line residual family at about 20.32, 20.88, 29.14, 32.26, 35.62 and
47.02 degrees. Those reflections index together in R-3 near a=8.89 and
c=10.46 A, while the reaction-balanced Mn3WO6 assignment closes the
MnWO4/WO3 chemistry. The solver constructs symmetry-diverse R-3, C2/c, Pa-3
and P21/c target-composition models. C2/c, Pa-3 and P21/c scales collapse,
whereas the two independent R-3 starts remain near 14 wt%.

Crucially, both serious R-3 starts are developed equally. The Mn3TeO6-derived
COD 2211528 basin reaches Rwp 7.099 with 14.32 wt% Mn3WO6; the independent
Cd3TeO6-derived COD 2242674 basin reaches Rwp 7.166 with 14.13 wt%. Both hit
the oxygen-coordinate neighborhood on the same atoms, those components are
rolled back, and the cleaner tier-1 parent wins the interior comparison. This
is the direct positive contrast with c06 replicate 3, which enumerated the
same R-3 parents but hard-coded only two C2/c models into its developed
shortlist.

The terminal model is conservative and replay-stable. It retains only a weak
WO3 [100] texture term, rejects bound-seeking SH/L and common-U branches, and
keeps physical positive size/strain values. The pre-polish checkpoint has Rwp
2.4631, no frozen variables, no short contacts and matching repeated replay.
The exact helper hash `954ecebf...` is invoked once; all coordinate orders are
eligible, and phasewise is selected at Rwp 1.93115 with final shift/esd 0.035,
no violations and fractions unchanged. Selected/result Rwp, final project,
collection and scorer hashes agree, followed only by read-only replay/export.

This passes every per-solve c06 mechanism gate and gives the first recovery
and R-3 selection among two completed replicates. Because replicate 3 failed
severely, the remaining replicate must also select R-3, recover, and score at
least 69.96 to reach the preregistered 2/3 selection, 2/3 recovery and mean
>=58 gates.

## b002-c02 replicate 2: `b002-v7-10eb16e2e037`

Score 20.87, hidden D 47.637, independently replayed Rwp 12.612%; unrecovered
and provisional because physical validity needs adjudication. It submits
MnWO4, monoclinic WO3 and analogue-derived Pnnm Mn2WO5 at
63.43/22.76/13.81 wt%. Only MnWO4 matches the true phase inventory; its
fraction is 4.28 percentage points high. Site accuracies against the three
hidden frameworks are 80.5% for MnWO4, 15.1% for the Mn2WO5 surrogate against
Mn3WO6, and 16.2% for WO3. Phase F1 is therefore 1/3 despite complete reported
quantification.

The central failure occurs before refinement. After MnWO4 plus WO3 leaves a
broad coherent family, the solver screens several formula families but
commits to A2BO5 because a Mn2AsO5 Pnnm parent needs only about 0.5% isotropic
cell scaling. It then constructs two Pnnm starts and one Cmcm pseudobrookite
alternative, develops those equally, and declares closure when both Pnnm
starts occupy the same basin. The available surviving tier-2 route—COD
2242674 Cd3TeO6 adapted to R-3 Mn3WO6—is never constructed or tested. Thus
the nominally symmetry-diverse comparison is diverse only within the wrong
Mn2WO5 formula and cannot adjudicate the intended A3BO6 topology.

The wrong basin advertises its weakness. The three-phase structural
checkpoint remains near Rwp 16.0, nearly every attempted coordinate atom is
rolled back, and the broad surrogate requires a fixed 0.045 micrometre size
with 7500 ppm microstrain plus supported texture. The solver nevertheless
interprets remaining residuals on those broad peaks as structure-factor or
profile error and spends extensive work on profile grids rather than reopening
the discrete phase model. This is the same shortlist-completion failure seen
in c06 replicate 3, now amplified by premature closure on a flexible broad
surrogate.

Ordinary-source validation also fails independently. Equal preliminary trials
reach Rwp 19.381 for short-contact COD 1528915 WO3, 19.244 for clean exact COD
2311041, and 19.174 for a triclinic alternative (the latter not fully settled
by shift/esd). The solver still carries COD 1528915 forward. Its four
symmetry-related 1.576 A O-O contacts trigger the scorer's adjudication flag;
calling them inherited from the parent does not make the submitted model
physical. This flag is separate from, and does not explain, the missing R-3
framework.

The exact helper hash `954ecebf...` is invoked once at the terminal claimed
checkpoint. All branches are eligible and phasewise safely lowers Rwp only
from 12.6966 to 12.6120, with final shift/esd 0.046 and unchanged phase
inventory. The result uses lowercase `rwp_percent`, so the generic audit's
result field is null; manual inspection confirms exact selected/replayed Rwp,
and final project, collection and scorer hashes agree. Local coordinate polish
cannot repair the absent topology or flagged parent.

This first completed harder-Mn solve constructs and selects no surviving R-3
route and does not recover. The two remaining replicates must together
construct R-3 at least twice overall, include at least one R-3 selection and
one recovery, and average at least 46.56 to reach the preregistered mean >=38
gate. The reusable lesson is to require every serious formula/topology family
to reach an equal checkpoint before closure, especially when a broad surrogate
still needs near-limit profile terms and leaves a high replay Rwp.

## b002-c01 replicate 3: `b002-v7-e7b9d70e5fdb`

Score 26.17, hidden D 61.747, independently replayed Rwp 19.883%; unrecovered
and provisional because physical validity needs adjudication. It submits the
correct ZnWO4/WO3/ZnO formulas at 87.23/10.07/2.70 wt%, versus true
82.00/13.32/4.68 wt%. The major fraction is 5.23 percentage points high.
ZnWO4 and ZnO match at 74.7% and 98.9% site accuracy, but the submitted WO3
has only 31.5% site accuracy and is not accepted as the physical hidden
framework. Formula closure therefore masks both a wrong ordinary parent and a
gross profile miss.

The dominant-phase search is broad but does not reproduce the successful
replicate's discrete registry treatment. The solver converts CoMoO4-II,
ScNbO4 and FeNbO4 P2/c parents plus triclinic and scheelite controls to ZnWO4.
Its initial one-phase comparisons are not clean equal checkpoints: the
CoMoO4, ScNbO4 and FeNbO4 branches finish with frozen profile or calibration
variables, and the FeNbO4 setting is discarded at Rwp 42.2 without the
canonical basis/origin and ordered-site transformation used by recovered
replicate 1. In the complete state, only ScNbO4 and CoMoO4 basins receive the
long comparison. ScNbO4 is eventually selected at Rwp 19.88 versus 21.57,
while the accepted-reflection intensity mismatch is treated as coordinates
and texture rather than a remaining site-registry alternative.

Ordinary WO3 selection independently violates the physical-start intent. The
frozen index enumerates clean exact COD 2311041, but actual multiphase scripts
construct only short-contact monoclinic COD 1528915, triclinic COD 2106293
and P21/m COD 1010618. Clean COD 2311041 never reaches a GSAS-II checkpoint.
The solver chooses COD 1528915 despite its four 1.570 A O-O contacts, calls
the defect inherited, and submits it. The scorer correctly marks the model
`needs_adjudication`; inherited source geometry remains submitted geometry.

The terminal profile is also far from a defensible closure. Major [111]
texture is correctly recovered near 0.704, and major size 0.071 micrometre is
reasonable, but common W rises to 29.70 while U stays at 10, zero settles at
0.236 degrees with displacement fixed to zero, and generating roughness is
omitted. WO3 uses the wrong [010] texture and ZnO texture/size/strain are
omitted after unstable branches; ZnO is consequently only 2.70 wt%. Oracle-
informed diagnosis confirms that the generating state instead has much lower
U/W, substantial specimen displacement and roughness, plus both minor-phase
textures. These values are case-specific diagnostics only, but they establish
that a severe compensating calibration/profile basin survived the stated
rollback rules.

The exact helper hash `954ecebf...` is invoked once at the claimed terminal
state. It correctly selects baseline: all, heavy/light and phasewise branches
reach about Rwp 19.410 but are ineligible because the weak ZnO cell freezes at
its bound and final shift/esd remains about 5.34. Baseline selected/result Rwp,
final project, collection and scorer hashes agree, and later work is read-only.
This is safe no-harm behavior, not evidence that the input was actually
terminal.

## b002-c01 case conclusion

Scores are 83.25/45.71/26.17, mean 51.71 versus the frozen >=65 gate and P0
mean about 72.28; D values are 0.260/3.109/61.747. Formula inventory is 3/3,
exact physical framework inventory is 2/3, and recovery is 1/3. Every
preregistered harder-Zn gate fails. Replicate 1 succeeds by explicitly testing
the ordered registry/basis alternative and completing minor textures;
replicate 2 preserves exact sources but enters a compensating profile basin;
replicate 3 omits both the registry transformation and clean WO3, then accepts
an Rwp-19.88 closure.

The case mean is about 20.57 points below P0, independently violating the
fixed no-case-more-than-15-below-incumbent rule. For v8, the reusable controls
are: normalize symmetry-equivalent settings before rejecting a parent; test
ordered site registries when indexed-reflection intensities remain reversed;
carry every enumerated clean serious ordinary parent into equal development;
and do not call a very high-Rwp, strongly compensating model terminal merely
because its residual extrema coincide with accepted reflections.

## b004-c01 replicate 3: `b004-v7-af49a9f47b75`

Score 67.17, hidden D 0.840, independently replayed Rwp 3.119%; physical and
recovered. It selects exact COD 1533878 Ba3W2O9, clean COD 2311041 monoclinic
WO3 and COD 9010928 BaCO3 at 71.89/23.00/5.12 wt%, with maximum fraction error
0.76 percentage point. Site accuracies are 90.2/76.9/49.3% for
Ba3W2O9/WO3/BaCO3. The weak carbonate light-atom precision limits the
structural score but does not compromise inventory recovery.

The solve reproduces the intended source and closure discipline. The initial
three-phase model establishes every coherent family, but its first profile
branch reaches laboratory bounds and makes zero/displacement about 99%
correlated, so the solver rolls it back. A systematic WO3 intensity reversal
then triggers equal cell, coordinate, Uiso and texture development of several
exact-composition sources. Clean COD 2311041 wins physically at Rwp 4.26%
versus 5.67% for COD 1528915; two lower-symmetry starts hit coordinate/Uiso
bounds, and a P21/m trial fails numerically and is correctly left unknown
rather than called rejected. Because the winning clean parent removes the
coherent family, the solver stops discrete phase search.

Accepted-model completion is careful but not floor-level. Unsupported
zero/displacement, roughness, width and anisotropic-strain branches are rolled
back; the retained replay-stable checkpoint reaches Rwp 3.2941 with maximum
shift/esd about 3e-6. It nevertheless keeps small WO3 and BaCO3 texture gains
that are absent from the generating realization and a compensating width
decomposition (notably elevated common X and overlarge minor-phase sizes).
These oracle-informed values diagnose the remaining D=0.840 gap but are not
reusable answer parameters.

The exact helper hash `954ecebf...` is invoked once and terminally. Baseline,
all, heavy/light and phasewise branches are all eligible and physical;
heavy/light wins at Rwp 3.118737 after the settle replay, final shift/esd
0.0050, no frozen variables or geometry violations, and stable fractions. The
submitted result Rwp, `final.gpx`, collection and scorer hashes all match this
selected project, followed only by read-only replay and export.

## b004-c01 case conclusion

Scores are 72.83/75.34/67.17, mean 71.78 versus P0 mean 75.92; D values are
0.587/0.506/0.840. Exact physical inventory and recovery are both 3/3, so all
preregistered b004 gates pass, including mean >=70. The -4.14 case difference
is ordinary variance and remains well inside the fixed -15 boundary. This
case validates weak-source retention, physical ordinary-parent comparison,
terminal ordering and helper no-harm. It also argues against a manifest that
blocks closure on every individual failed source: coverage should be enforced
per serious formula/topology family and clean accepted parent, while redundant
numerical failures remain explicitly unknown.

## b001-c06 replicate 1: `b001-v7-29ce7cb39320`

Score 29.45, hidden D 17.681, independently replayed Rwp 7.259%; physical but
unrecovered. It submits the exact MnWO4/WO3/Mn3WO6 formulas at
70.04/14.92/15.04 wt%, versus 68.42/16.12/15.46 wt% truth, but assigns
Mn3WO6 to the wrong C2/c Zn3TeO6-derived framework. MnWO4, Mn3WO6 and WO3 site
accuracies are 86.4/13.0/47.0%. Formula closure and accurate abundance thus
mask a discrete topology failure.

Unlike replicate 3, this solve does enumerate and construct the serious R-3
family. Mn3TeO6-derived COD 2211528 and Cd3TeO6-derived COD 2242674 are the
top topology-screen candidates and are compared with C2/c, Pnma, R3 and cubic
controls. At the first matched structural checkpoint the two R-3 starts are
slightly best at Rwp 33.690/33.713, versus 33.753 for Zn-derived C2/c and
34.341 for Co-derived C2/c. These are matched only within a poor rebuilt
state, not the guidance's best mature common state: every branch is recreated
from raw CIFs with crude fixed size/strain, and the candidate receives one
isotropic source-cell scale before local cell refinement. R-3 remains trapped
near c=10.786 A rather than the residual-indexed c near 10.46 A. All
minor-phase direct-coordinate proposals then make excessive shifts or short
contacts and are rolled back, while the selected R-3 checkpoint carries only
about 5.9 wt% Mn3WO6.

The downstream comparison is not equal. Four R-3 profile starts finish at
Rwp 15.43-15.95 with only 5.9-7.4 wt% Mn3WO6; all six directional-broadening
trials are rejected at supplied bounds. The solver then reopens C2/c and gives
it a new bounded coordinate line-search that is never applied to R-3. After
transferring the same developed MnWO4/WO3 coordinates and settling cells, the
Zn-derived C2/c model falls from Rwp 15.70 to 11.00 with 16.84 wt% Mn3WO6;
small physical line-search steps reach 9.98. A conservative 0.08-A branch is
then developed through additional phase-profile and intensity/texture tests,
reaching Rwp 8.21 before terminal refinement. The lower-symmetry model's much
denser reflection set can absorb the split/intensity residual family, but that
fit advantage is not evidence for the hidden framework when the independently
indexed higher-symmetry route has not received the same downstream adaptation.

The claimed terminal state also remains gross rather than closed: submitted
GOF is 4.098 and Rwp is 7.259. The exact helper hash `954ecebf...` is invoked
once after the claimed terminal checkpoint. All three non-baseline branches
are eligible; heavy/light safely lowers Rwp from 7.5058 to 7.2587 with final
shift/esd 0.315, no frozen variables or physical/fraction violations, and
matching selected project, result, collection and scorer hashes. The helper
does not cause or repair the topology choice.

This replicate therefore passes serious-family construction but fails R-3
selection and recovery. It shows that a construction manifest alone is not a
sufficient intervention. Recovered replicate 2 supplies the direct positive
contrast: it seeds the indexed metric near a=8.895, c=10.463 A in a mature
shared state and screens the two R-3 starts at Rwp 7.140/7.182 before equal
coordinate development. Comparisons must clone one mature common state, seed
the observed metric rather than an isotropic source scaling alone, and retain
equal depth through coordinate/profile/registry stages. A flexible
lower-symmetry basin must not terminate while GOF/residuals remain gross.

## b001-c06 case conclusion

Scores are 29.45/87.45/16.59, mean 44.50 versus the frozen >=58 gate and P0
mean 22.11; D values are 17.681/0.169/172.824. R-3 is constructed in
replicates 1 and 2 but selected and recovered only in replicate 2. Replicate 3
enumerates R-3 without constructing it, while replicate 1 constructs it but
later displaces it with an over-flexible C2/c basin. The preregistered R-3
selection >=2/3, recovery >=2/3 and mean >=58 gates all fail.

The +22.38 case-mean improvement over P0 is scientifically useful but cannot
offset either the failed mechanism gates or v7's fixed regressions elsewhere.
For the next candidate, serious-family coverage should be enforced at
construction and at each later comparison stage; closure should reopen when a
wrong-symmetry alternative wins only after unequal adaptation or still leaves
gross GOF/residuals.

## b002-c02 replicate 1: `b002-v7-f1e86fb5f76f`

Score 26.53 provisionally, hidden D 14.841, independently replayed Rwp
7.594%; unrecovered and requiring physical adjudication. It submits
MnWO4/WO3/Mn2WO5 at 62.56/20.38/17.07 wt%, versus the hidden
MnWO4/WO3/Mn3WO6 inventory at 59.14/20.00/20.86 wt%. Only MnWO4 matches an
exact hidden framework. Site accuracies are 92.4% for MnWO4, 42.4% for WO3
and 19.1% for the wrong Mn2WO5-to-Mn3WO6 correspondence.

The trajectory begins sensibly from MnWO4 plus WO3 and identifies one large
linked residual family. It then fragments that family: a low-angle subset is
indexed by a small tetragonal metric, interpreted as reaction-balanced
Mn2WO5, while other peaks are treated separately as scheelite, MnO or later
olivenite evidence. A composition survey explicitly considers A3WO6 but finds
only four direct W-containing entries, none R-3. A later signed-residual scan
over W-containing ternaries ranks Ba3WO6 among its top ten but is not expanded
to substituted A3BO6 topologies. The next exhaustive topology screen is
hard-coded to eight-atom O5 parents converted to Mn2WO5. Thus the surviving
Cd3TeO6-derived R-3 Mn3WO6 route is neither retrieved nor constructed even
though the solver spends substantial effort on symmetry-diverse P4/nmm,
scheelite, hexagonal-MnO and monoclinic/orthorhombic olivenite controls.

This is not simple lack of search breadth. The solve searches broadly after a
partial indexing has already become formula proof, so all later breadth is
inside the wrong stoichiometry/topology family. A serious candidate should
instead account for the full linked residual family; a convenient subset
metric is an alias to retain, not grounds to discard reaction-balanced
alternatives or substituted-chemistry parents.

The accepted monoclinic olivenite basin remains gross at GOF 3.815 and Rwp
7.594. It also knowingly retains COD 1528915 WO3 with four approximately
1.576-A O--O contacts, arguing that inherited low precision does not
undermine phase assignment. That is still a submitted physical defect and
correctly triggers adjudication. Residual coincidence with accepted-phase
positions does not establish closure at this fit quality.

The exact helper hash `954ecebf...` is invoked once on the claimed terminal
state. Baseline, all, heavy/light and phasewise endpoints are eligible;
heavy/light wins safely at Rwp 7.59412 versus baseline 8.18135, final
shift/esd 0.558, no final frozen variables or helper violations. The result,
submitted project, collection and scorer hashes agree. The helper is not the
cause of the topology, source-physicality or false-terminal decisions.

Across the first two harder-Mn solves, scores are 26.53/20.87, mean 23.70,
with R-3 construction 0/2. Even if replicate 3 constructs the route, the
preregistered >=2/3 construction gate is now impossible. Replicate 3 is the
only remaining opportunity for R-3 selection and recovery and must score at
least 66.59 to reach the mean-score gate of 38.
