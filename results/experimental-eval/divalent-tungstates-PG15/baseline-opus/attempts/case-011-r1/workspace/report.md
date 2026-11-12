# Phase analysis of `inputs/pattern.csv` (MnO₂ + WO₃, 300 °C)

## Result

Two crystalline phases, both unreacted precursors. No ternary Mn–W–O compound was formed.

| Phase | Identity | Space group | Weight fraction (normalised over the two modelled phases) | CIF |
|---|---|---|---|---|
| WO₃ | γ-WO₃, monoclinic tungsten(VI) oxide | *P*2₁/*n* (no. 14), *Z* = 8 | **70.3 wt%** (esd 0.2, realistic ±3) | `WO3_gamma_monoclinic.cif` |
| MnO₂ | β-MnO₂, pyrolusite (rutile type) | *P*4₂/*mnm* (no. 136), *Z* = 2 | **29.7 wt%** (esd 0.2, realistic ±3) | `MnO2_pyrolusite.cif` |

Fit statistics (whole pattern, 9.90–100.09° 2θ, 8301 points, 40 refined variables):

| | |
|---|---|
| R<sub>wp</sub> | 6.83 % |
| R<sub>p</sub> | 5.03 % |
| R<sub>exp</sub> (counting-statistics limit) | 2.69 % |
| Goodness of fit *S* = R<sub>wp</sub>/R<sub>exp</sub> | 2.54 (χ²<sub>red</sub> = 6.45) |
| Durbin–Watson | 0.34 |
| R<sub>F</sub> / R<sub>F²</sub>, WO₃ (438 reflections) | 2.72 % / 6.37 % |
| R<sub>F</sub> / R<sub>F²</sub>, MnO₂ (21 reflections) | 4.25 % / 11.07 % |

Refined cells (statistical esds in parentheses; see the systematic caveat below):

* γ-WO₃  a = 7.3174(4) Å, b = 7.5473(4) Å, c = 7.7033(4) Å, β = 90.754(3)°, V = 425.39(6) Å³
* β-MnO₂ a = 4.4054(3) Å, c = 2.8776(2) Å, V = 55.848(11) Å³

Derived molar ratio MnO₂ : WO₃ = **1.13 : 1** — close to an equimolar precursor mixture.

Files: `fit.csv` (2θ, y_obs, y_calc, y_diff, y_background), `fit.png` (same data plotted),
`final.gpx` (GSAS-II project that produced the submitted CIFs, fractions and profile),
`result.json` (machine-readable summary).

## Evidence for the phase assignment

**γ-WO₃.** The three strongest reflections of the pattern (23.44°, 23.93°, 24.69°) are the
002/020/200 triplet that is diagnostic of the room-temperature monoclinic polymorph of WO₃,
followed by the 022/20-2/202/220 group at 33.6–34.5° and the 400/140 pair at 50.2°. All 61
peaks detected above the noise are accounted for by WO₃ + MnO₂ (reflection markers in
`fit.png`). The refined monoclinic cell reproduces the accepted γ-WO₃ cell
(7.306/7.540/7.692 Å, β ≈ 90.9°) to within 0.16 %.

**β-MnO₂ (pyrolusite).** Refining WO₃ alone leaves large, sharp positive residuals at 29.01°,
37.68°, 42.2°, 56.96°, 59.66°, 65.1°, 67.5° and 72.5°. These index exactly as the
110, 101, 111, 211, 220, 002, 310 and 301 reflections of the tetragonal rutile-type MnO₂
(a = 4.405 Å, c = 2.878 Å), and the refined Mn–O distances (1.888 Å ×2, 1.891 Å ×4) are those
of an essentially regular MnO₆ octahedron, as expected for pyrolusite. Adding this phase drops
R<sub>wp</sub> from 10.5 % to 6.8 % and removes every one of those residual peaks.

**Chemical consistency.** The two phases are exactly the two precursors, and their refined
proportion corresponds to a near-equimolar mixture. At the reported 300 °C, MnWO₄ formation is
not expected (it normally requires ≥600 °C), and MnO₂ does not yet decompose to Mn₂O₃
(≈530 °C). The result is therefore "no reaction has taken place".

**Tests for further phases.** Starting from the converged two-phase model, each of the following
was added as a third phase and allowed to refine its scale, cell and size: MnWO₄, Mn₂O₃
(bixbyite), Mn₃O₄ (hausmannite), MnO (manganosite), ramsdellite-MnO₂, tetragonal WO₃ and
triclinic δ-WO₃. All except δ-WO₃ refined to ≤1.2 wt% and did **not** improve R<sub>wp</sub>
(MnWO₄ 0.4 wt%, R<sub>wp</sub> worse; Mn₂O₃ 1.2 wt%, ΔR<sub>wp</sub> ≈ 0; Mn₃O₄ and MnO rejected).
No third phase is therefore claimed; the detection limit under these conditions is roughly
1–2 wt%.

## Remaining uncertainty — what cannot be determined reliably

1. **Absolute lattice parameters carry a ~+0.15 % systematic error.** Both phases refine to
   cells 0.10–0.16 % larger than their accepted values, and a large 2θ zero correction
   (+0.393(4)°) is needed. The metadata state that the instrument profile was not calibrated.
   Because *both* independently refined phases require the *same* correction, this is an
   uncorrected 2θ-scale/zero error rather than a real lattice expansion; the zero point is also
   98.6 % correlated with the axial-divergence asymmetry term. Relative cell metrics
   (monoclinicity, c/a of MnO₂) are reliable; absolute values should be treated as
   ±0.15 % uncertain.

2. **Weight fractions: ±3 wt%, not ±0.2 wt%.** The least-squares esd is 0.2 wt%, but the value
   moves between 70 and 74 wt% WO₃ across physically defensible alternatives for the peak-shape
   and displacement-parameter model (fixed vs refined U<sub>iso</sub>, isotropic vs uniaxial vs
   Stephens microstrain, with/without March–Dollase texture). ±3 wt% is the honest uncertainty.
   Microabsorption is not a significant contributor here: µ(WO₃) ≈ 1010 cm⁻¹ and
   µ(MnO₂) ≈ 936 cm⁻¹ for Cu Kα are nearly equal, so no Brindley correction was applied.

3. **Oxygen positions are not determined.** With W (Z = 74) and Mn (Z = 25) dominating the
   scattering, lab Cu-Kα data of this resolution carry almost no information on the oxygen
   sublattice. Freely refining the oxygen coordinates lowered R<sub>wp</sub> to ≈5.2 % but drove
   W–O distances to 1.2–1.3 Å and several U<sub>iso</sub> values negative, i.e. the apparent
   improvement was absorbed peak-shape misfit, not structure. **In the submitted model the
   oxygen coordinates are therefore held at the published values** (γ-WO₃: COD 1528915,
   Tanisaki 1960; pyrolusite: COD 1514232, O at x = 0.303) and U<sub>iso</sub>(O) is fixed at
   0.012 Å². Only the two W positions and U<sub>iso</sub>(W), U<sub>iso</sub>(Mn) were refined.
   The submitted CIFs are consequently *lattice-refined literature models*, not independent
   structure determinations. Their W–O distances (1.82–2.18 Å) and Mn–O distances (1.89 Å) are
   chemically sound.

4. **U<sub>iso</sub>(Mn) = 0.025 Å² sits at its imposed upper bound** and is too large for
   crystalline MnO₂ (≈0.005 Å²). It is compensating for something the model does not capture —
   most likely de Wolff/stacking disorder in the MnO₂ (commercial "MnO₂" is frequently partly
   γ-type) or anisotropic MnO₂ broadening. The MnO₂ weight fraction is the quantity most
   sensitive to this, which is part of why ±3 wt% is quoted.

5. **A minor triclinic δ-WO₃ component cannot be excluded.** Adding triclinic WO₃ (COD 2106293)
   as a third phase lowered R<sub>wp</sub> from 5.67 % to 5.22 % in a comparison refinement and
   took 4.1 wt%, refining to a genuinely triclinic cell (α = 88.78°, γ = 91.15°). γ- and δ-WO₃
   have nearly identical cells, however, and a second, slightly distorted WO₃ is exactly what a
   single WO₃ phase with anisotropic strain broadening also mimics; with this profile quality
   the two explanations are not separable. It was therefore **not** included. If present, it
   would be at the few-wt% level and would come out of the γ-WO₃ fraction, leaving the
   WO₃-total/MnO₂ split unchanged.

6. **Residual misfit (S = 2.54) is peak-shape, not phase-related.** The remaining difference
   features are derivative-shaped at the strongest WO₃ reflections and at 41–43°, 72.4° and 77°,
   i.e. symmetric about peak positions rather than at unexplained positions. γ-WO₃ shows strongly
   anisotropic broadening (the h00 reflections are markedly sharper than 0k0 and 00l); a
   Stephens generalised-strain model was used, which reduced R<sub>wp</sub> from 7.44 % to 6.83 %.
   The nine S<sub>hkl</sub> coefficients are phenomenological and should not be read as physical
   strain components.

## Method summary

GSAS-II (scriptable interface). Candidate structures were taken from the local
COD-filtered-2024 CIF collection and screened by simulated-pattern matching before refinement.
Radiation was modelled as Cu Kα₁ + Kα₂ (1.540598 / 1.544426 Å, I₂/I₁ = 0.5) as stated in the
metadata; a Kα₁-only model fitted measurably worse (R<sub>wp</sub> 8.00 % vs 7.68 % at the same
refinement stage). Weights are 1/y<sub>obs</sub> (raw counts, Poisson).

Refined parameters (40): 12-term Chebyshev background; histogram scale; MnO₂ phase fraction;
2θ zero; both unit cells; Gaussian profile term *W* and axial-divergence asymmetry *SH/L*;
isotropic crystallite size for each phase; nine Stephens strain coefficients for WO₃;
W1/W2 coordinates; U<sub>iso</sub>(W1), U<sub>iso</sub>(W2), U<sub>iso</sub>(Mn).

Held fixed, with reasons: instrument *U*, *V*, *X*, *Y* = 0 (freely refining the full Caglioti
set drove the Gaussian variance negative above ≈40° 2θ — unphysical — and the sample broadening
is carried by the per-phase size/strain terms instead); polarisation 0.7; all oxygen coordinates
and U<sub>iso</sub>(O) = 0.012 Å² (item 3 above); MnO₂ microstrain held at 100 × 10⁻⁶ after it
refined to a slightly negative value, i.e. the MnO₂ broadening is size-dominated.

Refined microstructure: WO₃ volume-averaged domain size ≈ 85 nm with pronounced anisotropic
strain; MnO₂ ≈ 102 nm with negligible strain.
