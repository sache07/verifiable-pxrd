Determine the crystalline phases and their weight fractions from inputs/pattern.csv. Read inputs/metadata.json for the chemical context and measurement information. The product composition and number of phases are unknown.

Use the available scientific tools to determine and refine a structural model for each phase. Save one CIF per phase, the combined observed/calculated/difference profile as fit.csv, and result.json listing each phase, its CIF path, its weight fraction normalized over the modeled crystalline phases, and the fit statistics. Explain the evidence and remaining uncertainty briefly in report.md; state when a structure or fraction cannot be determined reliably.

Save the final GSAS-II project used to produce your submitted CIFs, phase fractions and fit.csv as final.gpx.


# Framework folder

`learned/divalent-tungstates/` is a read-only copy of the starting folder of an automated research process on powder XRD of divalent-metal tungstate syntheses. In that process a researcher generates synthetic, verifiable problems from the lab description, studies solver attempts and freezes learned solver packages. The folder holds the process's instructions (`evolve/PROMPT.md`, `evolve/TOOLS.md`, `evolve/AGENTS.md`), the lab description (`evolve/LAB.md`), the synthetic-pattern generator (`runtime/`), the scorer (`scorer/`) and the baseline package (`policies/P0/`). It is the folder as created, before any problem was generated or any package was learned.

Do not carry out that process: your task is only the analysis described above. You may read anything in the folder and use any information, instructions or code in it that helps this analysis.


# Cumulative, physical PXRD closure

Use only the public pattern, metadata, and reference library. Generator settings, frozen cases, scorer details, and laboratory distributions are not structural or profile priors: never use their ranges, coordinates, effects, or expected values as targets or bounds.

Physically screen every serious CIF before fitting. Prefer a passing source over a lower-Rwp review source. Build inventory from chemistry plus coherent multi-line residual families with coordinates fixed; refine fractions from the data. For a missing composition, construct several chemically plausible mapped frameworks, including ordered multication parents whose sites may collapse onto one product element. Carry composition- and topology-nearest parents through completed cumulative restarts even if early fixed-coordinate ranking is poor. Restage a credible branch that freezes, hits bounds, collapses scale/size, or fails to converge. Before final parent choice, give every credible mapped parent identical small element/site coordinate blocks, profile re-equilibration, physical screening, and an independent nuisance start. If lineages converge, prefer simpler or chemically nearer provenance over a tiny Rwp edge.

Close inventory before expensive coordinate work. A distinct unindexed multi-line family reopens inventory; extrema centered on modeled reflections call for structure/profile alternatives, not duplicate phases. After any inventory change, repeat residual and deletion tests for trace phases.

Before moving atoms, make one cumulative profile pass: background family/order; scale/cell; zero, displacement, and their joint alternative; common widths and axial divergence; roughness and polarization; then size, strain, and plausible texture for every phase. Retest earlier failures after major changes. Correlation alone is acceptable only when independent starts reproduce the curve, fractions, and structures without freezing or invalid widths.

Refine coordinates last in evidence-based element/site blocks. If an isolated ligand move creates contacts, allow one coupled neighboring-ligand retry with soft geometry restraints and smaller steps. If still unstable, restore the parent; do not proliferate branches. Reserve time for closure and export.

After a structural rollback, or when a physical complete model remains above counting noise, run once:

`$GSAS2_PYTHON learned/profile_closure.py final.gpx profile_closed.gpx inputs`

The helper fixes atoms, compares a held-common-width phase-size decomposition when size models are missing, tests uniaxial directions, missing roughness-A, and smooth background-order alternatives, and rejects frozen, nonstationary, nonphysical, or AIC-unsupported branches. Its starts are relative to the saved project, not sample priors. Inspect `profile_closed.size_restart.json` and replay the selected project. If clean, use `profile_closed.gpx` as `final.gpx` and re-export every CIF, fraction, `fit.csv`, and result from it.

Finally remove unsupported phases, rerun deletion and physical checks, independently replay `final.gpx`, and verify all submitted artifacts agree.

Reusable package files are in learned/.
