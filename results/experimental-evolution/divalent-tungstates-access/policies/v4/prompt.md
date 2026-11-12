Determine the crystalline phases and their weight fractions from inputs/pattern.csv. Read inputs/metadata.json for the chemical context and measurement information. The product composition and number of phases are unknown.

Use the available scientific tools to determine and refine a structural model for each phase. Save one CIF per phase, the combined observed/calculated/difference profile as fit.csv, and result.json listing each phase, its CIF path, its weight fraction normalized over the modeled crystalline phases, and the fit statistics. Explain the evidence and remaining uncertainty briefly in report.md; state when a structure or fraction cannot be determined reliably.

Save the final GSAS-II project used to produce your submitted CIFs, phase fractions and fit.csv as final.gpx.


# Framework folder

`learned/divalent-tungstates/` is a read-only copy of the starting folder of an automated research process on powder XRD of divalent-metal tungstate syntheses. In that process a researcher generates synthetic, verifiable problems from the lab description, studies solver attempts and freezes learned solver packages. The folder holds the process's instructions (`evolve/PROMPT.md`, `evolve/TOOLS.md`, `evolve/AGENTS.md`), the lab description (`evolve/LAB.md`), the synthetic-pattern generator (`runtime/`), the scorer (`scorer/`) and the baseline package (`policies/P0/`). It is the folder as created, before any problem was generated or any package was learned.

Do not carry out that process: your task is only the analysis described above. You may read anything in the folder and use any information, instructions or code in it that helps this analysis.


# Phase closure and topology coverage

Begin from the specimen inputs, pattern, and frozen reference index. Autonomous-evolution, controller, generator, and scorer sources are not specimen evidence and normally need no inspection. As soon as ordinary references give a physical multiphase model, save a complete replayable checkpoint before optional branches.

Map residual peaks against accepted reflections. For a coherent unassigned family, test exact-composition references and plausible precursors/intermediates first. If transfer is needed, rank a few target formulas by the measured precursor ratio and the molar balance of the whole current phase inventory, not by a residual cell alone. Prefer a formula that closes that balance without ad hoc extra phases. For each formula, cover distinct symmetry and coordination topologies before ranking: retain one chemically nearest physical parent per topology, including parents from substituted chemistries. Do not exhaustively screen many records of one formula or topology. Compare serious branches in the same multiphase state with comparable staged scale, cell, heavy-atom, limited light-atom, and profile relaxation; an early Rwp lead does not eliminate a topology. Same-composition alternatives must pass geometry screening. When their checkpoint fits are close, choose the physical model; a small Rwp gain never justifies known bad geometry.

Once every coherent family indexes to accepted phases, stop all reference and prototype search. Return to the best physical checkpoint and refine accepted phases: scales/background and cells/calibration; heavy then light coordinates with rollback; then specimen/profile terms, adding only one supported anisotropy or texture family at a time. If an accepted topology has the right reflections but wrong relative intensities, try a small number of physically bounded coordinate starts before changing phase identity. Preserve a complete physical replay after each genuine improvement. Reject a plausible weak phase only after stable scale collapse; numerical failure is unknown. Submit the best full-grid physical replay, not the last branch attempted.
