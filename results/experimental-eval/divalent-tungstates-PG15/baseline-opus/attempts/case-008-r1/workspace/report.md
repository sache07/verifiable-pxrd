# Phase analysis of the MnO + WO₃ (900 °C) product

Powder pattern: `inputs/pattern.csv`, Cu Kα₁/Kα₂ (1.540598 / 1.544426 Å, I₂/I₁ = 0.5),
Bragg–Brentano reflection, 9.90–100.09° 2θ, 0.01087° step, 8301 points, raw counts.
Analysis: Rietveld refinement with GSAS-II 5.7.8 (scriptable interface); project `final.gpx`.

## Result

| phase | description | space group | weight fraction | CIF |
|---|---|---|---|---|
| MnWO₄ | wolframite-type (hübnerite) | *P*2/*c* (13) | **0.978** (±0.005) | `MnWO4.cif` |
| γ-WO₃ | monoclinic WO₃, unreacted precursor | *P*2₁/*n* (14) | **0.022** (±0.005) | `WO3.cif` |

Two crystalline phases, normalised over the modelled crystalline content. The quoted ±0.005 is a
realistic uncertainty (see below); the purely statistical esd from the refinement is ±0.0004.
Fit: **R_wp = 3.98 %**, R_p = 3.02 %, GOF = 1.44, χ²_red = 2.09 (8301 observations, 44 parameters);
background-subtracted R_wp = 8.4 %. Per-phase Bragg residuals: R_F = 1.14 % / R_F² = 1.98 % (MnWO₄,
146 reflections) and R_F = 4.1 % / R_F² = 12.5 % (WO₃, 439 reflections).
Observed/calculated/difference profile: `fit.csv` (plotted in `fit.png`).

Refined cells (statistical esds in parentheses):

* MnWO₄ — a = 4.83209(4), b = 5.75822(4), c = 4.99749(4) Å, β = 91.2184(5)°, V = 139.020(2) Å³, ρ = 7.233 g cm⁻³
* γ-WO₃ — a = 7.3047(8), b = 7.5424(12), c = 7.6872(9) Å, β = 90.892° (fixed), V = 423.48(7) Å³

Both agree with the literature values for hübnerite (4.824, 5.750, 4.990 Å, 91.18°) and γ-WO₃
(7.301, 7.539, 7.690 Å, 90.89°) to within ≤ 0.2 %.

## Evidence

**MnWO₄ (major phase).** Every strong line of the pattern is indexed by the wolframite cell: the
(010)/(100) pair at 15.71/18.68°, the (011)/(110) doublet at 23.89/24.36°, the characteristic
(1̄11)/(111) doublet at 30.12/30.58°, (020) at 31.36° and (002)+(021) at 36.27°. The *relative*
intensities of a trial hübnerite model matched the observations before any refinement, and the
refined atomic coordinates moved only slightly from (and stayed close to) the published structure:

| site | refined x, y, z | literature hübnerite model (starting values) |
|---|---|---|
| Mn 2f | ½, 0.6866(3), ¼ | ½, 0.6853, ¼ |
| W 2e | 0, 0.18038(9), ¼ | 0, 0.1807, ¼ |
| O1 4g | 0.2113(7), 0.1026(6), 0.9423(7) | 0.2103, 0.1024, 0.9401 |
| O2 4g | 0.2538(6), 0.3726(6), 0.3961(7) | 0.2588, 0.3754, 0.3927 |

The resulting polyhedra are chemically sensible (Mn–O 2.10–2.29 Å, W–O 1.80–2.14 Å), U_iso values are
small and positive (0.003–0.006 Å²), and R_F² = 2.0 %. This is the expected product of
MnO + WO₃ → MnWO₄ at 900 °C.

**γ-WO₃ (minor phase).** Four weak lines cannot be indexed by MnWO₄: 23.46°, 24.68° and the
triplet 33.55°/33.86°/34.47°. They coincide (same specimen-displacement correction as the main
phase) with the (002)/(200) and (022)/(20̄2)/(202)+(220) reflections of room-temperature monoclinic
WO₃; the remaining WO₃ lines, (020) at ~23.85° and (120) at ~26.9°, fall under the MnWO₄ (011) peak
and at the noise level, respectively, as expected for a ~2 wt% component. Including the phase lowers
R_wp from 4.60 % to 3.98 % (χ² 23107 → 17235 for four extra parameters), and its refined scale is
45σ from zero. The lower panels of `fit.png` show the two regions with and without the WO₃
contribution.

**Phases that are *not* present.** In clean regions of the pattern there is no residual intensity at
the strongest lines of the candidate manganese oxides: MnO (111) at 35.2° leaves ≤ 20 counts
(2σ of the smoothed noise, 0.1 % of the strongest reflection), Mn₃O₄ (224) at 36.8° ≤ 28 counts and
Mn₂O₃ (222) at 33.25° ≤ 38 counts. (Larger residuals near 36.4° and 40.9° lie on the flanks of strong
MnWO₄ peaks and belong to the peak-shape misfit described below, not to a new phase — the companion
line of each candidate, of comparable calculated intensity, is absent.) Added as third phases and
refined on scale alone, MnO gives 0.07(5) wt% and Mn₃O₄ refines to zero: unreacted MnO is below
≈ 0.2 wt% (3σ). The precursor mixture therefore reacted essentially completely, with a small excess
of WO₃ surviving (consistent with a slightly W-rich charge or incomplete diffusion).

## Model choices and their justification

* **Specimen displacement.** All observed peaks are offset by ≈ +0.3·cos θ degrees: the (010) and
  (020) reflections of the same phase are mutually inconsistent (b = 5.638 vs 5.700 Å) unless a
  cos θ-dependent shift is applied, and with it both give b ≈ 5.758 Å. The refined "Shift" is
  −615 µm (≈ 0.6 mm specimen displacement, or an equivalent zero-point/height error); refining the
  constant Zero term in addition gave no improvement, so it was held at 0. Because the correction is
  large, the *absolute* accuracy of the cell constants is limited by it (see below), even though the
  statistical esds are ~1 × 10⁻⁴ Å.
* **Peak shape.** No calibrated instrument profile was supplied. Gaussian U, V, W and the
  Finger–Cox–Jephcoat axial-divergence asymmetry SH/L = 0.072 were refined (the asymmetry is
  essential: the observed peaks carry a low-angle tail out to ≈ −0.4°, and seeding SH/L at a realistic
  0.07 instead of 0.002 dropped R_wp from 6.0 % to 4.1 %). The instrumental Lorentzian terms X and Y
  were held and the Lorentzian width was carried by an isotropic crystallite size (0.209 µm),
  constrained to be equal for both phases because the 2 wt% WO₃ cannot support its own broadening
  parameters; microstrain was held at ~0 (it refines negative otherwise).
* **Surface roughness.** The observed intensities fall off less steeply with angle than a
  smooth-flat-plate model predicts; without a correction all U_iso values refine negative. The
  Suortti roughness correction (A = 0.028, B = 0.113) absorbs this low-angle deficit — physically
  reasonable for a strongly absorbing tungstate in reflection (it could equally be beam overflow at
  low angle) — and restores positive, sensible U_iso.
* **Texture.** A March–Dollase factor along [010] refines to 0.984, i.e. a 1.6 % effect; it was kept
  because it improved the fit slightly, but the sample is essentially untextured.
* **WO₃ structure held.** Only the WO₃ cell (a, b, c; β fixed) and scale were refined. Its atomic
  coordinates are those of the literature γ-WO₃ structure; at 2 wt% and with every WO₃ reflection
  overlapped by MnWO₄ they are not determinable from these data. Releasing the WO₃ cell angle made
  the refinement unstable (invalid metric tensor), hence the constraint.

## Uncertainty and what cannot be determined

* **Weight fractions.** The statistical esd is ±0.04 wt%, which is unrealistically small. Across the
  plausible model variants explored (with/without roughness, with/without texture, Lorentzian width
  carried by size vs. microstrain, polarisation 0.5 vs. refined 0.49) the WO₃ fraction moved only
  between 2.0 and 2.3 wt%. Adding microabsorption (MnWO₄ and WO₃ have similar but not identical
  linear absorption coefficients for Cu Kα, and no particle-size information is available) and the
  fixed WO₃ structure, a realistic uncertainty is **WO₃ = 2.2 ± 0.5 wt%, MnWO₄ = 97.8 ∓ 0.5 wt%**.
* **Amorphous/unobserved content.** No internal standard was measured, so the fractions are
  normalised over the modelled crystalline phases only; an amorphous fraction (or a phase with no
  distinct reflections) cannot be excluded or quantified.
* **Absolute cell accuracy.** The large specimen-displacement correction is strongly correlated with
  the cell scale. The statistical esds (≈ 4 × 10⁻⁵ Å) understate the true accuracy, which is limited
  to roughly ±0.001–0.002 Å (≈ 0.03 %) by that correlation; this is why the refined cell sits ~0.15 %
  above the literature hübnerite values rather than exactly on them.
* **MnWO₄ oxygen positions** are well determined for X-ray data dominated by W (esd ≈ 0.004 Å), but
  U_iso values are correlated with the empirical roughness correction and should be treated as
  effective, not thermodynamic, values. Mn/W site occupancies were fixed at full and were not tested;
  the data cannot resolve a few percent of Mn/W anti-site mixing or a small oxygen non-stoichiometry.
* **The γ-WO₃ polymorph assignment** rests on peak positions only (the monoclinic P2₁/n room-temperature
  form). The data do not distinguish it from the closely related triclinic (δ) or orthorhombic (β)
  WO₃ distortions, whose strongest lines lie within a few hundredths of a degree; nor can a slightly
  sub-stoichiometric WO₃₋ₓ be excluded. The *amount* of WO₃-type material is robust, but its detailed
  structure is not refined here.
* The residual structure left in the difference curve is confined to the flanks of the strongest
  MnWO₄ peaks (≤ 8σ smoothed, ~2 % of peak height), i.e. a remaining imperfection of the empirical
  peak-shape model, not evidence for a further phase.

## Files

| file | content |
|---|---|
| `MnWO4.cif`, `WO3.cif` | refined structures (one per phase), with cell, coordinates, U_iso, esds and fit statistics |
| `fit.csv` | `two_theta_deg, y_obs, y_calc, y_diff, y_background` over the full measured range |
| `result.json` | phases, CIF paths, weight fractions, cells, atoms, fit statistics, model tests |
| `final.gpx` | GSAS-II project that produced the CIFs, fractions and `fit.csv` |
| `fit.png` | fit overview plus zooms on the WO₃-only reflections |
| `scripts/` | all analysis scripts (`refine_final.py` reproduces `final.gpx` from `work/`) |
