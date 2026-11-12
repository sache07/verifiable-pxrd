# Powder X-ray diffraction phase analysis

## Result

The crystalline specimen is modeled by two phases:

| Phase | Space group | Refined cell in the submitted setting | Crystalline weight fraction |
|---|---|---|---:|
| monoclinic gamma-WO3 | P 21/c | a = 7.69329 Å, b = 7.53670 Å, c = 10.53570 Å, beta = 136.1008° | 67.35(16)% |
| wolframite CoWO4 | P 2/c | a = 4.66894 Å, b = 5.68402 Å, c = 4.95016 Å, beta = 90.0040° | 32.65(16)% |

Fractions are normalized over these modeled crystalline phases. The experiment has no internal standard, so an amorphous fraction or absolute crystalline yield cannot be determined.

## Evidence and refinement

The Cu K-alpha doublet and reflection geometry from `metadata.json` were used. A physical P 21/c gamma-WO3 reference (COD 2311041) accounts for the dominant reflection families. The remaining coherent families index as P 2/c wolframite CoWO4, consistent with reaction of the stated CoO and WO3 precursors at 900 °C. The CoWO4 model began from the isostructural ZnWO4 topology (COD 1520641), because the available old exact-composition CoWO4 record (COD 5910316) contains duplicated symmetry-equivalent sites. Its low-precision unique coordinates nevertheless independently agree with the final Co/W and O positions.

Cells, phase scales, specimen displacement, isotropic crystallite-size terms, background, and small March-Dollase corrections were refined. Heavy-atom coordinates were refined first. Oxygen coordinates were moved only by a bounded step toward the powder least-squares direction and then fixed. Final coordination is ordinary: WO3 W-O = 1.77-2.14 Å; CoWO4 W-O = 1.84-2.13 Å and Co-O = 2.06-2.14 Å. The refined size terms are 0.0634 µm for WO3 and 0.0973 µm for CoWO4; the March-Dollase ratios are 1.0785 along WO3 [110] and 0.9459 along CoWO4 [001].

All coherent residual reflection families are assigned by these two phases. Fixed-positive tests for residual Co3O4 and CoO worsened the fit monotonically from the two-phase baseline, even after re-optimizing background and major-phase scales. They therefore have no reliable positive phase fraction and were not included.

The final read-only replay of `final.gpx` regenerated the complete 8,301-point profile from atomic models with no physical review flags. Full-grid Rwp is 5.60997% and Rp is 4.32955%; GSAS-II Rwp over the 10-100° refined range is 5.61823% (GOF 1.71).

## Remaining uncertainty

The formal phase-fraction standard uncertainty is about 0.16 percentage point, but it does not include systematic uncertainty from preferred orientation, line-shape assumptions, or reference coordinates. The robust interpretation is therefore approximately 67.3 wt% WO3 and 32.7 wt% CoWO4 among crystalline material. Trace CoO or Co3O4 below roughly the 0.1-0.2 wt% level cannot be excluded reliably. Oxygen coordinates and atomic displacement parameters are not independently precise enough for a detailed bonding or thermal-motion interpretation.
