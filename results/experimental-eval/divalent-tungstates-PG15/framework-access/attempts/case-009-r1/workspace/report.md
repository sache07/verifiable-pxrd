# Powder XRD phase analysis

## Result

The crystalline pattern is adequately described by one phase: wolframite-type **MnWO4**, space group **P 2/c**, at a weight fraction of **1.000 (100 wt%) after normalization over the modeled crystalline phases**. No second crystalline phase can be quantified reliably.

The refined MnWO4 cell is `a = 4.83201 A`, `b = 5.75874 A`, `c = 4.99793 A`, `beta = 91.2196 deg`, and `V = 139.042 A^3` (`Z = 2`). The submitted atomic model is in `phase_MnWO4.cif`.

## Evidence and refinement

The Mn3O4 + WO3 precursor chemistry and 900 C treatment are consistent with MnWO4 formation. A P 2/c wolframite parent model (COD 1520200) accounts for the full peak inventory, including the strong observed maxima near 18.63, 23.85, 24.31, 30.07, 30.53, 36.22, and 37.45 degrees 2theta. The cell and atomic coordinates were then refined against the supplied scan.

The GSAS-II model uses the stated Cu Kalpha1/Kalpha2 doublet and Bragg-Brentano geometry, a smooth log-interpolated empirical background, surface roughness, crystallite-size broadening, and [001] uniaxial microstrain. The final whole-pattern statistics are `Rwp = 3.72755%`, `Rp = 2.87663%`, and `GOF = 1.08397` for 8,301 points (104 refined parameters; weights `1/max(Iobs,1)`). An independent replay from `final.gpx`, using fresh reflection lists and atomic structure factors rather than saved calculated arrays, reproduced these statistics and all calculated values in `fit.csv` to numerical precision.

Explicit trial additions of Mn3WO6 and WO3 refined to effectively zero. Mn3O4 refined to only 0.153(120) wt% and changed Rwp by 0.00034 percentage point, so it is not a significant detection and was omitted. In this particular candidate model, about 0.5 wt% is an approximate three-sigma upper bound for Mn3O4.

## Remaining uncertainty

The reported 100 wt% is relative only to the modeled crystalline material; amorphous content is not measured by this normalization, and trace crystalline phases below the pattern-dependent detection limit cannot be excluded. The Mn3O4 bound is not a universal detection limit for every possible impurity. Instrumental `U` reached its allowed upper bound, and specimen displacement and zero offset are strongly correlated, so the refined broadening and alignment nuisance parameters should not be interpreted uniquely. These limitations do not materially affect the one-phase identification, but uncertainties on the powder-refined atomic coordinates and microstructure are larger than the CIF's printed numerical precision implies.
