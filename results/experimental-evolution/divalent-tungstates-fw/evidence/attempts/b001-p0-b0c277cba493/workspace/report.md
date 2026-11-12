# Powder XRD phase analysis

The pattern is modeled as two crystalline phases:

- Orthorhombic witherite BaCO3, space group Pnma (COD 9010928): 0.4665 weight fraction (46.65 wt%).
- Monoclinic WO3, space group P21/c (COD 2311041): 0.5335 weight fraction (53.35 wt%).

These fractions are normalized over the modeled crystalline material; no amorphous fraction can be obtained from this scan alone. A realistic systematic uncertainty is about 2–3 wt% per phase because scale, surface roughness, polarization, and displacement parameters are correlated.

## Evidence

The BaCO3 model accounts for the witherite reflections around 24.1, 34.7, 42.1, and 45.1 degrees 2theta. The low-symmetry WO3 model accounts for the characteristic 23–25 degree triplet, the 33–35 degree cluster, and lines near 50.2 and 56.2 degrees. Whole-pattern screening of the available BaCO3 and WO3 polymorphs selected these two references. A close monoclinic WO3 alternative gave poorer agreement unless oxygen coordinates were displaced implausibly far. BaWO4 was tested, but its strongest expected line near 26.45 degrees and associated lines are not supported; its nonnegative refined scale collapsed to zero.

The final dual-wavelength Cu K-alpha GSAS-II refinement includes background, phase scales and cells, common specimen displacement, instrumental profile, isotropic crystallite size, surface roughness, phase-common isotropic displacement parameters, and small bounded coordinate adjustments. It gives Rwp = 1.9177%, Rexp = 1.8352%, Rp = 1.5291%, and goodness of fit = 1.0449 over 8,301 points. Independent native replay of `final.gpx` reproduces the same Rwp and phase fractions, with no physical-review flags; both exported CIFs pass the geometry/occupancy screen.

## Remaining uncertainty

The phase inventory and approximate fractions are reliable, but fine oxygen coordinates in WO3 are only weakly constrained by laboratory X-ray data. Closely related distorted WO3 descriptions cannot be excluded absolutely. The uncalibrated angular zero, specimen displacement, and lattice parameters are strongly correlated, so the reported cells should not be treated as precision lattice metrology. No additional crystalline phase is justified by the residual, though trace material below the pattern's detection limit remains possible.
