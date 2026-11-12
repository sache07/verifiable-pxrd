# Powder XRD phase analysis

The pattern is described by three crystalline phases. Fractions are normalized over those modeled crystalline phases.

| Phase | Structural assignment | Weight fraction |
|---|---|---:|
| ZnWO4 | wolframite type, P 2/c | 0.81210 (81.21 wt%) |
| ZnO | wurtzite type, P 63 m c | 0.05315 (5.32 wt%) |
| WO3 | monoclinic, P 21/c | 0.13475 (13.48 wt%) |

## Evidence

The synthesis context (ZnO + WO3, 700 °C) and the dominant peak series support wolframite ZnWO4. Its refined cell is a = 4.70416 Å, b = 5.73660 Å, c = 4.93516 Å, beta = 90.6380°. Coherent residual series from ordinary reference fitting require both wurtzite ZnO (a = 3.25684 Å, c = 5.18557 Å) and monoclinic WO3. The WO3 CIF uses a valid non-reduced P 21/c setting with a = 7.70842 Å, b = 7.52556 Å, c = 10.5416 Å and beta = 136.073°.

The selected full-grid GSAS-II replay gives Rwp = 2.7523%, Rp = 2.0488%, Rexp = 2.6464%, and goodness of fit = 1.0400 over all 8301 points. A separate native atomic replay regenerated the reflection lists and reproduced `fit.csv` to numerical precision without optimizing any parameter. The remaining positive and negative extrema are sparse and distributed among existing reflections rather than forming a coherent additional peak series.

Preferred orientation is needed for the intensity balance: March-Dollase ratios are 0.7067 along [111] for ZnWO4, 1.2013 along [100] for ZnO, and 1.4000 along [110] for WO3. Phase additions were tested with the other phases and nuisance parameters fixed in the same common project. Triclinic, scheelite and C2/c ZnWO4 transfers; cubic and rocksalt ZnO; alternative WO3 references; W2O7/W3O8/W18O49; and ZnO2 either collapsed or refined to at most about 0.05 wt%, so no fourth crystalline phase is justified. Several low-symmetry replacement refinements aborted with invalid metrics; those failed trials remain unknown and were not used as rejection evidence. Completed replacement/replay fits were appreciably worse than the submitted model.

All exported CIFs pass the broad occupancy/contact screen. Minimum O-O distances are 2.510 Å (ZnWO4), 3.203 Å (ZnO), and 2.538 Å (WO3). The refined coordination distances are chemically plausible: W-O = 1.821-2.179 Å and Zn-O = 1.986-2.210 Å in ZnWO4; Zn-O = 1.977-1.981 Å in ZnO; and W-O = 1.698-2.177 Å in WO3.

## Remaining uncertainty

The phase identities are reliable, but the quoted fractions are model-dependent rather than absolute assay values. They exclude any amorphous material, and systematic uncertainty from texture, peak broadening and displacement factors is likely larger than the scale-only statistical errors (roughly 1-2 absolute wt% is a realistic caution, especially for the minor phases). WO3 texture reaches the allowed upper bound, while ZnWO4 and WO3 isotropic displacement factors select opposite allowed bounds; this chiefly limits confidence in exact fractions and ADPs, not in phase presence.

ZnWO4 coordinates and the WO3 W positions were refined while maintaining physical geometry. The ZnO internal coordinate and WO3 oxygen framework were retained from physical references because unconstrained light-atom refinement was not independently reliable from this laboratory powder pattern. No additional phase structure or fraction can be determined reliably from the residual.
