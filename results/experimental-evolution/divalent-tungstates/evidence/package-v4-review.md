# v4 design

v3 proved that ordered common-profile fitting, global-intensity checks, and
texture-axis comparison can reach the noise floor (c02) and strongly improve
c03/c05. It failed reliably as a package because it did not distinguish the
provisional profile needed for inventory decisions from the final profile pass:
c04 finalized widths before adding Mn3O4, while c06 treated one unsuitable PbO
record as decisive. v4 makes those two transitions explicit and removes detail
that competes with them. The analogue helper remains byte-identical.

Prospective predictions for one fresh unresolved-case screen:

| Case | Required v4 behavior | Success check |
|---|---|---|
| c02 | Preserve v3's physical three-phase result and restart the final profile only after inventory stability. | Correct physical inventory and score >80. |
| c03 | Preserve monoclinic WO3 under a common nuisance comparison; challenge phase widths for all three retained phases before texture. | Correct structures/inventory and score >80. |
| c04 | Complete MnWO4/WO3/Mn3O4 inventory before the clean profile pass; test Mn3O4 and WO3 size/strain and early repeated asymmetry. | Correct physical inventory and major recovery toward score >80. |
| c05 | Invoke the unchanged analogue helper; retain Ca3WO6; preserve global-intensity-before-axis comparison while restarting widths after inventory completion. | Correct physical inventory and score >80. |
| c06 | Treat zero scale from one PbO record as record-specific; screen a second physical alternate and retain all four phases before final profiling. | PbO retained, physical replay, score >80. |

Any inventory or physical regression rejects v4. A stored-fit-only gain,
bound-seeking branch, or failure to restart after an inventory change does not
count as the intended mechanism.
