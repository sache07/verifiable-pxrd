# v5 design

v4 made the post-inventory restart salient but treated inventory and profile as
a one-way sequence. That failed when c04 judged overlapped Mn3O4 under a
provisional profile and never reconsidered it. The restart itself was also
fragile: c03 released U and SH/L only from lower bounds; c04 and c06 settled in
reduced common-profile basins. Meanwhile c05 skipped the named roughness branch
and replaced a global low-angle effect with a flexible background. v5 replaces
that sequence with a short inventory/profile loop and makes the relevant branch
comparisons explicit. The analogue helper remains byte-identical.

The first prospective request again covers only c03--c06. c01 and c02 remain
held regression cases until this unresolved screen succeeds.

| Case | Required v5 behavior | Prospective success check |
|---|---|---|
| c03 | Preserve SrWO4/monoclinic-WO3/SrCO3; compare zero-only with displacement-only after interior common-profile starts; test smooth background, polarization and roughness; include diagonal as well as axial texture axes; combine complementary WO3 size/strain branches. | Correct physical structures/inventory, no bound-derived profile pruning, and score >80. |
| c04 | Keep plausible Mn3O4 on a watch list and re-challenge it after a physical common restart; repeat the loop if retained, then test each phase's size/strain and anisotropy sequentially. | Complete physical MnWO4/WO3/Mn3O4 inventory and major recovery to score >80. |
| c05 | Preserve helper-driven Ca3WO6 recovery and [110] axis selection while explicitly comparing a smooth background, polarization and sample roughness before texture. | Correct physical inventory, no flexible-background surrogate, and score >80. |
| c06 | Preserve alternate-record recovery of massicot PbO; use interior common starts and test anisotropic phase strain when isotropic branches leave hkl-dependent widths. | Complete physical four-phase inventory and score >80. |
| c02 (held) | Preserve v3's noise-floor three-phase result under the shorter iterative wording. | Score >80 after unresolved cases pass. |
| c01 (held) | Leave the simple control low-dimensional and avoid nuisance overfitting. | Score >80 after unresolved cases pass. |

Any inventory or physical regression rejects v5. A candidate re-challenged only
under the original provisional profile, a common term declared absent after a
lower-bound start, an untested diagonal texture family, or an anisotropic term
retained without fresh replay does not count as the intended mechanism. If the
four unresolved cases pass, the remaining six development solves are reserved
for c01/c02 validation and the strongest permissible final comparison.

Frozen as v5 before rollout: 415 guidance words; guidance SHA-256
`83b85bdd57f98d5663b7f52ea5a5e5ea49a3d0ca7a81e1dfcf588e06ebbf1dee`;
helper SHA-256
`0d58e24b4c66dfc7d43567767635c32522c40d000b584912343304844794e5b8`;
prompt SHA-256
`272e3d6d8bc5c8e5900f23a868d94031b763bd0845c2e48395f2168753d7921e`.

## Results as completed

