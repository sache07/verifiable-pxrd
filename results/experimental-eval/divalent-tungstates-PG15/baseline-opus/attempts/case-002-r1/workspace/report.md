# Phase analysis of `inputs/pattern.csv` (BaO₂ + WO₃, 200 °C)

## Result

Two crystalline phases, both of them the unreacted precursors. No ternary Ba–W–O
product is detectable.

| Phase | Structure type | Space group | Weight fraction (normalised over crystalline phases) |
|---|---|---|---|
| **BaO₂** (barium peroxide) | CaC₂-type peroxide, I4/mmm | `I 4/m m m` | **0.330 ± 0.03** |
| **γ-WO₃** (monoclinic tungsten trioxide) | distorted ReO₃, P2₁/n | `P 21/n` | **0.670 ± 0.03** |

Rietveld fit (GSAS-II v5.7.8, 9.96–100.00° 2θ, 8287 points, 2 phases, 37 varied
parameters): **R_wp = 8.29 %**, R_p = 6.06 %, R_wp(expected) = 3.64 %,
**GOF = χ = 2.28** (χ² = 5.18), R_Bragg(all) = 7.54 %;
R_F = 1.92 % (BaO₂, 24 reflections) and 2.46 % (WO₃, 439 reflections).

Files: `final.gpx` (the project that produced everything below), `BaO2.cif`,
`WO3.cif`, `fit.csv` (2θ, y_obs, y_calc, y_diff, y_background), `fit.png`,
`result.json`.

## Evidence for the phase identification

**Search space.** The precursors fix the chemistry to Ba–W–O (+ possible
H/C/N contaminants). Every COD-filtered entry whose elements are a subset of
{Ba, W, O, H, C, N} was simulated and compared with the observed peak list.
Only two candidates reproduced the observed reflections: monoclinic WO₃ and
tetragonal BaO₂.

**Assignment.** All observed reflections are indexed by the two phases:

* γ-WO₃ accounts for the dominant triplet at 23.43 / 23.92 / 24.65° (the
  (002)/(020)/(200) pseudo-cubic triplet), 26.9, 28.9/29.2, 33.9, 34.4, 41.6–42.3,
  47.5, 50.2, 55.9° and the dense high-angle envelope.
* BaO₂ accounts for 26.31 (002), 27.05 (101), 33.55 (110), 42.96 (112),
  46.64 (103), 47.98 (200) and 55.6–56.0° (202/211).
* No peak in the clean 10–32° window is left unexplained. A Le Bail fit with
  free reflection intensities and the same two cells reached R_wp = 6.8 % with a
  flat residual at high angle, which shows the remaining Rietveld misfit comes
  from the intensity/profile model and **not** from a missing phase.

**Phases explicitly tested and rejected** (each added as a third phase to a
converged two-phase model, R_wp = 7.95 % variant, then its scale, size and cell
refined):

* BaWO₄ (scheelite): refines to 0.3 wt %, ΔR_wp = −0.07 %. Its 100 % reflection
  (112, 26.4°) hides under BaO₂ (002), but the (200) at ~32.1° and (101) at
  ~17.5° reflections that should accompany it are absent from the data.
* BaCO₃ (witherite, the usual BaO₂ air-exposure product): 0.4 wt %,
  ΔR_wp = −0.05 %. Its strongest reflection would hide under the WO₃ peak at
  23.9°, but the accompanying 24.3° and 44.9° reflections are absent.

Both are at or below the detection limit of this pattern (≈1–1.5 wt % for a
well-crystallised Ba/W phase), so they are reported as not detected rather than
as quantified minor phases.

This is chemically consistent with the reported 200 °C treatment: BaO₂ + WO₃ →
BaWO₄ requires much higher temperatures, so an essentially unreacted mixture is
expected.

## Structural models and refinement

Starting models were taken from the COD-filtered database shipped with the
environment: BaO₂ from COD 1010113 (I4/mmm) and γ-WO₃ from COD 1528915 (P2₁/n).

Refined, in this order: phase scales → 14-term Chebyshev background →
isotropic domain size → specimen-displacement (2θ aberration) → lattice
parameters → isotropic microstrain → March–Dollase preferred orientation
(along [001]) → free positional parameters of the heavy scatterers
(W1, W2 in WO₃; the O z coordinate in BaO₂).

