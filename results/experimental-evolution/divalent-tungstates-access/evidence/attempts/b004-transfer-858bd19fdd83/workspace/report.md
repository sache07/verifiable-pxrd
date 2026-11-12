# Powder XRD phase analysis

The pattern is described by three crystalline phases. Weight fractions are normalized over these modeled crystalline phases:

| Phase | Space group | Weight fraction |
|---|---:|---:|
| Ba3W2O9 | R-3c (No. 167) | 0.7137 (~71.4 wt%) |
| WO3 | P21/c (No. 14) | 0.2366 (~23.7 wt%) |
| BaCO3 | Pnma (No. 62) | 0.0498 (~5.0 wt%) |

The dominant broad reflection family at approximately 17.72, 26.20, 27.70, 30.78, 40.75, 42.96, and 53.67 degrees 2theta identifies rhombohedral Ba3W2O9; the starting model was COD 1533878. The sharper triplet near 23.35, 23.82, and 24.62 degrees and its higher-angle reflections identify monoclinic WO3. Several WO3 records were tested; COD 2311041 gave the best whole-profile agreement, and the refined model remains close to that parent. Weak independent reflections require residual orthorhombic BaCO3 (COD 9010928). Adding BaCO3 reduced the preliminary three-parameter-family Rwp from 11.21% to 9.38%; an alternative BaCO3 model (COD 1011149) refined toward zero abundance and fit substantially worse.

The final GSAS-II model includes Cu Kalpha1/Kalpha2 radiation, a refined zero offset, physically bounded instrumental broadening, phase-specific size/strain, and March-Dollase [110] texture for Ba3W2O9 and WO3. Symmetry-constrained coordinate adjustments are small and consistent with the stated reference-model variability. All exported structures pass the supplied hard-contact and oxide oxygen-contact screens.

Independent atomic replay of `final.gpx` gives Rwp = 2.511%, Rp = 1.854%, and a mean weighted squared residual of 1.192 using weights 1/max(observed,1), with no replay review flags. The remaining excess residual is concentrated mainly in the overlapping 33–35 degree WO3/BaCO3 multiplet; no additional phase has a distinct unexplained peak set.

The phase identities are reliable. Conservative absolute fraction uncertainties are about 1–2 wt% for the two major phases and about 0.5–1 wt% for BaCO3 because scale, displacement parameter, and texture are correlated. Oxygen coordinates, especially in the minor carbonate, are less certain than the heavy-atom framework. The fractions exclude any amorphous material, which cannot be quantified from this scan without an internal standard.
