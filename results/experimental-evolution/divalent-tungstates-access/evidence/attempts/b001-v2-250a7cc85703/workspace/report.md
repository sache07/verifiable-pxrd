# Powder XRD phase analysis

The pattern is best described by four crystalline phases. Fractions are normalized over those modeled crystalline phases only.

| Phase | Space group | Refined cell (angstrom, degrees) | Weight fraction |
|---|---|---|---:|
| CuWO4 | P -1 | a=4.61997, b=5.74547, c=4.85756; alpha=91.3252, beta=91.4807, gamma=84.7021 | 65.62% |
| WO3 | P 21/n | a=7.29670, b=7.55671, c=7.68133; beta=90.9678 | 18.83% |
| CuO | C 2/c | a=4.66682, b=3.42930, c=5.11944; beta=99.5441 | 2.49% |
| Cu3WO6 | P a -3 | a=9.78793 | 13.06% |

## Evidence and refinement

The starting models were COD 4000806 (CuWO4), 1528915 (WO3), 1011194 (CuO), and 1527404 (Cu3WO6). CuWO4 accounts for the dominant pattern; the characteristic WO3 multiplet and CuO lines require stable positive scales. Coherent residual peaks near 15.2, 19.8, 32.5, and 33.8 degrees identify cubic Cu3WO6. In the initial common-state test, adding Cu3WO6 with the other phases and nuisance terms fixed reduced Rwp from 18.50% to 14.88% and its scale remained positive. It remained at 13.06 wt% after ordinary joint refinement.

The final GSAS-II Rietveld model uses the supplied Cu K-alpha1/alpha2 doublet and the full 9.9034-100.0946 degree grid. Refined terms include phase scales and cells, a positive 30-term Chebyshev background, specimen-height shift and zero, polarization, physically bounded peak broadening, limited preferred orientation, and tightly bounded symmetry-preserving coordinates. A fresh native replay of `final.gpx`, ignoring saved calculated arrays and optimizing no parameters, gives Rwp=3.82490%, chi-square=46488.73, and GOF=2.37525 for 8301 observations and 61 refined parameters. The replay produced no profile-review flags; its observed, calculated, and observed-minus-calculated arrays are in `fit.csv`.

Residual-directed tests were performed in the common four-phase state. Exact Cu2WO4 and Cu2O precursor/product candidates collapsed to zero scale. Same-stoichiometry Cu2WO4 transfers based on Ag2WO4 (Pnn2), Na2WO4 (Fd-3m), Li2WO4 (C2/c, I41/amd, R-3), and Cu2GeO4 (I41/amd) either collapsed or gave only boundary-dependent traces. Alternative Cu3WO6 transfers from Ca3WO6 (P21/c), Mn3WO6 (R-3), and Cu3TeO6 (Ia-3), and alternate CuWO4/WO3/CuO polymorphs, fit substantially worse in replacement tests. A Cu4O3 trial and two transferred Cu2WO4 models produced at most about 0.1-0.4 wt% with unstable extreme profile parameters. Their identity and fractions cannot be determined reliably, so no fifth crystalline phase is reported.

## Physical screen and uncertainty

All submitted CIFs have full occupancies, nonnegative isotropic displacement parameters, and pass the contact screen. The historical WO3 parent coordinates contained a 1.59 angstrom O5-O6 contact; the two sites were moved symmetrically by approximately 0.11 angstrom each, the minimum repair giving a 1.82 angstrom contact. This changed full-grid Rwp by only 0.046 percentage point. Consequently, the WO3 phase assignment, cell, and scale are robust, but its detailed oxygen geometry is less certain than the cation framework.

The scale fractions are model-dependent nominal values, not absolute total-sample fractions. No amorphous fraction can be obtained from these data, and zero/specimen displacement are highly correlated. Systematic profile, texture, and background choices therefore dominate the formal least-squares precision, especially for the 2.49 wt% CuO phase and any sub-0.4 wt% trace component.