Fixed by choice: U_iso (Ba 0.010, W 0.005, O 0.012 Å²), oxygen positions in WO₃,
site occupancies (1.0), instrumental U, V, W (2.0, −2.0, 1.0 centideg²) and the
Kα₂/Kα₁ ratio (0.5) and polarisation (0.7) from the metadata.

Refined values versus the literature — a useful independent check, since the
literature values were never used as restraints:

| | refined | literature |
|---|---|---|
| BaO₂ a, c (Å) | 3.8137, 6.8462 | 3.808, 6.840 |
| BaO₂ O z | 0.3893(11) → O–O = 1.516 Å | 0.389 → O–O ≈ 1.49 Å |
| γ-WO₃ a, b, c (Å), β (°) | 7.3146, 7.5325, 7.6887, 90.712 | 7.306, 7.540, 7.692, 90.88 |
| γ-WO₃ W1, W2 (x, y, z) | (0.246, 0.028, 0.286), (0.254, 0.029, 0.780) | (0.252, 0.026, 0.285), (0.247, 0.033, 0.781) |

All refined values land within ~0.2 % (cells) and ~0.008 fractional units
(W positions) of the published structures, and the refined peroxide O–O bond
length is physically correct. This is the strongest evidence that both phase
assignments and the fitted scales are meaningful.

## Uncertainty and what is *not* reliable

**Large 2θ aberration.** The pattern is systematically displaced by about
+0.28° at low angle relative to both phases' literature cells. Modelled as a
Bragg–Brentano specimen displacement it refines to −495 µm; modelled instead as
a constant zero offset it refines to +0.302°. Both are physically large for a
well-aligned diffractometer (the metadata states no calibrated instrument
profile was supplied). The two models give the same R_wp to within 0.3 % and the
same weight fractions to within 0.02 absolute, and in both cases the refined
cells agree with literature, so the quantification is insensitive to this
choice — but the *absolute* 2θ scale of the dataset should be treated as
uncorrected.

**Weight-fraction uncertainty.** The covariance-matrix esd is only ±0.0015, which
is far too optimistic. Across the refinement variants I tried (displacement vs
zero-offset, with/without preferred orientation, isotropic vs free displacement
parameters, with/without free W coordinates) the BaO₂ fraction ranged
0.313–0.364. I therefore quote **±0.03 absolute**. In addition,
**microabsorption was not corrected**: μ(BaO₂) ≈ 1550 cm⁻¹ versus
μ(WO₃) ≈ 1000 cm⁻¹ at Cu Kα, so if the particle (not crystallite) size is of
order micrometres the BaO₂ fraction is biased *low*; the true value could be
several wt % higher. The derived molar ratio Ba:W = 0.68 should not be read as
evidence of a non-stoichiometric batch for this reason.

**Amorphous / unmodelled content is not quantified.** No internal standard is
available, and the pattern has a strong, smoothly decaying low-angle background
that a Chebyshev polynomial absorbs. The fractions above are normalised over the
two modelled crystalline phases only, as requested.

**Residual profile misfit.** The remaining misfit (χ = 2.3) is concentrated in
the three strongest WO₃ reflections and at 41.5–42.3°; it survives a Le Bail
fit, so it is a peak-shape/position effect. Attempts to absorb it with
anisotropic size/strain broadening, Lorentzian instrumental terms (X, Y),
axial-divergence asymmetry and spherical-harmonic texture all failed to improve
or destabilised the refinement. Most likely causes are anisotropic
microstructural broadening or a small amount of a second WO₃ distortion variant
(δ/ε) coexisting with γ-WO₃ — neither of which I can establish from these data.

**Microstructural parameters are not reliable.** The refined domain sizes
(41 nm BaO₂, 129 nm WO₃) and microstrains (0.6 % and 1.4 %) are 90 %+
correlated with each other and with the uncalibrated instrumental profile; they
are fitting parameters here, not measurements.

**Light-atom detail is not determined.** With W and Ba dominating the
scattering, the oxygen positions in WO₃ could not be refined (they are held at
the 1960 literature values) and no displacement parameter is determined — free
U_iso refinement drove Ba and W to small negative values, so all U_iso were
fixed. The CIFs should be read as "correct phase, refined cell and heavy-atom
positions", not as independent structure determinations.
