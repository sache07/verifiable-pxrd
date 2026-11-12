# Powder diffraction phase analysis

## Result

The modeled crystalline material is single-phase wolframite-type **MnWO4**, monoclinic **P2/c** (No. 13). Its weight fraction is **1.000 (100 wt%) after normalization over the modeled crystalline phases**. This normalization does not measure amorphous content and does not prove absolute chemical purity.

The refined ambient-pressure metric is:

- a = 4.8307(3) Å
- b = 5.7570(3) Å
- c = 4.9958(3) Å
- beta = 91.218(3)°
- V = 138.903(16) Å³

The parenthesized values are GSAS-II least-squares uncertainties. They are smaller than the likely absolute errors because the instrument profile was not calibrated and specimen displacement is correlated with the cell metric.

## Evidence

The diagnostic MnWO4 lines are all present, including the low-angle peaks near 15.67 and 18.63°, the 23.85/24.31° and 30.07/30.53° doublets, and the lines near 31.31, 36.22, 37.45, 41.13, and 51.45° 2theta. Their full sequence and relative intensities are reproduced by the P2/c wolframite model, and formation of MnWO4 is chemically consistent with firing Mn3O4 and WO3 at 900 °C.

Alternative phases were tested and are not justified. Mn3WO6 would give intense lines near 19.97, 20.50, 28.77, 35.27, 45.88, and 46.65° that are absent. Monoclinic WO3 would give a strong 23.1–24.4° triplet together with a conspicuous 33.3–34.2° group; the latter is absent. Residual Mn3O4 would require standalone peaks near 28.9 and 32.3° in addition to its overlaps with MnWO4, and these are absent. Fixed-model scale tests returned 0.03(22) wt% Mn3WO6 and drove WO3 to the nonnegative zero bound. A practical detection limit is about 1 wt% for a well-crystallized impurity, rather than the smaller formal scale errors, because profile and background systematics dominate the counting statistics.

## Refinement and uncertainty

GSAS-II used all 8301 raw points from 9.9034 to 100.0949° 2theta, the reported Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio, and Poisson weights (1/I) because pointwise uncertainties were not supplied. The model used a 15-term Chebyshev background, a Bragg–Brentano specimen-height correction, and only constant Gaussian and Lorentzian width terms; a full five-term profile was underdetermined without a calibrated standard. The final statistics are Rwp = 12.212%, Rp = 8.820%, Rexp = 3.461%, and goodness of fit = 3.534 (23 refined variables). The elevated goodness of fit and structured peak-shape residuals show that systematic instrumental/profile errors remain.

The available reference CIF was measured at 2.4 GPa. Its fractional coordinates produce chemically sensible MnO6 and WO6 octahedra and were retained, while the unit cell was initialized at ambient values and refined. Unconstrained coordinate refinement lowered Rwp but produced implausible Mn–O/W–O distances, so the powder data do not determine reliable independent atomic coordinates; the submitted CIF therefore contains the reference coordinates with the refined ambient cell. A zero-offset model fits almost as well as the specimen-height model and shifts cell lengths by several thousandths of an ångström, which is the main remaining metric uncertainty.
