# Powder XRD phase analysis

The modeled crystalline inventory is monoclinic WO3 (P 21/c), 46.07 wt%, and orthorhombic witherite BaCO3 (Pnma), 53.93 wt%. Fractions are normalized over these two crystalline phases; they do not include any amorphous material.

| Phase | Structural basis | Refined cell (angstrom, degrees) | Weight fraction |
|---|---|---|---:|
| WO3 | COD 2311041, P 21/c | a=7.31617, b=7.54651, c=10.55286, beta=133.1283 | 0.46069 |
| BaCO3 | COD 9010928, Pnma | a=6.44056, b=5.31463, c=8.92524 | 0.53931 |

## Evidence and model selection

The chemistry (BaCO3 + WO3, 400 degrees C) permits unreacted precursors and BaWO4 product. The observed WO3 families at approximately 23.44, 23.92, 24.68, 34.47, and 50.97 degrees 2theta, and distinct BaCO3 families near 34.88, 42.31, 47.08, and 68.88 degrees, are reproduced coherently over the full 9.90--100.09 degree scan. Under a common neutral profile, the selected WO3 record fitted better than tested monoclinic and triclinic alternatives; an alternate record's poor scale was not treated as rejection of the composition. Both submitted structures are ordered, fully occupied, and pass the geometry screen (minimum interatomic separations 1.742 and 1.276 angstrom for WO3 and BaCO3, respectively).

BaWO4 (COD 1527204) was retained on the watch list and reintroduced after the common profile was established. With an instrument-limited width it refined to only 0.245 wt% and lowered Rwp by 0.034 percentage point. Although its cell shift was plausible, its nominally unique strong families near 32.23, 69.35, and 96.79 degrees did not improve the local residual. Allowing its size to vary from three starts always collapsed to the 0.04 micrometre lower bound and changed its apparent fraction to about 0.9 wt%, showing that it was acting as a broad residual surrogate. It is therefore not included quantitatively. A very broad, sub-percent BaWO4 contribution cannot be ruled out, and neither its structure nor fraction can be determined reliably from this pattern.

## Refinement and uncertainty

The final full-range Rietveld model uses a smooth positive eight-coefficient Chebyshev background, one effective angular-zero correction (+0.36221 degrees), a common nonnegative U/W/X profile with U=10 and X=1 fixed to remove size/strain degeneracy, refined W and SH/L, isotropic WO3 size/strain, and supported BaCO3 [010] strain and weak [010] March-Dollase texture. Roughness and axis-ambiguous WO3 anisotropy were rejected. W and Ba coordinates were refined; unstable light-atom trials were rejected, so O and C coordinates retain their source-model values. The WO3 isotropic displacement value was fixed at 0.005 square angstrom because refinement drove it to a physical bound; one common BaCO3 Uiso refined to 0.01454 square angstrom. Consequently, oxygen positions and the last digits of the fractions are not independently determined.

The parameter-free native replay of `final.gpx` gives Rwp=6.8739%, Rp=5.3645%, chi-square=32373.61, and GOF=1.9790 over all 8301 points, with no replay review flags. The formal scale-only uncertainty is about 0.2 wt%, but profile/polarization/ADP correlations make a roughly percent-level interpretation more realistic; the defensible result is approximately 46 wt% WO3 and 54 wt% BaCO3. The saved project was reopened and reconverged before export, and the submitted CIFs agree with its full-precision phase models.
