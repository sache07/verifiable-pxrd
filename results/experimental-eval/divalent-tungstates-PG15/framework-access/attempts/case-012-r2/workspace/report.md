# Powder XRD phase analysis

The crystalline product is modeled as **NiWO4 (wolframite, P2/c)** plus residual **WO3 (monoclinic, P2_1/c)**. The refined crystalline-phase fractions are 76.37(15) wt% NiWO4 and 23.63(15) wt% WO3; the parenthesized values are formal one-standard-deviation scale uncertainties. A more realistic uncertainty, including background, profile and structural-model choices, is about 1 wt% absolute. These fractions are normalized over the modeled crystalline material only; this scan does not determine an amorphous fraction.

## Evidence

The dominant NiWO4 model accounts for the diagnostic reflections near 15.59, 19.19, 23.91, 24.85, 30.87, 31.48 and 36.52 degrees 2theta. The residual WO3 model accounts for the 23.06/23.53/24.28-degree triplet and peaks near 26.53, 28.82 and 33.2--34.1 degrees. Refined cells are a = 4.59777, b = 5.65991, c = 4.90759 A, beta = 89.9704 degrees for NiWO4, and a = 7.29869, b = 7.52943, c = 10.5227 A, beta = 133.094 degrees for WO3.

Several ambient WO3 references were tested. A triclinic P-1 model gave a comparable unconstrained fit, but its cell had to move toward a monoclinic metric by more than the expected reference variation. The P2_1/c model achieved the better restrained fit with fewer independent atomic coordinates and is therefore selected. NiWO4 was refined from a repaired P2/c wolframite reference. Atomic coordinate shifts were limited to modest reference-model deviations; oxygen coordinates remain less certain than the heavy-atom framework because of weak oxygen X-ray scattering and peak overlap.

A diagnostic NiO phase refined to only about 0.14(8) wt% (less than two standard deviations), and its strongest expected reflections were not independently resolved. NiO is therefore not included; a conservative detection limit is approximately 0.5 wt%.

## Fit and limitations

Independent zero-optimization replay of `final.gpx` over all 8,282 measured points gives Rwp = 4.0785%, Rp = 3.1799%, chi-square = 11,383.63 and goodness of fit = 1.1763 using weights 1/max(counts, 1). The replay reports no negative-background, negative-width, displacement-parameter or polarization warnings, and both exported structures pass the contact/occupancy screen.

The main remaining ambiguity is the near-pseudosymmetric WO3 polymorph assignment; P2_1/c is favored, but powder data alone do not make the closely related low-symmetry alternative mathematically unique. The reported oxygen positions should be treated as reference-guided refinements rather than an independent structure solution.
