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

## Results as completed

| Case | Score / profile | Behavioral result | Decision |
|---|---|---|---|
| c02 | 60.94; D 0.956; Rwp 3.840%; physical pass | Correct screened three-phase inventory and fresh replay. The solver used a sharp-peak lower envelope and separate size/strain challenges, but retained common W only and size-only terms for all phases. This underfit the low/mid/high-angle common trend and omitted WO3 strain; fractions remain biased. | Behavioral adoption passes but scientific result regresses from v1 72.56. Any successor must require common-profile angular adequacy before phase attribution, not merely a narrow lower envelope. |
| c05 | 52.30; D 2.190; Rwp 3.984%; physical pass | The helper again recovered Ca3WO6 and all three sources are physical. A nonnegative U/W/X baseline plus sequential challenges recovered CaWO4 size 0.0915 micrometre (truth 0.0886) and pruned unsupported minor-phase terms. Fractions remain close. The retained CaWO4 [001] texture branch repeats v1's likely intensity surrogate. | Profile-allocation mechanism partially passes (D 3.214->2.190) but target fails. Preserve the sequence; test common-profile angular adequacy and controlled texture-axis comparison next. |
| c04 | 36.48; D 12.941; Rwp 9.055%; physical pass | Correct three-phase inventory, closer ZnWO4-derived parent, and structural score 80.44. The solver anchored on MnWO4 but fixed common W=25 plus X, rejected U/SH-L, drove size branches to bounds, and represented broad minority peaks with 7640/9930 ppm strain. This is far from the known D=0.082 width-allocation ceiling. | Behavioral adoption passes but profile inference fails. A successor needs an explicit low/mid/high-angle adequacy test for the common Gaussian/Lorentz trend and must not reject bounded asymmetry solely for high covariance when reproducible residual evidence remains. |
| c03 | 38.74; D 4.250; Rwp 6.569%; physical pass | All three formulas were retained, but the solver selected triclinic WO3 after comparing candidates under a fixed common W=42 plus X profile. Under those confounded settings triclinic WO3 only marginally beat monoclinic WO3 (Rwp 7.537% versus 7.622%), then absorbed mismatch with 4195 ppm WO3 strain. The structural score fell to 68.28. | This is a polymorph/profile interaction, not missing chemistry. Compare polymorphs only after each candidate has an adequate common profile; the lower-envelope instruction must not freeze nuisance assumptions that bias structural selection. |
| c06 | 43.60; D 4.629; Rwp 5.768%; physical pass | The correct four-phase inventory remained physical with structural score 82.35, but the solver fixed common U=5, W=20, X=0 from a lower-envelope estimate before assigning three phase-size terms and WO3 strain. v1's much better fit used a strong angular common trend, so the forced narrow baseline caused the regression despite near-correct fractions. | Inventory behavior passes and profile behavior fails. A sharp lower envelope is only a guard against averaging phase widths; it cannot substitute for checking common width adequacy across low, middle, and high angle. |

Across unresolved c02--c06, v2 averaged 46.41 versus v1's 57.87 on the
same cases. All inventories remained complete and all projects replayed
physically, but four cases regressed and none met the predeclared score target.
The c01 holdout is therefore not spent. Reject the v2 wording as a package
candidate; retain only the evidence that sequential phase-width tests and fresh
replay are useful after, not before, an adequate common profile is established.

## Follow-up diagnostics

`ptest-common-release-v2-02` retained every submitted structure and phase term,
then released bounded common W, U, and X sequentially. All five projects stayed
physical, but fresh-replay D changed only c02 0.956->0.945, c03 4.250->4.249,
c04 12.941->12.299, c05 2.190->2.190, and c06 4.629->4.544. U returned to its
zero bound in every previously underfit endpoint. This rejects a post-hoc
release helper: after phase size/strain has absorbed the trend, local
reconvergence cannot recover the common angular profile. The useful successor
rule is sequencing and an adequacy checkpoint before phase terms, plus an
explicit return to that checkpoint when phase terms hit bounds; it is not
"free more U/W/X at the end."

`ptest-texture-axis-c05-01` compared a texture-free branch and primitive
first-shell March--Dollase directions from both independent c05 endpoints. Both
selected [110], with fitted ratios 1.266/1.265 rather than the retained [001]
ratios near 0.894. Fresh replay stayed physical and improved v1 D
3.214->1.817 (Rwp 4.617->3.765%) and v2 D 2.190->0.765 (Rwp
3.984->2.943%). This is a replicated causal intensity-allocation mechanism.
Add a concise comparison of no texture and plausible symmetry-distinct axes
using multiple diagnostic intensity families; do not ship the exhaustive
enumerator without transfer evidence.

`ptest-shl-v1-02` released bounded SH/L from all six v1 endpoints and the v2
c04 endpoint. All seven stayed physical, but this was not a c04 rescue: v1 D
8.892->8.815 and v2 D 12.941->12.910. Other changes were at most 0.009 in D.
Notably, c01 fitted an interior SH/L with 0.962 correlation to zero while D
slightly improved 0.0250->0.0235. Thus covariance alone is not a scientific
rejection criterion, but late release after other terms have absorbed the
signature is ineffective. Test reproducible low-angle asymmetry in a clean
common-profile branch before phase widths; do not ship a post-hoc SH/L helper.

`ptest-surface-roughness-01` released Suortti A then B from all v1 endpoints
and the v2 c02/c05 endpoints. The target effect replicated: c02 D
0.419->0.278 and 0.956->0.354; c05 D 3.214->2.234 and 2.190->1.349. c01
was unchanged and c06 nearly neutral, but misfit c03/c04 also gained smaller
amounts and three target fits drove A to a bound. This supports ordering, not an
automatic correction: diagnose a coherent global low-angle intensity trend and
test sample roughness/polarization before assigning phase texture; require
interior stability, diagnostic peaks, and fresh replay. Exclude the procedure
and every fitted value from v3.
