# Powder X-ray diffraction analysis

The pattern is explained by three crystalline phases: monoclinic WO3 (56.06 wt%), calcite CaCO3 (31.38 wt%), and scheelite CaWO4 (12.56 wt%). These fractions are normalized over the modeled crystalline material; they do not quantify any amorphous content.

## Evidence

- The dominant 23.4–24.7° triplet and its accompanying reflection families through the full angular range match monoclinic P21/c WO3. The refined COD 2311041 topology gave the best physical same-composition model; alternative WO3 polymorphs either misplaced or over-split these families.
- Calcite accounts for the characteristic reflections near 29.7°, 39.7°, 43.5°, and 48.8°. Its refined R-3c cell and C–O geometry remain physical.
- Scheelite CaWO4 accounts for the independent low-angle reflection near 18.9° and its families near 29°, 34°, 47°, and higher angles. Its refined I41/a geometry is physical.
- This inventory is chemically ordinary for partial reaction of CaCO3 and WO3 at the reported 500 °C. After all three phases were included, remaining residuals were chiefly peak-shape/intensity discrepancies at already indexed reflections rather than a coherent unassigned reflection family.

The full-grid GSAS-II replay gives Rwp = 7.3253%, Rp = 5.3795%, chi-square = 77627.85, and goodness of fit = 3.066 for 8,293 points. The project explicitly uses the reported Cu Kalpha1/Kalpha2 wavelengths and intensity ratio. Refined unit cells are a = 5.24526, c = 11.38466 A for CaWO4; a = 4.99080, c = 17.07412 A for calcite; and a = 7.69633, b = 7.54102, c = 10.54802 A, beta = 136.1423° for WO3.

## Uncertainty

The phase identities and three-phase inventory are reliable. Covariance-only fraction standard uncertainties are about 0.12–0.16 percentage point, but these understate systematic uncertainty from overlapping peaks, preferred orientation, profile calibration, and the absence of supplied pointwise uncertainties or an external standard. Oxygen coordinates are less strongly constrained than the phase topologies and cells. No additional crystalline phase is required by a coherent residual family, although trace crystalline material and amorphous content cannot be excluded reliably.

`final.gpx`, the three CIFs, and `fit.csv` were all exported or regenerated from the same saved physical checkpoint; `fit.csv` reports observed minus calculated intensity in its difference column.
