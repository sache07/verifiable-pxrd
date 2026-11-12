# PXRD phase analysis

The selected two-phase model is **98.14 wt% MnWO4 (wolframite, P2/c)** and **1.86 wt% triclinic WO3 (P-1)**, normalized over the modeled crystalline phases. The formal GSAS-II scale-factor uncertainty is 0.07 wt% (1σ) for each complementary fraction. The final full-pattern fit has Rwp = 6.885%, Rp = 4.838%, and GOF = 2.500 (8301 points, 29 refined variables).

## Evidence

MnWO4 is chemically consistent with the MnO + WO3 precursor inventory and accounts for the full characteristic series, including peaks at 15.679, 18.654, 23.859, and 24.329° 2θ, the resolved 30.085/30.563° pair, and numerous high-angle reflections. Its refined cell is a = 4.83044, b = 5.75629, c = 4.99562 Å and β = 91.2174°. The starting wolframite topology (COD 1520200) passed the composition, occupancy, symmetry, duplicate-site, and contact audit; its lattice and atomic coordinates were refined, and the resulting Mn–O/W–O geometry remained plausible.

The residual peak family is best explained by triclinic WO3 (starting model COD 2106293), whose strongest calculated groups occur at 23.453/23.940/24.637, 33.27–34.76, 47.61–50.15, and 55.58–56.56° 2θ. Removing this phase from the final model raises Rwp from 6.885% to 7.139% after complete reconvergence. An orthorhombic WO3 replacement was distinctly poorer, while MnO, Mn2O3, Mn3O4, and Mn3WO6 gave nonpositive or overlap-only scales and negligible full-pattern benefit. Both submitted CIFs pass `cif_audit.py` without flags.

The final model uses the smallest supported nuisance description: ten background coefficients, one specimen-shift correction, positive global Gaussian/Lorentzian width terms, and mild [110] March–Dollase texture for MnWO4. A joint zero/shift branch was rejected at 99.99% correlation. Matched removals of either retained width term materially worsened the fit. The final project converged with no SVD-dropped variables; regenerated and saved profiles agree exactly, and all reflection widths are positive.

## Remaining uncertainty

The reported 1.86 wt% WO3 value is conditional on the selected minimal profile/texture model and is not reliable to the small formal least-squares uncertainty. Plausible but non-unique minor-phase texture or broadening branches moved WO3 to approximately 1.4–3.2 wt%; this is the more realistic systematic range (and gives 96.8–98.6 wt% MnWO4). Because the WO3 scale is small, its lattice and atomic parameters could not be refined stably and were fixed to the audited source model. Thus the presence of residual WO3 is supported, but its exact polymorph-level structure and fraction are only moderately certain. Trace phases below roughly 0.5 wt% are not excluded. No amorphous fraction can be obtained without an internal standard, so all fractions refer only to modeled crystalline material. GOF also depends on GSAS-II counting-statistics weights because pointwise uncertainties were not supplied.
