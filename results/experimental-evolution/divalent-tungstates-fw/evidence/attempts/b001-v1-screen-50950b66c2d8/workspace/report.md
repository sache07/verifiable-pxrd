# Powder XRD phase analysis

The pattern is modeled with four crystalline phases. Weight fractions are normalized over these modeled crystalline phases only.

| Phase | Structural source | Space group | Weight fraction |
|---|---|---:|---:|
| CaWO4, scheelite | COD 7219229 | I 41/a | 0.63489 |
| WO3, triclinic | COD 2106293 | P -1 | 0.26711 |
| CaCO3, calcite | COD 1547347 | R -3 c | 0.06597 |
| CaO, rocksalt | COD 1563196 | F m -3 m | 0.03202 |

## Evidence and model selection

Scheelite CaWO4 accounts for the strong family at 18.69, 28.80, 31.65, 34.19, and 47.21 degrees 2theta. WO3 accounts for the independent split family at 23.21, 23.66, 24.45, 26.65, 29.18, and 33.33 degrees. Under an identical fixed-coordinate, low-flexibility refinement, the physically passing triclinic WO3 parent gave Rwp 11.91%, compared with 12.16% for the best passing monoclinic parent, 15.34% for orthorhombic WO3, and 22.35% for tetragonal WO3. An older monoclinic source with four O--O contacts at 1.57 A was rejected by the supplied physical screen.

Calcite was supported by a multi-line residual family at 29.52, 36.05, 39.53, 43.25, 47.57, 48.58, and 60.69 degrees. With CaO included, deleting calcite worsened the common low-flexibility fit from Rwp 11.35% to 11.69%. After the three-phase model was stabilized, residuals at 32.26, 37.42, 53.88, 64.15, 67.37, 79.60, 88.47, and 91.39 degrees identified rocksalt CaO; adding it improved low-flexibility Rwp from 11.75% to 11.35%. Aragonite and vaterite tests gave near-zero/unstable scales and negligible improvements. The refined phase inventory gives an approximate Ca:W molar ratio of 1.02, a chemistry check that was not used to constrain the fractions.

The retained profile terms were a specimen displacement, common positive U/W/X/Y widths, polarization, approximately 85 nm isotropic WO3 size, and weak WO3 [001] March--Dollase texture (ratio 1.068). Negative microstrain solutions, an unphysical/correlated roughness branch, and highly correlated extra phase-size terms were rejected. Atomic refinement was last and selective: the scheelite O site and one well-determined WO3 W site were refined; all other sites stayed at their published parents. Joint refinement of all WO3 W sites drifted on restart and was rejected.

## Fit and uncertainty

Independent no-refinement replay of `final.gpx` gives Rwp 3.98498%, Rp 3.09151%, and goodness-of-fit 1.44018 with Poisson count weights. Fresh replay fractions exactly match `result.json`; all four submitted CIFs match the project and pass the supplied geometry/occupancy screen. The replay reports no negative background, width, displacement-tensor, or polarization flags.

Fractions were stable across constant-zero/specimen-shift and six/eight-term-background restarts: the largest fraction change was about 0.16 percentage point. This spread is an internal model-sensitivity check, not a complete uncertainty interval; the two trace fractions should be regarded as less precise than the major-phase fractions. The absolute cells retain a small calibration-versus-displacement systematic uncertainty. The exact WO3 oxygen geometry is not reliably determined by this powder pattern and therefore remains the published parent geometry. No amorphous fraction or absolute crystalline yield can be determined from these data.
