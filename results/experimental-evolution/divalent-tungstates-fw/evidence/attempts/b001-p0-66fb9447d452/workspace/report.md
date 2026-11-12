# Powder X-ray diffraction analysis

## Result

The pattern is described by two crystalline precursor phases; no crystalline BaWO4 product is required.

| Phase | Structural model | Refined cell (Å, °) | Crystalline weight fraction |
|---|---|---|---:|
| Witherite, BaCO3 | Orthorhombic `Pnma` | a = 6.42233, b = 5.33770, c = 8.92576 | 0.4692 (46.92 wt%) |
| Monoclinic WO3 | `P21/c` setting | a = 7.29229, b = 7.53351, c = 10.52513, beta = 133.18527 | 0.5308 (53.08 wt%) |

The fractions are normalized over the modeled crystalline material only. The WO3 cell is a nonstandard but symmetry-equivalent `P21/c` setting of the room-temperature monoclinic structure.

## Evidence and refinement

The BaCO3 model accounts for the characteristic low-angle reflections near 19.6–20.1° 2theta and the strong features near 24.1° and 28.0°. Monoclinic WO3 is required by the resolved 23.4/23.9/24.6° group and the reflections around 33.5–34.4°. Together they account for the full measured range, 9.9034–100.0946° 2theta. A competing monoclinic WO3 structural model gave Rwp = 2.116% after comparable coordinate refinement, versus 1.892% for the selected model. Adding scheelite BaWO4 as a third phase drove its scale to the numerical lower bound (about 1e-13 of the crystalline mass), and its diagnostic reflections were not needed.

GSAS-II whole-pattern refinement used the supplied Cu K-alpha1/K-alpha2 wavelengths and 0.5 intensity ratio, a 12-term Chebyshev background, phase scales and cells, isotropic crystallite-size broadening, instrumental U/W/SH-L terms, and angular zero/sample-displacement terms. Unsupported preferred orientation, surface roughness, and microstrain terms were omitted. The final fit has Rwp = 1.8922%, Rp = 1.5123%, goodness of fit = 1.0311, and chi-square = 8794.74 for 8301 observations and 29 refined variables. An independent native GSAS-II replay of `final.gpx`, regenerating reflection lists and structure factors rather than trusting saved profile arrays, gives Rwp = 1.8922% and reproduces both phase fractions.

## Remaining uncertainty

Phase identity and the approximate 47:53 crystalline mass split are well supported. Model-sensitivity trials moved either fraction by less than about 0.5 percentage point; a conservative practical uncertainty is approximately 1–2 percentage points because no internal standard, calibrated instrumental profile, or absorption correction was supplied. This is not an absolute assay: amorphous material, if present, cannot be quantified, and a trace crystalline phase below the pattern's detection limit cannot be excluded. BaWO4 has no reliable positive fraction and is therefore not reported as a phase.

The cell metrics and Ba/W substructures are better determined than the oxygen coordinates. X-ray contrast is dominated by Ba and W, so individual O positions and displacement parameters should not be interpreted as high-precision bond-geometry measurements. Angular zero and specimen displacement are also strongly correlated, although their combined correction yields a stable phase inventory and fraction ratio.
