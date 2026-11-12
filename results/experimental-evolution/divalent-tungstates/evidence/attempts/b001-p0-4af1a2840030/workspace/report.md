# PXRD phase analysis

## Result

The pattern is modeled as a single crystalline phase: scheelite-type calcium tungstate, CaWO4, space group I 41/a (No. 88). Its weight fraction is **100.0 wt% after normalization over the modeled crystalline phases**. The refined model is in `CaWO4_scheelite.cif` and the complete refinement is in `final.gpx`.

The refined tetragonal cell is a = 5.248860(33) A, c = 11.385916(61) A, and V = 313.68809(386) A^3. The refined oxygen site is (x, y, z) = (0.155354, 0.010113, 0.208984); Ca and W remain on their symmetry-fixed special positions.

## Evidence

The observed strong lines at 18.61, 28.70, 29.03, 31.42, 34.16, 39.17, 47.07, 49.06, 54.25, and 57.82 degrees 2theta form the characteristic I-centered scheelite CaWO4 pattern. A COD CaWO4 model (COD 7219229) was used as the starting structure. The alternative chemically plausible phases were rejected by required reflections absent from the data: CaO requires strong lines near 32.2 and 37.3 degrees; Ca3WO6 requires strong lines near 18.9, 22.1, and 31.5 degrees; common WO3 polymorphs require the 23.1-24.4 degree cluster; and monoclinic CaWO4 requires strong lines near 19.3 and 29.8 degrees. The final difference trace does not contain a coherent second set of reflections.

## Refinement

GSAS-II Rietveld refinement used the full measured range (9.90343-100.09455 degrees 2theta), the reported Cu Kalpha1/Kalpha2 wavelengths and fixed 0.5 intensity ratio, a 12-term shifted-Chebyshev background, and an effective Gaussian CW profile with axial-divergence asymmetry. Refined quantities were phase scale, cell, profile U/W and SH/L terms, oxygen coordinates, and isotropic displacement parameters. The zero offset was held at zero and polarization at 0.7 to avoid unsupported correlations because no calibrated instrument profile or effective polarization was supplied. With no supplied pointwise uncertainties, counting uncertainties sigma(I) = sqrt(I) were used.

Fit statistics are Rwp = 2.6643%, Rp = 2.0210%, Rexp = 2.2809%, GOF = 1.1698, and Bragg R(F) = 1.9450% (8301 observations, 24 refined variables). `fit.csv` contains observed, calculated, observed-minus-calculated, and background profiles.

## Remaining uncertainty

The 100 wt% value is conditional on the crystalline model: without an internal standard it cannot quantify amorphous material, and trace impurities below the pattern's detection capability cannot be excluded. No quantitative detection limit was established. Statistical cell and coordinate uncertainties also understate possible systematic errors from specimen displacement and the uncalibrated instrumental profile. Crystallite size and microstrain were therefore not interpreted separately.
