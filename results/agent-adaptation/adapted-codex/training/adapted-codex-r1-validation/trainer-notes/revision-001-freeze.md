# Wave 1 assessment and selection

## Snapshot and panel

- Capability commit: `4701bedb466d970174c78c0fc0743ba486e3d99e`
- Capability SHA-256: `a2803fd4807ccea23915e368d3c23455f80b88156df81bb4b744979df3ccd5aa`
- Wave: `revision-4701bed-all-failures`
- Panel: all 20 baseline failures plus prior successes `vp-012`, `vp-014`, and `vp-029`
- Result: 9/23 selected exact and 9/23 candidates exact; no controller failures
- Budget used: 1 of the allowed 3 waves, 23 learned attempts, in addition to the 50-attempt baseline

## Prediction accounting

The element-specific periodic-realization contract engaged directly. `vp-002`, `vp-004`,
and `vp-049` converted from averaged or incorrectly decorated correct frameworks to exact
selected CIFs. Their traces explicitly separated ordered sites, tested finite element-to-site
assignments, and round-tripped full-occupancy CIFs. `vp-018` and the more complex `vp-045`
remained misses, so the note is helpful but not sufficient for every decoration problem.

The adapter changed DICVOL access as predicted. Twenty-one of 23 attempts invoked it in 30
native runs; the baseline had reached no valid `SEARCH OF` trace. Archived provenance contains
12 completed runs, four transparent backend-stop runs, and two explicit adapter timeouts (runs
written outside the archived workspace are not counted there). No malformed-header or file-open
failure recurred. In `vp-034`, the retained native run produced the decisive ~106.9 A^3
triclinic cell with M20 about 205, and the attempt converted to exact. `vp-005` and `vp-006`
also converted after successful adapter use, although the wave alone does not isolate causality.

Artifact behavior improved but not universally: 22/23 attempts declared 33 parseable CIFs,
and eight attempts materialized alternatives. `vp-037` moved from no CIF to three parseable
ordered CIFs, though all were structurally wrong. `vp-015` again timed out without a CIF because
it never accepted a physically valid model; this does not show a broken output interface.

All three regression probes remained selected exact. `vp-012` retained an explicit ordering
alternative, `vp-014` retained two ordered alternatives, and `vp-029` kept the correct primary.
The remaining misses were hard framework/coordinate searches or cases where the intended
contract had already engaged.

## Decision

Select `4701bedb466d970174c78c0fc0743ba486e3d99e` unchanged. A second unchanged wave would
mostly resample scientific search and would not test an observed mechanical defect. Adding
case-specific scientific advice would violate the minimal active surface and risk regression.
Freeze after final local checks with one of three allowed waves consumed.
