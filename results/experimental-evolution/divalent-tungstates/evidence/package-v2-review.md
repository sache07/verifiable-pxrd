# v2 design and prospective screen

v1 solved the reusable chemistry problem: all six inventories were correct, all
sources/projects passed physical replay, and mean score rose 50.04->64.56. Its
analogue helper recovered the withheld minor framework prospectively. Preserve
all candidate, inventory, and helper behavior.

The remaining cross-case defect is common-versus-phase profile allocation. The
dual-angular probe had negligible effect and >0.998 covariance. Exhaustive
anchor enumeration improved c05/c06 but timed out on c02 and produced a c04
stored-fit/replay contradiction, so it is excluded. The c04 oracle ceiling was
causal: retaining v1 structures while fixing only generating widths reduced D
8.892->0.082. v2 therefore changes prose only: define the common profile from
empirically sharp resolved peaks, test phase size/strain in separate sequential
branches, prune bound/correlated terms, and require fresh atomic replay after
each accepted profile change.

The first v2 screen uses one fresh development solve on unresolved c02--c06;
c01 is held for regression validation if those improve. Behavioral predictions:

| Case | v2 behavior required | Success check |
|---|---|---|
| c02 | Let sharp ZnO-like peaks constrain the common baseline; revisit WO3-specific broadening without losing inventory. | Physical correct inventory; score >80. |
| c03 | Keep the correct polymorphs/analogue; separate common widths from supported WO3 broadening and prune neutral terms. | Physical correct inventory; score >80. |
| c04 | Use sharp dominant-phase peaks as the common envelope; model broader minority phases sequentially and verify fresh replay. | Physical correct inventory; major recovery from 35.29, aiming >80. |
| c05 | Preserve helper recovery; use the sharpest phase for the baseline and assign finite size/strain to broader phases one at a time. | Ca3WO6 retained; physical; score >80. |
| c06 | Preserve all four phases; anchor common widths on sharp WO3-like peaks and test Pb-phase broadening sequentially. | PbO retained; physical; score >80. |

Any inventory regression rejects v2. Profile improvement accompanied by bounds,
non-replayable projects, or physical flags does not pass.
