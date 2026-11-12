Determine the crystalline phases and their weight fractions from inputs/pattern.csv. Read inputs/metadata.json for the chemical context and measurement information. The product composition and number of phases are unknown.

Use the available scientific tools to determine and refine a structural model for each phase. Save one CIF per phase, the combined observed/calculated/difference profile as fit.csv, and result.json listing each phase, its CIF path, its weight fraction normalized over the modeled crystalline phases, and the fit statistics. Explain the evidence and remaining uncertainty briefly in report.md; state when a structure or fraction cannot be determined reliably.

Save the final GSAS-II project used to produce your submitted CIFs, phase fractions and fit.csv as final.gpx.


# Framework folder

`learned/divalent-tungstates/` is a read-only copy of the starting folder of an automated research process on powder XRD of divalent-metal tungstate syntheses. In that process a researcher generates synthetic, verifiable problems from the lab description, studies solver attempts and freezes learned solver packages. The folder holds the process's instructions (`evolve/PROMPT.md`, `evolve/TOOLS.md`, `evolve/AGENTS.md`), the lab description (`evolve/LAB.md`), the synthetic-pattern generator (`runtime/`), the scorer (`scorer/`) and the baseline package (`policies/P0/`). It is the folder as created, before any problem was generated or any package was learned.

Do not carry out that process: your task is only the analysis described above. You may read anything in the folder and use any information, instructions or code in it that helps this analysis.


# Phase discovery and refinement discipline

Make the phase inventory falsifiable before fine refinement.

1. **Enumerate, then nominate.** For each likely composition, inspect all available same-formula structures. For any coherent unexplained peak family, search oxide prototypes with plausible cation stoichiometries, including parents requiring one or two element substitutions and fractional solid solutions. Do not restrict prototype search to the target chemical system. Construct target-composition CIFs while preserving site multiplicities and topology, then screen occupancy and geometry before fitting.

2. **Keep a candidate ledger.** Mark every planned branch pending, tested, rejected, or unknown. Compare candidates from the same stable project with common nuisance settings, first scale/background and then cell terms. Before each fit, verify that only the intended candidate is active, has a positive initialized scale, and is addressed by identity rather than a positional phase index. Let symmetry-independent lattice parameters accommodate plausible analogue mismatch. If a trial diverges, produces an invalid cell, is interrupted, or was never imported, roll back and mark it unknown—not rejected. Refit a topology- and symmetry-diverse shortlist under identical settings; prefer chemically economical routes over isolated metric or peak-position scores.

3. **Require phase closure.** After each inventory change, map positive and negative residual peak families. Do not stop while several coherent peaks remain or while a plausible precursor, intermediate, or polymorph gives a stable positive contribution. Remove additions whose scale collapses or whose apparent gain requires distorted cells or extreme broadening.

4. **Stage nuisance complexity.** Use scale/background; shift and cells; limited symmetry-allowed coordinates; isotropic profiles; then at most one supported anisotropy, texture, or roughness term at a time, retaining a simpler rollback. A lower Rwp is insufficient when a term is boundary-hitting, strongly correlated, localized, or unstable. Replay the final project and physically screen every submitted CIF.
