# PXRD phase analysis

The reliably modeled crystalline assemblage is PbWO4 (scheelite/stolzite), monoclinic WO3, and both common PbO polymorphs. Fractions below are normalized to 100% over these four modeled phases; they are not absolute bulk fractions because an unidentified crystalline contribution remains and no internal standard was supplied.

| Phase | Space group | Refined cell (Å, °) | Modeled crystalline wt.% |
|---|---|---|---:|
| PbWO4, scheelite/stolzite | I 41/a | a = 5.46566, c = 12.06116 | 73.93 (formal s.u. 0.28) |
| WO3, monoclinic | P 21/n | a = 7.30487, b = 7.54732, c = 7.70093, beta = 90.347 | 11.65 (0.25) |
| PbO, massicot | Pbcm | a = 5.89685, b = 5.49416, c = 4.75843 | 9.30 (0.15) |
| PbO, litharge | P 4/nmm | a = 3.97750, c = 5.02943 | 5.12 (0.13) |

Evidence is strongest for scheelite PbWO4: its 112 line at 27.70° and the series at 29.91, 33.05, 45.02, 47.28, 51.48, 55.54, and 56.81° continue consistently through the high-angle pattern. Monoclinic WO3 is identified by the characteristic 23.36/23.88/24.65° triplet and the 33.52/34.44° group. Massicot accounts for lines near 29.34, 30.61, 38.11, 53.38, 56.31, and 60.53°; litharge is independently supported by features near 28.9, 32.1, 36.0, 45.9, 48.8, and 54.9°. This is chemically consistent with partial reaction of the reported PbO and WO3 precursors at 500 °C.

The final GSAS-II refinement used the supplied Cu Kalpha1/Kalpha2 wavelengths (1.540598/1.544426 Å) and fixed 0.5 intensity ratio, Poisson-approximation weights because pointwise uncertainties were absent, an 18-term Chebyshev background, a common refined zero offset and profile, and independently refined phase scales and cells. Reference atomic coordinates were retained because the overlapping minor-phase reflections do not support stable coordinate refinement. The final full-range fit has Rp = 9.18%, Rwp = 13.65%, Rexp = 3.50%, and goodness of fit = 3.91 (8282 points, 39 variables). The calculated column in `fit.csv` includes the background; difference is observed minus calculated.

There is unresolved crystalline intensity, principally at 13.93, 25.91, 30.14, and 31.38° 2theta. A forced minium-type Pb3O4 trial reduced Rwp to about 12.82%, but required a = 9.093 and c = 6.736 Å—about 9% larger in volume than credible Pb3O4—and retained poor phase-specific intensity agreement. PbO2, reduced tungsten oxides, and monoclinic PbWO4 trials were less convincing. Therefore no structure or weight fraction is reported for this contribution. The formal fraction s.u. values above are covariance estimates only; unmodeled intensity, possible PbO preferred orientation, and the lack of a calibrated instrument profile make the true systematic uncertainty several times larger. Amorphous content cannot be determined without an internal standard.
