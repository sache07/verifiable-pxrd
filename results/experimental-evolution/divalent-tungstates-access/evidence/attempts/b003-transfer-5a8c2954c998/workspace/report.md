# Powder XRD phase analysis

## Result

The pattern is described by three crystalline phases:

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| MnWO₄ (wolframite) | P 2/c | a = 4.79288, b = 5.70338, c = 4.97131, β = 91.1635 | 0.64185 |
| monoclinic WO₃ | P 2₁/n (setting of No. 14) | a = 7.28161, b = 7.52386, c = 7.68028, β = 90.7582 | 0.17940 |
| Mn₃WO₆ | R -3 | a = b = 8.88157, c = 10.47390 | 0.17874 |

The fractions sum to 1.00000 over the modeled crystalline material. Native GSAS-II regeneration from `final.gpx` over all 8,301 measured points gives Rwp = 3.08875%, Rp = 2.27258%, and χ² = 38,929.93 using weights 1/max(Iobs, 1). The replay produced no negative-width, negative-background, or displacement-parameter review flags.

## Evidence and refinement

The Cu Kα₁/Kα₂ wavelengths and intensity ratio were fixed to the metadata. Candidate Mn–W–O structures were screened against the full pattern, then refined in GSAS-II with background, phase scales and cells, specimen displacement, bounded instrumental profile terms, phase size/strain broadening, and March–Dollase texture where supported. Starting models were COD 1520200 (MnWO₄), COD 1528915 (monoclinic WO₃), and COD 2002703 (Mn₃WO₆).

MnWO₄ accounts for the dominant fingerprint at approximately 15.26°, 18.25°, 23.46°, and the 29.8–30.3° group. WO₃ is required by the 22.9°, 24.2°, and 33–34° groups. Mn₃WO₆ supplies distinct intensity near 19.7–20.2°, 28.5°, and 35.0°. In staged omission tests, MnWO₄ alone gave Rwp ≈ 16.75%; the MnWO₄ + Mn₃WO₆ and MnWO₄ + WO₃ models gave ≈14.49% and ≈10.87%, respectively, whereas the three-phase model gave ≈6.95% before structural/profile polishing. An alternative P2₁/m WO₃ model was substantially worse.

Residual Mn₃O₄ was tested as a fourth phase. It refined to only about 0.7–0.9 wt%, changed Rwp by roughly 0.015 percentage point, and had an unstable/bound-limited broadening term. That signal is not sufficient to claim a resolved fourth phase, so Mn₃O₄ is not included in the reported inventory.

## Remaining uncertainty

The phase identities, crystal systems, and three-phase inventory are well supported. The quoted fractions are conditional on crystalline material and do not quantify amorphous content. Profile/texture overlap gives an estimated systematic uncertainty of roughly ±0.02 absolute fraction for each phase; this is a practical estimate, not a formal covariance-derived standard uncertainty.

The CIFs are refined powder models. Their lattice metrics and heavy-atom frameworks are reliable at this resolution, but individual oxygen coordinates and isotropic displacement parameters—especially in WO₃—are correlated with intensity/profile terms and should not be treated as a single-crystal-quality determination. In particular, the submitted WO₃ model retains a 1.684 Å O–O contact inherited from the matched historical reference (whose corresponding contact is about 1.575 Å). The powder intensities support this reference family over the tested alternative, but do not establish that oxygen geometry; the WO₃ oxygen substructure therefore requires physical adjudication and cannot be reported reliably. A trace phase below about 1 wt%, including residual Mn₃O₄, cannot be excluded reliably. Angular zero and specimen displacement are also strongly correlated, although their combined peak-position correction is well determined.
