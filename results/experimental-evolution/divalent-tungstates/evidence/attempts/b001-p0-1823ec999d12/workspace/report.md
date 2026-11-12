# PXRD phase analysis

The pattern is described by four crystalline phases: scheelite PbWO4, monoclinic WO3, minium Pb3O4, and massicot PbO. The refined crystalline-phase fractions are:

| Phase | Space group | Weight fraction | Refined cell (angstrom, degrees) |
|---|---:|---:|---|
| PbWO4 (scheelite) | I 41/a | 58.40(17)% | a = 5.47271, c = 12.07243 |
| WO3 (monoclinic) | P 21/c | 20.62(12)% | a = 7.70075, b = 7.54417, c = 10.53611, beta = 136.1934 (alternate setting) |
| Pb3O4 (minium) | P 42/m b c | 16.42(17)% | a = 8.81024, c = 6.56990 |
| PbO (massicot) | P b c m | 4.57(9)% | a = 5.88586, b = 5.49669, c = 4.75337 |

Fractions are normalized to the modeled crystalline material; they do not quantify any amorphous component. Parentheses are formal one-standard-deviation least-squares uncertainties in the last digits, not estimates of total systematic error.

## Evidence

The chemical context (WO3 and Pb3O4 heated at 500 °C) supports formation of lead tungstate with residual oxide precursors and lead oxide. Scheelite PbWO4 accounts for the dominant line series near 27.81, 30.02, 33.16, 45.13, 47.37, 51.59, and 55.63° 2theta. Monoclinic WO3 accounts for the characteristic 23.53/24.02/24.84° triplet and the 33.66/34.05/34.60° cluster. Peaks near 14.67, 26.81, 31.22, 32.55, 50.25, and 52.52° require tetragonal Pb3O4. The remaining coherent set near 29.55, 30.82, 38.25, 45.57, 49.78, and 53.70° is matched by orthorhombic massicot PbO; tetragonal litharge did not provide a comparably stable or coherent match.

Adding chemically and crystallographically consistent phases reduced Rwp from about 8.23% for PbWO4 + WO3, to 5.46% after adding Pb3O4, and to 4.346% after adding PbO. Alternative triclinic/older monoclinic WO3 models and alternative Pb3O4 structures gave worse fits. No further unassigned peak series supports a fifth crystalline phase.

## Refinement and uncertainty

The final GSAS-II Rietveld fit used Cu Kalpha1/Kalpha2 wavelengths 1.540598/1.544426 angstrom with the reported 0.5 intensity ratio (despite the metadata's Kalpha1 intent), a 14-term Chebyshev background, and Poisson counting weights because point uncertainties were not supplied. A common zero correction of +0.4411° 2theta was refined. Phase scales, lattice parameters, and one effective isotropic size-broadening term per phase were refined in stages; atomic coordinates were held at the COD reference values. The source structures were COD 9009811 (PbWO4), 2311041 (WO3), 9012124 (Pb3O4), and 2310433 (PbO).

Final statistics are Rwp = 4.346%, Rp = 3.173%, Rexp = 2.486%, and Rwp/Rexp = 1.748 (chi-square = 3.055). The larger residual structure is concentrated around intense, overlapping peaks and is consistent mainly with imperfect line-shape modeling.

Because no calibrated instrumental profile or standard-derived broadening function was provided, the refined broadening terms should not be interpreted as reliable crystallite sizes. The atomic arrangements are reference-based phase models rather than independently solved structures. Severe overlap, possible preferred orientation/microabsorption, and the uncalibrated profile make the formal fraction uncertainties optimistic; systematic uncertainty is plausibly of order 1–2 absolute weight percent, with the 4.6% PbO fraction the least secure. A minor additional phase below roughly this level, especially if its peaks overlap, cannot be excluded.

`final.gpx` is the serialized project from which the submitted CIFs, fractions, and `fit.csv` were exported.
