# PXRD phase analysis

The crystalline sample is modeled as **78.52 wt% NiWO4** and **21.48 wt% WO3**, normalized over the two modeled crystalline phases. The formal GSAS-II 1-sigma uncertainty is 0.08 wt% for each fraction. A more realistic uncertainty is about 1 wt% absolute because no instrumental profile calibration, internal standard, or supplied pointwise uncertainties were available. Amorphous content cannot be determined from this analysis.

## Evidence

Monoclinic wolframite-type NiWO4 (P 1 2/c 1) accounts for the dominant 30.87° line and the characteristic reflections near 19.19, 24.85, 36.52, 41.63, 44.70, 54.58, and 65.78° 2theta. Monoclinic WO3 (P 1 21/n 1) is required by the strong residual triplet at 23.06, 23.53, and 24.28° and supporting lines at 26.53, 28.82, 33.20, 34.09, 49.87, and 55.88°. Starting structures were based on COD 5910277 (NiWO4, reduced to independent symmetry sites) and COD 1528915 (room-temperature monoclinic WO3), followed by structural and profile refinement in GSAS-II.

The final fit over 10.009-99.994° has Rwp = 5.194%, Rp = 4.052%, Rexp = 3.479%, goodness of fit = 1.495, and reduced chi-squared = 2.236. The refined cells are:

- NiWO4: a = 4.59964 Å, b = 5.66115 Å, c = 4.90902 Å, beta = 89.9909°, V = 127.827 Å³.
- WO3: a = 7.30073 Å, b = 7.53177 Å, c = 7.68734 Å, beta = 90.8233°, V = 422.663 Å³.

## Remaining uncertainty

A triclinic WO3 test gave no fit improvement (Rwp = 5.196%) despite substantially more variables and produced strong coordinate correlations, so the simpler P 1 21/n 1 assignment is preferred. A NiO test refined to only 0.08(11) wt% with negligible fit improvement; NiO is therefore not detected reliably and is omitted. Weak residual structure and the low Durbin-Watson statistic indicate correlated profile mismatch, so the quoted formal fraction uncertainties should not be interpreted as total uncertainty. Atomic coordinates are suitable as powder-refined models, but oxygen positions—especially in WO3—are less certain than the phase identities and lattice parameters.

Cu Kalpha1/Kalpha2 wavelengths and their 0.5 intensity ratio were fixed to the metadata values. In the absence of supplied uncertainties, Poisson counting weights were used. `final.gpx` is the project used to generate both CIFs, `fit.csv`, and `result.json`.
