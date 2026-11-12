# c06 replicate-1 R-3 metric diagnostic

This is a bounded, case-specific oracle-informed mechanism diagnostic, not a
reusable solver package or a blind answer-recovery route.

The control and intervention clone the same c06 replicate-1 three-phase R-3
project and run the same deterministic cell/profile workflow. The control
retains the attempt's source-derived R-3 metric. The intervention changes only
the R-3 initialization to the independently indexed metric before refinement.

At the last explicitly accepted matched checkpoint
(`round2_phase0_size`):

| Branch | Rwp (%) | R-3 weight fraction (%) |
|---|---:|---:|
| Control | 15.436665 | 7.3904 |
| Indexed-metric seed | 4.405494 | 14.8405 |

The matched initialization change therefore lowers Rwp by 11.031171 points
and restores a substantial R-3 contribution before any answer-specific
coordinate substitution. Both long workflows were terminated by the command
time limit during later profile trials. Their mutable `control.gpx` and
`indexed.gpx` endpoints are consequently unadjudicated; the named accepted
checkpoint files above are the evidential comparison.

Conclusion: the original R-3 branch's metric basin is sufficient to explain
its false rejection. Reusable guidance may require symmetry-compatible
observed-metric seeding and matched development, but must not contain this
case's cell values, coordinates, fractions or source-specific answer.
