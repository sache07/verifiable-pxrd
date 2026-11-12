# Powder XRD phase analysis

## Result

The specimen is a three-phase crystalline mixture. Fractions are normalized over the modeled crystalline material:

| Phase | Structure | Weight fraction |
|---|---|---:|
| MgWO4 | wolframite, P 2/c | 0.7738 (77.4 wt%) |
| WO3 | monoclinic, P 21/c | 0.1417 (14.2 wt%) |
| MgO | rocksalt, F m -3 m | 0.0845 (8.5 wt%) |

The refined cells are MgWO4: a = 4.69356, b = 5.67774, c = 4.93143 A, beta = 90.7770 degrees; WO3: a = 7.69637, b = 7.54188, c = 10.5373 A, beta = 136.094 degrees (a valid nonstandard monoclinic setting); and MgO: a = 4.21470 A.

## Evidence and refinement

The MgO + WO3 precursor chemistry and 900 C heat treatment support formation of MgWO4 with residual reactants. The dominant observed family at approximately 19.24, 24.22, 30.81/31.12, 36.79, 41.86, 54.61, and 62.02 degrees 2theta is indexed by wolframite MgWO4. Monoclinic WO3 is independently required by its resolved 23.43/23.93/24.67 degree cluster and many weaker reflections. Rocksalt MgO is required by the coherent 43.21, 62.54, 75.05, and 94.25 degree family. Once these three phases were included, the remaining prominent residuals lay at already assigned peak positions rather than forming another indexable family.

Starting structures were COD 9013902 (MgWO4), COD 2311041 (WO3), and COD 9000499 (MgO). Alternative exact-composition WO3 references were tested before coordinate refinement; COD 2311041 gave the best physical checkpoint fit (Rwp 10.279%, versus 10.615% and 10.607% for the closest alternatives). The final GSAS-II refinement used the supplied Cu K-alpha1/K-alpha2 wavelengths and ratio, with background, scales, specimen displacement, zero, cells, bounded profile/size/strain terms, weak MgWO4 preferred orientation, coordinates, and one isotropic displacement parameter per phase refined in controlled stages. All submitted structures pass the geometry/occupancy screen and have chemically sensible nearest-neighbor distances.

Fresh atomic forward replay of `final.gpx` over all 8301 observations gives Rwp = 8.325%, Rp = 6.214%, chi-square = 70207.23, and goodness of fit = 2.914. The saved final refinement cycle reports Rwp = 8.317%; the small difference is from regenerating reflection lists rather than using GSAS-II's cached calculated array. `fit.csv` contains the independently replayed profile.

## Uncertainty

The three phase identifications are reliable, but the last digits of the fractions are not. Conditional least-squares e.s.d.s are 0.16, 0.08, and 0.17 percentage points for MgWO4, WO3, and MgO, respectively; they exclude model, overlap, preferred-orientation, absorption, and profile uncertainty. A more realistic practical uncertainty is about 1–2 absolute percentage points for each reported fraction. The fractions do not quantify amorphous material because no internal standard was supplied. Cell metrics and phase topology are substantially better determined than individual oxygen coordinates, especially in WO3, and some size/instrument broadening terms reached their imposed physical bounds. No fourth crystalline phase can be determined reliably from the remaining residual.