| Case | Score / profile | Behavioral result | Decision |
|---|---|---|---|
| c03 | 51.09; D 1.744; Rwp 4.760% versus 2.851% floor; physical pass | The solver preserved SrWO4/monoclinic-WO3/SrCO3 and followed the matched angular and shared-intensity branches: two interior common starts, displacement-only versus zero-only, smooth 8-term background, polarization, and roughness rejection. However, its texture script hard-coded only SrWO4 [001]/[110], WO3 [010]/[101], and SrCO3 [001]/[110]. It therefore omitted the generating diagonal SrWO4 [111] and axial WO3 [001] directions despite the prospective requirement, then retained wrong [110]/[101] terms. Common X inflated to 4.77 with U=0; all phase sizes and WO3 anisotropy were missed. The direct SrMoO4-derived prototype also reduced structural score to 73.06. | Initial-screen failure and regression below v3/v4. The angular/global-intensity mechanisms pass, but complete texture-axis and broadening mechanisms fail by nonadherence. Continue auditing c04--c06 before choosing how to spend the six-solve reserve. |
| c04 | 85.36; D 0.115; Rwp 2.613% versus 2.487% floor; physical pass | The reversible inventory/profile loop worked as intended. After interior common-profile starts, the solver re-challenged Mn3O4 under the clean profile, retained it, restarted after changing the MnWO4 parent and WO3 source, and rechecked the full watch list. It recovered MnWO4/WO3/Mn3O4 at 74.95/18.94/6.11 wt% versus 74.67/19.06/6.27 truth. Common U/W/SH-L and polarization closely match truth, and the final profile is near the noise floor. The structural caveat is material: it selected triclinic instead of generating monoclinic WO3, giving the WO3 model only 13.56 site accuracy and aggregate structural score 78.90. Correct WO3 size was paired with spurious 4175 ppm strain, while Mn3O4 size was missed and its strain inflated to 8586 ppm, so the wrong polymorph/microstructure combination is compensating despite a physical project and explicit caveat in the report. | Prospective headline, inventory, fraction, and physical criteria pass; this is the first strong causal success of the bidirectional loop. Credit profile/inventory recovery, but not unique structural or broadening recovery. Preserve a concise post-profile candidate re-challenge; do not infer that exhaustive branch enumeration is generally successful from this one case. |
| c05 | 43.80; D 5.266; Rwp 5.621% versus 2.234% floor; physical pass | The solver preserved CaWO4/monoclinic-WO3/Ca3WO6, used the analogue helper, recovered close fractions, and selected the correct CaWO4 [110] texture direction; structural score was 85.57. It also ran three interior common starts and the requested shared-intensity comparisons. All starts nevertheless converged to the same high-X/high-SH/L basin (U=30.92, W=21.73, X=11.17, SH/L=0.049). The nominally smooth 8-term background had large alternating coefficients and, with polarization=0.849 and an oversized CaWO4 size, absorbed the true low-angle/roughness and phase-broadening signals. Roughness became bound-correlated and was rejected; downstream width tests kept this poisoned common baseline fixed, leaving all phase strains and both minor-phase sizes absent. | Inventory/helper/texture mechanisms pass, but the common-profile/shared-intensity mechanism fails and the score regresses below v1--v4. Interiority alone is not an adequacy test: a successor needs a physical background-shape/low-angle checkpoint and a common-profile restart when all phase-width branches collapse, rather than more branch enumeration. |
| c06 | 74.72; D 0.449; Rwp 3.025% versus 2.509% floor; physical pass | The solver retained exact physical PbWO4/monoclinic-WO3/Pb3O4/massicot-PbO records and recovered fractions 57.74/20.44/16.86/4.96 wt% versus 55.34/22.56/16.68/5.43 truth. Massicot emerged only when the watched phase was replayed after a clean profile, lowering provisional Rwp 4.60% to 3.44%; source/polymorph re-challenges then preserved it. Profile allocation remained wrong: final U/W/X/SH-L were 14.89/9.17/4.43/0.0142 versus 27.38/7.31/2.68/0.00884 truth. A false roughness correction and false Pb3O4 [110] texture replaced the true high polarization and some broadening. PbWO4 size and WO3 strain were close, but WO3 size was omitted; Pb3O4 and PbO anisotropic strains were never tested, with isotropic size or strain surrogates retained instead. | Inventory/source/reversible-loop behavior passes and improves v1/v4, but the >80 target and anisotropic/global-intensity mechanisms fail. No anisotropic implementation appears in the artifact despite strong family-dependent widths. Preserve alternate-record/watch-list persistence, but replace exhaustive nuisance branching with direct physical-adequacy and residual-family checks. |

## Aggregate decision

v5 scores 51.09, 85.36, 43.80, and 74.72 on c03--c06 (mean 63.74),
the best package mean yet on this four-case subset and with every inventory
complete and physical. Only c04 passes the prospective >80 criterion, however;
c03/c05 regress severely and c06 remains below target. The package is rejected
as a final condition. Its transferable advance is the concise reversible
watch-list/source re-challenge after a clean profile; its exhaustive branch
enumeration is not transferable and will be replaced rather than extended.
