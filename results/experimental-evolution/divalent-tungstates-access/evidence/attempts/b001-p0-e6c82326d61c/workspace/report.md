# Powder XRD phase analysis

The pattern is described by four crystalline phases. Fractions below are normalized over these modeled crystalline phases.

| Phase | Space group | Weight fraction |
|---|---:|---:|
| CuWO4 | P -1 | 64.96% |
| WO3 | P 21/c | 19.32% |
| Cu3WO6 | P a -3 | 13.18% |
| CuO (tenorite) | C 2/c | 2.53% |

## Evidence and refinement

Candidate structures were screened against the full pattern and then refined in GSAS-II using the supplied Cu Kalpha1/Kalpha2 wavelengths and intensity ratio. The starting structural models were COD 4000806 (CuWO4), 2311041 (WO3), 1527404 (Cu3WO6), and 1011194 (CuO). The triclinic CuWO4 model accounts for the major reflections near 18.81, 29.09, 30.08, and 31.48 degrees 2theta. Monoclinic WO3 is required by the resolved 22.67--23.89 degree group. Cubic Cu3WO6 is supported by its low-angle 15.18 and 19.80 degree peaks and the sequence near 32.51, 33.76, 49.67, 57.60, and 63.28 degrees. Weak residual features near 34.9, 38.3, and 48.0 degrees support tenorite CuO.

The refinement covered the complete 9.9034--100.0946 degree grid. Refined terms included phase scales, cells, atomic coordinates, common isotropic displacement factors, crystallite size, instrumental profile, and background; WO3 additionally required [001] uniaxial microstrain. Preferred orientation and surface roughness were tested but were not supported. The final fit has Rwp = 1.7308%, Rp = 1.3010%, goodness of fit = 1.0774, and chi-square = 9519.45 for 8301 observations and 100 refined variables. A native zero-cycle replay of `final.gpx`, using fresh GSAS-II reflection lists and structure factors, reproduces these values and all four reported fractions.

## Uncertainty

All four phase identities have phase-specific diffraction evidence, but CuO is the least secure quantitative component because it is only 2.53% and many of its reflections overlap stronger phases. Its tenorite structure is supported; subtle coordinate details and its fraction should not be interpreted at the precision suggested by the formal least-squares standard uncertainty. Profile, background, and zero/displacement correlations likewise make the formal fraction uncertainties optimistic. No amorphous content or unmodeled noncrystalline mass can be determined from this refinement, so the fractions are not absolute bulk fractions. Within those limits, no crystalline component remains unresolved in the difference profile.
