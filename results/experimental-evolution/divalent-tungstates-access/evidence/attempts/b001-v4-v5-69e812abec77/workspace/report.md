# Powder XRD phase analysis

The final atomic Rietveld model contains three crystalline phases:

| Phase | Space group | Weight fraction |
|---|---:|---:|
| MnWO4 (wolframite topology) | P 2/c (No. 13) | 69.79 wt% |
| monoclinic WO3 | P 21/c (No. 14) | 14.84 wt% |
| Mn3WO6, R-3 analogue model | R -3 (No. 148) | 15.37 wt% |

Fractions are normalized over these modeled crystalline phases. The fit has Rwp = 3.014%, Rp = 2.296%, and GOF = 1.704 over all 8301 measured points. The independently regenerated atomic GSAS-II replay reproduces this Rwp, retains the original grid and counts, and raises no negative-width, negative-background, or other profile-validity flags.

## Evidence

MnWO4 accounts for the dominant wolframite reflection family. Its residual contains the complete physical monoclinic-WO3 family; the geometry-valid P21/c WO3 parent fits better than the poor-coordinate monoclinic record after comparable size/strain refinement. The remaining coherent peaks, including the families near 20.32, 20.88, 29.15, 35.62, and 47.00 degrees 2theta, are indexed by the R-3 Mn3WO6 model. After including these phases, every strong residual family maps to an accepted reflection.

The third formula also closes the synthesis balance: the refined inventory gives Mn:W = 1.016:1 on a molar-cation basis, close to the 1:1 precursor ratio. A physical R-3 model transferred from Mn3TeO6 was preferred over C2/c Mn3WO6, Mn3W2O9, Mn2WO6, R3, and Pa-3 alternatives. Apparent lower-Rwp minima for some alternatives required Mn-O contacts near 1.2-1.6 A, abnormal coordination, or extreme broadening. In contrast, the submitted R-3 structure has sixfold Mn coordination (Mn-O 2.12-2.35 A), octahedral W (1.87-1.94 A), and a 2.51 A minimum O-O contact. A final Mn3O4 precursor test from three different starting scales converged to effectively zero weight, so it was not retained.

The refinement used bounded physical profile terms: crystallite sizes of about 0.084, 0.058, and 0.222 micrometers for MnWO4, WO3, and Mn3WO6; microstrain values within the stated lab range; a small supported [001] uniaxial strain term for MnWO4; zero = 0.20 degrees; and specimen displacement = -361 micrometers. Preferred-orientation tests refined to essentially unity and were rejected. MnWO4 and Mn3WO6 oxygen-coordinate updates were retained only after geometry screening; a WO3 oxygen-coordinate branch was rolled back because it generated 1.45 A W-O bonds.

## Remaining uncertainty

MnWO4 and monoclinic WO3 are well determined by multiple distinctive reflections. The exact Mn3WO6 atomic structure is less secure: no exact-composition reference was available, so its R-3 model is an analogue-derived, balance-supported assignment rather than an unambiguous structure determination. Its scale remains stable and its geometry is credible, but the detailed light-atom coordinates, exact composition/topology, and therefore its 15.37 wt% fraction are conditional on that model. The very small covariance uncertainties in `result.json` reflect counting statistics only and do not include this model uncertainty.

No amorphous fraction was measured, and the reported fractions should not be interpreted as absolute whole-specimen mass fractions if amorphous material is present. Instrument U reached the allowed upper bound, indicating residual correlation among instrumental and specimen broadening; the phase fractions were nevertheless stable across the accepted physical checkpoints.

Structural provenance: MnWO4 started from COD 1520200, physical monoclinic WO3 from COD 2311041, and Mn3WO6 from COD 2211528 (Mn3TeO6 with Te replaced by W), followed by the refinements recorded in `final.gpx`.
