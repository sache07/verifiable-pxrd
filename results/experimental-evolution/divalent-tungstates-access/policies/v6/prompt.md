Determine the crystalline phases and their weight fractions from inputs/pattern.csv. Read inputs/metadata.json for the chemical context and measurement information. The product composition and number of phases are unknown.

Use the available scientific tools to determine and refine a structural model for each phase. Save one CIF per phase, the combined observed/calculated/difference profile as fit.csv, and result.json listing each phase, its CIF path, its weight fraction normalized over the modeled crystalline phases, and the fit statistics. Explain the evidence and remaining uncertainty briefly in report.md; state when a structure or fraction cannot be determined reliably.

Save the final GSAS-II project used to produce your submitted CIFs, phase fractions and fit.csv as final.gpx.


# Framework folder

`learned/divalent-tungstates/` is a read-only copy of the starting folder of an automated research process on powder XRD of divalent-metal tungstate syntheses. In that process a researcher generates synthetic, verifiable problems from the lab description, studies solver attempts and freezes learned solver packages. The folder holds the process's instructions (`evolve/PROMPT.md`, `evolve/TOOLS.md`, `evolve/AGENTS.md`), the lab description (`evolve/LAB.md`), the synthetic-pattern generator (`runtime/`), the scorer (`scorer/`) and the baseline package (`policies/P0/`). It is the folder as created, before any problem was generated or any package was learned.

Do not carry out that process: your task is only the analysis described above. You may read anything in the folder and use any information, instructions or code in it that helps this analysis.


# Close first, polish once

Work from the specimen inputs, pattern, and frozen reference index. Build the
chemically ordinary phases first and preserve a complete, physical, replayable
checkpoint before optional branches.

Map coherent residual reflection families in that best multiphase state. Test
exact-composition references and plausible residual precursors or products
there; require physical geometry, stable positive scale, and broad family
support. When same-composition checkpoint fits are close, choose the physical
model; a small Rwp gain never justifies bad geometry. Numerical failure is
unknown, not rejection. Use cross-chemistry transfer only while a coherent
family remains genuinely unassigned and its target stoichiometry has chemical
support.

Once every coherent family indexes to accepted phases, stop reference and
prototype search. Complete ordinary scales/background, cells/calibration,
coordinates, and supported specimen/profile terms from the best checkpoint.
If residual intensity errors remain centered on accepted reflections, save
that complete physical model as `final.gpx` and run the bounded final-stage
polish once:

```bash
$GSAS2_PYTHON learned/staged_polish.py final.gpx polished.gpx inputs
```

The helper compares coordinate orders, rolls clipped atoms back, audits
relative geometry and phase-fraction stability, and returns the starting
checkpoint unless a converged physical branch makes a material profile gain.
It cannot repair a wrong inventory or topology. Review
`polished.staged_polish.json`; reject any scientifically implausible result.
When a polished branch is accepted, make `polished.gpx` the submitted
`final.gpx` and re-export every CIF, phase fraction, `fit.csv`, and report from
that exact project so all deliverables remain consistent.

Reusable package files are in learned/.
