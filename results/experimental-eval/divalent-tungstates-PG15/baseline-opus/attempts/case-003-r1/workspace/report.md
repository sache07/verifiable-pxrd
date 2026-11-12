# Phase analysis of the CaCO3 + WO3 product heated at 500 °C

**Data**: `inputs/pattern.csv`, 8293 points, 9.99–100.09° 2θ, Cu Kα1+Kα2 (λ1 = 1.540598 Å,
λ2 = 1.544426 Å, I2/I1 = 0.5), Bragg–Brentano reflection geometry, raw counts
(no smoothing / background subtraction).
**Tool**: GSAS-II 5.x scriptable API (Rietveld); candidate structures taken from the local
COD-filtered-2024 structure database.

## Result

| Phase | Formula (mineral) | Space group | Weight fraction | esd (stat.) | Estimated total uncertainty | CIF |
|---|---|---|---|---|---|---|
| 1 | WO3 (γ-WO3, monoclinic) | P2₁/c (#14) | **0.568** | 0.002 | ±0.015 | `WO3.cif` |
| 2 | CaCO3 (calcite) | R-3c (#167) | **0.314** | 0.002 | ±0.012 | `CaCO3.cif` |
| 3 | CaWO4 (scheelite) | I4₁/a (#88) | **0.118** | 0.001 | ±0.015 | `CaWO4.cif` |

Fractions are normalised over the three modelled crystalline phases (sum = 1.000).

**Fit statistics** (full pattern, all points, background included in the denominator, as GSAS-II
reports them): Rwp = 7.22 %, Rp = 5.30 %, Rexp = 2.39 %, χ² = 9.17, GOF = 3.03,
8293 observations, 66 refined variables. With the background removed from the denominator
Rwp = 10.9 %. Observed/calculated/difference profile: `fit.csv`
(columns `two_theta_deg, y_obs, y_calc, y_obs_minus_calc, background`).
GSAS-II project: `final.gpx`.

Refined lattice parameters:

* γ-WO3 (deposited in the P2₁/c setting of COD 2311041): a = 7.6907(22), b = 7.53579(16),
  c = 10.5404(39) Å, β = 136.144(4)°, V = 423.249(21) Å³. In the conventional P2₁/n setting this
  is a = 7.300, b = 7.536, c = 7.691 Å, β = 90.68° — the standard room-temperature γ-WO3 cell
  (literature 7.306, 7.540, 7.692 Å, 90.88°).
* calcite: a = 4.9870(4), c = 17.0615(8) Å, V = 367.474(31) Å³ (literature 4.989, 17.061 Å).
* scheelite: a = 5.2421(7), c = 11.3786(14) Å, V = 312.68(8) Å³ (literature 5.243, 11.374 Å).

(esds are the statistical values from the covariance matrix; see the systematic ~0.05–0.1 %
scale uncertainty discussed below.)

## Evidence

**Phase identification.** The chemistry (Ca–C–O–W) limits the plausible phase space; all
Ca–O–W, O–W, C–Ca–O, Ca–H–O and Ca–O entries of the COD-filtered database were screened.
Three phases account for every resolved reflection in the pattern:

* The three strongest lines of the pattern (23.42, 23.90, 24.67° 2θ) are the
  (002)/(020)/(200) triplet of monoclinic γ-WO3 — unreacted precursor. Every γ-WO3 reflection
  with calculated intensity above ~2 % of the maximum is present up to 100° 2θ, including the
  superstructure lines (26.9, 28.8, 33.5, 41.9, 50.2, 55.0°) that distinguish γ-WO3 from the
  pseudo-cubic subcell descriptions.
* 29.71° (strongest calcite line, 104), 36.27 (110), 39.70 (113), 43.45 (202), 47.77 (018),
  48.78 (116), 57.6 (122)° — unreacted CaCO3 (calcite); its 012 line at 23.42° is overlapped by
  WO3 and carries no independent weight.
* 18.95 (101), 29.06 (112), 31.72 (004), 34.48 (200), 47.5 (204), 54.5 (116)° — CaWO4
  (scheelite), the reaction product of CaCO3 + WO3 → CaWO4 + CO2.

All observed peak positions are shifted +0.29° at low angle relative to the reference
structures; a single refined Bragg–Brentano **sample displacement of −0.50 mm**
(cos θ dependence, common to all three phases) reproduces this shift for every phase
simultaneously, which is itself strong evidence that the three-phase assignment is correct.
Adding a constant zero-point term on top of it gives no improvement (refines to −0.001°).

**Polymorph tests.** Three WO3 models were refined to convergence under an identical protocol:
the monoclinic γ-WO3 structure (COD 2311041, P2₁/c setting, V = 423 Å³) gives Rwp = 7.2 %; the
triclinic δ-WO3 model (COD 2106293, P-1, same cell metric) 8.2 %; the older γ-WO3 coordinate set
(COD 1528915, P2₁/n) 8.5 %. The remaining database entries for WO3 are subcell or
high-temperature descriptions (P4/ncc 1521532, V = 220 Å³; P2₁/c 1563541, V = 206 Å³;
P6/mmm 1004057, V = 180 Å³) with about half the observed cell volume, so they cannot generate
the observed superstructure reflections and were not pursued. The monoclinic γ polymorph is also
the expected room-temperature form, so it is adopted. Among CaCO3 polymorphs only calcite is
present (see below).

**Tests for additional phases.** Each of CaO, Ca(OH)2 (portlandite), aragonite, vaterite,
Ca3WO6 and H2WO4 was added to the converged three-phase model as a fourth phase with free
scale, cell and broadening. All refined to ≤ 0.3 wt % with ΔRwp ≤ 0.01, i.e. none is
detectable. Residual analysis of the difference curve (smoothed, > 4σ) shows no unindexed
maximum: every significant residual lies within 0.25° of a modelled reflection and has the
derivative-like shape of a small position/shape mismatch. The detection limit for an
additional crystalline phase here is ≈ 1 wt %. Conversely the model is not "over-populated":
for each of the three phases, every reflection with calculated intensity above 2 % of that
phase's strongest line has observed intensity above the background by more than 3σ.

**Instrumental/sample corrections used.** Unpolarised radiation (Polariz. = 0.5, i.e. no
monochromator) fits distinctly better than 0.7 (ΔRwp ≈ 0.4). Re-converging the final model with
the Kα2 component switched off is worse (Rwp 7.34 vs 7.22) but not dramatically so — the Kα2
satellites are not individually resolved at this resolution; the metadata ratio I2/I1 = 0.5 was
kept, and the choice changes the weight fractions by ≤ 0.5 wt %.
A Suortti surface-roughness term (B = 0.0778(13), A at its physical limit 0) improves the fit by
ΔRwp ≈ 0.4. Calcite shows a significant March–Dollase preferred orientation along [001]
(r = 0.9286(64), i.e. ~7 % texture on the rhombohedral cleavage); WO3 and CaWO4 show no
meaningful texture (r = 1.0088(13) and 0.987(8)). Background: 14-term Chebyshev polynomial
(refined).

**Microstructure** (apparent values; no instrumental line-shape standard was available, so the
sample broadening is an upper limit and the sizes are lower limits):
WO3 154(6) nm with 0.53(2) % microstrain, calcite no resolvable size broadening with 0.47(1) %
microstrain, CaWO4 31.8(11) nm with 0.36(6) % microstrain. This is consistent with the measured peak
widths (FWHM ≈ 0.17° for WO3, 0.11° for calcite, 0.33–0.36° for CaWO4 at 19–30° 2θ): the
product phase is markedly the most broadened, as expected for a phase newly nucleated at
500 °C on the precursor grains, while the two precursors remain well crystallised.

**Structural refinement.** For WO3 all eight independent atoms (2 W, 6 O) were refined; for
scheelite the single free oxygen position. The resulting geometry is chemically sound and was
checked independently: WO3 gives two distorted WO6 octahedra with W–O = 1.68–2.09 Å and
1.71–2.26 Å (literature γ-WO3 1.72–2.18 Å); scheelite gives W–O = 1.75 Å ×4 and
Ca–O = 2.43/2.53 Å (literature 1.78, 2.44/2.48 Å); calcite (atom positions held at the
reference values) gives C–O = 1.273 Å, Ca–O = 2.363 Å. Releasing the single free calcite oxygen
coordinate was tested and rejected: it lowers Rwp by only 0.014 and shortens C–O to 1.26 Å, i.e.
the light-atom position cannot be improved from these data while two heavy-atom phases dominate
the scattering (the weight fractions move by ≤ 0.3 wt % either way).

## What is uncertain or cannot be determined

* **Amorphous / non-diffracting content.** No internal standard was added and no absolute
  intensity scale is available, so the reported fractions are relative to the crystalline
  phases that are modelled. An amorphous component would be absorbed into the background and
  cannot be quantified from these data.
* **Microabsorption.** With Cu Kα, μ(WO3) ≈ 1100 cm⁻¹ and μ(CaWO4) ≈ 900 cm⁻¹ against
  μ(CaCO3) ≈ 190 cm⁻¹. No Brindley correction was applied (particle size unknown). For
  micrometre-sized particles this typically biases the strongly absorbing phases low and
  calcite high by a few relative percent; the direction is consistent with the Ca/W ratio
  found below.
* **Weight-fraction uncertainty.** The statistical esds (±0.1–0.2 wt %) are optimistic. Across
  eight independently converged model variants (ADPs refined vs fixed, isotropic vs mixed
  Lorentzian–Gaussian broadening, with/without texture, polarisation 0.5 vs 0.7) the fractions
  spanned WO3 54.6–57.1, CaCO3 30.0–31.4, CaWO4 11.8–14.4 wt %. A realistic uncertainty is
  therefore ±1.5 wt % absolute per phase (larger if microabsorption is significant). The
  CaWO4 fraction is the most model-sensitive because its peaks are broad and heavily
  overlapped.
* **Derived chemistry.** The refined fractions correspond to 0.041 mol CaWO4,
  0.245 mol WO3 and 0.314 mol CaCO3 per 100 g, i.e. a bulk molar Ca/W = 1.24 and conversion
  of only ~14 % of the tungsten (~12 % of the calcium) to CaWO4 — the 500 °C treatment left the
  reaction far from complete. A Ca/W ratio above 1 means either the precursor mixture was
  Ca-rich or calcite is somewhat overestimated (microabsorption, texture). This cannot be
  resolved from the diffraction data alone.
* **Structural detail.** Atomic displacement parameters could not be refined reliably (they
  correlate with the phase scales and with the background: refined values reached
  0.02–0.03 Å² for CaWO4 and were pinned at the lower bound for the WO3 oxygens), so they were
  fixed at reference values for the deposited CIFs; the effect on the weight fractions is
  ≤ 0.5 wt %. The WO3 oxygen positions are determined only to about ±0.04 Å (esd 0.005–0.007
  in fractional coordinates) because W dominates the scattering; the fine distinction between
  the monoclinic γ and triclinic δ WO3 descriptions therefore rests on the fit quality
  (Rwp 7.2 vs 8.2 %) rather than on resolved peak splitting. Lattice parameters carry a
  systematic uncertainty of ~0.05–0.1 % because the +0.29° displacement correction and the
  cell parameters are partly correlated (refining a zero shift instead of a displacement moves
  the cell edges by ~0.07 %).
* **Residual misfit.** GOF = 3.0 is dominated by the very high counting statistics
  (up to 27 000 counts at the strongest peak). The largest residuals (9–20 % of the peak
  height) sit at the very top of the four most intense reflections, where the calculated
  profile is 0.02–0.04° off and slightly too flat: the pseudo-Voigt profile with a fixed
  instrumental Gaussian cannot reproduce the sharp core plus extended tails of this
  uncalibrated laboratory profile (the metadata confirm no calibrated instrument profile was
  provided). This is a profile-shape limitation, not evidence of a missing phase.

## Files

| File | Content |
|---|---|
| `WO3.cif`, `CaCO3.cif`, `CaWO4.cif` | refined structures (one per phase) |
| `fit.csv` | 2θ, observed, calculated, difference, background |
| `result.json` | phases, CIF paths, weight fractions (+esd), fit statistics, limitations |
| `final.gpx` | GSAS-II project that produced the above |
| `work/` | scripts, intermediate projects and refinement logs of all model variants |
