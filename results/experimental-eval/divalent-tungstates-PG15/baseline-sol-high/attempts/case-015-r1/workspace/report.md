# PXRD phase analysis

## Result

The crystalline pattern is modeled with three phases:

| Phase | Space group | Weight fraction* |
|---|---:|---:|
| ZnWO4 (wolframite) | P 2/c | 76.22% |
| WO3 (monoclinic) | P 21/n | 16.13% |
| ZnO (wurtzite) | P 63mc | 7.65% |

\*Normalized over the modeled crystalline phases only. No internal standard was present, so an amorphous fraction cannot be measured.

The final GSAS-II Rietveld fit has Rwp = 6.37%, Rexp = 3.79%, GOF = 1.68, and Rp = 4.94% over 8284 observations (10-100 degrees 2theta). The Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio were fixed to the metadata values. Because pointwise uncertainties were absent, counting-statistical weights (sigma = sqrt(counts)) were used.

## Evidence

ZnWO4 accounts for the dominant wolframite line set, including the strong features near 18.98, 24.62, 30.69, 36.50, 51.86, and 53.77 degrees 2theta, and is the expected reaction product of ZnO and WO3 at 900 degrees C. Monoclinic WO3 accounts for the characteristic group near 23-25 degrees and additional reflections near 33-34 and 41 degrees. Wurtzite ZnO is supported by its 31.8/34.4/36.3-degree group and higher-angle lines. Under an identical initial protocol, ZnWO4 alone gave Rwp about 18.0%; ZnWO4 + WO3 gave 10.85%; adding ZnO reduced this to 10.05% and gave a low ZnO Bragg R factor. Refining the physically bounded polarization correction and the major-phase coordinates produced the submitted 6.37% fit.

The starting structures were COD 1520641 (ZnWO4), COD 1528915 (WO3), and COD 9004178 (ZnO). Unit cells and phase scales were refined for all phases. Coordinates were refined only for the 76 wt% ZnWO4 phase; minor-phase coordinates were retained from the reference structures because the overlapping laboratory pattern does not determine them independently.

## Remaining uncertainty

The formal least-squares fraction uncertainties are only about 0.1 wt%, but they understate the practical uncertainty. There is no calibrated instrumental profile, no supplied intensity uncertainties, and no particle-size information for a microabsorption correction; the W-rich phases and ZnO have substantially different absorption. The effective polarization was also unspecified: an unconstrained refinement moved above the physical range, so it was fixed at the physical upper bound (1.0). Fractions changed by less than 0.3 wt% between polarization treatments, but a practical uncertainty of roughly 1-2 wt% per phase is more realistic.

Closely related monoclinic/triclinic WO3 descriptions fit nearly equivalently; the higher-symmetry P 21/n model (an alternate setting of the source P 21/c structure) was selected on parsimony and chemical plausibility, so the exact room-temperature WO3 distortion is less certain than the WO3 phase assignment. Residual serial correlation (Durbin-Watson = 0.78) indicates remaining profile/intensity systematics. No additional phase is uniquely required by the residual; a weak, strongly overlapped impurity below roughly 1-2 wt% could remain undetected.
