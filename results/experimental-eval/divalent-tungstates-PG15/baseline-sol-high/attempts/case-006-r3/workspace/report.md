# PXRD phase analysis

The pattern is modeled as **triclinic CuWO4 (P -1)** with a small amount of **monoclinic WO3 (P 21/c)**. The refined crystalline-phase fractions are **97.91 wt% CuWO4** and **2.09 wt% WO3**, normalized to the modeled crystalline material.

## Evidence

The CuO + WO3 precursor chemistry and 800 °C treatment support copper tungstate formation, but phase assignment was based on the diffraction pattern. The strong lines at approximately 15.61, 19.32, 23.23/23.88/24.43, 26.27, 28.98, 30.44, and 31.94 degrees 2theta, together with the dense high-angle splitting, are indexed by the triclinic CuWO4 cell. Its refined cell is a = 4.710998 A, b = 5.845570 A, c = 4.883890 A, alpha = 91.65529 deg, beta = 92.53519 deg, gamma = 82.74856 deg.

A screen of CuO, Cu3WO6, and the available WO3 polymorphs found no positive CuO contribution and only a negligible, non-robust Cu3WO6 contribution. Room-temperature monoclinic WO3 was the best minor-phase model. Adding it reduced Rwp from 7.65% for CuWO4 alone to 7.17% in the jointly refined model and gave a positive scale corresponding to 2.09 wt%. The refined WO3 cell is a = 7.68914 A, b = 7.54551 A, c = 10.52421 A, beta = 136.0553 deg.

The final profile statistics are Rp = 5.22%, Rwp = 7.17%, Rexp = 2.43%, and goodness of fit = 2.95. The refined and calculated profiles in `fit.csv` cover 10.00-100.00 degrees 2theta.

## Remaining uncertainty

No pointwise standard uncertainties or calibrated instrumental profile were supplied, so sqrt(counts) weights and an empirical Cu K-alpha1/K-alpha2 profile were used. Formal fraction uncertainties from the least-squares covariance are about 0.06 wt% for WO3, but they do not include model, microabsorption, preferred-orientation, or instrumental systematic errors; a more realistic uncertainty for the minor phase is approximately +/-0.5 wt%. The large refined zero offset is correlated with absolute lattice scale, so the very small formal cell errors understate absolute-cell uncertainty.

CuWO4 Cu/O positions were refined while W was fixed to define the origin. For the ~2 wt% WO3 phase, atomic coordinates were retained from COD 2311041 and only its cell and scale were refined; its a, c, and beta values are weakly constrained because most WO3 peaks overlap CuWO4. Thus the WO3 phase identity and approximate fraction are supported, but detailed WO3 coordinates cannot be determined reliably from this pattern. Fractions exclude any amorphous material, which cannot be quantified without an internal standard.
