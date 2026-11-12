# Reversible, residual-led refinement

Apply these additions to P0.

## Build and revisit the inventory

Screen occupied composition, symmetry, source conditions, disorder, and
geometry before fitting. A poor fit or zero scale rejects that record, not a
chemically plausible phase: compare a physical alternate record or polymorph
under the same restrained nuisance model. Keep plausible weak phases supported
by coherent unique or partly overlapped families on a watch list.

If no exact entry exists, search cross-chemistry prototypes with

`python learned/stoichiometric_analogues.py FORMULA INDEX_JSON_GZ --cif-root CIF_ROOT`

Optionally add indexed `--space-group N` and
`--cell a b c alpha beta gamma`. Inspect several parents, justify any site
substitution, physical-screen the model, and refine scale before cell.

After any phase or source change, reconverge a smooth low-order background, all
scales, one angular correction, and cells. Once the provisional inventory is
coherent, establish a clean common profile and re-challenge the watch list
under it. If inventory changes, rebuild that profile before judging phases.

## Require a physically adequate baseline

Neutralize unused phase size/strain, roughness, and texture. Fit one zero or
specimen-displacement correction and a nonnegative low-dimensional U/W/X
profile; release SH/L when asymmetry repeats across peaks. Judge adequacy from
observed-versus-calculated positions, FWHM, and asymmetry for isolated families
of the same phase at low, middle, and high angle, plus a smooth plausible
background—not from Rwp, interior values, or covariance alone. If a systematic
trend remains, or all phase-width trials collapse or hit bounds, return to the
baseline and inventory rather than adding nuisance terms.

From the same saved checkpoint, compare neutral, size, strain, and combined
size-plus-strain one phase at a time. Retain only complementary replay-stable
terms. If hkl families remain differently broad, challenge
symmetry-appropriate anisotropy. Before texture, decide whether any coherent
cross-phase intensity trend is background, polarization, or low-angle
roughness; reject scale/background surrogates. Compare no texture with
symmetry-distinct axial and diagonal low-index axes, requiring support from
multiple isolated families.

## Complete supported heavy-atom coordinates

Only after inventory, sources, cells, and profile terms are stable, save and
reopen `final.gpx`, then run

`$GSAS2_PYTHON learned/staged_heavy_coordinates.py final.gpx coordinated.gpx inputs`

The helper challenges previously fixed sites with atomic number at least 20,
one site at a time. It rejects gains below 0.003 Rwp percentage point, moves
above 0.15 Å, new frozen variables, or failed contact checks. Adopt
`coordinated.gpx` as `final.gpx` only when its log reports accepted sites and a
fresh reopen preserves the gain; otherwise retain the original project.

After every accepted change, save, reopen, and replay the full original
observation grid. Prune unsupported or bound terms and verify geometry and
fractions. Never round or resample observations. If several matching
histograms remain, name the final one with `refinement_histogram` in
`result.json`. After the last replay, re-export every CIF, phase fraction,
`fit.csv`, and fit statistic from that exact `final.gpx`.
