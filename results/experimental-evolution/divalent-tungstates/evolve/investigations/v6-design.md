# v6 design and budget-limited final screen

The five package screens isolate one robust inventory intervention and one
repeated profile failure. v1 made every inventory complete, v3 reached the
noise floor on c02 and improved c03/c05, and v5's clean-profile watch-list
replay recovered Mn3O4 in c04 and massicot in c06. In contrast, adding more
enumerated branches never made an interior profile physically adequate:
c03/c05 retained common-width or shared-intensity surrogates, while c06 never
tested its generating anisotropy. v6 therefore replaces v5 rather than adding
to it. It retains reversible inventory decisions and the byte-identical
analogue helper, but makes direct peak/background residuals the acceptance
test and uses a restart trigger when every phase-width branch collapses.

Only six counted development solves remain, so the first prospective request
covers all six cases once. When those fill the 30-solve budget, the controller
allows one package used in this cycle to be completed to three solves per case
with uncounted `evaluation` repeats. After the initial screen, complete either
v6 or the stronger complete v1 condition to three rollouts, based on the
predeclared physical/inventory checks and aggregate evidence.

| Case | Required v6 behavior | Prospective success check |
|---|---|---|
| c01 | Preserve the simple control, neutralize unused HAP defaults, and stop expanding once direct peak checks and replay are at the noise floor. | Physical one-phase model and score >80 without nuisance overfit. |
| c02 | Preserve the complete ZnWO4/WO3/ZnO inventory and v3's adequate common-profile-before-phase-width sequence. | Complete physical inventory and score >80. |
| c03 | Preserve SrWO4/monoclinic-WO3/SrCO3, compare structures under one adequate baseline, and use residual families rather than default texture/common-X surrogates. | Correct physical inventory/structures and score >80. |
| c04 | Re-challenge watched Mn3O4 after the clean profile and restart after any retained source change, while avoiding a wrong-polymorph/strain compensation. | Complete physical inventory and score >80. |
| c05 | Invoke the helper, retain Ca3WO6, distinguish roughness/background/polarization before texture, and preserve the supported CaWO4 [110] family only if replay-stable. | Complete physical inventory and score >80. |
| c06 | Retain massicot through alternate-record/watch-list persistence and use family-dependent widths to trigger anisotropy rather than false roughness/texture. | Complete physical four-phase inventory and score >80. |

Any missing phase, physical failure, or non-replayable project rejects the
condition. At budget exhaustion, compare the complete v6 screen with P0 and
the complete v1 screen; promote the strongest complete physical package that
beats baseline after completing its three-rollout evaluation.

Frozen prospectively as v6 before rollout by accepted request
`freeze-v6-r1`: 331 guidance words; guidance SHA-256
`ed1dffd19e70e2fa6aed61b8dff05a43ad3940966d4218396a072c297d885b05`;
helper SHA-256
`0d58e24b4c66dfc7d43567767635c32522c40d000b584912343304844794e5b8`;
prompt SHA-256
`06abcffca01d2785a0020887c9fa78db1d851de2bfd9e4c35d5c8f36dfb1b7e6`.
The earlier `freeze-v6` request failed before state change because inline text
was supplied where the interface requires a notes-file path.

Before rollout, the local interface documentation corrected an operational
mistake in the frozen review note: evaluation replicates for one package become
uncounted after the 30 development solves are spent. The package bytes and
scientific predictions above are unchanged; no v6 outcome was known when this
correction was recorded.

## Initial-screen results as completed

