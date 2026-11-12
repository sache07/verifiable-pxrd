# PXRD phase analysis

## Result

The modeled crystalline material is a two-phase mixture of tetragonal barium peroxide and triclinic tungsten(VI) oxide. Weight fractions are normalized over these modeled crystalline phases; the experiment had no internal standard, so they do not quantify amorphous material.

| Phase | Space group | Refined cell | Crystalline weight fraction |
|---|---|---|---:|
| BaO2 | I4/mmm (No. 139) | a = 3.8128(2) Å, c = 6.8484(4) Å | 0.3262(19) |
| WO3 | P-1 (No. 2) | a = 7.3165(4), b = 7.5338(5), c = 7.6913(5) Å; alpha = 89.496(9), beta = 90.731(6), gamma = 90.298(8)° | 0.6738(19) |

The final full-pattern statistics are Rwp = 7.0551%, Rp = 5.3003%, Rexp = 3.6340%, goodness of fit = 1.9414, and chi-square = 31169.72 for 8301 observations and 31 refined variables. The refinement converged with no SVD-dropped variables and maximum shift/e.s.d. = 0.028.

## Evidence and model selection

The precursor chemistry restricts the principal search to Ba-W-O phases. The two selected atomistic models account for the peak positions and intensities over 9.90–100.09° 2theta using the metadata Cu Kalpha1/Kalpha2 wavelengths. Both precursor structures are required: leave-one-phase behavior leaves many strong, unique peaks, while the joint model gives positive stable scales.

The WO3 polymorph assignment was tested with identical mature nuisance models. Triclinic COD 2106293 gives Rwp 7.055%; monoclinic COD 2311041 gives 7.530%, and orthorhombic COD 2107312 gives 9.294% and does not converge. Tetragonal and hexagonal WO3 models were substantially worse in the initial matched screen. A second monoclinic entry and the available BaWO4 entry failed CIF geometry/duplicate-site audits and were rejected before quantitative use. The expected diagnostic BaWO4 intensity family is absent. Remaining positive residual maxima occur on peaks already assigned to BaO2 or WO3 rather than forming a coherent extra reflection family.

Refinement used a 10-term Chebyshev background, one specimen-shift correction, positive global U/X/Y width terms, polarization, weak one-axis March-Dollase corrections, isotropic BaO2 size, the BaO2 peroxide coordinate, and two element-grouped WO3 isotropic ADPs. Removing each retained term from the final model produces a reproducible complete-pattern degradation. Joint zero/shift refinement was rejected at 99.97% correlation. Added W, phase strain, WO3 size, and anisotropic BaO2 size branches were rejected because they were insignificant, correlated, boundary-seeking, or unstable.

## Structural checks and uncertainty

Both exported CIFs have full occupancies and plausible expanded structures. The WO3 CIF has no audit flags. The BaO2 audit flags its 1.452 Å O-O contact; this is the intended peroxide bond, not a duplicate-site collision, and the refined coordinate improves both the fit and peroxide geometry.

The parent WO3 atomic coordinates were retained because coordinate refinement was underdetermined and unstable; thus the data strongly determine the phase family and metric but do not independently redetermine every WO3 atom position. The covariance-only fraction uncertainty is about 0.19 wt% per phase. Profile/envelope and ADP branch sensitivity indicates a more realistic absolute uncertainty of roughly 1–2 wt%; microabsorption or unmodeled amorphous content could add systematic bias. Trace crystalline material hidden by overlap cannot be excluded, but no additional phase can be determined reliably from this pattern. Fractions should therefore be read as approximately 32.6 wt% BaO2 and 67.4 wt% WO3 on a modeled-crystalline-only basis.
