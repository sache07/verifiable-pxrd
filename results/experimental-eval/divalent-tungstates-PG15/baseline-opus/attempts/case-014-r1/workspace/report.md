# Quantitative phase analysis of the SrCO₃ + WO₃ (900 °C) product

**Data:** `inputs/pattern.csv` — 8282 points, 10.009–99.994° 2θ, step 0.01087°, Cu Kα₁+Kα₂
(λ₁ = 1.540598 Å, λ₂ = 1.544426 Å, I₂/I₁ = 0.5), Bragg–Brentano reflection geometry, raw counts.
Point uncertainties were not supplied, so Poisson weights σ = √N were used.

**Software:** GSAS-II 5.7.8 (scriptable interface). Project: `final.gpx`.

---

## 1. Result

| Phase | Structure type | Space group | Weight fraction* | wt % |
|---|---|---|---|---|
| **SrWO₄** | scheelite | *I*4₁/*a* (88) | 0.857 | **85.7 ± 1.5** |
| **WO₃** | γ-WO₃ (monoclinic), unreacted precursor | *P*2₁/*n* (14) | 0.143 | **14.3 ± 1.5** |

\* normalised over the two **modelled** crystalline phases. A third crystalline phase is present
(≈ 11 % of the total Bragg intensity) but could not be identified and is therefore **not** included
(Section 4). The quoted ±1.5 wt % is a realistic uncertainty; the purely statistical e.s.d. is
±0.2 wt %.

**Refined lattice parameters**

* SrWO₄: *a* = 5.41866(16) Å, *c* = 11.96043(30) Å, *V* = 351.18 Å³
  (literature SrWO₄: *a* = 5.4168 Å, *c* = 11.951 Å)
* WO₃: *a* = 7.30079(74) Å, *b* = 7.53826(87) Å, *c* = 7.69420(84) Å, β = 90.723(4)°, *V* = 423.42 Å³
  (literature γ-WO₃: *a* = 7.30 Å, *b* = 7.53 Å, *c* = 7.68 Å, β = 90.9°)

**Fit statistics (whole pattern, 10–100° 2θ)**

| R*wp* | R*p* | R*exp* | S = R*wp*/R*exp* | χ² | R(*F*) SrWO₄ | R(*F*) WO₃ |
|---|---|---|---|---|---|---|
| 9.72 % | 7.04 % | 3.54 % | 2.75 | 7.56 | 3.64 % | 15.2 % |

Observed / calculated / difference profile: `fit.csv`
(columns `two_theta_deg, y_obs, y_calc, y_diff, y_background`; the background column
includes the independent peaks used for the unidentified phase, Section 4).

---

## 2. Evidence for the phase assignment

### 2.1 2θ scale

Before any phase could be assigned the 2θ scale had to be calibrated. Single-peak
(Kα₁/Kα₂ doublet, pseudo-Voigt) fits to twelve isolated reflections gave positions that are
systematically **high** by +0.34° at 18° 2θ falling to +0.23° at 79° 2θ. A least-squares fit of
(a, c, specimen-displacement) to those positions, with the zero offset held at 0, reproduced all
twelve positions with an r.m.s. error of 0.005° and gave a cell (*a* = 5.4194, *c* = 11.9619 Å)
in excellent agreement with literature SrWO₄. The deviation is therefore a **specimen-displacement
error**, Δ2θ = +0.331·cos θ degrees (GSAS-II `Shift` = −578 µm at R = 200 mm), not a lattice effect.
Refining a zero offset in addition changed R*wp* by only 0.015 % and gave Zero = 0.0005°, so it was
kept fixed at zero. Without this calibration the d-spacings are biased by up to 1.5 %, which is
what initially made the phase identification ambiguous.

### 2.2 SrWO₄ (major phase)