| Case | Score / profile | Behavioral result | Decision |
|---|---|---|---|
| c01 | 95.68; D 0.0630; Rwp 2.350% versus 2.273% floor; physical pass | The solver retained only scheelite CaWO4 with structural score 98.10. Direct observed/calculated FWHM checks at isolated low-, middle-, and high-angle peaks exposed an initial zero-U local minimum; an interior restart recovered U/W and the final U/W values closely match truth. CaO, Ca3WO6, and three WO3 records were rejected by multi-family evidence. Phase size/strain, roughness, every tested texture axis, and atomic refinements were rejected; the submitted model kept a smooth six-term background, one tiny zero correction, polarization, and U/W/X. | Full prospective pass. v6 preserved the simple control near the noise floor without retaining nuisance overfit; continue the all-six screen. |
| c02 | 80.91; D 0.2108; Rwp 3.042% versus 2.791% floor; physical pass | The solver recovered the complete ZnWO4/ZnO/monoclinic-WO3 inventory at 72.66/8.58/18.75 wt%, with maximum fraction error 1.97 percentage points and structural score 78.39. It selected the generating ambient monoclinic WO3 record against a second monoclinic, triclinic, orthorhombic, and tetragonal set under a common model. Direct profile checks rejected negative U, pruned correlated SH/L/polarization, retained a smooth six-term background and modest roughness, and supported only ZnWO4 isotropic size plus WO3 [011] microstrain. All symmetry-distinct texture trials were near unity and pruned; weak fourth-phase challenges were rejected. | Full prospective pass. Inventory, source selection, direct profile adequacy, sequential broadening, and nuisance pruning all behaved as specified; the score clears 80 with exact framework inventory and replay. |
| c05 | 60.30; D 1.2739; Rwp 3.348% versus 2.234% floor; physical pass | The solver invoked the analogue helper and recovered physical CaWO4/monoclinic-WO3/Ca3WO6 at 78.63/11.44/9.93 wt%, within 1.71 percentage points of truth and with structural score 84.77. It selected the generating WO3 source, retained the supported CaWO4 [110] texture and near-true CaWO4 size, and pruned weak fourth phases. The direct-profile requirement was not executed deeply enough: final U=77.5, polarization=0.872, and zero=-0.204 degrees absorb omitted specimen displacement, roughness/asymmetry, and phase strain/anisotropy; the smooth six-term polynomial also substitutes partly for the true low-angle background. Only isotropic size was retained for CaWO4/Ca3WO6, while all strain was discarded without an anisotropic challenge. | Inventory/helper/source/texture behavior passes and the profile improves greatly over v5, but the >80 target and physical-baseline mechanism fail. This remains an oracle-informed allocation diagnosis, not a case-specific recovery rule. |
| c04 | 93.42; D 0.0667; Rwp 2.547% versus 2.487% floor; physical pass | The solver used the helper to build physical wolframite MnWO4, selected the generating monoclinic-WO3 family, and recovered watched hausmannite Mn3O4 only after the clean two-phase profile. Rebuilding after that inventory change gave 75.02/18.72/6.26 wt%, all within 0.35 percentage point, and structural score 92.92. Direct low/mid/high-angle checks retained near-generating U/W/SH-L/polarization, WO3 and Mn3O4 size, and a smooth eight-term background; roughness, texture, extra phases, and correlated strain were pruned. The final Mn3O4 size substitutes partly for generating size-plus-anisotropic-strain, but does not impair the near-floor replay or quantitation. | Full prospective pass. The reversible inventory loop, direct baseline, source selection, and post-inventory phase-width sequence all work, improving v5 by eight points while correcting its WO3 polymorph and structural deficit. |
| c06 | 79.08; D 0.3041; Rwp 2.844% versus 2.509% floor; physical pass | The solver recovered exact-source PbWO4/monoclinic-WO3/Pb3O4/massicot at 57.95/20.19/16.95/4.91 wt%, with full framework inventory, maximum fraction error 2.61 points, and structural score 82.68. Massicot was added from a coherent residual family and all sources were re-challenged; weak polymorph/prototype/oxide additions were pruned. PbWO4 and Pb3O4 sizes plus isotropic Pb3O4/PbO/WO3 strains were retained, with no texture or roughness. The common profile used W/SH-L/zero only and never challenged symmetry-appropriate anisotropy, so strong generating Pb3O4/PbO anisotropic strains remain represented by isotropic surrogates. | Inventory/source/replay behavior passes and this is the best c06 package result, but it narrowly misses >80 and does not execute the anisotropy branch. Credit substantial profile progress over v5, not full broadening recovery. |
| c03 | 83.76; D 0.1421; Rwp 3.039% versus 2.851% floor; physical pass | The solver invoked the analogue helper and selected a CaWO4-derived scheelite SrWO4 parent, the generating monoclinic WO3 record, and exact SrCO3. The complete 60.51/24.19/15.30 wt% inventory is within 1.46 percentage points of truth; structural score is 78.08. It explicitly discovered and neutralized the hidden fixed 1000-ppm strain state, selected the true SrWO4 [111] and SrCO3 [001] texture axes, and recovered the generating WO3 unique-b anisotropic strain after a texture-coupled recheck. A fitted roughness B, elevated common X, omitted phase sizes, and WO3 [10-1] rather than generating [001] texture remain nuisance substitutions, but the source/profile comparison and full replay are stable. | Full prospective score/inventory/structure pass and a 20-point gain over v1. Direct baseline, helper, diagonal texture, and anisotropy mechanisms execute; oracle audit prevents claiming unique recovery of every nuisance term. |

