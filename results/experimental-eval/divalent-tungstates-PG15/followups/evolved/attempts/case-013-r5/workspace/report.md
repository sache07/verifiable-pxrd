# Quantitative phase analysis

The pattern is modeled with eight crystalline phases. Fractions are normalized over the modeled crystalline material only; no amorphous fraction was measured.

| Phase | Space group/model | Weight % |
|---|---|---:|
| Scheelite PbWO4 | I41/a, COD 9009811 | 57.90(19) |
| Pb2WO5 | C2/m, Pb2MoO5 prototype with Mo6+ -> W6+ | 12.22(15) |
| Monoclinic WO3 | P21/n, COD 1528915 | 8.97(14) |
| Massicot PbO | Pbcm, COD 2310433 | 7.66(17) |
| Long-period alpha-PbO approximant | No. 57, COD 1533609 | 4.04(7) |
| Pb2O3, tentative | P21/c, geometry-screened COD 2311012 model | 4.57(11) |
| Pb3WO6 | Pnma, Pb3UO6 prototype with U6+ -> W6+ | 3.22(19) |
| Minium Pb3O4, weak | P42/mbc, COD 1537983 | 1.43(9) |

Parentheses are GSAS-II covariance-derived formal standard uncertainties on the last shown digits. They do not include model-selection, microabsorption, or prototype uncertainty and are therefore optimistic.

## Evidence

Scheelite PbWO4 accounts for the dominant families near 27.66, 29.88, 33.02, 44.99, 47.26, 55.52/56.79 degrees and their high-angle repeats. Monoclinic WO3 is supported by its resolved 23.36/23.84/24.63 degree triplet and families near 33.5-34.4 and 47.4-50.2 degrees. Massicot is required by families near 29.34, 30.56, 32.86, 38.06, 45.35, and 51.01 degrees. The long-period PbO model explains distinct lines near 28.85, 31.96/32.10, 35.95, 45.80, and 48.73/48.83 degrees and fits substantially better than the simple litharge record.

No exact Pb2WO5 or Pb3WO6 entry was available. Stoichiometric-analogue searches selected the closest same-valence parents. The retained Pb2MoO5 parent is a room-temperature single-crystal C2/m structure; Mo6+ -> W6+ preserves charge and coordination, and the substituted model has W-O distances of about 1.76-1.78 A. The Pb3UO6 parent provides the same Pb3M6+O6 chemistry; U6+ -> W6+ gives a physically plausible Pnma model with W-O distances about 1.89-2.19 A. Their refined cells remain close to the parent cells. Pb2WO5 contributes coherent families near 25.88, 26.73, 29.22/29.71, 30.63/31.02, and 34.85/35.36 degrees; the Pb3WO6 prototype contributes families near 26.62, 27.49, 29.07/29.47, 30.26, 34.43, 44.97, and 51.52 degrees.

The tentative Pb2O3 lattice explains the strong residual doublet near 30.16/30.30 degrees and additional families including 55.71 degrees. The sole exact COD model reports an impossible 1.34 A Pb-O contact. Changing O1 y from 0.964 to 0.164, treated as a probable one-digit transcription error and not refined, gives plausible mixed-valence Pb-O coordination. Pb3O4 is the weakest retained phase; partly independent families near 26.70, 31.04, 34.33, 46.46, 50.18, and 56.18 degrees support its positive scale.

Whole-pattern phase-deletion tests reconverged the common background, scales, zero, cells, and profile. Removing Pb2WO5, WO3, either PbO polymorph, or Pb2O3 raised Rwp from about 9.9% to 10.9-12.8%; removing Pb3WO6 or Pb3O4 raised it to about 10.05% or 9.99%, respectively. Raspite PbWO4 refined to zero. Alternative scheelite, WO3, and simple-litharge records were inferior under the same nuisance model.

## Refinement and uncertainty

The final full-range fit uses both reported Cu Kalpha wavelengths and the fixed reported 0.5 intensity ratio, a ten-coefficient smooth Chebyshev background, one zero correction, nonnegative W/X, and refined SH/L. U, V, and Y are zero. Size, roughness, extinction, and texture are neutral. Four symmetry-distinct scheelite texture axes all refined to March-Dollase coefficients of 0.992-1.002 and were removed. Only massicot isotropic microstrain was replay-stable and interior (3078 microstrain); all size trials and other strain trials were unsupported or bound-limited.

The final statistics are Rwp = 9.857%, Rp = 6.977%, Rexp = 3.502%, and GOF = 2.823 over 8282 points. Because pointwise uncertainties were not supplied, Poisson counting estimates, sigma = sqrt(max(counts, 1)), were used. The GOF above one and Durbin-Watson value of 0.286 show remaining correlated profile/intensity error, especially around the strongest PbWO4 peaks.

The PbWO4, WO3, massicot, and long-period PbO assignments are the most secure. Pb2WO5 is strongly required as a lattice/topology but its exact W/O coordinates are prototype-dependent. Pb3WO6 and Pb3O4 are weak and overlap other phases; their identities and fractions are less secure. The Pb2O3 atomic structure cannot be determined reliably from this mixture and should be regarded as a tentative lattice assignment with an approximate fraction. The long-period PbO CIF is a commensurate approximant; its incommensurate modulation was not refined. Atomic coordinates were otherwise held to source/prototype values, so the submitted CIFs are phase models with refined cells, not independent atomic-structure determinations.

All CIFs, fractions, and `fit.csv` were exported after reopening and replaying `final.gpx`; they correspond to that saved project state.
