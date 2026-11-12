# Powder XRD phase analysis

The pattern is best described by six crystalline phases. Weight fractions are normalized over these modeled crystalline phases; no amorphous fraction can be obtained from this measurement alone.

| Phase | Structural model | Weight fraction (wt%) |
|---|---|---:|
| PbWO4, scheelite | `I 41/a` | 55.35 (0.20) |
| Pb2WO5 | `C 2/m`, Pb2MoO5-type analogue | 12.28 (0.14) |
| Pb3WO6 | `P 21/n`, Ca3WO6-type analogue | 8.48 (0.21) |
| PbO, massicot | `P b c m` | 7.73 (0.15) |
| PbO, litharge | `P 4/n m m` | 6.44 (0.15) |
| WO3, monoclinic | `P 21/c` | 9.71 (0.13) |

Parentheses give conditional one-sigma covariance estimates in weight-percentage points. They do not include uncertainty from phase-model choice, peak overlap, absorption/microabsorption, or the assumed counting errors.

## Evidence and refinement

Scheelite PbWO4 accounts for the dominant reflection family. The remaining sharp families require both common PbO polymorphs and monoclinic WO3, consistent with residual PbO and WO3 precursors after heating at 500 °C. After those ordinary phases were fitted, coherent residual reflections near 25.9, 26.8, 30.1, and 31 degrees and their higher-angle partners were jointly explained by Pb2WO5 and Pb3WO6 models. Adding either model gave a positive, stable scale and broad multi-peak support. No additional coherent unindexed family remained in the six-phase residual; the largest residual features are predominantly derivative-shaped around fitted peaks.

Exact-composition reference structures were used for scheelite PbWO4 (COD 9009811), massicot PbO (COD 2310433), litharge PbO (COD 9012700, transformed to the standard origin), and monoclinic WO3 (COD 2311041). No suitable exact reference was available for the two intermediate lead tungstates. Pb2WO5 was therefore modeled from Pb2MoO5 (COD 7220560) by Mo/W substitution. Only after the other five phases left an unassigned family was Pb3WO6 modeled from the Ca3WO6 topology (COD 1563081) by Ca/Pb substitution and cell refinement. The final exported models have chemically plausible nearest-neighbor distances; unstable light-atom refinements that produced short contacts were rolled back.

The final full-grid refinement uses all 8,282 points from 10.0094 to 99.9944 degrees two-theta and the reported Cu K-alpha doublet. It gives `Rwp = 8.827%`, `Rp = 6.356%`, `Rexp = 3.491%`, and `Rwp/Rexp = 2.529` with 51 refined parameters. Because pointwise uncertainties were not supplied, Poisson counting uncertainties were assumed. Instrument-profile parameters are correlated, and Pb3WO6 requires about 0.99% isotropic microstrain.

## Remaining uncertainty

The presence of Pb2WO5 and Pb3WO6 is supported by reflection families and chemical balance, but their exact atomic structures cannot be determined reliably from this overlapped laboratory pattern. Their CIFs are physically constrained, analogue-derived working models, with oxygen coordinates retained from the prototypes. Consequently, their quoted fractions are conditional model estimates and are not reliable to the formal covariance precision; phase-model systematics could shift them by more than the parenthetical errors. The other four identities are substantially firmer, although all fractions remain conditional on the six-phase crystalline model. Minor phases below the residual/background sensitivity and amorphous material cannot be excluded.

`final.gpx` is the replayable GSAS-II project. `fit.csv` contains the observed, calculated, difference, and background profiles on the original measurement grid; `result.json` contains machine-readable paths, fractions, cells, provenance, and fit statistics.
