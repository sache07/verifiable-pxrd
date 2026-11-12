# Phase analysis of the NiO + WO3 (900 °C) product

**Result: two crystalline phases — wolframite-type NiWO4 (76.0 wt%) and monoclinic γ-WO3
(24.0 wt%). No unreacted NiO is detectable.**

| Phase | Structure type | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---|---|
| NiWO4 | wolframite | *P*2/*c* (13) | a = 4.60101(11), b = 5.66369(15), c = 4.91076(14), β = 89.980(10), V = 127.968(8) Å³ | **75.97 ± 0.11 wt%** (stat.) |
| WO3 (γ) | monoclinic ReO3-derived | *P*2₁/*n* (14) | a = 7.30333(28), b = 7.53483(30), c = 7.69010(30), β = 90.815(4), V = 423.139(33) Å³ | **24.03 ± 0.11 wt%** (stat.) |

Fractions are normalised over the two modelled crystalline phases (they sum to 1 by
construction). Fit: **Rwp = 4.33 %, Rp = 3.38 %, GOF = 1.25, χ² = 1.56**, 8282 points,
44 refined parameters, 10–100° 2θ. Files: `NiWO4.cif`, `WO3.cif`, `fit.csv`,
`result.json`, GSAS-II project `final.gpx`.

## Evidence for the phase identification

Search space: everything that NiO + WO3 can give at 900 °C in air — NiWO4, unreacted NiO,
unreacted WO3 (all polymorphs in the local COD subset: monoclinic γ, triclinic δ,
tetragonal, hexagonal), and reduced tungsten oxides (WO2, W18O49/W10O29, W3O8).
Candidate patterns were simulated and compared with the 126 peaks located in the data.

* **NiWO4** accounts for every strong line that WO3 cannot explain, including the
  strongest peak of the pattern at 30.87° ((111)/(-111), d = 2.889 Å) and the lines at
  19.20° (100), 23.89° (011), 24.84° (110), 31.49° (020), 36.5° (002)/(021), 39.05° (200),
  41.61° (121), 52.27° (130) and 54.57° (221). The refined cell matches published
  wolframite-type NiWO4 (4.599 / 5.661 / 4.907 Å) to <0.1 %.
* **γ-WO3** accounts for the characteristic triplet at 23.04/23.52/24.28° ((002)/(020)/(200))
  and the group at 33.19/33.50/34.00/34.09°, plus 26.53, 28.55/28.84, 41.4/41.8, 49.84 and
  55.85°. Refined cell 7.3033/7.5348/7.6901 Å, β = 90.82° — the textbook room-temperature
  γ-WO3 cell.
* **No unreacted NiO.** Its strongest line (200, 43.3°) and its (111) at 37.3° are absent.
  Adding NiO as a third phase to the converged model refines its weight fraction to
  0.08 ± 0.10 wt% with no change in Rwp (4.7225 → 4.7227 in that test model), i.e.
  indistinguishable from zero. The practical detection limit here is ≈0.3–0.5 wt%, so NiO
  is reported as absent rather than as a trace phase.
* **No reduced tungsten oxides.** The W18O49/W10O29 scale factor was not determinable
  (singular, no Rwp change); their strong lines at 23.5/24.7/32.8° are fully explained by
  the two phases above.
* Residual analysis after convergence shows no unassigned peak anywhere in 10–100° 2θ; all
  remaining residual excursions sit on top of modelled reflections and are peak-shape /
  intensity mismatches of a few percent (see `fit.csv`).

**Implied bulk composition.** 75.97 wt% NiWO4 + 24.03 wt% WO3 = 0.248 mol NiWO4 +
0.104 mol WO3 per 100 g, i.e. W:Ni ≈ 1.42:1. With no Ni-bearing phase other than NiWO4,
the reaction consumed all the NiO and the charge must have been W-rich (NiO:WO3 ≈ 1:1.4),
with the excess WO3 surviving the 900 °C treatment.

## Refinement

GSAS-II (scriptable), Cu Kα1/Kα2 (1.540598/1.544426 Å, I2/I1 = 0.5 from the metadata),
raw counts with σ = √N weighting, 14-term Chebyshev background, pseudo-Voigt peaks with
axial-divergence asymmetry (SH/L = 0.0169(17)), sample displacement 139.5(35) µm (the zero
offset was held at 0 — the two are 99.99 % correlated and cannot both be refined),
effective polarization refined to 0.706(11), isotropic Lorentzian microstrain per phase
(NiWO4 614(151)·10⁻⁶, WO3 1608(173)·10⁻⁶; WO3 peaks are measurably broader).

Structural parameters refined: both cells; Ni1 *y* = 0.6603(4), W1 *y* = 0.17972(14),
Uiso(Ni) = 0.0060(7) Å², Uiso(W) = 0.0065(5) Å² in NiWO4; W1 and W2 *x,y,z* in WO3. The
resulting coordination chemistry is correct: Ni–O = 2.075–2.085 Å (bond-valence sum 1.90 for
Ni²⁺), W–O = 1.77/1.86/2.13 Å in NiWO4 (BVS 6.45) and 1.74–2.18 Å in WO3 (BVS 6.35).

## What is *not* reliably determined

* **Oxygen positions.** They were deliberately held at published values (NiWO4: wolframite
  coordinates, COD 5910277-type; WO3: Loopstra & Boldrini's 1966 neutron refinement,
  COD 2311041, re-expressed in the conventional *P*2₁/*n* cell). Freeing the two NiWO4 O
  sites lowers Rwp from 4.33 to ≈4.09 %, but it drives Ni–O to 1.96–2.04 Å and W–O to
  1.90–2.22 Å, i.e. bond-valence sums of 2.4 for Ni²⁺ and 4.8 for W⁶⁺ — chemically wrong.
  With W dominating the scattering, that apparent improvement is absorption of systematic
  error, not structural information. The O positions in both CIFs are therefore *assumed*,
  not measured.
* **Accuracy of the weight fractions.** The ±0.11 wt% quoted above is the purely
  statistical (counting) esd and is far too optimistic. Across every defensible variant of
  the model tested (background 10–18 terms, zero-offset vs sample-displacement, three WO3
  starting models, instrument-profile vs phase-broadening parameterisation, polarization
  0.5–0.95, with/without preferred orientation, O free or fixed) the WO3 fraction stayed
  within 23.4–25.0 wt%. Including the usual systematic sources (microabsorption, granularity,
  fixed displacement parameters) a realistic figure is **WO3 = 24 ± 2 wt%,
  NiWO4 = 76 ± 2 wt%**. Microabsorption is expected to be mild here because the two phases
  have similar mass absorption coefficients (≈115 vs 139 cm² g⁻¹ at Cu Kα).
* **Any amorphous or non-diffracting fraction is invisible** — no internal standard was
  measured, so these are fractions of the crystalline, modelled material only.
* **Profile and broadening parameters are effective, not physical.** No calibrated
  instrument profile was supplied, so the instrumental U, V, W, X terms, the per-phase
  microstrain and the fixed 1 µm crystallite size are strongly correlated; the microstrain
  values should be read as "WO3 peaks are broader than NiWO4 peaks", not as absolute strain.
  Likewise the refined polarization (0.706) absorbs other smooth angle-dependent intensity
  errors; it was refined because the metadata states the effective polarization is unknown,
  and fixing it at 0.5 instead changes the WO3 fraction only from 24.0 to 23.7 wt%.
* **NiWO4 monoclinic angle.** β refines to 89.980(10)°, i.e. only ≈2σ from 90°; the
  deviation from the ideal 90° should not be considered established by this data set
  (published values scatter around 90.0–90.1°).
* **WO3 polymorph.** γ-WO3 (*P*2₁/*n*) is the correct room-temperature polymorph and fits
  well. A triclinic (δ, *P*-1) description refines to α = 89.89°, γ = 90.08°, i.e.
  metrically monoclinic, and cannot be distinguished from γ-WO3 with these data; a small
  admixture of the triclinic polymorph (commonly present in real WO3 powders) can neither be
  confirmed nor excluded.
