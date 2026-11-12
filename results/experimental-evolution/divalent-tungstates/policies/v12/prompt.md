Determine the crystalline phases and their weight fractions from inputs/pattern.csv. Read inputs/metadata.json for the chemical context and measurement information. The product composition and number of phases are unknown.

Use the available scientific tools to determine and refine a structural model for each phase. Save one CIF per phase, the combined observed/calculated/difference profile as fit.csv, and result.json listing each phase, its CIF path, its weight fraction normalized over the modeled crystalline phases, and the fit statistics. Explain the evidence and remaining uncertainty briefly in report.md; state when a structure or fraction cannot be determined reliably.

Save the final GSAS-II project used to produce your submitted CIFs, phase fractions and fit.csv as final.gpx.


# Anchor chemistry before cyclic refinement

Apply these additions to P0.

## Gate inventory and sources

For every likely retained source or adapted model, run

`python learned/cif_health.py CANDIDATE.cif [...]`

before fitting and on final CIFs. Health pass screens geometry, not whether one
record represents the observed polymorph. For each context- or balance-plausible
exact formula, if the first record fits poorly or its scale collapses, compare
at least one structurally distinct physical record or polymorph when available
before excluding that formula or constructing an analogue. Poor fit rejects the
record, not plausible chemistry. Treat alternate records as competitors, not
coexisting phases.

Retain a weak phase only with positive replay-stable scale and at least two
independent non-coincident families. Same-formula coexistence must also survive
replacing/removing either model plus broadening and texture challenges; unstable
fraction splitting or global gain is insufficient. Use reported precursor
amounts and ratios as fixed constraints; never vary them to manufacture closure.
If coherent families and imbalance remain after exact-formula source challenges,
enumerate charge-balanced formulas including non-1:1 products, search records or
run

`python learned/stoichiometric_analogues.py FORMULA INDEX_JSON_GZ --cif-root CIF_ROOT`

Inspect several parents, justify substitutions, construct and health-screen the
model, then refine scale before cell. Re-challenge the watch list after every
inventory/profile rebuild.

## Use a reversible convergence loop

Make inactive phase terms genuinely neutral: size at least 10 micrometres,
strain zero, March ratio one and roughness zero. Fit a smooth background, scales,
cells, one angular correction and nonnegative low-dimensional U/W/X; release
SH/L only for repeated asymmetry. A collapsed/bound trial invalidates that
comparison: reload all saved values, not only flags, and reconverge. Retest a
meaningful boundary with complementary broadening. If all phase-width trials
collapse or bound, return to the common baseline and inventory rather than
advancing a topology decision.

From one saved checkpoint, repeatedly:

1. reopen common profile and angular correction;
2. for each phase compare neutral, size, strain and combined size-plus-strain,
   then symmetry-compatible anisotropy when hkl-family widths differ;
3. compare a few simple smooth background orders, polarization and roughness
   before low-index axial/diagonal March-Dollase texture.

After any accepted phase, source, geometry, intensity, texture or broadening
change, repeat until terms, fractions and source ranking survive another full
loop. For shared intensity, require a replayed angular trend across independent
phase families, stable fractions and no compensating high-angle/background
error. Covariance alone neither rejects such evidence nor retains a term.

Audit isolated low/middle/high-angle families using position, FWHM and left/right
half-width. Give every serious source its own symmetry-appropriate loop, anchored
also at the neutral checkpoint. A lower-symmetry source must beat the simpler
physical source both before and after elaboration. If ranking reverses, cross-seed
shared nuisance values, reopen each candidate's complete low-index axes, and
treat persistent disagreement as coupling unless observed positions/splittings
exclude the simpler source. Reject harmonic-texture and scale/background
surrogates.

## Freeze consistent outputs

Save, reopen and replay the full range. Prune unsupported terms, rerun CIF
health, and verify geometry. Parse `result.json`: each phase needs numeric
`weight_fraction`, an existing `cif_path`, and `project_path` naming `final.gpx`;
fractions must sum to one, and CIFs, fractions and `fit.csv` must agree with it.

Reusable package files are in learned/.
