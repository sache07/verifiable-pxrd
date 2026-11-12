# Phase analysis of the WO3 + ZnO product fired at 900 °C

**Result in one line:** the sample is a three-phase mixture of **ZnWO₄ (sanmartinite, 73.4 wt%)**,
**unreacted γ-WO₃ (20.2 wt%)** and **unreacted ZnO (zincite, 6.4 wt%)**; the reaction is therefore
only ≈73 % complete. Final Rietveld fit: **R_wp = 4.73 %, R_p = 3.63 %, GOF = 1.25**
(8301 points, 44 refined parameters).

| phase | formula | space group | CIF | weight fraction |
|---|---|---|---|---|
| sanmartinite | ZnWO₄ | *P*2/*c* (13) | `ZnWO4.cif` | 0.7344(17) |
| γ-WO₃ | WO₃ | *P*2₁/*c* (14) | `WO3.cif` | 0.2021(13) |
| zincite | ZnO | *P*6₃*mc* (186) | `ZnO.cif` | 0.0635(15) |

Fractions are normalised over the three modelled crystalline phases and sum to 1.
Quoted esds are statistical (GSAS-II covariance matrix); see "Remaining uncertainty" for the
larger systematic component.

Files: `fit.csv` (2θ, y_obs, y_calc, y_diff, y_background), `fit.png` (same data plotted),
`result.json`, `final.gpx` (the GSAS-II project that produced all of the above).

---

## 1. How the phases were identified

**Step 1 — major phase.** The strongest reflection (2θ = 30.69°, *d* = 2.911 Å) together with
*d* = 4.673, 3.73, 3.63, 2.84, 2.46 Å indexes immediately on wolframite-type ZnWO₄
(*P*2/*c*, *a* ≈ 4.69, *b* ≈ 5.72, *c* ≈ 4.93 Å, β ≈ 90.6°), the only known binary compound in the
Zn–W–O system and the expected product of WO₃ + ZnO. A ZnWO₄-only Rietveld model reproduces most
of the pattern but leaves R_wp = 14.8 %.

**Step 2 — first residual set.** The difference curve of the ZnWO₄-only fit contains a clean,
self-consistent set of extra peaks at

*d* = 3.825, 3.747, 3.636, 3.334, 3.092, 2.681, 2.614, 1.916, 1.879, 1.820, 1.639 Å.

These index one-to-one on monoclinic γ-WO₃ as (002), (020), (200), (120), (11̄2)/(112),
(022)+(2̄02), (202)+(220), (004), (040), (400)+(140) and (420)+(402) — i.e. the characteristic
23.1°/23.6°/24.4° triplet and the 33.3°/34.2° doublet of the room-temperature WO₃ polymorph.
Adding WO₃ dropped R_wp from 14.8 % to 6.43 %.

**Step 3 — second residual set.** Two residual peaks survived at *d* = 2.814 Å (2θ ≈ 31.8°) and
*d* = 1.625 Å (2θ ≈ 56.6°), plus unexplained intensity near *d* = 2.60 and 2.48 Å. No ZnWO₄ or
WO₃ reflection occurs at 56.6°. These four positions are exactly ZnO (100), (110), (002) and
(101). Adding ZnO dropped R_wp from 6.43 % to 4.73 % and its cell refined to
*a* = 3.2514(4), *c* = 5.2081(5) Å — within 0.05 % of literature zincite (3.2498, 5.2066 Å),
which is strong independent confirmation rather than a numerical artefact.

**Step 4 — completeness.** After the three-phase refinement the difference curve is statistical
noise over the whole 10–100° range (see `fit.png`); no residual peak exceeds ~3 % of the strongest
reflection. Candidate structures were drawn from the local COD-derived library: every Zn–W–O,
W–O and Zn–O entry was enumerated (including the WO₃ polymorphs and the W₁₈O₄₉/W₁₀O₂₉ sub-oxides)
and the chemically plausible candidates were simulated and compared with the residual *d*-spacings.
Nothing beyond the three phases above was required.

**Independent chemical cross-check.** Converting the weight fractions to moles gives
total Zn/total W = **0.97**, i.e. the bulk cation ratio is 1:1 within ~3 %. That is exactly what an
equimolar WO₃ + ZnO charge that reacted only partially must look like, and it is a non-trivial
consistency test: an incorrect identification or badly wrong fractions would not reproduce a 1:1
bulk stoichiometry. 73 % of the W and 75 % of the Zn are bound in ZnWO₄.

## 2. Structural models and refinement

Starting models (local COD mirror):

* ZnWO₄ — COD 1520641 (Dahlborg & Åsberg Svensson, *Acta Chem. Scand.* **53** (1999) 1103).
* WO₃ — COD 2311041 (Loopstra & Boldrini, *Acta Cryst.* **21** (1966) 158; neutron data).
  This is the *P*2₁/*c* setting with β = 136.1°; it is metrically identical to the usual
  *P*2₁/*n* γ-WO₃ cell, for which the refined values correspond to
  *a* = 7.3045, *b* = 7.5383, *c* = 7.6935 Å, β = 90.82° (literature 7.3008, 7.5389, 7.6896 Å, 90.89°).
* ZnO — COD 9004178 (wurtzite type).

Refined quantities (44 parameters): 12-term Chebyshev background, histogram scale, two phase
fractions, sample displacement, Gaussian profile terms *U*, *V*, *W*, axial-divergence *SH/L*,
Suortti surface-roughness *B*, a Lorentzian isotropic size term per phase, the lattice parameters
of all three phases, one overall *U*_iso per phase, and the free positional parameters of ZnWO₄.
The K α₁/K α₂ doublet was modelled with the supplied λ values and I₂/I₁ = 0.5. Minor-phase atomic
coordinates were held at the published values — the WO₃ and ZnO fractions are too small and too
overlapped for their oxygen positions to be determined from these data.

Refined cells:

| phase | *a* (Å) | *b* (Å) | *c* (Å) | β (°) | *V* (Å³) | R(F) (%) | N_refl |
|---|---|---|---|---|---|---|---|
| ZnWO₄ | 4.69248(8) | 5.72051(10) | 4.92809(9) | 90.6349(9) | 132.279(6) | 1.34 | 142 |
| WO₃ | 7.6935(42) | 7.53830(34) | 10.5331(77) | 136.099(8) | 423.59(3) | 1.99 | 439 |
| ZnO | 3.25140(41) | = *a* | 5.20809(49) | — | 47.681(7) | 1.35 | 16 |

Refined ZnWO₄ positions: W (0, 0.18284(12), ¼), Zn (½, 0.68403(29), ¼),
O1 (0.2131(9), 0.1030(8), −0.0627(11)), O2 (0.2488(10), 0.3724(8), 0.3992(11)) — all within
0.01–0.02 fractional units (≈0.05–0.1 Å) of the single-crystal reference, so the wolframite model
is confirmed by, not merely assumed in, the refinement.

Two features of the data required explicit modelling and are worth flagging:

* **Strong suppression of low-angle intensity.** With a flat background and no absorption
  correction the model over-predicts every reflection below ~30° by up to a factor of two.
  A Suortti surface-roughness correction (*SR_A* fixed at 0, *SR_B* = 0.174) accounts for it and
  alone improves R_wp from 9.2 % to 5.3 %. This is the expected micro-absorption/roughness
  signature of a strongly absorbing W-bearing powder measured in reflection.
* **Large sample displacement.** The refined displacement is −0.26 mm (goniometer radius 200 mm),
  consistent with the roughly +0.1–0.15° offset seen in raw peak positions relative to literature
  *d*-spacings. Because displacement (∝ cos θ) and cell expansion (∝ tan θ) have different angular
  dependences they are separable here, and the independent agreement of the ZnO and WO₃ cells with
  literature values shows the separation worked.

## 3. Remaining uncertainty and what is *not* established

* **Weight fractions.** The statistical esds (±0.17, ±0.13, ±0.15 wt% absolute) understate the real
  uncertainty. Re-running the refinement with four different treatments of the displacement
  parameters / roughness correction (these are strongly correlated with the angular intensity
  distribution, which is what fixes the scale factors) moved the results over
  ZnWO₄ 73.4–74.3 wt%, WO₃ 19.0–20.2 wt%, ZnO 6.3–6.7 wt%. A realistic uncertainty is therefore
  **±1 wt% for ZnWO₄ and WO₃ and ±0.3 wt% for ZnO**. The 1:1 bulk Zn:W cross-check is satisfied
  across that whole range.
* **Amorphous / unmodelled content is not quantified.** No internal standard was supplied, so the
  fractions are normalised over the three modelled crystalline phases only, as requested. A glassy
  or X-ray-amorphous component would be absorbed into the Chebyshev background and would make all
  three fractions proportionally too high.
* **ZnWO₄ displacement parameters are not determined.** When freely refined, the overall *U*_iso of
  ZnWO₄ runs to ≈0 or slightly negative because it is strongly correlated with the
  surface-roughness correction. It was fixed at 0.0050 Å² (a physically sensible value, and the
  value it took before the positional parameters were released). The WO₃ and ZnO overall *U*_iso
  refined to plausible 0.0136 and 0.0053 Å². None of these should be interpreted physically.
* **Minor-phase structures are adopted, not determined.** Only the WO₃ and ZnO lattice parameters,
  scale factors and a size-broadening term were refined; their atomic coordinates come from the
  literature. In particular the oxygen sub-lattice of WO₃ — which distinguishes the γ (*P*2₁/*n*)
  polymorph from the closely related triclinic δ-WO₃ — cannot be verified at this phase fraction
  with Cu-Kα lab data. The metric is clearly that of monoclinic γ-WO₃ (the three-peak 23–24.5°
  group is reproduced in both position and relative intensity), but a small admixture of the
  triclinic polymorph, or a slight Zn substitution in WO₃, cannot be excluded.
* **Crystallite sizes should not be used.** The reported per-phase Lorentzian "size" terms
  (0.18, 0.09, 0.15 µm) are completely correlated with the refined Gaussian instrument terms
  (*U*, *V*, *W*), because no calibrated instrument profile was supplied (`metadata.json` lists
  `calibrated_instrument_profile: null`). They are fitting parameters, not a microstructural
  measurement. For the same reason the *U*, *V*, *W* values are empirical and *U*, *V* came out
  negative; the resulting Gaussian FWHM nevertheless stays positive and of a sensible magnitude
  (≈0.16–0.25°, on top of the Lorentzian size term) across the whole measured range.
* **Polarisation and counting statistics.** `effective_polarization` was not supplied; 0.7 was
  assumed (a typical value for this geometry). Point-wise uncertainties were not supplied, so
  σ = √(counts) was used, which makes GOF = 1.25 meaningful as an absolute measure.
* No preferred-orientation correction was applied. The difference curve shows no systematic
  *hkl*-dependent intensity bias and the phase Bragg residuals are only 1.3–2.0 %, so one does not
  appear to be needed; it was not, however, explicitly tested, and a mild texture effect in the
  needle-habit wolframite phase would bias the fractions slightly.

## 4. Reproducing this

`final.gpx` is the self-contained GSAS-II project behind the submitted CIFs, fractions and
`fit.csv`. The scripts that built it are in `work/scripts/` (`produce.py` runs the staged
refinement, `finish.py` the final coordinate polish, `deliver.py` writes the deliverables);
intermediate projects for the 1- and 2-phase comparison models are in `work/out/`.
