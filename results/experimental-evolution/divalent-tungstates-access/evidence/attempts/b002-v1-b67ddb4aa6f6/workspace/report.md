# Powder XRD phase analysis

The pattern is modeled as three crystalline phases. Fractions are normalized only over these phases.

| Phase | Structural model | Crystalline weight fraction |
|---|---|---:|
| ZnWO4 | Wolframite, P 2/c | 84.53% |
| WO3 | Monoclinic, P 21/c | 10.65% |
| ZnO | Wurtzite, P 63 m c | 4.82% |

The covariance-only one-standard-deviation errors from the phase scales are 0.21, 0.11, and 0.20 weight-percentage points, respectively. These do not include structure choice, preferred-orientation, background, or sample-preparation systematics; the corresponding simpler rollback branches vary by as much as about 0.7 weight-percentage point. The fractions therefore should not be interpreted to the formal precision. Absolute phase contents, including any amorphous material, cannot be determined from this scan without an external standard.

## Evidence

ZnO and WO3 are the stated precursors and the 700 °C reaction product is dominated by the expected ZnWO4 wolframite topology. No exact ZnWO4 record was present in the supplied filtered structure library, so the principal model was constructed from the isostructural CoMoO4-II P 2/c record COD 7205001 by Co->Zn and Mo->W substitution. Its refined cell is a = 4.70751 Å, b = 5.74081 Å, c = 4.94027 Å, beta = 90.6183°. It accounts for the dominant families near 19.23°, 24.14/24.83°, 30.75/31.00°, 36.56°, and 48.98° 2theta. A standardized FeNbO4 analogue was worse under the common screen, the MnReO4 branch became invalid, and scheelite, fergusonite, C2/c, and triclinic target-composition prototypes produced conflicting peak families.

The residual family near 23.43°, 24.00°, 24.70°, 26.99°, 28.92/29.26°, 33.61°, and 34.53° is explained by WO3. All nine supplied exact-formula WO3 records were screened under common nuisance settings. The nominated monoclinic COD 2311041 model gave Rwp = 18.607% in that two-phase screen; triclinic COD 2106293 gave 18.603%. That 0.004 percentage-point difference is not meaningful relative to the triclinic model's extra cell freedom, so the chemically economical monoclinic room-temperature model was retained. Its atomic coordinates were kept at the source values because unconstrained and bounded tungsten-coordinate trials drifted or diverged. The WO3 formula and approximately 10.7% fraction are well supported, but this powder pattern does not reliably distinguish a monoclinic structure from a closely related triclinic distortion or a small intergrowth of them.

Adding wurtzite ZnO gives a stable approximately 4.8% contribution at its 32.06°, 34.93°, 36.58°, 47.94°, and 56.79° families and closes the remaining coherent positive residuals. Rocksalt and zincblende trials did not remain valid in the mature project, so they are recorded as unknown rather than falsely rejected. Reduced tungsten-oxide candidates likewise collapsed to zero scale before invalid cell trials; no positive evidence for them was retained. After ZnO was added, the remaining residuals are predominantly intensity/shape errors at already modeled peaks rather than a coherent unmodeled family. The full branch ledger is in `analysis/candidate_ledger.csv`.

## Refinement and checks

The final GSAS-II refinement used the supplied Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio, a 12-term Chebyshev background, zero and sample-displacement corrections, symmetry-independent cell terms, limited ZnWO4 cation coordinates, isotropic crystallite-size broadening, and sequentially supported March-Dollase terms for ZnWO4 [111] (ratio 0.710) and WO3 [110] (ratio 1.449). ZnO texture was axis-ambiguous and was not retained. Strain and common Lorentzian-width trials collapsed or were singular; polarization hit its bound; roughness was strongly correlated; and Uiso trials hit bounds. Oxygen-coordinate trials in ZnWO4 and ZnO gave small profile gains only by excessive displacements, so the submitted models retain parent-topology oxygen coordinates. The submitted first-shell distances are physically credible: ZnWO4 Zn-O = 2.005-2.222 Å and W-O = 1.786-2.181 Å; WO3 W-O = 1.713-2.162 Å; ZnO Zn-O = 1.979-1.983 Å.

The converged fit has Rwp = 11.0169%, Rp = 6.6245%, goodness of fit = 4.1710, and 32 refined variables over 8,301 points. A fresh native GSAS-II replay from `final.gpx`, ignoring saved calculated arrays, gives Rwp = 11.0169% and no negative-background, negative-width, displacement-tensor, or polarization flags. The elevated goodness of fit and visible peak-shape/intensity residuals mean this is a useful phase model, not a uniquely determined high-precision crystal-structure solution.
