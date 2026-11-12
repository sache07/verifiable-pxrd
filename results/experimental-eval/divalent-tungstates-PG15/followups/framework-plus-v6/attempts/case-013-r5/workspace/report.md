# Powder XRD phase analysis

## Result

The pattern is best represented by seven crystalline components. Fractions below are normalized over those modeled crystalline phases; the diffraction data do not determine any amorphous fraction.

| Phase model | Space group | Crystalline wt.% | Structural basis |
|---|---:|---:|---|
| PbWO4_scheelite (PbWO4) | I 41/a | 54.28 | published; COD 9009811 |
| PbO_massicot (PbO) | P b c m | 8.91 | published; COD 2310433 |
| Pb2WO5_C2m (Pb2WO5) | C 2/m | 12.22 | analogue-derived; Pb2MoO5 prototype, COD 7220560; Mo(VI) replaced by W(VI) |
| PbO_long_period (PbO) | P b c m | 7.52 | published approximant; COD 1533609 |
| Pb3O4_minium (Pb3O4) | P 42/m b c | 1.63 | published; COD 9012124 |
| WO3_monoclinic (WO3) | P 21/c | 10.65 | published; COD 2311041 |
| Pb2O3_repaired (Pb2O3) | P 21/c | 4.79 | repaired; Pb sublattice from COD 2311012; symmetry-constrained O sublattice repair |

The atomic-model replay of `final.gpx` gives Rwp = 9.290%, Rp = 6.752%, and goodness of fit = 2.659 over 8282 points. The saved GSAS-II refinement Rwp is 9.290%. The small distinction is due to regenerating reflection lists over the complete submitted grid for the verification profile.

## Evidence and model selection

PbWO4 scheelite accounts for the dominant peak families. Massicot PbO, monoclinic WO3, Pb2WO5, and the long-period alpha-PbO approximant each contribute coherent low-, middle-, and high-angle families; omitting the long-period PbO component raised Rwp by about 2.35 percentage points. Pb2WO5 was identified through the isovalent Pb2MoO5 prototype because no suitable exact database entry was available; the W-for-Mo substitution gives chemically reasonable W-O geometry and a stable positive scale.

The two smallest components were re-challenged against the common final profile. Removing Pb3O4 raises Rwp from 9.290% to 9.466%, while removing Pb2O3 raises it to 10.445%; both were therefore retained. Pb-deficient tungstate, raspite PbWO4, WO2, PbO2, and hydrated tungsten-oxide candidates either collapsed to zero/unstable scale or lacked chemically credible source conditions. A separate litharge PbO entry gave only a marginal improvement and duplicates the average structure represented by the long-period alpha-PbO model, so it was not counted as another phase.

The final baseline uses one specimen-displacement correction, a smooth eight-term background, and a common nonnegative U/W/X profile. Roughness, an extra zero correction, SH/L refinement, and unsupported texture terms were pruned. Residual-led width tests retained a tetragonal axial/basal size contrast for PbWO4 and a massicot b-axis/perpendicular contrast; Pb2WO5 and WO3 anisotropy trials were not stable enough to retain. Replay-stable March-Dollase terms for massicot [100] and Pb2WO5 [010] were retained. Exported structures were screened for occupancies and short contacts.

## Remaining uncertainty

The Pb2O3 identification and its 4.79 wt.% fraction are less reliable than the major-phase results. Its database record had an unphysical oxygen arrangement; the submitted model preserves the peak-supported Pb sublattice but uses a symmetry-constrained, distance-optimized O sublattice. Powder data at this phase abundance do not uniquely determine those oxygen coordinates, so the CIF is a physically admissible working model rather than a unique structure solution.

Pb3O4 is near the practical detection limit (1.63 wt.%), and its fraction is correspondingly sensitive to background/profile choices. The long-period PbO model reaches the imposed crystallite-size floor and needs large microstrain, so its detailed modulation and its 7.52 wt.% fraction are model-dependent; it should be interpreted as a long-period alpha-PbO approximant. The reported fractions are conditional on this crystalline inventory and likely carry systematic uncertainty of roughly 1–2 absolute wt.% for major components and proportionally more for the minor components.

The massicot b-axis coherence length itself was not bounded tightly by the data; only the breadth contrast was supported. Its weak axial degree was therefore pruned and fixed at a neutral 1 micrometre. No precise massicot axial crystallite dimension is claimed.

`fit.csv` is the complete-grid, fresh atomic replay of the submitted project (SHA-256 `b022c7419f159cb86ea0a26ca5c2619a5fd5b9d310729ae211d9c5c0001c8699`), with observed, calculated, and observed-minus-calculated columns.
