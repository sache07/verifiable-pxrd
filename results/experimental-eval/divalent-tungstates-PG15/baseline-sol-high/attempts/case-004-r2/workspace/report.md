# PXRD phase analysis

The pattern is modeled as two crystalline phases: **32.03 wt% CoWO4** and **67.97 wt% WO3**, normalized over the modeled crystalline material. The formal GSAS-II scale-factor uncertainty is 0.14 wt% for either fraction. This is much smaller than the likely systematic uncertainty; without an internal standard, calibrated instrumental profile, or microabsorption correction, a practical uncertainty of several weight percent is more realistic. An amorphous fraction cannot be determined from these data.

## Evidence

Monoclinic WO3 (P 21/c) explains the characteristic three-peak group at approximately 23.18, 23.67, and 24.42 degrees 2theta, the 33-34.3 degree multiplet, and the strong groups near 50-56 degrees. Wolframite CoWO4 (P 2/c) accounts for the reflections near 19.09, 30.71, 36.44, 44.40, 52.15, and 65.15 degrees. These assignments are chemically consistent with the reported CoO/WO3 precursors and 900 degrees C heating.

CoO and Co3O4 trial assignments were rejected: their strongest expected reflections near 42.4 degrees (CoO) and 36.85/59.36 degrees (Co3O4) are not present with the required relative intensities. No third crystalline phase is required by the residual. Trace material at roughly the 1-3 wt% level cannot be excluded because a detection limit was not measured.

## Refinement and limitations

GSAS-II refinement used the metadata Cu K-alpha1/K-alpha2 wavelengths and fixed 0.5 intensity ratio, Poisson weights inferred from the measured counts, a 15-term Chebyshev background, and the 10-100 degrees 2theta interval. Phase scales, both unit cells, zero offset, and empirical profile terms were refined. The Co and W positional parameters supported by the CoWO4 pattern were refined; oxygen positions and the WO3 internal coordinates were held at literature starting values because the overlapping laboratory pattern does not constrain them reliably. The refined cells are:

- CoWO4: a = 4.66736 A, b = 5.68370 A, c = 4.95052 A, beta = 89.9921 degrees.
- WO3: a = 7.69230 A, b = 7.53652 A, c = 10.5355 A, beta = 136.109 degrees (an alternate monoclinic P 21/c setting).

The final fit has Rp = 4.831%, Rwp = 6.401%, Rexp = 3.283%, and goodness of fit = 1.954. Remaining structured residuals are concentrated in heavily overlapped peak groups and likely reflect the uncalibrated instrumental profile, preferred-orientation/microabsorption effects, and fixed light-atom coordinates. Thus the phase identities and two-phase interpretation are reliable, while detailed oxygen geometry and sub-percent fraction precision are not.
