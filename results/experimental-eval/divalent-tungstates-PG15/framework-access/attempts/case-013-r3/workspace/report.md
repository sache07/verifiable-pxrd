# Powder XRD phase analysis

The Cu K-alpha pattern is best represented by six crystalline components. Fractions below are normalized over those modeled crystalline phases; the data do not determine an amorphous fraction.

| Phase model | Space group | Refined wt% | Assessment |
|---|---:|---:|---|
| PbWO4, scheelite | I 41/a | 58.11(18) | Secure |
| WO3, monoclinic | P 21/c | 10.55(15) | Secure |
| PbO, massicot | Pbcm | 8.29(10) | Secure |
| PbO, litharge | P 4/nmm | 7.75(12) | Secure |
| Pb2WO5 analogue | C 2/m | 11.27(14) | Probable phase; oxygen coordinates/model are analogue-based |
| PbWO4, fluorite-type cubic model | F m -3 m | 4.04(9) | Cubic lattice secure; composition and atomic model tentative |

Parenthesized errors are the formal one-standard-deviation scale uncertainties from the final least-squares cycle, in wt%. They do not include phase-model, background, preferred-orientation, or profile systematic error, so the meaningful uncertainty is larger, especially for the final two components.

## Evidence

The dominant reflection set and refined tetragonal cell (a = 5.46810 A, c = 12.07090 A) identify scheelite PbWO4. Full-pattern matches independently require monoclinic WO3, orthorhombic massicot PbO, and tetragonal litharge PbO; both PbO polymorphs have distinct non-overlapped reflections and positive refined scales.

The remaining monoclinic reflections are matched by a C2/m Pb2WO5 model adapted from the isostructural Pb2MoO5 framework. Its refined cell is a = 14.23684 A, b = 5.81406 A, c = 7.36490 A, beta = 113.80825 degrees. The peak positions and scale support a separate phase, but this powder pattern does not reliably refine all of its oxygen coordinates. The submitted CIF therefore retains physically valid analogue coordinates rather than over-interpreting unstable coordinate shifts.

A five-phase Le Bail diagnostic left a coherent series of peaks and gave Rwp = 9.86%; adding an F-centered cubic lattice reduced it to 6.69%. Its characteristic peaks occur at approximately 30.28, 35.05, 50.25, 59.64, and 62.56 degrees 2-theta and refine to a = 5.16423 A. A charge-neutral mixed Pb/W fluorite-type PbWO4 model, with [111] preferred orientation, gave the best constrained profile among the tested models. However, PbO2 and several Pb-W-O defect-fluorite compositions gave nearly indistinguishable fits at only about 4 wt%. Thus the cubic lattice and approximate fraction are supported, but its Pb/W/O stoichiometry and fluorite atomic assignment cannot be determined reliably from this pattern alone.

## Fit and limitations

An independent no-refinement replay of `final.gpx` on all 8,282 observations gives Rwp = 8.2802%, Rp = 5.8465%, and goodness of fit = 2.3748 with Poisson count weights. `fit.csv` is taken from that replay and contains observed, calculated, observed-minus-calculated, and background profiles. All six exported structures pass the geometry/occupancy contact screen; no negative-background or invalid-width flag was produced.

The background is empirical, and instrumental width, specimen displacement, size/strain, and texture terms are correlated. Those nuisance parameters should not be interpreted as calibrated microstructure measurements. The reported phase fractions are conditional on the six-phase crystalline model, particularly the analogue-based Pb2WO5 and tentative cubic component.
