# v11 c03 source-loop diagnosis

## Outcome

v11 scored 71.8715 with a physical, exact-formula SrWO4/WO3/SrCO3 inventory,
`D = 0.31096`, and fresh atomic `Rwp = 3.2713%` versus the 2.851% noise
floor. Fractions were 61.889/23.556/14.554 wt%, with maximum absolute error
2.833 percentage points. The structural score fell to 65.26 because the solver
selected triclinic P-1 WO3 rather than the generating monoclinic P21/c model.

## Matched historical control

The v6 c03 solve selected monoclinic WO3 and scored 83.7632 (`D = 0.14215`,
fresh atomic `Rwp = 3.0390%`). Its fractions were 60.514/24.186/15.300 wt%,
with maximum error 1.458 points and structural score 78.08.

| Decision | v6 | v11 |
|---|---|---|
| Neutral source ranking | monoclinic 6.475% vs triclinic 7.304% Rwp | not retained as a veto; ranking reversed after separate loops |
| Final WO3 | monoclinic P21/c | triclinic P-1 |
| SrWO4 texture | [111], ratio 0.7005 | [110], ratio 0.7407 |
| WO3 texture | [10-1], ratio 1.3050 | [001], ratio 1.3207 |
| WO3 broadening | uniaxial strain along monoclinic b | uniaxial strain along triclinic [010] |
| Finite size | pruned for all phases | pruned at the neutral 10 micrometre boundary for all phases |
| Common profile | six-term background, W/X, shift; roughness/polarization pruned | 14-term background, W/X, polarization, shift; roughness pruned |

Both paths omit the true finite sizes, so that omission alone cannot explain
the source error. The decisive difference is path-dependent coupling. v6 first
ranked sources under a simple neutral nuisance model, retained monoclinic, then
replayed texture and anisotropic width alternatives. v11 allowed independently
elaborated loops to overturn that source ranking: a coupled SrWO4 [110] strain/
texture basin plus extra triclinic metric freedom generated apparent split-family
evidence and a 3.27% endpoint versus 4.05% for its underfit monoclinic endpoint.

The lower-symmetry endpoint is internally converged but not robust evidence of
the polymorph. A reusable guard should require a lower-symmetry candidate to
beat the simpler physical candidate at both a neutral low-dimensional checkpoint
and after converged loops. If ranking reverses only after candidate-specific
texture/broadening, cross-seed the finalists' shared nuisance basis, reopen the
complete symmetry-appropriate axis set from multiple saved starts, and treat a
remaining disagreement as unresolved coupling. Also restore v6's instruction
to return to the baseline/inventory when all phase-width trials collapse or hit
bounds. Finite-size multi-starts may improve adequacy, but are secondary to the
rank-reversal guard demonstrated here.
