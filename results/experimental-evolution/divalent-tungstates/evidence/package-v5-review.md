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
