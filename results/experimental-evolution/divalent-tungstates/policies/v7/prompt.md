Determine the crystalline phases and their weight fractions from inputs/pattern.csv. Read inputs/metadata.json for the chemical context and measurement information. The product composition and number of phases are unknown.

Use the available scientific tools to determine and refine a structural model for each phase. Save one CIF per phase, the combined observed/calculated/difference profile as fit.csv, and result.json listing each phase, its CIF path, its weight fraction normalized over the modeled crystalline phases, and the fit statistics. Explain the evidence and remaining uncertainty briefly in report.md; state when a structure or fraction cannot be determined reliably.

Save the final GSAS-II project used to produce your submitted CIFs, phase fractions and fit.csv as final.gpx.


# Evidence checkpoints before completion

Apply these additions to P0.

## Recover and revisit the inventory

Screen candidate composition, source conditions, disorder, and geometry. A
poor fit rejects that record, not plausible chemistry; compare a physical
alternate or polymorph under the same restrained nuisance model. Make a
precursor element/charge balance for retained phases. If coherent residual
families and an imbalance remain, enumerate a few charge-balanced formulas,
including non-1:1 products, then search exact records or run

`python learned/stoichiometric_analogues.py FORMULA INDEX_JSON_GZ --cif-root CIF_ROOT`

Inspect several parents and physical-screen any substitution. Keep plausible
weak phases on a watch list. After a phase/source change, reconverge a smooth
background, scales, cells, one angular correction, and common profile; then
re-challenge the watch list.

## Require measured profile evidence

Neutralize unused phase terms and establish a nonnegative low-dimensional
U/W/X baseline; release SH/L only for repeated asymmetry. Before calling it
adequate, record observed/calculated position, FWHM, and left/right half-width
for isolated peaks of each appreciable phase at low, middle, and high angle.
Overall Rwp or a prose claim is insufficient.

For an angle- or hkl-dependent mismatch, compare size and strain from the same
saved baseline, one phase at a time. Combine only complementary replay-stable
terms; if isotropic treatment leaves directional mismatch, test compatible
anisotropy. Before texture, challenge background, polarization, and roughness;
compare no texture with distinct axial and diagonal axes. Repeat the numerical
audit. If structured residual or goodness-of-fit materially above counting
expectation remains, return to the baseline and inventory.

## Freeze scorer-ready outputs

After each accepted change, save, reopen, and replay the full range. Prune
unsupported/bound terms and verify geometry. Before answering, parse
`result.json`: every phase needs a numeric `weight_fraction`, fractions must
sum to one, each `cif_path` must exist, `project_path` must name `final.gpx`,
and CIFs, fractions, and `fit.csv` must agree with that reopened project.

Reusable package files are in learned/.
