# Powder XRD phase analysis

The crystalline pattern is modeled as **75.10 wt% monoclinic WO3** (P 21/c) and **24.90 wt% orthorhombic Mn2O3** (Pbca), normalized over the modeled crystalline material. The fresh atomic replay of `final.gpx` gives Rwp = 5.874%, Rp = 4.269%, and goodness of fit = 2.209 with weights 1/max(observed counts, 1).

## Evidence

The strong WO3 contribution accounts for the resolved low-angle group near 23.4, 23.9, and 24.7 degrees 2theta and the associated reflections throughout 30-100 degrees. The remaining reproducible peaks, including the Mn2O3 features around 33, 38, 45, 50, 55, and 66 degrees, require the second phase. Removing either phase leaves structured residual peaks. MnWO4 and Mn3WO6 models did not account for those residuals. A second P21/n WO3 component could absorb about 2 wt% and lower Rwp only from 5.874% to 5.850%, but its crystallite size collapsed to the 0.04 micrometre lower bound and it supplied no uniquely resolved peaks. It is therefore not reliably distinguishable from residual peak-shape mismatch and was not included as a determined phase.

Several WO3 references/settings were tested. The selected P 21/c model fit substantially better from physically small parent-structure perturbations than P21/n, Pnma, P21/m, or P-1 alternatives. A nominally competitive P-1 fit required oxygen displacements far outside the stated reference-mismatch scale and was therefore rejected. For Mn2O3, Pbca was modestly but consistently better than the higher-symmetry cubic alternative after coordinate refinement.

Refined cells are a = 7.69489 A, b = 7.53888 A, c = 10.54776 A, beta = 136.1606 degrees for WO3, and a = 9.40606 A, b = 9.41386 A, c = 9.42699 A for Mn2O3. The fit includes the Cu K-alpha doublet, a -400 micrometre specimen-height term, 0.09723 degree zero term, phase-dependent size/strain, and weak WO3 preferred orientation. Both exported CIFs pass the supplied occupancy/contact screen and agree numerically with the phases in `final.gpx`.

## Remaining uncertainty

The scale covariance alone gives about 0.16 percentage points one-sigma uncertainty, but profile/background and polymorph correlations dominate; about +/-2 percentage points is a more realistic uncertainty for each crystalline fraction. The fractions do not quantify amorphous content. Trace crystalline phases below roughly 1-2 wt% cannot be excluded.

The heavy-atom frameworks and phase assignments are reliable, while exact oxygen coordinates are less well determined by this laboratory X-ray pattern. Oxygen shifts were therefore regularized toward the published parent structures within the stated reference-mismatch scale. The non-noise-floor residual (Rwp 5.87% versus Rexp 2.66%) indicates remaining profile/structural mismatch, so the submitted oxygen positions should not be interpreted as a uniquely determined high-precision structure.
