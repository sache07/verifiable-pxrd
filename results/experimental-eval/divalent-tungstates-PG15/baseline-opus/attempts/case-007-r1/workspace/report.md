# Phase analysis of the MgO + WO3 (900 °C) product

**Answer: three crystalline phases — MgWO₄ (wolframite type) 77.8 wt%, γ-WO₃ 15.2 wt%,
MgO (periclase) 7.1 wt%.** The target tungstate has formed but the reaction is incomplete;
both precursors are still present.

| Phase | Formula | Space group | CIF | Weight fraction | σ (stat.) | σ (combined) |
|---|---|---|---|---|---|---|
| MgWO₄ (huanzalaite) | MgWO₄ | *P*2/*c* (13) | `phase_MgWO4.cif` | 0.7777 | 0.0016 | 0.005 |
| γ-WO₃ | WO₃ | *P*2₁/*n* (14) | `phase_WO3.cif` | 0.1518 | 0.0009 | 0.004 |
| MgO (periclase) | MgO | *Fm-3m* (225) | `phase_MgO.cif` | 0.0705 | 0.0016 | 0.005 |

Fractions are normalised over the three modelled crystalline phases (they sum to 1.000).
Fit: **R_wp = 7.99 %, R_p = 5.66 %, R_exp = 2.89 %, GOF = 2.77** (8062 points,
45 refined parameters, 12.5–100.1° 2θ); per-phase R(F²) = 2.4 / 6.5 / 4.0 %.
Files: `final.gpx` (GSAS-II project), `fit.csv` (2θ, y_obs, y_calc, y_diff, y_bkg),
`result.json`, `fit.png`.

## How the phases were identified

The pattern contains close to 100 resolvable maxima between 15.9° and 100°. Indexing against the
MgO–WO₃ chemistry gave an immediate, unambiguous assignment once a **systematic peak shift of
about +0.3° at low angle** was recognised (see "Refinement model" below):

* **MgWO₄** accounts for the five strongest lines — 15.93° (010), 19.24° (100), 24.21° (011),
  30.81°/31.11° (1̄11/111) — and the whole mid-angle envelope. The refined cell,
  *a* = 4.6897, *b* = 5.6740, *c* = 4.9287 Å, β = 90.775°, V = 131.14 Å³, matches the
  published wolframite-type MgWO₄ (4.696/5.683/4.945 Å, 90.83°) to within 0.3 %.
  MgWO₄ is the only binary compound in the MgO–WO₃ system, so no alternative ternary
  candidate needs to be considered.
* **γ-WO₃** accounts for the 23.43/23.94/24.68° triplet (002/020/200) plus 26.91°, 29.22°,
  33.57°, 33.90°, 34.45°, 44.55°, 44.99°, 50.21° … The refined cell,
  7.3031/7.5340/7.6896 Å, β = 90.807°, V = 423.05 Å³, is the textbook room-temperature
  monoclinic γ-WO₃ cell. Other WO₃ polymorphs were tested against the same protocol and are
  excluded: orthorhombic β-WO₃ (*Pnma*) gives R_wp = 10.99 % where γ-WO₃ gives 8.05 % under
  an identical protocol, and triclinic
  δ-WO₃ (*P*-1) fitted worse than the monoclinic model (9.05 % vs 8.81 % at the matched
  intermediate stage) with α and γ refining to only 89.83° and 90.11°, i.e. within ~0.17° of 90°.
  The standard *P*2₁/*n* γ-WO₃ description is therefore reported.
* **MgO** is required by a well-resolved line at 43.21° that neither of the other two phases
  produces (nearest MgWO₄ reflections are at 41.9° and 44.5°; the only γ-WO₃ reflection nearby,
  032, is <2 % of its own maximum). It indexes as MgO 200 with *a* = 4.2122 Å, in essentially
  exact agreement with periclase (4.2117 Å); the 111 (37.2°), 220 (62.6°) and 311 (75.1°) lines
  are also accounted for. Dropping MgO from the model, with everything else identical, raises
  R_wp from 8.05 % to 9.36 % and leaves an obvious unfitted peak at 43.2°. (For reference,
  dropping WO₃ instead gives R_wp = 19.07 %.  These three comparisons were all run with the
  zero-error shift model, whose three-phase baseline is 8.05 %.)

A systematic search of the final difference curve shows **no unexplained Bragg intensity**
anywhere in 12.5–100.1°. Every point where the 11-point-smoothed residual exceeds 1.5 σ falls
into one of two categories, checked against the 585 calculated reflection positions of the
three phases: (i) within 0.18° of a modelled reflection, or (ii) part of the smooth,
asymmetric low-2θ tail of a strong modelled reflection (15.4–15.7° on MgWO₄ 010;
18.6–19.0° on MgWO₄ 100; 32.9–33.4° on WO₃ 022). No residual region contains a local maximum
of its own; the two broadest non-adjacent regions (27.8–28.1°, 43.7–43.8°) are flat
background-level offsets of ~30 counts on an ~800-count background. Three phases is therefore
the complete answer at the sensitivity of this scan — roughly ≥0.5–1 wt% for a well-crystallised
extra phase.

Structural models were taken from the local COD mirror and refined:
MgWO₄ from COD 9013902 (Macavei & Schulz 1993), γ-WO₃ from COD 2311041
(Loopstra & Boldrup 1966, transformed from its *P*2₁/*c*, β = 136.06° setting into the standard
*P*2₁/*n* setting — the transform *x* = −*z*₁, *y* = *y*₁, *z* = *x*₁ − *z*₁ was verified by
reproducing the known *P*2₁/*n* cell and W positions), MgO from COD 9000499 (Hazen 1976).
Refined cation–anion distances are chemically sound: MgWO₄ W–O 1.78–2.12 Å and Mg–O 2.03–2.18 Å
(published 1.78–2.13 / 2.05–2.17 Å), γ-WO₃ W–O 1.71–2.16 Å, MgO Mg–O 2.106 Å.

## Refinement model

Staged refinement in GSAS-II (see `refinement_log` in `result.json` for the R_wp at each stage):
14-term Chebyshev background → specimen displacement → three unit cells → instrumental
Gaussian *W* → per-phase isotropic microstrain and domain size → empirical low-angle intensity
correction → axial-divergence asymmetry (SH/L) → MgWO₄ atomic coordinates.
Cu Kα₁/Kα₂ (1.540598/1.544426 Å, I₂/I₁ = 0.5) as specified in the metadata.

Two instrument-related points had to be settled from the data itself, because the metadata
supplies neither:

* **Peak-position offset.** All three phases require the same systematic shift of ≈ +0.33° at
  15–30° 2θ. This is not a cell effect: with no shift term at all, every refined cell is forced 1–2 % too small.
  Both a constant zero error and a specimen displacement (∝ cos θ) were refined. The
  displacement model is adopted because it fits marginally better (R_wp 7.99 % vs 8.05 %) and,
  decisively, because it returns *a*(MgO) = 4.2122 Å against the periclase value of 4.2117 Å,
  whereas the zero-error model gives 4.2160 Å (+0.1 %, outside the normal range for MgO). Since
  the MgO is unreacted precursor its lattice parameter is a usable internal standard. The
  refined displacement is −544 µm for a 200 mm goniometer radius — a large but credible
  mounting error. Refining both terms together over-corrects (R_wp 8.09 %, *a*(MgO) = 4.2059 Å)
  and is rejected. **Weight fractions are insensitive to this choice** (0.7777/0.1518/0.0705
  with displacement vs 0.7781/0.1519/0.0700 with a zero error).
* **Polarization.** `effective_polarization` is null in the metadata. Fixing the GSAS-II
  `Polariz.` at 0.5 (unpolarized incident beam, i.e. Ni-filtered tube with no monochromator —
  consistent with the Kα₂/Kα₁ = 0.5 that is still present) gives R_wp = 8.21 % at the matched
  stage, versus 8.48 % at 0.7 and 9.03 % at 0.9. 0.5 was therefore adopted. Refining
  polarization freely is degenerate with the low-angle correction below and destabilised
  the MgO profile parameters, so it was not refined.

## Remaining uncertainty and what cannot be determined reliably

1. **Low-angle intensity deficit (the main systematic).** Before any correction, the MgWO₄
   integrated intensities are over-calculated by 10–21 % below ~25° 2θ (obs/calc = 0.83 at
   15.9°, 0.87 at 19.2°, 0.91–0.94 at 24–25°) and under-calculated by 7–11 % between 36° and
   52°, smoothly and monotonically. This is a geometric/instrumental effect in reflection mode
   (beam overflow off the specimen at low angle and/or surface roughness), not a structural one.
   It was absorbed with GSAS-II's Suortti surface-roughness function, which lowers R_wp from
   11.94 % to 8.16 % with two parameters. The refined *A* = −2.29 lies **outside the physical
   0–1 range of the Suortti model**, so this is an empirical correction, not a measured
   roughness; A and B are 99.98 % correlated and individually meaningless. Importantly, the
   weight fractions are almost insensitive to it: without the correction they are
   0.778/0.147/0.076, with it 0.778/0.152/0.071.
2. **Weight-fraction uncertainty.** The statistical esds (0.001–0.002) are optimistic. Across
   every model variant tested (three WO₃ structure models, polarization 0.5/0.7/0.9, zero-error
   vs specimen-displacement peak shift, with/without the low-angle correction, with/without
   preferred orientation, with/without Uiso refinement) the fractions span MgWO₄ 0.775–0.784,
   WO₃ 0.149–0.156, MgO 0.067–0.076. The quoted combined uncertainties (±0.5, ±0.4, ±0.5 abs%)
   reflect that spread.
3. **Microabsorption is not corrected.** MgO (μ ≈ 100 cm⁻¹ at Cu Kα) is a far weaker absorber
   than MgWO₄ (≈ 834 cm⁻¹) and WO₃ (≈ 988 cm⁻¹). With unknown particle sizes no Brindley
   correction could be justified, but the sign is known: **the true MgO content is more likely
   above 7.1 wt% than below.** For μR ≈ 0.2–0.4 (a few µm particles) the MgO fraction could
   plausibly be 1–3 abs% higher, with MgWO₄ correspondingly lower. This is the dominant
   uncertainty on the MgO number, and it is why the bulk Mg:W ratio derived from the fractions
   (1.31) should be treated as a lower-bound-quality estimate rather than a measured
   stoichiometry.
4. **Displacement parameters are not determined.** Uiso values were held at the published
   single-crystal values for every phase. They correlate directly with the empirical low-angle
   correction, so refining them would produce numbers without physical meaning (a test
   refinement did lower R_wp by ~0.2 % but is not reported for that reason).
5. **WO₃ oxygen positions are not determined by these data.** Releasing them changed R_wp by
   <0.01 % while moving some O atoms by >0.1 fractional units — a clear sign of overfitting.
   They are reported at the Loopstra & Boldrup single-crystal values. The W positions, which
   carry essentially all of the scattering power, are well constrained.
6. **Peak shape — the largest remaining misfit.** All strong peaks keep an asymmetric tail on
   their low-2θ flank, extending up to ~0.5°, which the pseudo-Voigt + finite-slit
   (axial-divergence, SH/L = 0.023) model under-reproduces; it is most visible on MgWO₄ 010
   (15.93°) and 100 (19.24°) and on WO₃ 022 (33.57°). Because it affects every phase it is
   instrumental rather than structural, but it was not possible to remove it (refining sample
   transparency gained only 0.03 % in R_wp). The refined per-phase broadening
   (MgWO₄: 0.19 µm domains, 1.75 × 10⁻³ microstrain; WO₃: 6.7 × 10⁻³ microstrain with no
   resolvable size broadening; MgO: 0.26 µm, 0.87 × 10⁻³) should therefore be read as empirical
   profile descriptors, not as microstructural measurements. This residual shape misfit is the
   main reason GOF is 2.77 rather than ~1 — the fit is limited by systematic profile error, not
   by counting statistics or by a missing phase.
7. **Excluded region.** 9.90–12.50° 2θ was left out of the refinement: it contains only the
   steeply rising direct-beam/air-scatter tail and no Bragg peaks. `fit.csv` covers the
   refined range 12.5–100.1°.

## Chemical consistency

From the weight fractions: 54.3 mol% MgWO₄, 12.5 mol% WO₃, 33.2 mol% MgO; 81 % of the tungsten
and 62 % of the magnesium have reacted. The co-existence of both precursors with the product
is self-consistent for an incomplete solid-state reaction at 900 °C. The implied bulk ratio
Mg:W = 1.31 suggests the starting mixture was Mg-rich rather than exactly 1:1 — but, as noted
in point 3, uncorrected microabsorption biases this ratio in the same direction, so it is not
proof of an off-stoichiometric batch.
