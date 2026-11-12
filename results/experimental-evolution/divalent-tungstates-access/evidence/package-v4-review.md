# v4 package review

## Intervention

v4 is a guidance-only candidate for cycle 2. It keeps the useful part of v3—stop structural search after reflection-family closure and finish accepted models—but repairs two observed failure modes.

First, reaction-balanced formula enumeration did not ensure topology coverage. Across three harder-Mn v3 runs, the submitted secondary phases were C2/c Mn3WO6, P21/c Mn2WO6, and P21/c Mn2WO5. The final run screened 136 A2BO5 frameworks while never constructing the surviving R-3 Cd3TeO6-derived Mn3WO6 route. v4 therefore ranks formulas by the whole-mixture precursor balance, keeps one chemically close physical parent per distinct symmetry/coordination topology, and covers those families before deep optimization. This is controlled diversity, not a broader exhaustive search.

Second, exact-inventory c03 runs still regressed because optional candidate work and weak final convergence displaced ordinary refinement. v4 asks for a complete physical replayable checkpoint early, stops all reference/prototype search at closure, and returns to staged coordinate/profile refinement. It explicitly preserves the best complete replay rather than submitting the last attempted branch. The completed b003 transfer adds a replicated same-formula selection failure: two runs chose flagged WO3 for only 0.049/0.124 Rwp-point checkpoint gains. v4 therefore makes physical geometry the near-tie rule. The third run chose clean WO3 and exact fractions but remained unrecovered, confirming that staged ordinary refinement is a separate target.

The package contains 303 guidance words and no executable helper. It includes no case identifiers, structures, coordinates, fractions, private effects, or lookup rules. The main risk is that topology coverage still consumes attention on already-closed ordinary cases; the early checkpoint and family trigger are intended to contain that risk.

## Prospective active-panel predictions

- b001-c02: at least 2/3 recover and mean is no more than 10 points below P0.
- b001-c03: exact inventory 3/3, at least 2/3 recover, and mean at least 69.12.
- b001-c06: R-3 selected at least 2/3, at least one recovery, and mean at least 42.11.
- b002-c01: exact inventory 3/3, at least 2/3 recover, and mean at least 57.28.
- b002-c02: surviving R-3 topology constructed at least 2/3, at least one recovery, and mean at least 41.50.
- b003-c01: exact R-3 selected 3/3, the full physical framework inventory at least 2/3, at least one formal recovery, and mean at least 50.00 versus P0 45.75.
- Package level: meet the fixed promotion rule over all six cases.

## Transfer evidence

`b003-transfer` completed at 46.58†/41.94†/48.73, mean 45.75, with exact R-3 selection 3/3 but recovery 0/3. Reps1/2 selected flagged WO3; rep3 selected clean WO3 and exact fractions yet remained profile-limited. The prospective comparison is complete, cycle 2 is open, and the predictions above are now frozen before any v4 solve.
