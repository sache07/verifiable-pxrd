# b002 harder-supplement review

This is an explicitly outcome-selected learning supplement, not part of the original b001 prospective panel. The protocol trigger was met when P0 had already recovered more than three b001 cases. Existing b001 cases and results remain frozen.

Both cases reuse the audited b001 pool-r2 catalog (`b4ca51a...`) and therefore the same published/validated truth models. The common WO3 source is physical COD 2311041; every registered source and generated reference must pass the frozen physical screen before this batch is frozen.

## b002-c01: close the prototype loopholes

b001-c05 prospectively removed every exact and tier-1 match reported by `library_neighbours.py`, but two P0 solvers independently used FeWO4 COD 1567215, which the strict geometry matcher had rejected despite its wolframite prototype label. A third used the Zn0.85Cu0.15WO4 solid solution COD 9005254, whose fractional composition was outside the strict matcher's integer-formula comparison.

The complementary `audit_fractional_analogues.py` audit therefore applies an explicit boundary: withhold exact ZnWO4, every one-element ABO4 wolframite substitution, and every Zn-bearing W-O wolframite solid solution that can be purified without discovering a new target site. This adds triclinic CuWO4 COD 4000806 and the six Zn/Cd or Zn/Cu records 1520642, 1520643, 1520644, 9005252, 9005253 and 9005254. Zn-free ordered double tungstates remain available because mapping their two distinct A-site elements to Zn is a genuine tier-2 adaptation. The loose FeWO4 record 1567215 remains withheld from the observed b001 route. `neighbours-znwo4-r2.json` confirms that the strict matcher's nearest survivor remains tier-2 NbInO4 COD 1524100, with substitutions In->Zn and Nb->W, framework RMS 0.0106 and 4.2% cell mismatch. The 82 wt% hidden product and equimolar residual ZnO/WO3 preserve global Zn:W = 1:1.

## b002-c02: tier-2 hidden secondary

This escalates the original Mn secondary-intermediate design without using any c06 outcome: exact Mn3WO6 COD 2002703 and tier-1 Mn3TeO6 COD 2211528 are withheld. `neighbours-mn3wo6.json` confirms tier-2 Cd3TeO6 COD 2242674 as the nearest survivor, requiring Cd->Mn and Te->W substitutions, framework RMS 0.0297 and 5.68% cell mismatch. The complementary direct-route audit (`fractional-prototypes-mn3wo6.json`) finds no omitted close target-bearing or one-element route: the only close direct entries are exact COD 2002703 and Mn3TeO6 COD 2211528. Mn/W-bearing Sr2MnWO6 and Ba2MnWO6 are structurally distant double perovskites (framework RMS 0.446 and 0.483). Setting Mn3WO6 to 20 wt% makes omission detectable while leaving MnWO4 as the major phase; twice as many moles of WO3 as Mn3WO6 preserve global Mn:W = 1:1.

The cases use distinct measurement sessions, high counts, ordinary unknown angular/specimen effects and independent seeds. Generation audits will record oracle fit, fraction recovery, omission signal, physical screens and strict eligibility before freeze.

## Generation audit

The first preview used the pre-expansion c01 withholding set. Preview-r2 regenerated both cases after expanding c01 to 19 withheld records. Both cases remain strictly eligible, every symmetry-preserving reference perturbation passes the physical screen, and the deterministic profiles are unchanged. For b002-c01, oracle Rwp is 2.6324%, maximum fraction error is 0.000240, and omission signals are 20.570 (ZnWO4), 1.630 (ZnO), and 5.461 (WO3) noise units. For b002-c02, oracle Rwp is 1.9754%, maximum fraction error is 0.000246, and omission signals are 23.867 (MnWO4), 8.175 (Mn3WO6), and 10.786 (WO3) noise units. These checks establish detectability, not uniqueness against unenumerated structures.
