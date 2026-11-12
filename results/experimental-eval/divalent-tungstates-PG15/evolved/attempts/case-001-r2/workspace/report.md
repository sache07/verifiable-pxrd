# PXRD phase analysis

## Result

The best-supported crystalline model contains three phases. Fractions are normalized to the modeled crystalline material only.

| Phase | Refined space group | Weight % (formal esd) | Assessment |
|---|---:|---:|---|
| monoclinic WO3 | P 21/c (No. 14) | 46.135 +/- 0.163 | robust identity |
| orthorhombic BaCO3 (witherite) | P m c n (No. 62) | 53.192 +/- 0.162 | robust identity |
| scheelite BaWO4 (trace, provisional) | I 41/a (No. 88) | 0.673 +/- 0.052 | provisional trace |

The major-phase identities are secure. The two major fractions should be interpreted to roughly 1-2 wt% practical precision, not at the much smaller formal esds. BaWO4 is a credible trace assignment, but its exact structure and fraction cannot be determined reliably from this pattern alone; report it as approximately 0.7 wt% and near the detection limit. No amorphous fraction can be measured without an internal standard.

## Evidence and inventory challenge

Monoclinic WO3 accounts for coherent families at approximately 23.43, 23.91, 24.65, 33.57, 34.45, 41.74/42.12, 50.21 and 56.18 degrees 2theta. Orthorhombic witherite BaCO3 accounts for the independent 24.21, 24.57, 34.04/34.86, 42.29, 45.17, 47.08 and 55.02 degree families. Their cells and intensities remain physical when refined together.

Composition-, symmetry-, disorder- and geometry-screening favored COD 2311041 for WO3 and COD 9010928 for BaCO3. Under the same initial nuisance model, the selected WO3 record gave Rwp 8.884%, versus 9.167% for another monoclinic record, 9.645% for a triclinic record, 14.91% for an orthorhombic record, and 24.4-28.2% for tetragonal/hexagonal records. Alternative BaCO3 records either gave poor fits or collapsed toward zero scale.

The weak residual families at about 26.82 (112), 28.41 (004), 32.24 (200), 43.35 (204), 49.07 (116) and 54.89 degrees (224) are consistent with scheelite BaWO4. The available exact COD entry was occupationally disordered and produced an unphysical short contact, so a stoichiometric-analogue search was used: ordered scheelite BaMoO4 (COD 2300459) was converted by the isovalent Mo6+ to W6+ substitution and its cell was started from BaWO4. Atomic coordinates were kept fixed. A final fair re-challenge under the same common profile and BaCO3 texture lowered Rwp from 7.2954% (WO3 + BaCO3) to 7.2217% with BaWO4. This multi-family improvement supports retaining the phase, but it is small enough that the assignment remains provisional.

## Refinement and fit quality

The final full-range replay converged with Rwp = 7.2217%, Rp = 5.5990%, Rexp = 3.4807% and GOF = 2.078 (8301 points, 26 variables). The original counts were fit with Poisson 1/I weights because pointwise uncertainties were not supplied. The Cu Kalpha doublet and reported 0.5 intensity ratio were fixed.

The retained nuisance model consists of an eight-term smooth Chebyshev background, one Bragg-Brentano specimen shift (-525.27 micrometres), a common nonnegative U/X profile (U = 170.968, W = 0, X = 12.735), and refined effective polarization (0.7785). WO3 requires one replay-stable isotropic size term; BaCO3 requires a replay-stable [110] March-Dollase correction. Unused phase size/strain, roughness, transparency, extinction and anisotropic broadening were neutralized. A released SH/L asymmetry term gave negligible improvement and was strongly correlated with specimen shift, so it was pruned. Strong isolated low-angle peaks and middle/high-angle families show no systematic position drift; the remaining serial residual structure and some overlapping-family width/intensity mismatch explain why GOF exceeds one.

Only phase scales and cells, the supported WO3 size and BaCO3 texture terms, common profile/polarization, one angular correction, and background were refined. Atomic coordinates, occupancies and displacement parameters come from the screened reference structures/prototype and were not determined de novo. Consequently, the BaWO4 oxygen geometry in particular is a plausible structural model rather than a unique solution. The quoted fractions also exclude any unmodeled crystalline phase below detection and all noncrystalline material.

The submitted CIFs, `fit.csv`, fractions and statistics were exported directly from the final replayed `final.gpx`.
