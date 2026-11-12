# Powder X-ray diffraction analysis

## Result

The pattern is explained by a single crystalline phase: wolframite-type MnWO4 in space group P 2/c (No. 13). Its weight fraction is **1.000 (100 wt%) after normalization over the modeled crystalline phases**. This normalization does not measure amorphous material or phases below the diffraction detection limit.

The refined unit cell is a = 4.83197 A, b = 5.75849 A, c = 4.99763 A, beta = 91.2179 degrees, and V = 139.027 A3 (Z = 2). The refined atomic coordinates and fixed isotropic displacement parameter Uiso = 0.004 A2 are in `phase_1_MnWO4.cif`.

## Evidence and refinement

The peak sequence at approximately 15.7, 18.6, 23.9/24.3, 30.1/30.5, 36.2, and 41.1 degrees 2theta, together with the remaining peaks across the full 9.90-100.09 degree scan, matches monoclinic wolframite MnWO4. This assignment is chemically consistent with the Mn3O4 + WO3 precursor context and the reported 900 degrees C treatment. A P 2/c MnWO4 starting model (COD 1520200) was refined against all 8,301 measured points using the stated Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio.

With Poisson count weights, the final stored GSAS-II profile gives Rwp = 3.7925%, Rp = 2.9384%, Rexp = 3.4605%, and goodness of fit = 1.0986. A fresh no-refinement forward replay from `final.gpx`, which discards the stored calculated array and regenerates reflections and structure factors, gives Rwp = 3.7982% and the same one-phase fraction. The small difference is from fresh reflection-list and numerical profile regeneration.

The model includes a 16-term Chebyshev-1 background, specimen displacement, zero offset, polarization, surface roughness, isotropic crystallite size, and [001] uniaxial microstrain. No preferred orientation was supported. The refined instrument U term reached its allowed upper bound and is correlated with specimen broadening; therefore the individual size/strain/profile parameters should not be interpreted uniquely. This does not materially affect the phase identity, cell, or one-phase conclusion.

## Remaining uncertainty

Explicit fixed-profile searches for residual Mn3O4, WO3, and Mn3WO6 models produced only unstable apparent fractions below 0.5 wt% and very small improvements (Delta chi-square at most about 13 over 8,301 points). These signals are not sufficient to claim another phase or determine a reliable trace fraction, so they were not included. Trace crystalline impurities at roughly the sub-percent to approximately 1 wt% level remain possible, depending on peak overlap and crystallinity. Consequently, 100 wt% is the normalized fraction of the detected/modelled crystalline material, not a demonstrated absolute bulk purity.
