Determine the crystalline phases and their weight fractions from inputs/pattern.csv. Read inputs/metadata.json for the chemical context and measurement information. The product composition and number of phases are unknown.

Use the available scientific tools to determine and refine a structural model for each phase. Save one CIF per phase, the combined observed/calculated/difference profile as fit.csv, and result.json listing each phase, its CIF path, its weight fraction normalized over the modeled crystalline phases, and the fit statistics. Explain the evidence and remaining uncertainty briefly in report.md; state when a structure or fraction cannot be determined reliably.

Save the final GSAS-II project used to produce your submitted CIFs, phase fractions and fit.csv as final.gpx.


# Inventory first, then restart the profile

Apply these additions to P0.

## Complete a physical inventory

Inspect occupied composition, symmetry, source conditions, disorder, and
interatomic geometry before fitting a record. A zero scale or poor fit rejects
that record, not a chemically plausible phase: test at least one physically
screened alternate record or polymorph under the same restrained provisional
profile before exclusion. After any phase/source change, reconverge background,
all scales, the chosen single angular correction, and cells, then reinspect
residual families and precursor/product balance. Keep this inventory-stage
profile provisional; do not finalize texture or phase broadening around an
incomplete model.

Compare polymorphs with the same modest nuisance schedule and diagnostic
reflections. If no exact entry exists, search cross-chemistry prototypes with

`python learned/stoichiometric_analogues.py FORMULA INDEX_JSON_GZ --cif-root CIF_ROOT`

Optionally add indexed `--space-group N` and `--cell a b c alpha beta gamma`.
Inspect several parents, document a chemically justified substitution, screen
the adapted geometry, and refine scale then cell. Do not force a candidate
whose unique peaks or geometry fail.

## Restart after the inventory stabilizes

Begin a clean final profile pass: neutralize unused HAP defaults, roughness,
and texture; retain only one identifiable zero/displacement term. Fit a
nonnegative low-dimensional common U/W/X model that reproduces resolved sharp
peaks from the same phase at low, middle, and high angle. Test bounded SH/L
early when asymmetry repeats across peaks. A term at a bound is a failed branch,
not a value to freeze. If the inventory changes later, restart this pass.

Then challenge size-only and strain-only branches for **every retained phase**,
one phase at a time from neutral values; combine or add anisotropy only for
reproducible hkl-dependent residuals. If a branch hits a bound, revisit the
common profile. Only afterward test coherent global intensity effects, then no
texture versus symmetry-distinct axes on multiple reflection families. Reject
bound-seeking surrogates.

After each accepted profile/intensity change, save, reopen, and perform a fresh
native full-range replay. Prune unsupported terms and recheck bounds, frozen
variables, correlations, geometry, fractions, and project/export agreement.

Reusable package files are in learned/.
