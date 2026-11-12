Determine the crystalline phases and their weight fractions from inputs/pattern.csv. Read inputs/metadata.json for the chemical context and measurement information. The product composition and number of phases are unknown.

Use the available scientific tools to determine and refine a structural model for each phase. Save one CIF per phase, the combined observed/calculated/difference profile as fit.csv, and result.json listing each phase, its CIF path, its weight fraction normalized over the modeled crystalline phases, and the fit statistics. Explain the evidence and remaining uncertainty briefly in report.md; state when a structure or fraction cannot be determined reliably.

Save the final GSAS-II project used to produce your submitted CIFs, phase fractions and fit.csv as final.gpx.


# Framework folder

`learned/divalent-tungstates/` is a read-only copy of the starting folder of an automated research process on powder XRD of divalent-metal tungstate syntheses. In that process a researcher generates synthetic, verifiable problems from the lab description, studies solver attempts and freezes learned solver packages. The folder holds the process's instructions (`evolve/PROMPT.md`, `evolve/TOOLS.md`, `evolve/AGENTS.md`), the lab description (`evolve/LAB.md`), the synthetic-pattern generator (`runtime/`), the scorer (`scorer/`) and the baseline package (`policies/P0/`). It is the folder as created, before any problem was generated or any package was learned.

Do not carry out that process: your task is only the analysis described above. You may read anything in the folder and use any information, instructions or code in it that helps this analysis.


# Stable, cumulative PXRD model selection

Treat only the public pattern and metadata as evidence. The generator, frozen cases, scorer, and laboratory distributions describe this training system, not the unknown sample. Never use their hidden mechanisms, ranges, coordinates, effect axes, or expected values as priors, bounds, targets, or reasons to add terms.

Normalize and physically screen every serious CIF before refinement. A lower Rwp never justifies a review-trigger source when a passing source exists. Build the crystalline inventory from coherent multi-line residual families and chemistry, keeping coordinates fixed. For a missing composition, map chemically sensible elements into several plausible frameworks, including ordered multication parents whose distinct sites may collapse onto one product element. Include composition- and topology-nearest parents even when their unadapted sticks or cells are not the closest; adapt cells and compare restrained whole-pattern fits. Preserve provenance. Fractions must remain data-refined, not fixed or rounded by chemistry. After any inventory change, repeat residual and deletion tests for earlier trace assignments.

An identical low-flexibility comparison creates a shortlist, not a final source or analogue decision. For a missing composition, carry several chemistry/topology-nearest framework parents through completed matched restarts despite different early Rwp or scale. After inventory and nuisance stabilization, swap each finalist into the cumulative model, re-equilibrate its plausible profile mechanisms, then give every credible parent the same restrained coordinate-adaptation opportunity. Fixed inherited coordinates rank particular parent refinements, not necessarily frameworks. Test small element/site blocks in identical order, re-equilibrating the cumulative model and physically screening after each accepted block; repeat promising results from an independent nuisance start. A failed, bound-hitting, nonconvergent, or initially collapsing credible-parent branch is inconclusive: restage it from lower flexibility rather than drop it. If distinct lineages converge to the same physical structure and profile, treat them as one solution and prefer simpler or chemically nearer provenance over a tiny Rwp difference.

Before moving atoms, make one mechanism-complete profile pass: background family/order; scales and cells; zero-only, specimen-displacement-only, and their joint branch; common width/asymmetry terms including axial divergence; roughness and polarization; then size, strain, and plausible texture for every phase. One-at-a-time trials are only screening. Inventory, profile, texture, and broadening effects can mask one another, so after each major change re-equilibrate the retained model and retest plausible earlier failures, including supported combinations. Do not declare the counting-noise floor unreachable while a coherent residual shape remains and this pass is incomplete.

Bounds, freezing, implausible coefficients, or branch-dependent fractions/structures require a different mechanism or restart. High correlation alone does not prove that the forward correction is false: retain a correlated nuisance subspace when independent plausible starts reproduce the calculated curve, fractions, and structures without frozen or physically invalid variables. Judge that subspace by predictive stability, not by interpreting its individual coefficients. Conversely, reject correlated drift that changes cells, fractions, structures, or the curve across starts.

Coordinate adaptation is model selection, not permission for unconstrained atom movement. Retain a block only when its intensity-residual improvement repeats across plausible nuisance starts and the structure passes screening; otherwise restore the defensible parent. Test remaining defensible blocks even if one block is unstable.

Before submission, remove unsupported phases, rerun deletion and physical/project screens, and independently replay `final.gpx`. Its positive phases, CIFs, fractions, and `fit.csv` must agree.
