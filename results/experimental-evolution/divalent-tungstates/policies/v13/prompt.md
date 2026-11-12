Determine the crystalline phases and their weight fractions from inputs/pattern.csv. Read inputs/metadata.json for the chemical context and measurement information. The product composition and number of phases are unknown.

Use the available scientific tools to determine and refine a structural model for each phase. Save one CIF per phase, the combined observed/calculated/difference profile as fit.csv, and result.json listing each phase, its CIF path, its weight fraction normalized over the modeled crystalline phases, and the fit statistics. Explain the evidence and remaining uncertainty briefly in report.md; state when a structure or fraction cannot be determined reliably.

Save the final GSAS-II project used to produce your submitted CIFs, phase fractions and fit.csv as final.gpx.


# Close the coupled basis before selecting

Apply these additions to P0.

## Gate inventory and sources

For every retained or adapted source run

`python learned/cif_health.py CANDIDATE.cif [...]`

before fitting and on final CIFs. Health pass checks geometry, not whether one
record represents the observed polymorph. If the first record for a
context- or balance-plausible exact formula fits poorly or collapses, compare
at least one structurally distinct physical record or polymorph when available
before excluding that formula or constructing an analogue. Poor fit rejects
the record, not plausible chemistry; alternate records compete rather than
coexist.

Retain a weak phase only with positive replay-stable scale and at least two
independent non-coincident families. Same-formula coexistence must additionally
survive replacing/removing either model plus broadening and texture challenges.
If coherent families and imbalance remain after exact-formula challenges,
enumerate charge-balanced formulas including non-1:1 products, then run

`python learned/stoichiometric_analogues.py FORMULA INDEX_JSON_GZ --cif-root CIF_ROOT`

Inspect several parents, justify substitutions, construct and health-screen
the model, and refine scale before cell. Re-challenge the watch list after each
inventory/profile rebuild. Use reported precursor amounts only as fixed data;
never vary them to manufacture closure.

## Converge a complete coupled basis

Make inactive terms literal: size at least 10 micrometres, strain zero, March
ratio one and roughness zero. Fit a smooth background, scales, cells, one
angular correction and nonnegative low-dimensional U/W/X; release SH/L only
for repeated asymmetry. A collapsed or bound trial invalidates that comparison:
reload every saved value and flag, then reconverge.
If every phase-width branch collapses, return to the common baseline and
inventory rather than advancing a topology decision.

From one checkpoint, repeatedly reopen common profile/angular terms; compare
each phase's neutral, size, strain and combined size-plus-strain models; then
test symmetry-compatible anisotropy and simple March-Dollase texture. Generate
the complete set of symmetry-inequivalent simple low-index axes: one diagonal
does not represent the others. Include equal- and unequal-index diagonals and
sign-distinct directions whenever symmetry does not equate them.

After the phasewise pass, perform one collective release of all phase sizes and
strains that showed family-level support or traded against common widths, from
low physical seeds while reopening U/W/X. An early one-at-a-time boundary does
not veto a term in this joint test. From an interior replay-stable collective
solution, delete each term separately; retain only terms whose deletion leaves
coherent width error. Restore the checkpoint if collective branches bind,
collapse or fail independent reseeds.

After any accepted source, inventory, intensity, texture or width change,
repeat until terms, fractions and source ranking survive a full loop. Compare
simple backgrounds, polarization and roughness using angular trends across
independent phase families, stable fractions and absence of compensating
high-angle/background error; covariance alone neither retains nor rejects.

Give every serious source the same complete-axis and collective-width loop at
neutral and elaborated checkpoints. Lower symmetry must win both. On rank
reversal, cross-seed shared nuisance values; without diagnostic positions or
splittings, prefer the simpler physical source.

## Freeze consistent outputs

Save, reopen and replay the full range. Prune unsupported terms, rerun CIF
health and verify geometry. In `result.json`, every phase needs numeric
`weight_fraction`, an existing `cif_path`, and `project_path` naming
`final.gpx`; fractions sum to one, and CIFs, fractions and `fit.csv` agree.

Reusable package files are in learned/.
