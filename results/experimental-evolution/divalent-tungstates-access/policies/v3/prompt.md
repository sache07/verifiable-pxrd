Determine the crystalline phases and their weight fractions from inputs/pattern.csv. Read inputs/metadata.json for the chemical context and measurement information. The product composition and number of phases are unknown.

Use the available scientific tools to determine and refine a structural model for each phase. Save one CIF per phase, the combined observed/calculated/difference profile as fit.csv, and result.json listing each phase, its CIF path, its weight fraction normalized over the modeled crystalline phases, and the fit statistics. Explain the evidence and remaining uncertainty briefly in report.md; state when a structure or fraction cannot be determined reliably.

Save the final GSAS-II project used to produce your submitted CIFs, phase fractions and fit.csv as final.gpx.


# Framework folder

`learned/divalent-tungstates/` is a read-only copy of the starting folder of an automated research process on powder XRD of divalent-metal tungstate syntheses. In that process a researcher generates synthetic, verifiable problems from the lab description, studies solver attempts and freezes learned solver packages. The folder holds the process's instructions (`evolve/PROMPT.md`, `evolve/TOOLS.md`, `evolve/AGENTS.md`), the lab description (`evolve/LAB.md`), the synthetic-pattern generator (`runtime/`), the scorer (`scorer/`) and the baseline package (`policies/P0/`). It is the folder as created, before any problem was generated or any package was learned.

Do not carry out that process: your task is only the analysis described above. You may read anything in the folder and use any information, instructions or code in it that helps this analysis.


# Reflection-family closure

Use cross-chemistry prototype transfer only for a coherent reflection family
that accepted phases and ordinary plausible precursor/product references do not
index. Residual intensity, position, or width errors at accepted reflections
call for structural/profile refinement, not another phase. For a genuinely
unassigned family, retain a small reaction-balanced set of plausible
stoichiometries; for each, search matching frameworks across chemistries,
including one- or two-element substitutions, and retain distinct plausible
symmetries.

Test additions, replacements, and physically clean same-formula references in
the current best multiphase project. Reject a plausible weak component only
after stable scale collapse; failed trials remain unknown. Prefer a chemically
economical, stoichiometrically supported topology. Do not rank it by an early
scale/cell fit against a more deeply adapted decoy: give serious candidates
comparable staged cell, symmetry-allowed coordinate, and profile relaxation.

Once every coherent residual family indexes to accepted phases, stop library
search. If an accepted transferred framework still misfits intensities at its
own reflections, test distinct physical coordinate starts before seeking
another phase. Refine accepted phases one at a time: well-resolved/heavy
coordinates before weak light-atom substructures, retaining physical
rollbacks; then calibration/specimen and phase-specific size, strain, and
texture. Keep only physical gains reproduced by fresh full-grid replay.
