# Iterate inventory and profile

Apply these additions to P0.

## Keep inventory decisions reversible

Inspect occupied composition, symmetry, source conditions, disorder, and
geometry before fitting a record. A zero scale or poor fit rejects that record,
not a plausible phase: test a physically screened alternate record or
polymorph under the same provisional nuisance model. Compare polymorphs by
diagnostic reflections with identical modest nuisance terms.

If no exact entry exists, search cross-chemistry prototypes with

`python learned/stoichiometric_analogues.py FORMULA INDEX_JSON_GZ --cif-root CIF_ROOT`

Optionally add indexed `--space-group N` and `--cell a b c alpha beta gamma`.
Inspect several parents, justify substitutions, and refine scale then cell.

After any phase/source change, reconverge smooth background, all scales, a
provisional angular correction, and cells. Keep plausible weak candidates whose unique
families partly overlap on a watch list; a small provisional gain is not a
final exclusion.

## Iterate after a clean restart

Once the provisional inventory is coherent, neutralize unused HAP defaults,
roughness, and texture. Fit nonnegative common U/W/X and early bounded SH/L
from more than one interior start, requiring resolved sharp peaks from the same
phase at low, middle, and high angle to share one angular width/asymmetry trend.
A bound branch is failed, not evidence that the term is absent: retry an
interior start or another resolved family. Do not proceed with a reduced common
profile while a systematic angular trend remains.

With the same converged common profile, compare zero-only and
specimen-displacement-only branches. Retain one unless independent calibration
supports both; judge coherent angle-dependent position residuals and plausible
cells, not Rwp alone.

Under that physical common profile, re-challenge every watched candidate and a
screened source alternate. If inventory changes, repeat the clean common pass;
iterate until both inventory and profile are stable.

Then test size-only and strain-only for every retained phase, one at a time
from truly neutral stored values. Combine terms only when both survive replay.
If both single-term branches are interior and explain complementary residual
families, test their combination rather than selecting only the lower Rwp.
If isotropic branches hit bounds while reproducible hkl-dependent widths
remain, challenge a symmetry-appropriate uniaxial strain model before pruning.

Before texture, explicitly compare a physically smooth background,
polarization, and sample roughness for coherent cross-phase intensity trends;
do not let a high-order background replace a shared low-angle effect. Then
compare no texture with symmetry-distinct axial and diagonal low-index axes on
multiple isolated families.

After each accepted change, save, reopen, and perform a native full-range
replay. Recheck bounds, frozen variables, correlations, geometry, fractions,
and project/export agreement.
