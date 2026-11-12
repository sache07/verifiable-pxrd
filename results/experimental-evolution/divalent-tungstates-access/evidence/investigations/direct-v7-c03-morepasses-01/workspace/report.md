# Research diagnostic: coordinate-stabilization budget

This is an oracle-free post-hoc diagnostic, not a solver submission or a
reusable answer. It starts from the physical exact-inventory v6 c03 replicate
3 project and changes only the chemistry-agnostic helper's maximum coordinate
stabilization passes from three to five.

The original helper rejected all three coordinate orders solely because the
third coordinate pass had maximum shift/esd near 1.52. With the larger fixed
budget, each order converged on its fourth coordinate pass with maximum
shift/esd below 0.015, no frozen variables, stable positive fractions, and no
geometry or displacement violations. The selected phasewise branch has Rwp
1.85701%, compared with 3.43945% for the original physical checkpoint.

`final.gpx`, all CIFs, `fit.csv`, and `result.json` are exported from that exact
selected endpoint. Independent controller scoring is used only to test whether
the previously hidden structural discrepancy also improves; it does not feed
case-specific information back into the helper.
