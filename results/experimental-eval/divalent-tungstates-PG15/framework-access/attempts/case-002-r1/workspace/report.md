# Powder XRD phase analysis

## Result

Two crystalline phases account for the pattern. Fractions are normalized over these modeled crystalline phases.

| Phase | Structure | Refined cell | Weight fraction |
|---|---|---|---:|
| BaO2 | tetragonal I4/mmm, COD 1010113 | a = 3.80606 Å, c = 6.82482 Å | 33.59 wt% |
| WO3 | monoclinic P21/c, COD 2311041 | a = 7.29697 Å, b = 7.51283 Å, c = 10.52413 Å, beta = 133.219° | 66.41 wt% |

The fresh, zero-parameter replay of `final.gpx` over all 8301 measured points gives Rwp = 8.480%, Rp = 6.336%, weighted chi-square = 45031.6, and chi-square/N = 5.425 (nominal GOF = 2.329). The counting-statistical Rwp floor estimated by GSAS-II is 3.641%. `fit.csv` is the replayed observed/calculated/difference profile, with difference defined as observed minus calculated.

## Evidence

The 23.4–24.7° triplet and the extensive higher-angle reflection set require distorted low-temperature WO3. Tetragonal BaO2 accounts for the strong reflections near 26.29°, 26.99°, 33.45°, 42.93°, and 47.92°. Under the same bounded profile treatment, the profile-only WO3 comparisons gave Rwp 8.70% for P21/c (COD 2311041), 8.86% for triclinic P-1 (COD 2106293), and 9.35% for the P21/n candidate (COD 1528915). Bounded coordinate refinement retained the P21/c preference.

BaWO4 is not supported: its diagnostic reflection near 31.9° is absent, and an explicit three-phase refinement drove the BaWO4 fraction to approximately 7e-14 while slightly worsening the fresh Rwp. No additional crystalline phase was retained.

## Uncertainty and limitations

The phase fractions were stable near 34:66 across the plausible WO3 models; a realistic model-sensitivity uncertainty is about ±2 wt% absolute for each fraction. This is not a formal standard uncertainty because pointwise experimental uncertainties were not supplied. The fractions exclude any amorphous material.

The P21/c assignment is preferred but not unique: the triclinic alternative is close enough that the WO3 polymorph should be regarded as moderate-confidence. Oxygen coordinates and isotropic displacement parameters are weakly determined by this broadened Cu X-ray pattern; oxygen shifts were therefore regularized to the stated reference-variation range and Uiso was retained at 0.005 Å². The BaO2 peroxide O–O distance is about 1.36 Å, as expected for peroxide; it triggers a generic short O–O review rule but is not an impossible contact.

Zero offset, specimen displacement, lattice parameters, and peak broadening are strongly correlated. Several profile terms reached their imposed bounds, so those nuisance values and the last digits of the refined cells are not independently reliable even though their combined profile is reproducible. The submitted CIFs, fractions, and `fit.csv` are exactly tied to the replay-verified `final.gpx`.
