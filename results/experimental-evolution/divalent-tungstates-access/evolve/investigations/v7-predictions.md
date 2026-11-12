# Prospective cycle-3 v7 predictions

Recorded after fixing `packages/v7` and before freezing or launching any v7
solve. The active panel is b001-c03/c06, b002-c01/c02, b003-c01, and b004-c01.
Promotion remains the controller's fixed rule: three fresh solves per case,
aggregate delta at least `max(4, 2*noise)`, and no case mean more than 15 below
P0.

## Package-wide expectations

- All 18 slots should produce physical scored submissions.
- A solver that invokes the helper should do so once on its final physical,
  replay-stable checkpoint and should not mutate scientific parameters after
  it. The five-pass helper itself should introduce no physical regression.
- The narrow conditional topology rule should improve c06/harder-Mn route
  construction without triggering post-closure prototype sprawl on c03,
  b003, or b004.

## Frozen case gates

| Case | Prospective gates |
|---|---|
| b001-c03 | Exact physical four-phase inventory 3/3; recovery at least 2/3; mean score at least 75. |
| b001-c06 | R-3 Mn3WO6 selected at least 2/3; recovery at least 2/3; mean score at least 58. |
| b002-c01 | Exact physical ZnWO4/WO3/ZnO inventory 3/3; recovery at least 2/3; mean at least 65. |
| b002-c02 | Surviving R-3 Mn3WO6 route constructed at least 2/3 and selected at least 1/3; at least one recovery; mean at least 38. |
| b003-c01 | Exact physical inventory 3/3; at least one recovery; mean at least 52. |
| b004-c01 | Exact physical Ba3W2O9/WO3/BaCO3 inventory 3/3; recovery at least 2/3; mean at least 70. |

These mechanism gates do not replace the fixed promotion decision. Failure on
ordinary c03 or new b004 would be evidence that package attention or terminal
ordering harms already competent solving even if a hard topology case improves.

