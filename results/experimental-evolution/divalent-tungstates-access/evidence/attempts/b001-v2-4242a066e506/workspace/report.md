# Powder XRD phase analysis

The crystalline model contains three phases. Weight fractions are normalized over these modeled crystalline phases; no amorphous fraction can be obtained from this scan without an internal standard.

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| ZnWO4, wolframite | P 2/c | a = 4.70242, b = 5.72887, c = 4.93997, beta = 90.5988 | 0.75062 |
| WO3, monoclinic | P 21/c | a = 7.30346, b = 7.53876, c = 10.52458, beta = 133.0291 (nonconventional setting) | 0.18490 |
| ZnO, zincite | P 63mc | a = b = 3.25625, c = 5.22040 | 0.06448 |

The full 9.903–100.095° profile has Rwp = 3.041% and Rp = 2.255% using Poisson counting weights. The final read-only GSAS-II forward replay reproduced `fit.csv` and the fractions exactly, with no negative background, negative peak-width, occupancy, or contact flags.

## Evidence

The strongest lines at 18.99°, 24.60°, 30.52/30.76°, 36.44°, and 38.37° identify wolframite ZnWO4. A P 2/c FeWO4 framework was transferred to Zn and refined. Common-state tests of same-stoichiometry triclinic CuWO4-derived and tetragonal scheelite-derived ZnWO4 models fit substantially worse, so the wolframite assignment is well supported.

Monoclinic WO3 accounts for the coherent precursor lines near 15.59° and the 23.2–24.0° cluster. Multiple ordinary WO3 references were compared in the same multiphase state; the retained P 21/c framework gave the best completed physical fit. One triclinic WO3 trial did not complete and therefore remains unknown rather than rejected.

In a two-phase fit, positive residuals at 31.84°, 34.48°, 47.56°, 56.61°, 62.82°, and 67.92° formed the zincite ZnO fingerprint. Adding ZnO while holding the accepted phases and nuisance state fixed reduced full-grid Rwp from 5.58% to 4.72% and its scale remained clearly positive. Subsequent ordinary three-phase refinement reached 3.04%. The residual ZnO/WO3 mole ratio is 0.993, independently consistent with equimolar unreacted precursors from incomplete ZnO + WO3 -> ZnWO4 conversion.

## Remaining uncertainty

Phase identities are reliable, and all three submitted CIFs pass the physical screen. Exact fractions are less certain than their printed digits because scale, preferred orientation, crystallite broadening, background, and surface roughness are correlated; ZnO is nanocrystalline and its fraction is the least precise. The fractions should be regarded as approximate crystalline-phase abundances rather than formal absolute assays.

The ZnWO4 metal framework and cell are robust. Detailed oxygen displacements in the minor WO3 phase cannot be determined reliably from this powder pattern: unconstrained further oxygen refinement produced implausibly short W-O distances, so the submitted WO3 coordinates are the last physically screened state (minimum W-O 1.692 Å and minimum O-O 2.016 Å). The weak ZnO oxygen coordinate was retained from the zincite reference. Surface-roughness parameters reached their allowed limits and should be viewed only as nuisance corrections, not as independently measured specimen properties.
