# PXRD phase analysis

The crystalline pattern is modeled as **wolframite ZnWO4 (P 2/c)**, **monoclinic WO3 (P 21/c)**, and **wurtzite ZnO (P 63 m c)**. The refined crystalline-phase fractions are 82.73 wt% ZnWO4, 12.11 wt% WO3, and 5.16 wt% ZnO, normalized to these three modeled phases. The complete-grid atomic forward replay of `final.gpx` gives Rwp = 3.03%, Rp = 2.22%, Rexp = 2.65%, and goodness of fit = 1.15; it produced no profile-review flags.

## Evidence

- The dominant peak set indexes and refines as wolframite ZnWO4, with a = 4.69966 A, b = 5.73120 A, c = 4.93041 A, and beta = 90.6381 degrees. An isostructural wolframite model was adapted to Zn and refined. A strong [111] March-Dollase texture term (ratio about 0.706) is required by the relative intensities.
- The secondary peak set is explained by monoclinic WO3 in the supplied P 21/c setting, with a = 7.70097 A, b = 7.51816 A, c = 10.5315 A, and beta = 136.074 degrees. A [110] texture term (ratio about 1.373) is also supported. Under the same constrained workflow this monoclinic model fit better than a triclinic WO3 alternative.
- Residual peaks near 32.0, 34.9, and 36.6 degrees, together with the corresponding higher-angle reflections, identify residual wurtzite ZnO. Its refined cell is a = 3.25390 A and c = 5.18041 A. Adding ZnO reduced the independently replayed Rwp from 4.84% to 3.03%; its refined crystallite size is about 0.062 micrometers, consistent with the broad weak peaks.
- All three submitted structures pass the geometry/occupancy screen. The submitted CIFs, phase fractions, and profile were regenerated from and checked against the saved final GSAS-II project.

## Uncertainty

The three-phase inventory is well supported, including the minority ZnO phase. Strong preferred orientation, correlated background/surface terms, nanoscale ZnO broadening, and peak overlap make the formal least-squares fraction errors optimistic; a realistic systematic uncertainty is roughly +/-2--3 wt% absolute for the major phases and about +/-1 wt% for ZnO. Fractions exclude amorphous material, which cannot be quantified without an internal standard.

The cells and W/Zn substructures are more reliable than individual oxygen coordinates. Oxygen positions in the 12 wt% WO3 phase are weakly constrained by laboratory X-ray data and were kept to modest, physically screened displacements from a published monoclinic model. The ZnO internal oxygen coordinate and isotropic displacement parameter were not independently determined reliably and were retained at physically plausible reference/fixed values. Monoclinic WO3 is preferred over triclinic WO3, but that polymorph distinction is less secure than the overall phase inventory. The fitted zero and specimen displacement are strongly correlated, with displacement near its search bound, so those calibration terms are not independently reliable.
