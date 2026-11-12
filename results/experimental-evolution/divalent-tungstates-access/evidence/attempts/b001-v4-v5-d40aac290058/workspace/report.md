# Powder XRD phase analysis

## Result

The specimen is a four-phase crystalline mixture. Weight fractions are normalized over the modeled crystalline phases.

| Phase | Structural model and refined cell | Weight fraction | CIF |
|---|---|---:|---|
| CuWO4 | triclinic `P -1`; a = 4.622080, b = 5.747958, c = 4.859791 Å; alpha = 91.32421, beta = 91.48004, gamma = 84.70377 degrees | 0.657293 (65.729 wt%) | [phase_CuWO4.cif](phase_CuWO4.cif) |
| WO3 | monoclinic `P 21/c`; a = 7.685016, b = 7.559494, c = 10.508663 Å; beta = 136.00624 degrees (nonstandard but valid setting) | 0.184881 (18.488 wt%) | [phase_WO3.cif](phase_WO3.cif) |
| Cu3WO6 | cubic `P a -3`; a = 9.792087 Å | 0.131089 (13.109 wt%) | [phase_Cu3WO6.cif](phase_Cu3WO6.cif) |
| CuO | monoclinic `C 2/c`; a = 4.669934, b = 3.431257, c = 5.120841 Å; beta = 99.55661 degrees | 0.026736 (2.674 wt%) | [phase_CuO.cif](phase_CuO.cif) |

The full-grid Rietveld fit has Rwp = 2.0836%, Rp = 1.5969%, goodness of fit = 1.2945, and chi-square = 13795.35 for 8301 points and 69 refined parameters. The independently regenerated GSAS-II profile gives Rwp = 2.0836% and no profile-physics review flags.

## Evidence

CuWO4 is the dominant reaction product expected from the stated CuO/WO3 precursors at 700 degrees C. Exact-composition reference structures used as starting models were COD 4000806 (CuWO4), 2311041 (WO3), 1011194 (CuO), and 1527404 (Cu3WO6). The WO3 and CuO models account for broad families from unreacted precursor material.

After fitting CuWO4, WO3, and CuO, a coherent residual family remained at approximately 15.18, 19.80, 32.51, 33.78, 42.86, 49.70, 57.60, 63.29, 70.23, and 86.96 degrees 2theta. These reflections are jointly indexed by cubic Cu3WO6 with a positive stable scale; adding it lowered Rwp from 18.68% to 9.09% before coordinate and profile refinement. No coherent reflection family remains unassigned in the final four-phase fit.

The refinement used the reported Cu K-alpha doublet and intensity ratio, raw-count weights because pointwise uncertainties were not supplied, a smooth 16-term Chebyshev background, phase scales and cells, heavy-atom coordinates, and CuWO4 oxygen coordinates. Only supported size/strain terms were retained. Attempts to refine all minority-phase oxygen positions produced implausibly short bonds and were rolled back. Every submitted CIF passes the occupancy/contact screen; representative final distances are W-O = 1.79-2.17 Å in CuWO4, W-O = 1.70-2.18 Å in WO3, Cu-O = 1.95-1.96 Å in CuO, and W-O = 1.78-2.10 Å in Cu3WO6.

## Remaining uncertainty

The fractions quantify only the modeled crystalline material; this diffraction pattern cannot establish an amorphous fraction. Formal GSAS-II fraction standard uncertainties are about 0.018-0.028 wt%, but they omit model, absorption, preferred-orientation, and calibration systematics and are therefore too optimistic. The CuO phase is securely detected but, at only 2.67 wt% and with substantial overlap, its exact fraction is less reliable than those of the three larger phases and should be treated as semi-quantitative.

Fine oxygen coordinates in WO3, CuO, and Cu3WO6 cannot be determined reliably from this powder pattern; their physically screened reference oxygen frameworks were retained while cells and supported heavy-atom coordinates were refined. The CuO coherent-domain size also reached the imposed 1.5 micrometer upper bound and is not reliably determined. Sample displacement was held at +800 micrometers to avoid its strong correlation with zero and cell parameters, so absolute lattice-parameter uncertainties exceed the formal least-squares errors.
