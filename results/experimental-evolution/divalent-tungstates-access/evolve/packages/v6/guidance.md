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
