Determine the crystalline phases and their weight fractions from inputs/pattern.csv. Read inputs/metadata.json for the chemical context and measurement information. The product composition and number of phases are unknown.

Use the available scientific tools to determine and refine a structural model for each phase. Save one CIF per phase, the combined observed/calculated/difference profile as fit.csv, and result.json listing each phase, its CIF path, its weight fraction normalized over the modeled crystalline phases, and the fit statistics. Explain the evidence and remaining uncertainty briefly in report.md; state when a structure or fraction cannot be determined reliably.

Save the final GSAS-II project used to produce your submitted CIFs, phase fractions and fit.csv as final.gpx.


# Framework folder

`learned/divalent-tungstates/` is a read-only copy of the starting folder of an automated research process on powder XRD of divalent-metal tungstate syntheses. In that process a researcher generates synthetic, verifiable problems from the lab description, studies solver attempts and freezes learned solver packages. The folder holds the process's instructions (`evolve/PROMPT.md`, `evolve/TOOLS.md`, `evolve/AGENTS.md`), the lab description (`evolve/LAB.md`), the synthetic-pattern generator (`runtime/`), the scorer (`scorer/`) and the baseline package (`policies/P0/`). It is the folder as created, before any problem was generated or any package was learned.

Do not carry out that process: your task is only the analysis described above. You may read anything in the folder and use any information, instructions or code in it that helps this analysis.
