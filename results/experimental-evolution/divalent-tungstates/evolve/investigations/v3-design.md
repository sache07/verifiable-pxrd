# v3 design and prospective screen

v3 restores v1's successful source, inventory, HAP-neutralization, and analogue
behavior. It removes v2's failed mandate to fix the common profile to a sharp
lower envelope. The replacement is an ordered adequacy test: common U/W/X and
conditional SH/L must describe resolved sharp peaks across angle before phase
widths; global angle-dependent intensity effects are tested before texture;
texture axes are compared rather than assumed. No diagnostic executable or
fitted value is shipped. The generic analogue helper is byte-identical to v1.

The first screen again uses one fresh solve on unresolved c02--c06, holding c01
until those cases improve. Predeclared behavioral predictions:

| Case | Required v3 behavior | Success check |
|---|---|---|
| c02 | Preserve all three physical phases; establish common angular widths before Zn/WO3 phase terms; test coherent global low-angle intensity behavior and WO3-specific strain without bound surrogates. | Correct physical inventory and score >80. |
| c03 | Compare WO3 polymorphs only after each has an adequate common profile; retain the physical monoclinic model; compare texture-free and symmetry-distinct axes on diagnostic families. | Correct physical structures/inventory and score >80. |
| c04 | Fit common U/W/X and reproducible low-angle asymmetry before minority phase widths; revisit the common model when size/strain branches hit bounds. | Major recovery toward the demonstrated D=0.082 ceiling and score >80. |
| c05 | Invoke the analogue helper and retain Ca3WO6; test global low-angle intensity effects before comparing dominant-phase texture axes; preserve sequential width allocation. | Correct inventory, physical replay, score >80. |
| c06 | Preserve four physical phases; verify common width trend across angle before selective Pb-phase size/anisotropic strain. | PbO retained, physical replay, score >80. |

Any inventory/physical regression rejects v3. Bound-seeking nuisance terms,
stored-fit-only gains, or adoption without scientific improvement do not pass.

## Results as completed

| Case | Score / profile | Behavioral result | Decision |
|---|---|---|---|
| c02 | 88.76; D 0.0965; Rwp 2.905% versus 2.791% floor; physical pass | Correct ZnWO4/ZnO/monoclinic-WO3 inventory and near-true fractions. The solver compared physical WO3 polymorphs under one preliminary schedule, established nonnegative common U/W/X before phase terms, rejected bound/correlated roughness and SH/L branches, then retained only ZnWO4 size and WO3 strain after ablations. No texture or frozen variable survived fresh replay. | Full predeclared pass and first noise-floor-level unresolved result. The key gain is ordered common-profile adequacy plus supported phase terms, not indiscriminate roughness adoption. |
| c06 | 36.73; D 6.963; Rwp 6.732%; physical pass | Submitted only PbWO4/WO3/Pb3O4, omitting true PbO and inflating PbWO4. The solver tried one P4/nmm PbO record (COD 9012700), obtained zero scale, and did not test a physically screened massicot alternate despite the retained candidate rule. Its common W/X/SH-L branch also omitted U and supported anisotropic strain, retained a large +0.453 degree zero, and remained far from adequate. | Inventory regression rejects v3 unchanged. This is a source-alternate/nonadherence failure plus profile failure, not evidence against the c02 mechanism. Determine after the screen whether shortening restores attention or whether c06 needs a replication under the same package. |
| c05 | 72.51; D 0.549; Rwp 2.747% versus 2.234% floor; physical pass | The helper retained Ca3WO6 and fractions remained close. The solver established stable surface roughness before texture, compared axes, independently selected CaWO4 [110] with ratio 1.252, recovered CaWO4 size 0.0790 micrometre, and retained a diagnostic Ca3WO6 strain branch. Structural score was 84.43. Common U was high, X was pruned, and one shift plus the selected phase terms left residual width/angular allocation error. | Behavioral mechanism passes strongly and score rises 20 points over v2, but the >80 target fails. Preserve the ordering/axis rule; diagnose the remaining coupled common-versus-phase and angular allocation after the screen. |
| c03 | 71.33; D 0.505; Rwp 3.535% versus 2.851% floor; physical pass | Correct SrWO4/monoclinic-WO3/SrCO3 inventory and near-true fractions. Under the same final nuisance model, monoclinic WO3 beat a fully converged triclinic branch (3.535% versus 3.571% Rwp), repairing v2's polymorph confounding. The solver established common U/W/X before phase terms and compared texture families, but retained SrWO4 [110] and WO3 [2,0,-2] axes rather than the generating families; common X rose to 4.19 while no phase-size term survived. SrCO3 [001] texture and WO3 isotropic strain were well recovered. | Inventory, source/polymorph, and ordered-profile mechanisms pass; score improves over v1/v2 but misses >80. Remaining error is localized to texture-axis and common-X-versus-phase-size allocation, with secondary structural-site precision. |
| c04 | 28.54; D 16.259; Rwp 10.081% versus 2.490% floor; physical pass | Correct MnWO4/monoclinic-WO3/Mn3O4 inventory, with 73.46/21.50/5.04 wt% versus 74.67/19.06/6.27 truth. The solver pruned U at a bound and accepted W/X as adequate, tested only MnWO4 and WO3 broadening, then added Mn3O4 afterward without restarting the profile sequence. Final U=0, SH/L=0.002, no Mn3O4 size/strain, and spurious roughness/weak texture left gross asymmetry and width error despite clean replay. Structural score was 62.65 because the FeWO4-derived coordinates were also imprecise. | Severe predeclared failure and regression below v1/v2. v3's wording allowed preliminary inventory fitting and final profile allocation to interleave; after any inventory change the common/phase profile sequence must explicitly restart for every retained phase. |

Across c02--c06, v3 averages 59.57, versus 57.87 for v1 and 46.41 for
v2 on the same cases. The small aggregate gain masks two severe failures, so
v3 is rejected unchanged and c01 remains held.

## Post-screen diagnostic

Predeclared test `ptest-full-inventory-restart-v3-01`: starting only from the
completed v3 c04 project, neutralize retained roughness/texture, restart common
U/W/X/SH-L from generic interior seeds, and jointly challenge isotropic size
and strain for every now-retained phase. The test contains no phase identity or
truth. If omission of the post-inventory restart is causal, a multi-start
physical replay should materially reduce D and activate phase-specific
broadening that the rollout never tested. Failure would imply that guidance
alone is unlikely to escape the allocation basin and a carefully scoped
execution substrate is needed. This is an oracle-scored diagnostic, not rollout
validation or a candidate helper.

The final scored endpoint (`ptest-common-restart-v3-c04-05`) retained the v3
inventory/structures but neutralized HAP, roughness, and texture before fitting
common U/W/X/SH-L from an interior asymmetry start. It remained physical and
improved D 16.259 -> 8.877 and Rwp 10.081% -> 7.898%, recovering U=25.70 and
SH/L=0.101 instead of v3's U=0 and SH/L=0.002. With all phase widths neutral,
fractions shifted to 79.88/15.71/4.41 wt%, so the restart is causal but
insufficient: supported phase terms must follow. Earlier exploratory branches
showed 7.47% Rwp for an all-size/high-SH-L start, while simultaneous all-phase
size+strain release was numerically ill-conditioned. This supports the v4
sequence (restart, then one phase at a time) and rejects a brute-force helper.
