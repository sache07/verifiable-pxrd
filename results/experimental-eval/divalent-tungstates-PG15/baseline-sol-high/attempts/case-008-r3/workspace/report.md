# PXRD phase analysis

The pattern is modeled as 97.95 wt% wolframite MnWO4 and 2.05 wt% monoclinic gamma-WO3, normalized over the modeled crystalline phases. The formal GSAS-II standard uncertainty on each fraction is 0.07 wt%, but a more realistic model-dependent uncertainty for the minor WO3 content is about 0.4 wt%.

## Evidence

The major reflections, including the intense pairs near 30.12/30.58 degrees 2theta and the lines near 18.68, 23.89, 24.36, 36.27, and 51.47 degrees, match monoclinic wolframite MnWO4 (P 2/c). A search of Mn-W-O, Mn-O, and W-O candidates was followed by whole-pattern refinements. MnO, Mn3WO6, MnO2, and the tested tetragonal, hexagonal, and orthorhombic WO3 models refined to zero or statistically insignificant amounts.

The remaining weak peaks are consistently accounted for by room-temperature monoclinic WO3 (P 21/n). Its diagnostic lines occur near 23.45, 23.91, 24.70, 33.58, and 34.45 degrees after the common specimen-displacement correction. Closely related monoclinic WO3 references fit similarly, so the assignment to monoclinic gamma-WO3 is secure, while the exact low-symmetry coordinate variant is less certain at only about 2 wt%.

## Refinement

GSAS-II Rietveld refinement used the full 9.903-100.095 degree range and the supplied Cu K-alpha1/K-alpha2 wavelengths (1.540598/1.544426 A) with the reported 0.5 intensity ratio. Refined terms included a 12-term Chebyshev background, phase scales and cells, specimen displacement, effective polarization, and a constrained physically positive peak-width model. The Mn and W positional parameters in MnWO4 were refined; oxygen coordinates and the minor-phase coordinates were retained from the reference structures because this laboratory X-ray pattern does not determine them reliably. The uncalibrated profile gives a 97.3% correlation between two width terms, so crystallite size or microstrain cannot be extracted reliably.

Final statistics are Rwp = 7.214%, Rp = 4.960%, Rexp = 2.759%, and goodness of fit = 2.620. The refined cells are:

- MnWO4: a = 4.83030 A, b = 5.75594 A, c = 4.99546 A, beta = 91.2194 degrees, P 2/c.
- WO3: a = 7.29980 A, b = 7.54080 A, c = 7.68067 A, beta = 90.8458 degrees, P 21/n.

Pointwise uncertainties were not supplied, so Poisson proxy weights (1/I) were used; consequently Rexp, goodness of fit, and formal parameter uncertainties are conditional on that assumption and are likely optimistic. The reported fractions exclude amorphous material and any crystalline phase below the practical detection limit. No reliable amorphous fraction can be obtained from these data alone.

The submitted [final.gpx](final.gpx) is the project used to export [MnWO4.cif](MnWO4.cif), [WO3.cif](WO3.cif), [fit.csv](fit.csv), and [result.json](result.json).
