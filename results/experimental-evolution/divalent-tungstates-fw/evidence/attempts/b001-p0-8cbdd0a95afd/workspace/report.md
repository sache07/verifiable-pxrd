# Powder XRD phase analysis

The pattern is modeled as a single crystalline phase: scheelite CaWO4 (space group I 41/a), at a normalized crystalline weight fraction of 1.000000 (100.00 wt%). The refined cell is a = b = 5.244270 A, c = 11.379681 A, V = 312.968 A^3. The independent oxygen coordinate is (0.150189, 0.009921, 0.211520).

Evidence: all resolved Bragg peaks, including 18.63, 28.72, 29.04, 31.43, 34.18, 39.20, 47.11, 54.29, and 57.88 degrees 2theta, index to the scheelite cell with the expected Cu Kalpha1/Kalpha2 splitting. Diagnostic lines for residual CaO (notably near 37.3 and 53.8 degrees), monoclinic WO3 (the 23.1-24.4 degree cluster), and Ca3WO6 (strong low-angle lines near 18.9-22.2 degrees) are absent. Adding texture, surface roughness, anisotropic strain, or extra smooth-background terms did not give physically supported improvements.

The fresh atomic-model replay of `final.gpx` gives Rwp = 3.5450% and chi-square = 8270.59 over 8301 points (Poisson deviance 8252.05); no negative background, displacement tensor, or peak-width flags were found. `fit.csv` was generated from this replay rather than from cached profile arrays.

Uncertainty: 100 wt% is normalized only over the modeled crystalline phases; it does not quantify amorphous material or absolute reaction yield. A trace, strongly overlapped crystalline impurity below practical detection cannot be excluded. The Ca/W framework and lattice are well constrained by this laboratory X-ray pattern, while oxygen coordinates are less precise and correlated with intensity/profile terms. Instrumental Lorentzian broadening and isotropic crystallite-size broadening are mathematically non-unique here, so the profile was retained but no unique size interpretation is claimed.
