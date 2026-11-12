# Phase-model and refinement integrity

After screening, save a stable project before every branch and compare complete-pattern behavior, not reported Rwp alone.

## 1. Validate and complete the phase model

**Trigger:** a candidate is imported or coherent residual peaks remain.

**Do:** Run `python learned/cif_audit.py CANDIDATE.cif`; review composition, occupancies, duplicate sites, symmetry expansion and contacts. Flags require review. Reject malformed candidates. Require an atomistic model to explain unique residual peaks without strong absent predictions. Carry near-tied structures through identical minimal nuisance refinement; do not split one coherent family among overlap matches. Pawley/Le Bail fits may diagnose or index, but unresolved atomistic components and conditional fractions must be reported honestly.

When indexing is ambiguous, retain non-equivalent cells and integer transforms until extinction and full-pattern tests discriminate them. Preserve reproducible metrics whose candidate intensities fail before making formula-first guesses. Use `python learned/cell_search.py --help` to rank masked-library cells across chemistries from measured cells and supported symmetries. For unresolved hexagonal-axis class query `--space-groups 143-194`. Inspect structures and make only charge-balanced substitutions from allowed elements while preserving topology and symmetry. A cell match is retrieval evidence, not identification.

Treat phase rejection as conditional. After a material inventory, angular, profile, texture or coordinate change, retest earlier source-supported candidates individually from the mature baseline; require stable positive scale, multi-peak support and matched leave-one-out benefit.

At retrieval, ledger every valid inspected candidate by formula and distinct cell/topology. Keep it open until replacement-tested from the latest complete model or rejected for audited chemistry/geometry or strong absent predictions; a coexisting same-formula addition does not count. After acceptance, reconverge and repeat open replacements to a no-change pass.

When a provisional atomistic component leaves coherent mature residuals and a material flexible-reflection advantage after major changes, overlap with its own reflections does not close the trigger: freeze companions, remove it, regenerate residual peaks and index all Bravais classes without its cell/family. Retrieve compatible/cross-chemistry models and test replacements; restore it if none gives stable full-pattern improvement.

**Check/rollback:** Require plausible geometry and material full-pattern improvement without cell collapse or overlap-only credit. Otherwise restore the stable project and report the unresolved component.

## 2. Diagnose and stage competing profile explanations

**Trigger:** after inventory stabilizes, centroid, width, asymmetry or intensity-envelope residuals vary systematically with angle or phase.

**Do:** Settle background, scales and cells. Run `$GSAS2_PYTHON learned/angular_branch_select.py BASE.gpx ANGULAR.gpx inputs`; inspect `ANGULAR_BRANCH_RESULT`, reject unstable/correlated branches, propagate only material improvement and rerun after downstream changes. Separately screen minimal global Gaussian/Lorentzian terms and require positive regenerated widths. Compare polarization and roughness; test axial divergence only for supported asymmetry.

From the selected state, neutralize inactive phase-width values, then test size and microstrain independently for every phase. Accept the best positive, stable, full-range term; reconverge and retest unretained terms after every accepted structure, profile, texture, coordinate or ADP change. Test size plus strain only when each is independently supported. Test simple March-Dollase axes one phase at a time before spherical harmonics.

**Check/rollback:** Keep the smallest interpretable branch with multi-region benefit. Roll back negative widths, boundaries, dropped/singular variables, large shift/esd, unsupported correlations, redundant terms or one-region gains. Before freezing, remove each retained optional term in matched copies and require material degradation.

## 3. Freeze a replay-safe answer

Reload the selected project and regenerate profiles/reflections. After angular changes re-export CIFs, fractions and `fit.csv`. Run `$GSAS2_PYTHON learned/gpx_audit.py final.gpx --summary`; audit every CIF and inspect every flag. Verify convergence, finite parameters, positive fractions, plausible atoms/ADPs and cross-file agreement. On failure restore, simplify, reconverge and re-export.

Run `python learned/submission_audit.py .`; read `result.json` back and verify recognized phase/CIF/fraction fields, intended files, normalized positive fractions and all deliverables.