Unambiguous. All 24 observable reflections of the scheelite pattern are present with the correct
relative intensities, e.g. (101) 18.30°, (112) 27.96°, (004) 30.21°, (200) 33.37°, (204) 45.44°,
(220) 47.72°, (116) 51.95°, (312) 56.09°, (224) 57.34°, (008) 62.3°, (400) 69.58°, (316) 72.99°,
(420) 79.21°, (424) 86.86°, (512) 95.04°. The refined cell matches published SrWO₄ to within
0.04 % and R(*F*) = 3.6 %. The refined O position (0.2388, 0.1045, 0.0418) gives
W–O = 1.81 Å (literature 1.78 Å) — reasonable for a light atom refined against a W-dominated
lab-XRD pattern. This is the expected product of SrCO₃ + WO₃ at 900 °C.

### 2.3 γ-WO₃ (minor phase, unreacted precursor)

Also unambiguous. The characteristic monoclinic triplet (002)/(020)/(200) is observed at
23.48/23.97/24.74° (apparent) with the correct ~100:80:100 intensity ratio, together with
(120) at 26.98°, the (022)/(202)/(220) group at 33.9–34.5°, (222) at 41.8/42.2°, (004) 47.8°,
(040) 48.6°, (114) 50.2–50.7°, (420) 56.2°, and higher-order reflections up to 96°. Refining the
cell freely from the COD starting model converged on *a* = 7.3008, *b* = 7.5383, *c* = 7.6942 Å,
β = 90.72° — the standard γ-WO₃ cell. Its presence means the reaction mixture was
tungsten-rich and/or incompletely reacted.

R(*F*) for WO₃ is relatively poor (15 %) because its oxygen positions were held at the literature
values (only the two W positions were refined); with only ~14 wt % of a phase whose reflections
are heavily overlapped, refining all 24 oxygen coordinates is not justified and was unstable
(negative U*iso*).

---

## 3. Refinement strategy

Refined, in this order: 14-term Chebyshev background → histogram scale and the two phase
fractions → both unit cells → peak widths (Gaussian *W*, Lorentzian *X*; the measured FWHM is
almost constant at 0.19–0.23° over the whole range, so *U*, *V* and *Y* were held at zero, which
is the only choice that keeps all width contributions positive) → independent peaks for the
unidentified phase → specimen displacement → Suortti surface-roughness correction →
SrWO₄ oxygen coordinates → SrWO₄ U*iso* (Sr 0.0108, W 0.0100, O 0.027 Å²) → WO₃ W coordinates.

The surface-roughness correction (SRA = −0.36, SRB = 0.115) was needed because the calculated
intensities were systematically too high at low angle and too low at high angle; it lowered R*wp*
from 12.3 to 10.5 %. This is physically plausible for a very strongly absorbing (Sr, W) powder in
reflection geometry. Without it the refinement instead drives U*iso* negative, which is why it is
included. It changes the SrWO₄:WO₃ ratio by about 0.8 wt %.

Kα₂/Kα₁ was kept at the instrument-reported 0.5; refining it gave 0.45 and improved R*wp* by only
0.04 %, so the reported value was retained.

---

## 4. The unidentified third phase — what can and cannot be determined

After the two-phase model converged, **a set of reflections remained that belongs to neither
SrWO₄ nor γ-WO₃** and that cannot be explained by peak-shape or 2θ-scale error. The most
conspicuous is a strong, clean, isolated peak at 29.73° (apparent), i.e. d = 3.035 Å — it is the
third-strongest peak of the whole pattern and sits in a region where SrWO₄ has nothing closer than
(004) at 30.21° and WO₃ nothing closer than (112) at 29.0/29.2°.

Corrected d-spacings and relative intensities (from the fitted independent peaks):

| d (Å) | 5.440 | 4.082 | **3.035** | 2.923 | 2.773 | 2.325 | 2.043 | 1.723 | 1.624 | 1.520 | 1.401 | 1.221 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| I (%) | 5 | 15 | **100** | 21 | 28 | 8 | 30 | 11 | 19 | 8 | 28 | 7 |

These peaks account for **≈ 11 % of the total Bragg intensity** in the measured range.

**Identification was attempted and failed.** Specifically:

* Pattern/d-spacing matching against the full local COD-filtered structure database
  (61 481 CIFs; and separately all 4124 entries containing W or Sr), both with the cell as
  published and with an isotropic cell-scaling factor allowed (0.88–1.18, to catch Sr analogues of
  Ca/Ba/Pb compounds) — no chemically sensible candidate explained more than ~60 % of these lines.
  The database contains only three Sr–W–O entries (SrWO₄ ×2, Sr₃W₂O₉); adding Sr₃W₂O₉ as a third
  phase did not fit (its cell diverged and R*wp* did not improve).
* Autoindexing (GSAS-II `DoIndexPeaks`, all 18 Bravais classes) and a purpose-written
  trial-and-error indexer gave no small-cell solution: every solution indexing all the lines
  required *a* ≈ 16–17 Å, i.e. a cell large enough to index almost anything. This is expected
  because the phase's weaker reflections are buried under the SrWO₄/WO₃ peaks, so the extracted
  line list is incomplete.
* Instrumental artefacts were excluded: the positions do not correspond to Cu Kβ or W Lα
  companions of any strong SrWO₄/WO₃ reflection, and the peak widths (0.17–0.36°) are
  Bragg-like.
* Candidate chemistries tested explicitly and rejected on peak positions/intensities: SrCO₃
  (both aragonite- and calcite-type), SrO, SrO₂, Sr(OH)₂, the other WO₃ polymorphs
  (β-Pnma, ε-Pc, hexagonal, tetragonal), reduced tungsten oxides (WO₂, W₃O₈, W₃O₁₀, W₁₈O₄₉),
  W metal, Al₂(WO₄)₃ and Zr(WO₄)₂ (crucible reaction), Al/Pt/Au/Si (sample holder), and
  Sr₃WO₆ constructed from the Ca₃WO₆ and Ba₃WO₆ structure types with the cell scaled and freely
  refined.

On chemical grounds the most likely candidates are the Sr-rich tungstates **Sr₂WO₅** or
**Sr₃WO₆** (neither is in the available database), which would arise from incomplete mixing —
Sr-rich regions reacting past SrWO₄ while free WO₃ survives elsewhere, consistent with the 14 wt %
of unreacted WO₃. However, **this is not established by the data**, and no structural model and
hence no weight fraction can be given for this phase.

**Consequence for the quantification.** The unidentified reflections were modelled as 12
independent pseudo-Voigt peaks sitting on the background, so that they do not bias the SrWO₄/WO₃
scale factors. The sensitivity of the answer to this choice is:

| treatment of the unidentified peaks | R*wp* | SrWO₄ | WO₃ |
|---|---|---|---|
| 12 independent peaks (reported model) | 9.72 % | 85.7 % | 14.3 % |
| 8 independent peaks (only the cleanest) | 11.2 % | 85.7 % | 14.3 % |
| none (pure two-phase fit) | 15.8 % | 87.2 % | 12.8 % |

The SrWO₄:WO₃ ratio is therefore robust to ±1.5 wt %. **But the absolute weight fractions are only
valid for the modelled subset of the sample**: if the unidentified phase is a Sr–W–O compound of
similar mass-absorption and scattering power, it would represent roughly 10 wt % of the
crystalline material, and the true fractions would be closer to SrWO₄ ≈ 77 %, WO₃ ≈ 13 %,
unknown ≈ 10 %. That figure is an order-of-magnitude estimate only.

---

## 5. Other limitations

* The background is high and strongly curved below 20° 2θ (≈ 2000 counts at 10°, falling to
  ≈ 350 counts at 100°). A 14-term Chebyshev polynomial describes it well, but an amorphous
  component cannot be excluded or quantified; all weight fractions are over the crystalline
  phases only.
* No calibrated instrument profile or standard was supplied, so the peak-shape parameters are
  empirical and partly correlated with the specimen displacement and the surface-roughness
  parameters.
* The specimen-displacement and lattice-parameter refinements are correlated. The absolute
  lattice parameters could carry a systematic error of a few parts in 10⁴ beyond the quoted e.s.d.s,
  although the agreement with literature values for both phases suggests the calibration is sound.
* Oxygen positions, and therefore bond distances, are weakly determined in both phases because of
  the dominant W scattering; the WO₃ oxygen positions were not refined at all.
