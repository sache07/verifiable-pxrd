Determine the crystalline phases and their weight fractions from inputs/pattern.csv. Read inputs/metadata.json for the chemical context and measurement information. The product composition and number of phases are unknown.

Use the available scientific tools to determine and refine a structural model for each phase. Save one CIF per phase, the combined observed/calculated/difference profile as fit.csv, and result.json listing each phase, its CIF path, its weight fraction normalized over the modeled crystalline phases, and the fit statistics. Explain the evidence and remaining uncertainty briefly in report.md; state when a structure or fraction cannot be determined reliably.

Save the final GSAS-II project used to produce your submitted CIFs, phase fractions and fit.csv as final.gpx.


# Phase-model and refinement integrity

Use this sequence after initial phase screening. Save a stable project before every branch and compare complete-pattern behavior, not reported Rwp alone.

## 1. Validate and complete the phase model

**Trigger:** a candidate is imported or coherent residual peaks remain.

**Do:** Run `python learned/cif_audit.py CANDIDATE.cif`; review composition, occupancies, duplicate sites, symmetry expansion and contacts. Flags require chemical review. Reject malformed candidates. Require an atomistic model to explain multiple unique residual peaks without strong absent predictions. Carry near-tied structures through identical minimal nuisance refinement. Do not split a coherent family among weak overlap matches. Pawley/Le Bail fits may diagnose or index; if no atomistic model passes, report the component unresolved and fractions conditional.

When indexing is ambiguous, retain plausible alternative cells/families and small integer transforms until extinction and full-pattern tests discriminate them. Preserve each reproducible metric whose candidate intensities fail before making formula-first guesses. Use `python learned/cell_search.py --help` to rank masked-library cells across chemistries with only measured cells and evidence-supported symmetries. For unresolved hexagonal-axis class, query `--space-groups 143-194`. Inspect structures and make only charge-balanced substitutions from allowed sample elements while initially preserving topology and symmetry. A cell match is retrieval evidence, not identification.

Treat phase rejection as conditional on its companion structures and nuisance model. After a material inventory, angular, profile, texture or coordinate change, retest earlier source-supported candidates one at a time from the mature baseline; require stable positive scale, multi-peak support and a matched leave-one-out benefit.

Keep materially distinct same-composition alternatives exposed during screening. After accepting one, reconverge the complete model and retest remaining replacements from that updated state; repeat until a full pass makes no change.

**Check/rollback:** Require plausible geometry and material full-pattern improvement without cell collapse or overlap-only credit. Otherwise restore the stable project and report the unresolved component.

## 2. Diagnose and stage competing profile explanations

**Trigger:** after inventory is stable, centroid, width, asymmetry or intensity-envelope residuals vary systematically with angle or phase.

**Do:** Settle background, scales and cells; save a baseline and summarize residuals by angle/reflection family. Run `$GSAS2_PYTHON learned/angular_branch_select.py BASE.gpx ANGULAR.gpx inputs`; inspect `ANGULAR_BRANCH_RESULT`, reject unstable/correlated branches, propagate only material improvement from `ANGULAR.gpx`, and rerun after downstream model changes. Separately screen minimal global Gaussian/Lorentzian terms and require positive widths after reflection regeneration. Compare polarization and simple surface roughness as competing envelope explanations; test axial divergence only for supported asymmetry.

From the selected global/envelope state, test phase size and microstrain independently for every phase. Accept the best positive, stable, full-range term; reconverge and retest unretained terms until none qualifies. Repeat after every accepted structure, profile, texture, coordinate or ADP change. Test size and strain jointly only when each is independently supported. Test simple March-Dollase axes one phase at a time before spherical harmonics.

**Check/rollback:** Keep the smallest interpretable branch with multi-region benefit. Roll back negative widths, boundaries, dropped/singular variables, large shift/esd, unsupported correlations, redundant envelope terms or one-region gains. Before freezing, remove each retained optional term in matched copies and require material degradation.

## 3. Freeze a replay-safe answer

Reload the selected project and regenerate profiles/reflections. If the angular helper changed it, re-export CIFs, fractions and `fit.csv`. Run `$GSAS2_PYTHON learned/gpx_audit.py final.gpx --summary`; audit every CIF and inspect every flag. Verify convergence, finite parameters, positive fractions, plausible atoms/ADPs and cross-file agreement. On failure restore a stable branch, simplify, reconverge and re-export.

Run `python learned/submission_audit.py .`. Treat failure as incomplete export: read `result.json` back and verify recognized phase/CIF/fraction fields, intended files, normalized positive fractions and all required deliverables.

Reusable package files are in learned/.
