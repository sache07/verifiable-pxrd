# v7 design and prospective screen predictions

v7 replaces v6's 331-word guidance with a 296-word evidence-checkpoint
version. It retains the unchanged generic analogue helper (SHA-256
`0d58e24b4c66dfc7d43567767635c32522c40d000b584912343304844794e5b8`)
and uses guidance SHA-256
`6f07978d376e90f63bbac49c1662cc7fab8860bea732e15144cedda26c7387b6`.
No case identity, hidden fraction, coordinate, source lookup, or fitted value is
encoded.

## Evidence for the replacement

The v6 source/analogue/watch-list loop transferred strongly to b002-c02: three
different ordered scheelite parents produced physical complete four-phase
projects with scores 84.30--85.61. That behavior is preserved but compressed.
The active failures have a different common mechanism. Solvers repeatedly call
a profile adequate without recording family-wise numerical peak-width evidence
(b001 c03--c06 and b002-c01 r2), while one c05 rollout never formulates the
missing cation-rich stoichiometry. The b002-c01 partial also proves that generic
“project/export agreement” does not guarantee the required JSON field names.

v7 therefore adds only three checkpoints:

1. use precursor element/charge balance to formulate a small set of missing
   non-1:1 products before analogue search;
2. record observed/calculated position, FWHM and left/right half-width at
   low/middle/high angle before accepting the profile, then require size,
   strain or anisotropy branches from the same baseline when the table shows a
   directional mismatch;
3. parse the final output and assert literal numeric `weight_fraction` fields,
   unit sum, existing CIF paths, and exact reopened-project agreement.

No new executable helper is added. A general GSAS-II peak-audit helper would be
larger and more brittle than the behavioral checkpoint, and the solvers already
demonstrated they can calculate these diagnostics.

## Prospective initial-screen predictions

- b002-c02 should remain above 80 with a complete physical inventory; this is
  the principal regression control for shortening the source prose.
- b002-c01 should retain all three phases, emit a valid quantified submission,
  and use the numerical audit to avoid the single-isotropic-strain basin.
- b001-c03, c04 and c06 should retain their already robust inventories while
  more consistently testing the required anisotropic/phase-width family.
- b001-c05 should invoke balance-led missing-formula generation and recover the
  off-stoichiometric phase before profile refinement.

The initial screen is one fresh v7 solve on all six active cases. A successful
screen requires physical complete inventories and scores in the 80+ range with
small allowance for rollout noise. Any failure will be diagnosed for actual
checkpoint adherence; subsequent versions will replace failed wording and run
only unresolved cases before a complete validation screen.
