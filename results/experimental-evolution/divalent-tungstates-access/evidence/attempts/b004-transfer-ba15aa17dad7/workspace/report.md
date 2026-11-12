# Powder XRD phase analysis

## Result

Three crystalline phases account for the pattern. Weight fractions are normalized over these modeled crystalline phases; they do not measure an amorphous fraction.

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| Ba3W2O9 | R -3 c (No. 167) | a = 10.13270, c = 13.96611 | 72.11% |
| monoclinic WO3 | P 21/c (No. 14), nonstandard cell | a = 7.69384, b = 7.53779, c = 10.52121, beta = 136.0845 | 22.95% |
| BaCO3 (witherite) | P m c n (No. 62; setting of Pnma) | a = 5.30460, b = 8.91369, c = 6.44767 | 4.94% |

The GSAS-II covariance matrix gives conditional one-sigma fraction uncertainties of about 0.04–0.05 weight-percent absolute. These are much smaller than the likely systematic uncertainty from background, preferred orientation, and structural/profile choices.

## Evidence

The dominant broad reflections at approximately 17.71, 26.20, 27.70, 30.77, 40.74, 42.95, 53.68/54.51, and 63.02° 2theta are indexed by trigonal Ba3W2O9. The sharp WO3 triplet near 23.35, 23.82, and 24.62°, together with its 33–34° reflections, requires monoclinic WO3. Weak but reproducible lines near 24.12, 24.49, 34.80, 42.24, and 45.06° are explained by orthorhombic BaCO3. The latter two phases are chemically credible residual precursors after the reported 800 °C treatment. No distinct residual reflection set requires BaWO4 or a fourth crystalline phase.

Starting atomic models were COD 1533878 (Ba3W2O9), 2311041 (WO3), and 9010928 (BaCO3). Their refined cells, full peak-position coverage, and the improvement from each phase support the assignments.

## Refinement and fit

The final full-pattern GSAS-II model uses the reported Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio, a smooth Chebyshev background, refined instrument/sample profile terms, phase scales, cells, isotropic size and microstrain, and common positive isotropic displacement parameters within each phase. Ba3W2O9 required March-Dollase preferred orientation along [110] (ratio 1.315); the much smaller WO3 [100] correction (1.025) is close to unity and is not strongly determined.

A fresh native replay of `final.gpx`, regenerating reflection lists and structure factors rather than using saved calculated arrays, gives Rwp = 2.728%, Rp = 2.108%, chi-square = 11679.03, and goodness of fit = 1.189 over all 8301 points. The submitted CIFs are byte-identical to the phase exports from that replay. All three structures pass broad contact, occupancy, and density checks.

## Remaining uncertainty

The phase identities are well supported, but the quoted covariance errors understate model uncertainty. A conservative reading is roughly 1–2 weight-percent absolute uncertainty for each major phase and about 0.5–1 weight-percent for the minor BaCO3 fraction; preferred orientation is the main limitation. Trace crystalline material below the practical detection limit could remain.

Independent light-atom coordinate refinement was unstable and correlated. The final O and C coordinates were therefore kept close to the published parent structures while the heavy-atom framework and profile were refined. The CIFs are suitable phase/profile models, but the detailed O/C coordinates should not be treated as a precise independent structure determination. Absolute amorphous content cannot be determined without an internal standard or complementary measurement.
