# Powder X-ray diffraction phase analysis

## Result

The crystalline specimen is modeled as partially reacted precursor/product material from the 650 °C CaCO3 + WO3 synthesis.

| Phase | Structural model | Refined cell (Å, °) | Crystalline wt.% |
|---|---|---|---:|
| CaWO4 (scheelite) | COD 7219229, *I* 41/*a* | *a* = 5.23813, *c* = 11.3351 | 81.05 |
| WO3 (monoclinic) | COD 2311041, *P* 21/*c* | *a* = 7.69459, *b* = 7.55755, *c* = 10.5189, beta = 135.947 | 14.08 |
| CaCO3 (calcite) | COD 1547347, *R* -3 *c* | *a* = 4.98705, *c* = 17.0554 | 4.87 |

Fractions are normalized over these modeled crystalline phases. Their conditional least-squares standard uncertainties are 0.20, 0.05, and 0.22 wt.% respectively, but these do not include structural, profile, preferred-orientation, absorption, or calibration model uncertainty.

## Evidence and refinement

The dominant scheelite model accounts for the complete CaWO4 family, including the reflections near 18.3, 28.4, 31.2, 33.8, 38.9, and 46.9° 2theta. Monoclinic WO3 accounts for the characteristic split 22.8–24.0° family and corroborating higher-angle reflections. After fitting those phases, a coherent residual family near 29.1, 35.7, 47.3, and 57.4° was indexed by calcite. Adding calcite produced a stable positive scale and removed that family. Calcite and WO3 are also chemically ordinary residual precursors for the stated synthesis. The resulting crystalline Ca:W mole ratio is approximately 0.965, independently supporting this product-plus-unreacted-precursors inventory.

The GSAS-II refinement used the supplied Cu Kalpha1/Kalpha2 wavelengths and intensity ratio over all 8,301 measured points from 9.9034 to 100.0946° 2theta. Main-phase cells, scales, and supported coordinates were refined; the calcite cell, scale, and crystallite-size term were refined while its light-atom coordinates and displacement parameters were retained from the reference. Instrument/profile, specimen displacement, and background terms were refined. The final fit has Rwp = 3.2228%, Rp = 2.4922%, reduced chi-square = 1.0574, and goodness of fit = 1.0283; the counting-statistical minimum Rwp is 3.1382%. Independent replay from `final.gpx` reproduces `fit.csv` to numerical precision, and all three exported structures pass the geometry and occupancy screen.

## Remaining uncertainty

The phase inventory and relative crystalline fractions are well supported, but the quoted formal fraction errors are conditional and should not be interpreted as full accuracy. No internal standard was present, so an amorphous fraction—and therefore absolute bulk phase fractions—cannot be determined reliably. Trace crystalline phases below the residual/noise level also cannot be excluded.

The monoclinic WO3 framework is supported, but individual oxygen displacements are not uniquely constrained by this powder pattern; a closely related distorted WO3 description remains the main structural ambiguity. At only about 4.9 wt.%, calcite's C/O coordinates, displacement parameters, and crystallite size (about 0.076 micrometres in this profile model) cannot be determined independently with high reliability. The specimen-displacement and zero-offset terms are correlated, so the zero offset was held at -0.200° while specimen displacement was refined; this does not materially change the accepted phase inventory.
