# PXRD phase analysis

The 750 °C product is modeled as four crystalline phases. Fractions are normalized over these modeled crystalline phases only.

| Phase | Structural model | Weight fraction |
|---|---|---:|
| BaWO4 | scheelite, I4_1/a | 0.6523 (65.23 wt%) |
| Ba3W2O9 | R-3c | 0.1575 (15.75 wt%) |
| WO3 | monoclinic, P2_1/c | 0.1161 (11.61 wt%) |
| BaCO3 | orthorhombic, Pnma-equivalent setting | 0.0741 (7.41 wt%) |

The full 9.9034–100.0946° 2θ replay gives Rwp = 5.520%, Rp = 3.826%, Rexp = 3.017%, and goodness of fit = 1.830 using Poisson counting weights. The metadata Cu Kα1/Kα2 wavelengths (1.540598/1.544426 Å) and 0.5 intensity ratio were fixed. No refined variable is frozen or at a bound in `final.gpx`.

## Evidence

BaWO4 accounts for the dominant scheelite families, including 26.70°, 28.39°, 32.05°, 43.20°, and 53.68°. Ba3W2O9 is required by independent families near 17.76°, 26.28°, 27.80°, 30.82°, 37.66°, 40.80°, 51.84°, 63.07°, and 63.83°. Monoclinic WO3 accounts for the characteristic 23.40°/23.86°/24.66° group and additional families near 33.55°–34.46°, 50.22°, and 56.23°. BaCO3 has replay-stable positive scale and non-coincident evidence near 19.71°, 27.99°, and 34.81°, in addition to overlapping families near 24.2°, 42.27°, and 45.12°.

BaCO3 remains at about 7.2–7.6 wt% under smooth-background and texture challenges after its supported isotropic strain is retained. Its scale stays positive when all texture is removed. A second standardized Pnma record (COD 1011149) gives only about 0.6 wt% and a poorer cell/intensity match; Ba3WO6 collapses to zero scale. Alternative WO3 records and tetragonal, orthorhombic, and triclinic polymorphs were worse than COD 2311041. No same-formula coexistence was retained.

The final profile uses a 10-term smooth background, specimen shift as the sole angular correction, common nonnegative W/X broadening, symmetry-compatible Ba3W2O9 c-axis microstrain, and isotropic WO3 and BaCO3 microstrain. Size and combined size/strain trials failed or ran to nonphysical limits. Polarization, roughness, U, and all March-Dollase texture trials either hit a bound or became negligible after BaCO3 was added, so they were removed.

An isolated-family shape audit (degrees 2θ; left/right values are half-widths at half maximum) was:

| Family | Observed position | Calculated position | Observed L/R | Calculated L/R | Observed/calculated FWHM |
|---|---:|---:|---:|---:|---:|
| low-angle BaWO4 112 | 26.7029 | 26.7029 | 0.0718 / 0.0770 | 0.0728 / 0.0759 | 0.1487 / 0.1487 |
| mid-angle BaWO4 024 | 43.1872 | 43.1981 | 0.0621 / 0.1333 | 0.0711 / 0.1223 | 0.1954 / 0.1934 |
| high-angle BaWO4 152 | 90.4343 | 90.4343 | 0.0667 / 0.0716 | 0.0634 / 0.0638 | 0.1384 / 0.1272 |

## Structural and quantitative uncertainty

All submitted CIFs pass `learned/cif_health.py`. The BaWO4 CIF is an ordered I4_1/a model adapted from the isovalent SrWO4 topology (COD 1546036) with Sr2+ replaced by Ba2+. The only exact BaWO4 record in the filtered index (COD 1527204) contains two half-occupied oxygen alternatives, 1.17 Å alternative-site O···O contacts, and an implausibly short W–O alternative. It can lower Rwp to 5.36% when coupled to [001] texture, but its neutral-source ranking reverses and the gain is an intensity/texture surrogate rather than positional evidence. Ordered BaMoO4- and EuWO4-derived competitors were also tested. Unconstrained oxygen-coordinate refinement drove W–O to about 2.15 Å and was rejected. Consequently, BaWO4 topology and cell are reliable, but its oxygen coordinates are parent-anchored and are not determined precisely by this mixture pattern.

The quoted GSAS-II fraction standard uncertainties are about 0.17–0.30 percentage point and do not include source/profile systematics. The split-site BaWO4 competitor shifts the four fractions to approximately 62.6/17.1/12.6/7.7 wt%, while omitting supported BaCO3 broadening lowers its estimate to about 5.1 wt%. A realistic model systematic is therefore roughly ±3 percentage points for BaWO4, ±1.5 for Ba3W2O9, ±1 for WO3, and ±2 for BaCO3. Atomic coordinates of the minor phases were retained from health-screened records; only cells, scales, and supported profile terms were refined. No precursor amount or ratio was reported, so no numerical mass-balance constraint was imposed. Residual peaks are dominated by intensity mismatch at already modeled BaWO4 families rather than a coherent additional phase family.