## Initial-screen decision

The complete v6 screen scores 95.68, 80.91, 83.76, 93.42, 60.30, and
79.08 on c01--c06, for a mean of 82.19. Every project is physical and has
the full framework inventory. Four cases exceed 80; c06 misses by 0.92 and
c05 remains the only material profile-allocation failure. Relative to the
complete physical v1 screen (mean 64.56), v6 improves five cases and the mean
by 17.63 points; only the simple c01 control decreases slightly (98.02 to
95.68). It also exceeds the P0 mean by 32.15 points. Under the predeclared
rule, v6 is therefore the strongest complete physical package and is selected
for two uncounted evaluation repeats per case to complete three rollouts.

Evaluation request `b001-v6-eval-r23` was submitted once with purpose
`evaluation`, v6, all six b001 cases, and two repeats. The durable request must
not be duplicated while controller acknowledgement or solver results are slow.
The controller acknowledged all twelve child jobs at 02:24:19 UTC with no
infrastructure flags.

## Evaluation results as completed

| Case / replicate | Score / profile | Audit | Result |
|---|---|---|---|
| c01 eval r1 (`84143dc22302`) | 99.03; D 0.0147; Rwp 2.2785% versus 2.2809% floor; physical pass | Exact single-phase scheelite CaWO4 at 100%. A direct low/mid/high-angle width audit led to a nonnegative U/W/X profile; size, strain, roughness, displacement and five texture axes were rejected. CaO, Ca3WO6 and multiple WO3 sources failed coherent-family/BIC checks. Eight-term background, tiny zero, polarization and SH/L replay at the Poisson floor; structural score 99.76. | Full evaluation pass. |
| c01 eval r2 (`12b6ecbd6bae`) | 97.69; D 0.0315; Rwp 2.3133% versus 2.2809% floor; physical pass | Exact single-phase scheelite CaWO4 at 100%. Polarization corrected the angle-dependent intensity trend; nonnegative U/W/X was retained while roughness, texture, size/strain and extra asymmetry were pruned. CaO remained only a rejected ~0.16(7) wt% watch-list trial with incoherent unique lines; Ca3WO6, fergusonite and WO3 alternatives were rejected. Structural score 98.82. | Full evaluation pass. |
| c02 eval r1 (`c1b62714e52b`) | 78.94; D 0.2513; Rwp 3.0941% versus 2.7906% floor; physical pass | Complete exact-source wolframite-ZnWO4/monoclinic-WO3/wurtzite-ZnO inventory at 73.05/18.27/8.69 wt%; maximum fraction error 2.46 points and structural score 77.49. The solver compared WO3 sources under one profile and retained the generating ambient monoclinic record. A coherent angle-dependent residual supported polarization; all three isotropic sizes and WO3 isotropic strain were retained, while negative U/strain, X and texture were pruned. W-only common width, SH/L and polarization leave a modest profile gap. | Inventory/source/physical pass; score misses 80 by 1.06. This is small profile and structural variance from the development solve, not a chemistry regression. |
| c02 eval r2 (`31384050e7dc`) | 85.25; D 0.1085; Rwp 2.9080% versus 2.7906% floor; physical pass | Complete exact-source wolframite-ZnWO4/monoclinic-WO3/wurtzite-ZnO inventory at 72.80/18.51/8.69 wt%; maximum fraction error 2.21 points and structural score 77.80. Equal-model source challenges retained the generating ambient monoclinic WO3 record. The solver rejected a bound U/W/X model, retained a simple positive-W baseline with interior polarization and small zero, and supported all three isotropic sizes plus WO3 strain; texture, roughness, extra phases, and unstable WO3 oxygen refinement were pruned. | Full inventory/source/profile/physical pass and score target pass. |
| c05 eval r2 (`7bc8c7bbdf70`) | 70.58; D 0.6495; Rwp 2.8479% versus 2.2339% floor; physical pass | Complete CaWO4/monoclinic-WO3/Ca3WO6 at 78.29/11.56/10.15 wt%, max fraction error 1.37 points and structural score 85.51. The solver executed the helper for Ca3WO6/Ca2WO5/CaWO3, selected the top Ca3OsO6 P21/n analogue, and retained the generating WO3 source. True CaWO4 [110] texture and weak size anisotropy were recovered. An eight-term background improves the development profile, but U=76.6, polarization=0.873 and zero=-0.204 degrees reproduce its angular/intensity surrogate; roughness and all strain remain omitted. | Strong inventory/helper/source/quantitation replication and improved profile, but target/direct-baseline mechanism still fails. |
| c04 eval r1 (`95bb77123895`) | 52.62; D 2.4739; Rwp 4.6474% versus 2.4868% floor; physical pass | Complete helper-derived MnWO4/generating monoclinic-WO3/tetragonal-Mn3O4 at 75.83/17.48/6.68 wt%, max fraction error 1.57 points and structural score 88.38. The solver recovered watched Mn3O4 from coherent families and rebuilt the three-phase model. However, the final common profile collapsed to U=W=0, X=5.62, SH/L=0.088 and zero=-0.424 degrees; WO3/Mn3O4 isotropic strains substitute for omitted phase sizes/anisotropy. Direct checks did not force another interior restart. | Inventory/helper/source/reversible-loop pass, severe profile-target fail. This is rollout variance in baseline execution, not weak-phase loss. |
| c05 eval r1 (`e35e7dd15c45`) | 26.24; D 18.5149; Rwp 9.0261% versus 2.2339% floor; physical pass | Submitted only CaWO4/monoclinic-WO3 at 86.38/13.62 wt%, omitting true 10.69 wt% Ca3WO6; full-framework inventory false and structural score 57.92. The helper was invoked for exact CaWO4, WO3 and CaO records, but the solver never inferred Ca3WO6 from residual families and never ran the relevant stoichiometric-analogue query. The accepted U=W=0, X=9.29, zero=-0.201 degree profile plus CaWO4 size/strain/texture is grossly inadequate despite a claim of no remaining FWHM trend. | Inventory/helper-targeting and direct-baseline fail. This is the first v6 rollout to lose a true framework phase. |
| c06 eval r1 (`5023b59dade4`) | 63.81; D 0.7616; Rwp 3.3207% versus 2.5090% floor; physical pass | Exact-source PbWO4/monoclinic-WO3/Pb3O4/massicot at 58.86/19.59/17.24/4.31 wt%, maximum fraction error 3.53 points and structural score 74.37. Massicot and Pb3O4 were added from coherent residual families; litharge and other source/polymorph challenges were rejected. The model retains sizes for all phases and Pb3O4 [001] size anisotropy, but fixes a narrow U/W baseline, drives polarization to 0.997, and rejects all strain; the strong generating Pb-oxide anisotropic strains remain unrecovered. | Full inventory/source/watch-list/physical pass; profile and quantitation regress from development and the target fails. |
| c03 eval r1 (`08d2259f87f1`) | 67.58; D 0.6054; Rwp 3.6375% versus 2.8506% floor; physical pass | Complete helper-derived SrWO4/generating monoclinic-WO3/SrCO3 at 61.71/22.97/15.32 wt%, maximum fraction error 2.65 points and structural score 75.51. The helper compared SrWO4 parents and selected the CaWO4-derived model. SrCO3 was recovered after a reversible expanded-cell seed. The final model uses SrWO4 [110] and WO3 [10-1] textures plus WO3 [010] size anisotropy rather than the generating SrWO4 [111], WO3 [001], and unique-b strain; U is zero, X is elevated, and roughness/phase sizes are omitted. | Inventory/helper/source/physical pass; profile/texture/broadening target fails and regresses from development. |
| c03 eval r2 (`65e05ffcf72e`) | 69.26; D 0.5429; Rwp 3.5513% versus 2.8506% floor; physical pass | Complete helper-derived SrWO4/generating monoclinic-WO3/SrCO3 at 58.96/25.01/16.03 wt%, with every fraction within 0.104 point and structural score 75.93. The helper was explicitly run for multiple Sr--W--O stoichiometries; a SrMoO4-derived scheelite parent was selected, while equal-model WO3 challenges retained the generating source. True SrWO4 [111] and SrCO3 [001] texture were recovered, but wrong WO3 [10-1] texture plus isotropic strain, W=39.9/X=4.04, and a large displacement surrogate leave a profile gap. | Inventory/helper/WO3-source/quantitation/physical pass; profile and analogue-site target fail. |
| c06 eval r2 (`4db1bb4a244b`) | 89.54; D 0.0967; Rwp 2.6101% versus 2.5090% floor; physical pass | Exact-source PbWO4/monoclinic-WO3/Pb3O4/massicot at 55.23/22.66/16.48/5.63 wt%, every fraction within 0.20 point and structural score 87.07. The solver rejected bound polarization, added physical WO3/PbO displacement terms, then recovered interior polarization 0.835 and positive U/W/X. PbWO4 size, Pb3O4 size+strain, and PbO strain survived; texture, raspite and litharge were pruned. | Full inventory/source/profile/quantitation pass. This is the first c06 rollout above 80 and reaches near-floor replay without false texture. |
| c04 eval r2 (`c58bdcc24147`) | 39.56; D 9.2093; Rwp 7.7118% versus 2.4868% floor; physical pass | Complete helper-derived MnWO4/generating monoclinic-WO3/tetragonal-Mn3O4 at 74.83/19.67/5.50 wt%, every fraction within 0.77 point and structural score 84.20. The helper compared wolframite parents, the watch-list loop retained Mn3O4 from several families, and equal-model source trials retained the generating WO3 record. However, U collapsed to zero while W=10.93, X=7.00, polarization=0.913 and a 787-micrometre displacement absorbed the profile; only WO3 isotropic size survived, with all MnWO4/Mn3O4 size, strain, anisotropy and texture pruned. | Inventory/helper/source/watch-list/quantitation pass; severe direct-profile and broadening failure. |

