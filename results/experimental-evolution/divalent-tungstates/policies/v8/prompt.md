Determine the crystalline phases and their weight fractions from inputs/pattern.csv. Read inputs/metadata.json for the chemical context and measurement information. The product composition and number of phases are unknown.

Use the available scientific tools to determine and refine a structural model for each phase. Save one CIF per phase, the combined observed/calculated/difference profile as fit.csv, and result.json listing each phase, its CIF path, its weight fraction normalized over the modeled crystalline phases, and the fit statistics. Explain the evidence and remaining uncertainty briefly in report.md; state when a structure or fraction cannot be determined reliably.

Save the final GSAS-II project used to produce your submitted CIFs, phase fractions and fit.csv as final.gpx.


# Physical gates before stopping

Apply these additions to P0.

## Gate the inventory and structures

For every likely retained source or adapted model, run

`python learned/cif_health.py CANDIDATE.cif [...]`

before fitting and on final CIFs. A `review` is not automatic rejection:
inspect the reported disorder/occupancy and contacts in chemical context, then
compare a passing alternate record or physical analogue under the same
restrained nuisance model. Retain a reviewed structure only with a documented
chemical reason. Poor fit or zero scale rejects that record, not plausible
chemistry. Alternate records/polymorphs are competitors, not simultaneous
phases, unless independent unique families require coexistence.

Make a precursor element/charge balance. If coherent residual families and an
imbalance remain, enumerate a few charge-balanced formulas including non-1:1
products; search exact records or run

`python learned/stoichiometric_analogues.py FORMULA INDEX_JSON_GZ --cif-root CIF_ROOT`

Inspect several parents and physical-screen substitutions. Keep plausible weak
phases on a watch list. After any phase/source change, reconverge background,
scales, cells, one angular correction and the common profile, then re-challenge
the watch list.

## Establish and act on profile evidence

Before profile decisions, set every inactive phase term genuinely neutral:
size at least 10 micrometres, strain zero, March ratio one, and roughness zero.
Turning refinement off does not neutralize GSAS-II's active 1 micrometre/1000
ppm defaults. Fit a nonnegative low-dimensional U/W/X baseline; release SH/L
only for repeated asymmetry.

Numerically spot-check observed/calculated position, FWHM and left/right
half-width for representative isolated low/middle/high-angle families. If a
structured mismatch or goodness-of-fit materially above counting expectation
remains, do not finish: from the same saved baseline test at least one targeted
cause (source/inventory, common profile/angular model, or phase size versus
strain/compatible anisotropy), replay, and repeat the check. Compare
background, polarization and roughness before texture; retain only
complementary replay-stable terms.

## Freeze consistent outputs

Save, reopen and replay the full range after accepted changes. Prune unsupported
or bound terms by value as well as flag, rerun the CIF health report, and verify
geometry. Parse `result.json`: each phase needs numeric `weight_fraction`, an
existing `cif_path`, fractions summing to one, and `project_path` naming
`final.gpx`; CIFs, fractions and `fit.csv` must agree with that reopened project.

Reusable package files are in learned/.
