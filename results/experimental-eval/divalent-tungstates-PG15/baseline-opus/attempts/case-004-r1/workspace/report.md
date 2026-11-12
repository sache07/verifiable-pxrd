# Phase analysis of the CoO + WO₃ (900 °C) product

**Result: a two-phase mixture of unreacted γ-WO₃ (70.3 wt%) and wolframite-type CoWO₄ (29.7 wt%).**

| Phase | Structure type | Space group | Weight fraction | CIF |
|---|---|---|---|---|
| WO₃ | γ-WO₃ (monoclinic) | *P*2₁/*n* (#14) | 70.3 wt% (e.s.d. 0.14, realistic ±1.5) | `WO3.cif` |
| CoWO₄ | wolframite | *P*2/*c* (#13) | 29.7 wt% (e.s.d. 0.14, realistic ±1.5) | `CoWO4.cif` |

Fractions are normalised to 100 % of the modelled crystalline phases.
Final Rietveld fit (GSAS-II, `final.gpx`): **R_wp = 5.34 %**, R_p = 4.09 %,
R_wp(background-subtracted) = 5.34 %, R_expected = 3.28 %, **GOF = 1.63**
(χ²_red = 2.67), 8301 observations, 37 refined variables.
Per-phase Bragg residuals: WO₃ R_F = 2.15 %, R_F² = 4.12 % (439 reflections);
CoWO₄ R_F = 2.35 %, R_F² = 4.59 % (140 reflections).
Profile: `fit.csv` (2θ, y_obs, y_calc, y_obs−y_calc, background), plotted in `fit.png`.

## Evidence for the phase identification

The pattern contains 60–70 resolvable reflections, all of which are accounted
for by two phases:

* **γ-WO₃** — the diagnostic (002)/(020)/(200) triplet at 23.17/23.67/24.41° 2θ
  with near-equal intensities (observed 96 : 92 : 100) is the fingerprint of
  room-temperature monoclinic WO₃, and the refined cell
  *a* = 7.30604(42), *b* = 7.53635(44), *c* = 7.69312(44) Å, β = 90.8054(37)°
  matches the literature γ-WO₃ cell (7.306, 7.540, 7.692 Å, β ≈ 90.9°).
  It also explains 26.66, 28.98, 33.35, 33.60, 34.21, 41.48/41.96, 47.28, 48.37,
  50.0/50.4/50.7, 53.6/54.2/54.8, 55.98, 61.8/62.3 ° and the high-angle multiplets.
* **CoWO₄ (wolframite)** — accounts for every reflection that WO₃ cannot:
  19.06° (100), 30.71° (1̄11, the strongest CoWO₄ line), 31.51° (020),
  36.45° (002/021), 37.02° (120), 38.60° (200), 52.13° (130), 65.13° (311/132).
  Refined cell *a* = 4.66944(29), *b* = 5.68363(35), *c* = 4.94991(33) Å,
  β = 90.056(9)°, i.e. the known CoWO₄ wolframite cell (4.669, 5.687, 4.951 Å).

This is the expected chemistry: CoO + WO₃ → CoWO₄ at 900 °C, with WO₃ left over
because the charge was WO₃-rich. The refined fractions correspond to
0.3033 mol WO₃ : 0.0968 mol CoWO₄, i.e. a bulk cation ratio Co : W ≈ 1 : 4.1
(24.2 mol % CoWO₄); all of the cobalt in the modelled phases is in CoWO₄.

**Phases explicitly tested and rejected.** Co₃O₄ (strong line at 36.85°) and CoO
(strongest line at 42.4°) were each added as a third phase to the converged
model; both refined to a scale factor of exactly zero with no change in R_wp
(5.343 → 5.345 and 5.343). No unindexed peak remains above the noise in the
difference curve, so neither unreacted CoO nor Co₃O₄ is detectable. With the
high fluorescence background of a Co-bearing sample measured with Cu Kα, the
practical detection limit here is roughly 1 wt%.

## Model and refinement strategy

* **Starting structures.** γ-WO₃ from COD 2311041 (1966 neutron/X-ray
  refinement, *P*2₁/*c*, β = 136.06°), transformed by
  (**a**′,**b**′,**c**′) → (**a**+**c**, **b**, −**a**) to the conventional
  *P*2₁/*n* setting; this model has clean WO₆ octahedra (W–O 1.72–2.16 Å),
  whereas the other monoclinic WO₃ entry in the available structure database
  (COD 1528915) contains a 1.58 Å O···O contact and gives a visibly worse
  intensity distribution around 33–34° 2θ. CoWO₄ from COD 5910316 (wolframite).
* **Refined:** scale, 12-term Chebyshev background, both phase fractions, both
  unit cells, sample displacement (−111 µm), peak shape (Gaussian *W*,
  Lorentzian *X*, axial divergence *SH/L*, isotropic microstrain per phase),
  Suortti surface-roughness parameters, and the metal-atom coordinates
  (W1, W2 in WO₃; the *y* coordinates of Co and W in CoWO₄, which are the only
  free cation parameters in *P*2/*c*).
* **Held fixed:** all oxygen coordinates and all U_iso (W 0.005, Co 0.008,
  O 0.012 Å²), the wavelengths, and the Kα₂/Kα₁ ratio of 0.50 given in the
  metadata (freely refining it gave 0.61 with no change in R_wp or in the phase
  fractions, confirming the doublet is present at about the reported level).

The refined metal positions move only 0.01–0.05 Å from the literature values
and the resulting coordination geometry is chemically correct:
both WO₃ octahedra give W–O = 1.72–2.19 Å (mean 1.93 Å), and CoWO₄ gives
Co–O = 2.07, 2.12, 2.16 Å (mean 2.12 Å, as expected for octahedral Co²⁺) and
W–O = 1.77, 1.89, 2.13 Å (mean 1.93 Å) — both typical wolframite values.

### Why a surface-roughness correction was included

Without an angle-dependent intensity correction the fit stalls at R_wp ≈ 8 %
and the refinement tries to drive every U_iso negative — the classic signature
of a reflection-geometry intensity deficit at low angles. Adding the Suortti
surface-roughness correction (A = 0.146, B = 0.780) with U_iso held at physical
values dropped R_wp from 7.97 % to 5.37 % and removed the negative-U_iso
pathology entirely. Physically this represents surface roughness and/or beam
overflow of a strongly absorbing, loosely packed powder; the correction is
empirical, and the quoted A and B should not be over-interpreted.

## Uncertainty and what cannot be determined reliably

* **Weight fractions.** The purely statistical e.s.d. is ±0.14 wt%, which is far
  too optimistic. Within the final model family the fractions are very stable:
  70.0–70.3 wt% WO₃ across variants with oxygen positions free or fixed, with
  12 or 20 background terms, and with or without a March–Dollase preferred-
  orientation parameter. Earlier models *without* the roughness correction
  spanned 67.7–74.6 wt%. Allowing for residual systematics (background model,
  the empirical intensity correction, and microabsorption, which is not modelled)
  I quote **70.3 ± 1.5 wt% WO₃ / 29.7 ± 1.5 wt% CoWO₄**.
* **Amorphous content is not determined.** No internal standard was added and
  the background is dominated by Co K fluorescence, so the fractions are
  relative to the crystalline phases only. A crystalline–amorphous split cannot
  be extracted from these data.
* **Oxygen positions are not determined.** Against W (Z = 74) the oxygen
  contribution is small, and releasing the oxygen coordinates lowers R_wp from
  5.34 % to 5.18 % while producing impossible bonds (W–O = 1.51 Å in WO₃). The
  oxygen sublattices in both CIFs are therefore the published ones, not
  refined values; the CIFs should be read as "literature structure with refined
  cell and refined metal positions", and the two WO₃ sites in particular should
  not be used to discuss the γ-WO₃ octahedral distortion.
* **Displacement parameters are not determined** for the same reason and because
  they are strongly correlated with the empirical roughness correction; they
  were fixed, so no thermal/static disorder conclusion can be drawn.
* **Absolute lattice parameters** carry an additional systematic from the large
  refined sample displacement (−111 µm), which correlates with the cell scale;
  the quoted e.s.d.s (≈0.0004 Å) understate the true accuracy, which is closer
  to ±0.002 Å. Relative values and the phase assignment are unaffected.
* **Peak-width interpretation.** The refined widths require ~0.39 % microstrain
  for WO₃ and essentially none for CoWO₄, with no instrumental Gaussian term
  (no calibrated instrument profile was supplied, and the instrumental
  contribution could not be separated from the sample contribution). The
  microstrain and crystallite-size values are therefore fitting parameters, not
  microstructural measurements.
* Small systematic residuals remain in the WO₃ 23–24.5° triplet and at 30.7°
  (CoWO₄ 1̄11), at the level of a few percent of peak height; they are
  peak-shape/anisotropy effects that a single isotropic broadening model per
  phase cannot capture, and they are the main reason GOF is 1.63 rather than 1.

## Files

| File | Contents |
|---|---|
| `WO3.cif`, `CoWO4.cif` | refined structures (one per phase) |
| `fit.csv` | 2θ, y_obs, y_calc, difference, background |
| `fit.png` | the same fit, plotted in three 2θ panels |
| `result.json` | phases, CIF paths, normalised weight fractions, fit statistics, model description |
| `final.gpx` (+ `final.lst`) | the GSAS-II project that produced all of the above |
