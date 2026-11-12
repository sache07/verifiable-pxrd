# Physical gates before stopping

Apply these additions to P0.

## Gate inventory and structures

For every likely retained source or adapted model, run

`python learned/cif_health.py CANDIDATE.cif [...]`

before fitting and on final CIFs. A `review` is not automatic rejection:
inspect disorder, occupancy and contacts chemically, then compare a passing
alternate record or physical analogue under the same restrained nuisance
model. Poor fit or zero scale rejects that record, not plausible chemistry.
Alternate records and polymorphs are competitors. Retain a new weak phase only
with positive replay-stable scale and at least two independent non-coincident
residual families. Same-composition coexistence additionally requires both
models to survive replacing/removing the other plus phase-broadening and
texture challenges; unstable fraction splitting or global gain is insufficient.

Use reported precursor amounts and ratios as fixed balance constraints; never
vary them to manufacture closure. If coherent residual families and imbalance
remain, enumerate a few charge-balanced formulas including non-1:1 products,
search exact records or run

`python learned/stoichiometric_analogues.py FORMULA INDEX_JSON_GZ --cif-root CIF_ROOT`

Inspect several parents, justify substitutions, construct and health-screen
the model, and refine scale before cell. Do not reject the leading
balance-motivated candidate before this matched-nuisance test. Keep plausible
weak phases on a watch list. After any phase/source change, reconverge
background, scales, cells, one angular correction and the common profile, then
re-challenge the watch list.

## Establish and act on profile evidence

Before profile or source decisions, make every inactive phase term genuinely
neutral: size at least 10 micrometres, strain zero, March ratio one and
roughness zero. Fit one angular correction and a nonnegative low-dimensional
U/W/X baseline; release SH/L only for repeated asymmetry.

A bound or collapsed branch invalidates that comparison. Reload the saved
pre-trial parameter values--do not merely disable refinement at trial values;
fixed values remain active physics--and reconverge a simpler baseline. For a
physically meaningful boundary, retest the term fixed at that boundary with
complementary phase broadening before deciding it is absent.

Judge adequacy from observed/calculated position, FWHM and left/right
half-width of isolated low/middle/high-angle families of the same phase plus a
smooth background, not from Rwp, interior values or covariance alone. If a
structured mismatch or high goodness-of-fit remains, do not promote a new
topology, polymorph or coexistence from that baseline. Recompare leading
physical source/analogue competitors under identical restored nuisance terms,
apply one targeted correction, replay, and repeat the audit.

Then compare size and strain from neutral values one phase at a time. Combine
complementary replay-stable terms; if hkl families differ, challenge
symmetry-compatible anisotropy. Compare coherent cross-phase angular trends
with background, polarization and roughness before texture. Covariance alone
does not reject a term: require independent angular/family support and fresh
replay, while rejecting scale/background surrogates. Compare no texture only
with symmetry-distinct low-index axial and diagonal March-Dollase models;
reject correlated high-order harmonic texture.

## Freeze consistent outputs

Save, reopen and replay the full range. Prune unsupported terms by value and
flag, rerun CIF health, and verify geometry. Parse `result.json`: each phase
needs numeric `weight_fraction`, an existing `cif_path`, fractions summing to
one, and `project_path` naming `final.gpx`; CIFs, fractions and `fit.csv` must
agree with that reopened project.
