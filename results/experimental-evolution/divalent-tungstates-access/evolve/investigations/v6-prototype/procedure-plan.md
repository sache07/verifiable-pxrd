# Prospective staged-polish procedure test

Recorded after dispatch and before any procedure result was available.

## Hypothesis

After a solver has closed a physical phase inventory, part of the remaining
variance comes from GSAS-II coordinate-order and bound handling rather than
phase discovery.  A reusable final-stage helper should improve accepted models
by comparing a few bounded refinement orders, rolling every clipped atom back,
and returning the original checkpoint when no converged, physical branch makes
a material observed-profile gain.

## Frozen test

`ptest-v6-staged-closed-01` uses script SHA-256
`2246b8ccea3e6297914b5f7386bb1b580e233ecc8907e19a04d83ebcb91d3a77` on:

- four exact, physical full-reference R-3 endpoints that missed recovery;
- two exact-inventory harder-Zn endpoints with weak transferred-framework
  completion; and
- one recovered c03 and one recovered c06 endpoint as no-harm controls.

The controller independently replays and scores outputs.  These are
oracle-informed diagnostics, not fresh-rollout validation.

## Decision criteria

- Every selected output must retain its phase inventory, pass the physical
  screen, avoid fraction collapse, and finish without frozen variables.
- A useful mechanism should lower hidden D on a majority of the six failed
  endpoints, not merely lower observed-pattern Rwp.  Improvement should occur
  beyond the two local b003 projects used while developing the script.
- Neither recovered control should lose recovery; a control D increase above
  0.1 is a meaningful no-harm failure.
- If harder-Zn outputs return baseline or remain essentially unchanged, the
  current helper is only a narrow b003 polish and is insufficient as the final
  cycle-2 candidate without a revised mechanism and another isolated test.
- If gains generalize while controls are preserved, v6 should pair the helper
  with only v5's concise closure/physical-checkpoint guidance.  It should not
  inherit v4's unsuccessful formula/topology coverage rule.
