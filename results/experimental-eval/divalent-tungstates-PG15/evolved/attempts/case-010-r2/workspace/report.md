# PXRD phase analysis

## Result

The final GSAS-II Rietveld model contains three crystalline phases. Fractions are normalized only over those modeled crystalline phases.

| Phase | Structural model | Weight fraction | Assessment |
|---|---|---:|---|
| WO3 | monoclinic P 21/c, COD 2311041 | 70.43(28) wt% | Established major phase |
| Mn2O3 | cubic bixbyite, I a -3, COD 1514230 | 28.66(27) wt% | Established major phase |
| MnWO4 | monoclinic wolframite, P 2/c, COD 1520200 | 0.91(8) wt% | Tentative weak phase |

The values in parentheses are one-standard-uncertainty covariance estimates from the final refinement. They do not include model selection, background, absorption, or sampling error. A more realistic reading is about ±1 wt% for each major-phase fraction. The MnWO4 fraction is not reliably known to ±0.08 wt%: approximately 0.9 ± 0.5 wt% is a more defensible model-level estimate, and even its presence should be treated as tentative. No external standard was present, so an amorphous fraction cannot be measured and is excluded from the normalization.

## Context and phase evidence

The metadata gives Mn2O3 and WO3 precursors heated at 500 °C. The pattern is an unprocessed reflection-geometry Cu K-alpha scan from 9.9034 to 100.0949° 2theta (8,301 points). Both wavelengths and the reported K-alpha2/K-alpha1 ratio of 0.5 were used. Since pointwise uncertainties were absent, counting uncertainties were approximated as `sqrt(counts)`.

- WO3 is required by many resolved families across the full range. Under the same restrained background/profile model, the selected P 21/c record gave Rwp 7.229% in the clean two-phase fit, versus 8.613% for a P 21/n record, 8.663% for P -1, and 15.408% for Pnma. Its unusual beta angle in the exported CIF reflects the nonstandard source-cell setting.

- Bixbyite Mn2O3 accounts coherently for families near 33.26, 38.53, 49.61, 55.48, and 66° 2theta. The physically standard I a -3 model outperformed an I 21 3 record (Rwp about 7.67%) and an orthorhombic alternative (above about 8.9% during its common-profile challenge).

- A small positive MnWO4 scale is supported mainly by the diagnostic pair near 30.36/30.73° and partly overlapped higher-angle families. With all nuisance terms fixed, its scale was 6.3 standard uncertainties above zero. Adding it and reconverging reduced Rwp from 7.229% to 7.161%. An independently generated P 2/c MnWO4 analogue made by the chemically justified Fe-to-Mn substitution in an ambient FeWO4 parent converged to a similar 0.9–1.0 wt%, supporting the assignment.

The MnWO4 evidence is nevertheless limited: only one strong family is clearly distinctive, its exact COD parent was measured at 2.4 GPa, and its phase-only R(F²) is 31.3%. Its cell was first refined to the values in the submitted CIF and then fixed for the final stable replay; its atomic coordinates were not independently determined. This is why the phase and fraction remain tentative.

Mn3WO6 was retained on the watch list and tested using both an exact record and a Mn3TeO6-derived W analogue. Tiny scales improved overlapped regions near 28.9 and 54–56°, but worsened the strongest unique predicted pair near 20.2/20.6°; it was rejected. Mn3O4 and additional WO3 polymorphs likewise lacked coherent unique-family support. Trace phases below roughly 1 wt% cannot be excluded by this pattern.

## Refinement and fit quality

The baseline uses a smooth six-coefficient Chebyshev background, one zero correction (0.37966°), a nonnegative common U/W/X profile with low-angle SH/L asymmetry, and a refined effective polarization of 0.6892. Four- and five-coefficient backgrounds were inadequate. Roughness, preferred orientation, and anisotropic broadening were left neutral. Phase size was held at a neutral 10 micrometres, and strain was zero except for replay-stable isotropic Mn2O3 microstrain of 1,687(220) microstrain. Atomic coordinates, occupancies, and displacement parameters were retained from the screened source structures; only scales, the two major cells, Mn2O3 strain, background, and zero were active in the final cycle.

Observed versus calculated peak positions, widths, and asymmetry were checked for isolated low-, middle-, and high-angle families. The final project was saved, reopened, and replayed three times over the full range; Rwp varied by only 0.00011 percentage point and every phase fraction by less than 0.002 wt%.

Final statistics are Rwp = 7.1609%, Rp = 5.4081%, Rexp = 2.6624%, and goodness of fit = 2.6923. The Durbin-Watson statistic is 0.308, so correlated profile residual remains and the fit is not noise-limited despite its low R factors. This, the approximate Poisson weighting, and minor-phase/background covariance are the principal remaining uncertainties.

The submitted [final.gpx](final.gpx) is the exact project used to export [WO3.cif](WO3.cif), [Mn2O3.cif](Mn2O3.cif), [MnWO4.cif](MnWO4.cif), the combined [fit.csv](fit.csv), and [result.json](result.json).
