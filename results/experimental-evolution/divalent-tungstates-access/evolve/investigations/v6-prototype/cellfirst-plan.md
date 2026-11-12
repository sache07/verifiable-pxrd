# Prospective cell-first variant test

Recorded before dispatch and before any result from this variant was available.

## Motivation and hypothesis

The covariance-safe local-polish helper improved hidden D on six of eight
projects without harm, but returned baseline on the weakest exact-inventory
harder-Zn endpoint.  That endpoint's accepted major cell was still about 1.2%
from the hidden structure.  The original helper freezes cells while first
fitting coordinates, then allows only a 1% reciprocal-metric window during the
final settle.  Coordinate gradients against displaced reflections may
therefore be misleading before the cell can reach its basin.

`staged_polish_cellfirst.py` makes one mechanism change: each coordinate order
first converges cells, scales, and background, using a 4% relative window on
the reciprocal metric (roughly a 2% length tolerance near an orthogonal cell),
then runs the same coordinate rollback, geometry/fraction audit, material-gain
gate, and baseline fallback.  This is a generic transfer tolerance, not a
generator-derived range.

## Test and decision

Test the two exact-inventory harder-Zn failures, one b003 endpoint improved by
the original helper, and recovered c03/c06 controls.

- The variant is worthwhile only if it makes a materially larger hidden-D
  improvement on at least one harder-Zn endpoint, especially the original
  baseline-return case.
- It must not worsen either recovered control or introduce physical flags,
  phase-fraction collapse, bound-hit acceptance, or nonconvergence.
- If gains are confined to models already helped by the narrower procedure,
  retain the simpler tested helper.  If cell-first rescues the weak transfer
  basin without control harm, prefer it for v6 and repeat enough tests under
  the exact final hash to establish portability.
