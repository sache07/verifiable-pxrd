# Powder XRD phase analysis

The pattern is described by three crystalline phases: monoclinic WO3, scheelite CaWO4, and calcite CaCO3. The crystalline-phase-normalized fractions are 55.57 wt% WO3, 12.20 wt% CaWO4, and 32.24 wt% CaCO3. This is chemically consistent with partial reaction of the CaCO3/WO3 precursor mixture after 1 h at 500 °C.

The monoclinic WO3 model (P 21/c, COD 2311041) accounts for the intense 23.42/23.90/24.67° triplet and the associated 33.57–34.46°, 50.21°, and 56.19° families. In otherwise identical checkpoint fits it outperformed a second monoclinic reference (COD 1528915) and triclinic WO3 (COD 2106293): Rwp was 21.52%, 23.04%, and 34.38%, respectively, before later profile refinements. Scheelite CaWO4 (I 41/a, COD 7219229) is supported by its 18.91°, 29.03°, 31.72°, and higher-angle families. Calcite (R -3 c, COD 1547347) is independently supported by peaks at 29.71°, 39.71°, 43.46°, 47.77°, 48.77°, 57.68°, and 64.92°. After these phases were included, no coherent residual reflection family remained to justify another crystalline phase.

The final full-grid fit has Rwp = 7.327%, Rp = 5.378%, and goodness of fit = 3.066 (expected Rwp from counting statistics: 2.394%). The independently regenerated GSAS-II profile gives Rwp = 7.327% and passes the project physical/profile checks without review flags. Refined cells are:

- WO3: a = 7.68987 Å, b = 7.53467 Å, c = 10.5391 Å, beta = 136.143°.
- CaWO4: a = 5.23911 Å, c = 11.3777 Å.
- CaCO3: a = 4.98648 Å, c = 17.0593 Å.

The quoted fraction e.s.d.s in `result.json` are conditional least-squares values (0.14, 0.08, and 0.16 wt percentage points) and understate systematic uncertainty. Sample height and the instrumental U term reached the supplied physical bounds, and phase broadening/texture overlap remains correlated with scale. Thus the inventory and fraction ordering are robust, but the last decimal places of the fractions are not; a few wt% systematic uncertainty is more realistic. Fractions exclude any amorphous material.

The phase topologies and cells are reliable. Exact light-atom coordinates, especially the WO3 oxygen positions, are less well determined by this overlapped powder pattern. WO3 oxygen shifts were bounded to the stated reference-mismatch scale; larger unconstrained shifts were rejected despite a small Rwp gain. CaWO4 and calcite oxygen-coordinate releases did not improve the accepted checkpoint and their reference positions were retained. The submitted structures remain chemically physical, but these detailed oxygen coordinates and displacement parameters should not be interpreted as a unique structure determination.
