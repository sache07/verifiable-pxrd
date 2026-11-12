# Powder XRD phase analysis

The crystalline pattern is described by two phases: wolframite CoWO4 at **29.77 wt%** and triclinic WO3 at **70.23 wt%**, normalized over the modeled crystalline material. No additional crystalline phase is supported at a reliable level.

| Phase | Space group | Refined cell | Crystalline wt% |
|---|---|---|---:|
| CoWO4 (wolframite) | P 2/c | a = 4.67001 A, b = 5.68443 A, c = 4.94999 A, beta = 90.0065 deg | 29.77 |
| WO3 (triclinic) | P -1 | a = 7.30757 A, b = 7.53671 A, c = 7.69314 A, alpha = 89.7586 deg, beta = 90.7969 deg, gamma = 90.2116 deg | 70.23 |

## Evidence and model selection

The CoO + WO3, 900 C context makes CoWO4 product plus residual WO3 chemically plausible. Triclinic WO3 accounts for the dominant split peaks at approximately 23.18, 23.67, and 24.42 deg 2theta and the coherent families near 33.3--34.3 and 47--50 deg. Wolframite CoWO4 accounts for independent or partly separated families near 19.07, 23.89/24.73, 30.71, 36.50, 41.46, and 52.12 deg, as well as their high-angle repeats.

The inventory was challenged with several monoclinic/orthorhombic WO3 records, a second wolframite analogue, CoO, and Co3O4 under the same restrained nuisance model. Triclinic WO3 gave the best physical profile. CoO and Co3O4 refined to zero scale and had no coherent unique residual families, so they were rejected rather than reported as trace phases.

No exact CoWO4 entry was available in the supplied index. Its model was therefore made by the chemically conservative Mo-to-W substitution in isostructural CoMoO4-II (same Co framework, P 2/c), then physically screened and refined. The final Co--O distances are 2.031--2.166 A and W--O distances are 1.794--2.130 A. The triclinic WO3 model is based on COD 2106293; its final W--O distances span about 1.716--2.210 A.

## Refinement and uncertainty

The final GSAS-II refinement uses the complete 9.9034--100.0949 deg scan, Poisson count weights, the stated Cu Kalpha1/Kalpha2 wavelengths and ratio, a smooth 10-term Chebyshev background, one specimen-displacement correction, and a common nonnegative U/W/X profile. Unsupported roughness, texture, microstrain, and extra phases were pruned. Only a replay-stable isotropic WO3 size term (0.205 micrometre) was retained. The fit has Rwp = 5.19655%, Rp = 4.00211%, and goodness of fit = 1.58669 (8,301 points, 26 refined parameters). A fresh atomic forward replay of `final.gpx` reproduces that Rwp and both phase fractions over the full grid without profile review flags.

The formal GSAS-II standard uncertainty on either fraction is 0.11 percentage point, but this understates source-structure and profile systematics. Candidate and nuisance-model sensitivity supports a more realistic uncertainty of roughly +/-2 wt percentage points: about 30(2) wt% CoWO4 and 70(2) wt% WO3. These fractions exclude any amorphous content.

Phase identification and the heavy-atom frameworks are well supported, but the oxygen coordinates are less certain. CoWO4 oxygen positions remain those of the substituted parent, and WO3 oxygen positions remain those of the selected record; freely refining all oxygen coordinates reduced Rwp only by producing implausible bonds. Residual intensity mismatches and polarization at its physical boundary likewise limit claims of high-precision atom positions. Thus the CIFs are appropriate phase/fraction models, not definitive oxygen-coordinate determinations.
