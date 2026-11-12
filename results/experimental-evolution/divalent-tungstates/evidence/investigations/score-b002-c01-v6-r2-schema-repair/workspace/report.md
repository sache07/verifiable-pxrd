# Quantitative phase analysis

## Result

The pattern is modeled by three crystalline phases, normalized over the modeled crystalline material:

| Phase | Structure used | Weight fraction |
|---|---|---:|
| MgWO4, wolframite | COD 9013902, P 2/c | 51.37 wt% |
| WO3, monoclinic | COD 2311041, P 21/c | 41.21 wt% |
| MgO, periclase | COD 9000499, F m -3 m | 7.42 wt% |

The final full-range fit has Rwp = 2.392%, Rp = 1.824%, and GOF = 1.569. These fractions do not measure amorphous content because no external standard was supplied.

## Evidence and model selection

The chemical context (MgO + WO3 heated at 700 °C) supports MgWO4 formation with residual WO3 and MgO. MgWO4 accounts for the intense 18.9° line and coherent families throughout the range; WO3 accounts for the 23.1–24.4° cluster and the numerous broader families at middle and high angle; MgO is supported by the coherent periclase sequence near 42.9°, 62.3°, 74.6°, 78.8°, and 93.8° 2theta. Removing MgO raises Rwp to 3.064%; removing WO3 or MgWO4 raises it to 17.57% and more than 21%, respectively. All selected source models are ordered, fully occupied records with chemically sensible geometry. Exact entries existed, so analogue substitution was not needed.

Several physical WO3 records were compared under the same restrained nuisance model. The room-temperature monoclinic neutron structure (COD 2311041) was selected. A triclinic alternative (COD 2106293) remained worse after staged polarization and three full reconvergences (Rwp 2.598%, still less stable, versus 2.392% for the replay-stable monoclinic model); orthorhombic/high-pressure alternatives either fit much worse or drove profile terms to bounds.

The retained refinement uses a smooth six-term Chebyshev background, all phase scales and cells, one specimen shift (32.056 micrometres in the GSAS-II convention), common nonnegative U/W/X profile terms, and a refined polarization fraction (0.53649). MgWO4 has a replay-stable March-Dollase [010] correction (coefficient 1.30069); no texture raises Rwp to 7.114%, and the other tested axial/diagonal axes are substantially worse. WO3 requires isotropic microstrain (7960 microstrain); size alone is inferior, and combined size+strain is 93.5% correlated and gives no improvement. MgWO4/MgO size and strain, SH/L asymmetry, roughness, additional texture, and anisotropic broadening were rejected as unsupported, unstable, or bound-seeking. Atomic coordinates and occupancies were not refined.

## Uncertainty

The tabulated fractions are well supported as a three-phase crystalline inventory, but their realistic precision is limited by profile/texture and WO3-structure systematics. The formal covariance errors in `result.json` (about 0.07–0.10 absolute wt%) assume ideal Poisson statistics and are too optimistic; about 1–2 absolute wt% is a more defensible interpretation. Laboratory powder data do not uniquely prove the fine monoclinic-versus-triclinic distortion or detailed WO3 coordinates, although the selected ambient monoclinic model is both physically appropriate and the best stable fit. The smooth residual contains no coherent extra peak family requiring a fourth crystalline phase.
