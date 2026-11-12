# Powder X-ray diffraction phase analysis

## Result

| Crystalline phase | Structural model | Weight fraction* |
|---|---|---:|
| ZnWO4, wolframite type | monoclinic `P 2/c` | 69.88% |
| WO3, gamma/room-temperature monoclinic form | monoclinic `P 21/n` | 22.77% |
| ZnO, wurtzite | hexagonal `P 63mc` | 7.35% |

\*Fractions are normalized over the modeled crystalline material. No internal standard was present, so an amorphous fraction or absolute mass balance cannot be determined.

The full-pattern GSAS-II fit over 10–100 degrees 2-theta, including the supplied Cu Kalpha1/Kalpha2 wavelengths and intensity ratio, gives `Rwp = 3.706%`, `Rp = 2.850%`, `Rexp = 2.692%`, and `Rwp/Rexp = 1.377` for 8,301 points.

## Evidence

The dominant wolframite ZnWO4 model accounts for the characteristic 19.19, 24.71, 30.73/30.97, and 36.58 degree features and the dense higher-angle pattern. Monoclinic WO3 is required by the resolved 23.45/23.90/24.08 degree group, together with lines near 26.91, 28.95/29.28, and 33.58/33.89/34.48 degrees. Wurtzite ZnO is independently supported by lines at approximately 32.07, 34.73, 47.84, 56.87, 63.16, 68.22, and 69.32 degrees, despite overlap of its strongest line near 36.6 degrees.

This inventory is also chemically consistent with partial reaction of the stated ZnO and WO3 precursors to ZnWO4. The refined residual WO3:ZnO molar ratio is about 1.09:1, close to the 1:1 consumption expected for `ZnO + WO3 -> ZnWO4`.

Starting models were taken from database structures: ZnWO4 was adapted from the closely related Zn/Cd wolframite COD 1520642, monoclinic WO3 from COD 1528915, and wurtzite ZnO from COD 9004178. Cells, profile terms, phase scales, selected atomic positions, and the instrumental/sample terms were refined in stages. WO3 required moderate [001] preferred orientation (March-Dollase ratio 1.379); competing WO3 structures left systematic unmatched intensities. All submitted CIFs agree numerically with the structures in `final.gpx` and pass broad contact and occupancy checks.

## Remaining uncertainty

Formal one-sigma scale-covariance errors are only about 0.05–0.06 weight-percentage points, but they do not include structural-model, preferred-orientation, absorption, or background systematics. The reported hundredths therefore document normalization rather than absolute accuracy; approximately percent-level accuracy is a more realistic interpretation of the fractions. The phase identities and three-phase inventory are secure because each phase has several diagnostic reflections.

The exact oxygen coordinates, especially in WO3 and in the analogue-derived ZnWO4 model, are less uniquely determined than the phase identities and lattice parameters because many intensities overlap and powder data alone provide limited oxygen sensitivity in these W-rich phases. The WO3 oxygen sublattice was kept within a physically screened neighborhood of the literature model rather than treated as an unconstrained structure solution. ZnO peak broadening is instrument-limited and its refined crystallite-size value reaches the model's upper bound, so that size cannot be determined reliably. No claim is made for unmodeled amorphous material.
