# Close a valid model before expanding

Apply these additions to P0.

## Gate inventory and sources

For every retained or adapted source run

`python learned/cif_health.py CANDIDATE.cif [...]`

before fitting and on final CIFs. Health pass checks geometry, not whether a
record represents the observed polymorph. If the first record for a context- or
balance-plausible exact formula fits poorly or collapses, compare at least one
structurally distinct physical record when available before excluding that
formula or constructing an analogue. Poor fit rejects the record, not plausible
chemistry; alternate records compete rather than coexist.

Retain a weak phase only with positive replay-stable scale and at least two
independent non-coincident families. Same-formula coexistence must additionally
survive replacing/removing either model plus broadening and texture challenges.
If coherent families and imbalance remain after exact-formula challenges,
enumerate charge-balanced formulas including non-1:1 products, then run

`python learned/stoichiometric_analogues.py FORMULA INDEX_JSON_GZ --cif-root CIF_ROOT`

Inspect several parents, justify substitutions, construct and health-screen the
model, and refine scale before cell. Use reported precursor amounts only as
fixed data; never vary them to manufacture closure.

## Converge once, then test focused alternatives

Make inactive terms literal: size at least 10 micrometres, strain zero, March
ratio one and roughness zero. Fit a smooth background, scales, cells, one
angular correction and nonnegative low-dimensional U/W/X; release SH/L only for
repeated asymmetry. A collapsed or bound trial invalidates that comparison:
reload every saved value and flag, then reconverge.

As soon as a complete physical inventory has a replay-stable model, save and
export a schema-complete checkpoint. Optional challenges may improve it, but
must not leave the run without a valid deliverable.

At one mature checkpoint, reopen common profile/angular terms. For each phase
compare neutral, size, strain and combined size-plus-strain. Then perform one
collective low-seed release of phase widths that showed family-level support or
traded against common widths, followed by one-term deletions. Restore the mature
checkpoint if joint branches bind, collapse or fail independent replay.

Test texture with a compact symmetry-aware basis: principal axes, an equal-index
diagonal, an unequal-index diagonal, and a sign partner only when symmetry does
not equate it. If one phase retains coherent directional residuals and has no
clear leader, expand that phase once to nearby simple axes. Do not enumerate
every primitive direction or restart complete axis sets after each change;
replay the leader and its neutral deletion instead.

Give serious source competitors the same compact basis. A decisively poorer
source stops after that matched comparison. Lower symmetry must win both the
neutral and compact elaborated checkpoints; on a near tie, cross-seed shared
nuisance values. Equal opportunity does not require exhaustive parity that
cannot change the topology decision.

Compare simple backgrounds, polarization and roughness using angular trends
across independent phase families, stable fractions and absence of compensating
high-angle error. After an accepted change, reopen common terms and recheck only
the affected term plus retained leaders. One stabilization pass is sufficient;
preserve the valid checkpoint when optional uncertainty remains.

## Freeze consistent outputs

Save, reopen and replay the full range. Prune unsupported terms, rerun CIF
health and verify geometry. In `result.json`, every phase needs numeric
`weight_fraction`, an existing `cif_path`, and `project_path` naming
`final.gpx`; fractions sum to one, and CIFs, fractions and `fit.csv` agree.