Together with the development result (95.68), c01 has a three-rollout mean of
97.47 and range 95.68--99.03. Inventory and physical validity pass in all
three; the two evaluation solvers independently reach the Poisson floor with
slightly different but replay-stable nuisance allocations.

For c02, the development and two evaluation scores are 80.91, 78.94 and
85.25: mean 81.70, population SD 2.63, and range 78.94--85.25. All three
recover the exact three-phase inventory, select the generating WO3 source,
and pass physical replay. Two clear 80 and the third misses by only 1.06;
this is the most stable mixed-phase v6 case.

For c03, scores are 83.76, 67.58 and 69.26: mean 73.53, population SD
7.27, and range 67.58--83.76. All three invoke the analogue helper, recover
the full inventory and pass physical replay. The two fresh solves miss the
profile target despite one attaining nearly exact fractions; diagonal texture
and anisotropic-broadening execution is therefore not robust.

For c04, scores are 93.42, 52.62 and 39.56: mean 61.87, population SD
22.94, and range 39.56--93.42. All three invoke the helper, recover the full
inventory and pass physical replay, but only the development solve executes a
near-floor profile. The watch-list chemistry loop is robust; the common-profile
restart and phase-broadening sequence are not.

For c05, the development and two evaluation scores are 60.30, 26.24 and
70.58: mean 52.37, population SD 18.95, and range 26.24--70.58. All three
projects are physical, but only development and evaluation r2 recover the
full inventory. Thus the helper-capable chemistry mechanism succeeds 2/3,
while profile adequacy fails 3/3 and is highly variable.

