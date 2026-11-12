# b003 full-reference Mn3WO6 transfer review

## Prospective role

This one-case transfer batch opens development cycle 2. It is a near-matched, easier control for the unresolved manganese secondary phase rather than an outcome-selected variant of a private realization. The phase recipe is fixed at 63.23 wt% MnWO4, 18.00 wt% R-3 Mn3WO6, and 18.77 wt% WO3. These fractions preserve the equimolar Mn:W precursor balance expected from WO3 + Mn3O4 by pairing every cation-rich Mn3WO6 contribution with the required residual WO3. The secondary abundance lies between the 15.46 wt% tier-1 case and 20.00 wt% tier-2 case.

The main experimental variable is reference availability. Exact published Mn3WO6 COD 2002703 remains available here, whereas b001-c06 withholds it and leaves tier-1 Mn3TeO6, and b002-c02 additionally withholds Mn3TeO6 and leaves tier-2 Cd3TeO6. A new seed and measurement session create an independent profile while retaining high counts and ordinary unknown specimen, angular, texture, and profile effects. This forms a full-reference/tier-1/tier-2 ladder without changing the target topology; the modest abundance difference prevents duplicate transfer content and keeps omission detectability comparable.

The source pool is the already audited clean b001 pool-r2 catalog (`b4ca51a...`). Its truth models are ordered and physical; in particular, the WO3 source is COD 2311041 rather than the historically problematic COD 1528915. Mn3WO6 COD 2002703 is the published R-3 manganese(II) oxotungstate, and its registered shortest separation is 1.903 A.

## Prospective predictions

- The generation audit must be strictly eligible, recover all fractions to the frozen oracle tolerance, and give the 18.00 wt% Mn3WO6 omission a clearly detectable signal.
- With P0 and the exact reference available, at least two of three fresh solves should select R-3 Mn3WO6, at least one should meet formal recovery, and the mean should exceed the tier-1 P0 mean of 22.11 by at least 20 score points.
- If exact-reference P0 still misses R-3 in most runs, the bottleneck is residual-family recognition or search persistence rather than analogue retrieval. If it reliably selects R-3 while tier-1/tier-2 cases do not, topology-preserving reference transfer is the primary bottleneck.

The seed, recipe, thresholds, and predictions above were fixed before generating the accepted private specimen realization.

## Generation audit

The revised transfer-valid realization in `preview-r2/` is strictly eligible. The frozen oracle refinement gives Rwp 1.4088% and a maximum phase-fraction error of 0.000344. Omission signals are 19.632 noise units for MnWO4, 6.089 for Mn3WO6, and 9.810 for WO3. Thus all three phases are independently detectable in the known-structure/background audit, with the target secondary comfortably above noise. These checks establish quantitative detectability and physical generation consistency, not uniqueness against unenumerated structures.

The initial draft used the exact b001-c06 structures and fractions with a new seed. Its realization was strictly eligible, but controller request `freeze-b003` rejected it before freezing because transfer batches cannot reuse an existing mixture merely as a measurement/resource variant. That unaccepted preview remains in `preview/` for provenance and is not a frozen case. The revised 18 wt% design and new seed were chosen from the stoichiometric ladder, not from the rejected realization's profile.

## Prospective P0 result

The frozen three-run transfer comparison completed at 46.58†, 41.94†, and 48.73 (D 2.484, 3.707, and 2.786; independent Rwp 2.643%, 3.089%, and 2.776%), for a mean score of 45.75. Exact COD 2002703 R-3 Mn3WO6 was selected 3/3 at 18.18, 17.87, and 17.98 wt%, and every run recovered the correct three formulas with near-truth fractions. Thus the prospective R-3 selection and mean-above-42.11 predictions pass. Formal recovery was 0/3, so that prediction fails.

The outcome separates topology recognition from downstream execution. Reps1/2 knowingly retained short-contact WO3 COD 1528915 and require physical adjudication; clean COD 2311041 was only 0.049 and 0.124 Rwp percentage points worse at their matched checkpoints. Rep3 rejected the flagged model, submitted the exact physical three-framework inventory with maximum fraction error 0.079 percentage point, and still stopped at D 2.786 because site/profile/calibration completion remained imperfect. Full-reference R-3 recognition is therefore reliable, but physical same-formula selection and ordinary post-closure refinement are independent bottlenecks. The completed comparison opened development cycle 2.
