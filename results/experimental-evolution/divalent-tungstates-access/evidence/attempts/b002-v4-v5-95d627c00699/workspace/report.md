# Powder XRD phase analysis

The crystalline model contains **ZnWO4 wolframite (85.36 wt%)** and **monoclinic WO3 (14.64 wt%)**. Fractions are normalized over these modeled crystalline phases; without an internal standard, amorphous material and absolute crystalline content cannot be quantified.

## Evidence

ZnWO4 in space group P2/c accounts for the dominant pattern, including the strong families near 19.2, 24.1–24.8, 31.0, 36.7, 50–55, and 64–65° 2θ. The frozen reference index did not contain exact-composition ZnWO4, so the model was initialized from the isostructural wolframite-type CoMoO4 topology with Co→Zn and Mo→W, then its cell and bounded atomic coordinates were refined. Its final cell is a = 4.70889, b = 5.74079, c = 4.93934 Å, beta = 90.6211°. The final geometry has no short nonbonded contacts (minimum O–O 2.64 Å; W–O 1.92–2.32 Å).

Residual families at approximately 23–25, 33–34, 41–42, 50, and 55–62° are jointly indexed by monoclinic WO3 (P21/c). The submitted physical reference setting has a = 7.72495, b = 7.53556, c = 10.55171 Å, beta = 136.0535°; this is an alternative monoclinic setting. Bounded W-coordinate refinement retained physical WO3 geometry (minimum O–O 2.54 Å and W–O 1.68 Å). A superficially better WO3 checkpoint based on a different reference was rejected because it contained an unphysical 1.58 Å O–O contact. ZnO was also tested, but its scale repeatedly refined to zero and it did not explain a coherent residual family.

Relative intensities require March–Dollase preferred orientation for ZnWO4 along [111] (ratio 0.719) and WO3 along [110] (ratio 1.329). Isotropic domain sizes are about 0.097 and 0.223 µm, respectively. No positive, stable microstrain or surface-roughness term was supported.

## Fit and uncertainty

An independent full-grid forward replay of `final.gpx` gives Rwp = 11.044% and Rp = 7.008% over all 8,301 measured points. Every coherent reflection family is assigned; remaining residuals are mainly relative-intensity and overlap errors rather than a distinct unindexed phase.

The principal uncertainties are systematic. The analogue-derived ZnWO4 oxygen coordinates and the weak-phase WO3 displacement factor sit near imposed physical bounds. WO3 Uiso and scale are correlated, so its 14.64 wt% fraction is less secure than the displayed digits; a practical uncertainty is roughly 1–2 wt% absolute. The bounded calibration uses zero = +0.25° and specimen displacement = −320 µm; these remain strongly correlated with both cells. Consequently, the phase identities are well supported, but detailed light-atom coordinates, absolute lattice calibration, and minor-phase fraction should not be interpreted at high precision.