For c06, scores are 79.08, 63.81 and 89.54: mean 77.47, population SD
10.56, and range 63.81--89.54. All three recover the exact four-phase
inventory and pass physical replay; evaluation r2 is the first full profile
pass, while the other two omit the generating anisotropic-strain detail.

## Evaluation decision

Across all 18 v6 rollouts, the mean is 74.07, population SD 19.56, and range
26.24--99.03. All 18 projects pass physical replay and 17/18 recover the full
framework inventory, but only 8/18 score above 80. Case means are 97.47,
81.70, 73.53, 61.87, 52.37 and 77.47 for c01--c06; only c01 and c02 exceed
80. Thus v6 does not pass the predeclared strong evaluation condition: one c05
rollout loses Ca3WO6, most runs do not reach the noise floor, and c03--c06
remain unresolved.

The development budget is exhausted, however, and the governing fallback is
to promote the evaluated package if it beats baseline. v6's 74.07 aggregate
exceeds P0's same-panel 18-run mean of 50.04 by 24.03 points, exceeds the
one-rollout complete v1 screen mean of 64.56 by 9.51, and every v6 case mean
exceeds its P0 case mean. It is therefore selected as the budget-exhausted
incumbent, explicitly not as a success-condition pass. Carry c03--c06 into the
next cycle; c01 and c02 are the validated successes.
