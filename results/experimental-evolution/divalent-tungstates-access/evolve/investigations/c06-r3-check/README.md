# b001-c06 R-3 route counterfactual

This diagnostic replays the Mn3WO6 model constructed from the surviving R-3 Mn3TeO6 parent in P0 attempt `b001-p0-1823ec999d12`. It tests a mechanism; it is not a reusable package component or a submitted solve.

The original comparison stopped before this candidate. A literal replay additionally exposed hard-coded phase-index behavior: a preceding wrong candidate remained active, the correct candidate was added at zero scale, and later refinement targeted the wrong phase index. The corrected replay disables legacy candidates by identity, initializes the new phase from the common active candidate scale, and widens symmetry-independent reciprocal-cell bounds from 1.2% to 3%.

The corrected branch reached Rwp 5.359, refined a=b=8.8924 and c=10.4769 A, and recovered 14.5 wt% Mn3WO6 versus 15.46 wt% truth. This validates the analogue route while leaving a substantial profile/coordinate-refinement gap to the oracle Rwp 1.808.
