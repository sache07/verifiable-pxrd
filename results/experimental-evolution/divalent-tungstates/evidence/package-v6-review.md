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

Only six development solves remain, so the prospective request covers all six
cases once. This is the strongest possible complete package comparison inside
the fixed 30-solve budget, but it cannot supply the requested two additional
replicates; that limitation will be carried into the promotion decision.

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
beats baseline, explicitly marking the missing replication evidence.
