# Powder XRD phase analysis

## Result

The modeled crystalline material is **99.4067 wt% MnWO4 wolframite** and **0.5933 wt% Mn2O3 bixbyite**, normalized over the two modeled crystalline phases. Formal covariance-based standard uncertainties are 0.1135 wt% for both complementary fractions; a more realistic rounded statement is about **99.4(2) wt% MnWO4 and 0.6(2) wt% Mn2O3** because background and profile choices add systematic uncertainty.

| Phase | Space group | Refined cell (A, degrees) | Crystalline weight fraction |
|---|---|---|---:|
| MnWO4, wolframite | P 2/c (No. 13) | a=4.831079, b=5.757432, c=4.996613, beta=91.21679 | 0.9940667 |
| Mn2O3, bixbyite | I a -3 (No. 206) | a=9.408637 | 0.0059333 |

The fit over all 8301 points from 9.9034 to 100.0949 degrees has Rwp=5.0116%, Rp=3.7449%, and GOF=1.4517 using weights 1/max(counts,1), since experimental point uncertainties were not supplied.

## Evidence and model selection

The dominant peaks, including the resolved low-angle groups near 23.8, 24.3, 30.1, and 30.5 degrees and the dense high-angle pattern, are all indexed by the P 2/c wolframite cell. The starting MnWO4 model was COD 1520200. That record was measured under pressure, so it was used as a topology rather than as an ambient-condition metric standard; ambient FeWO4, ZnWO4, and MgWO4 wolframite analogues were also screened and support the same framework. Cell, atomic coordinates, and one common isotropic displacement parameter were refined. All sites are fully occupied and the resulting geometry is physical: Mn-O distances are approximately 2.102, 2.144, and 2.296 A in pairs, and W-O distances are approximately 1.794, 1.916, and 2.137 A in pairs.

The weak Mn2O3 assignment is supported by separated bixbyite families near 33.2, 55.4, and 66.0 degrees, rather than by only an overlap with MnWO4. Its scale remains positive at about five formal standard deviations, and its fraction stays between 0.56 and 0.64 wt% when the smooth background order is varied. The accepted fully occupied Ia-3 model is COD 1514230; only its cubic cell and scale were refined because the phase is too weak to determine its atomic coordinates from this scan. Alternative Mn2O3 records give the same scale, while an orthorhombic model requires implausibly large cell distortion.

Mn3WO6 refined to the zero-scale boundary. Mn3O4 and MnO produced sub-0.2 wt% scales below useful significance and worsened penalized fit criteria. Several WO3 polymorphs obtained apparent scales of roughly 0.1-0.7 wt%, but their improvement came mainly from placing shoulders around the intense MnWO4 line near 23.8 degrees; they overpredicted other strong, candidate-specific families. WO3 is therefore retained only as an unresolved watch-list possibility, not reported as a phase. Its structure and fraction cannot be determined reliably from this pattern; the practical upper limit is of order 1 wt% and is strongly overlap-dependent.

## Refinement and remaining uncertainty

The final GSAS-II model uses the reported Cu Kalpha1/Kalpha2 wavelengths and fixed 0.5 intensity ratio, one specimen-displacement correction (-443.5 micrometers), a nonnegative U/W/X common profile with U fixed at its zero boundary, refined SH/L asymmetry, and a strictly positive smooth 18-coefficient Chebyshev background over the full 90-degree span. Higher background orders lowered least squares slightly but introduced extra turning points and were rejected. A one-parameter physical surface-roughness correction and weak [110] March-Dollase term (1.0295) are supported by multiple MnWO4 families. Polarization refinement was unsupported and was fixed at 0.75. Size and strain trials either collapsed to zero or were exactly confounded with the common Lorentzian X term, so phase size and microstrain were neutralized; crystallite size cannot be determined reliably here.

The largest remaining correlated residuals occur around the strongest low-angle MnWO4 peaks, while isolated middle- and high-angle families have consistent positions, widths, and asymmetry. Thus the formal fraction errors likely understate profile/background systematics, especially for Mn2O3. Fractions refer only to the modeled crystalline material: this scan cannot quantify amorphous content or a chemically plausible phase below its diffraction detection limit.

The submitted `final.gpx` was reopened and replayed without optimization. Independent native GSAS-II regeneration gave Rwp=5.0116012%, exactly reproduced both reported fractions, found no negative background or peak-width flags, and confirmed that both submitted CIFs match the saved project structures.
