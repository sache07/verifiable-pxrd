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

Then compare size and strain from neutral values, one phase at a time. Combine
only complementary replay-stable terms. If hkl families remain differently
broad, challenge symmetry-appropriate anisotropy. Before texture, decide
whether any coherent cross-phase intensity trend is background, polarization,
or low-angle roughness; reject scale/background surrogates. Compare no texture
with symmetry-distinct axial and diagonal low-index axes, requiring support
from multiple isolated families.

After each accepted change, save, reopen, and replay the full range. Prune
unsupported or bound terms and verify geometry, fractions, and exact
project/export agreement.
