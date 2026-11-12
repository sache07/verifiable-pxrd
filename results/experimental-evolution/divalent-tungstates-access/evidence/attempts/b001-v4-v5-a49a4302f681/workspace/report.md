# Powder XRD phase analysis

The specimen was modeled as three crystalline phases. Fractions below are normalized over those modeled crystalline phases; this experiment does not determine amorphous content or absolute crystalline yield.

| Phase | Space group | Weight fraction | Refined cell |
|---|---:|---:|---|
| MnWO4 (wolframite) | P 2/c | 0.68898 (68.90 wt%) | a = 4.79938, b = 5.71470, c = 4.98235 Å, beta = 91.1259° |
| WO3 (monoclinic) | P 21/c | 0.15728 (15.73 wt%) | a = 7.69856, b = 7.54324, c = 10.53383 Å, beta = 136.0809° |
| Mn3WO6 | R -3 | 0.15374 (15.37 wt%) | a = 8.89925, c = 10.46785 Å |

The final full-grid GSAS-II Rietveld fit has Rwp = 2.0741%, Rp = 1.5842%, Rexp = 1.7740%, and GOF = 1.1713. A native GSAS-II forward replay from `final.gpx`, with saved calculated arrays ignored, reproduces Rwp = 2.0741% and reports no negative-background, invalid-width, or displacement-parameter flags.

## Evidence

The dominant family is indexed by wolframite MnWO4, including the characteristic reflections near 15.9, 18.9, 24.1/24.6, 30.4/30.8, and 36.6° 2theta. An exact-composition P 2/c reference (COD 1520200) gave the chemically and geometrically ordinary starting topology.

Residual peaks after MnWO4 are broadly accounted for by room-temperature monoclinic WO3. The retained P 21/c neutron model (COD 2311041) was a slightly better and more physical exact-composition model than the close alternative settings tested. Its unusual beta near 136° is a valid nonstandard monoclinic setting.

A remaining coherent family at approximately 20.34/20.89, 29.15, 35.62, 47.02, and 54.95° indexed as a rhombohedral cell with a about 8.90 and c about 10.47 Å. An R -3 Mn3TeO6 topology (COD 2211528), adapted by the isovalent Te6+ to W6+ substitution, accounts for all members of this family as Mn3WO6. Adding this phase reduced the then-current full-pattern Rwp from about 18.0% to 5.26% before final coordinate/profile refinement. The final phase inventory also gives Mn:W = 1.004:1 from the refined mass fractions, consistent with the nominal 1:1 precursor metal ratio. No coherent unassigned reflection family remains.

The final structures have sensible contacts: minimum W-O distances are 1.789 Å in MnWO4, 1.701 Å in WO3, and 1.912 Å in Mn3WO6; no O-O contact is below 2.44 Å. Weak WO3 [010] preferred orientation and uniaxial broadening of the Mn3WO6 family were supported. A surface-roughness branch reached a bound and worsened the fit, so it was rejected.

## Remaining uncertainty

MnWO4 identification and topology are high confidence. Monoclinic WO3 identification is also strong, but its oxygen coordinates were not independently recoverable from this overlapped laboratory pattern: unconstrained refinement drifted excessively and bounded trials sat on their limits, so the physical reference oxygen sublattice was retained. The same limitation applies to the oxygen sublattice of Mn3WO6.

Mn3WO6 is the principal structural uncertainty because its submitted R -3 model is analogue-derived rather than an exact published Mn3WO6 reference. Its cell, peak family, positive scale, geometry, and chemical balance strongly support the phase and stoichiometry, but the detailed oxygen positions should be treated as a plausible topology rather than a uniquely solved structure.

Scale covariance alone gives very small statistical errors, but those omit reference choice, overlap, profile, and fixed-coordinate systematics. The extra digits record the fitted solution, not absolute accuracy; practical uncertainty is likely at least several tenths of a wt% for the minor phases. Calibration zero and specimen displacement are strongly correlated; zero was fixed at its physical checkpoint while displacement was refined. This correlation contributes additional systematic uncertainty to absolute cells but has little effect on the normalized phase fractions.
