Determine the crystalline phases and their weight fractions from inputs/pattern.csv. Read inputs/metadata.json for the chemical context and measurement information. The product composition and number of phases are unknown.

Use the available scientific tools to determine and refine a structural model for each phase. Save one CIF per phase, the combined observed/calculated/difference profile as fit.csv, and result.json listing each phase, its CIF path, its weight fraction normalized over the modeled crystalline phases, and the fit statistics. Explain the evidence and remaining uncertainty briefly in report.md; state when a structure or fraction cannot be determined reliably.

Save the final GSAS-II project used to produce your submitted CIFs, phase fractions and fit.csv as final.gpx.


# Converge chemistry and profile together

Apply these additions to P0.

## Gate inventory and structures

For every likely retained source or adapted model, run

`python learned/cif_health.py CANDIDATE.cif [...]`

before fitting and on final CIFs. A `review` requires chemical inspection and
comparison with a passing alternate record or physical analogue under matched
nuisance terms; poor fit or zero scale rejects that record, not plausible
chemistry. Treat alternate records and polymorphs as competitors. Retain a new
weak phase only with positive replay-stable scale and at least two independent
non-coincident residual families. Same-composition coexistence must also
survive replacing/removing either model plus broadening and texture challenges;
unstable fraction splitting or global gain is insufficient.

Use reported precursor amounts and ratios as fixed constraints; never vary
them to manufacture closure. If coherent residual families and imbalance
remain, enumerate a few charge-balanced formulas including non-1:1 products,
search exact records or run

`python learned/stoichiometric_analogues.py FORMULA INDEX_JSON_GZ --cif-root CIF_ROOT`

Inspect several parents, justify substitutions, construct and health-screen
the model, then refine scale before cell. Keep plausible weak phases on a watch
list and re-challenge them after every inventory/profile rebuild.

## Use a reversible convergence loop

Start from genuinely neutral inactive phase terms: size at least 10
micrometres, strain zero, March ratio one and roughness zero. Fit a smooth
background, scales, cells, one angular correction and a nonnegative
low-dimensional U/W/X profile; release SH/L only for repeated asymmetry. A
bound or collapsed trial invalidates that comparison: reload all saved
pre-trial values, not only refinement flags, and reconverge. Retest a physically
meaningful boundary fixed there with complementary broadening.

Treat profile selection as coordinate descent, not a one-pass checklist. From
the same saved checkpoint:

1. reopen the common profile and angular correction;
2. for each phase compare neutral, size, strain and combined size-plus-strain,
   then challenge symmetry-compatible anisotropy when hkl-family widths differ;
3. compare cross-phase intensity trends with background, polarization and
   roughness before low-index axial/diagonal March-Dollase texture.

After accepting any phase, source, geometry, shared-intensity, texture or
broadening change, repeat this loop. A previously rejected term may now be
complementary. Continue until another full loop leaves retained terms,
fractions and source ranking stable.

Audit isolated low/middle/high-angle families of each phase using position,
FWHM and left/right half-width. Structured mismatch or high goodness-of-fit
means the baseline is not adequate for topology decisions. Give every serious
source or polymorph its own neutral-to-converged, symmetry-appropriate loop.
A lower-symmetry model cannot win from Rwp alone: require observed diagnostic
splitting or families plus a physical, replay-stable advantage after equal
loops. Reject scale/background surrogates and correlated high-order harmonic
texture.

## Freeze consistent outputs

Save, reopen and replay the full range. Prune unsupported terms by value and
flag, rerun CIF health, and verify geometry. Parse `result.json`: every phase
needs numeric `weight_fraction`, an existing `cif_path`, and `project_path`
naming `final.gpx`; fractions must sum to one, and CIFs, fractions and
`fit.csv` must agree with that reopened project.

Reusable package files are in learned/.
