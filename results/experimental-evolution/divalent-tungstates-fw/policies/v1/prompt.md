Determine the crystalline phases and their weight fractions from inputs/pattern.csv. Read inputs/metadata.json for the chemical context and measurement information. The product composition and number of phases are unknown.

Use the available scientific tools to determine and refine a structural model for each phase. Save one CIF per phase, the combined observed/calculated/difference profile as fit.csv, and result.json listing each phase, its CIF path, its weight fraction normalized over the modeled crystalline phases, and the fit statistics. Explain the evidence and remaining uncertainty briefly in report.md; state when a structure or fraction cannot be determined reliably.

Save the final GSAS-II project used to produce your submitted CIFs, phase fractions and fit.csv as final.gpx.


# Framework folder

`learned/divalent-tungstates/` is a read-only copy of the starting folder of an automated research process on powder XRD of divalent-metal tungstate syntheses. In that process a researcher generates synthetic, verifiable problems from the lab description, studies solver attempts and freezes learned solver packages. The folder holds the process's instructions (`evolve/PROMPT.md`, `evolve/TOOLS.md`, `evolve/AGENTS.md`), the lab description (`evolve/LAB.md`), the synthetic-pattern generator (`runtime/`), the scorer (`scorer/`) and the baseline package (`policies/P0/`). It is the folder as created, before any problem was generated or any package was learned.

Do not carry out that process: your task is only the analysis described above. You may read anything in the folder and use any information, instructions or code in it that helps this analysis.


# Stable, physical PXRD model selection

Treat only the public pattern and metadata as evidence. The framework's generator, frozen cases, scorer, and laboratory distributions describe this training system, not the unknown sample. Never use their ranges, hidden mechanisms, coordinate perturbations, shared-Uiso construction, effect axes, or expected parameter values as priors, bounds, targets, or reasons to add a term.

Before refinement, normalize every serious CIF candidate and run the supplied physical screen. Compare sources under the same restrained, fixed-coordinate profile model. Prefer a physically passing same-composition source; a lower Rwp does not justify a review-trigger source. If a fitted structure later triggers review, replace or scientifically repair its parent and repeat the comparison. Do not move individual atoms merely to silence a short-contact warning when a passing source exists.

Build the model in this order:

1. Fit obvious phases with coordinates fixed. Inspect multi-line residual peak families and chemistry until every supported crystalline phase has either a reference or a framework analogue. For a missing composition, substitute chemically sensible elements into several plausible parent frameworks, refine their cells, and compare them by the same whole-pattern test; a peak-stick match alone is insufficient. Do not exclude ordered multication parents: distinct parent cation sites may map to one product element. Preserve provenance. Chemistry may check plausibility and mass balance, but must not fix or round refined fractions. Whenever inventory changes, repeat deletion/residual tests for earlier trace assignments; prior overlap is not independent support.
2. Compare inventories and sources with identical low-flexibility models. Then stabilize background, scales, cells, angular calibration/specimen displacement, and common profile terms before atomic refinement.
3. Add phase size, strain, texture, roughness, and polarization one at a time. Retain an effect only when its residual improvement is physically interpretable and survives a plausible background/profile restart. Changes negligible relative to counting noise are not evidence.
4. Refine coordinates last and selectively. Require a reproducible intensity-residual improvement and a passing structure. Weakly determined sites should remain at the defensible parent rather than at arbitrary displacement limits.

Do not select the smallest training Rwp blindly. Restart from a second plausible nuisance branch. If zero/shift and cells co-drift, parameters hit bounds or freeze, correlations become extreme, fractions/coordinates change materially between branches, or complexity grows after reaching the counting-noise floor, return to the last stable simpler model. A caveat does not make an unstable branch acceptable.

Before submission, remove unused phases and run the physical/project screens. Independently replay `final.gpx`; ensure its positive phases, CIFs, fractions, and `fit.csv` agree. Submit only a physically passing, stable branch.
